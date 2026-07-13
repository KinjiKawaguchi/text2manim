"""validate_script のテスト。"""

from text2manim.pipeline.validate import validate_script

VALID_SCRIPT = """
from manim import Scene, Square

class GeneratedScene(Scene):
    def construct(self):
        self.add(Square())
"""


def test_accepts_valid_script() -> None:
    """正しいスクリプトは None を返す。"""
    assert validate_script(VALID_SCRIPT, scene_name="GeneratedScene") is None


def test_rejects_syntax_error() -> None:
    """構文エラーは行番号付きで報告する。"""
    result = validate_script("def broken(:\n    pass", scene_name="GeneratedScene")
    assert result is not None
    assert "SyntaxError" in result


def test_rejects_missing_scene_class() -> None:
    """指定名の Scene クラスがなければ報告する。"""
    result = validate_script("x = 1", scene_name="GeneratedScene")
    assert result is not None
    assert "GeneratedScene" in result


def test_rejects_forbidden_import() -> None:
    """禁止モジュールの import を検出する。"""
    script = "import subprocess\n" + VALID_SCRIPT
    result = validate_script(script, scene_name="GeneratedScene")
    assert result is not None
    assert "subprocess" in result


def test_rejects_forbidden_import_from() -> None:
    """from形式・サブモジュール形式の import も検出する。"""
    script = "from urllib.request import urlopen\n" + VALID_SCRIPT
    result = validate_script(script, scene_name="GeneratedScene")
    assert result is not None
    assert "urllib" in result
