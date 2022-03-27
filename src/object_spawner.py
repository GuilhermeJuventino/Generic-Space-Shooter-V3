import pygame


class ObjectSpawner:
    def __init__(self, object_to_spawn):
        self.object = object_to_spawn
        self.object_group = pygame.sprite.Group()
        # self.surface = surface_to_spawn

    def spawn(self):
        # self.object_group = pygame.sprite.Group()
        self.object_group.add(self.object)
        print("True")

    def update(self):
        # self.object_group.draw(self.surface)
        self.object_group.update()
