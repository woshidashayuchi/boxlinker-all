package es

type Logger struct {
	Log 		string 			`json:"log"`
	Kubernetes 	map[string]interface{} 	`json:"kubernetes"`
	Timestamp 	string 			`json:"@timestamp"`
}
