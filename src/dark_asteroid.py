from asteroid import Asteroid


class DarkAsteroid(Asteroid):
    def __init__(self, image, position, width, height):
        super(DarkAsteroid, self).__init__(image, position, width, height)

    def update(self):
        super(DarkAsteroid, self).update()
