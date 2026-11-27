"""Тестирование объединённой памяти УВМ."""

import unittest
import tempfile
import csv
from pathlib import Path

from src.memory import Memory, MAX_ADDRESS


class TestMemory(unittest.TestCase):
    """Тесты работы с памятью."""

    def setUp(self):
        """Создать пустую память перед каждым тестом."""
        self.memory = Memory()

    def test_read_empty(self):
        """Проверить чтение пустой ячейки."""
        self.assertEqual(self.memory.read(100), 0)

    def test_write(self):
        """Проверить запись значения."""
        self.memory.write(100, 25)
        self.assertEqual(self.memory.read(100), 25)

    def test_overwrite(self):
        """Проверить перезапись значения."""
        self.memory.write(100, 25)
        self.memory.write(100, 50)
        self.assertEqual(self.memory.read(100), 50)

    def test_invalid_address(self):
        """Проверить недопустимые адреса."""
        with self.assertRaises(ValueError):
            self.memory.read(-1)

        with self.assertRaises(ValueError):
            self.memory.write(MAX_ADDRESS + 1, 25)

    def test_load_program(self):
        """Проверить загрузку машинного кода."""
        program = bytes.fromhex(
            "BB 38 66 00 00 00 "
            "3C 41 6F 15 00 00"
        )

        self.memory.write(100, 42)
        count = self.memory.load_program(program)

        self.assertEqual(count, 2)
        self.assertEqual(self.memory.read(0), 0x6638BB)
        self.assertEqual(self.memory.read(1), 0x156F413C)
        self.assertEqual(self.memory.read(100), 0)

    def test_invalid_program_size(self):
        """Проверить некорректный размер программы."""
        with self.assertRaises(ValueError):
            self.memory.load_program(bytes(5))

    def test_dump_memory(self):
        """Проверить сохранение дампа памяти."""
        self.memory.write(100, 15)
        self.memory.write(101, 25)
        self.memory.write(103, 42)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dump.csv"
            self.memory.dump_memory(path, 100, 104)

            with path.open(encoding="utf-8", newline="") as file:
                result = list(csv.reader(file))

        expected = [
            ["address", "value"],
            ["100", "15"],
            ["101", "25"],
            ["102", "0"],
            ["103", "42"],
            ["104", "0"],
        ]

        self.assertEqual(result, expected)

    def test_invalid_range(self):
        """Проверить некорректный диапазон дампа."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dump.csv"

            with self.assertRaises(ValueError):
                self.memory.dump_memory(path, 104, 100)


if __name__ == "__main__":
    unittest.main()