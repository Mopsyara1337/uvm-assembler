"""Интерпретатор учебной виртуальной машины."""

from src.codec import (
    BYTE_ORDER,
    INSTRUCTION_SIZE,
    decode_instruction,
)
from src.instructions import REGISTER_BITS, INSTRUCTION_SET
from src.memory import Memory
import argparse
import sys
from pathlib import Path

REGISTER_COUNT = 1 << REGISTER_BITS


class Interpreter:
    """Модель процессора учебной виртуальной машины."""

    def __init__(self):
        """Инициализировать виртуальную машину."""
        self.memory = Memory()
        self.registers = [0] * REGISTER_COUNT
        self.pc = 0
        self.program_size = 0
        self.operations = {
            INSTRUCTION_SET["LOAD_CONST"]["opcode"]: self.execute_load_const,
            INSTRUCTION_SET["READ"]["opcode"]: self.execute_read,
            INSTRUCTION_SET["WRITE"]["opcode"]: self.execute_write,
        }

    def load_program(self, program):
        """Подготовить виртуальную машину к выполнению программы."""
        self.program_size = self.memory.load_program(program)
        self.registers = [0] * REGISTER_COUNT
        self.pc = 0

    def fetch_instruction(self):
        """Получить и декодировать текущую команду."""
        number = self.memory.read(self.pc)
        instruction = number.to_bytes(
            INSTRUCTION_SIZE, byteorder=BYTE_ORDER)

        return decode_instruction(instruction)

    def execute_load_const(self, register, value):
        """Загрузить константу в регистр."""
        self.registers[register] = value

    def execute_write(self, register, address):
        """Записать значение регистра в память."""
        self.memory.write(address, self.registers[register])

    def execute_read(self, base_register, target_register, offset):
        """Прочитать значение из памяти в регистр."""
        address = self.registers[base_register] + offset
        self.registers[target_register] = self.memory.read(address)

    def execute_instruction(self, instruction):
        """Выполнить декодированную команду."""
        opcode = instruction[0]
        operands = instruction[1:]
        operation = self.operations.get(opcode)

        if operation is None:
            raise ValueError(f"Неподдерживаемая операция: {opcode}")

        operation(*operands)

    def run(self):
        """Выполнить загруженную программу."""
        while self.pc < self.program_size:
            instruction = self.fetch_instruction()
            self.execute_instruction(instruction)
            self.pc += 1

def parse_args():
    """Разобрать аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Интерпретатор учебной виртуальной машины"
    )

    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--range", required=True, type=int, nargs=2
    )

    return parser.parse_args()

def main():
    """Выполнить программу на учебной виртуальной машине."""
    args = parse_args()

    try:
        program = args.input.read_bytes()
        interpreter = Interpreter()
        interpreter.load_program(program)
        interpreter.run()
        interpreter.memory.dump_memory(args.output, *args.range)

    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
