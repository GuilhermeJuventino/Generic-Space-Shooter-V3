import pygame
from random import randrange
from enemy import Enemy


class EnemySpawner:
    def __init__(self):
        self.enemy_group = pygame.sprite.Group()
        self.spawn_timer = randrange(30, 120)

    def update(self):
        self.enemy_group.update()

        if self.spawn_timer == 0:
            self.spawn_enemy()
            self.spawn_timer = randrange(30, 120)

        self.spawn_timer -= 1

    def spawn_enemy(self):
        new_enemy = Enemy("src/images/Asteroid.png", 11, 7)
        self.enemy_group.add(new_enemy)
