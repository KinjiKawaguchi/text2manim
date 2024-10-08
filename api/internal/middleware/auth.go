package middleware

import (
	"context"
	"log/slog"
	"net"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/peer"
	"google.golang.org/grpc/status"

	"github.com/KinjiKawaguchi/text2manim/api/internal/config"
)

type AuthMiddleware struct {
	config *config.Config
	logger *slog.Logger
}

func NewAuthMiddleware(cfg *config.Config, logger *slog.Logger) *AuthMiddleware {
	return &AuthMiddleware{config: cfg, logger: logger}
}

func (am *AuthMiddleware) UnaryInterceptor() grpc.UnaryServerInterceptor {
	return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
		am.logger.Info("Unary interceptor called", "method", info.FullMethod)
		if err := am.authorize(ctx); err != nil {
			am.logger.Warn("Authorization failed", "method", info.FullMethod, "error", err)
			return nil, err
		}
		am.logger.Info("Authorization successful", "method", info.FullMethod)
		return handler(ctx, req)
	}
}

func (am *AuthMiddleware) StreamInterceptor() grpc.StreamServerInterceptor {
	return func(srv interface{}, ss grpc.ServerStream, info *grpc.StreamServerInfo, handler grpc.StreamHandler) error {
		am.logger.Info("Stream interceptor called", "method", info.FullMethod)
		if err := am.authorize(ss.Context()); err != nil {
			am.logger.Warn("Authorization failed", "method", info.FullMethod, "error", err)
			return err
		}
		am.logger.Info("Authorization successful", "method", info.FullMethod)
		return handler(srv, ss)
	}
}

func (am *AuthMiddleware) authorize(ctx context.Context) error {
	if err := am.checkIPWhitelist(ctx); err != nil {
		return err
	}
	return am.checkAPIKey(ctx)
}

func (am *AuthMiddleware) checkIPWhitelist(ctx context.Context) error {
	p, ok := peer.FromContext(ctx)
	if !ok {
		am.logger.Error("Unable to get peer info")
		return status.Error(codes.Unauthenticated, "unable to get peer info")
	}
	ip, _, err := net.SplitHostPort(p.Addr.String())
	if err != nil {
		am.logger.Error("Unable to get IP address", "error", err)
		return status.Error(codes.Unauthenticated, "unable to get IP address")
	}
	for _, allowedIP := range am.config.IPWhitelist {
		if allowedIP == ip {
			am.logger.Info("IP whitelisting successful", "ip", ip)
			return nil
		}
	}
	am.logger.Warn("IP not in whitelist", "ip", ip)
	return status.Error(codes.PermissionDenied, "IP not in whitelist")
}

func (am *AuthMiddleware) checkAPIKey(ctx context.Context) error {
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		am.logger.Error("Unable to get metadata")
		return status.Error(codes.Unauthenticated, "unable to get metadata")
	}
	apiKeys := md.Get("x-api-key")
	if len(apiKeys) == 0 {
		am.logger.Warn("API key not provided")
		return status.Error(codes.Unauthenticated, "API key not provided")
	}
	apiKey := apiKeys[0]
	if serviceInfo, exists := am.config.APIKeys[apiKey]; exists {
		am.logger.Info("API key validation successful", "service", serviceInfo.Service)
		// ここで必要に応じて追加の権限チェックを行うことができます
		// ctx = context.WithValue(ctx, "service", serviceInfo.Service)
		return nil
	}
	am.logger.Warn("Invalid API key")
	return status.Error(codes.Unauthenticated, "invalid API key")
}