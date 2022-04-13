import pygame
import constants as c
from enemy import Enemy


class Dweller(Enemy):
    def __init__(self, image, position, width, height, target):
        super().__init__(image, position, width, height)
        self.image = pygame.transform.scale(self.image, (self.width * 2.7, self.height * 2.7))
        self.rect = self.image.get_rect()
        self.target = target
        self.rect.center = position
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 3

    def follow_target(self):
        dirvect = pygame.math.Vector2(self.target.rect.x - self.rect.x,
                                      self.target.rect.y - self.rect.y)

        if dirvect.length() > 0:

            dirvect.normalize()
            dirvect.scale_to_length(self.speed)

        self.rect.move_ip(dirvect)

        if self.rect.top <= 100:
            self.rect.top = 100

        elif self.rect.bottom >= c.DISPLAY_BOTTOM:
            self.rect.bottom = c.DISPLAY_BOTTOM

        if self.rect.left <= 0:
            self.rect.left = 0

        elif self.rect.right >= c.DISPLAY_WIDTH:
            self.rect.right = c.DISPLAY_WIDTH

    def update(self):
        self.follow_target()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
