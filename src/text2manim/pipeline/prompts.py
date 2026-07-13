"""LLM へ渡すプロンプトの構築。

プロンプト本文は英語で書く。Manim のドキュメント・エラーメッセージが英語であり、
コード生成の品質が安定するため。
"""

from text2manim.llm import ChatMessage

SCENE_NAME = "GeneratedScene"

SYSTEM_PROMPT = f"""\
You are an expert Manim (Community Edition) developer.
Generate a complete, runnable Manim script from the user's request.

Rules:
- Define exactly one Scene subclass named `{SCENE_NAME}`.
- Use only Manim Community Edition and the Python standard library.
- Do not read or write files, access the network, or use external assets.
- Use `Tex`/`MathTex` only for mathematical notation; use `Text` for plain text
  (including non-ASCII text such as Japanese).
- Keep the total animation length reasonable (roughly 15-60 seconds).
- Output ONLY Python code in a single ```python code block. No explanations.
"""


def build_initial_message(prompt: str) -> ChatMessage:
    """ユーザーの依頼文から最初のメッセージを組み立てる。"""
    return ChatMessage(
        role="user",
        content=(
            "Create a Manim script for the following request:\n\n"
            f"{prompt}\n\n"
            "Output only the Python code."
        ),
    )


def build_repair_message(log: str) -> ChatMessage:
    """検証・レンダリングの失敗ログから修復依頼メッセージを組み立てる。"""
    return ChatMessage(
        role="user",
        content=(
            "The script has a problem. Here is the error output:\n\n"
            f"```\n{log}\n```\n\n"
            "Fix the problem and return the FULL corrected script. "
            "Output only the Python code."
        ),
    )
