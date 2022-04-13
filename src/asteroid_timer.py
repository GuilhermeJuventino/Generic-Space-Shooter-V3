import constants as c
from random import randrange
from asteroid import Asteroid
from dark_asteroid import DarkAsteroid
from object_spawner import ObjectSpawner


class AsteroidTimer:
    def __init__(self):
        self.asteroid_spawner = ObjectSpawner()
        self.dark_asteroid_spawner = ObjectSpawner()
        self.spawn_timer = randrange(30, 120)

    def update(self):
        self.asteroid_spawner.update()
        self.dark_asteroid_spawner.update()

        if self.spawn_timer == 0:
            self.spawn_enemy()
            self.spawn_timer = randrange(30, 120)

        self.spawn_timer -= 1

    def spawn_enemy(self):
        asteroid_value1 = randrange(0, 6)
        asteroid_value2 = randrange(0, 6)

        if asteroid_value1 == 0 or asteroid_value2 == 0:
            for i in range(randrange(1, 2)):
                dark_asteroid_x = randrange(0, c.DISPLAY_WIDTH - 11)
                new_enemy = DarkAsteroid(c.DARK_ASTEROID, (dark_asteroid_x, 0), 28, 20)
                self.dark_asteroid_spawner.spawn(new_enemy)

        else:
            for i in range(randrange(1, 3)):
                asteroid_x = randrange(0, c.DISPLAY_WIDTH - 11)
                new_enemy = Asteroid(c.ASTEROID, (asteroid_x, 0), 28, 20)
                self.asteroid_spawner.spawn(new_enemy)
