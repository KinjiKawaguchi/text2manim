"""テキストから Manim 動画を生成するエンジン。

代表的な使い方:

    from pathlib import Path
    from text2manim import generate_video

    result = generate_video(
        "比例と反比例について説明する動画",
        output_path=Path("out.mp4"),
    )
"""

from text2manim.config import (
    LlmProvider,
    LlmSettings,
    PipelineSettings,
    RenderQuality,
    RenderSettings,
)
from text2manim.errors import (
    EmptyLlmResponseError,
    MissingModelError,
    RenderExhaustedError,
    SandboxUnavailableError,
    Text2ManimError,
)
from text2manim.events import (
    PipelineCompleted,
    PipelineEvent,
    RenderFailed,
    RenderStarted,
    ScriptGenerated,
    ScriptGenerationStarted,
    ValidationFailed,
)
from text2manim.generate import GenerationOptions, GenerationResult, generate_video

__version__ = "0.1.0"  # x-release-please-version

__all__ = [
    "EmptyLlmResponseError",
    "GenerationOptions",
    "GenerationResult",
    "LlmProvider",
    "LlmSettings",
    "MissingModelError",
    "PipelineCompleted",
    "PipelineEvent",
    "PipelineSettings",
    "RenderExhaustedError",
    "RenderFailed",
    "RenderQuality",
    "RenderSettings",
    "RenderStarted",
    "SandboxUnavailableError",
    "ScriptGenerated",
    "ScriptGenerationStarted",
    "Text2ManimError",
    "ValidationFailed",
    "generate_video",
]
