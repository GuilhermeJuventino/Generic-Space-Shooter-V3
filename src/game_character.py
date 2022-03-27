from game_object import GameObject


class GameCharacter(GameObject):
    def __init__(self, image, width, height):
        super(GameCharacter, self).__init__(image, width, height)
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
