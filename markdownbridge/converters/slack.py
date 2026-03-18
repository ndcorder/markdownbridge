from __future__ import annotations

from ..ast_nodes import (
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
from .base import BaseConverter


class SlackConverter(BaseConverter):
    def __init__(self) -> None:
        super().__init__()
        self._list_depth = 0
        self._ordered_index: list[int] = []

    def render_document(self, node: Document) -> str:
        return self.render_children(node)

    def render_heading(self, node: Heading) -> str:
        inner = self.render_children(node)
        return f"*{inner}*\n\n"

    def render_paragraph(self, node: Paragraph) -> str:
        inner = self.render_children(node)
        return f"{inner}\n\n"

    def render_text(self, node: Text) -> str:
        return _escape_slack(node.content)

    def render_bold(self, node: Bold) -> str:
        return f"*{self.render_children(node)}*"

    def render_italic(self, node: Italic) -> str:
        return f"_{self.render_children(node)}_"

    def render_strikethrough(self, node: Strikethrough) -> str:
        return f"~{self.render_children(node)}~"

    def render_code(self, node: Code) -> str:
        return f"`{node.content}`"

    def render_codeblock(self, node: CodeBlock) -> str:
        content = node.content
        if content.endswith("\n"):
            content = content[:-1]
        return f"```\n{content}\n```\n\n"

    def render_link(self, node: Link) -> str:
        inner = self.render_children(node)
        return f"<{node.url}|{inner}>"

    def render_image(self, node: Image) -> str:
        return f"<{node.url}>"

    def render_unorderedlist(self, node: UnorderedList) -> str:
        self._list_depth += 1
        result = self.render_children(node)
        self._list_depth -= 1
        return result

    def render_orderedlist(self, node: OrderedList) -> str:
        self._list_depth += 1
        self._ordered_index.append(node.start)
        result = self.render_children(node)
        self._ordered_index.pop()
        self._list_depth -= 1
        return result

    def render_listitem(self, node: ListItem) -> str:
        indent = "  " * (self._list_depth - 1)
        if self._ordered_index:
            idx = self._ordered_index[-1]
            prefix = f"{indent}{idx}. "
            self._ordered_index[-1] = idx + 1
        else:
            prefix = f"{indent}\u2022 "

        inner = self._render_listitem_content(node)
        return f"{prefix}{inner}\n"

    def _render_listitem_content(self, node: Node) -> str:
        parts = []
        for child in node.children:
            if isinstance(child, Paragraph):
                parts.append(self.render_children(child))
            elif isinstance(child, (UnorderedList, OrderedList)):
                parts.append("\n" + self.render_node(child).rstrip("\n"))
            else:
                parts.append(self.render_node(child))
        return "".join(parts).strip()

    def render_table(self, node: Table) -> str:
        all_rows: list[list[str]] = []
        if node.headers:
            all_rows.append([self.render_children(h).strip() for h in node.headers])
        for row in node.rows:
            all_rows.append([self.render_children(c).strip() for c in row])

        if not all_rows:
            return ""

        col_widths = [0] * len(all_rows[0])
        for row in all_rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(cell))

        lines = []
        for row in all_rows:
            cells = []
            for i, cell in enumerate(row):
                width = col_widths[i] if i < len(col_widths) else len(cell)
                cells.append(cell.ljust(width))
            lines.append("  ".join(cells))

        return "```\n" + "\n".join(lines) + "\n```\n\n"

    def render_blockquote(self, node: Blockquote) -> str:
        inner = self.render_children(node).strip()
        lines = inner.split("\n")
        quoted = "\n".join(f"&gt; {line}" for line in lines)
        return quoted + "\n\n"

    def render_horizontalrule(self, node: HorizontalRule) -> str:
        return "---\n"

    def render_linebreak(self, node: LineBreak) -> str:
        return "\n"

    def render_softbreak(self, node: SoftBreak) -> str:
        return "\n"


def _escape_slack(text: str) -> str:
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text
