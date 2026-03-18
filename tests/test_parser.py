from markdownbridge.parser import parse
from markdownbridge.ast_nodes import (
    Bold,
    Blockquote,
    Code,
    CodeBlock,
    Document,
    Heading,
    HorizontalRule,
    Image,
    Italic,
    Link,
    ListItem,
    OrderedList,
    Paragraph,
    Strikethrough,
    Table,
    Text,
    UnorderedList,
)


def test_parse_heading_levels():
    for level in range(1, 7):
        doc = parse(f"{'#' * level} Heading {level}\n")
        assert isinstance(doc, Document)
        assert len(doc.children) == 1
        h = doc.children[0]
        assert isinstance(h, Heading)
        assert h.level == level


def test_parse_bold():
    doc = parse("**bold text**\n")
    p = doc.children[0]
    assert isinstance(p, Paragraph)
    bold = p.children[0]
    assert isinstance(bold, Bold)
    assert isinstance(bold.children[0], Text)
    assert bold.children[0].content == "bold text"


def test_parse_italic():
    doc = parse("*italic text*\n")
    p = doc.children[0]
    assert isinstance(p, Paragraph)
    it = p.children[0]
    assert isinstance(it, Italic)
    assert it.children[0].content == "italic text"


def test_parse_code_inline():
    doc = parse("`some code`\n")
    p = doc.children[0]
    code = p.children[0]
    assert isinstance(code, Code)
    assert code.content == "some code"


def test_parse_code_block_with_language():
    doc = parse("```python\nprint('hi')\n```\n")
    cb = doc.children[0]
    assert isinstance(cb, CodeBlock)
    assert cb.language == "python"
    assert "print('hi')" in cb.content


def test_parse_code_block_without_language():
    doc = parse("```\nhello\n```\n")
    cb = doc.children[0]
    assert isinstance(cb, CodeBlock)
    assert cb.language is None
    assert "hello" in cb.content


def test_parse_link():
    doc = parse("[Click](https://example.com)\n")
    p = doc.children[0]
    link = p.children[0]
    assert isinstance(link, Link)
    assert link.url == "https://example.com"
    assert link.children[0].content == "Click"


def test_parse_image():
    doc = parse("![Alt text](https://example.com/img.png)\n")
    p = doc.children[0]
    img = p.children[0]
    assert isinstance(img, Image)
    assert img.url == "https://example.com/img.png"
    assert img.alt == "Alt text"


def test_parse_unordered_list():
    doc = parse("- Item 1\n- Item 2\n")
    ul = doc.children[0]
    assert isinstance(ul, UnorderedList)
    assert len(ul.children) == 2
    assert isinstance(ul.children[0], ListItem)


def test_parse_ordered_list():
    doc = parse("1. First\n2. Second\n")
    ol = doc.children[0]
    assert isinstance(ol, OrderedList)
    assert len(ol.children) == 2


def test_parse_nested_list():
    doc = parse("- Item 1\n  - Nested\n")
    ul = doc.children[0]
    assert isinstance(ul, UnorderedList)
    li = ul.children[0]
    assert isinstance(li, ListItem)
    # Nested list should be a child of the list item
    has_nested = any(isinstance(c, UnorderedList) for c in li.children)
    assert has_nested


def test_parse_table():
    md = "| Name | Age |\n|------|-----|\n| Alice | 30 |\n"
    doc = parse(md)
    table = doc.children[0]
    assert isinstance(table, Table)
    assert len(table.headers) == 2
    assert len(table.rows) == 1


def test_parse_blockquote():
    doc = parse("> quoted text\n")
    bq = doc.children[0]
    assert isinstance(bq, Blockquote)


def test_parse_horizontal_rule():
    doc = parse("---\n")
    hr = doc.children[0]
    assert isinstance(hr, HorizontalRule)


def test_parse_strikethrough():
    doc = parse("~~deleted~~\n")
    p = doc.children[0]
    s = p.children[0]
    assert isinstance(s, Strikethrough)
    assert s.children[0].content == "deleted"


def test_parse_empty_document():
    doc = parse("")
    assert isinstance(doc, Document)
    assert len(doc.children) == 0


def test_parse_mixed_content(sample_markdown):
    doc = parse(sample_markdown)
    assert isinstance(doc, Document)
    assert len(doc.children) > 5  # Should have multiple elements
