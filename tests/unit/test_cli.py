"""Basic CLI smoke tests."""

from typer.testing import CliRunner
from openeraseme.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "OpenEraseMe" in result.stdout


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "openeraseme" in result.stdout
