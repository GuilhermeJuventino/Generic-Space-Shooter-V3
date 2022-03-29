import constants as c
from random import randrange
from asteroid import Asteroid
from object_spawner import ObjectSpawner


class AsteroidTimer:
    def __init__(self):
        self.spawner = ObjectSpawner()
        self.spawn_timer = randrange(30, 120)

    def update(self):
        self.spawner.update()

        if self.spawn_timer == 0:
            self.spawn_enemy()
            self.spawn_timer = randrange(30, 120)

        self.spawn_timer -= 1

    def spawn_enemy(self):
        x = randrange(0, c.DISPLAY_WIDTH - 11)
        new_enemy = Asteroid(c.ASTEROID, (x, 0), 11, 7)
        self.spawner.spawn(new_enemy)
