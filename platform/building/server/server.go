package server

import (
	"net/http"
	"github.com/cabernety/boxlinker/platform/building"
	"github.com/cabernety/boxlinker/platform/building/server/api"
	"github.com/gorilla/mux"
	"github.com/ejholmes/hookshot"
	"github.com/cabernety/boxlinker/platform/building/server/github"
)

type Config struct {
	APIAuth func(http.Handler) http.Handler

	GitHubSecret string
}

func NewServer(b *building.Building, config Config) http.Handler {
	r := mux.NewRouter()

	r.MatcherFunc(githubWebhook).Handler(
		hookshot.Authorize(github.NewServer(b), config.GitHubSecret),
	)

	r.NotFoundHandler = api.NewServer(b,config.APIAuth)

	return r
}

func githubWebhook(r *http.Request, _ *mux.RouteMatch) bool {
	h := r.Header[http.CanonicalHeaderKey("X-GitHub-Event")]
	return len(h) > 0
}
