"""LLM 応答からの Python コード抽出。"""

import re

_CODE_BLOCK_PATTERN = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL)


def extract_code(content: str) -> str:
    """応答テキストからコード部分を取り出す。

    コードブロックがあれば最初のブロックの中身を、なければ全体を
    コードとみなして返す。ブロック前後の説明文は無視される。
    """
    match = _CODE_BLOCK_PATTERN.search(content)
    if match is not None:
        return match.group(1).strip()
    return content.strip()
