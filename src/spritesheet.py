import pygame


class Spritesheet:
    def __init__(self, image):
        self.sheet = image

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height], pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        return sprite

    def get_animation(self, x, y, width, height):
        pass
