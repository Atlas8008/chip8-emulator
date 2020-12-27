import opcodes as op

__all__ = ["fetch", "decode"]


def fetch(p_id, byteprog):
    return byteprog[2 * p_id:2 * p_id + 2]


def decode(bytes):
    bw1 = w2i(bytes[0])
    bw2 = w2i(bytes[1])

    w = list(bw1) + list(bw2)
    w_int = sum(16 ** i * v for i, v in enumerate(w[::-1]))

    opcode_id = -1

    if w[0] == 0x0:
        if w_int == 0x00E0:
            opcode_id = op.OP_00E0
        elif w_int == 0x00EE:
            opcode_id = op.OP_00EE
        else:
            opcode_id = op.OP_0NNN
    elif w[0] == 0x1:
        opcode_id = op.OP_1NNN
    elif w[0] == 0x2:
        opcode_id = op.OP_2NNN
    elif w[0] == 0x3:
        opcode_id = op.OP_3XNN
    elif w[0] == 0x4:
        opcode_id = op.OP_4XNN
    elif w[0] == 0x5:
        opcode_id = op.OP_5XY0
    elif w[0] == 0x6:
        opcode_id = op.OP_6XNN
    elif w[0] == 0x7:
        opcode_id = op.OP_7XNN
    elif w[0] == 0x8:
        opcode_id = OPCODE_8_IDS[w[-1]]
    elif w[0] == 0x9:
        opcode_id = op.OP_9XY0
    elif w[0] == 0xA:
        opcode_id = op.OP_ANNN
    elif w[0] == 0xB:
        opcode_id = op.OP_BNNN
    elif w[0] == 0xC:
        opcode_id = op.OP_CXNN
    elif w[0] == 0xD:
        opcode_id = op.OP_DXYN
    elif w[0] == 0xE:
        if w[-1] == 0xE:
            opcode_id = op.OP_EX9E
        elif w[-1] == 0x1:
            opcode_id = op.OP_EXA1
    elif w[0] == 0xF:
        if w[3] == 0x0:
            if w[4] == 0x7:
                opcode_id = op.OP_FX07
            elif w[4] == 0xA:
                opcode_id = op.OP_FX0A
        elif w[3] == 0x1:
            if w[4] == 0x5:
                opcode_id = op.OP_FX15
            elif w[4] == 0x8:
                opcode_id = op.OP_FX18
            elif w[4] == 0xE:
                opcode_id = op.OP_FX1E
        elif w[3] == 0x2:
            opcode_id = op.OP_FX29
        elif w[3] == 0x3:
            opcode_id = op.OP_FX33
        elif w[3] == 0x5:
            opcode_id = op.OP_FX55
        elif w[3] == 0x6:
            opcode_id = op.OP_FX65

    if opcode_id == -1:
        invalid_opcode(w)

    return opcode_id, OPCODE_ID_TO_DECODER[opcode_id](bytes)


def decode_words(code, f=1, t=-1):
    words = []

    for byte in code:
        words.extend(w2i(byte))

    words = words[f:t + 1]

    val = 0

    for idx, word in enumerate(words[::-1]):
        val += 16 ** idx * word

    return val


def decode_address(c):
    return decode_words(c, 1),


def decode_reg_id_and_address(c):
    return decode_words(c, 1, 1), decode_words(c, 2)


def decode_reg_id(c):
    return decode_words(c, 1, 1)


def decode_double_reg_id(c):
    return decode_words(c, 1, 1), decode_words(c, 2, 2)


def decode_double_reg_id_and_address(c):
    return decode_words(c, 1, 1), decode_words(c, 2, 2), decode_words(c, 3, 3)


def b2i(b):
    return int(b[0])


def w2i(b):
    i = b2i(b)

    return i // 16, i % 16


def bytes_to_int(bytes, endianness="big"):
    if endianness == "big":
        return 16 * int(bytes[1][0]) + int(bytes[0][0])
    else:
        raise NotImplementedError()


def invalid_opcode(opcode):
    raise ValueError(f"Invalid opcode: {opcode}")


OPCODE_PATTERNS = {
    "0XXX": (0, decode_address),
    "00E0": (1, lambda c: None),  # Nothing to decode
    "00EE": (2, lambda c: None),  # Nothing to decode
    "1XXX": (3, decode_address),
    "2XXX": (4, decode_address),
    "3XXX": (5, decode_reg_id_and_address),
    "4XXX": (6, decode_reg_id_and_address),
    "5XX0": (7, decode_double_reg_id),
    "6XXX": (8, decode_reg_id_and_address),
    "7XXX": (9, decode_reg_id_and_address),
    "8XX0": (10, decode_double_reg_id),
    "8XX1": (11, decode_double_reg_id),
    "8XX2": (12, decode_double_reg_id),
    "8XX3": (13, decode_double_reg_id),
    "8XX4": (14, decode_double_reg_id),
    "8XX5": (15, decode_double_reg_id),
    "8XX6": (16, decode_double_reg_id),
    "8XX7": (17, decode_double_reg_id),
    "8XXE": (18, decode_double_reg_id),
    "9XX0": (19, decode_double_reg_id),
    "AXXX": (20, decode_address),
    "BXXX": (21, decode_address),
    "CXXX": (22, decode_reg_id_and_address),
    "DXXX": (23, decode_double_reg_id_and_address),
    "EX9E": (24, decode_reg_id),
    "EXA1": (25, decode_reg_id),
    "FX07": (26, decode_reg_id),
    "FX0A": (27, decode_reg_id),
    "FX15": (28, decode_reg_id),
    "FX18": (29, decode_reg_id),
    "FX1E": (30, decode_reg_id),
    "FX29": (31, decode_reg_id),
    "FX33": (32, decode_reg_id),
    "FX55": (33, decode_reg_id),
    "FX65": (34, decode_reg_id),
}

OPCODE_ID_TO_DECODER = {
    op.OP_0NNN: decode_address,
    op.OP_00E0: lambda c: None,  # Nothing to decode
    op.OP_00EE: lambda c: None,  # Nothing to decode
    op.OP_1NNN: decode_address,
    op.OP_2NNN: decode_address,
    op.OP_3XNN: decode_reg_id_and_address,
    op.OP_4XNN: decode_reg_id_and_address,
    op.OP_5XY0: decode_double_reg_id,
    op.OP_6XNN: decode_reg_id_and_address,
    op.OP_7XNN: decode_reg_id_and_address,
    op.OP_8XY0: decode_double_reg_id,
    op.OP_8XY1: decode_double_reg_id,
    op.OP_8XY2: decode_double_reg_id,
    op.OP_8XY3: decode_double_reg_id,
    op.OP_8XY4: decode_double_reg_id,
    op.OP_8XY5: decode_double_reg_id,
    op.OP_8XY6: decode_double_reg_id,
    op.OP_8XY7: decode_double_reg_id,
    op.OP_8XYE: decode_double_reg_id,
    op.OP_9XY0: decode_double_reg_id,
    op.OP_ANNN: decode_address,
    op.OP_BNNN: decode_address,
    op.OP_CXNN: decode_reg_id_and_address,
    op.OP_DXYN: decode_double_reg_id_and_address,
    op.OP_EX9E: decode_reg_id,
    op.OP_EXA1: decode_reg_id,
    op.OP_FX07: decode_reg_id,
    op.OP_FX0A: decode_reg_id,
    op.OP_FX15: decode_reg_id,
    op.OP_FX18: decode_reg_id,
    op.OP_FX1E: decode_reg_id,
    op.OP_FX29: decode_reg_id,
    op.OP_FX33: decode_reg_id,
    op.OP_FX55: decode_reg_id,
    op.OP_FX65: decode_reg_id,
}

OPCODE_8_IDS = {
    0x0: op.OP_8XY0,
    0x1: op.OP_8XY1,
    0x2: op.OP_8XY2,
    0x3: op.OP_8XY3,
    0x4: op.OP_8XY4,
    0x5: op.OP_8XY5,
    0x6: op.OP_8XY6,
    0x7: op.OP_8XY7,
    0xE: op.OP_8XYE,
}
