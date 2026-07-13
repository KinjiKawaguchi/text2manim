"""生成→レンダリング→修復ループの本体。"""

from typing import TYPE_CHECKING

from text2manim.errors import RenderExhaustedError
from text2manim.events import (
    PipelineCompleted,
    PipelineEvent,
    RenderFailed,
    RenderStarted,
    ScriptGenerated,
    ScriptGenerationStarted,
    ValidationFailed,
)
from text2manim.llm.base import ChatMessage, LlmClient
from text2manim.pipeline.extract import extract_code
from text2manim.pipeline.prompts import (
    SCENE_NAME,
    SYSTEM_PROMPT,
    build_initial_message,
    build_repair_message,
)
from text2manim.pipeline.validate import validate_script
from text2manim.sandbox.base import RenderFailure, RenderSuccess, Sandbox

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from text2manim.config import PipelineSettings

# LLM へ渡すレンダリングログの上限。長大なトレースバックは末尾が本質的。
_RENDER_LOG_LIMIT = 6000


def run_pipeline(
    prompt: str,
    *,
    llm: LlmClient,
    sandbox: Sandbox,
    output_path: Path,
    settings: PipelineSettings,
) -> Iterator[PipelineEvent]:
    """プロンプトから動画を生成し、進捗イベントを順に yield する。

    成功時は最後に `PipelineCompleted` を yield して終了する。
    全試行が失敗した場合は `RenderExhaustedError` を送出する。
    """
    messages: tuple[ChatMessage, ...] = (build_initial_message(prompt),)
    last_log = ""
    for attempt in range(1, settings.max_attempts + 1):
        yield ScriptGenerationStarted(attempt=attempt, is_repair=attempt > 1)
        raw_response = llm.complete(system=SYSTEM_PROMPT, messages=messages)
        script = extract_code(raw_response)
        yield ScriptGenerated(attempt=attempt, script=script)

        validation_error = validate_script(script, scene_name=SCENE_NAME)
        if validation_error is not None:
            last_log = validation_error
            yield ValidationFailed(attempt=attempt, log=validation_error)
            messages = (
                *messages,
                ChatMessage(role="assistant", content=raw_response),
                build_repair_message(validation_error),
            )
            continue

        yield RenderStarted(attempt=attempt)
        result = sandbox.render(script, scene_name=SCENE_NAME, output_path=output_path)
        match result:
            case RenderSuccess(video_path=video_path):
                yield PipelineCompleted(video_path=video_path, script=script, attempts=attempt)
                return
            case RenderFailure(log=log):
                last_log = _tail(log, _RENDER_LOG_LIMIT)
                yield RenderFailed(attempt=attempt, log=last_log)
                messages = (
                    *messages,
                    ChatMessage(role="assistant", content=raw_response),
                    build_repair_message(last_log),
                )
    raise RenderExhaustedError(settings.max_attempts, last_log)


def _tail(text: str, limit: int) -> str:
    """テキストの末尾 `limit` 文字を返す。"""
    return text if len(text) <= limit else text[-limit:]
