"""パイプライン全体の設定型。

すべてイミュータブルなデータクラスとして定義し、実行中の状態変更を許さない。
"""

from dataclasses import dataclass
from typing import Literal

type LlmProvider = Literal["anthropic", "openai-compatible"]
type RenderQuality = Literal["low", "medium", "high"]
type SandboxKind = Literal["docker", "local"]

DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-5"


@dataclass(frozen=True, slots=True)
class LlmSettings:
    """LLMプロバイダーへの接続設定。

    `openai-compatible` は OpenAI 本家に加え、OpenAI 互換 API を話す
    ローカルLLMサーバー (Ollama / vLLM / LM Studio 等) を `base_url` 指定でカバーする。
    `api_key` が None の場合は各プロバイダーの標準環境変数から解決される。
    """

    provider: LlmProvider = "anthropic"
    model: str | None = None
    api_key: str | None = None
    base_url: str | None = None
    max_output_tokens: int = 8192
    temperature: float = 0.2


@dataclass(frozen=True, slots=True)
class RenderSettings:
    """Manim レンダリングの設定。

    生成コードの実行は任意コード実行に相当するため、隔離された `docker` を既定とする。
    `local` はホストの manim を直接使う開発用途向け。
    """

    quality: RenderQuality = "medium"
    timeout_seconds: float = 600.0
    sandbox: SandboxKind = "docker"
    manim_executable: str = "manim"
    docker_image: str = "manimcommunity/manim:stable"
    docker_memory_limit: str = "2g"
    docker_cpu_limit: float = 2.0


@dataclass(frozen=True, slots=True)
class PipelineSettings:
    """生成→レンダリング→修復ループの設定。

    `max_attempts` は初回生成を含む総試行回数。
    """

    max_attempts: int = 3
