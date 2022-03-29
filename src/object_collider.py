import pygame


class ObjectCollider:

    @staticmethod
    def check_collision(a, b):
        collide = pygame.sprite.groupcollide(a, b, False, False)
        if collide:
            return True

        return False
