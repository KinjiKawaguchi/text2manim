from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class CreateGenerationRequest(_message.Message):
    __slots__ = ("prompt",)
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    def __init__(self, prompt: _Optional[str] = ...) -> None: ...

class CreateGenerationResponse(_message.Message):
    __slots__ = ("request_id",)
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    def __init__(self, request_id: _Optional[str] = ...) -> None: ...

class GetGenerationStatusRequest(_message.Message):
    __slots__ = ("request_id",)
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    def __init__(self, request_id: _Optional[str] = ...) -> None: ...

class GetGenerationStatusResponse(_message.Message):
    __slots__ = ("generation_status",)
    GENERATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    generation_status: GenerationStatus
    def __init__(
        self, generation_status: _Optional[_Union[GenerationStatus, _Mapping]] = ...
    ) -> None: ...

class StreamGenerationStatusRequest(_message.Message):
    __slots__ = ("request_id",)
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    def __init__(self, request_id: _Optional[str] = ...) -> None: ...

class StreamGenerationStatusResponse(_message.Message):
    __slots__ = ("generation_status",)
    GENERATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    generation_status: GenerationStatus
    def __init__(
        self, generation_status: _Optional[_Union[GenerationStatus, _Mapping]] = ...
    ) -> None: ...

class GenerationStatus(_message.Message):
    __slots__ = ("status", "video_url", "script_url", "prompt", "updated_at")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATUS_UNSPECIFIED: _ClassVar[GenerationStatus.Status]
        STATUS_PENDING: _ClassVar[GenerationStatus.Status]
        STATUS_PROCESSING: _ClassVar[GenerationStatus.Status]
        STATUS_COMPLETED: _ClassVar[GenerationStatus.Status]
        STATUS_FAILED: _ClassVar[GenerationStatus.Status]

    STATUS_UNSPECIFIED: GenerationStatus.Status
    STATUS_PENDING: GenerationStatus.Status
    STATUS_PROCESSING: GenerationStatus.Status
    STATUS_COMPLETED: GenerationStatus.Status
    STATUS_FAILED: GenerationStatus.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VIDEO_URL_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_URL_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    status: GenerationStatus.Status
    video_url: str
    script_url: str
    prompt: str
    updated_at: int
    def __init__(
        self,
        status: _Optional[_Union[GenerationStatus.Status, str]] = ...,
        video_url: _Optional[str] = ...,
        script_url: _Optional[str] = ...,
        prompt: _Optional[str] = ...,
        updated_at: _Optional[int] = ...,
    ) -> None: ...
