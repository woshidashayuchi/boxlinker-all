package worker

import (
	"time"
	"golang.org/x/net/context"
	"io"
	log "github.com/Sirupsen/logrus"
	"github.com/cabernety/boxlinker/platform/building/builder"
	"github.com/cabernety/boxlinker/platform/building"
	"sync"
)

const (
	DefaultTimeout = 20 * time.Minute
)

type Building interface {
	Writer(ctx context.Context, buildID string) (io.Writer, error)
	BuildStarted(ctx context.Context, buildID string) error
	BuildComplete(ctx context.Context, buildID, image string) error
	BuildFailed(ctx context.Context, buildID string, err error) error
}

type Workers []*Worker

func (w Workers) Start() {
	for _, worker := range w {
		go worker.Start()
	}
}

func (w Workers) Shutdown() error {
	var (
		wg 	sync.WaitGroup
		errors 	[]error
	)

	for _, worker := range w {
		wg.Add(1)
		go func(worker *Worker) {
			defer wg.Done()
			if err := worker.Shutdown(); err != nil {
				errors = append(errors, err)
			}
		}(worker)
	}

	wg.Wait()

	if len(errors) == 0 {
		return nil
	}

	return errors[0]
}

func NewPool(b Building, num int, options Options) (workers Workers) {
	for i := 0; i < num; i++ {
		w := New(b, options)
		workers = append(workers, w)
	}
	return
}

type Options struct {
	Builder builder.Builder
	BuildRequests chan building.BuildContext
}

type Worker struct {
	Building
	builder.Builder
	buildRequests chan building.BuildContext
	shutdown chan struct{}
	done chan error
}

func New(b Building, options Options) *Worker {
	return &Worker{
		Building: 	b,
		Builder:	builder.WithCancel(options.Builder),
		buildRequests: 	options.BuildRequests,
		shutdown: 	make(chan struct{}),
		done: 		make(chan error),
	}
}

func (w *Worker) Start() error {
	for {
		select {
		case <-w.shutdown:
			var err error
			if b, ok := w.Builder.(interface{
				Cancel() error
			}); ok {
				err = b.Cancel()
			}

			w.done <- err
			break
		case req, ok := <-w.buildRequests:
			if !ok {
				break
			}

			if err := w.build(req.Ctx, req.BuildOptions); err != nil {
				log.Error(err)
			}

			continue
		}

		break
	}
	return nil
}

func (w *Worker) build(ctx context.Context, options builder.BuildOptions) (err error) {
	buildID := options.ID

	err = w.BuildStarted(ctx, buildID)
	if err != nil {
		return
	}

	var image string
	var logger io.Writer
	logger, err = w.Writer(ctx, buildID)
	if err != nil {
		return
	}
	defer func(){
		if err == nil {
			err = w.BuildComplete(ctx, buildID, image)
		} else {
			w.BuildFailed(ctx, buildID, err)
		}
	}()

	image, err = w.Build(ctx, logger, options)

	if err != nil {
		return
	}

	return
}

func (w *Worker) Shutdown() error {
	close(w.shutdown)
	return <-w.done
}