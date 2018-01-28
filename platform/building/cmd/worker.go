package main

import (
	"github.com/codegangsta/cli"
	"github.com/cabernety/boxlinker/platform/building/builder/docker"
	"github.com/cabernety/boxlinker/platform/building"
	log "github.com/Sirupsen/logrus"
	"github.com/cabernety/boxlinker/platform/building/worker"
	"os"
	"syscall"
	"os/signal"
	"runtime"
)

var workerFlags = []cli.Flag{
	cli.StringFlag{
		Name: "github-token",
		Value: "ecd2d3149554086cc4d025b5f57409a123ff8967",
		Usage: "GitHub API token to use",
		EnvVar: "GITHUB_TOKEN",
	},
	cli.StringFlag{
		Name: "dry",
		Usage: "Enable dry run mode.",
		EnvVar: "DRY",
	},
	cli.StringFlag{
		Name: "builder-image",
		Value: docker.DefaultBuilderImage,
		Usage: "A docker image to use to perform the build.",
		EnvVar: "BUILDER_IMAGE",
	},
	cli.IntFlag{
		Name: "workers",
		Value: runtime.NumCPU(),
		Usage: "Number of workers",
		EnvVar: "WORKERS",
	},
	cli.StringFlag{
		Name:   "stats",
		Value:  "",
		Usage:  "If provided, defines where build metrics are sent. Available options are dogstatsd://<host>",
		EnvVar: "STATS",
	},
}

var cmdWorker = cli.Command{
	Name: "worker",
	Usage: "Run workers.",
	Action: workerAction,
	Flags: append(sharedFlags, workerFlags...),
}

func workerAction(c *cli.Context) {
	b := newBuilding(c)

	if err := runWorker(b, c); err != nil {
		must(err)
	}
}

func runWorker(b *building.Building, c *cli.Context) error {
	numWorkers := c.Int("workers")

	log.Debugf("Starting %d workers",numWorkers)

	ch := make(chan building.BuildContext)
	b.BuildQueue.Subscribe(ch)

	workers := worker.NewPool(b, numWorkers, worker.Options{
		Builder: newBuilder(c),
		BuildRequests: ch,
	})

	workers.Start()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
	sig := <-quit
	log.Infof("Signal %d received. Shutting down workers.", sig)
	return workers.Shutdown()
}