"""Tokens for the interpreter."""

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
    ENTER_LOOP = "["
    EXIT_LOOP = "]"

    @classmethod
    def from_character(cls: type[Self], character: str) -> Self | None:
        """Get the token from a string."""
        try:
            return cls(character)
        except ValueError:
            return None
