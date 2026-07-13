"""生成スクリプトのレンダリング前の静的検証。

サンドボックスの起動には秒単位のコストがかかるため、静的に検出できる問題は
ミリ秒で弾いて修復ループへ直接返す。セキュリティ境界はあくまでサンドボックスであり、
ここでの禁止 import チェックは多層防御と高速失敗を目的とする。
"""

import ast

_FORBIDDEN_MODULES = frozenset({"subprocess", "socket", "ctypes", "urllib", "http", "requests"})


def validate_script(script: str, *, scene_name: str) -> str | None:
    """スクリプトを静的に検証し、問題があれば LLM へ返すエラーメッセージを返す。

    問題がなければ None を返す。
    """
    try:
        tree = ast.parse(script)
    except SyntaxError as exc:
        return f"SyntaxError: {exc.msg} (line {exc.lineno})"
    forbidden = _find_forbidden_imports(tree)
    if forbidden:
        modules = ", ".join(sorted(forbidden))
        return (
            f"The script imports forbidden module(s): {modules}. "
            "Use only Manim and safe standard-library modules (math, random, etc.)."
        )
    if not _has_class(tree, scene_name):
        return f"The script must define a Scene subclass named `{scene_name}`."
    return None


def _find_forbidden_imports(tree: ast.Module) -> frozenset[str]:
    """禁止モジュールの import をトップレベル名で検出する。"""
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            found.add(node.module.split(".")[0])
    return frozenset(found & _FORBIDDEN_MODULES)


def _has_class(tree: ast.Module, class_name: str) -> bool:
    """指定名のクラス定義が存在するかを調べる。"""
    return any(
        isinstance(node, ast.ClassDef) and node.name == class_name for node in ast.walk(tree)
    )
