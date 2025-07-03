package service

import (
	"bytes"
	"encoding/json"
	"log"
	"net/http"
	"sync"
	"time"
)

var client *http.Client
var once sync.Once
var api *API
var baseURL = "http://localhost:8001"

func GetHTTPClient(timeout time.Duration, maxIdleConns, maxIdleConnsPerHost int) *http.Client {
	once.Do(func() {
		client = &http.Client{
			Timeout: timeout,
			Transport: &http.Transport{
				MaxIdleConns:        maxIdleConns,
				MaxIdleConnsPerHost: maxIdleConnsPerHost,
			},
		}
	})
	return client
}

type API struct {
	client *http.Client
}

func getAPI() *API {
	once.Do(func() {
		client = &http.Client{
			Timeout: 10 * time.Second,
			Transport: &http.Transport{
				MaxIdleConns:        100,
				MaxIdleConnsPerHost: 10,
			},
		}
		api = &API{client: client}
	})
	return api
}

func NewAPI() *API {
	return &API{
		client: GetHTTPClient(10*time.Second, 100, 10),
	}
}

func (api *API) Post(url string, payload interface{}) (*http.Response, error) {
	jsonData, err := json.Marshal(payload)
	log.Println(jsonData)
	if err != nil {
		return nil, err
	}
	url = baseURL + url
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))

	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")
	log.Println(req)
	resp, err := api.client.Do(req)
	log.Println(resp)
	if err != nil {
		return nil, err
	}

	return resp, nil
}
