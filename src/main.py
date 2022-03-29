import pygame
import constants as c
import ultracolors as color
from sys import exit
from player import Player
from asteroid_timer import AsteroidTimer
from object_collider import ObjectCollider

pygame.init()
clock = pygame.time.Clock()

# Game window
window = pygame.display.set_mode(c.DISPLAY_SIZE)

# Classes.
player = Player(c.SHIP, (c.DISPLAY_WIDTH_CENTER, c.DISPLAY_BOTTOM), 26, 37)
asteroid_timer = AsteroidTimer()
collider = ObjectCollider()

# Sprite groups.
player_group = pygame.sprite.Group()
player_group.add(player)

while True:
    # Setting the framerate.
    clock.tick(c.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if collider.check_collision(player.projectile.group, asteroid_timer.spawner.group):
        pygame.sprite.groupcollide(player.projectile.group, asteroid_timer.spawner.group, True, True)

    if collider.check_collision(player_group, asteroid_timer.spawner.group):
        pygame.sprite.groupcollide(player_group, asteroid_timer.spawner.group, True, True)

    # Refreshing the screen.
    window.fill(color.BLACK)

    # Drawing sprite groups.
    player_group.draw(window)
    asteroid_timer.spawner.group.draw(window)
    player.projectile.group.draw(window)

    # Updating sprite groups.
    player_group.update()
    asteroid_timer.update()
    pygame.display.update()
