import pygame
import constants as c
from random import randrange
from game_character import GameCharacter


class Enemy(GameCharacter):
    def __init__(self, image, width, height):
        super(Enemy, self).__init__(image, width, height)
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (self.width * 8, self.height * 8))
        self.rect = self.image.get_rect()
        self.rect.x = randrange(0, c.DISPLAY_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

        self.speed_x = randrange(-3, 3)
        self.speed_y = randrange(6, 8)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top > c.DISPLAY_HEIGHT:
            self.kill()

        if self.rect.left > c.DISPLAY_WIDTH or self.rect.right < 0:
            self.kill()
