"""FastAPI アプリケーションの構築。

サーバーモードはステートレスなワーカーとして振る舞う。
1リクエスト = 1生成で、進捗はそのまま SSE で流し、ジョブの永続化やキューは持たない。
ジョブ管理 (履歴・リトライ・スケジューリング) が必要な場合はアプリケーション側が担う。
"""

import json
import re
import threading
import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

from text2manim import PipelineCompleted, PipelineSettings, Text2ManimError
from text2manim.pipeline import run_pipeline
from text2manim.server.event_codec import serialize_event

# FastAPI はルート引数の型を実行時に解決するため TYPE_CHECKING へ移動できない
from text2manim.server.schemas import CreateGenerationRequest  # noqa: TC001

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from text2manim.llm import LlmClient
    from text2manim.sandbox import Sandbox

_VIDEO_FILENAME_PATTERN = re.compile(r"^[0-9a-f]{32}\.mp4$")


@dataclass(frozen=True, slots=True)
class ServerConfig:
    """serve モードの構成。

    `api_keys` が空の場合は認証なし (ローカル利用想定)。
    `max_concurrent_renders` を超えるリクエストはスロットが空くまで待機する。
    """

    llm: LlmClient
    sandbox: Sandbox
    output_dir: Path
    pipeline: PipelineSettings = field(default_factory=PipelineSettings)
    api_keys: tuple[str, ...] = ()
    max_concurrent_renders: int = 1


def create_app(config: ServerConfig) -> FastAPI:
    """構成からステートレスworkerの FastAPI アプリを構築する。"""
    app = FastAPI(title="text2manim", description="テキストから Manim 動画を生成する API")
    render_slots = threading.Semaphore(config.max_concurrent_renders)

    async def require_api_key(
        x_api_key: Annotated[str | None, Header()] = None,
    ) -> None:
        """APIキーが設定されている場合のみ認証を要求する。"""
        if config.api_keys and x_api_key not in config.api_keys:
            raise HTTPException(status_code=401, detail="無効なAPIキーです")

    auth = Depends(require_api_key)

    @app.get("/v1/health")
    async def health() -> dict[str, str]:
        """稼働確認。"""
        return {"status": "ok"}

    @app.post("/v1/generations", dependencies=[auth])
    async def create_generation(request: CreateGenerationRequest) -> StreamingResponse:
        """動画を生成し、進捗を SSE でストリームする。

        終端イベントは `completed` (video_url 付き) または `failed`。
        """
        return StreamingResponse(
            _generation_stream(config, render_slots, request.prompt),
            media_type="text/event-stream",
        )

    @app.get("/v1/videos/{filename}", dependencies=[auth])
    async def get_video(filename: str) -> FileResponse:
        """生成済みの動画ファイルを返す。"""
        if _VIDEO_FILENAME_PATTERN.fullmatch(filename) is None:
            raise HTTPException(status_code=404, detail="指定された動画が見つかりません")
        video_path = config.output_dir / filename
        if not video_path.is_file():
            raise HTTPException(status_code=404, detail="指定された動画が見つかりません")
        return FileResponse(video_path, media_type="video/mp4")

    return app


def _generation_stream(
    config: ServerConfig, render_slots: threading.Semaphore, prompt: str
) -> Iterator[str]:
    """1件の生成を実行し、進捗イベントを SSE 形式で yield する。"""
    video_id = uuid.uuid4().hex
    output_path = config.output_dir / f"{video_id}.mp4"
    with render_slots:
        try:
            for event in run_pipeline(
                prompt,
                llm=config.llm,
                sandbox=config.sandbox,
                output_path=output_path,
                settings=config.pipeline,
            ):
                payload = serialize_event(event)
                if isinstance(event, PipelineCompleted):
                    payload["video_url"] = f"/v1/videos/{video_id}.mp4"
                yield _sse(payload)
        except Text2ManimError as exc:
            yield _sse({"type": "failed", "error": str(exc)})


def _sse(payload: dict[str, object]) -> str:
    """辞書を SSE の data 行に変換する。"""
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
