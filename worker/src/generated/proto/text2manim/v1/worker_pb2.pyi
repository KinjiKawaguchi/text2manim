from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GenerateManimScriptRequest(_message.Message):
    __slots__ = ("task_id", "prompt")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    prompt: str
    def __init__(
        self, task_id: _Optional[str] = ..., prompt: _Optional[str] = ...
    ) -> None: ...

class GenerateManimScriptResponse(_message.Message):
    __slots__ = ("task_id", "script", "script_url")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_URL_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    script: str
    script_url: str
    def __init__(
        self,
        task_id: _Optional[str] = ...,
        script: _Optional[str] = ...,
        script_url: _Optional[str] = ...,
    ) -> None: ...

class GenerateManimVideoRequest(_message.Message):
    __slots__ = ("task_id", "script")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    script: str
    def __init__(
        self, task_id: _Optional[str] = ..., script: _Optional[str] = ...
    ) -> None: ...

class GenerateManimVideoResponse(_message.Message):
    __slots__ = ("task_id", "success", "video_url", "script_url", "error_message")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    VIDEO_URL_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_URL_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    success: bool
    video_url: str
    script_url: str
    error_message: str
    def __init__(
        self,
        task_id: _Optional[str] = ...,
        success: bool = ...,
        video_url: _Optional[str] = ...,
        script_url: _Optional[str] = ...,
        error_message: _Optional[str] = ...,
    ) -> None: ...
