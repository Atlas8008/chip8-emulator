import time
import random
import numpy as np

from threading import Thread

from .decoder import *
from .graphics import GraphicsEmulator
from .memory import Memory
from .sound_emu import SoundEmulator
from .arithmetics import Arithmetics
from .input import Input

import modules.opcodes as op

# TODO: Set interpreter frequency
# TODO: Implement program counter as index and put program code in memory

class Emulator:
    def __init__(self, fname):
        self.memory = Memory()
        self.graphics = GraphicsEmulator(memory=self.memory)
        self.sound = SoundEmulator(memory=self.memory)
        self.arithmetics = Arithmetics(self.memory)
        self.input = Input()

        self.delay_timer = Thread(target=self.delay_timer_fun, daemon=True)
        self.sound_timer = Thread(target=self.sound_timer_fun, daemon=True)

        self.jumped = False

        self.verbosity = 0

        self.OPCODE_TO_ACTION = self.define_opcode_actions()

        with open(fname, "rb") as f:
            self.prog = f.read()

            if self.verbosity >= 1:
                print(self.prog)
                print(len(self.prog))

            progbytes_to_memory(self.prog, self.memory)

    def run(self):
        self.delay_timer.start()
        self.sound_timer.start()

        while True:
            self.jumped = False

            opcode = fetch(self.memory)

            # Skip empty opcodes
            #if not opcode:
            #    continue
            if self.verbosity >= 1:
                print("Opcode: ", opcode)
                print("Opcode hex: ", bytes(opcode).hex())

            opcode_id, args = decode(opcode)

            action = self.OPCODE_TO_ACTION[opcode_id]

            if self.verbosity >= 1:
                print("Opcode id: ", opcode_id)
                print("Opcode args:", args)

            action(*args)

            if not self.jumped:
                self.memory.pc += 0x2

    def jump_to_subroutine(self, addr):
        self.memory.stack_pointer += 0x2
        self.memory.mem[self.memory.stack_pointer:self.memory.stack_pointer + 2] = \
            np.array([self.memory.pc // 2 ** 8, self.memory.pc % 2 ** 8])

        self.memory.pc = addr
        self.jumped = True

    def return_from_subroutine(self):
        vals = self.memory.mem[self.memory.stack_pointer:self.memory.stack_pointer + 2]

        self.memory.pc = vals[0] * 2 ** 8 | vals[1]
        self.memory.pc += 2  # Go to next instruction after jumping back

        self.memory.stack_pointer -= 2

        self.jumped = True

    def jump_to_address(self, addr):
        self.memory.pc = addr
        self.jumped = True

    def jump_to_address_relative(self, addr):
        # Jump to adress value + v0
        self.memory.pc = addr + self.memory.reg[0]
        self.jumped = True

    def skip_if_reg_num_equal(self, vx, num):
        if self.memory.reg[vx] == num:
            self.memory.pc += 4
            self.jumped = True

    def skip_if_reg_num_unequal(self, vx, num):
        if self.memory.reg[vx] != num:
            self.memory.pc += 4
            self.jumped = True

    def skip_if_regs_equal(self, vx, vy):
        if self.memory.reg[vx] == self.memory.reg[vy]:
            self.memory.pc += 4
            self.jumped = True

    def skip_if_regs_unequal(self, vx, vy):
        if self.memory.reg[vx] != self.memory.reg[vy]:
            self.memory.pc += 4
            self.jumped = True

    def set_mem_address_pointer(self, addr):
        self.memory.mem_reg = addr

    def random_number(self, vx, nn):
        self.memory.reg[vx] = np.bitwise_and(random.randint(0, 255), nn)

    def skip_if_key_pressed(self, vx):
        if self.input.key_pressed(self.memory.reg[vx]):
            self.memory.pc += 4
            self.jumped = True

    def skip_if_key_unpressed(self, vx):
        if self.input.key_unpressed(self.memory.reg[vx]):
            self.memory.pc += 4
            self.jumped = True

    def get_delay_timer(self, vx):
        self.memory.reg[vx] = self.memory.delay_reg

    def wait_for_keypress(self, vx):
        key = self.input.wait_for_keypress()

        self.memory.reg[vx] = key

    def set_delay_timer(self, vx):
        self.memory.delay_reg = self.memory.reg[vx]

    def set_sound_timer(self, vx):
        self.memory.sound_reg = self.memory.reg[vx]

    def add_reg_to_mem_addr(self, vx):
        self.memory.mem_reg += self.memory.reg[vx]

    def set_addr_to_sprite_loc(self, vx):
        # Sprites are stored at the first 16 sprite locations in memory; each sprite location has a size of 5 byte
        self.memory.mem_reg = self.memory.reg[vx] * 5

    def store_bcd(self, vx):
        val = self.memory.reg[vx]

        digits = []

        for i in range(3):
            digits.append(val % 10)
            val //= 10

        digits = digits[::-1]

        #bcd = byte_to_bits(np.array(digits))

        self.memory.mem[self.memory.mem_reg:self.memory.mem_reg + 3] = digits

    def store_regs_in_mem(self, vx):
        to_store = self.memory.reg[0:vx + 1]

        self.memory.mem[self.memory.mem_reg:self.memory.mem_reg + vx + 1] = to_store

    def load_regs_from_mem(self, vx):
        self.memory.reg[0:vx + 1] = self.memory.mem[self.memory.mem_reg:self.memory.mem_reg + vx + 1]

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
            op.OP_00EE: self.return_from_subroutine,  # Return from subroutine
            op.OP_1NNN: self.jump_to_address,  # Jump to address
            op.OP_2NNN: self.jump_to_subroutine,  # Call subroutine
            op.OP_3XNN: self.skip_if_reg_num_equal,  # Skip next if reg equal to num
            op.OP_4XNN: self.skip_if_reg_num_unequal,  # Skip next if regs are unequal
            op.OP_5XY0: self.skip_if_regs_equal,  # Skip next if regs are equal
            op.OP_6XNN: self.arithmetics.assign_val,  # Assign val
            op.OP_7XNN: self.arithmetics.assign_add_val,  # Assign add val
            op.OP_8XY0: self.arithmetics.assign,  # Assign reg
            op.OP_8XY1: self.arithmetics.assign_bitwise_or,  # Assign bitwise or reg
            op.OP_8XY2: self.arithmetics.assign_bitwise_and,  # Assign bitwise and reg
            op.OP_8XY3: self.arithmetics.assign_bitwise_xor,  # Assign bitwise xor reg
            op.OP_8XY4: self.arithmetics.assign_add,  # Assign add reg
            op.OP_8XY5: self.arithmetics.assign_subtract,  # Assign subtract reg
            op.OP_8XY6: self.arithmetics.bit_shift_right,  # Assign bit shift right
            op.OP_8XY7: self.arithmetics.assign_subtract_inverse,  # Assign inverse subtract reg
            op.OP_8XYE: self.arithmetics.bit_shift_left,  # Assign bit shift left
            op.OP_9XY0: self.skip_if_regs_unequal,  # Skip next if regs are unequal
            op.OP_ANNN: self.set_mem_address_pointer,  # Set address pointer to num
            op.OP_BNNN: self.jump_to_address_relative,  # Jump to address (relative)
            op.OP_CXNN: self.random_number,  # Random number
            op.OP_DXYN: self.graphics.draw_sprite,  # Draw sprite
            op.OP_EX9E: self.skip_if_key_pressed,  # Skip next instruction if key is pressed
            op.OP_EXA1: self.skip_if_key_unpressed,  # Skip next instruction if key is not pressed
            op.OP_FX07: self.get_delay_timer,  # Get value of delay timer
            op.OP_FX0A: self.wait_for_keypress,  # Wait for key press + store it
            op.OP_FX15: self.set_delay_timer,  # Set delay timer
            op.OP_FX18: self.set_sound_timer,  # Set sound timer
            op.OP_FX1E: self.add_reg_to_mem_addr,  # Add reg to mem reg
            op.OP_FX29: self.set_addr_to_sprite_loc,  # Set I to sprite location
            op.OP_FX33: self.store_bcd,  # Store BCD representation of reg
            op.OP_FX55: self.store_regs_in_mem,  # Store regs in memory
            op.OP_FX65: self.load_regs_from_mem,  # Fill regs with vals from memory
        }