package middleware

import (
	"context"
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
}

func NewAuthMiddleware(cfg *config.Config) *AuthMiddleware {
	return &AuthMiddleware{config: cfg}
}

func (am *AuthMiddleware) UnaryInterceptor() grpc.UnaryServerInterceptor {
	return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
		if err := am.authorize(ctx); err != nil {
			return nil, err
		}
		return handler(ctx, req)
	}
}

func (am *AuthMiddleware) StreamInterceptor() grpc.StreamServerInterceptor {
	return func(srv interface{}, ss grpc.ServerStream, info *grpc.StreamServerInfo, handler grpc.StreamHandler) error {
		if err := am.authorize(ss.Context()); err != nil {
			return err
		}
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
		return status.Error(codes.Unauthenticated, "unable to get peer info")
	}

	ip, _, err := net.SplitHostPort(p.Addr.String())
	if err != nil {
		return status.Error(codes.Unauthenticated, "unable to get IP address")
	}

	for _, allowedIP := range am.config.IPWhitelist {
		if allowedIP == ip {
			return nil
		}
	}

	return status.Error(codes.PermissionDenied, "IP not in whitelist")
}

func (am *AuthMiddleware) checkAPIKey(ctx context.Context) error {
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return status.Error(codes.Unauthenticated, "unable to get metadata")
	}

	apiKeys := md.Get("x-api-key")
	if len(apiKeys) == 0 {
		return status.Error(codes.Unauthenticated, "API key not provided")
	}

	apiKey := apiKeys[0]
	if serviceInfo, exists := am.config.APIKeys[apiKey]; exists {
		// ここで必要に応じて追加の権限チェックを行うことができます
		ctx = context.WithValue(ctx, "service", serviceInfo.Service)
		return nil
	}

	return status.Error(codes.Unauthenticated, "invalid API key")
}
