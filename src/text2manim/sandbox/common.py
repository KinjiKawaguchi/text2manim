"""サンドボックス実装間で共有する manim 実行まわりのヘルパー。"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import subprocess
    from pathlib import Path

    from text2manim.config import RenderQuality

SCRIPT_FILENAME = "scene.py"

QUALITY_FLAGS: dict[RenderQuality, str] = {
    "low": "-ql",
    "medium": "-qm",
    "high": "-qh",
}


def combine_output(process: subprocess.CompletedProcess[str]) -> str:
    """Manim はエラー詳細を stdout 側に出すことがあるため両方を結合する。"""
    return "\n".join(part for part in (process.stderr, process.stdout) if part.strip())


def find_rendered_video(media_dir: Path) -> Path | None:
    """メディアディレクトリから最終出力の mp4 を探す。"""
    candidates = [
        path for path in sorted(media_dir.rglob("*.mp4")) if "partial_movie_files" not in path.parts
    ]
    return candidates[0] if candidates else None
