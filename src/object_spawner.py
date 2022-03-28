import pygame


class ObjectSpawner:
    def __init__(self):
        self.group = pygame.sprite.Group()

    def spawn(self, object):
        new_object = object
        self.group.add(new_object)

    def update(self):
        self.group.update()
