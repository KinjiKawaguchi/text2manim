"""ホスト上で manim を直接実行するサンドボックス実装。

プロセスレベルの隔離がないため、信頼できる環境での利用と、
Cloud Run などコンテナ自体が隔離境界となるデーモンレス環境を想定する。
LLM API キー等のシークレットを生成コードへ渡さないよう、
subprocess の環境変数は許可リスト方式で最小化する。
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from text2manim.errors import SandboxUnavailableError
from text2manim.sandbox.base import RenderFailure, RenderResult, RenderSuccess
from text2manim.sandbox.common import (
    QUALITY_FLAGS,
    SCRIPT_FILENAME,
    combine_output,
    find_rendered_video,
)

if TYPE_CHECKING:
    from text2manim.config import RenderSettings

_INHERITED_ENV_VARS = ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR")


class LocalSandbox:
    """PATH 上の manim を subprocess で起動するサンドボックス。"""

    def __init__(self, settings: RenderSettings) -> None:
        """レンダリング設定を保持する。"""
        self._settings = settings

    def render(self, script: str, *, scene_name: str, output_path: Path) -> RenderResult:
        """一時ディレクトリ内でスクリプトをレンダリングする。"""
        with tempfile.TemporaryDirectory(prefix="text2manim-") as tmp:
            workdir = Path(tmp)
            (workdir / SCRIPT_FILENAME).write_text(script, encoding="utf-8")
            media_dir = workdir / "media"
            command = [
                self._settings.manim_executable,
                "render",
                QUALITY_FLAGS[self._settings.quality],
                "--media_dir",
                str(media_dir),
                SCRIPT_FILENAME,
                scene_name,
            ]
            try:
                # 生成コードの実行はこのサンドボックスの本来の責務であり、
                # コマンドは固定の実行ファイルと引数リストから組み立てている。
                process = subprocess.run(  # noqa: S603
                    command,
                    cwd=workdir,
                    capture_output=True,
                    text=True,
                    timeout=self._settings.timeout_seconds,
                    check=False,
                    env=_minimal_env(),
                )
            except FileNotFoundError as exc:
                raise SandboxUnavailableError(self._settings.manim_executable) from exc
            except subprocess.TimeoutExpired:
                return RenderFailure(
                    log=(
                        f"レンダリングが {self._settings.timeout_seconds} 秒で"
                        "タイムアウトしました。アニメーションを短く単純にしてください。"
                    )
                )
            if process.returncode != 0:
                return RenderFailure(log=combine_output(process))
            video_path = find_rendered_video(media_dir)
            if video_path is None:
                return RenderFailure(
                    log="manim は正常終了しましたが mp4 が見つかりません。\n"
                    + combine_output(process)
                )
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(video_path, output_path)
            return RenderSuccess(video_path=output_path)


def _minimal_env() -> dict[str, str]:
    """レンダリング subprocess に渡す最小限の環境変数を組み立てる。

    LLM API キー等のシークレットを生成コードに継承させないため、
    許可リスト方式で構成する。
    """
    return {
        name: value for name in _INHERITED_ENV_VARS if (value := os.environ.get(name)) is not None
    }
