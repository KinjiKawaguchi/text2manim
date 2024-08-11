// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.34.2
// 	protoc        (unknown)
// source: text2manim/v1/client.proto

package text2manim_v1

import (
	_ "google.golang.org/genproto/googleapis/api/annotations"
	_ "google.golang.org/genproto/googleapis/api/httpbody"
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type GenerationStatus_Status int32

const (
	GenerationStatus_STATUS_UNSPECIFIED GenerationStatus_Status = 0
	GenerationStatus_STATUS_PENDING     GenerationStatus_Status = 1
	GenerationStatus_STATUS_PROCESSING  GenerationStatus_Status = 2
	GenerationStatus_STATUS_COMPLETED   GenerationStatus_Status = 3
	GenerationStatus_STATUS_FAILED      GenerationStatus_Status = 4
)

// Enum value maps for GenerationStatus_Status.
var (
	GenerationStatus_Status_name = map[int32]string{
		0: "STATUS_UNSPECIFIED",
		1: "STATUS_PENDING",
		2: "STATUS_PROCESSING",
		3: "STATUS_COMPLETED",
		4: "STATUS_FAILED",
	}
	GenerationStatus_Status_value = map[string]int32{
		"STATUS_UNSPECIFIED": 0,
		"STATUS_PENDING":     1,
		"STATUS_PROCESSING":  2,
		"STATUS_COMPLETED":   3,
		"STATUS_FAILED":      4,
	}
)

func (x GenerationStatus_Status) Enum() *GenerationStatus_Status {
	p := new(GenerationStatus_Status)
	*p = x
	return p
}

func (x GenerationStatus_Status) String() string {
	return protoimpl.X.EnumStringOf(x.Descriptor(), protoreflect.EnumNumber(x))
}

func (GenerationStatus_Status) Descriptor() protoreflect.EnumDescriptor {
	return file_text2manim_v1_client_proto_enumTypes[0].Descriptor()
}

func (GenerationStatus_Status) Type() protoreflect.EnumType {
	return &file_text2manim_v1_client_proto_enumTypes[0]
}

func (x GenerationStatus_Status) Number() protoreflect.EnumNumber {
	return protoreflect.EnumNumber(x)
}

// Deprecated: Use GenerationStatus_Status.Descriptor instead.
func (GenerationStatus_Status) EnumDescriptor() ([]byte, []int) {
	return file_text2manim_v1_client_proto_rawDescGZIP(), []int{6, 0}
}

type CreateGenerationRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Prompt string `protobuf:"bytes,1,opt,name=prompt,proto3" json:"prompt,omitempty"`
}

func (x *CreateGenerationRequest) Reset() {
	*x = CreateGenerationRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_text2manim_v1_client_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *CreateGenerationRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*CreateGenerationRequest) ProtoMessage() {}

func (x *CreateGenerationRequest) ProtoReflect() protoreflect.Message {
	mi := &file_text2manim_v1_client_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use CreateGenerationRequest.ProtoReflect.Descriptor instead.
func (*CreateGenerationRequest) Descriptor() ([]byte, []int) {
	return file_text2manim_v1_client_proto_rawDescGZIP(), []int{0}
}

func (x *CreateGenerationRequest) GetPrompt() string {
	if x != nil {
		return x.Prompt
	}
	return ""
}

type CreateGenerationResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	RequestId string `protobuf:"bytes,1,opt,name=request_id,json=requestId,proto3" json:"request_id,omitempty"`
}

func (x *CreateGenerationResponse) Reset() {
	*x = CreateGenerationResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_text2manim_v1_client_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *CreateGenerationResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*CreateGenerationResponse) ProtoMessage() {}

func (x *CreateGenerationResponse) ProtoReflect() protoreflect.Message {
	mi := &file_text2manim_v1_client_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use CreateGenerationResponse.ProtoReflect.Descriptor instead.
func (*CreateGenerationResponse) Descriptor() ([]byte, []int) {
	return file_text2manim_v1_client_proto_rawDescGZIP(), []int{1}
}

func (x *CreateGenerationResponse) GetRequestId() string {
	if x != nil {
		return x.RequestId
	}
	return ""
}

type GetGenerationStatusRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	RequestId string `protobuf:"bytes,1,opt,name=request_id,json=requestId,proto3" json:"request_id,omitempty"`
}

func (x *GetGenerationStatusRequest) Reset() {
	*x = GetGenerationStatusRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_text2manim_v1_client_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *GetGenerationStatusRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*GetGenerationStatusRequest) ProtoMessage() {}

func (x *GetGenerationStatusRequest) ProtoReflect() protoreflect.Message {
	mi := &file_text2manim_v1_client_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use GetGenerationStatusRequest.ProtoReflect.Descriptor instead.
func (*GetGenerationStatusRequest) Descriptor() ([]byte, []int) {
	return file_text2manim_v1_client_proto_rawDescGZIP(), []int{2}
}

func (x *GetGenerationStatusRequest) GetRequestId() string {
	if x != nil {
		return x.RequestId
	}
	return ""
}

type GetGenerationStatusResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	GenerationStatus *GenerationStatus `protobuf:"bytes,1,opt,name=generation_status,json=generationStatus,proto3" json:"generation_status,omitempty"`
}

func (x *GetGenerationStatusResponse) Reset() {
	*x = GetGenerationStatusResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_text2manim_v1_client_proto_msgTypes[3]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *GetGenerationStatusResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*GetGenerationStatusResponse) ProtoMessage() {}

func (x *GetGenerationStatusResponse) ProtoReflect() protoreflect.Message {
	mi := &file_text2manim_v1_client_proto_msgTypes[3]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use GetGenerationStatusResponse.ProtoReflect.Descriptor instead.
func (*GetGenerationStatusResponse) Descriptor() ([]byte, []int) {
	return file_text2manim_v1_client_proto_rawDescGZIP(), []int{3}
}

func (x *GetGenerationStatusResponse) GetGenerationStatus() *GenerationStatus {
	if x != nil {
		return x.GenerationStatus
	}
	return nil
}

type StreamGenerationStatusRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	RequestId string `protobuf:"bytes,1,opt,name=request_id,json=requestId,proto3" json:"request_id,omitempty"`
}

func (x *StreamGenerationStatusRequest) Reset() {
	*x = StreamGenerationStatusRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_text2manim_v1_client_proto_msgTypes[4]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *StreamGenerationStatusRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*StreamGenerationStatusRequest) ProtoMessage() {}

func (x *StreamGenerationStatusRequest) ProtoReflect() protoreflect.Message {
	mi := &file_text2manim_v1_client_proto_msgTypes[4]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use StreamGenerationStatusRequest.ProtoReflect.Descriptor instead.
func (*StreamGenerationStatusRequest) Descriptor() ([]byte, []int) {
	return file_text2manim_v1_client_proto_rawDescGZIP(), []int{4}
}

func (x *StreamGenerationStatusRequest) GetRequestId() string {
	if x != nil {
		return x.RequestId
	}
	return ""
}

type StreamGenerationStatusResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	GenerationStatus *GenerationStatus `protobuf:"bytes,1,opt,name=generation_status,json=generationStatus,proto3" json:"generation_status,omitempty"`
}

func (x *StreamGenerationStatusResponse) Reset() {
	*x = StreamGenerationStatusResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_text2manim_v1_client_proto_msgTypes[5]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *StreamGenerationStatusResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*StreamGenerationStatusResponse) ProtoMessage() {}

func (x *StreamGenerationStatusResponse) ProtoReflect() protoreflect.Message {
	mi := &file_text2manim_v1_client_proto_msgTypes[5]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use StreamGenerationStatusResponse.ProtoReflect.Descriptor instead.
func (*StreamGenerationStatusResponse) Descriptor() ([]byte, []int) {
	return file_text2manim_v1_client_proto_rawDescGZIP(), []int{5}
}

func (x *StreamGenerationStatusResponse) GetGenerationStatus() *GenerationStatus {
	if x != nil {
		return x.GenerationStatus
	}
	return nil
}

type GenerationStatus struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Status    GenerationStatus_Status `protobuf:"varint,1,opt,name=status,proto3,enum=text2manim.v1.GenerationStatus_Status" json:"status,omitempty"`
	VideoUrl  string                  `protobuf:"bytes,2,opt,name=video_url,json=videoUrl,proto3" json:"video_url,omitempty"`
	Prompt    string                  `protobuf:"bytes,3,opt,name=prompt,proto3" json:"prompt,omitempty"`
	UpdatedAt int64                   `protobuf:"varint,4,opt,name=updated_at,json=updatedAt,proto3" json:"updated_at,omitempty"`
}

func (x *GenerationStatus) Reset() {
	*x = GenerationStatus{}
	if protoimpl.UnsafeEnabled {
		mi := &file_text2manim_v1_client_proto_msgTypes[6]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *GenerationStatus) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*GenerationStatus) ProtoMessage() {}

func (x *GenerationStatus) ProtoReflect() protoreflect.Message {
	mi := &file_text2manim_v1_client_proto_msgTypes[6]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use GenerationStatus.ProtoReflect.Descriptor instead.
func (*GenerationStatus) Descriptor() ([]byte, []int) {
	return file_text2manim_v1_client_proto_rawDescGZIP(), []int{6}
}

func (x *GenerationStatus) GetStatus() GenerationStatus_Status {
	if x != nil {
		return x.Status
	}
	return GenerationStatus_STATUS_UNSPECIFIED
}

func (x *GenerationStatus) GetVideoUrl() string {
	if x != nil {
		return x.VideoUrl
	}
	return ""
}

func (x *GenerationStatus) GetPrompt() string {
	if x != nil {
		return x.Prompt
	}
	return ""
}

func (x *GenerationStatus) GetUpdatedAt() int64 {
	if x != nil {
		return x.UpdatedAt
	}
	return 0
}

var File_text2manim_v1_client_proto protoreflect.FileDescriptor

var file_text2manim_v1_client_proto_rawDesc = []byte{
	0x0a, 0x1a, 0x74, 0x65, 0x78, 0x74, 0x32, 0x6d, 0x61, 0x6e, 0x69, 0x6d, 0x2f, 0x76, 0x31, 0x2f,
	0x63, 0x6c, 0x69, 0x65, 0x6e, 0x74, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x12, 0x0d, 0x74, 0x65,
	0x78, 0x74, 0x32, 0x6d, 0x61, 0x6e, 0x69, 0x6d, 0x2e, 0x76, 0x31, 0x1a, 0x1c, 0x67, 0x6f, 0x6f,
	0x67, 0x6c, 0x65, 0x2f, 0x61, 0x70, 0x69, 0x2f, 0x61, 0x6e, 0x6e, 0x6f, 0x74, 0x61, 0x74, 0x69,
	0x6f, 0x6e, 0x73, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x1a, 0x19, 0x67, 0x6f, 0x6f, 0x67, 0x6c,
	0x65, 0x2f, 0x61, 0x70, 0x69, 0x2f, 0x68, 0x74, 0x74, 0x70, 0x62, 0x6f, 0x64, 0x79, 0x2e, 0x70,
	0x72, 0x6f, 0x74, 0x6f, 0x22, 0x31, 0x0a, 0x17, 0x43, 0x72, 0x65, 0x61, 0x74, 0x65, 0x47, 0x65,
	0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12,
	0x16, 0x0a, 0x06, 0x70, 0x72, 0x6f, 0x6d, 0x70, 0x74, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52,
	0x06, 0x70, 0x72, 0x6f, 0x6d, 0x70, 0x74, 0x22, 0x39, 0x0a, 0x18, 0x43, 0x72, 0x65, 0x61, 0x74,
	0x65, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x52, 0x65, 0x73, 0x70, 0x6f,
	0x6e, 0x73, 0x65, 0x12, 0x1d, 0x0a, 0x0a, 0x72, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x5f, 0x69,
	0x64, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x09, 0x72, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74,
	0x49, 0x64, 0x22, 0x3b, 0x0a, 0x1a, 0x47, 0x65, 0x74, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74,
	0x69, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74,
	0x12, 0x1d, 0x0a, 0x0a, 0x72, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x5f, 0x69, 0x64, 0x18, 0x01,
	0x20, 0x01, 0x28, 0x09, 0x52, 0x09, 0x72, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x49, 0x64, 0x22,
	0x6b, 0x0a, 0x1b, 0x47, 0x65, 0x74, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e,
	0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x4c,
	0x0a, 0x11, 0x67, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x5f, 0x73, 0x74, 0x61,
	0x74, 0x75, 0x73, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x1f, 0x2e, 0x74, 0x65, 0x78, 0x74,
	0x32, 0x6d, 0x61, 0x6e, 0x69, 0x6d, 0x2e, 0x76, 0x31, 0x2e, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61,
	0x74, 0x69, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x10, 0x67, 0x65, 0x6e, 0x65,
	0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x22, 0x3e, 0x0a, 0x1d,
	0x53, 0x74, 0x72, 0x65, 0x61, 0x6d, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e,
	0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x1d, 0x0a,
	0x0a, 0x72, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x5f, 0x69, 0x64, 0x18, 0x01, 0x20, 0x01, 0x28,
	0x09, 0x52, 0x09, 0x72, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x49, 0x64, 0x22, 0x6e, 0x0a, 0x1e,
	0x53, 0x74, 0x72, 0x65, 0x61, 0x6d, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e,
	0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x4c,
	0x0a, 0x11, 0x67, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x5f, 0x73, 0x74, 0x61,
	0x74, 0x75, 0x73, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x1f, 0x2e, 0x74, 0x65, 0x78, 0x74,
	0x32, 0x6d, 0x61, 0x6e, 0x69, 0x6d, 0x2e, 0x76, 0x31, 0x2e, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61,
	0x74, 0x69, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x10, 0x67, 0x65, 0x6e, 0x65,
	0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x22, 0x9c, 0x02, 0x0a,
	0x10, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x75,
	0x73, 0x12, 0x3e, 0x0a, 0x06, 0x73, 0x74, 0x61, 0x74, 0x75, 0x73, 0x18, 0x01, 0x20, 0x01, 0x28,
	0x0e, 0x32, 0x26, 0x2e, 0x74, 0x65, 0x78, 0x74, 0x32, 0x6d, 0x61, 0x6e, 0x69, 0x6d, 0x2e, 0x76,
	0x31, 0x2e, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74,
	0x75, 0x73, 0x2e, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x06, 0x73, 0x74, 0x61, 0x74, 0x75,
	0x73, 0x12, 0x1b, 0x0a, 0x09, 0x76, 0x69, 0x64, 0x65, 0x6f, 0x5f, 0x75, 0x72, 0x6c, 0x18, 0x02,
	0x20, 0x01, 0x28, 0x09, 0x52, 0x08, 0x76, 0x69, 0x64, 0x65, 0x6f, 0x55, 0x72, 0x6c, 0x12, 0x16,
	0x0a, 0x06, 0x70, 0x72, 0x6f, 0x6d, 0x70, 0x74, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52, 0x06,
	0x70, 0x72, 0x6f, 0x6d, 0x70, 0x74, 0x12, 0x1d, 0x0a, 0x0a, 0x75, 0x70, 0x64, 0x61, 0x74, 0x65,
	0x64, 0x5f, 0x61, 0x74, 0x18, 0x04, 0x20, 0x01, 0x28, 0x03, 0x52, 0x09, 0x75, 0x70, 0x64, 0x61,
	0x74, 0x65, 0x64, 0x41, 0x74, 0x22, 0x74, 0x0a, 0x06, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x12,
	0x16, 0x0a, 0x12, 0x53, 0x54, 0x41, 0x54, 0x55, 0x53, 0x5f, 0x55, 0x4e, 0x53, 0x50, 0x45, 0x43,
	0x49, 0x46, 0x49, 0x45, 0x44, 0x10, 0x00, 0x12, 0x12, 0x0a, 0x0e, 0x53, 0x54, 0x41, 0x54, 0x55,
	0x53, 0x5f, 0x50, 0x45, 0x4e, 0x44, 0x49, 0x4e, 0x47, 0x10, 0x01, 0x12, 0x15, 0x0a, 0x11, 0x53,
	0x54, 0x41, 0x54, 0x55, 0x53, 0x5f, 0x50, 0x52, 0x4f, 0x43, 0x45, 0x53, 0x53, 0x49, 0x4e, 0x47,
	0x10, 0x02, 0x12, 0x14, 0x0a, 0x10, 0x53, 0x54, 0x41, 0x54, 0x55, 0x53, 0x5f, 0x43, 0x4f, 0x4d,
	0x50, 0x4c, 0x45, 0x54, 0x45, 0x44, 0x10, 0x03, 0x12, 0x11, 0x0a, 0x0d, 0x53, 0x54, 0x41, 0x54,
	0x55, 0x53, 0x5f, 0x46, 0x41, 0x49, 0x4c, 0x45, 0x44, 0x10, 0x04, 0x32, 0xd0, 0x03, 0x0a, 0x11,
	0x54, 0x65, 0x78, 0x74, 0x32, 0x4d, 0x61, 0x6e, 0x69, 0x6d, 0x53, 0x65, 0x72, 0x76, 0x69, 0x63,
	0x65, 0x12, 0x7f, 0x0a, 0x10, 0x43, 0x72, 0x65, 0x61, 0x74, 0x65, 0x47, 0x65, 0x6e, 0x65, 0x72,
	0x61, 0x74, 0x69, 0x6f, 0x6e, 0x12, 0x26, 0x2e, 0x74, 0x65, 0x78, 0x74, 0x32, 0x6d, 0x61, 0x6e,
	0x69, 0x6d, 0x2e, 0x76, 0x31, 0x2e, 0x43, 0x72, 0x65, 0x61, 0x74, 0x65, 0x47, 0x65, 0x6e, 0x65,
	0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x27, 0x2e,
	0x74, 0x65, 0x78, 0x74, 0x32, 0x6d, 0x61, 0x6e, 0x69, 0x6d, 0x2e, 0x76, 0x31, 0x2e, 0x43, 0x72,
	0x65, 0x61, 0x74, 0x65, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x52, 0x65,
	0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x22, 0x1a, 0x82, 0xd3, 0xe4, 0x93, 0x02, 0x14, 0x3a, 0x01,
	0x2a, 0x22, 0x0f, 0x2f, 0x76, 0x31, 0x2f, 0x67, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f,
	0x6e, 0x73, 0x12, 0x92, 0x01, 0x0a, 0x13, 0x47, 0x65, 0x74, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61,
	0x74, 0x69, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x12, 0x29, 0x2e, 0x74, 0x65, 0x78,
	0x74, 0x32, 0x6d, 0x61, 0x6e, 0x69, 0x6d, 0x2e, 0x76, 0x31, 0x2e, 0x47, 0x65, 0x74, 0x47, 0x65,
	0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x65,
	0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x2a, 0x2e, 0x74, 0x65, 0x78, 0x74, 0x32, 0x6d, 0x61, 0x6e,
	0x69, 0x6d, 0x2e, 0x76, 0x31, 0x2e, 0x47, 0x65, 0x74, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74,
	0x69, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73,
	0x65, 0x22, 0x24, 0x82, 0xd3, 0xe4, 0x93, 0x02, 0x1e, 0x12, 0x1c, 0x2f, 0x76, 0x31, 0x2f, 0x67,
	0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x73, 0x2f, 0x7b, 0x72, 0x65, 0x71, 0x75,
	0x65, 0x73, 0x74, 0x5f, 0x69, 0x64, 0x7d, 0x12, 0xa4, 0x01, 0x0a, 0x16, 0x53, 0x74, 0x72, 0x65,
	0x61, 0x6d, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74,
	0x75, 0x73, 0x12, 0x2c, 0x2e, 0x74, 0x65, 0x78, 0x74, 0x32, 0x6d, 0x61, 0x6e, 0x69, 0x6d, 0x2e,
	0x76, 0x31, 0x2e, 0x53, 0x74, 0x72, 0x65, 0x61, 0x6d, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74,
	0x69, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74,
	0x1a, 0x2d, 0x2e, 0x74, 0x65, 0x78, 0x74, 0x32, 0x6d, 0x61, 0x6e, 0x69, 0x6d, 0x2e, 0x76, 0x31,
	0x2e, 0x53, 0x74, 0x72, 0x65, 0x61, 0x6d, 0x47, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f,
	0x6e, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x22,
	0x2b, 0x82, 0xd3, 0xe4, 0x93, 0x02, 0x25, 0x12, 0x23, 0x2f, 0x76, 0x31, 0x2f, 0x67, 0x65, 0x6e,
	0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x73, 0x2f, 0x7b, 0x72, 0x65, 0x71, 0x75, 0x65, 0x73,
	0x74, 0x5f, 0x69, 0x64, 0x7d, 0x2f, 0x73, 0x74, 0x72, 0x65, 0x61, 0x6d, 0x30, 0x01, 0x42, 0x4d,
	0x5a, 0x4b, 0x67, 0x69, 0x74, 0x68, 0x75, 0x62, 0x2e, 0x63, 0x6f, 0x6d, 0x2f, 0x6b, 0x69, 0x6e,
	0x6a, 0x69, 0x6b, 0x61, 0x77, 0x61, 0x67, 0x75, 0x63, 0x68, 0x69, 0x2f, 0x74, 0x65, 0x78, 0x74,
	0x32, 0x6d, 0x61, 0x6e, 0x69, 0x6d, 0x2f, 0x61, 0x70, 0x69, 0x2f, 0x70, 0x6b, 0x67, 0x2f, 0x70,
	0x62, 0x2f, 0x74, 0x65, 0x78, 0x74, 0x32, 0x6d, 0x61, 0x6e, 0x69, 0x6d, 0x2f, 0x76, 0x31, 0x3b,
	0x74, 0x65, 0x78, 0x74, 0x32, 0x6d, 0x61, 0x6e, 0x69, 0x6d, 0x5f, 0x76, 0x31, 0x62, 0x06, 0x70,
	0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_text2manim_v1_client_proto_rawDescOnce sync.Once
	file_text2manim_v1_client_proto_rawDescData = file_text2manim_v1_client_proto_rawDesc
)

func file_text2manim_v1_client_proto_rawDescGZIP() []byte {
	file_text2manim_v1_client_proto_rawDescOnce.Do(func() {
		file_text2manim_v1_client_proto_rawDescData = protoimpl.X.CompressGZIP(file_text2manim_v1_client_proto_rawDescData)
	})
	return file_text2manim_v1_client_proto_rawDescData
}

var file_text2manim_v1_client_proto_enumTypes = make([]protoimpl.EnumInfo, 1)
var file_text2manim_v1_client_proto_msgTypes = make([]protoimpl.MessageInfo, 7)
var file_text2manim_v1_client_proto_goTypes = []any{
	(GenerationStatus_Status)(0),           // 0: text2manim.v1.GenerationStatus.Status
	(*CreateGenerationRequest)(nil),        // 1: text2manim.v1.CreateGenerationRequest
	(*CreateGenerationResponse)(nil),       // 2: text2manim.v1.CreateGenerationResponse
	(*GetGenerationStatusRequest)(nil),     // 3: text2manim.v1.GetGenerationStatusRequest
	(*GetGenerationStatusResponse)(nil),    // 4: text2manim.v1.GetGenerationStatusResponse
	(*StreamGenerationStatusRequest)(nil),  // 5: text2manim.v1.StreamGenerationStatusRequest
	(*StreamGenerationStatusResponse)(nil), // 6: text2manim.v1.StreamGenerationStatusResponse
	(*GenerationStatus)(nil),               // 7: text2manim.v1.GenerationStatus
}
var file_text2manim_v1_client_proto_depIdxs = []int32{
	7, // 0: text2manim.v1.GetGenerationStatusResponse.generation_status:type_name -> text2manim.v1.GenerationStatus
	7, // 1: text2manim.v1.StreamGenerationStatusResponse.generation_status:type_name -> text2manim.v1.GenerationStatus
	0, // 2: text2manim.v1.GenerationStatus.status:type_name -> text2manim.v1.GenerationStatus.Status
	1, // 3: text2manim.v1.Text2ManimService.CreateGeneration:input_type -> text2manim.v1.CreateGenerationRequest
	3, // 4: text2manim.v1.Text2ManimService.GetGenerationStatus:input_type -> text2manim.v1.GetGenerationStatusRequest
	5, // 5: text2manim.v1.Text2ManimService.StreamGenerationStatus:input_type -> text2manim.v1.StreamGenerationStatusRequest
	2, // 6: text2manim.v1.Text2ManimService.CreateGeneration:output_type -> text2manim.v1.CreateGenerationResponse
	4, // 7: text2manim.v1.Text2ManimService.GetGenerationStatus:output_type -> text2manim.v1.GetGenerationStatusResponse
	6, // 8: text2manim.v1.Text2ManimService.StreamGenerationStatus:output_type -> text2manim.v1.StreamGenerationStatusResponse
	6, // [6:9] is the sub-list for method output_type
	3, // [3:6] is the sub-list for method input_type
	3, // [3:3] is the sub-list for extension type_name
	3, // [3:3] is the sub-list for extension extendee
	0, // [0:3] is the sub-list for field type_name
}

func init() { file_text2manim_v1_client_proto_init() }
func file_text2manim_v1_client_proto_init() {
	if File_text2manim_v1_client_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_text2manim_v1_client_proto_msgTypes[0].Exporter = func(v any, i int) any {
			switch v := v.(*CreateGenerationRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_text2manim_v1_client_proto_msgTypes[1].Exporter = func(v any, i int) any {
			switch v := v.(*CreateGenerationResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_text2manim_v1_client_proto_msgTypes[2].Exporter = func(v any, i int) any {
			switch v := v.(*GetGenerationStatusRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_text2manim_v1_client_proto_msgTypes[3].Exporter = func(v any, i int) any {
			switch v := v.(*GetGenerationStatusResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_text2manim_v1_client_proto_msgTypes[4].Exporter = func(v any, i int) any {
			switch v := v.(*StreamGenerationStatusRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_text2manim_v1_client_proto_msgTypes[5].Exporter = func(v any, i int) any {
			switch v := v.(*StreamGenerationStatusResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_text2manim_v1_client_proto_msgTypes[6].Exporter = func(v any, i int) any {
			switch v := v.(*GenerationStatus); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_text2manim_v1_client_proto_rawDesc,
			NumEnums:      1,
			NumMessages:   7,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_text2manim_v1_client_proto_goTypes,
		DependencyIndexes: file_text2manim_v1_client_proto_depIdxs,
		EnumInfos:         file_text2manim_v1_client_proto_enumTypes,
		MessageInfos:      file_text2manim_v1_client_proto_msgTypes,
	}.Build()
	File_text2manim_v1_client_proto = out.File
	file_text2manim_v1_client_proto_rawDesc = nil
	file_text2manim_v1_client_proto_goTypes = nil
	file_text2manim_v1_client_proto_depIdxs = nil
}