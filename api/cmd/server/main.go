package main

import (
	"fmt"
	"log/slog"
	"net"
	"os"

	"github.com/KinjiKawaguchi/text2manim/api/internal/config"
	"github.com/KinjiKawaguchi/text2manim/api/internal/infrastructure/grpc/handler"
	"github.com/KinjiKawaguchi/text2manim/api/internal/infrastructure/repository"
	"github.com/KinjiKawaguchi/text2manim/api/internal/infrastructure/worker"
	"github.com/KinjiKawaguchi/text2manim/api/internal/middleware"
	"github.com/KinjiKawaguchi/text2manim/api/internal/usecase"
	pb "github.com/KinjiKawaguchi/text2manim/api/pkg/pb/text2manim/v1"
	"google.golang.org/grpc"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
	slog.SetDefault(logger)

	cfg, err := config.LoadConfig(logger)
	if err != nil {
		logger.Error("Failed to load config", "error", err)
		os.Exit(1)
	}

	// 新しいリポジトリファクトリー関数を使用
	repo, err := repository.NewVideoRepository(cfg, logger)
	if err != nil {
		logger.Error("Failed to create video repository", "error", err)
		os.Exit(1)
	}

	// PostgreSQLを使用している場合、アプリケーション終了時にDBコネクションを閉じる
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
