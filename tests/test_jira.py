from markdownbridge import MarkdownBridge


def test_heading():
    result = MarkdownBridge.to_jira("# Hello\n")
    assert "h1. Hello" in result


def test_heading_h2():
    result = MarkdownBridge.to_jira("## Sub\n")
    assert "h2. Sub" in result


def test_bold():
    result = MarkdownBridge.to_jira("**bold**\n")
    assert "*bold*" in result


def test_italic():
    result = MarkdownBridge.to_jira("*italic*\n")
    assert "_italic_" in result


def test_strikethrough():
    result = MarkdownBridge.to_jira("~~deleted~~\n")
    assert "-deleted-" in result


def test_code_inline():
    result = MarkdownBridge.to_jira("`code`\n")
    assert "{{code}}" in result


def test_code_block():
    result = MarkdownBridge.to_jira("```python\nprint('hi')\n```\n")
    assert "{code:python}" in result
    assert "print('hi')" in result
    assert "{code}" in result


def test_code_block_no_lang():
    result = MarkdownBridge.to_jira("```\nhello\n```\n")
    assert "{code}\nhello\n{code}" in result


def test_link():
    result = MarkdownBridge.to_jira("[Click](https://example.com)\n")
    assert "[Click|https://example.com]" in result


def test_image():
    result = MarkdownBridge.to_jira("![Alt](https://example.com/img.png)\n")
    assert "!https://example.com/img.png!" in result


def test_unordered_list():
    result = MarkdownBridge.to_jira("- Item 1\n- Item 2\n")
    assert "* Item 1" in result
    assert "* Item 2" in result


def test_ordered_list():
    result = MarkdownBridge.to_jira("1. First\n2. Second\n")
    assert "# First" in result
    assert "# Second" in result


def test_nested_list():
    result = MarkdownBridge.to_jira("- Item 1\n  - Nested\n")
    assert "* Item 1" in result
    assert "** Nested" in result


def test_table():
    md = "| Name | Age |\n|------|-----|\n| Alice | 30 |\n"
    result = MarkdownBridge.to_jira(md)
    assert "||Name||Age||" in result
    assert "|Alice|30|" in result


def test_blockquote():
    result = MarkdownBridge.to_jira("> quoted\n")
    assert "{quote}" in result
    assert "quoted" in result


def test_horizontal_rule():
    result = MarkdownBridge.to_jira("---\n")
    assert "----" in result
