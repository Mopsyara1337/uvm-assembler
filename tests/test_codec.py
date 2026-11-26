"""Тестирование кодирования команд УВМ."""

import unittest
from src.codec import encode_instruction, encode_program


class TestCodec(unittest.TestCase):
    """Тесты формирования машинного кода."""

    def test_load_const(self):
        instruction = (59, 98, 817)

        result = encode_instruction(instruction)
        expected = bytes.fromhex("BB 38 66 00 00 00")
        self.assertEqual(result, expected)

    def test_read(self):
        instruction = (60, 4, 122, 342)

        result = encode_instruction(instruction)
        expected = bytes.fromhex("3C 41 6F 15 00 00")
        self.assertEqual(result, expected)

    def test_write(self):
        instruction = (43, 114, 279)

        result = encode_instruction(instruction)
        expected = bytes.fromhex("AB FC 22 00 00 00")
        self.assertEqual(result, expected)

    def test_add(self):
        instruction = (30, 10, 63)

        result = encode_instruction(instruction)
        expected = bytes.fromhex("9E E2 07 00 00 00")
        self.assertEqual(result, expected)

    def test_encode_program(self):
        instruction = (
            (59, 98, 817),
            (60, 4, 122, 342),
            (43, 114, 279),
            (30, 10, 63)
        )

        result = encode_program(instruction)
        expected = bytes.fromhex(
            "BB 38 66 00 00 00 "
            "3C 41 6F 15 00 00 "
            "AB FC 22 00 00 00 "
            "9E E2 07 00 00 00"
        )
        self.assertEqual(result, expected)

    def test_program_size(self):
        """Проверить размер машинного кода программы."""
        instruction = (
            (59, 98, 817),
            (60, 4, 122, 342),
            (43, 114, 279),
            (30, 10, 63),
        )

        result = encode_program(instruction)
        self.assertEqual(len(result), 24)

    def test_empty_program(self):
        instruction = ()

        result = encode_program(instruction)
        expected = b""
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()