import pygame
import constants as c
from math import sqrt, floor
from game_character import GameCharacter
from object_spawner import ObjectSpawner
from projectile import Projectile
from sound_effects import SoundEffects
from spritesheet import SpriteSheet
from explosion import Explosion


class Player(GameCharacter):
    def __init__(self, image, position, width, height):
        super().__init__(image, width, height)
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 5

        self.spritesheet = SpriteSheet(image)
        self.idle_animation = self.spritesheet.get_images(1, 5, 26, 37, scale=1.5)
        self.image = self.idle_animation[0]
        self.rect = self.image.get_rect()
        self.rect.center = position

        self.projectile = ObjectSpawner()
        self.ready = True
        self.cooldown = 300
        self.projectile_time = 0
        self.projectile_sound = SoundEffects(c.PROJECTILE_SOUND, 0.3)

        self.animation_loop = 0

        self.last_shot = pygame.time.get_ticks()

        self.is_alive = True
        self.is_invincible = False
        self.invincibility_timer = 300
        self.lives = 3

    def update(self):
        self.move_player()
        self.animate_player()
        self.recharge()
        self.invincibility()

    def get_hit(self):
        if not self.is_invincible and self.is_alive:
            self.hurt_sound.play()
            self.is_alive = False
            self.kill()
            self.new_explosion = Explosion(c.EXPLOSION, self.rect.center, 30, 30)
            self.explosion.spawn(self.new_explosion)
            self.explosion_sound.play()
            self.lives -= 1

            if self.lives <= 0:
                self.lives = 0

            self.is_invincible = True

    def invincibility(self):
        if self.is_alive and self.is_invincible:
            self.invincibility_timer -= 1

            if self.invincibility_timer <= 0:
                self.invincibility_timer = 300
                self.is_invincible = False

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.projectile_time >= self.cooldown:
                self.ready = True

    def shoot_projectile(self):
        new_projectile = Projectile(c.LASER, (self.rect.centerx, self.rect.top), 4, 15)
        self.projectile_sound.play()
        self.projectile.spawn(new_projectile)

    def animate_player(self):
        self.image = self.idle_animation[floor(self.animation_loop)]
        self.animation_loop += 0.25

        if self.animation_loop >= 5:
            self.animation_loop = 0

    def normalize_speed(self):
        self.speed_x = self.speed_x * (sqrt(2) / 2)
        self.speed_y = self.speed_y * (sqrt(2) / 2)

    def move_player(self):
        self.keystate = pygame.key.get_pressed()

        # Moving left or right.
        if self.keystate[pygame.K_RIGHT] and not self.keystate[pygame.K_LEFT]:
            self.speed_x = self.speed

        elif self.keystate[pygame.K_LEFT] and not self.keystate[pygame.K_RIGHT]:
            self.speed_x = -self.speed

        # Preventing increase of speed while moving diagonally.
        elif self.speed_x != 0 and self.speed_y != 0:
            self.normalize_speed()

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
