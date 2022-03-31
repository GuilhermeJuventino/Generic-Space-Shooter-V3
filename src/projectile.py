import pygame
from game_object import GameObject


class Projectile(GameObject):
    def __init__(self, image, position, width, height):
        super(Projectile, self).__init__(image, width, height)
        self.speed_y = 10
        self.rect.center = position

    def update(self):
        self.rect.y -= self.speed_y

        if self.rect.bottom < 100:
            self.kill()
