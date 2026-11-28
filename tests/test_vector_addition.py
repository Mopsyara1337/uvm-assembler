"""Тестирование поэлементного сложения векторов."""

import unittest
from pathlib import Path

from src.assembler import read_program, translate_program
from src.codec import encode_program
from src.interpreter import Interpreter


class TestVectorAddition(unittest.TestCase):
    """Тесты итоговой задачи варианта 13."""

    def setUp(self):
        """Подготовить интерпретатор перед тестом."""
        self.interpreter = Interpreter()
        root = Path(__file__).resolve().parents[1]
        self.directory = root / "examples"

    def read_vector(self, address):
        """Прочитать вектор из памяти."""
        return [
            self.interpreter.memory.read(address + index)
            for index in range(7)
        ]

    def check_program(self, filename, first, second, expected):
        """Проверить выполнение программы сложения."""
        path = self.directory / filename
        program = read_program(path)
        translated = translate_program(program)
        encoded = encode_program(translated)

        self.interpreter.load_program(encoded)
        self.interpreter.run()

        self.assertEqual(self.read_vector(100), first)
        self.assertEqual(self.read_vector(200), second)
        self.assertEqual(self.read_vector(300), expected)
        self.assertEqual(self.interpreter.pc, 57)
        self.assertEqual(len(encoded), 342)

    def test_vector_addition_1(self):
        """Проверить сложение обычных векторов."""
        self.check_program(
            "vector_add_1.json",
            [1, 2, 3, 4, 5, 6, 7],
            [10, 20, 30, 40, 50, 60, 70],
            [11, 22, 33, 44, 55, 66, 77],
        )

    def test_vector_addition_2(self):
        """Проверить сложение векторов с нулями."""
        self.check_program(
            "vector_add_2.json",
            [0, 5, 0, 10, 0, 15, 0],
            [7, 0, 8, 0, 9, 0, 10],
            [7, 5, 8, 10, 9, 15, 10],
        )

    def test_vector_addition_3(self):
        """Проверить сложение различных значений."""
        self.check_program(
            "vector_add_3.json",
            [100, 200, 300, 400, 500, 600, 700],
            [700, 600, 500, 400, 300, 200, 100],
            [800, 800, 800, 800, 800, 800, 800],
        )


if __name__ == "__main__":
    unittest.main()