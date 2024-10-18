package usecase

import (
	"context"
	"fmt"
	"log/slog"
	"time"

	"github.com/KinjiKawaguchi/text2manim/api/internal/domain"
	"github.com/KinjiKawaguchi/text2manim/api/internal/interface/repository"
	"github.com/KinjiKawaguchi/text2manim/api/internal/interface/worker"
	"github.com/google/uuid"
)

type VideoGeneratorUseCase struct {
	repo         repository.VideoRepository
	workerClient worker.WorkerClient
	logger       *slog.Logger
}

func NewVideoGeneratorUseCase(repo repository.VideoRepository, workerClient worker.WorkerClient, logger *slog.Logger) *VideoGeneratorUseCase {
	return &VideoGeneratorUseCase{
		repo:         repo,
		workerClient: workerClient,
		logger:       logger,
	}
}

func (uc *VideoGeneratorUseCase) CreateGeneration(ctx context.Context, prompt string) (string, error) {
	uc.logger.Info("Creating new generation", "prompt", prompt)
	video := &domain.Generation{
		ID:        generateUniqueID(),
		Prompt:    prompt,
		Status:    domain.StatusPending,
		UpdatedAt: time.Now(),
	}
	if err := uc.repo.Save(ctx, video); err != nil {
		uc.logger.Error("Failed to save video", "error", err)
		return "", fmt.Errorf("failed to save video: %w", err)
	}
	go uc.processGeneration(video)
	uc.logger.Info("Generation created", "id", video.ID)
	return video.ID, nil
}

func (uc *VideoGeneratorUseCase) GetGenerationStatus(ctx context.Context, id string) (*domain.Generation, error) {
	uc.logger.Info("Getting generation status", "id", id)
	video, err := uc.repo.FindByID(ctx, id)
	if err != nil {
		uc.logger.Error("Failed to find video", "id", id, "error", err)
		return nil, fmt.Errorf("failed to find video: %w", err)
	}
	uc.logger.Info("Generation status retrieved", "id", id, "status", video.Status)
	return video, nil
}

func (uc *VideoGeneratorUseCase) StreamGenerationStatus(ctx context.Context, id string, sendUpdate func(*domain.Generation) error) error {
	uc.logger.Info("Starting to stream generation status", "id", id)
	for {
		select {
		case <-ctx.Done():
			uc.logger.Info("Streaming stopped due to context cancellation", "id", id)
			return ctx.Err()
		default:
			video, err := uc.GetGenerationStatus(ctx, id)
			if err != nil {
				uc.logger.Error("Failed to get generation status", "id", id, "error", err)
				return err
			}
			if err := sendUpdate(video); err != nil {
				uc.logger.Error("Failed to send update", "id", id, "error", err)
				return err
			}
			if video.Status == domain.StatusCompleted || video.Status == domain.StatusFailed {
				uc.logger.Info("Streaming ended", "id", id, "finalStatus", video.Status)
				return nil
			}
			time.Sleep(1 * time.Second)
		}
	}
}

func (uc *VideoGeneratorUseCase) processGeneration(video *domain.Generation) {
	ctx := context.Background()
	uc.logger.Info("Starting generation process", "id", video.ID)

	// スクリプト生成
	uc.updateStatus(ctx, video, domain.StatusProcessing, "", "")
	script, err := uc.workerClient.GenerateManimScript(ctx, video.ID, video.Prompt)
	if err != nil {
		uc.logger.Error("Failed to generate Manim script", "id", video.ID, "error", err)
		uc.updateStatus(ctx, video, domain.StatusFailed, "", err.Error())
		return
	}
	uc.logger.Info("Manim script generated", "id", video.ID)

	// ビデオ生成
	videoURL, err := uc.workerClient.GenerateManimVideo(ctx, video.ID, script)
	if err != nil {
		uc.logger.Error("Failed to generate Manim video", "id", video.ID, "error", err)
		uc.updateStatus(ctx, video, domain.StatusFailed, "", err.Error())
		return
	}
	uc.logger.Info("Manim video generated", "id", video.ID, "url", videoURL)

	// 完了
	uc.updateStatus(ctx, video, domain.StatusCompleted, videoURL, "")
	uc.logger.Info("Generation process completed", "id", video.ID)
}

func (uc *VideoGeneratorUseCase) updateStatus(ctx context.Context, video *domain.Generation, status domain.GenerationStatus, videoURL string, errorMessage string) {
	uc.logger.Info("Updating video status", "id", video.ID, "newStatus", status)
	video.Status = status
	video.UpdatedAt = time.Now()
	if videoURL != "" {
		video.VideoURL = videoURL
	}
	if errorMessage != "" {
		video.ErrorMessage = errorMessage
	}
	if err := uc.repo.Update(ctx, video); err != nil {
		uc.logger.Error("Failed to update video status", "id", video.ID, "error", err)
	}
}

func (uc *VideoGeneratorUseCase) HealthCheck(ctx context.Context) error {
	if err := uc.workerClient.HealthCheck(ctx); err != nil {
		uc.logger.Error("Worker health check failed", "error", err)
		return fmt.Errorf("worker health check failed: %w", err)
	}
	return nil
}

func generateUniqueID() string {
	return uuid.New().String()
}
