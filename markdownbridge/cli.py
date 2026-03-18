from __future__ import annotations

import sys

import click

from .parser import parse
from .registry import get_converter, list_converters
from .reverse.jira_to_md import jira_to_markdown


@click.group()
def main() -> None:
    """Convert Markdown to platform-specific formats."""


@main.command()
@click.option(
    "--to",
    "target",
    required=True,
    type=click.Choice(
        ["confluence", "confluence-adf", "jira", "slack", "teams"]
    ),
)
@click.option("--output", default=None, type=click.Path())
@click.option(
    "--from",
    "source_format",
    default=None,
    help="Source format for reverse conversion",
)
@click.argument("file", required=False, type=click.Path(exists=True))
def convert(
    target: str,
    output: str | None,
    source_format: str | None,
    file: str | None,
) -> None:
    """Convert a Markdown file to the target format."""
    if file:
        with open(file) as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    if source_format == "jira":
        result = jira_to_markdown(content)
    else:
        doc = parse(content)
        converter = get_converter(target)
        result = converter.convert(doc)

    if output:
        with open(output, "w") as f:
            f.write(result)
        click.echo(f"Written to {output}")
    else:
        click.echo(result)


@main.command()
def formats() -> None:
    """List available conversion formats."""
    for name in list_converters():
        click.echo(name)
