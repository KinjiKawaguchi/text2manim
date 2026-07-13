"""パイプラインの進捗イベント。

パイプラインはこれらのイベントを順に yield し、CLI の進捗表示と
サーバーモードの SSE の両方が同じストリームを購読する。
`attempt` はいずれも 1 始まり。
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True, slots=True)
class ScriptGenerationStarted:
    """LLM によるスクリプト生成の開始。2回目以降の試行は修復を意味する。"""

    attempt: int
    is_repair: bool


@dataclass(frozen=True, slots=True)
class ScriptGenerated:
    """スクリプト生成の完了。"""

    attempt: int
    script: str


@dataclass(frozen=True, slots=True)
class ValidationFailed:
    """レンダリング前の静的検証の失敗。ログは修復のために LLM へ渡される。"""

    attempt: int
    log: str


@dataclass(frozen=True, slots=True)
class RenderStarted:
    """レンダリングの開始。"""

    attempt: int


@dataclass(frozen=True, slots=True)
class RenderFailed:
    """レンダリングの失敗。ログは修復のために LLM へ渡される。"""

    attempt: int
    log: str


@dataclass(frozen=True, slots=True)
class PipelineCompleted:
    """パイプライン全体の成功。"""

    video_path: Path
    script: str
    attempts: int


type PipelineEvent = (
    ScriptGenerationStarted
    | ScriptGenerated
    | ValidationFailed
    | RenderStarted
    | RenderFailed
    | PipelineCompleted
)
