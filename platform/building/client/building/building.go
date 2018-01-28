package building

import (
	"net/http"
	"io"
	"bytes"
	"reflect"
	"encoding/json"
	"github.com/google/go-querystring/query"
	"fmt"
	"runtime"
	"time"
)

const (
	Version 	 = ""
	DefaultURL 	 = "http://localhost:8080"
	DefaultUserAgent = "building/" + Version + " (" + runtime.GOOS + "; " + runtime.GOARCH + ")"
)

type Service struct {
	client *http.Client
	URL 	string
}

func NewService(c *http.Client) *Service {
	if c == nil {
		c = http.DefaultClient
	}

	return &Service{
		client: c,
		URL: 	DefaultURL,
	}
}

func (s *Service) NewRequest(method, path string, body interface{}, q interface{}) (*http.Request, error) {
	var ctype string
	var rbody io.Reader
	switch t := body.(type) {
	case nil:
	case string:
		rbody = bytes.NewBufferString(t)
	case io.Reader:
		rbody = t
	default:
		v := reflect.ValueOf(body)
		if !v.IsValid() {
			break
		}
		if v.Type().Kind() == reflect.Ptr {
			v = reflect.Indirect(v)
			if !v.IsValid() {
				break
			}
		}
		j, err := json.Marshal(body)
		if err != nil {
			return nil, err
		}
		rbody = bytes.NewReader(j)
		ctype = "application/json"
	}
	req, err := http.NewRequest(method, s.URL+path, rbody)
	if err != nil {
		return nil, err
	}
	if q != nil {
		v, err := query.Values(q)
		if err != nil {
			return nil, err
		}
		query := v.Encode()
		if req.URL.RawQuery != "" && query != "" {
			req.URL.RawQuery += "&"
		}
		req.URL.RawQuery += query
	}
	req.Header.Set("Accept", "application/json")
	req.Header.Set("User-Agent", DefaultUserAgent)
	if ctype != "" {
		req.Header.Set("Conttent-Type", ctype)
	}
	return req, nil
}

func (s *Service) Do(v interface{}, method, path string, body interface{}, q interface{}, lr *ListRange) error {
	req, err := s.NewRequest(method, path, body, q)
	if err != nil {
		return err
	}
	if lr != nil {
		lr.SetHeader(req)
	}
	resp, err := s.client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	switch t := v.(type) {
	case nil:
	case io.Writer:
		_, err = io.Copy(t, resp.Body)
	default:
		err = json.NewDecoder(resp.Body).Decode(v)
	}
	return err
}


// Get sends a GET request and decodes the response into v.
func (s *Service) Get(v interface{}, path string, query interface{}, lr *ListRange) error {
	return s.Do(v, "GET", path, nil, query, lr)
}

// Patch sends a Path request and decodes the response into v.
func (s *Service) Patch(v interface{}, path string, body interface{}) error {
	return s.Do(v, "PATCH", path, body, nil, nil)
}

// Post sends a POST request and decodes the response into v.
func (s *Service) Post(v interface{}, path string, body interface{}) error {
	return s.Do(v, "POST", path, body, nil, nil)
}

// Put sends a PUT request and decodes the response into v.
func (s *Service) Put(v interface{}, path string, body interface{}) error {
	return s.Do(v, "PUT", path, body, nil, nil)
}

// Delete sends a DELETE request.
func (s *Service) Delete(v interface{}, path string) error {
	return s.Do(v, "DELETE", path, nil, nil, nil)
}

type ListRange struct {
	Field 		string
	Max 		int
	Descending 	bool
	FirstID 	string
	LastID 		string
}

func (lr *ListRange) SetHeader(req *http.Request) {
	var hdrval string
	if lr.Field != "" {
		hdrval += lr.Field + " "
	}
	hdrval += lr.FirstID + ".." + lr.LastID
	if lr.Max != 0 {
		hdrval += fmt.Sprintf("; max=%d",lr.Max)
		if lr.Descending {
			hdrval += ", "
		}
	}
	if lr.Descending {
		hdrval += ", order=desc"
	}
	req.Header.Set("Range", hdrval)
	return
}

// An artifact is the result of a successful build. It represents a
// built Docker image and will tell what what you need to pull to obtain
// the image.
type Artifact struct {
	Build struct {
		      ID string `json:"id" url:"id,key"` // unique identifier of build
	      } `json:"build" url:"build,key"`
	ID    string `json:"id" url:"id,key"`       // unique identifier of artifact
	Image string `json:"image" url:"image,key"` // the name of the Docker image. This can be pulled with `docker pull`
}

func (s *Service) ArtifactInfo(artifactIdentity string) (*Artifact, error) {
	var artifact Artifact
	return &artifact, s.Get(&artifact, fmt.Sprintf("/artifacts/%v", artifactIdentity), nil, nil)
}

// A build represents a request to build a git commit for a repo.
type Build struct {
	Branch string `json:"branch" url:"branch,key"` // the branch within the GitHub repository that the build was triggered
						       // from
	CompletedAt *time.Time `json:"completed_at" url:"completed_at,key"` // when the build moved to the `"succeeded"` or `"failed"` state
	CreatedAt   *time.Time  `json:"created_at" url:"created_at,key"`     // when the build was created
	ID          string     `json:"id" url:"id,key"`                     // unique identifier of build
	Repository  string     `json:"repository" url:"repository,key"`     // the GitHub repository that this build is for
	Sha         string     `json:"sha" url:"sha,key"`                   // the git commit to build
	StartedAt   *time.Time `json:"started_at" url:"started_at,key"`     // when the build moved to the `"building"` state
	State       string     `json:"state" url:"state,key"`               // the current state of the build
}
type BuildCreateOpts struct {
	Branch string `json:"branch,omitempty" url:"branch,omitempty,key"` // the branch within the GitHub repository that the build was triggered
									    // from
	Repository string  `json:"repository" url:"repository,key"`       // the GitHub repository that this build is for
	Sha        string `json:"sha,omitempty" url:"sha,omitempty,key"` // the git commit to build
}
// Defines the format that errors are returned in
type Error struct {
	ID      string `json:"id" url:"id,key"`           // unique identifier of error
	Message string `json:"message" url:"message,key"` // human readable message
}


