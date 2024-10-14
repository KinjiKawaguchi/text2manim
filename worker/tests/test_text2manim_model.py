import pytest
from models.text2manim_model import extract_code_from_markdown


def test_extract_code_from_markdown_with_python_code_block():
    markdown_content = """```python
def hello_world():
    print("Hello, World!")
```"""
    expected_output = """def hello_world():
    print("Hello, World!")"""
    assert extract_code_from_markdown(markdown_content) == expected_output


def test_extract_code_from_markdown_with_no_language_specified():
    markdown_content = """```
def hello_world():
    print("Hello, World!")
```"""
    expected_output = """def hello_world():
    print("Hello, World!")"""
    assert extract_code_from_markdown(markdown_content) == expected_output


def test_extract_code_from_markdown_with_multiple_code_blocks():
    markdown_content = """```python
def first_function():
    pass
```
Some text in between
```python
def second_function():
    pass
```"""
    expected_output = """def first_function():
    pass"""
    assert extract_code_from_markdown(markdown_content) == expected_output


def test_extract_code_from_markdown_with_no_code_block():
    content = "This is just plain text without any code block."
    assert extract_code_from_markdown(content) == content


def test_extract_code_from_markdown_with_empty_string():
    assert extract_code_from_markdown("") == ""


def test_extract_code_from_markdown_with_only_opening_markdown():
    content = "```python\ndef incomplete_function():"
    assert extract_code_from_markdown(content) == content


def test_extract_code_from_markdown_with_only_closing_markdown():
    content = "def incomplete_function():\n```"
    assert extract_code_from_markdown(content) == content


def test_extract_code_from_markdown_with_nested_code_blocks():
    markdown_content = """```python
def outer_function():
    ```
    def inner_function():
        pass
    ```
    pass
```"""
    expected_output = """def outer_function():
    ```
    def inner_function():
        pass
    ```
    pass"""
    assert extract_code_from_markdown(markdown_content) == expected_output


def test_extract_code_from_markdown_with_inline_code():
    content = "This is text with `inline code` which should not be extracted."
    assert extract_code_from_markdown(content) == content


def test_extract_code_from_markdown_with_multiline_code():
    markdown_content = """```python
def multiline_function():
    print("This is a")
    print("multiline function")
    return None
```"""
    expected_output = """def multiline_function():
    print("This is a")
    print("multiline function")
    return None"""
    assert extract_code_from_markdown(markdown_content) == expected_output
