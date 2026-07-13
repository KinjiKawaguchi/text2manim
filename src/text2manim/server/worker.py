"""ジョブを順に処理するバックグラウンドワーカー。

レンダリングはマシンリソースを大きく使うため、単一スレッドで直列に処理する。
生成処理は `GenerateFn` として注入し、テストではフェイクに差し替える。
"""

import queue
import threading
from typing import TYPE_CHECKING

from text2manim.errors import Text2ManimError
from text2manim.generate import generate_video
from text2manim.server.event_codec import serialize_event

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from text2manim.events import PipelineEvent
    from text2manim.generate import GenerationOptions, GenerationResult
    from text2manim.server.store import JobStore

type GenerateFn = Callable[[str, Path, Callable[[PipelineEvent], None]], GenerationResult]


def build_generate_fn(options: GenerationOptions) -> GenerateFn:
    """生成オプションを束縛した GenerateFn を作る。"""

    def _generate(
        prompt: str,
        output_path: Path,
        on_event: Callable[[PipelineEvent], None],
    ) -> GenerationResult:
        return generate_video(prompt, output_path=output_path, options=options, on_event=on_event)

    return _generate


class GenerationWorker:
    """キューからジョブを取り出してパイプラインを実行するワーカー。"""

    def __init__(self, store: JobStore, generate: GenerateFn, output_dir: Path) -> None:
        """依存を注入してワーカーを構築する。"""
        self._store = store
        self._generate = generate
        self._output_dir = output_dir
        self._queue: queue.Queue[str] = queue.Queue()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """ワーカースレッドを起動する。"""
        thread = threading.Thread(target=self._run, name="text2manim-worker", daemon=True)
        self._thread = thread
        thread.start()

    def submit(self, generation_id: str) -> None:
        """ジョブをキューに積む。"""
        self._queue.put(generation_id)

    def _run(self) -> None:
        """キューを消費し続ける。"""
        while True:
            generation_id = self._queue.get()
            self._process(generation_id)
            self._queue.task_done()

    def _process(self, generation_id: str) -> None:
        """1ジョブを処理し、進捗と結果をストアへ記録する。"""
        record = self._store.get(generation_id)
        if record is None:
            return
        self._store.update_status(generation_id, "processing")
        self._store.append_event(generation_id, {"type": "status", "status": "processing"})

        def on_event(event: PipelineEvent) -> None:
            self._store.append_event(generation_id, serialize_event(event))

        output_path = self._output_dir / f"{generation_id}.mp4"
        try:
            result = self._generate(record.prompt, output_path, on_event)
        except Text2ManimError as exc:
            self._fail(generation_id, str(exc))
        except Exception as exc:  # noqa: BLE001 -- ワーカースレッドを死なせず失敗として記録する
            self._fail(generation_id, f"予期しないエラー: {exc}")
        else:
            self._store.update_status(
                generation_id,
                "completed",
                script=result.script,
                video_path=str(result.video_path),
            )
            self._store.append_event(generation_id, {"type": "status", "status": "completed"})

    def _fail(self, generation_id: str, error: str) -> None:
        """ジョブを失敗として記録する。"""
        self._store.update_status(generation_id, "failed", error=error)
        self._store.append_event(
            generation_id, {"type": "status", "status": "failed", "error": error}
        )
