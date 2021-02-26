import time
import numpy as np

from threading import Thread

from .decoder import *
from .graphics import GraphicsEmulator
from .memory import Memory
from .sound_emu import SoundEmulator

import modules.opcodes as op

# TODO: Set interpreter frequency

class Emulator:
    def __init__(self, fname):
        self.memory = Memory()
        self.graphics = GraphicsEmulator(memory=self.memory)
        self.sound = SoundEmulator(memory=self.memory)

        self.delay_timer = Thread(target=self.delay_timer_fun)
        self.sound_timer = Thread(target=self.sound_timer_fun)

        self.pc = np.array(0)

        self.OPCODE_TO_ACTION = self.define_opcode_actions()

        with open(fname, "rb") as f:
            self.prog = f.read()

    def run(self):
        self.pc = np.array(0)
        self.delay_timer.start()
        self.sound_timer.start()

        while True:
            opcode = fetch(self.prog, self.pc)

            opcode_id, args = decode(opcode)

            action = self.OPCODE_TO_ACTION[opcode_id]

            ret = action(*args)

    def delay_timer_fun(self):
        while True:
            time.sleep(1 / 60)

            if self.memory.delay_reg > 0:
                self.memory.delay_reg -= 1

    def sound_timer_fun(self):
        while True:
            time.sleep(1 / 60)

            if self.memory.sound_reg > 0:
                self.memory.sound_reg -= 1

    def define_opcode_actions(self):
        return {
            op.OP_0NNN: lambda args: None,  # Call machine code routine
            op.OP_00E0: self.graphics.clear_screen,  # Clear screen
            op.OP_00EE: lambda args: None,  # Return from subroutine
            op.OP_1NNN: lambda args: None,  # Jump to address
            op.OP_2NNN: lambda args: None,  # Call subroutine
            op.OP_3XNN: lambda args: None,  # Skip next if reg equal to num
            op.OP_4XNN: lambda args: None,  # Skip next if regs are unequal
            op.OP_5XY0: lambda args: None,  # Skip next if regs are equal
            op.OP_6XNN: lambda args: None,  # Assign val
            op.OP_7XNN: lambda args: None,  # Assign add val
            op.OP_8XY0: lambda args: None,  # Assign reg
            op.OP_8XY1: lambda args: None,  # Assign bitwise or reg
            op.OP_8XY2: lambda args: None,  # Assign bitwise and reg
            op.OP_8XY3: lambda args: None,  # Assign bitwise xor reg
            op.OP_8XY4: lambda args: None,  # Assign add reg
            op.OP_8XY5: lambda args: None,  # Assign subtract reg
            op.OP_8XY6: lambda args: None,  # Assign bit shift right
            op.OP_8XY7: lambda args: None,  # Assign inverse subtract reg
            op.OP_8XYE: lambda args: None,  # Assign bit shift left
            op.OP_9XY0: lambda args: None,  # Skip next if
            op.OP_ANNN: lambda args: None,  # Set address pointer to num
            op.OP_BNNN: lambda args: None,  # Jump to address
            op.OP_CXNN: lambda args: None,  # Random number
            op.OP_DXYN: lambda args: None,  # Draw sprite
            op.OP_EX9E: lambda args: None,  # Skip next instruction if key is pressed
            op.OP_EXA1: lambda args: None,  # Skip next instruction if key is not pressed
            op.OP_FX07: lambda args: None,  # Get value of delay timer
            op.OP_FX0A: lambda args: None,  # Wait for key press + store it
            op.OP_FX15: lambda args: None,  # Set delay timer
            op.OP_FX18: lambda args: None,  # Set sound timer
            op.OP_FX1E: lambda args: None,  # Add reg to mem reg
            op.OP_FX29: lambda args: None,  # Set I to sprite location
            op.OP_FX33: lambda args: None,  # Store BCD representation of reg
            op.OP_FX55: lambda args: None,  # Store regs in memory
            op.OP_FX65: lambda args: None,  # Fill regs with vals from memory
        }