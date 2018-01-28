package oss

import (
	"github.com/aliyun/aliyun-oss-go-sdk/oss"
	"time"
	"sync"
	"bytes"
	"io/ioutil"
	log "github.com/Sirupsen/logrus"
	"strconv"
)

type Reader struct {
	stream string
	bucket *oss.Bucket
	pos int64
	throttle <-chan time.Time
	b lockingBuffer
	closed bool
	err error
}

func NewReader(stream string, bucket *oss.Bucket) *Reader {
	return newReader(stream, bucket)
}

func newReader(stream string, bucket *oss.Bucket) *Reader {
	r := &Reader{
		stream: stream,
		bucket: bucket,
		throttle: time.Tick(readThrottle),
		closed: false,
	}
	go r.start()
	return r
}


func (r *Reader) start() {
	for {
		<-r.throttle

		if r.closed {
			break
		}

		if r.err = r.read(); r.err != nil {
			log.Errorf("OSS Reader err: %v",r.err)
			return
		}
	}
}
func (r *Reader) Close() error {
	r.closed = true
	return nil
}

func (r *Reader) read() error {
	header, err := r.bucket.GetObjectMeta(r.stream)
	if err != nil {
		return err
	}
	l, err := strconv.ParseInt(header.Get(oss.HTTPHeaderContentLength),10,64)
	if err != nil {
		return err
	}
	if r.pos >= l {
		return nil
	}
	log.Infof("GetObject for %s Range: %d ~ %d", r.stream, r.pos, l)
	body, err := r.bucket.GetObject(r.stream, []oss.Option{
		oss.Range(r.pos,l),
	}...)
	if err != nil {
		return err
	}
	b, err := ioutil.ReadAll(body)
	if err != nil {
		return err
	}

	if len(b) == 0 {
		return nil
	}

	if int64(len(b)) == l {
		b = b[r.pos:l]
	}

	r.b.WriteString(string(b))

	r.pos = l
	//log.Debugf("reader pos: %d",r.pos)
	return nil
}

func (r *Reader) read1() error {
	body, err := r.bucket.GetObject(r.stream, []oss.Option{
		oss.Range(r.pos, r.pos+int64(1000)),
	}...)
	if err != nil {
		return err
	}
	b, err := ioutil.ReadAll(body)
	if err != nil {
		return err
	}

	if len(b) == 0 {
		return nil
	}

	r.b.WriteString(string(b))
	r.pos += int64(len(b))
	log.Debugf("reader pos: %d",r.pos)

	return nil
}

func (r *Reader) Read(b []byte) (int, error) {
	if r.err != nil {
		return 0, r.err
	}

	if r.b.Len() == 0 {
		return 0, nil
	}
	return r.b.Read(b)
}


type lockingBuffer struct {
	sync.Mutex
	bytes.Buffer
}

func (r *lockingBuffer) Read(b []byte) (int, error) {
	r.Lock()
	defer r.Unlock()

	return r.Buffer.Read(b)
}

func (r *lockingBuffer) Write(b []byte) (int, error) {
	r.Lock()
	defer r.Unlock()

	return r.Buffer.Write(b)
}