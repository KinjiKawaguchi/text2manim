"""サーバーモード: ステートレスな生成ワーカー (REST + SSE 進捗ストリーム)。"""

from text2manim.server.app import ServerConfig, create_app

__all__ = ["ServerConfig", "create_app"]
