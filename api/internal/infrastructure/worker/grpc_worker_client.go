package worker

import (
	"context"
	"fmt"
	"log/slog"
	"time"

	pb "github.com/KinjiKawaguchi/text2manim/api/pkg/pb/text2manim/v1"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
)

type GRPCWorkerClient struct {
	client pb.WorkerServiceClient
	logger *slog.Logger
}

func NewGRPCWorkerClient(address string, logger *slog.Logger) (*GRPCWorkerClient, error) {
	logger.Info("Connecting to worker", "address", address)
	creds := credentials.NewClientTLSFromCert(nil, "")
	conn, err := grpc.NewClient(address, grpc.WithTransportCredentials(creds))
	if err != nil {
		logger.Error("Failed to connect to worker", "error", err)
		return nil, fmt.Errorf("failed to connect to worker: %w", err)
	}
	client := pb.NewWorkerServiceClient(conn)
	logger.Info("Successfully connected to worker")
	return &GRPCWorkerClient{client: client, logger: logger}, nil
}

func (c *GRPCWorkerClient) GenerateManimScript(ctx context.Context, taskID, prompt string) (string, error) {
	c.logger.Info("Generating Manim script", "taskID", taskID)
	startTime := time.Now()

	request := &pb.GenerateManimScriptRequest{
		TaskId: taskID,
		Prompt: prompt,
	}
	response, err := c.client.GenerateManimScript(ctx, request)
	if err != nil {
		c.logger.Error("Failed to generate Manim script", "taskID", taskID, "error", err)
		return "", fmt.Errorf("failed to generate Manim script: %w", err)
	}

	duration := time.Since(startTime)
	c.logger.Info("Successfully generated Manim script", "taskID", taskID, "duration", duration)
	return response.Script, nil
}

func (c *GRPCWorkerClient) GenerateManimVideo(ctx context.Context, taskID, script string) (string, error) {
	c.logger.Info("Generating Manim video", "taskID", taskID)
	startTime := time.Now()

	request := &pb.GenerateManimVideoRequest{
		TaskId: taskID,
		Script: script,
	}
	response, err := c.client.GenerateManimVideo(ctx, request)
	if err != nil {
		c.logger.Error("Failed to generate Manim video", "taskID", taskID, "error", err)
		return "", fmt.Errorf("failed to generate Manim video: %w", err)
	}
	if !response.Success {
		c.logger.Error("Video generation failed", "taskID", taskID, "errorMessage", response.ErrorMessage)
		return "", fmt.Errorf("video generation failed: %s", response.ErrorMessage)
	}

	duration := time.Since(startTime)
	c.logger.Info("Successfully generated Manim video", "taskID", taskID, "duration", duration, "videoURL", response.VideoUrl)
	return response.VideoUrl, nil
}
