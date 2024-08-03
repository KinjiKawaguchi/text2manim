package worker

import (
	"context"
	"fmt"

	pb "github.com/KinjiKawaguchi/text2manim/api/pkg/pb/text2manim/v1"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type GRPCWorkerClient struct {
	client pb.WorkerServiceClient
}

func NewGRPCWorkerClient(address string) (*GRPCWorkerClient, error) {
	conn, err := grpc.NewClient(address, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return nil, fmt.Errorf("failed to connect to worker: %w", err)
	}

	client := pb.NewWorkerServiceClient(conn)
	return &GRPCWorkerClient{client: client}, nil
}

func (c *GRPCWorkerClient) GenerateManimScript(ctx context.Context, taskID, prompt string) (string, error) {
	request := &pb.GenerateManimScriptRequest{
		TaskId: taskID,
		Prompt: prompt,
	}

	response, err := c.client.GenerateManimScript(ctx, request)
	if err != nil {
		return "", fmt.Errorf("failed to generate Manim script: %w", err)
	}

	return response.Script, nil
}

func (c *GRPCWorkerClient) GenerateManimVideo(ctx context.Context, taskID, script string) (string, error) {
	request := &pb.GenerateManimVideoRequest{
		TaskId: taskID,
		Script: script,
	}

	response, err := c.client.GenerateManimVideo(ctx, request)
	if err != nil {
		return "", fmt.Errorf("failed to generate Manim video: %w", err)
	}

	if !response.Success {
		return "", fmt.Errorf("video generation failed: %s", response.ErrorMessage)
	}

	return response.VideoUrl, nil
}
