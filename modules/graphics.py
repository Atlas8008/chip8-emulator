import pygame
import numpy as np

from .utils import byte_to_bits


pygame.init()


class GraphicsEmulator:
    def __init__(self, memory, real_pixels_per_pixel=15):
        self.memory = memory
        # Resolution of chip-8 is 64x32
        self.display_px = np.zeros((64, 32), dtype="uint8")
        self.display = pygame.display.set_mode((64 * real_pixels_per_pixel, 32 * real_pixels_per_pixel))
        self.rppp = real_pixels_per_pixel

        pygame.display.set_caption("Chip-8 Interpreter")

    def clear_screen(self):
        self.display_px = np.zeros((64, 32), dtype="uint8")

        self.display.fill((0, 0, 0))
        pygame.display.update()

    def draw_sprite(self, vx, vy, n):
        x = self.memory.reg[vx]
        y = self.memory.reg[vy]
        width = 8
        height = n + 1

        sprite_data = self.memory.mem[self.memory.mem_reg:self.memory.mem_reg + height]
        sprite_data = byte_to_bits(sprite_data)

        orig_content = self.display_px[x:x + width, y:y + height]

        # Check, if any value is flipped from set to unset during xor to set flag or unset it
        self.memory.reg[-1] = np.any(np.logical_and(orig_content, sprite_data))

        self.display_px[x:x + width, y:y + height] = np.logical_xor(orig_content, sprite_data)

        self.render()

    def render(self):
        for x, col in enumerate(self.display_px):
            for y, px in enumerate(col):
                if px:
                    pygame.draw.rect(
                        self.display,
                        color="white",
                        rect=(x * self.rppp, y * self.rppp, (x + 1) * self.rppp, (y + 1) * self.rppp)
                    )

        pygame.display.update()