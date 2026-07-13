"""REST API の入出力スキーマ。

システム境界のバリデーションは Pydantic が担う。
"""

from pydantic import BaseModel, Field


class CreateGenerationRequest(BaseModel):
    """動画生成リクエスト。"""

    prompt: str = Field(min_length=1, max_length=4000)
