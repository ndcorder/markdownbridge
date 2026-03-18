import json

from markdownbridge import MarkdownBridge


def test_valid_adf_structure():
    result = MarkdownBridge.to_confluence_adf("# Hello\n")
    data = json.loads(result)
    assert data["version"] == 1
    assert data["type"] == "doc"
    assert "content" in data


def test_heading():
    result = MarkdownBridge.to_confluence_adf("# Hello\n")
    data = json.loads(result)
    heading = data["content"][0]
    assert heading["type"] == "heading"
    assert heading["attrs"]["level"] == 1


def test_bold_text_has_strong_mark():
    result = MarkdownBridge.to_confluence_adf("**bold**\n")
    data = json.loads(result)
    para = data["content"][0]
    assert para["type"] == "paragraph"
    text_node = para["content"][0]
    assert text_node["type"] == "text"
    assert any(m["type"] == "strong" for m in text_node.get("marks", []))


def test_italic_text_has_em_mark():
    result = MarkdownBridge.to_confluence_adf("*italic*\n")
    data = json.loads(result)
    para = data["content"][0]
    text_node = para["content"][0]
    assert any(m["type"] == "em" for m in text_node.get("marks", []))


def test_code_block():
    result = MarkdownBridge.to_confluence_adf("```python\ncode\n```\n")
    data = json.loads(result)
    cb = data["content"][0]
    assert cb["type"] == "codeBlock"
    assert cb["attrs"]["language"] == "python"


def test_link_produces_link_mark():
    result = MarkdownBridge.to_confluence_adf("[Click](https://example.com)\n")
    data = json.loads(result)
    para = data["content"][0]
    text_node = para["content"][0]
    link_marks = [m for m in text_node.get("marks", []) if m["type"] == "link"]
    assert len(link_marks) == 1
    assert link_marks[0]["attrs"]["href"] == "https://example.com"


def test_bullet_list():
    result = MarkdownBridge.to_confluence_adf("- Item 1\n- Item 2\n")
    data = json.loads(result)
    bl = data["content"][0]
    assert bl["type"] == "bulletList"
    assert len(bl["content"]) == 2
    assert bl["content"][0]["type"] == "listItem"


def test_ordered_list():
    result = MarkdownBridge.to_confluence_adf("1. First\n2. Second\n")
    data = json.loads(result)
    ol = data["content"][0]
    assert ol["type"] == "orderedList"


def test_table():
    md = "| A | B |\n|---|---|\n| 1 | 2 |\n"
    result = MarkdownBridge.to_confluence_adf(md)
    data = json.loads(result)
    table = data["content"][0]
    assert table["type"] == "table"
    assert table["content"][0]["content"][0]["type"] == "tableHeader"


def test_blockquote():
    result = MarkdownBridge.to_confluence_adf("> quote\n")
    data = json.loads(result)
    bq = data["content"][0]
    assert bq["type"] == "blockquote"


def test_horizontal_rule():
    result = MarkdownBridge.to_confluence_adf("---\n")
    data = json.loads(result)
    rule = data["content"][0]
    assert rule["type"] == "rule"


def test_full_document(sample_markdown):
    result = MarkdownBridge.to_confluence_adf(sample_markdown)
    data = json.loads(result)
    assert data["version"] == 1
    assert data["type"] == "doc"
    assert len(data["content"]) > 5
