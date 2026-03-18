import json

from markdownbridge import MarkdownBridge


def test_valid_adaptive_card_structure():
    result = MarkdownBridge.to_teams("# Hello\n")
    data = json.loads(result)
    assert data["type"] == "AdaptiveCard"
    assert data["version"] == "1.5"
    assert "body" in data


def test_heading():
    result = MarkdownBridge.to_teams("# Hello\n")
    data = json.loads(result)
    block = data["body"][0]
    assert block["type"] == "TextBlock"
    assert block["size"] == "ExtraLarge"
    assert block["weight"] == "Bolder"
    assert "Hello" in block["text"]


def test_heading_h2():
    result = MarkdownBridge.to_teams("## Sub\n")
    data = json.loads(result)
    block = data["body"][0]
    assert block["size"] == "Large"


def test_code_block():
    result = MarkdownBridge.to_teams("```python\ncode\n```\n")
    data = json.loads(result)
    block = data["body"][0]
    assert block["type"] == "TextBlock"
    assert block["fontType"] == "Monospace"


def test_image():
    result = MarkdownBridge.to_teams("![Alt](https://example.com/img.png)\n")
    data = json.loads(result)
    # Image might be inside a paragraph or standalone
    found = False
    for el in data["body"]:
        if el.get("type") == "Image":
            assert el["url"] == "https://example.com/img.png"
            found = True
            break
    # If not found as standalone, it may be inline text
    if not found:
        # Check it appears somewhere in the output
        assert "example.com/img.png" in result


def test_table():
    md = "| A | B |\n|---|---|\n| 1 | 2 |\n"
    result = MarkdownBridge.to_teams(md)
    data = json.loads(result)
    table = data["body"][0]
    assert table["type"] == "Table"
    assert len(table["columns"]) == 2


def test_unordered_list():
    result = MarkdownBridge.to_teams("- Item 1\n- Item 2\n")
    data = json.loads(result)
    block = data["body"][0]
    assert block["type"] == "TextBlock"
    assert "Item 1" in block["text"]
    assert "Item 2" in block["text"]


def test_full_document(sample_markdown):
    result = MarkdownBridge.to_teams(sample_markdown)
    data = json.loads(result)
    assert data["type"] == "AdaptiveCard"
    assert len(data["body"]) > 3
