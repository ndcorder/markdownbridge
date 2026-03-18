from __future__ import annotations

from .parser import parse
from .registry import get_converter

__version__ = "0.1.0"


class MarkdownBridge:
    @staticmethod
    def to_confluence(md: str) -> str:
        doc = parse(md)
        return get_converter("confluence").convert(doc)

    @staticmethod
    def to_confluence_adf(md: str) -> str:
        doc = parse(md)
        return get_converter("confluence-adf").convert(doc)

    @staticmethod
    def to_jira(md: str) -> str:
        doc = parse(md)
        return get_converter("jira").convert(doc)

    @staticmethod
    def to_slack(md: str) -> str:
        doc = parse(md)
        return get_converter("slack").convert(doc)

    @staticmethod
    def to_teams(md: str) -> str:
        doc = parse(md)
        return get_converter("teams").convert(doc)

    @staticmethod
    def convert(md: str, target: str) -> str:
        doc = parse(md)
        return get_converter(target).convert(doc)

    @staticmethod
    def from_jira(jira_markup: str) -> str:
        from .reverse.jira_to_md import jira_to_markdown

        return jira_to_markdown(jira_markup)
