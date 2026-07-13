"""OpenAI 互換 API クライアント実装。

OpenAI 本家に加え、`base_url` を指定することで OpenAI 互換 API を話す
ローカルLLMサーバー (Ollama / vLLM / LM Studio 等) に接続できる。
"""

from typing import TYPE_CHECKING

from openai import OpenAI, omit

from text2manim.errors import EmptyLlmResponseError, MissingModelError

if TYPE_CHECKING:
    from collections.abc import Sequence

    from openai.types.chat import ChatCompletionMessageParam

    from text2manim.config import LlmSettings
    from text2manim.llm.base import ChatMessage

# ローカルサーバーは認証キーを要求しないことが多いが、SDK はキーを必須とするため
# base_url 指定時のみプレースホルダーで埋める。
_LOCAL_PLACEHOLDER_API_KEY = "no-key-required"


class OpenAiCompatibleClient:
    """Chat Completions API を使う LlmClient 実装。

    `api_key` が未指定の場合、`base_url` があればプレースホルダーを使い、
    なければ SDK が環境変数 `OPENAI_API_KEY` から解決する。
    """

    def __init__(self, settings: LlmSettings) -> None:
        """接続設定からクライアントを構築する。"""
        if settings.model is None:
            raise MissingModelError
        self._settings = settings
        self._model = settings.model
        api_key = settings.api_key
        if api_key is None and settings.base_url is not None:
            api_key = _LOCAL_PLACEHOLDER_API_KEY
        self._client = OpenAI(api_key=api_key, base_url=settings.base_url)

    def complete(self, *, system: str, messages: Sequence[ChatMessage]) -> str:
        """システムプロンプトと対話履歴から応答テキストを生成する。"""
        params: list[ChatCompletionMessageParam] = [{"role": "system", "content": system}]
        params.extend(_to_openai_message(message) for message in messages)
        temperature = self._settings.temperature
        response = self._client.chat.completions.create(
            model=self._model,
            messages=params,
            max_completion_tokens=self._settings.max_output_tokens,
            temperature=omit if temperature is None else temperature,
        )
        content = response.choices[0].message.content if response.choices else None
        if content is None or not content.strip():
            raise EmptyLlmResponseError
        return content


def _to_openai_message(message: ChatMessage) -> ChatCompletionMessageParam:
    """ChatMessage を role ごとに対応する型付きメッセージへ変換する。"""
    match message.role:
        case "user":
            return {"role": "user", "content": message.content}
        case "assistant":
            return {"role": "assistant", "content": message.content}
