// repository/memory_video_repository.go
package repository

import (
	"context"
	"sync"

	"github.com/KinjiKawaguchi/text2manim/api/internal/domain"
)

type MemoryVideoRepository struct {
	videos map[string]*domain.Video
	mu     sync.RWMutex
}

// FindByID implements repository.VideoRepository.
func (m *MemoryVideoRepository) FindByID(ctx context.Context, id string) (*domain.Video, error) {
	panic("unimplemented")
}

// Save implements repository.VideoRepository.
func (m *MemoryVideoRepository) Save(ctx context.Context, video *domain.Video) error {
	panic("unimplemented")
}

// Update implements repository.VideoRepository.
func (m *MemoryVideoRepository) Update(ctx context.Context, video *domain.Video) error {
	panic("unimplemented")
}

func NewMemoryVideoRepository() *MemoryVideoRepository {
	return &MemoryVideoRepository{
		videos: make(map[string]*domain.Video),
	}
}
