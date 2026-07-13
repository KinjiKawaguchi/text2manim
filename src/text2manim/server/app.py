"""FastAPI アプリケーションの構築。

エンドポイントは旧設計の語彙を継承する:
POST /v1/generations → GET /v1/generations/{id} → GET /v1/generations/{id}/stream (SSE)
"""

import asyncio
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

from text2manim.server.schemas import (
    CreateGenerationRequest,
    CreateGenerationResponse,
    GenerationStatusResponse,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from text2manim.server.store import GenerationRecord, JobStore
    from text2manim.server.worker import GenerationWorker

_STREAM_POLL_INTERVAL_SECONDS = 0.5


def create_app(
    *,
    store: JobStore,
    worker: GenerationWorker,
    api_keys: tuple[str, ...] = (),
) -> FastAPI:
    """依存を束ねて FastAPI アプリを構築する。

    `api_keys` が空の場合は認証なし (ローカル利用想定)。
    """
    app = FastAPI(title="text2manim", description="テキストから Manim 動画を生成する API")

    async def require_api_key(
        x_api_key: Annotated[str | None, Header()] = None,
    ) -> None:
        """APIキーが設定されている場合のみ認証を要求する。"""
        if api_keys and x_api_key not in api_keys:
            raise HTTPException(status_code=401, detail="無効なAPIキーです")

    auth = Depends(require_api_key)

    @app.get("/v1/health")
    async def health() -> dict[str, str]:
        """稼働確認。"""
        return {"status": "ok"}

    @app.post("/v1/generations", status_code=202, dependencies=[auth])
    async def create_generation(request: CreateGenerationRequest) -> CreateGenerationResponse:
        """動画生成ジョブを作成してキューに積む。"""
        record = store.create(request.prompt)
        worker.submit(record.id)
        return CreateGenerationResponse(request_id=record.id)

    @app.get("/v1/generations/{request_id}", dependencies=[auth])
    async def get_generation(request_id: str) -> GenerationStatusResponse:
        """ジョブの状態を返す。"""
        return GenerationStatusResponse.from_record(_get_record_or_404(store, request_id))

    @app.get("/v1/generations/{request_id}/video", dependencies=[auth])
    async def get_generation_video(request_id: str) -> FileResponse:
        """完成した動画ファイルを返す。"""
        record = _get_record_or_404(store, request_id)
        if record.status != "completed" or record.video_path is None:
            raise HTTPException(status_code=409, detail="動画はまだ完成していません")
        return FileResponse(record.video_path, media_type="video/mp4")

    @app.get("/v1/generations/{request_id}/stream", dependencies=[auth])
    async def stream_generation(request_id: str) -> StreamingResponse:
        """進捗イベントを SSE で流す。ジョブ終了後にストリームを閉じる。"""
        _get_record_or_404(store, request_id)
        return StreamingResponse(_event_stream(store, request_id), media_type="text/event-stream")

    return app


def _get_record_or_404(store: JobStore, request_id: str) -> GenerationRecord:
    """レコードを取得し、なければ 404 を返す。"""
    record = store.get(request_id)
    if record is None:
        raise HTTPException(status_code=404, detail="指定されたジョブが見つかりません")
    return record


async def _event_stream(store: JobStore, request_id: str) -> AsyncIterator[str]:
    """DB をポーリングして SSE イベントを生成する。

    ワーカーは別スレッドで DB に書き込むため、スレッド間の橋渡しを
    ポーリングで行う (単一プロセス・低頻度アクセス前提の割り切り)。
    """
    last_seq = 0
    while True:
        events = store.list_events(request_id, after_seq=last_seq)
        for event in events:
            last_seq = event.seq
            yield f"data: {event.payload}\n\n"
        record = store.get(request_id)
        is_terminal = record is None or record.status in ("completed", "failed")
        if is_terminal and not events:
            return
        await asyncio.sleep(_STREAM_POLL_INTERVAL_SECONDS)
