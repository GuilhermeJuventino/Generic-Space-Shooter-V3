import pygame
from random import randrange
from enemy import Enemy


class Asteroid(Enemy):
    def __init__(self, image, position, width, height):
        super().__init__(image, position, width, height)
        self.base_image = image
        self.base_image = pygame.transform.scale(self.base_image, (self.width * 2.3, self.height * 2.3)).convert_alpha()
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = 95
        self.speed_x = randrange(-3, 3)
        self.speed_y = randrange(1, 4)
        self.angle = 0
        self.rotation_speed = randrange(-7, 7)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_update > 50:
            self.last_update = current_time
            self.angle = (self.angle + self.rotation_speed) % 360
            self.image = pygame.transform.rotate(self.base_image, self.angle)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        super().update()
        self.rotate()
