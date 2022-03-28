import pygame
from projectile import Projectile


class ObjectSpawner:
    def __init__(self):
        #self.object = object_to_spawn
        self.object_group = pygame.sprite.Group()

    def spawn(self, x, y):
        new_object = Projectile("src/images/bullet.png", (x, y), 11, 11)
        self.object_group.add(new_object)
        print("True")

    def update(self):
        self.object_group.update()
