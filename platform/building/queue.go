package building

import (
	"golang.org/x/net/context"
	"github.com/cabernety/boxlinker/platform/building/builder"
)

type BuildQueue interface {
	Push(context.Context, builder.BuildOptions) error
	Subscribe(chan BuildContext) error
}

type BuildContext struct {
	builder.BuildOptions
	Ctx context.Context
}

type buildQueue struct {
	queue chan BuildContext
}

func newBuildQueue(buffer int) *buildQueue {
	return &buildQueue{
		queue: make(chan BuildContext, buffer),
	}
}

func NewBuildQueue(buffer int) BuildQueue {
	return newBuildQueue(buffer)
}

func (q *buildQueue) Push(ctx context.Context, options builder.BuildOptions) error {
	q.queue <- BuildContext{
		Ctx: ctx,
		BuildOptions: options,
	}
	return nil
}

func (q *buildQueue) Subscribe(ch chan BuildContext) error {
	go func(){
		for req := range q.queue {
			ch <- req
		}
	}()
	return nil
}