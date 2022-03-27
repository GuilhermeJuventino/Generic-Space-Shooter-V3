import pygame
import constants as c
import ultracolors as color
from sys import exit
from player import Player
# from projectile import Projectile
from enemy_spawner import EnemySpawner
# from object_spawner import ObjectSpawner

pygame.init()
clock = pygame.time.Clock()

# Game window
window = pygame.display.set_mode(c.DISPLAY_SIZE)

# Classes.
player = Player("src/spritesheets/Spaceship2.png", (c.DISPLAY_WIDTH_CENTER, c.DISPLAY_BOTTOM), 26, 37)
enemy_spawner = EnemySpawner()

# Sprite groups.
player_group = pygame.sprite.Group()
player_group.add(player)

while True:
    clock.tick(c.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    window.fill(color.BLACK)

    # Drawing sprite groups.
    player_group.draw(window)
    enemy_spawner.enemy_group.draw(window)
    player.projectile_group.draw(window)

    # Updating sprite groups.
    player_group.update()
    enemy_spawner.update()
    pygame.display.update()
