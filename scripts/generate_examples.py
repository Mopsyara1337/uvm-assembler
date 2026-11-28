"""Генерация тестовых программ сложения векторов."""

import json
from pathlib import Path

VECTOR_LENGTH = 7
FIRST_ADDRESS = 100
SECOND_ADDRESS = 200
RESULT_ADDRESS = 300

def generate_vector(values, start_address):
    """Сформировать команды записи вектора в память."""
    program = []
    for index, value in enumerate(values):
        load = {
            "op": "LOAD_CONST",
            "register": 0,
            "value": value,
        }
        program.append(load)
        write = {
            "op": "WRITE",
            "register": 0,
            "address": start_address + index,
        }
        program.append(write)

    return program

def generate_addition(length, first_address, second_address,
                      result_address):
    """Сформировать команды поэлементного сложения векторов."""
    program = [
        {"op": "LOAD_CONST",
         "register": 1,
         "value": first_address},
    ]

    for index in range(length):
        read = {
            "op": "READ",
            "base_register": 1,
            "target_register": 2,
            "offset": index,
        }
        program.append(read)
        load = {
            "op": "LOAD_CONST",
            "register": 3,
            "value": second_address + index,
        }
        program.append(load)
        add = {
            "op": "ADD",
            "address_register": 3,
            "target_register": 2,
        }
        program.append(add)
        write = {
            "op": "WRITE",
            "register": 2,
            "address": result_address + index,
        }
        program.append(write)

    return program

def generate_program(first, second):
    """Сформировать программу сложения двух векторов."""
    if len(first) != VECTOR_LENGTH or len(second) != VECTOR_LENGTH:
        raise ValueError("Длина векторов должна быть равна 7")

    program = generate_vector(first, FIRST_ADDRESS)
    program.extend(generate_vector(second, SECOND_ADDRESS))
    program.extend(generate_addition(
        VECTOR_LENGTH,
        FIRST_ADDRESS,
        SECOND_ADDRESS,
        RESULT_ADDRESS,
    ))

    return program

def save_program(path, program):
    """Сохранить сгенерированную программу в JSON."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(program, file, indent=4)

def main():
    """Создать три тестовые программы."""
    examples = [
        (
            [1, 2, 3, 4, 5, 6, 7],
            [10, 20, 30, 40, 50, 60, 70],
        ),
        (
            [0, 5, 0, 10, 0, 15, 0],
            [7, 0, 8, 0, 9, 0, 10],
        ),
        (
            [100, 200, 300, 400, 500, 600, 700],
            [700, 600, 500, 400, 300, 200, 100],
        ),
    ]

    directory = Path(__file__).resolve().parents[1] / "examples"

    for index, (first, second) in enumerate(examples, start=1):
        program = generate_program(first, second)
        path = directory / f"vector_add_{index}.json"
        save_program(path, program)
        print(f"Создан файл: {path.name}")


if __name__ == "__main__":
    main()