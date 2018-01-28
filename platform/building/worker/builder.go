package worker

import (
	"github.com/cabernety/boxlinker/platform/building/builder"
	"time"
	"golang.org/x/net/context"
	"io"
	log "github.com/Sirupsen/logrus"
)

type Builder struct {
	builder builder.Builder
	Timeout time.Duration
}

func NewBuilder(b builder.Builder) *Builder {
	return &Builder{
		builder: builder.CloseWriter(b),
		Timeout: DefaultTimeout,
	}
}

func (b *Builder) Build(ctx context.Context, w io.Writer, opts builder.BuildOptions) (image string, err error) {
	log.Debugf("Starting build: id=%s repository=%s branch=%s sha=%s",
		opts.ID,
		opts.Repository,
		opts.Branch,
		opts.Sha,
	)

	if b.Timeout != 0 {
		var cancel context.CancelFunc
		ctx, cancel = context.WithTimeout(ctx, b.Timeout)
		defer cancel()
	}

	image, err = b.builder.Build(ctx, w, opts)
	return
}
