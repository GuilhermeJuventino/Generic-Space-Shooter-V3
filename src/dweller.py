import pygame
import constants as c
from math import sqrt
from enemy import Enemy


class Dweller(Enemy):
    def __init__(self, image, position, width, height, target):
        super(Dweller, self).__init__(image, position, width, height)
        self.image = pygame.transform.scale(self.image, (self.width * 2.7, self.height * 2.7))
        self.rect = self.image.get_rect()
        self.target = target
        self.rect.center = position
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 1

    def follow_target(self):
        if self.rect.top < self.target.rect.y:
            self.speed_y += self.speed

        elif self.rect.bottom > self.target.rect.y:
            self.speed_y += -self.speed

        if self.rect.right < self.target.rect.x:
            self.speed_x += self.speed

        elif self.rect.left > self.target.rect.x:
            self.speed_x += -self.speed

        if self.speed_x != 0 and self.speed_y != 0:
            self.normalize_speed()

        if self.rect.top <= 100:
            self.rect.top = 100

        elif self.rect.bottom >= c.DISPLAY_BOTTOM:
            self.rect.bottom = c.DISPLAY_BOTTOM

        if self.rect.left <= 0:
            self.rect.left = 0

        elif self.rect.right >= c.DISPLAY_WIDTH:
            self.rect.right = c.DISPLAY_WIDTH

    def normalize_speed(self):
        self.speed_x = self.speed_x * (sqrt(2) / 2)
        self.speed_y = self.speed_y * (sqrt(2) / 2)

    def update(self):
        self.follow_target()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
