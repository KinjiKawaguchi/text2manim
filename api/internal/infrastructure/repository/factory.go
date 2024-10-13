package repository

import (
	"fmt"
	"log/slog"

	"github.com/KinjiKawaguchi/text2manim/api/internal/config"
	interfaceRepo "github.com/KinjiKawaguchi/text2manim/api/internal/interface/repository"
)

// NewVideoRepository は VideoRepository インターフェースの新しいインスタンスを作成します
func NewVideoRepository(cfg *config.Config, logger *slog.Logger) (interfaceRepo.VideoRepository, error) {
	switch cfg.DBType {
	case "memory":
		return NewMemoryVideoRepository(logger), nil
	case "postgres":
		return NewPostgresVideoRepository(cfg, logger)
	default:
		return nil, fmt.Errorf("unsupported database type: %s", cfg.DBType)
	}
}
