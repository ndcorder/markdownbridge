import pytest

from markdownbridge.registry import get_converter, list_converters, register
from markdownbridge.converters.base import BaseConverter


def test_get_confluence():
    c = get_converter("confluence")
    assert isinstance(c, BaseConverter)


def test_get_confluence_adf():
    c = get_converter("confluence-adf")
    assert isinstance(c, BaseConverter)


def test_get_jira():
    c = get_converter("jira")
    assert isinstance(c, BaseConverter)


def test_get_slack():
    c = get_converter("slack")
    assert isinstance(c, BaseConverter)


def test_get_teams():
    c = get_converter("teams")
    assert isinstance(c, BaseConverter)


def test_list_converters():
    names = list_converters()
    assert "confluence" in names
    assert "confluence-adf" in names
    assert "jira" in names
    assert "slack" in names
    assert "teams" in names


def test_unknown_converter():
    with pytest.raises(ValueError, match="Unknown converter"):
        get_converter("nonexistent")


def test_register_custom():
    class MyConverter(BaseConverter):
        pass

    register("custom", MyConverter)
    c = get_converter("custom")
    assert isinstance(c, MyConverter)
