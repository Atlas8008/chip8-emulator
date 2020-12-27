from .decoder import *
from .graphics_emu import GraphicsEmulator
from .mem_emu import Memory
from .sound_emu import SoundEmulator

import opcodes as op


class Emulator:
    def __init__(self, fname):
        self.graphics = GraphicsEmulator()
        self.memory = Memory()
        self.sound = SoundEmulator()

        self.pid = 0

        with open(fname, "rb") as f:
            self.prog = f.read()

    def run(self):
        self.pid = 0

        while True:
            opcode = fetch(self.prog, self.pid)

            opcode_id, args = decode(opcode)

            action = OPCODE_TO_ACTION[opcode_id]

            ret = action(*args)


OPCODE_TO_ACTION = {
    op.OP_0NNN: lambda emu, args: None,
    op.OP_00E0: lambda emu, args: None,
    op.OP_00EE: lambda emu, args: None,
    op.OP_1NNN: lambda emu, args: None,
    op.OP_2NNN: lambda emu, args: None,
    op.OP_3XNN: lambda emu, args: None,
    op.OP_4XNN: lambda emu, args: None,
    op.OP_5XY0: lambda emu, args: None,
    op.OP_6XNN: lambda emu, args: None,
    op.OP_7XNN: lambda emu, args: None,
    op.OP_8XY0: lambda emu, args: None,
    op.OP_8XY1: lambda emu, args: None,
    op.OP_8XY2: lambda emu, args: None,
    op.OP_8XY3: lambda emu, args: None,
    op.OP_8XY4: lambda emu, args: None,
    op.OP_8XY5: lambda emu, args: None,
    op.OP_8XY6: lambda emu, args: None,
    op.OP_8XY7: lambda emu, args: None,
    op.OP_8XYE: lambda emu, args: None,
    op.OP_9XY0: lambda emu, args: None,
    op.OP_ANNN: lambda emu, args: None,
    op.OP_BNNN: lambda emu, args: None,
    op.OP_CXNN: lambda emu, args: None,
    op.OP_DXYN: lambda emu, args: None,
    op.OP_EX9E: lambda emu, args: None,
    op.OP_EXA1: lambda emu, args: None,
    op.OP_FX07: lambda emu, args: None,
    op.OP_FX0A: lambda emu, args: None,
    op.OP_FX15: lambda emu, args: None,
    op.OP_FX18: lambda emu, args: None,
    op.OP_FX1E: lambda emu, args: None,
    op.OP_FX29: lambda emu, args: None,
    op.OP_FX33: lambda emu, args: None,
    op.OP_FX55: lambda emu, args: None,
    op.OP_FX65: lambda emu, args: None,
}