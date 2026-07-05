"""Tokens for the interpreter."""

from enum import Enum
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from collections.abc import Sequence


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


def _tokenize_with_positions(code: str) -> Sequence[tuple[Token, int]]:
    """Convert text to (token, original_char_index) tuples.

    Returns
    -------
    A sequence of (token, original_char_index) tuples preserving the
    character's position in the original source string.
    """
    tokens = []
    for position, character in enumerate(code):
        token = Token.from_character(character)
        if token is None:
            continue
        tokens.append((token, position))
    return tokens
