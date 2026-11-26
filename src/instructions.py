"""Спецификация команд учебной виртуальной машины."""

OPCODE_BITS = 6
REGISTER_BITS = 7
CONSTANT_BITS = 20
ADDRESS_BITS = 29
OFFSET_BITS = 11

INSTRUCTION_SET = {
    "LOAD_CONST": {
        "opcode": 59,
        "operands": (
            ("register", REGISTER_BITS),
            ("value", CONSTANT_BITS),
        ),
    },
    "READ": {
        "opcode": 60,
        "operands": (
            ("base_register", REGISTER_BITS),
            ("target_register", REGISTER_BITS),
            ("offset", OFFSET_BITS),
        ),
    },
    "WRITE": {
        "opcode": 43,
        "operands": (
            ("register", REGISTER_BITS),
            ("address", ADDRESS_BITS),
        ),
    },
    "ADD": {
        "opcode": 30,
        "operands": (
            ("address_register", REGISTER_BITS),
            ("target_register", REGISTER_BITS),
        ),
    },
}