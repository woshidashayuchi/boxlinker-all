package builder

import (
	"golang.org/x/net/context"
	"io"
	"sync"
	"time"
	"errors"
	"text/template"
	"fmt"
	"strings"
	"bytes"
	"github.com/google/go-github/github"
)

const (
	Context = "container/docker"
)

var (
	ErrShuttingDown = errors.New("shutting down")
)
type BuildCanceledError struct {
	Err    error
	Reason error
}

// Error implements the error interface.
func (e *BuildCanceledError) Error() string {
	return fmt.Sprintf("%s (%s)", e.Err.Error(), e.Reason.Error())
}

type BuildOptions struct {
	ID string
	Repository string
	Sha string
	Branch string
	NoCache bool
	Registry string
}

type Builder interface {
	Build(ctx context.Context, w io.Writer, opts BuildOptions) (image string, err error)
}

type BuilderFunc func(context.Context, io.Writer, BuildOptions) (string, error)

func (fn BuilderFunc) Build(ctx context.Context, w io.Writer, opts BuildOptions) (string, error) {
	return fn(ctx, w, opts)
}

var since = time.Since

type statusUpdaterBuilder struct {
	Builder
	github GitHubClient
	urlTmpl *template.Template
}

func UpdateGitHubCommitStatus(b Builder, g GitHubClient, urlTmpl string) *statusUpdaterBuilder {
	return &statusUpdaterBuilder{
		Builder: b,
		github: g,
		urlTmpl: template.Must(template.New("url").Parse(urlTmpl)),
	}
}

func (b *statusUpdaterBuilder) Build(ctx context.Context, w io.Writer, opts BuildOptions) (image string, err error) {
	t := time.Now()

	defer func(){
		duration := since(t)
		description := fmt.Sprintf("Image built in %v.", duration)
		status := "success"
		if err != nil {
			status = "failure"
			description = err.Error()
		}
		b.updateStatus(w, opts, status, description)
	}()

	if err = b.updateStatus(w, opts, "pending", "Image building."); err != nil {
		return
	}
	image, err = b.Builder.Build(ctx, w, opts)
	return
}

func (b *statusUpdaterBuilder) updateStatus(w io.Writer, opts BuildOptions, status string, description string) error {
	context := Context
	parts := strings.SplitN(opts.Repository, "/", 2)

	var desc *string
	if description != "" {
		desc = &description
	}

	url, err := b.url(opts)
	if err != nil {
		return err
	}
	_, _, err = b.github.CreateStatus(parts[0], parts[1], opts.Sha, &github.RepoStatus{
		State: 		&status,
		Context: 	&context,
		Description: 	desc,
		TargetURL: 	github.String(url),
	})
	return err
}

func (b *statusUpdaterBuilder) url(opts BuildOptions) (string, error) {
	buf := new(bytes.Buffer)
	err := b.urlTmpl.Execute(buf, opts)
	return buf.String(), err
}

func WithCancel(b Builder) *CancelBuilder {
	return &CancelBuilder{
		Builder: b,
		builds: make(map[context.Context]context.CancelFunc),
	}
}

type CancelBuilder struct {
	Builder

	sync.Mutex
	stopped bool
	builds map[context.Context]context.CancelFunc
}

func (b *CancelBuilder) Build(ctx context.Context, w io.Writer, opts BuildOptions) (string, error) {
	if b.stopped {
		return "", ErrShuttingDown
	}

	ctx = b.addBuild(ctx)
	defer b.removeBuild(ctx)

	return b.Builder.Build(ctx, w, opts)
}

func (b *CancelBuilder) Cancel() error {
	b.Lock()
	b.stopped = true
	for _, cancel := range b.builds {
		cancel()
	}

	b.Unlock()

	for {
		<-time.After(time.Second)

		if len(b.builds) == 0{
			break
		}
	}

	return nil
}

func (b *CancelBuilder) addBuild(ctx context.Context) context.Context {
	b.Lock()
	defer b.Unlock()

	ctx, cancel := context.WithCancel(ctx)
	b.builds[ctx] = cancel
	return ctx
}

func (b *CancelBuilder) removeBuild(ctx context.Context) {
	b.Lock()
	defer b.Unlock()

	delete(b.builds, ctx)
}

func CloseWriter(b Builder) Builder {
	return BuilderFunc(func(ctx context.Context, w io.Writer, opts BuildOptions) (image string, err error) {
		defer func(){
			var closeErr error
			if w, ok := w.(io.Closer); ok {
				closeErr = w.Close()
			}
			if err == nil {
				err = closeErr
			}
		}()

		image, err = b.Build(ctx, w, opts)
		return
	})
}