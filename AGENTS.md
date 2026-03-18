# AGENTS.md

## Project Overview

MarkdownBridge is a Python library and CLI tool that converts Markdown to platform-specific markup formats (Confluence, Confluence ADF, Jira, Slack, Microsoft Teams) with reverse conversion support (Jira-to-Markdown).

## Tech Stack

- **Language:** Python 3.10+ (uses `from __future__ import annotations`, `X | None` union syntax)
- **Build system:** Hatchling (`pyproject.toml`)
- **Runtime deps:** `markdown-it-py`, `click`
- **Dev deps:** `pytest`, `pytest-cov`

## Commands

```bash
# Install for development
pip install -e .

# Run tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=markdownbridge

# CLI usage
markdownbridge convert --to <format> [--output FILE] [FILE]
markdownbridge formats
```

## Architecture

- **Parser** (`parser.py`): Converts `markdown-it-py` tokens into a dataclass AST (18 node types in `ast_nodes.py`)
- **Registry** (`registry.py`): Plugin pattern — converters self-register via `registry.register()`
- **Converters** (`converters/`): Each extends `BaseConverter` using a visitor pattern (`render_node()` dispatches to `render_<NodeType>()` methods)
- **Reverse converters** (`reverse/`): Platform-specific markup back to Markdown
- **CLI** (`cli.py`): Click-based CLI wrapping the `MarkdownBridge` facade (`__init__.py`)
- **Facade** (`__init__.py`): `MarkdownBridge` class provides the public Python API (`to_jira()`, `to_slack()`, `to_confluence()`, `to_teams()`, `convert()`, `from_jira()`)

## Code Conventions

- All source files use `from __future__ import annotations`
- Use Python dataclasses for AST nodes
- Converter methods follow `render_<NodeType>` naming convention
- Tests use `pytest` with shared fixtures in `conftest.py`
- No linter/formatter is currently configured — follow existing code style when editing
