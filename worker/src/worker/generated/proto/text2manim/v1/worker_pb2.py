# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: text2manim/v1/worker.proto
# Protobuf Python Version: 5.27.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    3,
    '',
    'text2manim/v1/worker.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1atext2manim/v1/worker.proto\x12\rtext2manim.v1\"M\n\x1aGenerateManimScriptRequest\x12\x17\n\x07task_id\x18\x01 \x01(\tR\x06taskId\x12\x16\n\x06prompt\x18\x02 \x01(\tR\x06prompt\"N\n\x1bGenerateManimScriptResponse\x12\x17\n\x07task_id\x18\x01 \x01(\tR\x06taskId\x12\x16\n\x06script\x18\x02 \x01(\tR\x06script\"L\n\x19GenerateManimVideoRequest\x12\x17\n\x07task_id\x18\x01 \x01(\tR\x06taskId\x12\x16\n\x06script\x18\x02 \x01(\tR\x06script\"\x91\x01\n\x1aGenerateManimVideoResponse\x12\x17\n\x07task_id\x18\x01 \x01(\tR\x06taskId\x12\x18\n\x07success\x18\x02 \x01(\x08R\x07success\x12\x1b\n\tvideo_url\x18\x03 \x01(\tR\x08videoUrl\x12#\n\rerror_message\x18\x04 \x01(\tR\x0c\x65rrorMessage2\xec\x01\n\rWorkerService\x12n\n\x13GenerateManimScript\x12).text2manim.v1.GenerateManimScriptRequest\x1a*.text2manim.v1.GenerateManimScriptResponse\"\x00\x12k\n\x12GenerateManimVideo\x12(.text2manim.v1.GenerateManimVideoRequest\x1a).text2manim.v1.GenerateManimVideoResponse\"\x00\x42JZHgithub.com/KinjiKawaguchi/text2manim/api/pkg/text2manim/v1;text2manim_v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'text2manim.v1.worker_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZHgithub.com/KinjiKawaguchi/text2manim/api/pkg/text2manim/v1;text2manim_v1'
  _globals['_GENERATEMANIMSCRIPTREQUEST']._serialized_start=45
  _globals['_GENERATEMANIMSCRIPTREQUEST']._serialized_end=122
  _globals['_GENERATEMANIMSCRIPTRESPONSE']._serialized_start=124
  _globals['_GENERATEMANIMSCRIPTRESPONSE']._serialized_end=202
  _globals['_GENERATEMANIMVIDEOREQUEST']._serialized_start=204
  _globals['_GENERATEMANIMVIDEOREQUEST']._serialized_end=280
  _globals['_GENERATEMANIMVIDEORESPONSE']._serialized_start=283
  _globals['_GENERATEMANIMVIDEORESPONSE']._serialized_end=428
  _globals['_WORKERSERVICE']._serialized_start=431
  _globals['_WORKERSERVICE']._serialized_end=667
# @@protoc_insertion_point(module_scope)