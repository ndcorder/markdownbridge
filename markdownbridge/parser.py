from __future__ import annotations

from markdown_it import MarkdownIt

from .ast_nodes import (
    Blockquote,
    Bold,
    Code,
    CodeBlock,
    Document,
    Heading,
    HorizontalRule,
    Image,
    Italic,
    LineBreak,
    Link,
    ListItem,
    Node,
    OrderedList,
    Paragraph,
    SoftBreak,
    Strikethrough,
    Table,
    Text,
    UnorderedList,
)


def parse(markdown: str) -> Document:
    md = MarkdownIt("commonmark", {"typographer": False})
    md.enable("table")
    md.enable("strikethrough")
    tokens = md.parse(markdown)
    return _build_document(tokens)


def _build_document(tokens: list) -> Document:
    doc = Document()
    stack: list[Node] = [doc]
    i = 0
    while i < len(tokens):
        token = tokens[i]
        ttype = token.type

        if ttype == "heading_open":
            level = int(token.tag[1])
            node = Heading(level=level)
            stack[-1].children.append(node)
            stack.append(node)

        elif ttype == "heading_close":
            stack.pop()

        elif ttype == "paragraph_open":
            node = Paragraph()
            stack[-1].children.append(node)
            stack.append(node)

        elif ttype == "paragraph_close":
            stack.pop()

        elif ttype == "blockquote_open":
            node = Blockquote()
            stack[-1].children.append(node)
            stack.append(node)

        elif ttype == "blockquote_close":
            stack.pop()

        elif ttype == "bullet_list_open":
            node = UnorderedList()
            stack[-1].children.append(node)
            stack.append(node)

        elif ttype == "bullet_list_close":
            stack.pop()

        elif ttype == "ordered_list_open":
            start = 1
            if token.attrGet("start") is not None:
                start = int(token.attrGet("start"))
            node = OrderedList(start=start)
            stack[-1].children.append(node)
            stack.append(node)

        elif ttype == "ordered_list_close":
            stack.pop()

        elif ttype == "list_item_open":
            node = ListItem()
            stack[-1].children.append(node)
            stack.append(node)

        elif ttype == "list_item_close":
            stack.pop()

        elif ttype == "fence":
            lang = token.info.strip() if token.info and token.info.strip() else None
            node = CodeBlock(content=token.content, language=lang)
            stack[-1].children.append(node)

        elif ttype == "code_block":
            node = CodeBlock(content=token.content)
            stack[-1].children.append(node)

        elif ttype == "hr":
            stack[-1].children.append(HorizontalRule())

        elif ttype == "inline":
            _process_inline(token.children or [], stack[-1])

        elif ttype == "html_block":
            stack[-1].children.append(Text(content=token.content))

        elif ttype in ("thead_open", "thead_close", "tbody_open", "tbody_close"):
            pass

        elif ttype == "table_open":
            table_node, end_i = _process_table(tokens, i)
            stack[-1].children.append(table_node)
            i = end_i
            i += 1
            continue

        i += 1

    return doc


def _process_inline(tokens: list, parent: Node) -> None:
    stack: list[Node] = [parent]
    for token in tokens:
        ttype = token.type

        if ttype == "text":
            if token.content:
                stack[-1].children.append(Text(content=token.content))

        elif ttype == "code_inline":
            stack[-1].children.append(Code(content=token.content))

        elif ttype == "softbreak":
            stack[-1].children.append(SoftBreak())

        elif ttype == "hardbreak":
            stack[-1].children.append(LineBreak())

        elif ttype == "strong_open":
            node = Bold()
            stack[-1].children.append(node)
            stack.append(node)

        elif ttype == "strong_close":
            stack.pop()

        elif ttype == "em_open":
            node = Italic()
            stack[-1].children.append(node)
            stack.append(node)

        elif ttype == "em_close":
            stack.pop()

        elif ttype == "s_open":
            node = Strikethrough()
            stack[-1].children.append(node)
            stack.append(node)

        elif ttype == "s_close":
            stack.pop()

        elif ttype == "link_open":
            url = token.attrGet("href") or ""
            title = token.attrGet("title")
            node = Link(url=url, title=title)
            stack[-1].children.append(node)
            stack.append(node)

        elif ttype == "link_close":
            stack.pop()

        elif ttype == "image":
            url = token.attrGet("src") or ""
            alt = token.content or ""
            title = token.attrGet("title")
            node = Image(url=url, alt=alt, title=title)
            stack[-1].children.append(node)

        elif ttype == "html_inline":
            stack[-1].children.append(Text(content=token.content))


def _process_table(tokens: list, start: int) -> tuple[Table, int]:
    table = Table()
    i = start + 1
    in_header = False
    current_row: list[Node] = []
    current_cell: Node | None = None

    while i < len(tokens):
        token = tokens[i]
        ttype = token.type

        if ttype == "table_close":
            return table, i

        elif ttype == "thead_open":
            in_header = True

        elif ttype == "thead_close":
            in_header = False

        elif ttype == "tbody_open":
            pass

        elif ttype == "tbody_close":
            pass

        elif ttype == "tr_open":
            current_row = []

        elif ttype == "tr_close":
            if in_header:
                table.headers = current_row
            else:
                table.rows.append(current_row)

        elif ttype in ("th_open", "td_open"):
            current_cell = Paragraph()

        elif ttype in ("th_close", "td_close"):
            if current_cell is not None:
                current_row.append(current_cell)
            current_cell = None

        elif ttype == "inline":
            if current_cell is not None:
                _process_inline(token.children or [], current_cell)

        i += 1

    return table, i
