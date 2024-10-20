package handler

import (
	"context"
	"log/slog"
	"time"

	"github.com/KinjiKawaguchi/text2manim/api/internal/usecase"
	pb "github.com/KinjiKawaguchi/text2manim/api/pkg/pb/text2manim/v1"
	"google.golang.org/protobuf/types/known/emptypb"
	"google.golang.org/protobuf/types/known/timestamppb"
)

type Handler struct {
	pb.Text2ManimServiceServer
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
			RequestId:    req.RequestId,
			Status:       pb.GenerationStatus_Status(video.Status),
			VideoUrl:     video.VideoURL,
			ScriptUrl:    "", // TODO: Implement script URL https://github.com/KinjiKawaguchi/text2manim/issues/32
			ErrorMessage: video.ErrorMessage,
			Prompt:       video.Prompt,
			CreatedAt:    timestamppb.New(video.CreatedAt),
			UpdatedAt:    timestamppb.New(video.UpdatedAt),
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

func (h *Handler) HealthCheck(ctx context.Context, req *emptypb.Empty) (*emptypb.Empty, error) {
	h.logger.Info("HealthCheck request received")
	if err := h.useCase.HealthCheck(ctx); err != nil {
		h.logger.Error("HealthCheck failed", "error", err)
		return nil, err
	}
	h.logger.Info("HealthCheck completed")
	return &emptypb.Empty{}, nil
}
