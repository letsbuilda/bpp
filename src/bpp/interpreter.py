"""The interpreter."""

import sys
from collections.abc import Sequence
from enum import Enum, auto
from typing import NoReturn, Self

from .exceptions import BrainfuckSyntaxError
from .tokens import Token, tokenize


class ResultState(Enum):
    """Possible interpreter states after handling a token."""

    SUCCESS = auto()
    JUMP_FORWARD = auto()
    JUMP_BACKWARD = auto()


def validate_syntax(syntax: Sequence[Sequence[Token]]) -> None | NoReturn:
    """Validate the given syntax."""
    in_loop = False
    loop_started_at_line = 0
    loop_started_at_character = 0
    for line_index, line in enumerate(syntax):
        for character_index, token in enumerate(line):
            if token == Token.ENTER_LOOP:
                in_loop = True
                loop_started_at_line = line_index
                loop_started_at_character = character_index
            if token == Token.EXIT_LOOP:
                if not in_loop:
                    msg = (
                        "Syntax error: Unexpected closing bracket in line "
                        f"{loop_started_at_line + 1} at char {loop_started_at_character + 1}!"
                    )
                    raise BrainfuckSyntaxError(msg)
                in_loop = False
    if in_loop:
        msg = (
            "Syntax error: Unclosed bracket in line "
            f"{loop_started_at_line + 1} at char {loop_started_at_character + 1}!"
        )
        raise BrainfuckSyntaxError(msg)
    return None


class Interpreter:
    """The interpreter for the language."""

    def __init__(self: Self, byte_min: int = 0, byte_max: int = 255) -> None:
        self.memory: dict[int, int] = {}
        self.current_position = 0
        self.byte_min = byte_min
        self.byte_max = byte_max

    def increment_pointer(self: Self) -> None:
        """Increment the pointer."""
        self.current_position += 1

    def decrement_pointer(self: Self) -> None:
        """Decrement the pointer."""
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
        print(chr(self.memory[self.current_position]), end="")  # noqa: T201

    def get_input(self: Self) -> None:
        """Output the ASCII value of the byte at the current position."""
        self.memory[self.current_position] = ord(sys.stdin.read(1))

    def handle_token(self: Self, token: Token) -> ResultState:
        """Handle a single token."""
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
            case Token.ENTER_LOOP:
                if self.memory[self.current_position] != 0:
                    return ResultState.JUMP_FORWARD
            case Token.EXIT_LOOP:
                if self.memory[self.current_position] != 0:
                    return ResultState.JUMP_BACKWARD
        return ResultState.SUCCESS

    def run(self: Self, code: str) -> None:
        """Run code."""
        syntax = [tokenize(line) for line in code.split("\n")]
        validate_syntax(syntax)
        tokens = [token for line in syntax for token in line]

        last_loop_start = 0
        for index in range(len(tokens)):
            token = tokens[index]
            if token == Token.ENTER_LOOP:
                last_loop_start = index
            match self.handle_token(token):
                case ResultState.SUCCESS:
                    continue
                case ResultState.JUMP_BACKWARD:
                    index = last_loop_start  # noqa: PLW2901 - That's the point of this line
                case ResultState.JUMP_FORWARD:
                    for i in range(index, len(tokens)):
                        if tokens[i] == Token.EXIT_LOOP and i > index:
                            index = i  # noqa: PLW2901 - That's the point of this line
                            break
