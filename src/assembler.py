"""Ассемблер учебной виртуальной машины."""

import argparse
import json
import sys
from pathlib import Path

from src.instructions import INSTRUCTION_SET

MIN_OPERAND_VALUE = 0
FIELD_NAMES = "ABCD"

def parse_args():
    """Разобрать аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Ассемблер учебной виртуальной машины"
    )

    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--test-mode", action="store_true")

    return parser.parse_args()

def read_program(path):
    """Прочитать исходную программу из JSON-файла."""
    with path.open("r", encoding="utf-8") as file:
        program = json.load(file)

    if not isinstance(program, list):
        raise ValueError("Программа должна быть JSON-массивом")

    return program

def validate_operand(name, value, bits):
    """Проверить тип и допустимый диапазон операнда."""
    if type(value) is not int:
        raise ValueError(f"Операнд {name} должен быть целым числом")

    max_value = (1 << bits) - 1

    if not MIN_OPERAND_VALUE <= value <= max_value:
        raise ValueError(
            f"Операнд {name} должен быть в диапазоне "
            f"от {MIN_OPERAND_VALUE} до {max_value}"
        )

def translate_instruction(instruction):
    """Преобразовать команду в промежуточное представление."""
    if not isinstance(instruction, dict):
        raise ValueError("Команда должна быть JSON-объектом")

    name = instruction.get("op")

    if not isinstance(name, str) or name not in INSTRUCTION_SET:
        raise ValueError(f"Неизвестная команда: {name}")

    specification = INSTRUCTION_SET[name]
    result = [specification["opcode"]]

    for operand_name, bits in specification["operands"]:
        if operand_name not in instruction:
            raise ValueError(f"Отсутствует операнд {operand_name}")

        value = instruction[operand_name]
        validate_operand(operand_name, value, bits)
        result.append(value)

    return tuple(result)

def translate_program(program):
    """Преобразовать все команды программы."""
    return [
        translate_instruction(instruction)
        for instruction in program
    ]

def print_test_result(program):
    """Вывести поля команд и их значения."""
    for instruction in program:
        fields = [
            f"{name}={value}"
            for name, value in zip(FIELD_NAMES, instruction)
        ]

        print(", ".join(fields))

def main():
    """Выполнить ассемблирование исходной программы."""
    args = parse_args()

    try:
        program = read_program(args.input)
        translated = translate_program(program)

        if args.test_mode:
            print_test_result(translated)

    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())