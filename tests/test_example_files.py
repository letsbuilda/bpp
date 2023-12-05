"""Can execute example files and return expected results."""

from io import StringIO
from pathlib import Path

import pytest
from bpp import Interpreter


@pytest.mark.parametrize(
    ("example_file", "expected_result"),
    [
        (Path("./examples/hello-world.bf"), "Hello, World!"),
        (Path("./examples/jump.bf"), ""),
        (Path("./examples/decrement_not_in_memory.bf"), ""),
    ],
)
def test_example_files(example_file: Path, expected_result: str) -> None:
    """Test example files."""
    source = example_file.read_text()
    interpreter = Interpreter()
    assert interpreter.run(source) == expected_result


def test_example_files_with_input(monkeypatch) -> None:  # noqa: ANN001 -- pytest builtin fixture
    """Test example files with input."""
    source = Path("./examples/echo.bf").read_text()
    monkeypatch.setattr("sys.stdin", StringIO("a"))
    interpreter = Interpreter()
    assert interpreter.run(source) == "a"
