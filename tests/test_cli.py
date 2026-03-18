import tempfile
import os

from click.testing import CliRunner

from markdownbridge.cli import main


def test_convert_jira_from_file():
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False
    ) as f:
        f.write("# Hello\n")
        f.flush()
        result = runner.invoke(main, ["convert", "--to", "jira", f.name])
    os.unlink(f.name)
    assert result.exit_code == 0
    assert "h1. Hello" in result.output


def test_convert_slack_from_stdin():
    runner = CliRunner()
    result = runner.invoke(
        main, ["convert", "--to", "slack"], input="**bold**\n"
    )
    assert result.exit_code == 0
    assert "*bold*" in result.output


def test_convert_confluence_to_output_file():
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False
    ) as src:
        src.write("# Test\n")
        src.flush()
        with tempfile.NamedTemporaryFile(
            suffix=".html", delete=False
        ) as dst:
            dst_path = dst.name

        result = runner.invoke(
            main,
            ["convert", "--to", "confluence", "--output", dst_path, src.name],
        )
    os.unlink(src.name)
    assert result.exit_code == 0
    assert "Written to" in result.output

    with open(dst_path) as f:
        content = f.read()
    os.unlink(dst_path)
    assert "<h1>Test</h1>" in content


def test_formats_command():
    runner = CliRunner()
    result = runner.invoke(main, ["formats"])
    assert result.exit_code == 0
    assert "confluence" in result.output
    assert "jira" in result.output
    assert "slack" in result.output
    assert "teams" in result.output


def test_convert_teams():
    runner = CliRunner()
    result = runner.invoke(
        main, ["convert", "--to", "teams"], input="# Hello\n"
    )
    assert result.exit_code == 0
    assert "AdaptiveCard" in result.output
