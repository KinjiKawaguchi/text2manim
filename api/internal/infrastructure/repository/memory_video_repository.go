// repository/memory_video_repository.go
package repository

import (
	"context"
	"errors"
	"sync"

	"github.com/KinjiKawaguchi/text2manim/api/internal/domain"
)

type MemoryVideoRepository struct {
	videos map[string]*domain.Video
	mu     sync.RWMutex
}

// FindByID implements repository.VideoRepository.
func (m *MemoryVideoRepository) FindByID(ctx context.Context, id string) (*domain.Video, error) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	video, exists := m.videos[id]
	if !exists {
		return nil, errors.New("video not found")
	}
	return video, nil
}

// Save implements repository.VideoRepository.
func (m *MemoryVideoRepository) Save(ctx context.Context, video *domain.Video) error {
	m.mu.Lock()
	defer m.mu.Unlock()

	if _, exists := m.videos[video.ID]; exists {
		return errors.New("video already exists")
	}
	m.videos[video.ID] = video
	return nil
}

// Update implements repository.VideoRepository.
func (m *MemoryVideoRepository) Update(ctx context.Context, video *domain.Video) error {
	m.mu.Lock()
	defer m.mu.Unlock()

	if _, exists := m.videos[video.ID]; !exists {
		return errors.New("video not found")
	}
	m.videos[video.ID] = video
	return nil
}

func NewMemoryVideoRepository() *MemoryVideoRepository {
	return &MemoryVideoRepository{
		videos: make(map[string]*domain.Video),
	}
}
