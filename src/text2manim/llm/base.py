"""LLM クライアントのプロトコル定義。

パイプラインはこのプロトコルにのみ依存し、具体的なプロバイダーを知らない。
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Protocol

if TYPE_CHECKING:
    from collections.abc import Sequence

type Role = Literal["user", "assistant"]


@dataclass(frozen=True, slots=True)
class ChatMessage:
    """LLM との対話における1メッセージ。"""

    role: Role
    content: str


class LlmClient(Protocol):
    """テキスト補完を提供する LLM クライアント。"""

    def complete(self, *, system: str, messages: Sequence[ChatMessage]) -> str:
        """システムプロンプトと対話履歴から応答テキストを生成する。"""
        ...
