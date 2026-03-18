from __future__ import annotations

from ..ast_nodes import Document, Node


class BaseConverter:
    def convert(self, document: Document) -> str:
        return self.render_node(document)

    def render_node(self, node: Node) -> str:
        method_name = f"render_{type(node).__name__.lower()}"
        method = getattr(self, method_name, self.render_default)
        return method(node)

    def render_children(self, node: Node) -> str:
        return "".join(self.render_node(child) for child in node.children)

    def render_default(self, node: Node) -> str:
        if hasattr(node, "children"):
            return self.render_children(node)
        return ""
