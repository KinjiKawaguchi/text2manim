package repository

import (
	"context"

	"github.com/KinjiKawaguchi/text2manim/api/internal/domain"
)

type VideoRepository interface {
	Save(ctx context.Context, video *domain.Video) error
	FindByID(ctx context.Context, id string) (*domain.Video, error)
	Update(ctx context.Context, video *domain.Video) error
}

type NewMemoryVideoRepository struct {
	videos map[string]*domain.Video
}
