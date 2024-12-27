package repository

import (
	"context"
	"errors"
	"log/slog"
	"sync"

	"github.com/KinjiKawaguchi/text2manim/api/internal/domain/ent"
	"github.com/google/uuid"
)

type MemoryVideoRepository struct {
	videos map[string]*ent.Generation
	mu     sync.RWMutex
	logger *slog.Logger
}

// FindByID implements repository.VideoRepository.
func (m *MemoryVideoRepository) FindByID(ctx context.Context, id uuid.UUID) (*ent.Generation, error) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	m.logger.Debug("Finding video by ID", "id", id)
	video, exists := m.videos[id.String()]
	if !exists {
		m.logger.Warn("Video not found", "id", id)
		return nil, errors.New("video not found")
	}
	m.logger.Debug("Video found", "id", id)
	return video, nil
}

// Save implements repository.VideoRepository.
func (m *MemoryVideoRepository) Save(ctx context.Context, video *ent.Generation) (*ent.Generation, error) {
	m.mu.Lock()
	defer m.mu.Unlock()

	m.logger.Debug("Attempting to save video", "id", video.ID)
	if _, exists := m.videos[video.ID.String()]; exists {
		m.logger.Warn("Video already exists", "id", video.ID)
		return nil, errors.New("video already exists")
	}
	m.videos[video.ID.String()] = video
	m.logger.Info("Video saved successfully", "id", video.ID)
	return m.videos[video.ID.String()], nil
}

// Update implements repository.VideoRepository.
func (m *MemoryVideoRepository) Update(ctx context.Context, video *ent.Generation) (*ent.Generation, error) {
	m.mu.Lock()
	defer m.mu.Unlock()

	m.logger.Debug("Attempting to update video", "id", video.ID)
	if _, exists := m.videos[video.ID.String()]; !exists {
		m.logger.Warn("Video not found for update", "id", video.ID)
		return nil, errors.New("video not found")
	}
	m.videos[video.ID.String()] = video
	m.logger.Info("Video updated successfully", "id", video.ID)
	return m.videos[video.ID.String()], nil
}

func NewMemoryVideoRepository(logger *slog.Logger) (*MemoryVideoRepository, error) {
	return &MemoryVideoRepository{
		videos: make(map[string]*ent.Generation),
		logger: logger,
	}, nil
}
