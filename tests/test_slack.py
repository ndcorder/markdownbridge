from markdownbridge import MarkdownBridge


def test_heading():
    result = MarkdownBridge.to_slack("# Hello\n")
    assert "*Hello*" in result


def test_bold():
    result = MarkdownBridge.to_slack("**bold**\n")
    assert "*bold*" in result


def test_italic():
    result = MarkdownBridge.to_slack("*italic*\n")
    assert "_italic_" in result


def test_strikethrough():
    result = MarkdownBridge.to_slack("~~deleted~~\n")
    assert "~deleted~" in result


def test_code_inline():
    result = MarkdownBridge.to_slack("`code`\n")
    assert "`code`" in result


def test_code_block():
    result = MarkdownBridge.to_slack("```python\nprint('hi')\n```\n")
    assert "```" in result
    assert "print('hi')" in result


def test_link():
    result = MarkdownBridge.to_slack("[Click](https://example.com)\n")
    assert "<https://example.com|Click>" in result


def test_image():
    result = MarkdownBridge.to_slack("![Alt](https://example.com/img.png)\n")
    assert "<https://example.com/img.png>" in result


def test_blockquote():
    result = MarkdownBridge.to_slack("> quoted\n")
    assert "&gt;" in result
    assert "quoted" in result


def test_table_preformatted():
    md = "| A | B |\n|---|---|\n| 1 | 2 |\n"
    result = MarkdownBridge.to_slack(md)
    assert "```" in result


def test_unordered_list():
    result = MarkdownBridge.to_slack("- Item 1\n- Item 2\n")
    assert "\u2022" in result  # bullet character
    assert "Item 1" in result


def test_ordered_list():
    result = MarkdownBridge.to_slack("1. First\n2. Second\n")
    assert "1." in result
    assert "First" in result
