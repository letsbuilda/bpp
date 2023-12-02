"""Test execution chunks of code."""

from bpp import Interpreter

HELLO_WORLD = ">++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."  # noqa: E501


def test_hello_world(capsys) -> None:  # noqa: ANN001 -- pytest builtin fixture
    """Can parse a hello world program."""
    interpreter = Interpreter()
    interpreter.run(HELLO_WORLD)
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!"
