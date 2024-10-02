// config.go
package config

import (
	"os"

	"github.com/spf13/viper"
)

type Config struct {
	APIKeys     map[string]ServiceInfo `mapstructure:"api_keys"`
	IPWhitelist []string               `mapstructure:"ip_whitelist"`
	WorkerAddr  string
	ServerPort  string
	LogLevel    string
}

type ServiceInfo struct {
	Service     string   `mapstructure:"service"`
	Permissions []string `mapstructure:"permissions"`
}

func LoadConfig() (*Config, error) {
	// YAML file for API keys and IP whitelist
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("./config/")
	viper.AddConfigPath("/etc/text2manim/")

	if err := viper.ReadInConfig(); err != nil {
		return nil, err
	}

	var cfg Config
	if err := viper.Unmarshal(&cfg); err != nil {
		return nil, err
	}

	// Environment variables for other configurations
	cfg.WorkerAddr = getEnv("WORKER_ADDR", "worker:50052")
	cfg.ServerPort = getEnv("SERVER_PORT", "50051")
	cfg.LogLevel = getEnv("LOG_LEVEL", "info")

	return &cfg, nil
}

func getEnv(key, fallback string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return fallback
}
