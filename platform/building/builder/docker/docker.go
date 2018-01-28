package docker

import (
	"github.com/cabernety/boxlinker/platform/building/builder"
	"github.com/fsouza/go-dockerclient"
	"golang.org/x/net/context"
	uuid "github.com/codeskyblue/go-uuid"
	"fmt"
	"io"
	"strings"
	"os"
	log "github.com/Sirupsen/logrus"
)

const (
	DefaultBuilderImage = "remind101/conveyor-builder:master"
	DefaultDataVolume = "data"
)

var newUUID = uuid.New

type dockerClient interface {
	CreateContainer(docker.CreateContainerOptions) (*docker.Container, error)
	RemoveContainer(docker.RemoveContainerOptions) error
	StartContainer(string, *docker.HostConfig) error
	AttachToContainer(docker.AttachToContainerOptions) error
	StopContainer(string, uint) error
	WaitContainer(string) (int, error)
}

type Builder struct {
	DataVolume string
	Image string
	DryRun bool
	client dockerClient
}

func NewBuilder(c *docker.Client) *Builder {
	return &Builder{client: c}
}

func NewBuilderFromEnv() (*Builder, error) {
	c, err := docker.NewClientFromEnv()
	if err != nil {
		return nil, err
	}

	return NewBuilder(c), nil
}

func (b *Builder) Build(ctx context.Context, w io.Writer, opts builder.BuildOptions) (image string, err error ) {
	image = fmt.Sprintf("%s/%s:%s", opts.Registry, opts.Repository, opts.Sha)
	err = b.build(ctx, w, opts)
	return
}

func (b *Builder) build(ctx context.Context, w io.Writer, opts builder.BuildOptions) error {
	env := []string{
		fmt.Sprintf("DOCKER_DAEMON_ARGS=%s", strings.ToLower("--insecure-registry=index.boxlinker.com")),
		fmt.Sprintf("REPOSITORY=%s", strings.ToLower(opts.Repository)),
		fmt.Sprintf("REGISTRY_HOST=%s", strings.ToLower(opts.Registry)),
		fmt.Sprintf("BRANCH=%s", opts.Branch),
		fmt.Sprintf("SHA=%s", opts.Sha),
		fmt.Sprintf("CACHE=%s", b.cache(opts)),
	}

	name := strings.Join([]string{
		strings.Replace(opts.Repository, "/", "-", -1),
		opts.Sha,
		newUUID(),
	}, "-")

	c, err := b.client.CreateContainer(docker.CreateContainerOptions{
		Name: name,
		HostConfig: &docker.HostConfig{
			Privileged: true,
			VolumesFrom: []string{b.dataVolume()},
		},
		Config: &docker.Config{
			Tty: 		false,
			AttachStdout: 	true,
			AttachStderr: 	true,
			OpenStdin: 	true,
			Image: 		b.image(),
			Hostname: 	hostname,
			Env: 		env,
		},
	})
	if err != nil {
		return fmt.Errorf("create container: %v",err)
	}
	defer b.client.RemoveContainer(docker.RemoveContainerOptions{
		ID: 		c.ID,
		RemoveVolumes: 	true,
		Force: 		true,
	})

	log.Debugf("starting container: %s",c.ID)

	if err := b.client.StartContainer(c.ID, nil); err != nil {
		return fmt.Errorf("start container: %v", err)
	}

	done := make(chan error, 1)
	go func(){
		done <- b.client.AttachToContainer(docker.AttachToContainerOptions{
			Container: 	c.ID,
			OutputStream: 	w,
			ErrorStream: 	w,
			Logs: 		true,
			Stream: 	true,
			Stdout: 	true,
			Stderr: 	true,
			RawTerminal: 	false,
		})
	}()

	var canceled bool
	select {
	case <-ctx.Done():
		if err := b.client.StopContainer(c.ID, 10); err != nil {
			return fmt.Errorf("stop: %v", err)
		}

		if err := <-done; err != nil {
			return fmt.Errorf("attach: %v", err)
		}

		canceled = true
	case err := <-done:
		if err != nil {
			return fmt.Errorf("attach: %v", err)
		}
	}

	exit, err := b.client.WaitContainer(c.ID)
	if exit != 0 {
		err := fmt.Errorf("container returned a non-zero exit code: %d, err: %v", exit, ctx.Err())
		if canceled {
			err = &builder.BuildCanceledError{
				Err: err,
				Reason: ctx.Err(),
			}
		}
		return err
	}
	return nil
}

func (b *Builder) dryRun() string {
	if b.DryRun {
		return "true"
	}
	return ""
}

func (b *Builder) image() string {
	if b.Image == "" {
		return DefaultBuilderImage
	}
	return b.Image
}

func (b *Builder) dataVolume() string {
	if b.DataVolume == "" {
		return DefaultDataVolume
	}
	return b.DataVolume
}

func (b *Builder) cache(opts builder.BuildOptions) string {
	if opts.NoCache {
		return "off"
	}

	return "on"
}

var hostname string

func init() {
	hostname, _ = os.Hostname()
}
