from markdownbridge import MarkdownBridge


def test_heading():
    result = MarkdownBridge.to_confluence("# Hello\n")
    assert "<h1>Hello</h1>" in result


def test_bold():
    result = MarkdownBridge.to_confluence("**bold**\n")
    assert "<strong>bold</strong>" in result


def test_italic():
    result = MarkdownBridge.to_confluence("*italic*\n")
    assert "<em>italic</em>" in result


def test_code_inline():
    result = MarkdownBridge.to_confluence("`code`\n")
    assert "<code>code</code>" in result


def test_code_block():
    result = MarkdownBridge.to_confluence('```python\nprint("hi")\n```\n')
    assert '<ac:structured-macro ac:name="code">' in result
    assert '<ac:parameter ac:name="language">python</ac:parameter>' in result
    assert "<![CDATA[" in result
    assert 'print("hi")' in result


def test_link():
    result = MarkdownBridge.to_confluence("[Click](https://example.com)\n")
    assert '<a href="https://example.com">Click</a>' in result


def test_image():
    result = MarkdownBridge.to_confluence(
        "![Alt](https://example.com/img.png)\n"
    )
    assert "<ac:image>" in result
    assert 'ri:value="https://example.com/img.png"' in result


def test_unordered_list():
    result = MarkdownBridge.to_confluence("- Item 1\n- Item 2\n")
    assert "<ul>" in result
    assert "<li>" in result


def test_ordered_list():
    result = MarkdownBridge.to_confluence("1. First\n2. Second\n")
    assert "<ol>" in result
    assert "<li>" in result


def test_table():
    md = "| Name | Age |\n|------|-----|\n| Alice | 30 |\n"
    result = MarkdownBridge.to_confluence(md)
    assert "<table>" in result
    assert "<tbody>" in result
    assert "<th>" in result
    assert "<td>" in result


def test_blockquote():
    result = MarkdownBridge.to_confluence("> quoted\n")
    assert "<blockquote>" in result


def test_horizontal_rule():
    result = MarkdownBridge.to_confluence("---\n")
    assert "<hr />" in result


def test_strikethrough():
    result = MarkdownBridge.to_confluence("~~deleted~~\n")
    assert "text-decoration: line-through" in result


def test_full_document(sample_markdown):
    result = MarkdownBridge.to_confluence(sample_markdown)
    assert "<h1>" in result
    assert "<strong>" in result
    assert "<em>" in result
    assert "<code>" in result
