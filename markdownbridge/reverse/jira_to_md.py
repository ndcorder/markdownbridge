from __future__ import annotations

import re


def jira_to_markdown(text: str) -> str:
    lines = text.split("\n")
    result: list[str] = []
    i = 0
    in_code = False
    code_lang = ""
    code_lines: list[str] = []

    while i < len(lines):
        line = lines[i]

        # Code blocks
        code_start = re.match(r"\{code(?::(\w+))?\}", line)
        if code_start and not in_code:
            in_code = True
            code_lang = code_start.group(1) or ""
            code_lines = []
            i += 1
            continue

        if line.strip() == "{code}" and in_code:
            in_code = False
            result.append(f"```{code_lang}")
            result.extend(code_lines)
            result.append("```")
            result.append("")
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Quote blocks
        if line.strip() == "{quote}":
            i += 1
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip() != "{quote}":
                quote_lines.append(lines[i])
                i += 1
            for ql in quote_lines:
                result.append(f"> {ql}")
            result.append("")
            i += 1
            continue

        # Headings
        heading = re.match(r"^h([1-6])\.\s+(.*)", line)
        if heading:
            level = int(heading.group(1))
            text_content = heading.group(2)
            text_content = _convert_inline(text_content)
            result.append(f"{'#' * level} {text_content}")
            result.append("")
            i += 1
            continue

        # Horizontal rule
        if line.strip() == "----":
            result.append("---")
            result.append("")
            i += 1
            continue

        # Table header row
        if line.startswith("||"):
            headers = _parse_table_header(line)
            result.append("| " + " | ".join(headers) + " |")
            result.append("|" + "|".join("-" for _ in headers) + "|")
            i += 1
            continue

        # Table data row
        if line.startswith("|") and not line.startswith("||"):
            cells = _parse_table_row(line)
            result.append("| " + " | ".join(cells) + " |")
            i += 1
            continue

        # Unordered list
        list_match = re.match(r"^(\*+)\s+(.*)", line)
        if list_match:
            depth = len(list_match.group(1))
            content = _convert_inline(list_match.group(2))
            indent = "  " * (depth - 1)
            result.append(f"{indent}- {content}")
            i += 1
            continue

        # Ordered list
        olist_match = re.match(r"^(#+)\s+(.*)", line)
        if olist_match:
            depth = len(olist_match.group(1))
            content = _convert_inline(olist_match.group(2))
            indent = "  " * (depth - 1)
            result.append(f"{indent}1. {content}")
            i += 1
            continue

        # Regular line - convert inline formatting
        converted = _convert_inline(line)
        result.append(converted)
        i += 1

    return "\n".join(result).strip() + "\n"


def _convert_inline(text: str) -> str:
    # Inline code {{text}} -> `text`
    text = re.sub(r"\{\{(.+?)\}\}", r"`\1`", text)

    # Bold *text* -> **text** (but not inside words)
    text = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"**\1**", text)

    # Italic _text_ -> *text* (but not inside words)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"*\1*", text)

    # Strikethrough -text- -> ~~text~~
    text = re.sub(r"(?<!\w)-(.+?)-(?!\w)", r"~~\1~~", text)

    # Links [text|url] -> [text](url)
    text = re.sub(r"\[([^|]+?)\|([^\]]+?)\]", r"[\1](\2)", text)

    # Images !url! -> ![](url)
    text = re.sub(r"!([^!\s]+?)!", r"![](\1)", text)

    return text


def _parse_table_header(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("||"):
        line = line[2:]
    if line.endswith("||"):
        line = line[:-2]
    cells = line.split("||")
    return [_convert_inline(c.strip()) for c in cells]


def _parse_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells = line.split("|")
    return [_convert_inline(c.strip()) for c in cells]
