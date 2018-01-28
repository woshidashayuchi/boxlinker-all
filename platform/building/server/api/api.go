package api

import (
	"golang.org/x/net/context"
	"io"
	"net/http"
	"github.com/cabernety/boxlinker/platform/building"
	"github.com/gorilla/mux"
	schema "github.com/cabernety/boxlinker/platform/building/client/building"
	"encoding/json"
	"database/sql"
	"fmt"
	"github.com/remind101/pkg/stream"
	streamhttp "github.com/remind101/pkg/stream/http"
	"time"
)

type client interface {
	Logs(context.Context, string) (io.Reader, error)
	Build(context.Context, building.BuildRequest) (*building.Build, error)
	FindBuild(context.Context, string) (*building.Build, error)
	FindArtifact(context.Context, string) (*building.Artifact, error)
}

type Server struct {
	client
	mux http.Handler
}

func NewServer(b *building.Building, auth func(http.Handler) http.Handler) *Server {
	return newServer(b, auth)
}

func newServer(c client, auth func(http.Handler) http.Handler) *Server {
	s := &Server{
		client: c,
	}

	authFunc := func(h http.HandlerFunc) http.Handler {
		return auth(http.HandlerFunc(h))
	}

	r := mux.NewRouter()


	/**
	* @api {post} /builds 生成自动构建
	* @apiName BuildCreate
	* @apiGroup AutoBuild
	* @apiVersion 1.0.0
	*
	* @apiParam {String} branch git项目分支
	* @apiParam {String} repository git项目名称, p.s. user/repo
	* @apiParam {String} sha git commit sha, optional
	*
	* @apiSuccess {String} id build id
	* @apiSuccess {String} repository git repo name, "user/repo"
	* @apiSuccess {String} branch git branch
	* @apiSuccess {String} sha git commit sha
	* @apiSuccess {String} state 构建状态, 可能的值 pending|building|failed|succeeded
	* @apiSuccess {String} createdAt 创建时间
	* @apiSuccess {String} startedAt 开始时间
	* @apiSuccess {String} completedAt 完成时间
	*/
	r.Handle("/builds", authFunc(s.BuildCreate)).Methods("POST")
	r.Handle("/builds/{owner}/{repo}@{sha}", authFunc(s.BuildInfo)).Methods("GET")

	/**
	* @api {post} /builds/:id 获取 build 流程详细信息
	* @apiName BuildInfo
	* @apiGroup AutoBuild
	* @apiVersion 1.0.0
	*
	* @apiParam {String} id build id
	*
	* @apiSuccess {String} id build id
	* @apiSuccess {String} repository git repo name, "user/repo"
	* @apiSuccess {String} branch git branch
	* @apiSuccess {String} sha git commit sha
	* @apiSuccess {String} state 构建状态, 可能的值 pending | building | failed | succeeded
	* @apiSuccess {String} createdAt 创建时间
	* @apiSuccess {String} startedAt 开始时间
	* @apiSuccess {String} completedAt 完成时间
	*/
	r.Handle("/builds/{id}", authFunc(s.BuildInfo)).Methods("GET")

	r.Handle("/artifacts/{owner}/{repo}@{sha}", authFunc(s.ArtifactInfo)).Methods("GET")
	r.Handle("/artifacts/{id}", authFunc(s.ArtifactInfo)).Methods("GET")

	/**
	* @api {post} /logs/:id 获取 build 流程日志
	* @apiName BuildInfo
	* @apiGroup AutoBuild
	* @apiDescription 这是一个 long polling 接口
	* @apiVersion 1.0.0
	*
	* @apiParam {String} id build id
	*
	*/
	r.HandleFunc("/logs/{id}", s.LogsStream).Methods("GET")

	s.mux = r

	return s
}

func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request){
	s.mux.ServeHTTP(w,r)
}

// LogsStream is an http.HandlerFunc that will stream the logs for a build.
func (s *Server) LogsStream(rw http.ResponseWriter, req *http.Request) {
	ctx := context.TODO()

	vars := mux.Vars(req)

	// Get a handle to an io.Reader to stream the logs from.
	r, err := s.client.Logs(ctx, vars["id"])
	if err != nil {
		http.Error(rw, err.Error(), http.StatusBadRequest)
		return
	}

	rw.Header().Set("Content-Type", "text/plain")

	// Chrome won't show data if we don't set this. See
	// http://stackoverflow.com/questions/26164705/chrome-not-handling-chunked-responses-like-firefox-safari.
	rw.Header().Set("X-Content-Type-Options", "nosniff")

	w := streamhttp.StreamingResponseWriter(rw)
	defer close(stream.Heartbeat(w, time.Second*25)) // Send a null character every 25 seconds.

	// Copy the log stream to the client.
	_, err = io.Copy(w, r)
	if err != nil {
		fmt.Fprintf(w, "error: %v", err)
	}
}

func newBuild(b *building.Build) schema.Build {
	return schema.Build{
		ID:          b.ID,
		Repository:  b.Repository,
		Branch:      b.Branch,
		Sha:         b.Sha,
		State:       b.State.String(),
		CreatedAt:   b.CreatedAt,
		StartedAt:   b.StartedAt,
		CompletedAt: b.CompletedAt,
	}
}

func (s *Server) BuildCreate(w http.ResponseWriter, r *http.Request){
	ctx := context.TODO()

	var req schema.BuildCreateOpts
	if err := decode(r.Body, &req); err != nil {
		encodeErr(w, err)
		return
	}

	if req.Repository == "" {
		http.Error(w, "repository is null", http.StatusBadRequest)
		return
	}

	if req.Branch == "" {
		req.Branch = "master"
	}

	b, err := s.client.Build(ctx, building.BuildRequest{
		Repository: 	req.Repository,
		Branch:  	req.Branch,
		Sha: 		req.Sha,
	})
	if err != nil {
		encodeErr(w, err)
		return
	}

	encode(w, newBuild(b))
}

// BuildInfo returns a Build.
func (s *Server) BuildInfo(w http.ResponseWriter, r *http.Request) {
	ctx := context.TODO()

	ident := identity(mux.Vars(r))

	b, err := s.client.FindBuild(ctx, ident)
	if err != nil {
		encodeErr(w, err)
		return
	}

	encode(w, newBuild(b))
}


func newArtifact(a *building.Artifact) schema.Artifact {
	artifact := schema.Artifact{
		ID:    a.ID,
		Image: a.Image,
	}
	artifact.Build.ID = a.BuildID
	return artifact
}

// ArtifactInfo returns an Artifact.
func (s *Server) ArtifactInfo(w http.ResponseWriter, r *http.Request) {
	ctx := context.TODO()

	ident := identity(mux.Vars(r))

	a, err := s.client.FindArtifact(ctx, ident)
	if err != nil {
		encodeErr(w, err)
		return
	}

	encode(w, newArtifact(a))
	return
}

func identity(vars map[string]string) string {
	if id := vars["id"]; id != "" {
		return id
	}

	return fmt.Sprintf("%s/%s@%s", vars["owner"], vars["repo"], vars["sha"])
}

func decode(r io.Reader, v interface{}) error {
	return json.NewDecoder(r).Decode(v)
}
func encode(w io.Writer, v interface{}) error {
	return json.NewEncoder(w).Encode(v)
}

func encodeErr(w http.ResponseWriter, e error) error {
	err := newError(e)

	switch err {
	case schema.ErrNotFound:
		w.WriteHeader(http.StatusNotFound)
	default:
		w.WriteHeader(http.StatusInternalServerError)
	}

	return encode(w, err)
}


func newError(err error) *schema.Error {
	if err == sql.ErrNoRows {
		return schema.ErrNotFound
	}

	return &schema.Error{
		ID:      "internal_error",
		Message: err.Error(),
	}
}
