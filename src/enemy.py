import constants as c
from game_character import GameCharacter


class Enemy(GameCharacter):
    def __init__(self, image, position, width, height):
        super().__init__(image, width, height)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        super().update()
        if self.rect.top > c.DISPLAY_HEIGHT:
            self.kill()

        if self.rect.left > c.DISPLAY_WIDTH or self.rect.right < 0:
            self.kill()
