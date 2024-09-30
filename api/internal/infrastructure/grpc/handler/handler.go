package handler

import (
	"context"
	"log/slog"
	"time"

	"github.com/KinjiKawaguchi/text2manim/api/internal/usecase"
	pb "github.com/KinjiKawaguchi/text2manim/api/pkg/pb/text2manim/v1"
)

type Handler struct {
	pb.UnimplementedText2ManimServiceServer
	useCase *usecase.VideoGeneratorUseCase
	logger  *slog.Logger
}

func NewHandler(useCase *usecase.VideoGeneratorUseCase, logger *slog.Logger) *Handler {
	return &Handler{useCase: useCase, logger: logger}
}

func (h *Handler) CreateGeneration(ctx context.Context, req *pb.CreateGenerationRequest) (*pb.CreateGenerationResponse, error) {
	h.logger.Info("CreateGeneration request received", "prompt", req.Prompt)
	startTime := time.Now()

	id, err := h.useCase.CreateGeneration(ctx, req.Prompt)
	if err != nil {
		h.logger.Error("Failed to create generation", "error", err)
		return nil, err
	}

	duration := time.Since(startTime)
	h.logger.Info("CreateGeneration completed", "requestID", id, "duration", duration)
	return &pb.CreateGenerationResponse{RequestId: id}, nil
}

func (h *Handler) GetGenerationStatus(ctx context.Context, req *pb.GetGenerationStatusRequest) (*pb.GetGenerationStatusResponse, error) {
	h.logger.Info("GetGenerationStatus request received", "requestID", req.RequestId)
	startTime := time.Now()

	video, err := h.useCase.GetGenerationStatus(ctx, req.RequestId)
	if err != nil {
		h.logger.Error("Failed to get generation status", "requestID", req.RequestId, "error", err)
		return nil, err
	}

	response := &pb.GetGenerationStatusResponse{
		GenerationStatus: &pb.GenerationStatus{
			Status:   pb.GenerationStatus_Status(video.Status),
			VideoUrl: video.VideoURL,
			Prompt:   video.Prompt,
		},
	}

	duration := time.Since(startTime)
	h.logger.Info("GetGenerationStatus completed",
		"requestID", req.RequestId,
		"status", response.GenerationStatus.Status,
		"duration", duration)
	return response, nil
}

func (h *Handler) StreamGenerationStatus(req *pb.StreamGenerationStatusRequest, stream pb.Text2ManimService_StreamGenerationStatusServer) error {
	h.logger.Warn("StreamGenerationStatus called but not implemented")
	return nil
}