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
    specification = get_specification(instruction[0])
    result = instruction[0]
    shift = OPCODE_BITS
    for value, (name, bits) in zip(
            instruction[1:], specification["operands"]):
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

def decode_instruction(instruction):
    """Декодировать машинную команду."""
    if len(instruction) != INSTRUCTION_SIZE:
        raise ValueError("Некорректный размер команды")

    number = int.from_bytes(instruction, byteorder=BYTE_ORDER)
    mask = (1 << OPCODE_BITS) - 1
    opcode = number & mask
    specification = get_specification(opcode)
    result = [opcode]
    shift = OPCODE_BITS

    for _, bits in specification["operands"]:
        mask = (1 << bits) - 1
        result.append((number >> shift) & mask)
        shift += bits

    return tuple(result)





