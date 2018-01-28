package building

import (
	"github.com/cabernety/boxlinker/platform/building/logs"
	"golang.org/x/net/context"
	"io"
	"github.com/jmoiron/sqlx"
	"github.com/cabernety/boxlinker/platform/building/builder"
	"fmt"
	"strings"
)

type Building struct {
	BuildQueue
	Logger logs.Logger
	GitHub GitHubAPI
	db *sqlx.DB
	Registry string
}

func New(db *sqlx.DB) *Building {
	return &Building{db: db}
}

func (b *Building) Logs(ctx context.Context, buildID string) (io.Reader, error) {
	return b.Logger.Open(buildID)
}

type BuildRequest struct {
	Repository string
	Sha string
	Branch string
	NoCache bool
}

func (b *Building) Build(ctx context.Context, req BuildRequest) (*Build, error) {
	if req.Sha == "" && req.Branch != "" {
		owner, repo := splitRepo(req.Repository)
		sha, err := b.GitHub.ResolveBranch(owner, repo, req.Branch)
		if err != nil {
			return nil, err
		}
		req.Sha = sha
	}

	tx, err := b.db.Beginx()
	if err != nil {
		return nil, err
	}

	build := &Build{
		Repository: 	req.Repository,
		Sha: 		req.Sha,
		Branch: 	req.Branch,
	}

	if err := buildsCreate(tx, build); err != nil {
		tx.Rollback()
		return build, err
	}

	if err := tx.Commit(); err != nil {
		return build, err
	}

	return build, b.BuildQueue.Push(ctx, builder.BuildOptions{
		ID: 		build.ID,
		Repository: req.Repository,
		Sha:        req.Sha,
		Branch:     req.Branch,
		NoCache:    req.NoCache,
		Registry: 	b.Registry,
	})
}

// FindBuild finds a build by its identity.
func (c *Building) FindBuild(ctx context.Context, buildIdentity string) (*Build, error) {
	tx, err := c.db.Beginx()
	if err != nil {
		return nil, err
	}

	var find func(*sqlx.Tx, string) (*Build, error)
	switch strings.Contains(buildIdentity, "@") {
	case true:
		find = buildsFindByRepoSha
	default:
		find = buildsFindByID
	}

	b, err := find(tx, buildIdentity)
	if err != nil {
		tx.Rollback()
		return b, err
	}

	return b, tx.Commit()
}


// FindArtifact finds an artifact by its identity.
func (c *Building) FindArtifact(ctx context.Context, artifactIdentity string) (*Artifact, error) {
	tx, err := c.db.Beginx()
	if err != nil {
		return nil, err
	}

	var find func(*sqlx.Tx, string) (*Artifact, error)
	switch strings.Contains(artifactIdentity, "@") {
	case true:
		find = artifactsFindByRepoSha
	default:
		find = artifactsFindByID
	}

	a, err := find(tx, artifactIdentity)
	if err != nil {
		tx.Rollback()
		return a, err
	}

	return a, tx.Commit()
}

func (b *Building) Writer(ctx context.Context, buildID string) (io.Writer, error) {
	fmt.Sprintf("buildID: %s",buildID)
	return b.Logger.Create(buildID)
}


func (b *Building) BuildStarted(cex context.Context, buildID string) error {
	tx, err := b.db.Beginx()
	if err != nil {
		return err
	}

	if err := buildsUpdateState(tx, buildID, StateBuilding); err != nil {
		tx.Rollback()
		return err
	}

	return tx.Commit()
}

func (b *Building) BuildComplete(ctx context.Context, buildID, image string) error {
	tx, err := b.db.Beginx()
	if err != nil {
		return err
	}

	if err := buildsUpdateState(tx, buildID, StateSucceeded); err != nil {
		tx.Rollback()
		return err
	}

	if err := artifactsCreate(tx, &Artifact{
		BuildID: buildID,
		Image:   image,
	}); err != nil {
		tx.Rollback()
		return err
	}

	return tx.Commit()
}

func (b *Building) BuildFailed(ctx context.Context, buildID string, err error) error {
	tx, err := b.db.Beginx()
	if err != nil {
		return err
	}

	if err := buildsUpdateState(tx, buildID, StateFailed); err != nil {
		tx.Rollback()
		return err
	}

	return tx.Commit()
}


func insert(tx *sqlx.Tx, sql string, v interface{}, returns ...interface{}) error {
	rows, err := tx.NamedQuery(sql, v)
	if err != nil {
		return err
	}
	defer rows.Close()
	if rows.Next() {
		for _, r := range returns {
			rows.Scan(r)
		}
	} else {
		panic("expected id to be returned")
	}
	return nil
}