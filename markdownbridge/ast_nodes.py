from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    children: list[Node] = field(default_factory=list)


@dataclass
class Document(Node):
    pass


@dataclass
class Heading(Node):
    level: int = 1


@dataclass
class Paragraph(Node):
    pass


@dataclass
class Text(Node):
    content: str = ""


@dataclass
class Bold(Node):
    pass


@dataclass
class Italic(Node):
    pass


@dataclass
class Strikethrough(Node):
    pass


@dataclass
class Code(Node):
    content: str = ""


@dataclass
class CodeBlock(Node):
    content: str = ""
    language: str | None = None


@dataclass
class Link(Node):
    url: str = ""
    title: str | None = None


@dataclass
class Image(Node):
    url: str = ""
    alt: str = ""
    title: str | None = None


@dataclass
class UnorderedList(Node):
    pass


@dataclass
class OrderedList(Node):
    start: int = 1


@dataclass
class ListItem(Node):
    pass


@dataclass
class Table(Node):
    headers: list[Node] = field(default_factory=list)
    rows: list[list[Node]] = field(default_factory=list)


@dataclass
class Blockquote(Node):
    pass


@dataclass
class HorizontalRule(Node):
    pass


@dataclass
class LineBreak(Node):
    pass


@dataclass
class SoftBreak(Node):
    pass
