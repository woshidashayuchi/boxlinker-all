package main

import (
	"github.com/codegangsta/cli"
	log "github.com/Sirupsen/logrus"
	"os"
	"fmt"
)

var sharedFlags = []cli.Flag{
	cli.StringFlag{
		Name:	"queue",
		Value:	"memory://",
		Usage: 	"构建队列,默认内存队列",
		EnvVar: "QUEUE",
	},
	cli.StringFlag{
		Name: 	"logger-url",
		Value: 	"stdout://",
		Usage: 	"日志输入地址,默认 stdout",
		EnvVar: "LOGGER_URL",
	},
	cli.StringFlag{
		Name:   "url",
		Value:  "http://boxlinker.com",
		Usage:  "Canonical URL for this instance. Used when adding webhooks to repos.",
		EnvVar: "BASE_URL",
	},
	cli.StringFlag{
		Name:   "logger",
		Value:  "stdout://",
		Usage:  "The logger to use. Available options are `stdout://`, `oss://oss_url`, `es://es_url`, `s3://bucket` or `cloudwatch://`.",
		EnvVar: "LOGGER",
	},
	cli.StringFlag{
		Name: "oss-access-key-id",
		Value: "LTAIRgaFkdGaZlVM",
		Usage: "oss access key id",
		EnvVar: "OSS_ACCESS_KEY_ID",
	},
	cli.StringFlag{
		Name: "oss-access-key-secret",
		Value: "EGv0wHzPE5cv97INkIQ4vYdqyYzxnH",
		Usage: "oss access key secret",
		EnvVar: "OSS_ACCESS_KEY_SECRET",
	},
	cli.StringFlag{
		Name: "oss-bucket-name",
		Value: "boxlinker-logs",
		Usage: "oss bucket name",
		EnvVar: "OSS_BUCKET_NAME",
	},
	cli.StringFlag{
		Name: 	"db",
		Value: 	"postgres://postgres:postgres@127.0.0.1/postgres?sslmode=disable",
		Usage: 	"postgres 数据库地址",
		EnvVar: "DATABASE_URL",
	},
	cli.StringFlag{
		Name: 	"registry-host",
		Value: 	"index.boxlinker.com",
		Usage: 	"需要推送的镜像库地址",
		EnvVar: "REGISTRY_HOST",
	},
	cli.BoolFlag{
		Name: 	"debug, D",
		Usage: 	"debug mode",
	},

}

func main(){
	app := cli.NewApp()
	app.Name = "boxlinker image builder"
	app.Usage = "根据 Github 项目构建镜像"
	app.Action = mainAction
	app.Before = func(c *cli.Context) error {
		if c.GlobalBool("debug") {
			log.SetLevel(log.DebugLevel)
		}
		return nil
	}
	app.Flags = append(
		sharedFlags,
		append(workerFlags,serverFlags...)...,
		//append(amqpFlags,append(workerFlags,serverFlags...)...)...,
	)

	app.Commands = []cli.Command{
		cmdServer,
		//cmdAmqp,
		cmdWorker,
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}

func mainAction(c *cli.Context){
	b := newBuilding(c)

	server := make(chan error)
	//amqp := make(chan error)
	worker := make(chan error)

	go func(){
		server <- runServer(b, c)
	}()
	//go func(){
	//	amqp <- runAmqp(b,c)
	//}()

	go func(){
		worker <- runWorker(b, c)
	}()
	var err error
	if err = <-server; err != nil {
		log.Errorf("server err: %v",err)
	}
	//if err = <-amqp; err != nil {
	//	log.Errorf("amqp err: %v",err)
	//}
	if err = <-worker; err != nil {
		log.Errorf("server err: %v",err)
	}
}


func must(err error){
	if err != nil {
		fmt.Fprintf(os.Stderr, "%v\n", err)
		os.Exit(1)
	}
}