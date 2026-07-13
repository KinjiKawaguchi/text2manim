"""実LLMとDockerサンドボックスを使う端到端テスト。

LLM API コストとレンダリング時間が発生するため、既定のテスト実行からは除外している:

    uv run pytest -m e2e

ANTHROPIC_API_KEY と Docker が利用できない場合は各テストがスキップされる。
"""

import os
import shutil
from typing import TYPE_CHECKING

import pytest

from text2manim import (
    GenerationOptions,
    PipelineSettings,
    RenderSettings,
    generate_video,
)
from text2manim.sandbox import DockerSandbox, RenderSuccess

if TYPE_CHECKING:
    from pathlib import Path

pytestmark = pytest.mark.e2e

_requires_docker = pytest.mark.skipif(
    shutil.which("docker") is None, reason="Docker が利用できない"
)
_requires_anthropic_key = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"), reason="ANTHROPIC_API_KEY が未設定"
)

_FIXED_SCRIPT = """
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        square = Square(color=BLUE)
        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))
"""


@_requires_docker
def test_docker_sandbox_renders_fixed_script(tmp_path: Path) -> None:
    """固定スクリプトが Docker サンドボックスでレンダリングできる (LLM 不要)。"""
    sandbox = DockerSandbox(RenderSettings(quality="low", timeout_seconds=240))
    output_path = tmp_path / "fixed.mp4"

    result = sandbox.render(_FIXED_SCRIPT, scene_name="GeneratedScene", output_path=output_path)

    assert isinstance(result, RenderSuccess)
    assert output_path.exists()
    assert output_path.stat().st_size > 1_000


@_requires_docker
@_requires_anthropic_key
def test_generates_video_from_prompt(tmp_path: Path) -> None:
    """プロンプトから動画生成までの全パイプラインが通る。"""
    output_path = tmp_path / "e2e.mp4"
    options = GenerationOptions(
        render=RenderSettings(quality="low", timeout_seconds=300),
        pipeline=PipelineSettings(max_attempts=3),
    )

    result = generate_video(
        "A square morphs into a circle. Keep it under 5 seconds.",
        output_path=output_path,
        options=options,
    )

    assert result.video_path == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 10_000
    assert 1 <= result.attempts <= 3
    assert "GeneratedScene" in result.script
