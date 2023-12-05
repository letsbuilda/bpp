"""Test the CLI."""

from bpp.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def test_app() -> None:
    """Initial test for the CLI."""
    result = runner.invoke(app, ["run", r"./examples/hello-world.bf"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout
