// config.go
package config

import (
	"errors"
	"log/slog"
	"os"
	"strings"

	"github.com/joho/godotenv"
)

type Config struct {
	APIKeys     []string
	IPWhitelist []string
	WorkerAddr  string
	ServerPort  string
	LogLevel    string
	DBType      string
	DBHost      string
	DBPort      string
	DBUser      string
	DBPassword  string
	DBName      string
}

func LoadConfig(logger *slog.Logger) (*Config, error) {
	// .envファイルを読み込む
	err := godotenv.Load()
	if err != nil {
		logger.Warn("Failed to load .env file", "error", err)
	}

	cfg := &Config{
		APIKeys:     strings.Split(getEnv("API_KEYS", ""), ","),
		IPWhitelist: strings.Split(getEnv("IP_WHITELIST", ""), ","),
		WorkerAddr:  getEnv("WORKER_ADDR", "worker:50052"),
		ServerPort:  getEnv("SERVER_PORT", "50051"),
		LogLevel:    getEnv("LOG_LEVEL", "info"),
		DBType:      getEnv("DB_TYPE", "memory"),
		DBHost:      getEnv("DB_HOST", "localhost"),
		DBPort:      getEnv("DB_PORT", "5432"),
		DBUser:      getEnv("DB_USER", ""),
		DBPassword:  getEnv("DB_PASSWORD", ""),
		DBName:      getEnv("DB_NAME", ""),
	}

	// APIキーの読み込み
	if len(cfg.APIKeys) == 0 || (len(cfg.APIKeys) == 1 && cfg.APIKeys[0] == "") {
		return nil, errors.New("API keys are not set")
	}

	return cfg, nil
}

func getEnv(key, fallback string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return fallback
}
