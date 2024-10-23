package usecase

import (
	"context"
	"fmt"
	"log/slog"

	"github.com/KinjiKawaguchi/text2manim/api/internal/domain/ent"
	"github.com/KinjiKawaguchi/text2manim/api/internal/domain/ent/generation"
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
	video := &ent.Generation{
		Prompt: prompt,
		Status: generation.StatusPending,
	}
	video, err := uc.repo.Save(ctx, video)
	if err != nil {
		uc.logger.Error("Failed to create video", "error", err)
		return "", fmt.Errorf("failed to create video: %w", err)
	}
	go uc.processGeneration(video)
	uc.logger.Info("Generation created", "id", video.ID)
	return video.ID.String(), nil
}

func (uc *VideoGeneratorUseCase) GetGenerationStatus(ctx context.Context, id string) (*ent.Generation, error) {
	uc.logger.Info("Getting generation status", "id", id)
	uuid, err := uuid.Parse(id)
	if err != nil {
		uc.logger.Error("Failed to parse UUID", "id", id, "error", err)
		return nil, fmt.Errorf("invalid id: %w", err)
	}
	video, err := uc.repo.FindByID(ctx, uuid)
	if err != nil {
		uc.logger.Error("Failed to find video", "id", id, "error", err)
		return nil, fmt.Errorf("failed to find video: %w", err)
	}
	uc.logger.Info("Generation status retrieved", "id", id, "status", video.Status)
	return video, nil
}

func (uc *VideoGeneratorUseCase) StreamGenerationStatus(ctx context.Context, id string, sendUpdate func(*ent.Generation) error) error {
	panic("not implemented")
}

func (uc *VideoGeneratorUseCase) processGeneration(video *ent.Generation) {
	ctx := context.Background()
	uc.logger.Info("Starting generation process", "id", video.ID)

	// スクリプト生成
	uc.updateStatus(ctx, video, generation.StatusProcessing, "", "")
	script, err := uc.workerClient.GenerateManimScript(ctx, video.ID.String(), video.Prompt)
	if err != nil {
		uc.logger.Error("Failed to generate Manim script", "id", video.ID, "error", err)
		uc.updateStatus(ctx, video, generation.StatusFailed, "", err.Error())
		return
	}
	uc.logger.Info("Manim script generated", "id", video.ID)

	// ビデオ生成
	videoURL, err := uc.workerClient.GenerateManimVideo(ctx, video.ID.String(), script)
	if err != nil {
		uc.logger.Error("Failed to generate Manim video", "id", video.ID, "error", err)
		uc.updateStatus(ctx, video, generation.StatusFailed, "", err.Error())
		return
	}
	uc.logger.Info("Manim video generated", "id", video.ID, "url", videoURL)

	// 完了
	uc.updateStatus(ctx, video, generation.StatusCompleted, videoURL, "")
	uc.logger.Info("Generation process completed", "id", video.ID)
}

func (uc *VideoGeneratorUseCase) updateStatus(ctx context.Context, video *ent.Generation, status generation.Status, videoURL string, errorMessage string) {
	uc.logger.Info("Updating video status", "id", video.ID, "newStatus", status)
	video.Status = status
	video.VideoURL = videoURL
	video.ErrorMessage = errorMessage
	update, err := uc.repo.Update(ctx, video)
	if err != nil {
		uc.logger.Error("Failed to update video status", "id", video.ID, "error", err)
		return
	}
	uc.logger.Info("Video status updated", "id", video.ID, "newStatus", update.Status)
}

func (uc *VideoGeneratorUseCase) HealthCheck(ctx context.Context) error {
	if err := uc.workerClient.HealthCheck(ctx); err != nil {
		uc.logger.Error("Worker health check failed", "error", err)
		return fmt.Errorf("worker health check failed: %w", err)
	}
	return nil
}
