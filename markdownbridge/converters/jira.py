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


class JiraConverter(BaseConverter):
    def __init__(self) -> None:
        super().__init__()
        self._list_depth = 0
        self._list_type_stack: list[str] = []

    def render_document(self, node: Document) -> str:
        return self.render_children(node)

    def render_heading(self, node: Heading) -> str:
        inner = self.render_children(node)
        return f"h{node.level}. {inner}\n"

    def render_paragraph(self, node: Paragraph) -> str:
        inner = self.render_children(node)
        return f"{inner}\n\n"

    def render_text(self, node: Text) -> str:
        return node.content

    def render_bold(self, node: Bold) -> str:
        return f"*{self.render_children(node)}*"

    def render_italic(self, node: Italic) -> str:
        return f"_{self.render_children(node)}_"

    def render_strikethrough(self, node: Strikethrough) -> str:
        return f"-{self.render_children(node)}-"

    def render_code(self, node: Code) -> str:
        return f"{{{{{node.content}}}}}"

    def render_codeblock(self, node: CodeBlock) -> str:
        lang = node.language or ""
        content = node.content
        if content.endswith("\n"):
            content = content[:-1]
        if lang:
            return f"{{code:{lang}}}\n{content}\n{{code}}\n"
        return f"{{code}}\n{content}\n{{code}}\n"

    def render_link(self, node: Link) -> str:
        inner = self.render_children(node)
        return f"[{inner}|{node.url}]"

    def render_image(self, node: Image) -> str:
        return f"!{node.url}!"

    def render_unorderedlist(self, node: UnorderedList) -> str:
        self._list_depth += 1
        self._list_type_stack.append("*")
        result = self.render_children(node)
        self._list_type_stack.pop()
        self._list_depth -= 1
        return result

    def render_orderedlist(self, node: OrderedList) -> str:
        self._list_depth += 1
        self._list_type_stack.append("#")
        result = self.render_children(node)
        self._list_type_stack.pop()
        self._list_depth -= 1
        return result

    def render_listitem(self, node: ListItem) -> str:
        prefix = "".join(self._list_type_stack)
        inner = self._render_listitem_children(node)
        return f"{prefix} {inner}\n"

    def _render_listitem_children(self, node: Node) -> str:
        parts = []
        for child in node.children:
            if isinstance(child, Paragraph):
                parts.append(self.render_children(child))
            elif isinstance(child, (UnorderedList, OrderedList)):
                parts.append(self.render_node(child))
            else:
                parts.append(self.render_node(child))
        result = "".join(parts)
        return result.strip()

    def render_table(self, node: Table) -> str:
        lines = []
        if node.headers:
            header_cells = "||".join(
                self.render_children(h) for h in node.headers
            )
            lines.append(f"||{header_cells}||")
        for row in node.rows:
            row_cells = "|".join(self.render_children(c) for c in row)
            lines.append(f"|{row_cells}|")
        return "\n".join(lines) + "\n"

    def render_blockquote(self, node: Blockquote) -> str:
        inner = self.render_children(node).strip()
        return f"{{quote}}\n{inner}\n{{quote}}\n"

    def render_horizontalrule(self, node: HorizontalRule) -> str:
        return "----\n"

    def render_linebreak(self, node: LineBreak) -> str:
        return "\\\\"

    def render_softbreak(self, node: SoftBreak) -> str:
        return "\n"
