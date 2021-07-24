import numpy as np
import modules.opcodes as op

__all__ = ["fetch", "decode", "progbytes_to_memory"]


def progbytes_to_memory(bytes, memory, addr=0x200, endianness="big"):
    mem = np.zeros((len(bytes)), dtype="uint8")

    if endianness == "big":
        for i in range(len(mem) // 2):
            mem[2 * i] = bytes[2 * i]
            mem[2 * i + 1] = bytes[2 * i + 1]
    else:
        raise NotImplementedError("Endianness not implemented: " + endianness)

    memory.mem[addr:addr + len(mem)] = mem


def fetch(memory):
    return memory.mem[memory.pc], memory.mem[memory.pc + 1]


def decode(bytes):
    bw1 = w2i(bytes[0])
    bw2 = w2i(bytes[1])

    w = list(bw1) + list(bw2)
    w_int = sum(16 ** i * v for i, v in enumerate(w[::-1]))

    opcode_id = -1

    if w[0] == 0x0:
        if w_int == 0x00E0:
            opcode_id = op.OP_00E0  # Clear screen
        elif w_int == 0x00EE:
            opcode_id = op.OP_00EE  # Return
        else:
            opcode_id = op.OP_0NNN  # Call machine code routine
    elif w[0] == 0x1:
        opcode_id = op.OP_1NNN  # GOTO
    elif w[0] == 0x2:
        opcode_id = op.OP_2NNN  # Call subroutine
    elif w[0] == 0x3:
        opcode_id = op.OP_3XNN  # Cond eq
    elif w[0] == 0x4:
        opcode_id = op.OP_4XNN  # Cond ne
    elif w[0] == 0x5:
        opcode_id = op.OP_5XY0  # Cond reg eq
    elif w[0] == 0x6:
        opcode_id = op.OP_6XNN  # Const/set
    elif w[0] == 0x7:
        opcode_id = op.OP_7XNN  # Add-assign
    elif w[0] == 0x8:
        opcode_id = OPCODE_8_IDS[w[-1]]  # Different assignments
    elif w[0] == 0x9:
        opcode_id = op.OP_9XY0  # Cond req ne
    elif w[0] == 0xA:
        opcode_id = op.OP_ANNN  # Set address
    elif w[0] == 0xB:
        opcode_id = op.OP_BNNN  # Jump
    elif w[0] == 0xC:
        opcode_id = op.OP_CXNN  # Rand
    elif w[0] == 0xD:
        opcode_id = op.OP_DXYN  # Draw sprite
    elif w[0] == 0xE:
        if w[-1] == 0xE:
            opcode_id = op.OP_EX9E  # Skip next if key
        elif w[-1] == 0x1:
            opcode_id = op.OP_EXA1  # Skip next if not key
    elif w[0] == 0xF:
        if w[2] == 0x0:
            if w[3] == 0x7:
                opcode_id = op.OP_FX07  # Timer
            elif w[3] == 0xA:
                opcode_id = op.OP_FX0A  # Wait + assign key press
        elif w[2] == 0x1:
            if w[3] == 0x5:
                opcode_id = op.OP_FX15  # Set delay timer
            elif w[3] == 0x8:
                opcode_id = op.OP_FX18  # Set sound timer
            elif w[3] == 0xE:
                opcode_id = op.OP_FX1E  # Mem add-assign
        elif w[2] == 0x2:
            opcode_id = op.OP_FX29  # Set sprite location
        elif w[2] == 0x3:
            opcode_id = op.OP_FX33  # Store BCD
        elif w[2] == 0x5:
            opcode_id = op.OP_FX55  # Store V0 to VX
        elif w[2] == 0x6:
            opcode_id = op.OP_FX65  # Fill F0 to VX

    if opcode_id == -1:
        invalid_opcode(w)

    return opcode_id, OPCODE_ID_TO_DECODER[opcode_id](bytes)


def decode_words(code, f=1, t=-1):
    words = []

    for byte in code:
        words.extend(w2i(byte))

    if t != -1:
        words = words[f:t + 1]
    else:
        words = words[f:]

    val = 0

    for idx, word in enumerate(words[::-1]):
        val += 16 ** idx * word

    return val


def decode_address(c):
    return decode_words(c, 1),


def decode_reg_id_and_address(c):
    return decode_words(c, 1, 1), decode_words(c, 2)


def decode_reg_id(c):
    return decode_words(c, 1, 1),


def decode_double_reg_id(c):
    return decode_words(c, 1, 1), decode_words(c, 2, 2)


def decode_double_reg_id_and_address(c):
    return decode_words(c, 1, 1), decode_words(c, 2, 2), decode_words(c, 3, 3)


def b2i(b):
    return int(b)


def w2i(b):
    i = b2i(b)

    return i // 16, i % 16


def invalid_opcode(opcode):
    raise ValueError(f"Invalid opcode: {opcode}")


OPCODE_ID_TO_DECODER = {
    op.OP_0NNN: decode_address,
    op.OP_00E0: lambda c: tuple(),  # Nothing to decode
    op.OP_00EE: lambda c: tuple(),  # Nothing to decode
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
