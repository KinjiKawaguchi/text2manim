"""text2manim の例外階層。

メッセージは例外クラス自身が持ち、送出側は文脈情報だけを渡す。
"""


class Text2ManimError(Exception):
    """text2manim が送出するすべての例外の基底クラス。"""


class MissingModelError(Text2ManimError):
    """モデル名が必要なプロバイダーでモデル名が未指定。"""

    def __init__(self) -> None:
        """既定メッセージで初期化する。"""
        super().__init__("openai-compatible プロバイダーではモデル名の指定が必須です (--model)")


class EmptyLlmResponseError(Text2ManimError):
    """LLM の応答に利用可能なテキストが含まれていない。"""

    def __init__(self) -> None:
        """既定メッセージで初期化する。"""
        super().__init__("LLMの応答にテキストが含まれていません")


class SandboxUnavailableError(Text2ManimError):
    """レンダリング実行環境が利用できない。"""

    def __init__(self, executable: str) -> None:
        """見つからなかった実行ファイル名を添えて初期化する。"""
        super().__init__(
            f"manim 実行ファイルが見つかりません: {executable}"
            " (インストール方法: https://docs.manim.community/)"
        )
        self.executable = executable


class RenderExhaustedError(Text2ManimError):
    """すべての試行でレンダリングに失敗した。"""

    def __init__(self, attempts: int, last_log: str) -> None:
        """試行回数と最後のレンダリングログを保持して初期化する。"""
        super().__init__(f"{attempts}回の試行すべてでレンダリングに失敗しました")
        self.attempts = attempts
        self.last_log = last_log
