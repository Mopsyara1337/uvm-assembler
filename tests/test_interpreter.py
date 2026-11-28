"""Тестирование интерпретатора УВМ."""

import unittest
from pathlib import Path

from src.assembler import read_program, translate_program
from src.codec import encode_program
from src.interpreter import Interpreter


class TestInterpreter(unittest.TestCase):
    """Тесты выполнения машинных команд."""

    def setUp(self):
        """Создать виртуальную машину перед каждым тестом."""
        self.interpreter = Interpreter()

    def test_initial_state(self):
        """Проверить начальное состояние УВМ."""
        self.assertEqual(self.interpreter.registers, [0] * 128)
        self.assertEqual(self.interpreter.pc, 0)
        self.assertEqual(self.interpreter.program_size, 0)

    def test_load_program(self):
        """Проверить загрузку и сброс состояния УВМ."""
        program = bytes.fromhex("BB 38 66 00 00 00")

        self.interpreter.registers[0] = 100
        self.interpreter.pc = 5
        self.interpreter.load_program(program)

        self.assertEqual(self.interpreter.program_size, 1)
        self.assertEqual(self.interpreter.pc, 0)
        self.assertEqual(self.interpreter.registers, [0] * 128)

    def test_fetch_instruction(self):
        """Проверить получение и декодирование команды."""
        program = bytes.fromhex("BB 38 66 00 00 00")
        self.interpreter.load_program(program)

        result = self.interpreter.fetch_instruction()

        self.assertEqual(result, (59, 98, 817))
        self.assertEqual(self.interpreter.pc, 0)

    def test_execute_load_const(self):
        """Проверить загрузку константы."""
        self.interpreter.execute_load_const(2, 100)

        self.assertEqual(self.interpreter.registers[2], 100)

    def test_execute_write(self):
        """Проверить запись регистра в память."""
        self.interpreter.registers[2] = 42
        self.interpreter.execute_write(2, 100)

        self.assertEqual(self.interpreter.memory.read(100), 42)

    def test_execute_read(self):
        """Проверить чтение из памяти со смещением."""
        self.interpreter.registers[0] = 100
        self.interpreter.memory.write(103, 42)

        self.interpreter.execute_read(0, 2, 3)

        self.assertEqual(self.interpreter.registers[2], 42)

    def test_unsupported_operation(self):
        """Проверить обработку неизвестной операции."""
        with self.assertRaises(ValueError):
            self.interpreter.execute_instruction((0,))

    def test_unified_memory(self):
        """Проверить использование общей памяти."""
        program = bytes.fromhex("BB 38 66 00 00 00")
        self.interpreter.load_program(program)

        self.interpreter.memory.write(0, 0x07E29E)

        result = self.interpreter.fetch_instruction()

        self.assertEqual(result, (30, 10, 63))

    def test_copy_array(self):
        """Проверить выполнение программы копирования массива."""
        root = Path(__file__).resolve().parents[1]
        path = root / "examples" / "copy_array.json"

        program = read_program(path)
        translated = translate_program(program)
        encoded = encode_program(translated)

        self.interpreter.load_program(encoded)
        self.interpreter.run()

        source = [
            self.interpreter.memory.read(address)
            for address in range(100, 103)
        ]

        target = [
            self.interpreter.memory.read(address)
            for address in range(200, 203)
        ]

        self.assertEqual(source, [15, 25, 35])
        self.assertEqual(target, [15, 25, 35])
        self.assertEqual(self.interpreter.pc, 13)

    def test_execute_add(self):
        """Проверить сложение регистра со значением из памяти."""
        self.interpreter.registers[2] = 100
        self.interpreter.registers[4] = 15
        self.interpreter.memory.write(100, 25)

        self.interpreter.execute_add(2, 4)

        self.assertEqual(self.interpreter.registers[4], 40)
        self.assertEqual(self.interpreter.registers[2], 100)
        self.assertEqual(self.interpreter.memory.read(100), 25)

    def test_add_zero(self):
        """Проверить сложение с нулём."""
        self.interpreter.registers[2] = 100
        self.interpreter.registers[4] = 15

        self.interpreter.execute_add(2, 4)

        self.assertEqual(self.interpreter.registers[4], 15)

    def test_add_same_register(self):
        """Проверить использование одного регистра для ADD."""
        self.interpreter.registers[2] = 100
        self.interpreter.memory.write(100, 25)

        self.interpreter.execute_add(2, 2)

        self.assertEqual(self.interpreter.registers[2], 125)

    def test_addition_program(self):
        """Проверить выполнение программы сложения."""
        root = Path(__file__).resolve().parents[1]
        path = root / "examples" / "addition.json"

        program = read_program(path)
        translated = translate_program(program)
        encoded = encode_program(translated)

        self.interpreter.load_program(encoded)
        self.interpreter.run()

        self.assertEqual(self.interpreter.registers[2], 40)
        self.assertEqual(self.interpreter.memory.read(100), 25)
        self.assertEqual(self.interpreter.memory.read(200), 40)
        self.assertEqual(self.interpreter.pc, 6)


if __name__ == "__main__":
    unittest.main()