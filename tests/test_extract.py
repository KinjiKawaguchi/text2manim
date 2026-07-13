"""extract_code のテスト。"""

from text2manim.pipeline.extract import extract_code


def test_extracts_code_block_body() -> None:
    """前後の説明文があってもブロック内だけを返す。"""
    content = "説明です。\n```python\nfrom manim import *\n```\n以上です。"
    assert extract_code(content) == "from manim import *"


def test_handles_block_without_language() -> None:
    """``` だけのフェンスにも対応する。"""
    content = "```\nx = 1\n```"
    assert extract_code(content) == "x = 1"


def test_treats_whole_content_as_code() -> None:
    """生のコードが返ってきた場合はそのまま使う。"""
    content = "from manim import *\n"
    assert extract_code(content) == "from manim import *"


def test_uses_first_of_multiple_blocks() -> None:
    """複数ブロックがある応答では最初のブロックを採用する。"""
    content = "```python\na = 1\n```\n途中の説明\n```python\nb = 2\n```"
    assert extract_code(content) == "a = 1"
