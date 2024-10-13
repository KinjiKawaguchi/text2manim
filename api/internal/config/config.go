// config.go
package config

import (
	"errors"
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
}

func LoadConfig() (*Config, error) {
	// .envファイルを読み込む
	godotenv.Load()

	cfg := &Config{
		APIKeys:     strings.Split(getEnv("API_KEYS", ""), ","),
		IPWhitelist: strings.Split(getEnv("IP_WHITELIST", ""), ","),
		WorkerAddr:  getEnv("WORKER_ADDR", "worker:50052"),
		ServerPort:  getEnv("SERVER_PORT", "50051"),
		LogLevel:    getEnv("LOG_LEVEL", "info"),
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
