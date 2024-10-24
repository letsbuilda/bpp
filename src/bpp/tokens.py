"""Tokens for the interpreter."""

from collections.abc import Sequence
from enum import Enum
from typing import Self


class Token(Enum):
    """Tokens for the interpreter."""

    INCREMENT_POINTER = ">"
    DECREMENT_POINTER = "<"
    INCREMENT_BYTE = "+"
    DECREMENT_BYTE = "-"
    OUTPUT_BYTE = "."
    INPUT_BYTE = ","
    LOOP_START = "["
    LOOP_END = "]"

    @classmethod
    def from_character(cls: type[Self], character: str) -> Self | None:
        """Get the token from a string.

        Returns
        -------
        The token or None if the character is not a token.
        """
        try:
            return cls(character)
        except ValueError:
            return None


def tokenize(code: str) -> Sequence[Token]:
    """Convert text to tokens.

    Returns
    -------
    A sequence of tokens.
    """
    tokens = []
    for character in code:
        token = Token.from_character(character)
        if token is None:
            continue
        tokens.append(token)
    return tokens
