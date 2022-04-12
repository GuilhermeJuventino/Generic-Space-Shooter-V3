import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super(GameObject, self).__init__()
        self.width = width
        self.height = height
        self.image = image
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
