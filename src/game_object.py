import pygame
from spritesheet import Spritesheet


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super(GameObject, self).__init__()
        self.width = width
        self.height = height
        self.spritesheet = Spritesheet(image)
        self.image = self.spritesheet.get_sprite(0, 0, self.width, self.height).convert_alpha()
        self.rect = self.image.get_rect()

