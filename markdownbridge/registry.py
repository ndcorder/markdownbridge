from __future__ import annotations

from .converters.base import BaseConverter

_converters: dict[str, type[BaseConverter]] = {}


def register(name: str, converter_class: type[BaseConverter]) -> None:
    _converters[name] = converter_class


def get_converter(name: str) -> BaseConverter:
    if name not in _converters:
        raise ValueError(
            f"Unknown converter: {name}. Available: {list_converters()}"
        )
    return _converters[name]()


def list_converters() -> list[str]:
    return sorted(_converters.keys())


def _register_builtins() -> None:
    from .converters.confluence import ConfluenceConverter
    from .converters.confluence_adf import ConfluenceADFConverter
    from .converters.jira import JiraConverter
    from .converters.slack import SlackConverter
    from .converters.teams import TeamsConverter

    register("confluence", ConfluenceConverter)
    register("confluence-adf", ConfluenceADFConverter)
    register("jira", JiraConverter)
    register("slack", SlackConverter)
    register("teams", TeamsConverter)


_register_builtins()
