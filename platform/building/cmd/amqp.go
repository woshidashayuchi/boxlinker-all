package main

import (
	"github.com/codegangsta/cli"
	"github.com/cabernety/boxlinker/platform/building"
	"fmt"
	log "github.com/Sirupsen/logrus"
	"github.com/streadway/amqp"
	"errors"
	"os"
	"syscall"
	"os/signal"
	"github.com/ejholmes/hookshot/events"
	"regexp"
	"strings"
	"golang.org/x/net/context"
	"encoding/json"
	"bytes"
)

var amqpFlags = []cli.Flag{
	cli.StringFlag{
		Name: "rabbitmq-host",
		Value: "boxlinker.com",
		Usage: "消息队列 hostname",
		EnvVar: "RABBITMQ_HOST",
	},
	cli.StringFlag{
		Name: "rabbitmq-port",
		Value: "30001",
		Usage: "消息队列 port",
		EnvVar: "RABBITMQ_PORT",
	},
	cli.StringFlag{
		Name: "rabbitmq-exchange-name",
		Value: "boxlinker_building_2",
		Usage: "消息队列订阅的名称",
		EnvVar: "RABBITMQ_EXCHANGE_NAME",
	},


}

var cmdAmqp = cli.Command{
	Name: "amqp",
	Usage: "start amqp receiver",
	Action: amqpAction,
	Flags: append(sharedFlags, amqpFlags...),
}

func amqpAction(c *cli.Context){
	b := newBuilding(c)

	runAmqp(b,c)
}

func runAmqp(b *building.Building, c *cli.Context) error {
	host := c.String("rabbitmq-host")
	port := c.Int("rabbitmq-port")
	exchangeName := c.String("rabbitmq-exchange-name")

	if exchangeName == "" {
		log.Error("no rabbitmq exchange name found")
		return errors.New("no rabbitmq exchange name found")
	}

	log.Infof("Starting amqp on %s:%d",host,port)

	conn,err := amqp.Dial(fmt.Sprintf("amqp://%s:%d",host,port))
	if err != nil {
		log.Error("connect to rabbitmq failed: %v",err)
		return err
	}
	defer conn.Close()

	ch,err := conn.Channel()
	if err != nil {
		log.Error("fail to open a channel: %v",err)
		return err
	}
	defer ch.Close()

	err1 := ch.ExchangeDeclare(
		exchangeName,   // name
		"fanout", // type
		false,     // durable
		false,    // auto-deleted
		false,    // internal
		false,    // no-wait
		nil,      // arguments
	)
	if err1 != nil {
		log.Error("fail to create exchange: %v",err1)
		return err1
	}

	q, err := ch.QueueDeclare(
		"",    // name
		false, // durable
		false, // delete when usused
		true,  // exclusive
		false, // no-wait
		nil,   // arguments
	)
	if err != nil {
		log.Error("fail to declare queue: %v",err)
		return err
	}

	err2 := ch.QueueBind(
		q.Name, // queue name
		"",     // routing key
		exchangeName, // exchange
		false,
		nil,
	)
	if err2 != nil {
		log.Error("fail to bind queue: %v",err2)
		return err2
	}

	msgs,err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	if err != nil {
		log.Error("fail to register a consumer: %v",err)
		return err
	}

	go func() {
		for d := range msgs {
			var event events.Push
			if err := json.NewDecoder(bytes.NewReader(d.Body)).Decode(&event); err != nil {
				log.Errorf("Received a message but bad request")
				continue
			}
			if event.Repository.Fork {
				log.Errorf("No building for fork")
				continue
			}
			if event.Deleted {
				log.Errorf("No building for deleted branch")
				continue
			}
			opts := building.BuildRequest{
				Repository: event.Repository.FullName,
				Branch:     strings.Replace(event.Ref, "refs/heads/", "", -1),
				Sha: 	    event.HeadCommit.ID,
				NoCache:    noCache(event.HeadCommit.Message),
			}
			ctx := context.TODO()
			build, err := b.Build(ctx, opts)
			if err != nil {
				log.Errorf("Building error: %v",err)
				continue
			}
			log.Infof("Building: %s",build.ID)
		}
	}()
	log.Infof(" [*] Waiting for messages. To exit press CTRL+C")

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)


	select {
	case <-quit:
		return nil
	}
}

var noCacheRegexp = regexp.MustCompile(`\[docker nocache\]`)

func noCache(message string) bool {
	return noCacheRegexp.MatchString(message)
}