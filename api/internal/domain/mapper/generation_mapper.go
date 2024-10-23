package mapper

import (
	pb "github.com/KinjiKawaguchi/text2manim/api/pkg/pb/text2manim/v1"
	"google.golang.org/protobuf/types/known/timestamppb"

	"github.com/KinjiKawaguchi/text2manim/api/internal/domain/ent"
	"github.com/KinjiKawaguchi/text2manim/api/internal/domain/ent/generation"
)

func ToProto(video *ent.Generation) *pb.GenerationStatus {
	var status pb.GenerationStatus_Status
	switch video.Status {
	case generation.StatusUnspecified:
		status = pb.GenerationStatus_STATUS_UNSPECIFIED
	case generation.StatusPending:
		status = pb.GenerationStatus_STATUS_PENDING
	case generation.StatusProcessing:
		status = pb.GenerationStatus_STATUS_PROCESSING
	case generation.StatusCompleted:
		status = pb.GenerationStatus_STATUS_COMPLETED
	case generation.StatusFailed:
		status = pb.GenerationStatus_STATUS_FAILED
	default:
		status = pb.GenerationStatus_STATUS_UNSPECIFIED
	}

	return &pb.GenerationStatus{
		RequestId:    video.ID.String(),
		Prompt:       video.Prompt,
		Status:       status,
		VideoUrl:     video.VideoURL,
		ScriptUrl:    video.ScriptURL,
		ErrorMessage: video.ErrorMessage,
		CreatedAt:    timestamppb.New(video.CreatedAt),
		UpdatedAt:    timestamppb.New(video.UpdatedAt),
	}
}
