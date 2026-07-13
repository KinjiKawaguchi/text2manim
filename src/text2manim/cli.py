"""CLI エントリポイント。

使用例:

    text2manim "比例と反比例について説明する動画" -o out.mp4
    text2manim "..." --provider openai --base-url http://localhost:11434/v1 --model qwen3
    text2manim serve --port 8000
"""

import argparse
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import uvicorn

from text2manim import (
    GenerationOptions,
    LlmSettings,
    PipelineCompleted,
    PipelineSettings,
    RenderFailed,
    RenderSettings,
    RenderStarted,
    ScriptGenerated,
    ScriptGenerationStarted,
    Text2ManimError,
    ValidationFailed,
    generate_video,
)
from text2manim.llm import create_llm_client
from text2manim.sandbox import create_sandbox
from text2manim.server import ServerConfig, create_app

if TYPE_CHECKING:
    from collections.abc import Sequence

    from text2manim.config import LlmProvider, RenderQuality, SandboxKind
    from text2manim.events import PipelineEvent

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

_API_KEYS_ENV_VAR = "TEXT2MANIM_API_KEYS"


def main() -> None:
    """CLI のエントリポイント。第1引数 serve でサーバーモードを起動する。"""
    argv = sys.argv[1:]
    if argv and argv[0] == "serve":
        _run_serve(argv[1:])
    else:
        _run_generate(argv)


def _run_generate(argv: Sequence[str]) -> None:
    """1本の動画を生成して終了する。"""
    parser = argparse.ArgumentParser(
        prog="text2manim",
        description="テキストから Manim 動画を生成する (`text2manim serve` でサーバーモード)",
    )
    parser.add_argument("prompt", help="生成したい動画の説明")
    parser.add_argument(
        "-o", "--output", default="out.mp4", help="出力先の動画パス (既定: out.mp4)"
    )
    _add_generation_flags(parser)
    namespace = parser.parse_args(list(argv))
    options = _options_from_namespace(namespace)
    try:
        result = generate_video(
            str(namespace.prompt),
            output_path=Path(str(namespace.output)),
            options=options,
            on_event=_print_event,
        )
    except Text2ManimError as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print(f"完了: {result.video_path} (試行回数: {result.attempts})")


def _run_serve(argv: Sequence[str]) -> None:
    """サーバーモードを起動する。"""
    parser = argparse.ArgumentParser(
        prog="text2manim serve",
        description="REST API + ジョブキュー + SSE のサーバーモード",
    )
    parser.add_argument("--host", default="127.0.0.1", help="バインドするホスト (既定: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="ポート番号 (既定: 8000)")
    parser.add_argument(
        "--output-dir",
        default="videos",
        help="生成した動画の保存先ディレクトリ (既定: videos)",
    )
    parser.add_argument(
        "--max-concurrency",
        type=int,
        default=1,
        help="同時に実行するレンダリング数の上限 (既定: 1)",
    )
    _add_generation_flags(parser)
    namespace = parser.parse_args(list(argv))
    options = _options_from_namespace(namespace)

    output_dir = Path(str(namespace.output_dir))
    output_dir.mkdir(parents=True, exist_ok=True)
    api_keys = _api_keys_from_env()
    if not api_keys:
        print(f"警告: {_API_KEYS_ENV_VAR} が未設定のため認証なしで起動します", file=sys.stderr)
    app = create_app(
        ServerConfig(
            llm=create_llm_client(options.llm),
            sandbox=create_sandbox(options.render),
            output_dir=output_dir,
            pipeline=options.pipeline,
            api_keys=api_keys,
            max_concurrent_renders=int(namespace.max_concurrency),
        )
    )
    uvicorn.run(app, host=str(namespace.host), port=int(namespace.port))


def _add_generation_flags(parser: argparse.ArgumentParser) -> None:
    """生成パイプラインの共通フラグを追加する。"""
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


def _options_from_namespace(namespace: argparse.Namespace) -> GenerationOptions:
    """解析済み引数から生成オプションを組み立てる。"""
    return GenerationOptions(
        llm=LlmSettings(
            provider=_PROVIDER_CHOICES[str(namespace.provider)],
            model=None if namespace.model is None else str(namespace.model),
            base_url=None if namespace.base_url is None else str(namespace.base_url),
        ),
        render=RenderSettings(
            quality=_QUALITY_CHOICES[str(namespace.quality)],
            sandbox=_SANDBOX_CHOICES[str(namespace.sandbox)],
            timeout_seconds=float(namespace.timeout),
        ),
        pipeline=PipelineSettings(max_attempts=int(namespace.max_attempts)),
    )


def _api_keys_from_env() -> tuple[str, ...]:
    """環境変数からAPIキーの一覧を読む。"""
    raw = os.environ.get(_API_KEYS_ENV_VAR, "")
    return tuple(key.strip() for key in raw.split(",") if key.strip())


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
