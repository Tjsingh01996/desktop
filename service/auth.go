package service

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"io"
	"log"
	"net/http"
	"sync"

	database "github.com/Tjsingh01996/desktop/db"
)

type AuthService struct {
	db *sql.DB
}

var (
	authServiceInstance *AuthService
	authServiceOnce     sync.Once
)

func GetAuthService() *AuthService {
	authServiceOnce.Do(func() {
		authServiceInstance = &AuthService{db: database.GetDbConnection()}
	})
	return authServiceInstance
}

type LoginRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}
type ErrorResponse struct {
	Message string `json:"message"`
	Status  uint16 `json:"status"`
}

func HandleError(body io.ReadCloser, message any) error {
	errorResponse := ErrorResponse{}
	bodyBytes, _ := io.ReadAll(body)
	err := json.Unmarshal(bodyBytes, &errorResponse)
	if err != nil {
		if message != "" {
			return errors.New("internal server error")
		}
		return errors.New("failed to decode error response")
	}
	return errors.New(errorResponse.Message)
}

func (auth *AuthService) Login(ctx context.Context, email string, password string) (map[string]interface{}, error) {
	payload := LoginRequest{
		Email:    email,
		Password: password,
	}
	api := getAPI()
	resp, err := api.Post("/login", payload)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode == http.StatusOK {
		var user map[string]interface{}
		err := json.NewDecoder(resp.Body).Decode(&user)
		if err != nil {
			log.Fatal(err)
		}
		return user, nil
	}
	if resp.StatusCode == http.StatusUnauthorized {

		return nil, HandleError(resp.Body, "invalid email or password")
	}

	if resp.StatusCode == http.StatusInternalServerError {

		return nil, HandleError(resp.Body, "internal server error")
	}
	return nil, HandleError(resp.Body, "login failed")
}
