package handler

import (
	"context"

	"github.com/KinjiKawaguchi/text2manim/api/internal/usecase"
	pb "github.com/KinjiKawaguchi/text2manim/api/pkg/pb/text2manim/v1"
)

type Handler struct {
	pb.UnimplementedText2ManimServiceServer
	useCase *usecase.VideoGeneratorUseCase
}

func NewHandler(useCase *usecase.VideoGeneratorUseCase) *Handler {
	return &Handler{useCase: useCase}
}

func (h *Handler) CreateGeneration(ctx context.Context, req *pb.CreateGenerationRequest) (*pb.CreateGenerationResponse, error) {
	id, err := h.useCase.CreateGeneration(ctx, req.Prompt)
	if err != nil {
		return nil, err
	}
	return &pb.CreateGenerationResponse{RequestId: id}, nil
}

func (h *Handler) GetGenerationStatus(ctx context.Context, req *pb.GetGenerationStatusRequest) (*pb.GetGenerationStatusResponse, error) {
	video, err := h.useCase.GetGenerationStatus(ctx, req.RequestId)
	if err != nil {
		return nil, err
	}

	return &pb.GetGenerationStatusResponse{
		GenerationStatus: &pb.GenerationStatus{
			Status:   pb.GenerationStatus_Status(video.Status),
			VideoUrl: video.VideoURL,
			Prompt:   video.Prompt,
		},
	}, nil
}

func (h *Handler) StreamGenerationStatus(req *pb.StreamGenerationStatusRequest, stream pb.Text2ManimService_StreamGenerationStatusServer) error {
	panic("unimplemented")
}
