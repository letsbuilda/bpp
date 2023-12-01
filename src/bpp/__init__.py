import sys


class Symbol:
    ENTER_LOOP = "["
    EXIT_LOOP = "]"
    INC = "+"
    DEC = "-"
    MOVRIGHT = ">"
    MOVLEFT = "<"
    OUT = "."
    IN = ","


def strip(code: str) -> list:
    output = []
    for symbol in code:
        if symbol in "[]+-<>.,":
            output.append(symbol)

    return output


def verify(code: list) -> bool:
    stack = []

    for symbol in code:
        if symbol == Symbol.ENTER_LOOP:
            stack.append(symbol)
        elif symbol == Symbol.EXIT_LOOP:
            if len(stack) == 0:
                return False

            if stack.pop() != Symbol.ENTER_LOOP:
                return False

    return len(stack) == 0


def run(code: str) -> bool:
    code = strip(code)

    if not verify(code):
        print("Segmentation fault")
        return False

    pointer = 0
    code_pointer = 0

    loop_stack = []
    memory = [0] * 30000

    while code_pointer < len(code):
        symbol = code[code_pointer]

        if symbol == Symbol.ENTER_LOOP:
            if memory[pointer] != 0:
                loop_stack.append(code_pointer + 1)
            else:
                while code[code_pointer] != Symbol.EXIT_LOOP:
                    code_pointer += 1
        elif symbol == Symbol.EXIT_LOOP:
            if memory[pointer] == 0:
                if len(loop_stack) != 0:
                    loop_stack.pop()
            else:
                while code[code_pointer] != Symbol.ENTER_LOOP:
                    code_pointer -= 1

        elif symbol == Symbol.INC:
            memory[pointer] += 1
        elif symbol == Symbol.DEC:
            memory[pointer] -= 1

        elif symbol == Symbol.MOVLEFT:
            pointer -= 1
        elif symbol == Symbol.MOVRIGHT:
            pointer += 1

        elif symbol == Symbol.OUT:
            print(chr(memory[pointer]), end="")
        elif symbol == Symbol.IN:
            memory[pointer] = ord(sys.stdin.read(1))

        code_pointer += 1
    return None
