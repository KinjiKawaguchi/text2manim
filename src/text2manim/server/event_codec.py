"""パイプラインイベントの SSE 向けシリアライズ。"""

from typing import TYPE_CHECKING

from text2manim.events import (
    PipelineCompleted,
    RenderFailed,
    RenderStarted,
    ScriptGenerated,
    ScriptGenerationStarted,
    ValidationFailed,
)

if TYPE_CHECKING:
    from text2manim.events import PipelineEvent


def serialize_event(event: PipelineEvent) -> dict[str, object]:
    """イベントを JSON 化可能な辞書に変換する。

    スクリプト全文は完了イベントにのみ含め、途中経過は行数だけを流す
    (SSE のペイロードを小さく保つため)。
    """
    match event:
        case ScriptGenerationStarted(attempt=attempt, is_repair=is_repair):
            return {"type": "script_generation_started", "attempt": attempt, "is_repair": is_repair}
        case ScriptGenerated(attempt=attempt, script=script):
            return {
                "type": "script_generated",
                "attempt": attempt,
                "script_lines": len(script.splitlines()),
            }
        case ValidationFailed(attempt=attempt, log=log):
            return {"type": "validation_failed", "attempt": attempt, "log": log}
        case RenderStarted(attempt=attempt):
            return {"type": "render_started", "attempt": attempt}
        case RenderFailed(attempt=attempt, log=log):
            return {"type": "render_failed", "attempt": attempt, "log": log}
        case PipelineCompleted(video_path=video_path, script=script, attempts=attempts):
            return {
                "type": "completed",
                "video_path": str(video_path),
                "script": script,
                "attempts": attempts,
            }
