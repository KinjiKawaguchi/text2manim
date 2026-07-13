"""REST API の入出力スキーマ。

システム境界のバリデーションは Pydantic が担う。
"""

from pydantic import BaseModel, Field

from text2manim.server.store import GenerationRecord, GenerationStatus


class CreateGenerationRequest(BaseModel):
    """動画生成ジョブの作成リクエスト。"""

    prompt: str = Field(min_length=1, max_length=4000)


class CreateGenerationResponse(BaseModel):
    """ジョブ作成の応答。"""

    request_id: str


class GenerationStatusResponse(BaseModel):
    """ジョブの状態の応答。"""

    request_id: str
    prompt: str
    status: GenerationStatus
    video_path: str | None
    error: str | None
    created_at: str
    updated_at: str

    @classmethod
    def from_record(cls, record: GenerationRecord) -> GenerationStatusResponse:
        """ストアのレコードから応答を組み立てる。"""
        return cls(
            request_id=record.id,
            prompt=record.prompt,
            status=record.status,
            video_path=record.video_path,
            error=record.error,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )
