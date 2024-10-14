package main

import (
	"context"
	"log/slog"
	"net"
	"net/http"
	"os"

	"github.com/KinjiKawaguchi/text2manim/api/internal/config"
	pb "github.com/KinjiKawaguchi/text2manim/api/pkg/pb/text2manim/v1"
	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/metadata"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))

	cfg, err := config.LoadConfig(logger)
	if err != nil {
		logger.Error("Failed to load config", "error", err)
		os.Exit(1)
	}

	ctx := context.Background()
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	mux := runtime.NewServeMux(
		runtime.WithIncomingHeaderMatcher(CustomMatcher),
		runtime.WithMetadata(addOriginalIPMetadata),
	)
	opts := []grpc.DialOption{grpc.WithTransportCredentials(insecure.NewCredentials())}

	err = pb.RegisterText2ManimServiceHandlerFromEndpoint(ctx, mux, cfg.GrpcServerAddress, opts)
	if err != nil {
		logger.Error("Failed to register gRPC gateway", "error", err)
		os.Exit(1)
	}

	logger.Info("Starting HTTP server", "address", ":8080")
	if err := http.ListenAndServe(":8080", loggingMiddleware(mux, logger)); err != nil {
		logger.Error("Failed to serve HTTP", "error", err)
		os.Exit(1)
	}
}

func addOriginalIPMetadata(ctx context.Context, r *http.Request) metadata.MD {
	ip, _, _ := net.SplitHostPort(r.RemoteAddr)
	return metadata.Pairs("x-original-ip", ip)
}

func CustomMatcher(key string) (string, bool) {
	switch key {
	case "X-Api-Key":
		return key, true
	case "X-Original-Ip":
		// このヘッダーは転送しない
		return "", false
	default:
		return runtime.DefaultHeaderMatcher(key)
	}
}

func loggingMiddleware(next http.Handler, logger *slog.Logger) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		logger.Info("Received request",
			"method", r.Method,
			"path", r.URL.Path,
			"remote_addr", r.RemoteAddr,
		)
		next.ServeHTTP(w, r)
	})
}
