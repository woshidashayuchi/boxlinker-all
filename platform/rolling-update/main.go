package main

import (
	"flag"
	"k8s.io/kubernetes/pkg/api"
	"k8s.io/kubernetes/pkg/client/unversioned"
	"k8s.io/kubernetes/pkg/kubectl"
	"k8s.io/kubernetes/pkg/labels"
	"k8s.io/kubernetes/pkg/client/restclient"
	"os"
	"fmt"
	"sync"
	"net/http"
	"time"
	"io"
	"io/ioutil"
	"strings"
	"encoding/json"
	"html/template"
	"k8s.io/kubernetes/pkg/util/intstr"
	"errors"
	log "github.com/Sirupsen/logrus"
	"bytes"
)

const (
	APP_NAME = "rolling-update"
)

func main() {
	fs := flag.NewFlagSet(APP_NAME,flag.ExitOnError)

	debug := fs.Bool("debug",false,"debug")
	listen := fs.String("listen",":8080",`default service port`)
	deploymentKey := fs.String("deployment-key","deployment","Key to use to differentiate between two different controllers.")
	namespace := fs.String("namespace",api.NamespaceDefault,"Namespace the replication controller.")
	k8sEndpoint := fs.String("k8s-endpoint","http://123.56.21.188:8080","k8s api server address.")
	esHost := fs.String("es-host","http://elasticsearch:9200","elasticsearch host url")
	//controllerName := fs.String("controller-name","nginx-demo","controller name")
	dryRun := fs.Bool("dry-run",false,"dry run")
	test := fs.Bool("test",false,"for test")

	if err := fs.Parse(os.Args[1:]); err != nil {
		fmt.Println(os.Stderr,err.Error())
		os.Exit(1)
	}

	fmt.Printf("args: %v\n",os.Args)
	fmt.Printf("debug enable: %v\n",*debug)
	fmt.Printf("test enable: %v\n",*test)
	fmt.Printf("elasticsearch endpoint: %v\n",*esHost)

	if *debug {
		log.SetLevel(log.DebugLevel)
	} else {
		log.SetLevel(log.ErrorLevel)
	}

	if *deploymentKey == "" {
		panic("need deployment-key")
	}

	k := &Krud{
		DeploymentKey: *deploymentKey,
		Namespace: *namespace,
		//ControllerName: *controllerName,
		Endpoint: *k8sEndpoint,
		DryRun: *dryRun,
		Test: *test,
		ESHost: *esHost,
	}

	http.HandleFunc("/",k.push)
	//http.HandleFunc("/view", k.view)
	log.Fatal(k.listen(*listen))
}

type Krud struct {
	DeploymentKey   string
	ControllerName  string
	Namespace 	string
	Endpoint 	string
	Test 		bool
	ESHost 		string

	Hooks 		[]*Webhook
	Next 		chan *Webhook
	Logger 		chan *Logger

	Queues 		map[string] chan *Webhook

	DryRun 		bool

	sync.Mutex
}
type Logger struct {
	Log 		string 			`json:"log"`
	Kubernetes 	map[string]interface{} 	`json:"kubernetes"`
	Timestamp 	string 			`json:"@timestamp"`
}

func (k *Krud) listen(listen string) error {
	k.Next = make(chan *Webhook)
	k.Logger = make(chan *Logger)
	go k.start()
	go k.logger()
	log.Println("Serving on:",listen)
	return http.ListenAndServe(listen,nil)
}

func (k *Krud) sendLog(logger *Logger) {
	b,err := json.Marshal(logger)
	if err != nil {
		log.Errorf("sendLog err: %v",err)
	} else {
		host := fmt.Sprintf("%s/logstash-%s/fluentd?pretty",k.ESHost,time.Now().Format("2006.01.02"))
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
				}
				log.Debugf("send log response: %s", string(body))
			}
		}
	}

}

func (k *Krud) logger(){
	for {
		l := <-k.Logger
		k.sendLog(l)
	}
}

func (k *Krud) start() {
	// TODO 需要为 k.Next 队列分组 , 只要 username/imagename/imagetag 有一个不同就需要分组, 不然会漏掉
	for {
		h := <-k.Next
	Loop:
		for {
			select {
			case c:= <-k.Next:
				if h.Received.Before(c.Received) {
					h = c
				}
			default:
				break Loop
			}
		}
		if err := k.update(h); err != nil {
			//k.Lock()
			log.Errorf("rolling update error: %v",err)
			go func(){
				k.Logger <- getLogger(h,fmt.Sprintf("rolling update error: %v",err))
			}()
			//h.UpdateError = err
			//k.Unlock()
		}
	}
}


var (
	viewFuncs = template.FuncMap{
		"json": func(v interface{}) (string, error) {
			b, err := json.MarshalIndent(v, "", "  ")
			return string(b), err
		},
	}
	viewTemplate = template.Must(template.New("").Funcs(viewFuncs).Parse(indexHTML))
)
func reverse(numbers []*Webhook) []*Webhook {
	newNumbers := make([]*Webhook, len(numbers))
	for i, j := 0, len(numbers)-1; i < j; i, j = i+1, j-1 {
		newNumbers[i], newNumbers[j] = numbers[j], numbers[i]
	}
	return newNumbers
}

func (k *Krud) view(w http.ResponseWriter, r *http.Request) {
	k.Lock()
	defer k.Unlock()
	err := viewTemplate.Execute(w, k)
	if err != nil {
		fmt.Println(err)
		serveError(w, err)
	}
}
func serveError(w http.ResponseWriter,err error) {
	log.Println(err)
	http.Error(w,err.Error(),http.StatusInternalServerError)
}

func parseWebhook(r io.Reader,v interface{}) (kind string, err error) {
	b,err := ioutil.ReadAll(r)
	if err != nil {
		return "", err
	}
	{
		if err := json.Unmarshal(b,&v); err == nil {
			return "DockerRegistry", nil
		}
	}
	return "", fmt.Errorf("unrecognized webhook")

}
func (k *Krud) push(w http.ResponseWriter, r *http.Request) {
	var d = &RegistryWebhook{}
	kind,err := parseWebhook(r.Body,d)
	if err != nil {
		serveError(w,err)
		return
	}
	k.Lock()
	defer k.Unlock()
	for _,event := range d.Events {
		if event.Action == "pull" {
			continue
		}
		if event.Target.MediaType != "application/vnd.docker.distribution.manifest.v2+json" {
			continue
		}
		wh := &Webhook{
			Data: event,
			Kind: kind,
			Source: r.RemoteAddr,
			Received: time.Now(),
		}
		//k.Hooks = append(k.Hooks,wh)
		if k.DryRun {
			b,err := json.MarshalIndent(wh,"","\t")
			if err != nil {
				log.Errorf("parse webhook error: %v",err)
			}
			log.Println(string(b))
		}else {
			go func(){
				k.Next <- wh
			}()
		}
	}

}

type Webhook struct {
	Data 		Event
	Kind 		string
	Source 		string
	Received 	time.Time
	UpdateError 	error
	UpdateAttempt 	bool
	// UpdateSuccess is true if the attempted update was successful.
	UpdateSuccess bool
	UpdateStart 	time.Time
	UpdateEnd 	time.Time
	// UpdateID is the ID of this update, which is what the value of the deployment
	// key is set to.
	UpdateID 	string
	UpdateStatus  	string
	ServiceName 	string
}
type Target struct {
	Repository  string    `json:"repository"`
	Tag 	    string    `json:"tag"`
	MediaType   string    `json:"mediaType"`
	Size        int       `json:"size"`
	Digest      string    `json:"digest"`
	Url         string    `json:"url"`
}

type ImageInfo struct {
	Namespace string `json:"namespace"`
	ImageName string `json:"name"`
	Tag string `json:"tag"`
}

type Request struct {
	Host	string 	`json:"host"`
}

type Event struct {
	Id 	  string    `json:"id"`
	Timestamp string    `json:"timestamp"`
	Action 	  string    `json:"action"`
	Target    Target    `json:"target"`
	Request   Request   `json:"request"`
}

func (e *Event) getImageInfo() (imageInfo *ImageInfo) {
	info := &ImageInfo{}
	info.Tag = e.Target.Tag
	if info.Tag == "" {
		info.Tag = "latest"
	}
	repo := e.Target.Repository
	a := strings.Split(repo,"/")
	if len(a) == 1 {
		info.ImageName = a[0]
	}
	if len(a) == 2 {
		info.Namespace = a[0]
		info.ImageName = a[1]
	}
	return info
}

func (e *Event) getImageURL() (url string) {
	arr := strings.Split(e.Target.Repository,"/")
	host := e.Request.Host
	//host := "index.36ap.com"
	if len(arr) == 1 {
		return host+"/"+arr[0]+":"+e.Target.Tag
	}
	return host+"/"+arr[0]+"/"+arr[1]+":"+e.Target.Tag
}
type RegistryWebhook struct {
	Events []Event `json:"events"`
}

func (k *Krud) update (h *Webhook) error {

	out := &lockBuffer{
		k: k,
		h: h,
	}

	repo := h.Data.Target.Repository
	if h.Data.Action != "push" ||  repo == "" {
		fmt.Sprintf("Warnings: Webhook action %v ignored, repo %v.",h.Data.Action,repo)
		return nil
	} else {
		fmt.Sprintf("Webhook action: %v , data: %v",h.Data.Action,h.Data)

	}
	imageInfo := h.Data.getImageInfo()

	if imageInfo.ImageName == "" || imageInfo.Namespace == "" {
		return errors.New(fmt.Sprintf("no namespace or contrller name: %v",h.Data))
	}

	if imageInfo.ImageName == APP_NAME && imageInfo.Namespace == k.Namespace {
		fmt.Println("ignore update self.")
		return nil
	}

	h.UpdateAttempt = true
	h.UpdateStart = time.Now()
	defer func(){
		h.UpdateEnd = time.Now()
	}()
	var client *unversioned.Client
	var err error
	if k.Test {
		conf := &restclient.Config{
			Host: k.Endpoint,
		}
		client,err = unversioned.New(conf)
	} else {
		client,err = unversioned.NewInCluster()
	}

	if err != nil {
		return err
	}
	rcs := client.ReplicationControllers(imageInfo.Namespace)

	selector := labels.SelectorFromSet(labels.Set{
		"rc-krud": imageInfo.Namespace + "_" +imageInfo.ImageName, // 对于所有版本号的镜像都采取更新措施
	})

	rcList,err := rcs.List(api.ListOptions{
		LabelSelector: selector,
	})
	if err != nil {
		return err
	}
	//fmt.Println(&logInfo{
	//	UserId: imageInfo.Namespace,
	//	LogInfo: "start to rolling update",
	//	Time: time.Now().Format("2016-01-02 15:04:05"),
	//});
	if len(rcList.Items) == 0 {
		return errors.New("can not find rc .")
	}

	//k.Lock()
	//h.UpdateSuccess = err == nil
	//k.Unlock()
	//return nil

	for _, item := range rcList.Items {
		oldRc := &item
		h.ServiceName = oldRc.Name

		go func(){
			k.Logger <- getLogger(h,"Start to rolling update .")
			k.Logger <- getLogger(h,fmt.Sprintf("Use image: %s",h.Data.getImageURL()))
		}()

		log.Debugf("Get rc %s - %s",oldRc.Namespace,oldRc.Name)
		codec := api.Codecs.LegacyCodec(client.APIVersion())
		hash,err := api.HashObject(oldRc,codec)
		if err != nil {
			return err
		}
		newName := fmt.Sprintf("%s-%s", oldRc.Name, hash)
		log.Debugf("ImageURL: %s",h.Data.getImageURL())
		newControllerConfig := &kubectl.NewControllerConfig{
			Namespace: imageInfo.Namespace,
			OldName: oldRc.Name,
			NewName: newName,
			Image:  h.Data.getImageURL(),
			DeploymentKey: k.DeploymentKey,
			PullPolicy: api.PullAlways,
			Container: "",
		}

		newRc, err := kubectl.CreateNewControllerFromCurrentController(client, codec, newControllerConfig)

		if err != nil {
			return err
		}

		oldHash, err := api.HashObject(newRc, codec)
		if err != nil {
			return err
		}
		oldRc, err = kubectl.UpdateExistingReplicationController(client, oldRc, imageInfo.Namespace, newRc.Name, k.DeploymentKey, oldHash, out)
		if err != nil {
			return err
		}

		var hasLabel bool
		//log.Printf("old selector: %v , new selector: %v",oldRc.Spec.Selector,newRc.Spec.Selector)
		for key, oldValue := range oldRc.Spec.Selector {
			if newValue, ok := newRc.Spec.Selector[key]; ok && newValue != oldValue {
				hasLabel = true
				break
			}
		}
		if !hasLabel {
			return fmt.Errorf("must specify a matching key with non-equal value in Selector for %s, selector old: %v, selector new: %v",
				oldRc.Name,oldRc.Spec.Selector,newRc.Spec.Selector)
		}

		h.UpdateID = hash

		ruconf := kubectl.RollingUpdaterConfig{
			Out: out,
			OldRc:          oldRc,
			NewRc:          newRc,
			UpdatePeriod:   time.Second * 3, // todo: change to time.Minute
			Timeout:        time.Minute * 5,
			Interval:       time.Second * 3,
			CleanupPolicy:  kubectl.RenameRollingUpdateCleanupPolicy,
			MaxUnavailable: intstr.FromInt(1),
			MaxSurge: 	intstr.FromInt(1),
		}


		err = kubectl.NewRollingUpdater(imageInfo.Namespace, client).Update(&ruconf)

		if err != nil {
			return err
		}
		go func(){
			k.Logger <- getLogger(h,"Rolling update successfully")
		}()
	}
	return nil
}


func getLogger(h *Webhook, logInfo string) *Logger {
	namespace := h.Data.getImageInfo().Namespace
	ll := map[string]interface{}{
		"time": time.Now().UnixNano() / int64(time.Millisecond),
		"level":"INFO",
		"file":"krud.go",
		"log": map[string]string{
			"userid": namespace,
			"log_info": logInfo,
		},
	}
	b,err := json.Marshal(ll)
	log.Debugf("===> %s",string(b))
	if err != nil {
		log.Debugf("parse log error %v",ll)
	}
	return &Logger{
		Log: string(b),
		Kubernetes: map[string]interface{}{
			"namespace_name":"krud",
			"pod_id":"krud",
			"pod_name":"krud",
			"container_name":"krud",
			"labels":map[string]string{
				"logs":h.ServiceName,
			},
		},
		Timestamp: time.Now().UTC().Format("2006-01-02T15:04:05.000000Z"),
	}
}

type lockBuffer struct {
	k *Krud
	h *Webhook
}

func (l *lockBuffer) Write(p []byte) (n int, err error) {
	//l.k.Lock()
	//defer l.k.Unlock()
	//l.h.UpdateStatus += string(p)
	go func(){
		l.k.Logger <- getLogger(l.h,string(p))
	}()
	return len(p), nil
}

type logInfo struct {
	UserId 		string		`json:"userid"`
	LogInfo 	string		`json:"log_info"`
	Time 		string 		`json:"time"`
}

func (l *logInfo) String() string {
	m, _ := json.Marshal(l)
	return string(m)
}

// todo 优化处理 log 的显示, 应该是需要集成到 log 显示页面
const indexHTML = `<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>krud</title>
	</head>
	<body>
		{{range .Hooks}}
			<div>
				Err: {{.UpdateError}}
				<br>Status: <pre>{{.UpdateStatus}}</pre>
				<br>Value: <pre>{{. | json}}</pre>
			</div>
			<hr>
		{{end}}
	</body>
</html>
`