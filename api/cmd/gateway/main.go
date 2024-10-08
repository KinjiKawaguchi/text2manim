package main

import (
	"context"
	"fmt"
	"log/slog"
	"net/http"
	"os"

	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	pb "github.com/KinjiKawaguchi/text2manim/api/pkg/pb/text2manim/v1"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

const grpcServerAddress = "api:50051"

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: logLevel}))
	slog.SetDefault(logger)

	ctx := context.Background()
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	mux := runtime.NewServeMux(
		runtime.WithIncomingHeaderMatcher(CustomMatcher),
	)
	opts := []grpc.DialOption{grpc.WithTransportCredentials(insecure.NewCredentials())}

	err := pb.RegisterText2ManimServiceHandlerFromEndpoint(ctx, mux, grpcServerAddress, opts)
	if err != nil {
		slog.Error("Failed to register gRPC gateway", "error", err)
		os.Exit(1)
	}

	slog.Info("Starting HTTP server", "address", ":8080")
	if err := http.ListenAndServe(":8080", loggingMiddleware(mux)); err != nil {
		slog.Error("Failed to serve HTTP", "error", err)
		os.Exit(1)
	}
}

func CustomMatcher(key string) (string, bool) {
	switch key {
	case "X-Api-Key":
		return key, true
	default:
		return runtime.DefaultHeaderMatcher(key)
	}
}

func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		slog.Info("Received request",
			"method", r.Method,
			"path", r.URL.Path,
			"remote_addr", r.RemoteAddr,
		)
		next.ServeHTTP(w, r)
	})
}