"""サーバーモード (ステートレスworker) の API テスト。"""

import json
from typing import TYPE_CHECKING

from fastapi.testclient import TestClient

from text2manim import PipelineSettings
from text2manim.sandbox import RenderFailure, RenderSuccess, Sandbox
from text2manim.server import ServerConfig, create_app

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

    from text2manim.llm import ChatMessage
    from text2manim.sandbox import RenderResult

_VALID_RESPONSE = '```python\nclass GeneratedScene:\n    marker = "v1"\n```'


class FakeLlm:
    """常に同じ応答を返す LlmClient 実装。"""

    def __init__(self, response: str = _VALID_RESPONSE) -> None:
        """応答を保持する。"""
        self._response = response

    def complete(self, *, system: str, messages: Sequence[ChatMessage]) -> str:
        """固定の応答を返す。"""
        del system, messages
        return self._response


class FakeSandbox:
    """出力先に固定バイト列を書き込む Sandbox 実装。"""

    def __init__(self, *, fail: bool = False) -> None:
        """成否を設定する。"""
        self._fail = fail

    def render(self, script: str, *, scene_name: str, output_path: Path) -> RenderResult:
        """成功時はダミー動画を書き込む。"""
        del script, scene_name
        if self._fail:
            return RenderFailure(log="render boom")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"fake-mp4")
        return RenderSuccess(video_path=output_path)


def _make_client(
    tmp_path: Path,
    *,
    sandbox: Sandbox | None = None,
    api_keys: tuple[str, ...] = (),
) -> TestClient:
    """テスト用のアプリとクライアントを組み立てる。"""
    app = create_app(
        ServerConfig(
            llm=FakeLlm(),
            sandbox=sandbox if sandbox is not None else FakeSandbox(),
            output_dir=tmp_path / "videos",
            pipeline=PipelineSettings(max_attempts=2),
            api_keys=api_keys,
        )
    )
    return TestClient(app)


def _collect_events(client: TestClient, prompt: str) -> list[dict[str, object]]:
    """生成リクエストを送り、SSE イベントをすべて集める。"""
    with client.stream("POST", "/v1/generations", json={"prompt": prompt}) as response:
        assert response.status_code == 200
        return [
            json.loads(line.removeprefix("data: "))
            for line in response.iter_lines()
            if line.startswith("data: ")
        ]


def test_generation_streams_events_and_serves_video(tmp_path: Path) -> None:
    """生成の進捗がSSEで流れ、終端イベントのURLから動画を取得できる。"""
    client = _make_client(tmp_path)

    events = _collect_events(client, "テスト動画")

    types = [event["type"] for event in events]
    assert "script_generation_started" in types
    assert types[-1] == "completed"

    completed = events[-1]
    video_url = completed["video_url"]
    assert isinstance(video_url, str)

    video = client.get(video_url)
    assert video.status_code == 200
    assert video.content == b"fake-mp4"


def test_failed_generation_ends_with_failed_event(tmp_path: Path) -> None:
    """全試行が失敗した場合は failed イベントで終わる。"""
    client = _make_client(tmp_path, sandbox=FakeSandbox(fail=True))

    events = _collect_events(client, "テスト動画")

    assert events[-1]["type"] == "failed"
    error = events[-1]["error"]
    assert isinstance(error, str)
    assert "2回" in error


def test_requires_api_key_when_configured(tmp_path: Path) -> None:
    """APIキーが設定されている場合、無効なキーは 401 になる。"""
    client = _make_client(tmp_path, api_keys=("secret-key",))

    denied = client.post("/v1/generations", json={"prompt": "テスト動画"})
    assert denied.status_code == 401

    with client.stream(
        "POST",
        "/v1/generations",
        json={"prompt": "テスト動画"},
        headers={"x-api-key": "secret-key"},
    ) as allowed:
        assert allowed.status_code == 200


def test_video_endpoint_rejects_invalid_filenames(tmp_path: Path) -> None:
    """UUID形式以外のファイル名 (パストラバーサル等) は 404 になる。"""
    client = _make_client(tmp_path)

    for filename in ("../../etc/passwd", "a.mp4", "0" * 32 + ".txt"):
        response = client.get(f"/v1/videos/{filename}")
        assert response.status_code == 404


def test_empty_prompt_is_rejected(tmp_path: Path) -> None:
    """空のプロンプトはバリデーションで弾かれる。"""
    client = _make_client(tmp_path)
    response = client.post("/v1/generations", json={"prompt": ""})
    assert response.status_code == 422


def test_health(tmp_path: Path) -> None:
    """ヘルスチェックは認証なしで応答する。"""
    client = _make_client(tmp_path, api_keys=("secret-key",))
    response = client.get("/v1/health")
    assert response.status_code == 200
