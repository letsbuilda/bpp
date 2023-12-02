"""Test the tokenizer."""

import pytest
from bpp import Token, tokenize


@pytest.mark.parametrize(
    ("code", "tokens"),
    [
        ("", []),
        ("><", [Token.INCREMENT_POINTER, Token.DECREMENT_POINTER]),
        ("[><]", [Token.ENTER_LOOP, Token.INCREMENT_POINTER, Token.DECREMENT_POINTER, Token.EXIT_LOOP]),
    ],
)
def test_invalid_syntax_fails(code: str, tokens: list[Token]) -> None:
    """Make sure that invalid syntax fails."""
    assert tokenize(code) == tokens
