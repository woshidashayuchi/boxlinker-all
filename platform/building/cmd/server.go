package main

import (
	"github.com/codegangsta/cli"
	"github.com/cabernety/boxlinker/platform/building"
	"os"
	"os/signal"
	"syscall"
	log "github.com/Sirupsen/logrus"
	"net/http"
)

var serverFlags = []cli.Flag{
	cli.StringFlag{
		Name: "port",
		Value: "8080",
		Usage: "服务运行端口",
		EnvVar: "PORT",
	},
	cli.StringFlag{
		Name: "auth",
		Value: "",
		Usage: "API 校验, user:pass",
		EnvVar: "BASIC_AUTH",
	},
}

var cmdServer = cli.Command{
	Name: "server",
	Usage: "运行服务",
	Action: serverAction,
	Flags: append(sharedFlags, serverFlags...),
}

func serverAction(c *cli.Context){
	b := newBuilding(c)
	runServer(b,c)
}

func runServer(b *building.Building, c *cli.Context) error {
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)

	port := c.String("port")
	log.Infof("Starting server on %s", port)

	errCh := make(chan error)
	go func(){
		errCh <- http.ListenAndServe(":"+port, newServer(b, c))
	}()

	select {
	case err := <-errCh:
		return err
	case <-quit:
		return nil
	}
}


