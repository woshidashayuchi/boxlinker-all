package es

import (
	"io"
	"errors"
	"time"
	"fmt"
	log "github.com/Sirupsen/logrus"
	"bytes"
	"encoding/json"
	"net/http"
	"io/ioutil"
)


type Logs struct {
	Host 	string
	Queue 	chan *Logger
}

func NewLogger(host string) *Logs {
	l := &Logs{
		Host: host,
		Queue: make(chan *Logger),
	}
	go l.start()
	return l
}

func (l *Logs) Create(name string) (io.Writer, error) {
	return &writer{
		logs: l,
		name: name,
	}, nil
}

func (l *Logs) start() {
	for {
		log := <-l.Queue
		l.sendLog(log)
	}
}

func (l *Logs) sendLog(logger *Logger){
	b,err := json.Marshal(logger)
	if err != nil {
		log.Errorf("sendLog err: %v",err)
	} else {
		host := fmt.Sprintf("http://%s/logstash-%s/fluentd?pretty",l.Host,time.Now().Format("2006.01.02"))
		log.Debugf("send log to %s: %s",host,string(b))
		req,err := http.NewRequest("POST",host,bytes.NewBuffer(b))
		if err != nil {
			log.Errorf("make request error: %v",err)
		} else {
			client := &http.Client{}
			res,err := client.Do(req)
			defer res.Body.Close()
			if err != nil {
				log.Errorf("send log reponse error: %v",err)
			} else {
				body,err := ioutil.ReadAll(res.Body)
				if err != nil {
					log.Errorf("send log read response body error: %v",err)
				} else {
					log.Debugf("resp: %s",string(body))
					fmt.Print(logger.Log)
				}
			}
		}
	}
}

func (l *Logs) Open(name string) (io.Reader, error) {
	return nil, errors.New("es logs: read is not implemented yet.")
}

type writer struct {
	io.WriteCloser
	logs *Logs
	name string
}

func (w *writer) Write(p []byte) (int, error) {
	w.logs.Queue <- &Logger{
		Log: string(p),
		Kubernetes: map[string]interface{}{
			"namespace_name":"boxlinker",
			"pod_id":fmt.Sprintf("boxlinker_building_%s",w.name),
			"pod_name":fmt.Sprintf("boxlinker_building_%s",w.name),
			"container_name":fmt.Sprintf("boxlinker_building_%s",w.name),
			"labels":map[string]string{
				"logs":w.name,
			},
		},
		Timestamp: time.Now().UTC().Format("2006-01-02T15:04:05.000000Z"),
	}
	return len(string(p)), nil
}

func (w *writer) Close() error {
	return nil
}