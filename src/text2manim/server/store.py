"""SQLite によるジョブと進捗イベントの永続化。

外部DBを必須にしないためのセルフホスト向け実装。接続は操作ごとに開閉し、
WAL モードでワーカースレッドと API スレッドの並行アクセスを成立させる。
"""

import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from pathlib import Path

type GenerationStatus = Literal["pending", "processing", "completed", "failed"]

_SCHEMA = """
CREATE TABLE IF NOT EXISTS generations (
    id TEXT PRIMARY KEY,
    prompt TEXT NOT NULL,
    status TEXT NOT NULL,
    script TEXT,
    video_path TEXT,
    error TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS generation_events (
    seq INTEGER PRIMARY KEY AUTOINCREMENT,
    generation_id TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_events_generation
    ON generation_events (generation_id, seq);
"""


@dataclass(frozen=True, slots=True)
class GenerationRecord:
    """1つの動画生成ジョブの状態。"""

    id: str
    prompt: str
    status: GenerationStatus
    script: str | None
    video_path: str | None
    error: str | None
    created_at: str
    updated_at: str


@dataclass(frozen=True, slots=True)
class StoredEvent:
    """永続化された進捗イベント。payload は JSON 文字列。"""

    seq: int
    payload: str


class JobStore:
    """SQLite バックエンドのジョブストア。"""

    def __init__(self, db_path: Path) -> None:
        """データベースファイルを開き、スキーマを初期化する。"""
        self._db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.executescript(_SCHEMA)

    def create(self, prompt: str) -> GenerationRecord:
        """新しいジョブを pending 状態で登録する。"""
        now = _utc_now()
        record = GenerationRecord(
            id=uuid.uuid4().hex,
            prompt=prompt,
            status="pending",
            script=None,
            video_path=None,
            error=None,
            created_at=now,
            updated_at=now,
        )
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO generations"
                " (id, prompt, status, script, video_path, error, created_at, updated_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    record.id,
                    record.prompt,
                    record.status,
                    record.script,
                    record.video_path,
                    record.error,
                    record.created_at,
                    record.updated_at,
                ),
            )
        return record

    def get(self, generation_id: str) -> GenerationRecord | None:
        """ジョブを取得する。存在しなければ None。"""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, prompt, status, script, video_path, error, created_at, updated_at"
                " FROM generations WHERE id = ?",
                (generation_id,),
            ).fetchone()
        if row is None:
            return None
        return _record_from_row(row)

    def update_status(
        self,
        generation_id: str,
        status: GenerationStatus,
        *,
        script: str | None = None,
        video_path: str | None = None,
        error: str | None = None,
    ) -> None:
        """ジョブの状態と結果フィールドを更新する。"""
        with self._connect() as conn:
            conn.execute(
                "UPDATE generations SET status = ?,"
                " script = COALESCE(?, script),"
                " video_path = COALESCE(?, video_path),"
                " error = COALESCE(?, error),"
                " updated_at = ? WHERE id = ?",
                (status, script, video_path, error, _utc_now(), generation_id),
            )

    def append_event(self, generation_id: str, payload: dict[str, object]) -> None:
        """進捗イベントを追記する。"""
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO generation_events (generation_id, payload, created_at)"
                " VALUES (?, ?, ?)",
                (generation_id, json.dumps(payload, ensure_ascii=False), _utc_now()),
            )

    def list_events(self, generation_id: str, *, after_seq: int = 0) -> list[StoredEvent]:
        """指定シーケンス番号より後の進捗イベントを取得する。"""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT seq, payload FROM generation_events"
                " WHERE generation_id = ? AND seq > ? ORDER BY seq",
                (generation_id, after_seq),
            ).fetchall()
        return [StoredEvent(seq=int(row[0]), payload=str(row[1])) for row in rows]

    def _connect(self) -> sqlite3.Connection:
        """操作ごとの新しい接続を返す。"""
        return sqlite3.connect(self._db_path, timeout=30.0)


_KNOWN_STATUSES: dict[str, GenerationStatus] = {
    "pending": "pending",
    "processing": "processing",
    "completed": "completed",
    "failed": "failed",
}


def _record_from_row(row: tuple[object, ...]) -> GenerationRecord:
    """SELECT 結果の行を GenerationRecord に変換する。"""
    status = _KNOWN_STATUSES.get(str(row[2]))
    if status is None:
        message = f"不正なステータスがDBに保存されています: {row[2]}"
        raise ValueError(message)
    return GenerationRecord(
        id=str(row[0]),
        prompt=str(row[1]),
        status=status,
        script=None if row[3] is None else str(row[3]),
        video_path=None if row[4] is None else str(row[4]),
        error=None if row[5] is None else str(row[5]),
        created_at=str(row[6]),
        updated_at=str(row[7]),
    )


def _utc_now() -> str:
    """UTC の ISO 8601 文字列を返す。"""
    return datetime.now(UTC).isoformat()
