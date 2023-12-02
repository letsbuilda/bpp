"""Tests for the interpreter."""

from io import StringIO

import pytest
from bpp import BrainfuckSyntaxError, Interpreter

ASCII_LOWERCASE_A = 97


def test_increment_pointer() -> None:
    """Test increment pointer."""
    interpreter = Interpreter()
    interpreter.increment_pointer()
    assert interpreter.current_position == 1


def test_pointer_doesnt_go_negative() -> None:
    """Make sure that the pointer can't become a negative number."""
    interpreter = Interpreter()
    with pytest.raises(BrainfuckSyntaxError):
        interpreter.decrement_pointer()


def test_byte_overflows() -> None:
    """Make sure that byte overflows."""
    interpreter = Interpreter()
    for _ in range(256):
        interpreter.increment_byte_at_current_pointer()
    assert interpreter.memory[interpreter.current_position] == interpreter.byte_min


def test_byte_underflows() -> None:
    """Make sure that byte underflows."""
    interpreter = Interpreter()
    interpreter.decrement_byte_at_current_pointer()
    assert interpreter.memory[interpreter.current_position] == interpreter.byte_max


def test_can_output_letter(capsys) -> None:  # noqa: ANN001 -- pytest builtin fixture
    """Output the ASCII value of byte at the current position, make sure that there is no newline."""
    interpreter = Interpreter()
    for _ in range(97):
        interpreter.increment_byte_at_current_pointer()
    interpreter.output_current_byte()
    interpreter.output_current_byte()
    captured = capsys.readouterr()
    assert captured.out == "aa"


def test_can_input_letter(monkeypatch) -> None:  # noqa: ANN001 -- pytest builtin fixture
    """Input an ASCII character."""
    interpreter = Interpreter()
    monkeypatch.setattr("sys.stdin", StringIO("a"))
    interpreter.get_input()
    assert interpreter.memory[interpreter.current_position] == ASCII_LOWERCASE_A


@pytest.mark.parametrize(
    ("code", "error_message"),
    [
        ("[", "Syntax error: Unclosed bracket in line 1 at char 1!"),
        ("]", "Syntax error: Unexpected closing bracket in line 1 at char 1!"),
    ],
)
def test_invalid_syntax_fails(code: str, error_message: str) -> None:
    """Make sure that invalid syntax fails."""
    interpreter = Interpreter()
    with pytest.raises(BrainfuckSyntaxError, match=error_message):
        interpreter.run(code)
