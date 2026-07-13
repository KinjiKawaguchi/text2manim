"""run_pipeline の修復ループのテスト。"""

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from text2manim.config import PipelineSettings
from text2manim.errors import RenderExhaustedError
from text2manim.events import (
    PipelineCompleted,
    RenderFailed,
    ScriptGenerationStarted,
    ValidationFailed,
)
from text2manim.pipeline.runner import run_pipeline
from text2manim.sandbox.base import RenderFailure, RenderResult, RenderSuccess

if TYPE_CHECKING:
    from collections.abc import Sequence

    from text2manim.llm.base import ChatMessage


def scene_script(marker: str) -> str:
    """検証を通過する最小のシーンスクリプトを作る。"""
    return f'class GeneratedScene:\n    marker = "{marker}"'


def llm_response(marker: str) -> str:
    """コードブロックに包まれた LLM 応答を作る。"""
    return f"```python\n{scene_script(marker)}\n```"


class FakeLlm:
    """呼び出しごとに用意した応答を順に返す LlmClient 実装。"""

    def __init__(self, responses: Sequence[str]) -> None:
        """応答のシーケンスを保持する。"""
        self._responses = responses
        self.calls: list[tuple[ChatMessage, ...]] = []

    def complete(self, *, system: str, messages: Sequence[ChatMessage]) -> str:
        """記録を残しつつ次の応答を返す。"""
        del system
        self.calls.append(tuple(messages))
        return self._responses[len(self.calls) - 1]


class FakeSandbox:
    """呼び出しごとに用意した結果を順に返す Sandbox 実装。"""

    def __init__(self, results: Sequence[RenderResult]) -> None:
        """結果のシーケンスを保持する。"""
        self._results = results
        self.rendered_scripts: list[str] = []

    def render(self, script: str, *, scene_name: str, output_path: Path) -> RenderResult:
        """記録を残しつつ次の結果を返す。"""
        del scene_name, output_path
        self.rendered_scripts.append(script)
        return self._results[len(self.rendered_scripts) - 1]


def test_completes_without_repair_on_first_success() -> None:
    """1回目のレンダリングが成功したらイベント列が完了で終わる。"""
    llm = FakeLlm([llm_response("v1")])
    sandbox = FakeSandbox([RenderSuccess(video_path=Path("out.mp4"))])

    events = list(
        run_pipeline(
            "テスト動画",
            llm=llm,
            sandbox=sandbox,
            output_path=Path("out.mp4"),
            settings=PipelineSettings(max_attempts=3),
        )
    )

    completed = events[-1]
    assert isinstance(completed, PipelineCompleted)
    assert completed.attempts == 1
    assert completed.script == scene_script("v1")
    assert len(llm.calls) == 1


def test_repairs_with_error_log_on_failure() -> None:
    """失敗ログが assistant 応答とともに次の LLM 呼び出しへ渡る。"""
    llm = FakeLlm([llm_response("v1"), llm_response("v2")])
    sandbox = FakeSandbox(
        [RenderFailure(log="NameError: undefined"), RenderSuccess(video_path=Path("out.mp4"))]
    )

    events = list(
        run_pipeline(
            "テスト動画",
            llm=llm,
            sandbox=sandbox,
            output_path=Path("out.mp4"),
            settings=PipelineSettings(max_attempts=3),
        )
    )

    repair_starts = [
        event for event in events if isinstance(event, ScriptGenerationStarted) and event.is_repair
    ]
    assert len(repair_starts) == 1
    failed = [event for event in events if isinstance(event, RenderFailed)]
    assert len(failed) == 1
    assert "NameError" in failed[0].log

    second_call = llm.calls[1]
    assert second_call[1].role == "assistant"
    assert "NameError" in second_call[2].content
    assert sandbox.rendered_scripts == [scene_script("v1"), scene_script("v2")]


def test_validation_failure_skips_render_and_repairs() -> None:
    """静的検証で弾かれたらレンダリングせずに修復へ回す。"""
    llm = FakeLlm(["```python\nx = 1\n```", llm_response("v2")])
    sandbox = FakeSandbox([RenderSuccess(video_path=Path("out.mp4"))])

    events = list(
        run_pipeline(
            "テスト動画",
            llm=llm,
            sandbox=sandbox,
            output_path=Path("out.mp4"),
            settings=PipelineSettings(max_attempts=3),
        )
    )

    validation_failures = [event for event in events if isinstance(event, ValidationFailed)]
    assert len(validation_failures) == 1
    assert "GeneratedScene" in validation_failures[0].log

    # 検証で弾かれた1回目はサンドボックスに到達しない
    assert sandbox.rendered_scripts == [scene_script("v2")]
    assert "GeneratedScene" in llm.calls[1][2].content

    completed = events[-1]
    assert isinstance(completed, PipelineCompleted)
    assert completed.attempts == 2


def test_raises_after_all_attempts_fail() -> None:
    """max_attempts 回すべて失敗したら RenderExhaustedError になる。"""
    llm = FakeLlm([llm_response("v1"), llm_response("v2")])
    sandbox = FakeSandbox([RenderFailure(log="error 1"), RenderFailure(log="error 2")])

    with pytest.raises(RenderExhaustedError) as exc_info:
        list(
            run_pipeline(
                "テスト動画",
                llm=llm,
                sandbox=sandbox,
                output_path=Path("out.mp4"),
                settings=PipelineSettings(max_attempts=2),
            )
        )

    assert exc_info.value.attempts == 2
    assert exc_info.value.last_log == "error 2"
