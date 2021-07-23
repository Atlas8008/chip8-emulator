import pygame


KEY_MAPPINGS = {
    0x0: [pygame.K_0, pygame.K_KP0],
    0x1: [pygame.K_1, pygame.K_KP1],
    0x2: [pygame.K_2, pygame.K_KP2],
    0x3: [pygame.K_3, pygame.K_KP3],
    0x4: [pygame.K_4, pygame.K_KP4],
    0x5: [pygame.K_5, pygame.K_KP5],
    0x6: [pygame.K_6, pygame.K_KP6],
    0x7: [pygame.K_7, pygame.K_KP7],
    0x8: [pygame.K_8, pygame.K_KP8],
    0x9: [pygame.K_9, pygame.K_KP9],
    0xA: [pygame.K_a],
    0xB: [pygame.K_b],
    0xC: [pygame.K_c],
    0xD: [pygame.K_d],
    0xE: [pygame.K_e],
    0xF: [pygame.K_f],
}


KEY_MAPPINGS_LAYOUT = {
    0x0: [pygame.K_x],
    0x1: [pygame.K_1],
    0x2: [pygame.K_2],
    0x3: [pygame.K_3],
    0x4: [pygame.K_q],
    0x5: [pygame.K_w],
    0x6: [pygame.K_e],
    0x7: [pygame.K_a],
    0x8: [pygame.K_s],
    0x9: [pygame.K_d],
    0xA: [pygame.K_y],
    0xB: [pygame.K_c],
    0xC: [pygame.K_4],
    0xD: [pygame.K_r],
    0xE: [pygame.K_f],
    0xF: [pygame.K_v],
}


class Input:
    def __init__(self):
        # Active key mapping
        self.acm = KEY_MAPPINGS

    def key_pressed(self, val):
        key = self.acm[val]

        return pygame.key.get_pressed()[key]

    def key_unpressed(self, val):
        key = self.acm[val]

        return not pygame.key.get_pressed()[key]

    def wait_for_keypress(self, val):
        key = self.acm[val]

        pygame.event.clear()
        while True:
            event = pygame.event.wait()

            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[key]:
                return

