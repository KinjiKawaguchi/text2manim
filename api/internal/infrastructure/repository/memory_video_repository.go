package repository

import (
	"context"
	"errors"
	"log/slog"
	"sync"

	"github.com/KinjiKawaguchi/text2manim/api/internal/domain"
)

type MemoryVideoRepository struct {
	videos map[string]*domain.Generation
	mu     sync.RWMutex
	logger *slog.Logger
}

// FindByID implements repository.VideoRepository.
func (m *MemoryVideoRepository) FindByID(ctx context.Context, id string) (*domain.Generation, error) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	m.logger.Debug("Finding video by ID", "id", id)
	video, exists := m.videos[id]
	if !exists {
		m.logger.Warn("Video not found", "id", id)
		return nil, errors.New("video not found")
	}
	m.logger.Debug("Video found", "id", id)
	return video, nil
}

// Save implements repository.VideoRepository.
func (m *MemoryVideoRepository) Save(ctx context.Context, video *domain.Generation) error {
	m.mu.Lock()
	defer m.mu.Unlock()

	m.logger.Debug("Attempting to save video", "id", video.ID)
	if _, exists := m.videos[video.ID]; exists {
		m.logger.Warn("Video already exists", "id", video.ID)
		return errors.New("video already exists")
	}
	m.videos[video.ID] = video
	m.logger.Info("Video saved successfully", "id", video.ID)
	return nil
}

// Update implements repository.VideoRepository.
func (m *MemoryVideoRepository) Update(ctx context.Context, video *domain.Generation) error {
	m.mu.Lock()
	defer m.mu.Unlock()

	m.logger.Debug("Attempting to update video", "id", video.ID)
	if _, exists := m.videos[video.ID]; !exists {
		m.logger.Warn("Video not found for update", "id", video.ID)
		return errors.New("video not found")
	}
	m.videos[video.ID] = video
	m.logger.Info("Video updated successfully", "id", video.ID)
	return nil
}

func NewMemoryVideoRepository(logger *slog.Logger) *MemoryVideoRepository {
	return &MemoryVideoRepository{
		videos: make(map[string]*domain.Generation),
		logger: logger,
	}
}
