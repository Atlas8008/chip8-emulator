import numpy as np


class Arithmetics:
    def __init__(self, memory):
        self.memory = memory

    def assign(self, vx, vy):
        """ 8XY0 """
        self.memory.reg[vx] = self.memory.reg[vy]

    def assign_bitwise_or(self, vx, vy):
        """ 8XY1 """
        self.memory.reg[vx] = np.bitwise_or(self.memory.reg[vx], self.memory.reg[vy])

    def assign_bitwise_and(self, vx, vy):
        """ 8XY2 """
        self.memory.reg[vx] = np.bitwise_and(self.memory.reg[vx], self.memory.reg[vy])

    def assign_bitwise_xor(self, vx, vy):
        """ 8XY3 """
        self.memory.reg[vx] = np.bitwise_xor(self.memory.reg[vx], self.memory.reg[vy])

    def assign_add(self, vx, vy):
        """ 8XY4 """
        self.memory.reg[vx] = np.add(self.memory.reg[vx], self.memory.reg[vy])

    def assign_subtract(self, vx, vy):
        """ 8XY5 """
        self.memory.reg[vx] = np.subtract(self.memory.reg[vx], self.memory.reg[vy])

    def bit_shift_right(self, vx, vy):
        """ 8XY6 """
        # Set flag, if rightmost bit is set
        self.memory.reg[-1] = self.memory.reg[vx] % 2
        self.memory.reg[vx] = np.right_shift(self.memory.reg[vx], 1)

    def assign_subtract_inverse(self, vx, vy):
        """ 8XY7 """
        self.memory.reg[vx] = np.subtract(self.memory.reg[vy], self.memory.reg[vx])

    def bit_shift_left(self, vx, vy):
        """ 8XYE """
        # Set flag, if leftmost bit is set
        self.memory.reg[-1] = self.memory.reg[vx] // 128 % 2
        self.memory.reg[vx] = np.left_shift(self.memory.reg[vx], 1)