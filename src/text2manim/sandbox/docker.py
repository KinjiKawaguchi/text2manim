"""Docker コンテナ内で manim を実行するサンドボックス実装。

ネットワーク遮断・メモリ/CPU 制限・使い捨てコンテナにより、
LLM 生成コードの実行を隔離する。公開環境での既定サンドボックス。
"""

import os
import shutil
import subprocess
import tempfile
import uuid
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

_CONTAINER_WORKDIR = "/manim"
_DOCKER_EXECUTABLE = "docker"


class DockerSandbox:
    """manim 公式イメージを使い捨てコンテナで起動するサンドボックス。"""

    def __init__(self, settings: RenderSettings) -> None:
        """レンダリング設定を保持する。"""
        self._settings = settings

    def render(self, script: str, *, scene_name: str, output_path: Path) -> RenderResult:
        """一時ディレクトリをマウントしたコンテナ内でレンダリングする。"""
        with tempfile.TemporaryDirectory(prefix="text2manim-") as tmp:
            workdir = Path(tmp)
            (workdir / SCRIPT_FILENAME).write_text(script, encoding="utf-8")
            container_name = f"text2manim-{uuid.uuid4().hex}"
            command = self._build_command(workdir, container_name, scene_name)
            try:
                # 生成コードの実行はこのサンドボックスの本来の責務であり、
                # コマンドは固定の実行ファイルと引数リストから組み立てている。
                process = subprocess.run(  # noqa: S603
                    command,
                    capture_output=True,
                    text=True,
                    timeout=self._settings.timeout_seconds,
                    check=False,
                )
            except FileNotFoundError as exc:
                raise SandboxUnavailableError(_DOCKER_EXECUTABLE) from exc
            except subprocess.TimeoutExpired:
                _kill_container(container_name)
                return RenderFailure(
                    log=(
                        f"レンダリングが {self._settings.timeout_seconds} 秒で"
                        "タイムアウトしました。アニメーションを短く単純にしてください。"
                    )
                )
            if process.returncode != 0:
                return RenderFailure(log=combine_output(process))
            video_path = find_rendered_video(workdir / "media")
            if video_path is None:
                return RenderFailure(
                    log="manim は正常終了しましたが mp4 が見つかりません。\n"
                    + combine_output(process)
                )
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(video_path, output_path)
            return RenderSuccess(video_path=output_path)

    def _build_command(self, workdir: Path, container_name: str, scene_name: str) -> list[str]:
        """コンテナ起動のコマンドラインを組み立てる。"""
        command = [
            _DOCKER_EXECUTABLE,
            "run",
            "--rm",
            "--name",
            container_name,
            "--network",
            "none",
            f"--memory={self._settings.docker_memory_limit}",
            f"--cpus={self._settings.docker_cpu_limit}",
            "-v",
            f"{workdir}:{_CONTAINER_WORKDIR}",
            "-w",
            _CONTAINER_WORKDIR,
        ]
        if hasattr(os, "getuid"):
            # マウント先に書かれるファイルの所有者をホストユーザーに揃える
            command.extend(["--user", f"{os.getuid()}:{os.getgid()}"])
        command.extend(
            [
                self._settings.docker_image,
                "manim",
                "render",
                QUALITY_FLAGS[self._settings.quality],
                "--media_dir",
                "media",
                SCRIPT_FILENAME,
                scene_name,
            ]
        )
        return command


def _kill_container(container_name: str) -> None:
    """タイムアウトしたコンテナを停止する。失敗しても続行する (--rm で自然消滅するため)。"""
    subprocess.run(  # noqa: S603
        [_DOCKER_EXECUTABLE, "kill", container_name],
        capture_output=True,
        check=False,
        timeout=30,
    )
