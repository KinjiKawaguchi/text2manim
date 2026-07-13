"""スクリプト実行のサンドボックス抽象と各実装。"""

from text2manim.sandbox.base import RenderFailure, RenderResult, RenderSuccess, Sandbox
from text2manim.sandbox.docker import DockerSandbox
from text2manim.sandbox.factory import create_sandbox
from text2manim.sandbox.local import LocalSandbox

__all__ = [
    "DockerSandbox",
    "LocalSandbox",
    "RenderFailure",
    "RenderResult",
    "RenderSuccess",
    "Sandbox",
    "create_sandbox",
]
