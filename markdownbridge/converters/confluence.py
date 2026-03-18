from __future__ import annotations

import html

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
    OrderedList,
    Paragraph,
    SoftBreak,
    Strikethrough,
    Table,
    Text,
    UnorderedList,
)
from .base import BaseConverter


class ConfluenceConverter(BaseConverter):
    def render_document(self, node: Document) -> str:
        return self.render_children(node)

    def render_heading(self, node: Heading) -> str:
        inner = self.render_children(node)
        return f"<h{node.level}>{inner}</h{node.level}>"

    def render_paragraph(self, node: Paragraph) -> str:
        inner = self.render_children(node)
        return f"<p>{inner}</p>"

    def render_text(self, node: Text) -> str:
        return html.escape(node.content)

    def render_bold(self, node: Bold) -> str:
        return f"<strong>{self.render_children(node)}</strong>"

    def render_italic(self, node: Italic) -> str:
        return f"<em>{self.render_children(node)}</em>"

    def render_strikethrough(self, node: Strikethrough) -> str:
        inner = self.render_children(node)
        return f'<span style="text-decoration: line-through;">{inner}</span>'

    def render_code(self, node: Code) -> str:
        return f"<code>{html.escape(node.content)}</code>"

    def render_codeblock(self, node: CodeBlock) -> str:
        lang_param = ""
        if node.language:
            lang_param = (
                f'<ac:parameter ac:name="language">{node.language}</ac:parameter>'
            )
        content = node.content
        if content.endswith("\n"):
            content = content[:-1]
        return (
            f'<ac:structured-macro ac:name="code">'
            f"{lang_param}"
            f"<ac:plain-text-body><![CDATA[{content}]]></ac:plain-text-body>"
            f"</ac:structured-macro>"
        )

    def render_link(self, node: Link) -> str:
        inner = self.render_children(node)
        return f'<a href="{html.escape(node.url)}">{inner}</a>'

    def render_image(self, node: Image) -> str:
        return f'<ac:image><ri:url ri:value="{html.escape(node.url)}" /></ac:image>'

    def render_unorderedlist(self, node: UnorderedList) -> str:
        return f"<ul>{self.render_children(node)}</ul>"

    def render_orderedlist(self, node: OrderedList) -> str:
        return f"<ol>{self.render_children(node)}</ol>"

    def render_listitem(self, node: ListItem) -> str:
        return f"<li>{self.render_children(node)}</li>"

    def render_table(self, node: Table) -> str:
        rows = ""
        if node.headers:
            cells = "".join(
                f"<th>{self.render_children(h)}</th>" for h in node.headers
            )
            rows += f"<tr>{cells}</tr>"
        for row in node.rows:
            cells = "".join(f"<td>{self.render_children(c)}</td>" for c in row)
            rows += f"<tr>{cells}</tr>"
        return f"<table><tbody>{rows}</tbody></table>"

    def render_blockquote(self, node: Blockquote) -> str:
        return f"<blockquote>{self.render_children(node)}</blockquote>"

    def render_horizontalrule(self, node: HorizontalRule) -> str:
        return "<hr />"

    def render_linebreak(self, node: LineBreak) -> str:
        return "<br />"

    def render_softbreak(self, node: SoftBreak) -> str:
        return "\n"
