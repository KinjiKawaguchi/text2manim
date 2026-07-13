"""サンドボックスのプロトコル定義とレンダリング結果型。"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True, slots=True)
class RenderSuccess:
    """レンダリング成功。動画は `video_path` に配置済み。"""

    video_path: Path


@dataclass(frozen=True, slots=True)
class RenderFailure:
    """レンダリング失敗。`log` は修復のために LLM へ渡される。"""

    log: str


type RenderResult = RenderSuccess | RenderFailure


class Sandbox(Protocol):
    """Manim スクリプトをレンダリングする実行環境。

    LLM が生成したコードは任意コード実行に相当するため、
    実装は可能な限り隔離された環境で実行することが期待される。
    """

    def render(self, script: str, *, scene_name: str, output_path: Path) -> RenderResult:
        """スクリプトをレンダリングし、成功時は `output_path` に動画を配置する。"""
        ...
