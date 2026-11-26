"""Кодирование и декодирование команд УВМ."""

from src.instructions import INSTRUCTION_SET, OPCODE_BITS

INSTRUCTION_SIZE = 6
BYTE_ORDER = "little"

def get_specification(opcode):
    """Получить спецификацию команды по коду операции."""
    for specification in INSTRUCTION_SET.values():
        if specification["opcode"] == opcode:
            return specification
    raise ValueError("Команда не найдена")

def encode_instruction(instruction):
    """Преобразовать команду в машинный код."""
    comm = get_specification(instruction[0])
    result = instruction[0]
    shift = OPCODE_BITS
    for value, (name, bits) in zip(
            instruction[1:], comm["operands"]):
        result |= value << shift
        shift += bits

    return result.to_bytes(INSTRUCTION_SIZE, byteorder=BYTE_ORDER)

def encode_program(program):
    """Преобразовать всю программу в машинный код."""
    encoded = [
        encode_instruction(instruction)
        for instruction in program
    ]

    return b"".join(encoded)
