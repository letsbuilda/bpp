"""Test the CLI."""

from typer.testing import CliRunner

from bpp.cli import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["run", r".\examples\hello-world.bf"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout
