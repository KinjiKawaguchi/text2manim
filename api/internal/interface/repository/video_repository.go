package repository

import (
	"context"
	"log/slog"

	"github.com/KinjiKawaguchi/text2manim/api/internal/config"
	"github.com/KinjiKawaguchi/text2manim/api/internal/domain"
)

type VideoRepository interface {
	Save(ctx context.Context, video *domain.Generation) error
	FindByID(ctx context.Context, id string) (*domain.Generation, error)
	Update(ctx context.Context, video *domain.Generation) error
}

type VideoRepositoryFactory func(cfg *config.Config, logger *slog.Logger) (VideoRepository, error)
