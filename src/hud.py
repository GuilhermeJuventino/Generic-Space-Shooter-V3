import pygame
from game_object import GameObject


class HUD(GameObject):
    def __init__(self, image, position, width, height):
        super(HUD, self).__init__(image, width, height)
        self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width * 9, self.rect.height * 6))
        self.rect.center = position
