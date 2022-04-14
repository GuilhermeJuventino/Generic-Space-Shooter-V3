import pygame
import constants as c
from math import atan2, degrees, floor
from enemy import Enemy
from spritesheet import SpriteSheet


class Dweller(Enemy):
    def __init__(self, image, position, width, height, target):
        super().__init__(image, position, width, height)
        self.base_image = image
        self.spritesheet = SpriteSheet(self.base_image)
        self.animation = self.spritesheet.get_images(1, 5, 20, 30, scale=2.1)
        self.base_image = self.animation[0]

        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.target = target
        self.rect.center = position
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 3
        self.angle = 0
        self.rotation_speed = 0

        self.last_update = pygame.time.get_ticks()
        self.animation_loop = 0

    def follow_target(self):
        self.dirvect = pygame.math.Vector2(self.target.rect.x - self.rect.x,
                                           self.target.rect.y - self.rect.y)

        if self.dirvect.length() > 0:

            self.dirvect.normalize()
            self.dirvect.scale_to_length(self.speed)

        self.rect.move_ip(self.dirvect)

        if self.rect.top <= 100:
            self.rect.top = 100

        elif self.rect.bottom >= c.DISPLAY_BOTTOM:
            self.rect.bottom = c.DISPLAY_BOTTOM

        if self.rect.left <= 0:
            self.rect.left = 0

        elif self.rect.right >= c.DISPLAY_WIDTH:
            self.rect.right = c.DISPLAY_WIDTH

    def rotate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_update > 50:
            self.last_update = current_time
            self.angle = (self.get_angle((self.rect.x, self.rect.y), (self.target.rect.x,
                                                                      self.target.rect.y)) + self.rotation_speed) % 360
            self.image = pygame.transform.rotate(self.base_image, self.angle)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def get_angle(self, coord_1, coord_2):
        new_angle = atan2(coord_2[0] - coord_1[0], coord_2[1] - coord_1[1])
        return degrees(new_angle)

    def animate(self):
        self.base_image = self.animation[floor(self.animation_loop)]
        self.animation_loop += 0.25

        if self.animation_loop >= 5:
            self.animation_loop = 0

    def update(self):
        self.follow_target()
        self.animate()
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
