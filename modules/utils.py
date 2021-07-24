import numpy as np


def byte_to_bits(bytearray: np.ndarray):
    bitarray = np.zeros(bytearray.shape + (8,), dtype="uint8")

    for i in range(7, -1, -1):
        bitarray[..., 7 - i] = bytearray // (2 ** i) % 2

    return bitarray


if __name__ == "__main__":
    print(byte_to_bits(np.array(255)))
    print(byte_to_bits(np.array(254)))
    print(byte_to_bits(np.array(33)))

    print(byte_to_bits(np.array([33, 5, 7, 9, 15])))
    print(np.logical_not(byte_to_bits(np.array([33, 5, 7, 9, 15]))).astype("byte"))
