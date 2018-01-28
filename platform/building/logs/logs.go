package logs

import (
	"io/ioutil"
	"io"
	"strings"
	"os"
	"errors"
)
var Discard = &nullLogger{}

var Stdout = &stdoutLogger{}

type Logger interface {
	Create(name string) (io.Writer, error)
	Open(name string) (io.Reader, error)
}

type nullLogger struct {}

func (l *nullLogger) Create(name string) (io.Writer, error) {
	return ioutil.Discard, nil
}

func (l *nullLogger) Open(name string) (io.Reader, error) {
	return strings.NewReader(""), nil
}



type stdoutLogger struct {}

func (l *stdoutLogger) Create(name string) (io.Writer, error) {
	return os.Stdout, nil
}
func (l *stdoutLogger) Open(name string) (io.Reader, error) {
	return strings.NewReader(""), errors.New("stdout logger: reading is not implemented")
}

