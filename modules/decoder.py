__all__ = ["fetch", "decode"]


def fetch(byteprog):
    return byteprog[:2], byteprog[2:]


def decode(bytes):
    bw1 = w2i(bytes[0])
    bw2 = w2i(bytes[1])

    w = list(bw1) + list(bw2)
    w_int = sum(16 ** i * v for i, v in enumerate(w[::-1]))

    opcode_id = -1

    if w[0] == 0x0:
        if w_int == 0x00E0:
            opcode_id = 1
        elif w_int == 0x00EE:
            opcode_id = 2
        else:
            opcode_id = 0
    elif w[0] == 0x1:
        opcode_id = 3
    elif w[0] == 0x2:
        opcode_id = 4
    elif w[0] == 0x3:
        opcode_id = 5
    elif w[0] == 0x4:
        opcode_id = 6
    elif w[0] == 0x5:
        opcode_id = 7
    elif w[0] == 0x6:
        opcode_id = 8
    elif w[0] == 0x7:
        opcode_id = 9
    elif w[0] == 0x8:
        opcode_id = OPCODE_8_IDS[w[-1]]
    elif w[0] == 0x9:
        opcode_id = 19
    elif w[0] == 0xA:
        opcode_id = 20
    elif w[0] == 0xB:
        opcode_id = 21
    elif w[0] == 0xC:
        opcode_id = 22
    elif w[0] == 0xD:
        opcode_id = 23
    elif w[0] == 0xE:
        if w[-1] == 0xE:
            opcode_id = 24
        elif w[-1] == 0x1:
            opcode_id = 25
    elif w[0] == 0xF:
        if w[3] == 0x0:
            if w[4] == 0x7:
                opcode_id = 26
            elif w[4] == 0xA:
                opcode_id = 27
        elif w[3] == 0x1:
            if w[4] == 0x5:
                opcode_id = 28
            elif w[4] == 0x8:
                opcode_id = 29
            elif w[4] == 0xE:
                opcode_id = 30
        elif w[3] == 0x2:
            opcode_id = 31
        elif w[3] == 0x3:
            opcode_id = 32
        elif w[3] == 0x5:
            opcode_id = 33
        elif w[3] == 0x6:
            opcode_id = 34

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
    0: decode_address,
    1: lambda c: None,  # Nothing to decode
    2: lambda c: None,  # Nothing to decode
    3: decode_address,
    4: decode_address,
    5: decode_reg_id_and_address,
    6: decode_reg_id_and_address,
    7: decode_double_reg_id,
    8: decode_reg_id_and_address,
    9: decode_reg_id_and_address,
    10: decode_double_reg_id,
    11: decode_double_reg_id,
    12: decode_double_reg_id,
    13: decode_double_reg_id,
    14: decode_double_reg_id,
    15: decode_double_reg_id,
    16: decode_double_reg_id,
    17: decode_double_reg_id,
    18: decode_double_reg_id,
    19: decode_double_reg_id,
    20: decode_address,
    21: decode_address,
    22: decode_reg_id_and_address,
    23: decode_double_reg_id_and_address,
    24: decode_reg_id,
    25: decode_reg_id,
    26: decode_reg_id,
    27: decode_reg_id,
    28: decode_reg_id,
    29: decode_reg_id,
    30: decode_reg_id,
    31: decode_reg_id,
    32: decode_reg_id,
    33: decode_reg_id,
    34: decode_reg_id,
}

OPCODE_8_IDS = {
    0x0: 10,
    0x1: 11,
    0x2: 12,
    0x3: 13,
    0x4: 14,
    0x5: 15,
    0x6: 16,
    0x7: 17,
    0xE: 18,

}