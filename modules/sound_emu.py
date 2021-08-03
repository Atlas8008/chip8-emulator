import pygame

from pygame import midi

midi.init()


class SoundEmulator:
    def __init__(self):
        self.default_id = midi.get_default_output_id()
        self.midi_out = midi.Output(device_id=self.default_id)
        self.midi_out.set_instrument(82)

    def sound_on(self):
        self.midi_out.note_on(72, 127)

    def sound_off(self):
        self.midi_out.note_off(72, 127)