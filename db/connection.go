package db

import (
	"database/sql"
	"fmt"
	"log"
	"sync"

	"github.com/go-sql-driver/mysql"
	_ "github.com/go-sql-driver/mysql"
)

var (
	instance *sql.DB
	once     sync.Once
)

func GetDbConnection() *sql.DB {
	once.Do(func() {
		log.Println("it called bro")
		cfg := mysql.Config{
			User:                 "root",
			Passwd:               "root",
			Net:                  "tcp",
			Addr:                 "127.0.0.1:3306",
			DBName:               "desktop_app",
			AllowNativePasswords: true,
			ParseTime:            true,
		}
		fmt.Println(cfg.FormatDSN())
		db, err := sql.Open("mysql", cfg.FormatDSN())
		if err != nil {
			log.Fatal("Failed to connect to database:", err)
		}
		pingError := db.Ping()
		if pingError == nil {
			log.Print("Database Connected")
		}
		instance = db
	})
	return instance
}
