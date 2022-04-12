import constants as c
from game_object import GameObject
from object_spawner import ObjectSpawner
from explosion import Explosion
from sound_effects import SoundEffects


class GameCharacter(GameObject):
    def __init__(self, image, width, height):
        super().__init__(image, width, height)
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 5

        self.explosion = ObjectSpawner()

        self.hurt_sound = SoundEffects(c.HIT_HURT_SOUND, 0.6)
        self.explosion_sound = SoundEffects(c.EXPLOSION_SOUND, 0.3)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def get_hit(self):
        self.hurt_sound.play()
        self.kill()
        self.new_explosion = Explosion(c.EXPLOSION, self.rect.center, 30, 30)
        self.explosion.spawn(self.new_explosion)
        self.explosion_sound.play()
