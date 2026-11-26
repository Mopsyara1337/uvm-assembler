"""Тестирование ассемблера учебной виртуальной машины."""

import unittest

from src.assembler import translate_instruction


class TestAssembler(unittest.TestCase):
    """Тесты преобразования команд ассемблера."""

    def test_load_const(self):
        """Проверить преобразование загрузки константы."""
        instruction = {
            "op": "LOAD_CONST",
            "register": 98,
            "value": 817,
        }

        result = translate_instruction(instruction)

        self.assertEqual(result, (59, 98, 817))

    def test_read(self):
        """Проверить преобразование чтения из памяти."""
        instruction = {
            "op": "READ",
            "base_register": 4,
            "target_register": 122,
            "offset": 342,
        }

        result = translate_instruction(instruction)

        self.assertEqual(result, (60, 4, 122, 342))

    def test_write(self):
        """Проверить преобразование записи в память."""
        instruction = {
            "op": "WRITE",
            "register": 114,
            "address": 279,
        }

        result = translate_instruction(instruction)

        self.assertEqual(result, (43, 114, 279))

    def test_add(self):
        """Проверить преобразование команды сложения."""
        instruction = {
            "op": "ADD",
            "address_register": 10,
            "target_register": 63,
        }

        result = translate_instruction(instruction)

        self.assertEqual(result, (30, 10, 63))

    def test_invalid_register(self):
        """Проверить недопустимый номер регистра."""
        instruction = {
            "op": "LOAD_CONST",
            "register": 128,
            "value": 817,
        }

        with self.assertRaises(ValueError):
            translate_instruction(instruction)

    def test_unknown_operation(self):
        """Проверить неизвестную команду."""
        instruction = {
            "op": "UNKNOWN",
        }

        with self.assertRaises(ValueError):
            translate_instruction(instruction)

    def test_missing_operand(self):
        """Проверить отсутствие обязательного операнда."""
        instruction = {
            "op": "LOAD_CONST",
            "register": 98,
        }

        with self.assertRaises(ValueError):
            translate_instruction(instruction)


if __name__ == "__main__":
    unittest.main()