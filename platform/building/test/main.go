package main

import (
	log "github.com/Sirupsen/logrus"
	"fmt"
	"database/sql/driver"
)
type BuildState int

const (
	//_ BuildState = iota
	StatePending BuildState = iota
	StateBuilding
	StateFailed
	StateSucceeded
)


func (s BuildState) String() string {
	switch s {
	case StatePending:
		return "pending"
	case StateBuilding:
		return "building"
	case StateFailed:
		return "failed"
	case StateSucceeded:
		return "succeeded"
	default:
		panic(fmt.Sprintf("未知的构建状态: %v", s))
	}
}


func (s *BuildState) Scan(src interface{}) error {
	if v, ok := src.([]byte); ok {
		switch string(v) {
		case "pending":
			*s = StatePending
		case "building":
			*s = StateBuilding
		case "failed":
			*s = StateFailed
		case "succeeded":
			*s = StateSucceeded
		default:
			return fmt.Errorf("未知的构建状态: %v", string(v))
		}
	}
	return nil
}

func (s BuildState) Value() (driver.Value, error) {
	return driver.Value(s.String()), nil
}

func main(){
	log.SetLevel(log.DebugLevel)

	log.Debugf(">> %s, %s, %s, %s",StatePending,StateBuilding,StateFailed,StateSucceeded)
}