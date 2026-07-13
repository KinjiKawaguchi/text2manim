"""CLI エントリポイント。

使用例:

    text2manim "比例と反比例について説明する動画" -o out.mp4
    text2manim "..." --provider openai --model gpt-5.2
    text2manim "..." --provider openai --base-url http://localhost:11434/v1 --model qwen3
"""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from text2manim.config import (
    LlmProvider,
    LlmSettings,
    PipelineSettings,
    RenderQuality,
    RenderSettings,
    SandboxKind,
)
from text2manim.errors import Text2ManimError
from text2manim.events import (
    PipelineCompleted,
    PipelineEvent,
    RenderFailed,
    RenderStarted,
    ScriptGenerated,
    ScriptGenerationStarted,
    ValidationFailed,
)
from text2manim.generate import GenerationOptions, generate_video

_PROVIDER_CHOICES: dict[str, LlmProvider] = {
    "anthropic": "anthropic",
    "openai": "openai-compatible",
}

_QUALITY_CHOICES: dict[str, RenderQuality] = {
    "low": "low",
    "medium": "medium",
    "high": "high",
}

_SANDBOX_CHOICES: dict[str, SandboxKind] = {
    "docker": "docker",
    "local": "local",
}


@dataclass(frozen=True, slots=True)
class CliArgs:
    """検証済みのコマンドライン引数。"""

    prompt: str
    output_path: Path
    provider: LlmProvider
    model: str | None
    base_url: str | None
    quality: RenderQuality
    sandbox: SandboxKind
    max_attempts: int
    timeout_seconds: float


def main() -> None:
    """CLI のエントリポイント。"""
    args = _parse_args(sys.argv[1:])
    options = GenerationOptions(
        llm=LlmSettings(provider=args.provider, model=args.model, base_url=args.base_url),
        render=RenderSettings(
            quality=args.quality,
            sandbox=args.sandbox,
            timeout_seconds=args.timeout_seconds,
        ),
        pipeline=PipelineSettings(max_attempts=args.max_attempts),
    )
    try:
        result = generate_video(
            args.prompt,
            output_path=args.output_path,
            options=options,
            on_event=_print_event,
        )
    except Text2ManimError as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print(f"完了: {result.video_path} (試行回数: {result.attempts})")


def _parse_args(argv: list[str]) -> CliArgs:
    """引数を解析し、検証済みの型付き引数に変換する。"""
    parser = argparse.ArgumentParser(
        prog="text2manim",
        description="テキストから Manim 動画を生成する",
    )
    parser.add_argument("prompt", help="生成したい動画の説明")
    parser.add_argument(
        "-o", "--output", default="out.mp4", help="出力先の動画パス (既定: out.mp4)"
    )
    parser.add_argument(
        "--provider",
        choices=sorted(_PROVIDER_CHOICES),
        default="anthropic",
        help="LLM プロバイダー。openai は OpenAI 互換 API 全般 (ローカルLLM含む)",
    )
    parser.add_argument("--model", default=None, help="モデル名 (openai では必須)")
    parser.add_argument(
        "--base-url",
        default=None,
        help="OpenAI 互換サーバーの URL (例: http://localhost:11434/v1)",
    )
    parser.add_argument(
        "--quality",
        choices=sorted(_QUALITY_CHOICES),
        default="medium",
        help="レンダリング品質 (既定: medium)",
    )
    parser.add_argument(
        "--sandbox",
        choices=sorted(_SANDBOX_CHOICES),
        default="docker",
        help="レンダリング実行環境。local はホストの manim を直接使う (既定: docker)",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=3,
        help="修復を含む最大試行回数 (既定: 3)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=600.0,
        help="レンダリングのタイムアウト秒数 (既定: 600)",
    )
    namespace = parser.parse_args(argv)
    return CliArgs(
        prompt=str(namespace.prompt),
        output_path=Path(str(namespace.output)),
        provider=_PROVIDER_CHOICES[str(namespace.provider)],
        model=None if namespace.model is None else str(namespace.model),
        base_url=None if namespace.base_url is None else str(namespace.base_url),
        quality=_QUALITY_CHOICES[str(namespace.quality)],
        sandbox=_SANDBOX_CHOICES[str(namespace.sandbox)],
        max_attempts=int(namespace.max_attempts),
        timeout_seconds=float(namespace.timeout),
    )


def _print_event(event: PipelineEvent) -> None:
    """進捗イベントを1行ずつ表示する。"""
    match event:
        case ScriptGenerationStarted(attempt=attempt, is_repair=True):
            print(f"[{attempt}] エラーを基にスクリプトを修正中...")
        case ScriptGenerationStarted(attempt=attempt):
            print(f"[{attempt}] スクリプトを生成中...")
        case ScriptGenerated(attempt=attempt, script=script):
            print(f"[{attempt}] スクリプト生成完了 ({len(script.splitlines())} 行)")
        case ValidationFailed(attempt=attempt):
            print(f"[{attempt}] スクリプト検証失敗")
        case RenderStarted(attempt=attempt):
            print(f"[{attempt}] レンダリング中...")
        case RenderFailed(attempt=attempt):
            print(f"[{attempt}] レンダリング失敗")
        case PipelineCompleted():
            pass
