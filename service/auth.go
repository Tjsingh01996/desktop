package service

import (
	"context"
	"database/sql"
	"sync"

	database "github.com/Tjsingh01996/desktop/db"
	authors "github.com/Tjsingh01996/desktop/mysql"
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

func (auth *AuthService) Login(ctx context.Context, name string, email string) (bool, error) {
	queries := authors.New(auth.db)
	_, err := queries.VerifyUser(ctx, authors.VerifyUserParams{
		email,
		name,
	})
	if err != nil {
		return false, err
	}

	return true, nil
}
