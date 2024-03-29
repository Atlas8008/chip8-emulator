import sys
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

RESET = -1


class Input:
    def __init__(self):
        # Active key mapping
        self.acm = KEY_MAPPINGS_LAYOUT

        self.pressed = {k: False for k in self.acm.keys()}

    def update_keys(self):
        while True:
            event = pygame.event.poll()

            if event.type == pygame.NOEVENT:
                return 0
            elif event.type == pygame.WINDOWCLOSE:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                for v, keys in self.acm.items():
                    for k in keys:
                        if event.key == k:
                            self.pressed[v] = True

                if event.key == pygame.K_ESCAPE:
                    #pygame.display.quit()
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_RETURN:
                    pygame.event.clear()

                    return RESET
            elif event.type == pygame.KEYUP:
                for v, keys in self.acm.items():
                    for k in keys:
                        if event.key == k:
                            self.pressed[v] = False

    def key_pressed(self, val):
        #keys = self.acm[val].keys()

        #return any(self.pressed[k] for k in keys)
        return self.pressed[val]

    def key_unpressed(self, val):
        #keys = self.acm[val].keys()

        #return not any(self.pressed[k] for k in keys)
        return not self.pressed[val]

    def wait_for_keypress(self):
        pygame.event.clear()
        while True:
            event = pygame.event.wait()

            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()

                keyval = -1

                for v, keys in self.acm.items():
                    for k in keys:
                        if pressed[k]:
                            keyval = v
                            break

                    if keyval != -1:
                        break

                if keyval != -1:
                    return keyval
                elif pressed[pygame.K_ESCAPE]:
                    #pygame.display.quit()
                    pygame.quit()
                    exit()

