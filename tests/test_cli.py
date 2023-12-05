"""Test the CLI."""

from runpy import run_module

from bpp.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def test_app() -> None:
    """Initial test for the CLI."""
    result = runner.invoke(app, ["run", r"./examples/hello-world.bf"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout


def test_dash_m() -> None:
    """`python -m bpp` works."""
    output_globals = run_module("bpp")
    assert all(global_.startswith("__") or global_ == "app" for global_ in output_globals)
