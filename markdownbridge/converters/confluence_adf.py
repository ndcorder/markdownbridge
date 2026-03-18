from __future__ import annotations

import json

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


class ConfluenceADFConverter(BaseConverter):
    def convert(self, document: Document) -> str:
        adf = {
            "version": 1,
            "type": "doc",
            "content": self._render_block_children(document),
        }
        return json.dumps(adf, indent=2)

    def _render_block_children(self, node: Node) -> list[dict]:
        result = []
        for child in node.children:
            rendered = self._render_block(child)
            if rendered is not None:
                result.append(rendered)
        return result

    def _render_block(self, node: Node) -> dict | None:
        if isinstance(node, Heading):
            return {
                "type": "heading",
                "attrs": {"level": node.level},
                "content": self._render_inline_children(node),
            }
        elif isinstance(node, Paragraph):
            content = self._render_inline_children(node)
            if content:
                return {"type": "paragraph", "content": content}
            return {"type": "paragraph"}
        elif isinstance(node, CodeBlock):
            result: dict = {"type": "codeBlock"}
            if node.language:
                result["attrs"] = {"language": node.language}
            content = node.content
            if content.endswith("\n"):
                content = content[:-1]
            result["content"] = [{"type": "text", "text": content}]
            return result
        elif isinstance(node, UnorderedList):
            return {
                "type": "bulletList",
                "content": [
                    self._render_list_item(c)
                    for c in node.children
                    if isinstance(c, ListItem)
                ],
            }
        elif isinstance(node, OrderedList):
            return {
                "type": "orderedList",
                "content": [
                    self._render_list_item(c)
                    for c in node.children
                    if isinstance(c, ListItem)
                ],
            }
        elif isinstance(node, Blockquote):
            return {
                "type": "blockquote",
                "content": self._render_block_children(node),
            }
        elif isinstance(node, HorizontalRule):
            return {"type": "rule"}
        elif isinstance(node, Table):
            return self._render_table(node)
        elif isinstance(node, Image):
            return {
                "type": "mediaSingle",
                "content": [
                    {
                        "type": "media",
                        "attrs": {"type": "external", "url": node.url},
                    }
                ],
            }
        elif isinstance(node, Text):
            return {"type": "paragraph", "content": [{"type": "text", "text": node.content}]}
        return None

    def _render_list_item(self, node: ListItem) -> dict:
        content = []
        for child in node.children:
            rendered = self._render_block(child)
            if rendered is not None:
                content.append(rendered)
        return {"type": "listItem", "content": content}

    def _render_inline_children(self, node: Node) -> list[dict]:
        result: list[dict] = []
        self._collect_inline(node.children, [], result)
        return result

    def _collect_inline(
        self, nodes: list[Node], marks: list[dict], result: list[dict]
    ) -> None:
        for node in nodes:
            if isinstance(node, Text):
                entry: dict = {"type": "text", "text": node.content}
                if marks:
                    entry["marks"] = list(marks)
                result.append(entry)
            elif isinstance(node, Code):
                entry = {"type": "text", "text": node.content}
                entry["marks"] = list(marks) + [{"type": "code"}]
                result.append(entry)
            elif isinstance(node, Bold):
                self._collect_inline(
                    node.children, marks + [{"type": "strong"}], result
                )
            elif isinstance(node, Italic):
                self._collect_inline(
                    node.children, marks + [{"type": "em"}], result
                )
            elif isinstance(node, Strikethrough):
                self._collect_inline(
                    node.children, marks + [{"type": "strike"}], result
                )
            elif isinstance(node, Link):
                link_mark = {"type": "link", "attrs": {"href": node.url}}
                self._collect_inline(
                    node.children, marks + [link_mark], result
                )
            elif isinstance(node, Image):
                # Images at inline level get promoted to block level in ADF
                # but we handle them as inline here for simplicity
                pass
            elif isinstance(node, LineBreak):
                result.append({"type": "hardBreak"})
            elif isinstance(node, SoftBreak):
                entry = {"type": "text", "text": " "}
                if marks:
                    entry["marks"] = list(marks)
                result.append(entry)

    def _render_table(self, node: Table) -> dict:
        rows = []
        if node.headers:
            cells = []
            for h in node.headers:
                cell_content = self._render_inline_children(h)
                cell: dict = {"type": "tableHeader"}
                if cell_content:
                    cell["content"] = [
                        {"type": "paragraph", "content": cell_content}
                    ]
                else:
                    cell["content"] = [{"type": "paragraph"}]
                cells.append(cell)
            rows.append({"type": "tableRow", "content": cells})

        for row in node.rows:
            cells = []
            for c in row:
                cell_content = self._render_inline_children(c)
                cell = {"type": "tableCell"}
                if cell_content:
                    cell["content"] = [
                        {"type": "paragraph", "content": cell_content}
                    ]
                else:
                    cell["content"] = [{"type": "paragraph"}]
                cells.append(cell)
            rows.append({"type": "tableRow", "content": cells})

        return {"type": "table", "content": rows}
