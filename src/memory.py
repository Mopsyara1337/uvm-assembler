"""Модель объединённой памяти УВМ."""

import csv
from src.instructions import ADDRESS_BITS
from src.codec import INSTRUCTION_SIZE, BYTE_ORDER

MIN_ADDRESS = 0
MAX_ADDRESS = (1 << ADDRESS_BITS) - 1


class Memory:
    """Объединённая память команд и данных."""

    def __init__(self):
        """Инициализировать пустую память."""
        self.cells = {}

    def validate_address(self, address):
        """Проверить допустимость адреса памяти."""
        if type(address) is not int:
            raise ValueError("Адрес должен быть целым числом")

        if not MIN_ADDRESS <= address <= MAX_ADDRESS:
            raise ValueError("Недопустимый адрес")

    def read(self, address):
        """Прочитать значение из памяти."""
        self.validate_address(address)
        return self.cells.get(address, 0)

    def write(self, address, value):
        """Записать значение в память."""
        self.validate_address(address)
        self.cells[address] = value

    def load_program(self, program):
        """Загрузить машинный код в память."""
        if len(program) % INSTRUCTION_SIZE != 0:
            raise ValueError("Неверный размер программы")

        self.cells.clear()
        address = 0

        for start in range(0, len(program), INSTRUCTION_SIZE):
            instruction = program[start:start + INSTRUCTION_SIZE]
            value = int.from_bytes(instruction, byteorder=BYTE_ORDER)
            self.write(address, value)
            address += 1

        return address

    def dump_memory(self, path, start, end):
        """Сохранить содержимое памяти в CSV-файл."""
        self.validate_address(start)
        self.validate_address(end)
        if start > end:
            raise ValueError("Недопустимый адрес памяти")

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            writer.writerow(["address", "value"])
            for address in range(start, end + 1):
                writer.writerow([address, self.read(address)])