import numpy as np


MEM_OFFSET = 512


class Memory:
    def __init__(self):
        self.mem = np.zeros(512, dtype="byte")
        self.reg = np.array(16, dtype="byte")