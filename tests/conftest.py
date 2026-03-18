import pytest


SAMPLE_MARKDOWN = """\
# Hello World

This is a **bold** and *italic* paragraph with `inline code`.

## Code Block

```python
def hello():
    print("world")
```

## Links and Images

[Click here](https://example.com)

![Alt text](https://example.com/image.png)

## Lists

- Item 1
- Item 2
  - Nested item

1. First
2. Second

## Table

| Name | Age |
|------|-----|
| Alice | 30 |
| Bob | 25 |

> This is a blockquote

---

~~strikethrough text~~
"""


@pytest.fixture
def sample_markdown():
    return SAMPLE_MARKDOWN


@pytest.fixture
def simple_heading():
    return "# Hello\n"


@pytest.fixture
def simple_bold():
    return "**bold text**\n"


@pytest.fixture
def simple_italic():
    return "*italic text*\n"


@pytest.fixture
def simple_code():
    return "`code`\n"


@pytest.fixture
def simple_link():
    return "[Click](https://example.com)\n"


@pytest.fixture
def simple_image():
    return "![Alt](https://example.com/img.png)\n"
