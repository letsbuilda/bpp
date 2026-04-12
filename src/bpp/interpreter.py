"""The interpreter."""

import sys
from enum import Enum, auto
from io import StringIO
from typing import TYPE_CHECKING, Self

from .exceptions import BrainfuckSyntaxError
from .tokens import Token, tokenize

if TYPE_CHECKING:
    from collections.abc import Sequence


class ResultState(Enum):
    """Possible interpreter states after handling a token."""

    SUCCESS = auto()
    JUMP_FORWARD = auto()
    JUMP_BACKWARD = auto()


def validate_syntax(syntax: Sequence[Sequence[Token]]) -> None:
    """Validate the given syntax.

    Raises
    ------
    BrainfuckSyntaxError
        If the syntax is invalid.
    """
    depth = 0
    loop_started_at_line = 0
    loop_started_at_character = 0
    for line_index, line in enumerate(syntax):
        for character_index, token in enumerate(line):
            if token == Token.LOOP_START:
                loop_started_at_line = line_index
                loop_started_at_character = character_index
                depth += 1
            if token == Token.LOOP_END:
                if depth == 0:
                    msg = (
                        "Syntax error: Unexpected closing bracket in line "
                        f"{line_index + 1} at char {character_index + 1}!"
                    )
                    raise BrainfuckSyntaxError(msg)
                depth -= 1
    if depth > 0:
        msg = (
            "Syntax error: Unclosed bracket in line "
            f"{loop_started_at_line + 1} at char {loop_started_at_character + 1}!"
        )
        raise BrainfuckSyntaxError(msg)


class Interpreter:
    """The interpreter for the language."""

    def __init__(self: Self, byte_min: int = 0, byte_max: int = 255) -> None:
        self.current_index = 0
        self.memory: dict[int, int] = {0: 0}
        self.current_position = 0
        self.byte_min = byte_min
        self.byte_max = byte_max
        self.output = StringIO()

    def increment_pointer(self: Self) -> None:
        """Increment the pointer."""
        self.current_position += 1

    def decrement_pointer(self: Self) -> None:
        """Decrement the pointer.

        Raises
        ------
        BrainfuckSyntaxError
            If the pointer goes negative.
        """
        if self.current_position == 0:
            msg = "Pointer can't be negative!"
            raise BrainfuckSyntaxError(msg)
        self.current_position -= 1

    def increment_byte_at_current_pointer(self: Self) -> None:
        """Increment the byte at the current position."""
        if self.current_position not in self.memory:
            self.memory[self.current_position] = 0
        self.memory[self.current_position] += 1
        if self.memory[self.current_position] > self.byte_max:
            self.memory[self.current_position] = self.byte_min

    def decrement_byte_at_current_pointer(self: Self) -> None:
        """Decrement the byte at the current position."""
        if self.current_position not in self.memory:
            self.memory[self.current_position] = 0
        self.memory[self.current_position] -= 1
        if self.memory[self.current_position] < self.byte_min:
            self.memory[self.current_position] = self.byte_max

    def output_current_byte(self: Self) -> None:
        """Output the ASCII value of the byte at the current position."""
        self.output.write(chr(self.memory.get(self.current_position, 0)))

    def get_input(self: Self) -> None:
        """Output the ASCII value of the byte at the current position."""
        self.memory[self.current_position] = ord(sys.stdin.read(1))

    def handle_token(self: Self, token: Token) -> ResultState:  # noqa: C901
        """Handle a single token.

        Returns
        -------
        The state of the interpreter after handling the token
        """
        match token:
            case Token.INCREMENT_POINTER:
                self.increment_pointer()
            case Token.DECREMENT_POINTER:
                self.decrement_pointer()
            case Token.INCREMENT_BYTE:
                self.increment_byte_at_current_pointer()
            case Token.DECREMENT_BYTE:
                self.decrement_byte_at_current_pointer()
            case Token.OUTPUT_BYTE:
                self.output_current_byte()
            case Token.INPUT_BYTE:
                self.get_input()
            case Token.LOOP_START:
                if self.memory.get(self.current_position, 0) == 0:
                    return ResultState.JUMP_FORWARD
            case Token.LOOP_END:
                if self.memory.get(self.current_position, 0) != 0:
                    return ResultState.JUMP_BACKWARD
        return ResultState.SUCCESS

    def run(self: Self, code: str) -> str:
        """Run code.

        Returns
        -------
        The output of the code.
        """
        syntax = [tokenize(line) for line in code.split("\n")]
        validate_syntax(syntax)
        tokens = [token for line in syntax for token in line]

        # Precompute matching bracket pairs to support nested loops.
        # validate_syntax guarantees brackets are balanced, so the stack is
        # always non-empty when a LOOP_END token is encountered here.
        bracket_map: dict[int, int] = {}
        stack: list[int] = []
        for i, token in enumerate(tokens):
            if token == Token.LOOP_START:
                stack.append(i)
            elif token == Token.LOOP_END:
                j = stack.pop()
                bracket_map[j] = i
                bracket_map[i] = j

        while True:
            token = tokens[self.current_index]
            match self.handle_token(token):
                case ResultState.SUCCESS:
                    pass
                case ResultState.JUMP_BACKWARD:
                    self.current_index = bracket_map[self.current_index]
                case ResultState.JUMP_FORWARD:
                    self.current_index = bracket_map[self.current_index]

            self.current_index += 1
            if self.current_index >= len(tokens):
                break
        return self.output.getvalue()
