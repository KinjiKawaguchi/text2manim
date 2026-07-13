"""サーバーモードの API テスト。"""

import json
import time
from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient

from text2manim import (
    GenerationResult,
    PipelineCompleted,
    RenderExhaustedError,
    ScriptGenerationStarted,
)
from text2manim.server import GenerationWorker, JobStore, create_app

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from text2manim.events import PipelineEvent
    from text2manim.server.worker import GenerateFn

_WAIT_TIMEOUT_SECONDS = 10.0


def _fake_generate(
    prompt: str,
    output_path: Path,
    on_event: Callable[[PipelineEvent], None],
) -> GenerationResult:
    """即座に成功するフェイクの生成処理。"""
    del prompt
    on_event(ScriptGenerationStarted(attempt=1, is_repair=False))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(b"fake-mp4")
    on_event(PipelineCompleted(video_path=output_path, script="script", attempts=1))
    return GenerationResult(video_path=output_path, script="script", attempts=1)


def _failing_generate(
    prompt: str,
    output_path: Path,
    on_event: Callable[[PipelineEvent], None],
) -> GenerationResult:
    """必ず失敗するフェイクの生成処理。"""
    del prompt, output_path, on_event
    raise RenderExhaustedError(3, "boom")


def _make_client(
    tmp_path: Path,
    *,
    generate: GenerateFn = _fake_generate,
    api_keys: tuple[str, ...] = (),
) -> TestClient:
    """テスト用のアプリとクライアントを組み立てる。"""
    store = JobStore(tmp_path / "jobs.db")
    worker = GenerationWorker(store, generate, tmp_path / "videos")
    worker.start()
    app = create_app(store=store, worker=worker, api_keys=api_keys)
    return TestClient(app)


def _wait_terminal(client: TestClient, request_id: str) -> dict[str, object]:
    """ジョブが終端状態になるまでポーリングする。"""
    deadline = time.monotonic() + _WAIT_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        response = client.get(f"/v1/generations/{request_id}")
        body: dict[str, object] = response.json()
        if body["status"] in ("completed", "failed"):
            return body
        time.sleep(0.05)
    pytest.fail("ジョブが時間内に終端状態になりませんでした")


def test_generation_lifecycle(tmp_path: Path) -> None:
    """作成→処理→完了→動画取得の一連の流れが機能する。"""
    client = _make_client(tmp_path)

    created = client.post("/v1/generations", json={"prompt": "テスト動画"})
    assert created.status_code == 202
    request_id = created.json()["request_id"]

    body = _wait_terminal(client, request_id)
    assert body["status"] == "completed"
    assert body["video_path"] is not None

    video = client.get(f"/v1/generations/{request_id}/video")
    assert video.status_code == 200
    assert video.content == b"fake-mp4"


def test_failed_generation_reports_error(tmp_path: Path) -> None:
    """生成失敗時は failed 状態とエラーメッセージが記録される。"""
    client = _make_client(tmp_path, generate=_failing_generate)

    created = client.post("/v1/generations", json={"prompt": "テスト動画"})
    body = _wait_terminal(client, created.json()["request_id"])

    assert body["status"] == "failed"
    error = body["error"]
    assert isinstance(error, str)
    assert "3回" in error


def test_stream_returns_events_and_closes(tmp_path: Path) -> None:
    """SSE ストリームはイベントを流し、ジョブ終了後に閉じる。"""
    client = _make_client(tmp_path)
    created = client.post("/v1/generations", json={"prompt": "テスト動画"})
    request_id = created.json()["request_id"]
    _wait_terminal(client, request_id)

    with client.stream("GET", f"/v1/generations/{request_id}/stream") as response:
        assert response.status_code == 200
        payloads = [
            json.loads(line.removeprefix("data: "))
            for line in response.iter_lines()
            if line.startswith("data: ")
        ]

    types = [payload["type"] for payload in payloads]
    assert "script_generation_started" in types
    assert "completed" in types
    assert types[-1] == "status"


def test_requires_api_key_when_configured(tmp_path: Path) -> None:
    """APIキーが設定されている場合、無効なキーは 401 になる。"""
    client = _make_client(tmp_path, api_keys=("secret-key",))

    denied = client.post("/v1/generations", json={"prompt": "テスト動画"})
    assert denied.status_code == 401

    allowed = client.post(
        "/v1/generations",
        json={"prompt": "テスト動画"},
        headers={"x-api-key": "secret-key"},
    )
    assert allowed.status_code == 202


def test_unknown_generation_returns_404(tmp_path: Path) -> None:
    """存在しないジョブは 404 を返す。"""
    client = _make_client(tmp_path)
    response = client.get("/v1/generations/does-not-exist")
    assert response.status_code == 404


def test_empty_prompt_is_rejected(tmp_path: Path) -> None:
    """空のプロンプトはバリデーションで弾かれる。"""
    client = _make_client(tmp_path)
    response = client.post("/v1/generations", json={"prompt": ""})
    assert response.status_code == 422
