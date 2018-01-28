package main

import (
	"github.com/codegangsta/cli"
	"github.com/cabernety/boxlinker/platform/building"
	"net/http"
	"strings"
	"github.com/goji/httpauth"
	"github.com/gorilla/mux"
	"github.com/cabernety/boxlinker/platform/building/server"
	"github.com/codegangsta/negroni"
	"net/url"
	"fmt"
	"github.com/cabernety/boxlinker/platform/building/builder"
	"github.com/cabernety/boxlinker/platform/building/builder/docker"
	"github.com/cabernety/boxlinker/platform/building/worker"
	"github.com/jmoiron/sqlx"
	"github.com/cabernety/boxlinker/platform/building/logs"
	"github.com/google/go-github/github"
	"golang.org/x/oauth2"
	"github.com/cabernety/boxlinker/platform/building/logs/es"
	"github.com/cabernety/boxlinker/platform/building/logs/oss"
	log "github.com/Sirupsen/logrus"
)


const logsURLTemplate = "%s/logs/{{.ID}}"

func newDB(c *cli.Context) *sqlx.DB {
	db := sqlx.MustConnect("postgres", c.String("db"))
	if err := building.MigrateUp(db); err != nil {
		panic(err)
	}
	return db
}

func newBuilding(c *cli.Context) *building.Building{
	b := building.New(newDB(c))
	b.BuildQueue = newBuildQueue(c)
	b.Logger = newLogger(c)
	b.GitHub = building.NewGitHub(newGitHubClient(c))
	b.Registry = c.String("registry-host")
	return b
}

func newGitHubClient(c *cli.Context) *github.Client {
	ts := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: c.String("github-token")},
	)
	tc := oauth2.NewClient(oauth2.NoContext, ts)

	return github.NewClient(tc)
}

func newLogger(c *cli.Context) logs.Logger {
	u := urlParse(c.String("logger"))
	log.Infof("Use Logger: %s",u.String())
	switch u.Scheme {
	case "stdout":
		return logs.Stdout
	case "es":
		return es.NewLogger(u.Host)
	case "oss":
		keyId := c.String("oss-access-key-id")
		keySecret := c.String("oss-access-key-secret")
		bucketName := c.String("oss-bucket-name")
		return oss.NewLogger(&oss.LogsConfig{
			Endpoint: u.Host,
			AccessKeyId: keyId,
			AccessKeySecret: keySecret,
			Bucket: bucketName,
		})
	default:
		must(fmt.Errorf("Unknown logger: %v", u.Scheme))
		return nil
	}
}

func newServer(b *building.Building, c *cli.Context) http.Handler {
	var apiAuth func(http.Handler) http.Handler
	if auth := c.String("auth"); auth != "" {
		parts := strings.Split(auth, ":")
		apiAuth = httpauth.SimpleBasicAuth(parts[0],parts[1])
	} else {
		apiAuth = func(h http.Handler) http.Handler { return h }
	}

	r := mux.NewRouter()
	r.NotFoundHandler = server.NewServer(b, server.Config{
		APIAuth: 	apiAuth,
	})

	n := negroni.Classic()
	n.UseHandler(r)

	return n
}

func newBuildQueue(c *cli.Context) building.BuildQueue {
	u := urlParse(c.String("queue"))

	switch u.Scheme {
	case "memory":
		return building.NewBuildQueue(100)
	default:
		must(fmt.Errorf("Unknown queue: %v",u.Scheme))
		return nil
	}
}

func newBuilder(c *cli.Context) builder.Builder {
	db, err := docker.NewBuilderFromEnv()
	if err != nil {
		must(err)
	}
	db.DryRun = c.Bool("dry")
	db.Image = c.String("builder-image")

	g := builder.NewGitHubClient(c.String("github-token"))

	var backend builder.Builder = builder.UpdateGitHubCommitStatus(db, g, fmt.Sprintf(logsURLTemplate, c.String("url")))

	// todo DataDog

	b := worker.NewBuilder(backend)

	return b
}

func urlParse(uri string) *url.URL {
	u, err := url.Parse(uri)
	if err != nil {
		must(err)
	}
	return u
}