"""ライブラリ利用者向けの高水準 API。"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from text2manim.config import LlmSettings, PipelineSettings, RenderSettings
from text2manim.events import PipelineCompleted, PipelineEvent
from text2manim.llm import create_llm_client
from text2manim.pipeline import run_pipeline
from text2manim.sandbox import create_sandbox

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


@dataclass(frozen=True, slots=True)
class GenerationResult:
    """動画生成の最終結果。"""

    video_path: Path
    script: str
    attempts: int


@dataclass(frozen=True, slots=True)
class GenerationOptions:
    """`generate_video` の設定一式。すべて既定値を持つ。"""

    llm: LlmSettings = field(default_factory=LlmSettings)
    render: RenderSettings = field(default_factory=RenderSettings)
    pipeline: PipelineSettings = field(default_factory=PipelineSettings)


def generate_video(
    prompt: str,
    *,
    output_path: Path,
    options: GenerationOptions | None = None,
    on_event: Callable[[PipelineEvent], None] | None = None,
) -> GenerationResult:
    """プロンプトから動画を生成する。

    進捗を購読したい場合は `on_event` にコールバックを渡す。
    より細かい制御が必要な場合は `text2manim.pipeline.run_pipeline` を直接使う。
    """
    resolved = options if options is not None else GenerationOptions()
    llm = create_llm_client(resolved.llm)
    sandbox = create_sandbox(resolved.render)
    completed: PipelineCompleted | None = None
    for event in run_pipeline(
        prompt,
        llm=llm,
        sandbox=sandbox,
        output_path=output_path,
        settings=resolved.pipeline,
    ):
        if on_event is not None:
            on_event(event)
        if isinstance(event, PipelineCompleted):
            completed = event
    if completed is None:
        # run_pipeline は成功時に必ず PipelineCompleted を yield するため、ここには
        # 実装欠陥がない限り到達しない。
        message = "パイプラインが完了イベントを返しませんでした"
        raise RuntimeError(message)
    return GenerationResult(
        video_path=completed.video_path,
        script=completed.script,
        attempts=completed.attempts,
    )
