// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.4.0
// - protoc             (unknown)
// source: text2manim/v1/worker.proto

package text2manim_v1

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	emptypb "google.golang.org/protobuf/types/known/emptypb"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.62.0 or later.
const _ = grpc.SupportPackageIsVersion8

const (
	WorkerService_GenerateManimScript_FullMethodName = "/text2manim.v1.WorkerService/GenerateManimScript"
	WorkerService_GenerateManimVideo_FullMethodName  = "/text2manim.v1.WorkerService/GenerateManimVideo"
	WorkerService_HealthCheck_FullMethodName         = "/text2manim.v1.WorkerService/HealthCheck"
)

// WorkerServiceClient is the client API for WorkerService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type WorkerServiceClient interface {
	GenerateManimScript(ctx context.Context, in *GenerateManimScriptRequest, opts ...grpc.CallOption) (*GenerateManimScriptResponse, error)
	GenerateManimVideo(ctx context.Context, in *GenerateManimVideoRequest, opts ...grpc.CallOption) (*GenerateManimVideoResponse, error)
	HealthCheck(ctx context.Context, in *emptypb.Empty, opts ...grpc.CallOption) (*emptypb.Empty, error)
}

type workerServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewWorkerServiceClient(cc grpc.ClientConnInterface) WorkerServiceClient {
	return &workerServiceClient{cc}
}

func (c *workerServiceClient) GenerateManimScript(ctx context.Context, in *GenerateManimScriptRequest, opts ...grpc.CallOption) (*GenerateManimScriptResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(GenerateManimScriptResponse)
	err := c.cc.Invoke(ctx, WorkerService_GenerateManimScript_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *workerServiceClient) GenerateManimVideo(ctx context.Context, in *GenerateManimVideoRequest, opts ...grpc.CallOption) (*GenerateManimVideoResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(GenerateManimVideoResponse)
	err := c.cc.Invoke(ctx, WorkerService_GenerateManimVideo_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *workerServiceClient) HealthCheck(ctx context.Context, in *emptypb.Empty, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, WorkerService_HealthCheck_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// WorkerServiceServer is the server API for WorkerService service.
// All implementations must embed UnimplementedWorkerServiceServer
// for forward compatibility
type WorkerServiceServer interface {
	GenerateManimScript(context.Context, *GenerateManimScriptRequest) (*GenerateManimScriptResponse, error)
	GenerateManimVideo(context.Context, *GenerateManimVideoRequest) (*GenerateManimVideoResponse, error)
	HealthCheck(context.Context, *emptypb.Empty) (*emptypb.Empty, error)
	mustEmbedUnimplementedWorkerServiceServer()
}

// UnimplementedWorkerServiceServer must be embedded to have forward compatible implementations.
type UnimplementedWorkerServiceServer struct {
}

func (UnimplementedWorkerServiceServer) GenerateManimScript(context.Context, *GenerateManimScriptRequest) (*GenerateManimScriptResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GenerateManimScript not implemented")
}
func (UnimplementedWorkerServiceServer) GenerateManimVideo(context.Context, *GenerateManimVideoRequest) (*GenerateManimVideoResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GenerateManimVideo not implemented")
}
func (UnimplementedWorkerServiceServer) HealthCheck(context.Context, *emptypb.Empty) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method HealthCheck not implemented")
}
func (UnimplementedWorkerServiceServer) mustEmbedUnimplementedWorkerServiceServer() {}

// UnsafeWorkerServiceServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to WorkerServiceServer will
// result in compilation errors.
type UnsafeWorkerServiceServer interface {
	mustEmbedUnimplementedWorkerServiceServer()
}

func RegisterWorkerServiceServer(s grpc.ServiceRegistrar, srv WorkerServiceServer) {
	s.RegisterService(&WorkerService_ServiceDesc, srv)
}

func _WorkerService_GenerateManimScript_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GenerateManimScriptRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(WorkerServiceServer).GenerateManimScript(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: WorkerService_GenerateManimScript_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(WorkerServiceServer).GenerateManimScript(ctx, req.(*GenerateManimScriptRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _WorkerService_GenerateManimVideo_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GenerateManimVideoRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(WorkerServiceServer).GenerateManimVideo(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: WorkerService_GenerateManimVideo_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(WorkerServiceServer).GenerateManimVideo(ctx, req.(*GenerateManimVideoRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _WorkerService_HealthCheck_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(emptypb.Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(WorkerServiceServer).HealthCheck(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: WorkerService_HealthCheck_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(WorkerServiceServer).HealthCheck(ctx, req.(*emptypb.Empty))
	}
	return interceptor(ctx, in, info, handler)
}

// WorkerService_ServiceDesc is the grpc.ServiceDesc for WorkerService service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var WorkerService_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "text2manim.v1.WorkerService",
	HandlerType: (*WorkerServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "GenerateManimScript",
			Handler:    _WorkerService_GenerateManimScript_Handler,
		},
		{
			MethodName: "GenerateManimVideo",
			Handler:    _WorkerService_GenerateManimVideo_Handler,
		},
		{
			MethodName: "HealthCheck",
			Handler:    _WorkerService_HealthCheck_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "text2manim/v1/worker.proto",
}
