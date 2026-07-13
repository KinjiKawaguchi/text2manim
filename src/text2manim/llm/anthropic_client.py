"""Anthropic API クライアント実装。"""

from typing import TYPE_CHECKING

from anthropic import Anthropic, omit
from anthropic.types import MessageParam, TextBlock

from text2manim.config import DEFAULT_ANTHROPIC_MODEL, LlmSettings
from text2manim.errors import EmptyLlmResponseError

if TYPE_CHECKING:
    from collections.abc import Sequence

    from text2manim.llm.base import ChatMessage


class AnthropicClient:
    """Anthropic Messages API を使う LlmClient 実装。

    `api_key` が未指定の場合は SDK が環境変数 `ANTHROPIC_API_KEY` から解決する。
    """

    def __init__(self, settings: LlmSettings) -> None:
        """接続設定からクライアントを構築する。"""
        self._settings = settings
        self._model = settings.model or DEFAULT_ANTHROPIC_MODEL
        self._client = (
            Anthropic(api_key=settings.api_key) if settings.api_key is not None else Anthropic()
        )

    def complete(self, *, system: str, messages: Sequence[ChatMessage]) -> str:
        """システムプロンプトと対話履歴から応答テキストを生成する。"""
        params: list[MessageParam] = [
            {"role": message.role, "content": message.content} for message in messages
        ]
        temperature = self._settings.temperature
        response = self._client.messages.create(
            model=self._model,
            system=system,
            messages=params,
            max_tokens=self._settings.max_output_tokens,
            temperature=omit if temperature is None else temperature,
        )
        texts = [block.text for block in response.content if isinstance(block, TextBlock)]
        if not texts:
            raise EmptyLlmResponseError
        return "\n".join(texts)
