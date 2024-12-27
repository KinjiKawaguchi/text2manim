package repository

import (
	"context"
	"log/slog"

	"github.com/KinjiKawaguchi/text2manim/api/internal/config"
	"github.com/KinjiKawaguchi/text2manim/api/internal/domain/ent"
	"github.com/google/uuid"
)

type VideoRepository interface {
	Save(ctx context.Context, video *ent.Generation) (*ent.Generation, error)
	FindByID(ctx context.Context, id uuid.UUID) (*ent.Generation, error)
	Update(ctx context.Context, video *ent.Generation) (*ent.Generation, error)
}

type VideoRepositoryFactory func(cfg *config.Config, logger *slog.Logger) (VideoRepository, error)
