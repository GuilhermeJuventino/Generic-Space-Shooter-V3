import pygame

class SoundEffects:
    def __init__(self, filename, volume=None):
        self.filename = filename
        self.volume = volume

        if not volume:
            self.volume = 1.0

        self.sound = pygame.mixer.Sound(f"{self.filename}")

    def play(self):
        pygame.mixer.Sound.play(self.sound)
        self.sound.set_volume(self.volume)