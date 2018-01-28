package oss

import (
	"github.com/aliyun/aliyun-oss-go-sdk/oss"
	osslog "github.com/cabernety/boxlinker/platform/building/oss"
	log "github.com/Sirupsen/logrus"
	"io"
)

//type Logs struct {
//	bucket 	*oss.Bucket
//}

type LogsConfig struct {
	Endpoint 	string
	AccessKeyId 	string
	AccessKeySecret string
	Bucket  	string
}

type Group struct {
	*osslog.Group
}

func NewLogger(config *LogsConfig) *Group {
	c, err := oss.New(config.Endpoint, config.AccessKeyId, config.AccessKeySecret)
	if err != nil {
		log.Fatalf("Get oss err: %v",err)
		return nil
	}
	log.Infof("OSS logger config - Endpoint: %s, AccessKeyId: %s, AccessKeySecret: %s",
		config.Endpoint, config.AccessKeyId, config.AccessKeySecret)
	bucket, err := c.Bucket(config.Bucket)
	if err != nil {
		log.Fatalf("Get Bucket err: %v",err)
		return nil
	}
	return &Group{
		osslog.NewGroup(bucket),
	}
}

func (l *Group) Create(buildID string) (io.Writer, error) {
	w, err := l.Group.Create(buildID)
	if err != nil {
		return w, err
	}
	log.Debugf("OSS create logger stream: %s",buildID)
	return &writer{w.(io.WriteCloser)}, nil
}

func (l *Group) Open(buildID string) (io.Reader, error) {
	r, err := l.Group.Open(buildID)
	if err != nil {
		return r, err
	}
	return &reader{r.(io.ReadCloser),false}, nil
}

const endOfText = '\x03'

type writer struct {
	io.WriteCloser
}

func (w *writer) Close() error {
	_, err := w.Write([]byte{endOfText})
	if err != nil {
		return err
	}
	return w.WriteCloser.Close()
}

type reader struct {
	io.ReadCloser
	closed bool
}

func (r *reader) Read(b []byte) (int, error) {
	if r.closed == true {
		return 0, io.EOF
	}

	n,err := r.ReadCloser.Read(b)
	if err != nil {
		return n, err
	}

	if n > 0 &&b[n-1] == endOfText {
		r.closed = true
		r.ReadCloser.Close()
		return n, io.EOF
	}

	return n, nil

}