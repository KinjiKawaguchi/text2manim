"""設定から LLM クライアントを構築するファクトリ。"""

from typing import TYPE_CHECKING

from text2manim.llm.anthropic_client import AnthropicClient
from text2manim.llm.openai_compat import OpenAiCompatibleClient

if TYPE_CHECKING:
    from text2manim.config import LlmSettings
    from text2manim.llm.base import LlmClient


def create_llm_client(settings: LlmSettings) -> LlmClient:
    """プロバイダー設定に応じたクライアントを返す。"""
    match settings.provider:
        case "anthropic":
            return AnthropicClient(settings)
        case "openai-compatible":
            return OpenAiCompatibleClient(settings)
