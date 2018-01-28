package oss

import (
	"github.com/aliyun/aliyun-oss-go-sdk/oss"
	"io"
	"time"
)
const (
// The maximum rate of a GetLogEvents request is 10 requests per second per AWS account.
	readThrottle = time.Second / 2

// The maximum rate of a PutLogEvents request is 5 requests per second per log stream.
	writeThrottle = time.Second / 5
)
var now = time.Now

type Group struct {
	bucket *oss.Bucket
}

func NewGroup( bucket *oss.Bucket) *Group {
	return &Group{
		bucket: bucket,
	}
}

func (g *Group) Create(stream string) (io.Writer, error) {
	return NewWriter(stream, g.bucket), nil
}

func (g *Group) Open(stream string) (io.Reader, error) {
	return NewReader(stream, g.bucket), nil
}