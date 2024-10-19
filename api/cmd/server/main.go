package main

import (
	"context"
	"fmt"
	"log/slog"
	"net"
	"os"
	"time"

	"github.com/KinjiKawaguchi/text2manim/api/internal/config"
	"github.com/KinjiKawaguchi/text2manim/api/internal/infrastructure/grpc/handler"
	"github.com/KinjiKawaguchi/text2manim/api/internal/infrastructure/repository"
	"github.com/KinjiKawaguchi/text2manim/api/internal/infrastructure/worker"
	"github.com/KinjiKawaguchi/text2manim/api/internal/middleware"
	"github.com/KinjiKawaguchi/text2manim/api/internal/usecase"
	pb "github.com/KinjiKawaguchi/text2manim/api/pkg/pb/text2manim/v1"
	"google.golang.org/grpc"
	"google.golang.org/protobuf/types/known/emptypb"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
	slog.SetDefault(logger)

	cfg, err := config.LoadConfig(logger)
	if err != nil {
		logger.Error("Failed to load config", "error", err)
		os.Exit(1)
	}

	repo, err := repository.NewVideoRepository(cfg, logger)
	if err != nil {
		logger.Error("Failed to create video repository", "error", err)
		os.Exit(1)
	}

	if closer, ok := repo.(interface{ Close() error }); ok {
		defer func() {
			if err := closer.Close(); err != nil {
				logger.Error("Failed to close database connection", "error", err)
			}
		}()
	}

	workerClient, err := worker.NewGRPCWorkerClient(cfg.WorkerAddr, logger)
	if err != nil {
		logger.Error("Failed to create worker client", "error", err)
		os.Exit(1)
	}

	useCase := usecase.NewVideoGeneratorUseCase(repo, workerClient, logger)
	handler := handler.NewHandler(useCase, logger)

	// 1分間ヘルスチェックをリトライする
	ctx, cancel := context.WithTimeout(context.Background(), time.Minute)
	defer cancel()

	for {
		select {
		case <-ctx.Done():
			logger.Error("Health check failed after 1 minute of retrying")
			os.Exit(1)
		default:
			_, err = handler.HealthCheck(ctx, &emptypb.Empty{})
			if err == nil {
				logger.Info("Health check passed")
				break
			}
			logger.Warn("Health check failed, retrying...", "error", err)
			time.Sleep(time.Second) // 1秒待ってからリトライ
		}
		if err == nil {
			break
		}
	}

	authMiddleware := middleware.NewAuthMiddleware(cfg, logger)
	server := grpc.NewServer(
		grpc.UnaryInterceptor(authMiddleware.UnaryInterceptor()),
		grpc.StreamInterceptor(authMiddleware.StreamInterceptor()),
	)
	pb.RegisterText2ManimServiceServer(server, handler)

	lis, err := net.Listen("tcp", fmt.Sprintf("0.0.0.0:%s", cfg.ServerPort))
	if err != nil {
		logger.Error("Failed to listen", "error", err, "port", cfg.ServerPort)
		os.Exit(1)
	}

	logger.Info("Server started", "port", cfg.ServerPort)
	if err := server.Serve(lis); err != nil {
		logger.Error("Failed to serve", "error", err)
		os.Exit(1)
	}
}
