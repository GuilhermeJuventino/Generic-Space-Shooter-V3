from math import floor
from game_object import GameObject
from spritesheet import SpriteSheet


class Explosion(GameObject):
    def __init__(self, image, position, width, height):
        super(Explosion, self).__init__(image, width, height)
        self.spritesheet = SpriteSheet(image)
        self.animation = self.spritesheet.get_images(1, 6, 30, 30)
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.rect.center = position

        self.animation_loop = 0

    def animate(self):
        self.image = self.animation[floor(self.animation_loop)]
        self.animation_loop += 0.25

        if self.animation_loop >= 6:
            self.kill()

    def update(self):
        self.animate()
