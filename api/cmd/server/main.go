package main

import (
	"fmt"
	"log"
	"net"

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
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	repo := repository.NewMemoryVideoRepository()
	workerClient, err := worker.NewGRPCWorkerClient(cfg.WorkerAddr)
	if err != nil {
		log.Fatalf("Failed to create worker client: %v", err)
	}

	useCase := usecase.NewVideoGeneratorUseCase(repo, workerClient)
	handler := handler.NewHandler(useCase)

	authMiddleware := middleware.NewAuthMiddleware(cfg)

	server := grpc.NewServer(
		grpc.UnaryInterceptor(authMiddleware.UnaryInterceptor()),
		grpc.StreamInterceptor(authMiddleware.StreamInterceptor()),
	)

	pb.RegisterText2ManimServiceServer(server, handler)

	lis, err := net.Listen("tcp", fmt.Sprintf("0.0.0.0:%s", cfg.ServerPort))
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	log.Printf("Server started on %s", cfg.ServerPort)
	if err := server.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
