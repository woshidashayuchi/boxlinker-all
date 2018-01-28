package github

import (
	"net/http"
	"github.com/cabernety/boxlinker/platform/building"
	"golang.org/x/net/context"
	"github.com/ejholmes/hookshot"
	"io"
	"github.com/ejholmes/hookshot/events"
	"encoding/json"
	"strings"
	"regexp"
	log "github.com/Sirupsen/logrus"
)

type client interface {
	Build(context.Context, building.BuildRequest) (*building.Build, error)
}

type Server struct {
	client
	mux http.Handler
}

func NewServer(b *building.Building) *Server {
	return newServer(b)
}

func newServer(c client) *Server {
	s := &Server{
		client: c,
	}

	g := hookshot.NewRouter()
	g.HandleFunc("ping", s.Ping)
	g.HandleFunc("push", s.Push)
	s.mux = g
	return s
}

func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	s.mux.ServeHTTP(w, r)
}

func (s *Server) Ping(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Ok\n")
}
func (s *Server) Push(w http.ResponseWriter, r *http.Request) {
	ctx := context.TODO()

	var event events.Push
	if err := json.NewDecoder(r.Body).Decode(&event); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if event.Repository.Fork {
		io.WriteString(w, "Not building fork")
		return
	}

	if event.Deleted {
		io.WriteString(w, "Not building deleted branch")
		return
	}

	opts := building.BuildRequest{
		Repository: event.Repository.FullName,
		Branch:     strings.Replace(event.Ref, "refs/heads/", "", -1),
		Sha: 	    event.HeadCommit.ID,
		NoCache:    noCache(event.HeadCommit.Message),
	}

	b, err := s.client.Build(ctx, opts)
	if err != nil {
		log.Errorf("Github Push Build err: %v",err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	io.WriteString(w, b.ID)
}

var noCacheRegexp = regexp.MustCompile(`\[docker nocache\]`)

func noCache(message string) bool {
	return noCacheRegexp.MatchString(message)
}