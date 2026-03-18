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

_SIZE_MAP = {1: "ExtraLarge", 2: "Large", 3: "Medium"}


class TeamsConverter(BaseConverter):
    def convert(self, document: Document) -> str:
        card = {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.5",
            "body": self._render_body(document),
        }
        return json.dumps(card, indent=2)

    def _render_body(self, node: Node) -> list[dict]:
        elements: list[dict] = []
        for child in node.children:
            rendered = self._render_element(child)
            if rendered is not None:
                elements.append(rendered)
        return elements

    def _render_element(self, node: Node) -> dict | None:
        if isinstance(node, Heading):
            text = self._render_inline_text(node)
            size = _SIZE_MAP.get(node.level, "Default")
            return {
                "type": "TextBlock",
                "text": text,
                "size": size,
                "weight": "Bolder",
                "wrap": True,
            }
        elif isinstance(node, Paragraph):
            text = self._render_inline_text(node)
            return {"type": "TextBlock", "text": text, "wrap": True}
        elif isinstance(node, CodeBlock):
            content = node.content
            if content.endswith("\n"):
                content = content[:-1]
            return {
                "type": "TextBlock",
                "text": content,
                "fontType": "Monospace",
                "wrap": True,
            }
        elif isinstance(node, Image):
            result: dict = {"type": "Image", "url": node.url}
            if node.alt:
                result["altText"] = node.alt
            return result
        elif isinstance(node, UnorderedList):
            items = []
            for child in node.children:
                if isinstance(child, ListItem):
                    text = self._render_listitem_text(child)
                    items.append(f"- {text}")
            return {
                "type": "TextBlock",
                "text": "\n".join(items),
                "wrap": True,
            }
        elif isinstance(node, OrderedList):
            items = []
            idx = node.start
            for child in node.children:
                if isinstance(child, ListItem):
                    text = self._render_listitem_text(child)
                    items.append(f"{idx}. {text}")
                    idx += 1
            return {
                "type": "TextBlock",
                "text": "\n".join(items),
                "wrap": True,
            }
        elif isinstance(node, Table):
            return self._render_table(node)
        elif isinstance(node, Blockquote):
            inner_parts = []
            for child in node.children:
                if isinstance(child, Paragraph):
                    inner_parts.append(self._render_inline_text(child))
                else:
                    inner_parts.append(self._render_inline_text(child))
            text = "\n".join(inner_parts)
            return {"type": "TextBlock", "text": text, "wrap": True}
        elif isinstance(node, HorizontalRule):
            return {"type": "TextBlock", "text": "---", "separator": True}
        return None

    def _render_inline_text(self, node: Node) -> str:
        parts: list[str] = []
        for child in node.children:
            parts.append(self._inline_to_text(child))
        return "".join(parts)

    def _inline_to_text(self, node: Node) -> str:
        if isinstance(node, Text):
            return node.content
        elif isinstance(node, Bold):
            inner = "".join(self._inline_to_text(c) for c in node.children)
            return f"**{inner}**"
        elif isinstance(node, Italic):
            inner = "".join(self._inline_to_text(c) for c in node.children)
            return f"_{inner}_"
        elif isinstance(node, Strikethrough):
            inner = "".join(self._inline_to_text(c) for c in node.children)
            return f"~~{inner}~~"
        elif isinstance(node, Code):
            return f"`{node.content}`"
        elif isinstance(node, Link):
            inner = "".join(self._inline_to_text(c) for c in node.children)
            return f"[{inner}]({node.url})"
        elif isinstance(node, Image):
            return f"![{node.alt}]({node.url})"
        elif isinstance(node, LineBreak):
            return "\n"
        elif isinstance(node, SoftBreak):
            return " "
        return ""

    def _render_listitem_text(self, node: Node) -> str:
        parts = []
        for child in node.children:
            if isinstance(child, Paragraph):
                parts.append(self._render_inline_text(child))
            else:
                parts.append(self._render_inline_text(child))
        return " ".join(parts).strip()

    def _render_table(self, node: Table) -> dict:
        num_cols = 0
        if node.headers:
            num_cols = len(node.headers)
        elif node.rows:
            num_cols = len(node.rows[0])

        columns = [{"width": 1} for _ in range(num_cols)]

        rows = []
        if node.headers:
            cells = []
            for h in node.headers:
                text = self._render_inline_text(h)
                cells.append(
                    {
                        "type": "TableCell",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": text,
                                "weight": "Bolder",
                                "wrap": True,
                            }
                        ],
                    }
                )
            rows.append({"type": "TableRow", "cells": cells})

        for row in node.rows:
            cells = []
            for c in row:
                text = self._render_inline_text(c)
                cells.append(
                    {
                        "type": "TableCell",
                        "items": [
                            {"type": "TextBlock", "text": text, "wrap": True}
                        ],
                    }
                )
            rows.append({"type": "TableRow", "cells": cells})

        return {"type": "Table", "columns": columns, "rows": rows}
