package oss

import (
	"time"
	"sync"
	"github.com/aliyun/aliyun-oss-go-sdk/oss"
	"io"
	"bufio"
	"bytes"
	"fmt"
	//log "github.com/Sirupsen/logrus"
)

type Writer struct {
	stream string
	bucket 	*oss.Bucket
	closed 	bool
	pos 	int64
	err 	error
	events  eventsBuffer
	throttle <-chan time.Time
	sync.Mutex
}

func NewWriter(stream string, bucket *oss.Bucket) *Writer {
	w := &Writer{
		stream: stream,
		bucket: bucket,
		throttle: time.Tick(writeThrottle),
	}
	go w.start()
	return w
}

func (w *Writer) start() error {
	for {
		if w.closed {
			return nil
		}
		<-w.throttle
		if err := w.Flush(); err != nil {
			fmt.Errorf("OSS writer err: %v",err)
			return err
		}
	}
}

func (w *Writer) Flush() error {
	w.Lock()
	defer w.Unlock()

	events := w.events.drain()

	if len(events) == 0 {
		return nil
	}

	w.err = w.flush(events)
	return w.err
}

func (w *Writer) flush(events []*InputLogEvent) error {
	for _, event := range events {
		//if log.GetLevel() == log.DebugLevel {
		//	fmt.Print(string(event.Message))
		//}
		pos, err := w.bucket.AppendObject(w.stream, bytes.NewReader(event.Message), w.pos)
		if err != nil {
			return err
		}
		w.pos = pos
	}
	return nil
}

func (w *Writer) Close() error {
	w.closed = true
	return w.Flush()
}

func (w *Writer) Write(b []byte) (int, error) {
	if w.closed {
		return 0, io.ErrClosedPipe
	}

	if w.err != nil {
		return 0, w.err
	}

	return w.buffer(b)
}

func (w *Writer) buffer(b []byte) (int, error) {
	r := bufio.NewReader(bytes.NewReader(b))

	var (
		n int
		eof bool
	)

	for !eof {
		b, err := r.ReadBytes('\n')
		if err != nil {
			if err == io.EOF {
				eof = true
			} else {
				break
			}
		}

		if len(b) == 0 {
			continue
		}

		w.events.add(&InputLogEvent{
			Message: b,
			Timestamp: now().UnixNano() / 1000000,
		})

		n += len(b)
	}

	return n, nil
}

type InputLogEvent struct {
	Message []byte
	Timestamp int64
}

type eventsBuffer struct {
	sync.Mutex
	events []*InputLogEvent
}

func (b *eventsBuffer) add(event *InputLogEvent) {
	b.Lock()
	defer b.Unlock()

	b.events = append(b.events, event)
}

func (b *eventsBuffer) drain() []*InputLogEvent {
	b.Lock()
	defer b.Unlock()

	events := b.events[:]
	b.events = nil
	return events
}


