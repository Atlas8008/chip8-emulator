import numpy as np


MEM_OFFSET = 512


class Memory:
    def __init__(self):
        # Memory:
        # Originally 512 bytes for interpreter itself (0-511/0x000-0x200), usually not used
        # Uppermost 256 bytes (3840-4095/0xF00-0xFFF) reserved for display refresh
        # 96 Bytes below that (3744-3839/0xEA0-0xEFF) reserved for call stack, internal use and other variables
        self.mem = np.zeros(4096, dtype="int8")

        self.stack_pointer = np.array(0xEA0, dtype="int16")

        # Registers:
        # 16 8-bit registers named V0 to VF
        # VF doubles as flag for some instructions, e.g. as carry flag during subtractions
        self.reg = np.array(16, dtype="int8")

        # 16-bit memory register
        self.mem_reg = np.array(1, dtype="uint16")

        # Delay timer register
        self.delay_reg = np.array(0, dtype="uint8")

        # Sound timer register
        self.sound_reg = np.array(0, dtype="uint8")