from markdownbridge.reverse.jira_to_md import jira_to_markdown
from markdownbridge import MarkdownBridge


def test_heading():
    result = jira_to_markdown("h1. Hello\n")
    assert "# Hello" in result


def test_heading_h3():
    result = jira_to_markdown("h3. Sub\n")
    assert "### Sub" in result


def test_bold():
    result = jira_to_markdown("*bold text*\n")
    assert "**bold text**" in result


def test_italic():
    result = jira_to_markdown("_italic text_\n")
    assert "*italic text*" in result


def test_strikethrough():
    result = jira_to_markdown("-deleted-\n")
    assert "~~deleted~~" in result


def test_code_inline():
    result = jira_to_markdown("{{code}}\n")
    assert "`code`" in result


def test_code_block():
    jira = "{code:python}\nprint('hi')\n{code}\n"
    result = jira_to_markdown(jira)
    assert "```python" in result
    assert "print('hi')" in result
    assert "```" in result


def test_link():
    result = jira_to_markdown("[Click|https://example.com]\n")
    assert "[Click](https://example.com)" in result


def test_image():
    result = jira_to_markdown("!https://example.com/img.png!\n")
    assert "![](https://example.com/img.png)" in result


def test_unordered_list():
    result = jira_to_markdown("* Item 1\n* Item 2\n")
    assert "- Item 1" in result
    assert "- Item 2" in result


def test_ordered_list():
    result = jira_to_markdown("# First\n# Second\n")
    assert "1. First" in result
    assert "1. Second" in result


def test_table_header():
    result = jira_to_markdown("||Name||Age||\n|Alice|30|\n")
    assert "| Name | Age |" in result
    assert "| Alice | 30 |" in result


def test_horizontal_rule():
    result = jira_to_markdown("----\n")
    assert "---" in result


def test_quote():
    result = jira_to_markdown("{quote}\nhello\n{quote}\n")
    assert "> hello" in result


def test_round_trip_heading():
    md = "# Hello\n"
    jira = MarkdownBridge.to_jira(md)
    back = MarkdownBridge.from_jira(jira)
    assert "# Hello" in back


def test_round_trip_bold():
    md = "**bold**\n"
    jira = MarkdownBridge.to_jira(md)
    back = MarkdownBridge.from_jira(jira)
    assert "**bold**" in back
