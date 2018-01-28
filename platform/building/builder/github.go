package builder

import (
	"github.com/google/go-github/github"
	"golang.org/x/oauth2"
	log "github.com/Sirupsen/logrus"
)

type GitHubClient interface {
	CreateStatus(owner, repo, ref string, status *github.RepoStatus) (*github.RepoStatus, *github.Response, error)
}

func NewGitHubClient(token string) GitHubClient {
	if token == "" {
		return &nullGitHubClient{}
	}
	log.Debugf("New GitHub client use token: %s",token)
	ts := oauth2.StaticTokenSource(&oauth2.Token{AccessToken: token})
	tc := oauth2.NewClient(oauth2.NoContext, ts)
	return github.NewClient(tc).Repositories
}

type nullGitHubClient struct {}

func (c *nullGitHubClient) CreateStatus(owner, repo, ref string, status *github.RepoStatus) (*github.RepoStatus, *github.Response, error) {
	return nil, nil, nil
}