"""設定からサンドボックスを構築するファクトリ。"""

from typing import TYPE_CHECKING

from text2manim.sandbox.docker import DockerSandbox
from text2manim.sandbox.local import LocalSandbox

if TYPE_CHECKING:
    from text2manim.config import RenderSettings
    from text2manim.sandbox.base import Sandbox


def create_sandbox(settings: RenderSettings) -> Sandbox:
    """サンドボックス設定に応じた実装を返す。"""
    match settings.sandbox:
        case "docker":
            return DockerSandbox(settings)
        case "local":
            return LocalSandbox(settings)
