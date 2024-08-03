package usecase

import (
	"context"
	"fmt"
	"time"

	"github.com/KinjiKawaguchi/text2manim/api/internal/domain"
	"github.com/KinjiKawaguchi/text2manim/api/internal/interface/repository"
	"github.com/KinjiKawaguchi/text2manim/api/internal/interface/worker"
)

type VideoGeneratorUseCase struct {
	repo         repository.VideoRepository
	workerClient worker.WorkerClient
}

func NewVideoGeneratorUseCase(repo repository.VideoRepository, workerClient worker.WorkerClient) *VideoGeneratorUseCase {
	return &VideoGeneratorUseCase{
		repo:         repo,
		workerClient: workerClient,
	}
}

func (uc *VideoGeneratorUseCase) CreateGeneration(ctx context.Context, prompt string) (string, error) {
	video := &domain.Video{
		ID:        generateUniqueID(),
		Prompt:    prompt,
		Status:    domain.StatusPending,
		UpdatedAt: time.Now(),
	}

	if err := uc.repo.Save(ctx, video); err != nil {
		return "", fmt.Errorf("failed to save video: %w", err)
	}

	go uc.processGeneration(video)

	return video.ID, nil
}

func (uc *VideoGeneratorUseCase) GetGenerationStatus(ctx context.Context, id string) (*domain.Video, error) {
	video, err := uc.repo.FindByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to find video: %w", err)
	}

	return video, nil
}

func (uc *VideoGeneratorUseCase) StreamGenerationStatus(ctx context.Context, id string, sendUpdate func(*domain.Video) error) error {
	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
			video, err := uc.GetGenerationStatus(ctx, id)
			if err != nil {
				return err
			}

			if err := sendUpdate(video); err != nil {
				return err
			}

			if video.Status == domain.StatusCompleted || video.Status == domain.StatusFailed {
				return nil
			}

			time.Sleep(1 * time.Second)
		}
	}
}

func (uc *VideoGeneratorUseCase) processGeneration(video *domain.Video) {
	ctx := context.Background()

	// スクリプト生成
	uc.updateStatus(ctx, video, domain.StatusProcessing)
	script, err := uc.workerClient.GenerateManimScript(ctx, video.ID, video.Prompt)
	if err != nil {
		uc.updateStatus(ctx, video, domain.StatusFailed)
		return
	}

	// ビデオ生成
	videoURL, err := uc.workerClient.GenerateManimVideo(ctx, video.ID, script)
	if err != nil {
		uc.updateStatus(ctx, video, domain.StatusFailed)
		return
	}

	// 完了
	uc.updateStatus(ctx, video, domain.StatusCompleted, videoURL)
}

func (uc *VideoGeneratorUseCase) updateStatus(ctx context.Context, video *domain.Video, status domain.VideoStatus, videoURL ...string) {
	video.Status = status
	video.UpdatedAt = time.Now()
	if len(videoURL) > 0 {
		video.VideoURL = videoURL[0]
	}

	if err := uc.repo.Update(ctx, video); err != nil {
		// エラーログを記録するべきですが、処理は続行します
		fmt.Printf("Failed to update video status: %v\n", err)
	}
}

func generateUniqueID() string {
	return fmt.Sprintf("vid_%d", time.Now().UnixNano())
}
