import constants as c
from random import randrange
from asteroid import Asteroid
from object_spawner import ObjectSpawner


class AsteroidTimer:
    def __init__(self):
        self.asteroid_spawner = ObjectSpawner()
        self.spawn_timer = randrange(30, 120)

    def update(self):
        self.asteroid_spawner.update()

        if self.spawn_timer == 0:
            self.spawn_enemy()
            self.spawn_timer = randrange(30, 120)

        self.spawn_timer -= 1

    def spawn_enemy(self):
        new_enemy = Asteroid(c.ASTEROID, 11, 7)
        self.asteroid_spawner.spawn(new_enemy)
