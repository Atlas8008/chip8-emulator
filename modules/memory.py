import numpy as np


MEM_OFFSET = 512

FONT_DATA = [
    np.array([ # 0
        0b11110000,
        0b10010000,
        0b10010000,
        0b10010000,
        0b11110000,
    ], dtype="uint8"),
    np.array([ # 1
        0b00100000,
        0b01100000,
        0b00100000,
        0b00100000,
        0b01110000,
    ], dtype="uint8"),
    np.array([ # 2
        0b11110000,
        0b00010000,
        0b11110000,
        0b10000000,
        0b11110000,
    ], dtype="uint8"),
    np.array([ # 3
        0b11110000,
        0b00010000,
        0b11110000,
        0b00010000,
        0b11110000,
    ], dtype="uint8"),
    np.array([ # 4
        0b10010000,
        0b10010000,
        0b11110000,
        0b00010000,
        0b00010000,
    ], dtype="uint8"),
    np.array([ # 5
        0b11110000,
        0b10000000,
        0b11110000,
        0b00010000,
        0b11110000,
    ], dtype="uint8"),
    np.array([ # 6
        0b11110000,
        0b10000000,
        0b11110000,
        0b10010000,
        0b11110000,
    ], dtype="uint8"),
    np.array([ # 7
        0b11110000,
        0b00010000,
        0b00100000,
        0b01000000,
        0b01000000,
    ], dtype="uint8"),
    np.array([ # 8
        0b11110000,
        0b10010000,
        0b11110000,
        0b10010000,
        0b11110000,
    ], dtype="uint8"),
    np.array([ # 9
        0b11110000,
        0b10010000,
        0b11110000,
        0b00010000,
        0b11110000,
    ], dtype="uint8"),
    np.array([ # A
        0b11110000,
        0b10010000,
        0b11110000,
        0b10010000,
        0b10010000,
    ], dtype="uint8"),
    np.array([ # B
        0b11100000,
        0b10010000,
        0b11100000,
        0b10010000,
        0b11100000,
    ], dtype="uint8"),
    np.array([ # C
        0b11110000,
        0b10000000,
        0b10000000,
        0b10000000,
        0b11110000,
    ], dtype="uint8"),
    np.array([ # D
        0b11100000,
        0b10010000,
        0b10010000,
        0b10010000,
        0b11100000,
    ], dtype="uint8"),
    np.array([ # E
        0b11110000,
        0b10000000,
        0b11110000,
        0b10000000,
        0b11110000,
    ], dtype="uint8"),
    np.array([ # F
        0b11110000,
        0b10000000,
        0b11110000,
        0b10000000,
        0b10000000,
    ], dtype="uint8"),
]

class Memory:
    def __init__(self):
        # Memory:
        # Originally 512 bytes for interpreter itself (0-511/0x000-0x200), usually not used (except for font data)
        # Uppermost 256 bytes (3840-4095/0xF00-0xFFF) reserved for display refresh
        # 96 Bytes below that (3744-3839/0xEA0-0xEFF) reserved for call stack, internal use and other variables
        self.mem = np.zeros(4096, dtype="uint8")

        # Initialize font data
        for i, bindata in enumerate(FONT_DATA):
            self.mem[i * 5:i * 5 + 5] = bindata

        self._stack_pointer = np.array([0xEA0], dtype="uint16")

        # Registers:
        # 16 8-bit registers named V0 to VF
        # VF doubles as flag for some instructions, e.g. as carry flag during subtractions
        self.reg = np.zeros(16, dtype="uint8")

        # 16-bit memory register
        self._mem_reg = np.array([0x200], dtype="uint16")

        # Delay timer register
        self._delay_reg = np.array([0], dtype="uint8")

        # Sound timer register
        self._sound_reg = np.array([0], dtype="uint8")

        self._pc = np.array([0x200], dtype="uint16")

    @property
    def mem_reg(self):
        return self._mem_reg[0]

    @mem_reg.setter
    def mem_reg(self, v):
        self._mem_reg[0] = v

    @property
    def delay_reg(self):
        return self._delay_reg[0]

    @delay_reg.setter
    def delay_reg(self, v):
        self._delay_reg[0] = v

    @property
    def sound_reg(self):
        return self._sound_reg[0]

    @sound_reg.setter
    def sound_reg(self, v):
        self._sound_reg[0] = v

    @property
    def stack_pointer(self):
        return self._stack_pointer[0]

    @stack_pointer.setter
    def stack_pointer(self, v):
        self._stack_pointer[0] = v

    @property
    def pc(self):
        return self._pc[0]

    @pc.setter
    def pc(self, v):
        self._pc[0] = v

