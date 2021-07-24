import pygame
import numpy as np


if __name__ == "__main__":
    from utils import byte_to_bits
else:
    from .utils import byte_to_bits


pygame.init()


class GraphicsEmulator:
    def __init__(self, memory, real_pixels_per_pixel=15):
        self.memory = memory
        # Resolution of chip-8 is 64x32
        self.display_px = np.zeros((32, 64), dtype="uint8")
        self.display = pygame.display.set_mode((64 * real_pixels_per_pixel, 32 * real_pixels_per_pixel))
        self.rppp = real_pixels_per_pixel

        pygame.display.set_caption("Chip-8 Interpreter")

    def clear_screen(self):
        self.display_px = np.zeros((32, 64), dtype="uint8")

        self.display.fill((0, 0, 0))
        pygame.display.update()

    def draw_sprite(self, vx, vy, n):
        x = self.memory.reg[vx]
        y = self.memory.reg[vy]
        width = 8
        height = n

        sprite_data = self.memory.mem[self.memory.mem_reg:self.memory.mem_reg + height]
        sprite_data = byte_to_bits(sprite_data)

        orig_content = self.display_px[y:y + height, x:x + width]  # TODO: Screen wraparound

        # Zero pad orig content
        """orig_content = np.pad(
            orig_content,
            [
                [-min(0, y), max(y + height, self.display_px.shape[0]) - self.display_px.shape[0]],
                [-min(0, x), max(x + width, self.display_px.shape[1]) - self.display_px.shape[1]],
            ],
        )

        # Allow sprites at the right border by cropping the sprite to fit into the window
        sprite_data = sprite_data[:, :orig_content.shape[1]]"""

        # Check, if any value is flipped from set to unset during xor to set flag or unset it
        self.memory.reg[-1] = np.any(np.logical_and(orig_content, sprite_data))

        self.display_px[y:y + height, x:x + width] = np.logical_xor(orig_content, sprite_data)

        self.render()

    def render(self):
        for y, row in enumerate(self.display_px):
            for x, px in enumerate(row):
                if px:
                    pygame.draw.rect(
                        self.display,
                        color="white",
                        rect=(x * self.rppp, y * self.rppp, self.rppp, self.rppp)
                    )

        pygame.display.update()


if __name__ == "__main__":
    from memory import Memory

    mem = Memory()

    ge = GraphicsEmulator(mem, real_pixels_per_pixel=20)

    print(mem.reg)

    mem.reg[2] = 1
    mem.reg[3] = 7

    mem.mem_reg = 200
    mem.mem[200] = 0b10010110
    mem.mem[201] = 0b11110000
    mem.mem[202] = 0b00000011
    mem.mem[203] = 0b11111100

    print("Mem:")
    print(mem.mem[200])

    ge.clear_screen()
    ge.draw_sprite(2, 3, 3)

    print(mem.reg[-1])

    ge.draw_sprite(2, 3, 3)

    print(mem.reg[-1])

    ge.draw_sprite(2, 3, 3)

    print(mem.reg[-1])

    print(np.sum(ge.display_px))

    input()