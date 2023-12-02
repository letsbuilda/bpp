"""Test the tokenizer."""

import pytest
from bpp import Token, tokenize


@pytest.mark.parametrize(
    ("code", "tokens"),
    [
        ("", []),
        ("><", [Token.INCREMENT_POINTER, Token.DECREMENT_POINTER]),
        (">hi I'm a comment!!<", [Token.INCREMENT_POINTER, Token.DECREMENT_POINTER]),
        ("[><]", [Token.LOOP_START, Token.INCREMENT_POINTER, Token.DECREMENT_POINTER, Token.LOOP_END]),
    ],
)
def test_invalid_syntax_fails(code: str, tokens: list[Token]) -> None:
    """Make sure that invalid syntax fails."""
    assert tokenize(code) == tokens
