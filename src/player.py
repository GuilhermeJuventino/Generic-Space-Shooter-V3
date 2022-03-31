import pygame
import constants as c
from math import sqrt, floor
from game_character import GameCharacter
from object_spawner import ObjectSpawner
from projectile import Projectile
from src.sound_effects import SoundEffects


class Player(GameCharacter):
    def __init__(self, image, position, width, height):
        super(Player, self).__init__(image, width, height)
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 5

        self.image = pygame.transform.scale(self.image, (self.width * 2, self.height * 2))
        self.rect = self.image.get_rect()
        self.rect.center = position

        self.idle_animation = [self.spritesheet.get_sprite(0, 0, self.width, self.height).convert_alpha(),
                               self.spritesheet.get_sprite(26, 0, self.width, self.height).convert_alpha(),
                               self.spritesheet.get_sprite(52, 0, self.width, self.height).convert_alpha(),
                               self.spritesheet.get_sprite(78, 0, self.width, self.height).convert_alpha(),
                               self.spritesheet.get_sprite(104, 0, self.width, self.height).convert_alpha()]

        self.projectile = ObjectSpawner()
        self.ready = True
        self.cooldown = 300
        self.projectile_time = 0
        self.projectile_sound = SoundEffects(c.PROJECTILE_SOUND, 0.3)

        self.animation_loop = 0

        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.move_player()
        self.animate_player()
        self.recharge()
        self.projectile.update()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.projectile_time >= self.cooldown:
                self.ready = True

    def shoot_projectile(self):
        new_projectile = Projectile(c.PROJECTILE, (self.rect.centerx, self.rect.top), 11, 11)
        self.projectile_sound.play()
        self.projectile.spawn(new_projectile)

    def animate_player(self):
        for i in range(0, 5):
            self.idle_animation[i] = pygame.transform.scale(self.idle_animation[i], (self.width * 2, self.height * 2))

        self.image = self.idle_animation[floor(self.animation_loop)]
        self.animation_loop += 0.25

        if self.animation_loop >= 5:
            self.animation_loop = 0

    def move_player(self):
        self.keystate = pygame.key.get_pressed()

        # Moving left or right.
        if self.keystate[pygame.K_RIGHT] and not self.keystate[pygame.K_LEFT]:
            self.speed_x = self.speed

        elif self.keystate[pygame.K_LEFT] and not self.keystate[pygame.K_RIGHT]:
            self.speed_x = -self.speed

        # Preventing increase of speed while moving diagonally.
        elif self.speed_x != 0 and self.speed_y != 0:
            self.speed_x = self.speed_x * (sqrt(2) / 2)
            self.speed_y = self.speed_y * (sqrt(2) / 2)

        else:
            self.speed_x = 0

        # Moving up or down.
        if self.keystate[pygame.K_DOWN]:
            self.speed_y = self.speed

        elif self.keystate[pygame.K_UP]:
            self.speed_y = -self.speed

        else:
            self.speed_y = 0

        if self.keystate[pygame.K_z] and self.ready:
            self.shoot_projectile()
            self.ready = False
            self.projectile_time = pygame.time.get_ticks()

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Preventing player from leaving the screen.
        if self.rect.top <= 100:
            self.rect.top = 100

        elif self.rect.bottom >= c.DISPLAY_BOTTOM:
            self.rect.bottom = c.DISPLAY_BOTTOM

        if self.rect.left <= 0:
            self.rect.left = 0

        elif self.rect.right >= c.DISPLAY_WIDTH:
            self.rect.right = c.DISPLAY_WIDTH
