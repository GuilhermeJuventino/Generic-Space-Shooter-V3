import pygame
import constants as c
import ultracolors as color
from sys import exit
from player import Player
from asteroid_timer import AsteroidTimer
from object_collider import ObjectCollider
from src.sound_effects import SoundEffects

pygame.init()
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)

# Game window
window = pygame.display.set_mode(c.DISPLAY_SIZE)

# Classes.
player = Player(c.SHIP, (c.DISPLAY_WIDTH_CENTER, c.DISPLAY_BOTTOM), 26, 37)
asteroid_timer = AsteroidTimer()
collider = ObjectCollider()

# Sprite groups.
player_group = pygame.sprite.Group()
player_group.add(player)

# Sound effects.
explosion = SoundEffects(c.EXPLOSION_SOUND, 0.3)
hit_hurt = SoundEffects(c.HIT_HURT_SOUND, 0.6)

# Text variables.
score = 0
lives = 3
font = pygame.font.Font("freesansbold.ttf", 32)
player_death_timer = 200
player_invincibility_timer = 300
player_invincible = False

while True:
    # Setting the framerate.
    clock.tick(c.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if collider.check_collision(player.projectile.group, asteroid_timer.spawner.group):
        pygame.sprite.groupcollide(player.projectile.group, asteroid_timer.spawner.group, True, True)
        hit_hurt.play()
        explosion.play()
        score += 1

    if collider.check_collision(player_group, asteroid_timer.spawner.group) and not player_invincible:
        pygame.sprite.groupcollide(player_group, asteroid_timer.spawner.group, True, True)
        player.projectile.group.empty()
        hit_hurt.play()
        explosion.play()
        lives -= 1
        player.alive = False

        if player_invincible:
            pygame.sprite.groupcollide(player_group, asteroid_timer.spawner.group, False, True)

        if lives <= 0:
            lives = 0

    if player_death_timer > 0 and not player.alive:
        player_death_timer -= 1
        if player_death_timer == 0:
            player_group.add(player)
            player.rect.center = (c.DISPLAY_WIDTH_CENTER, c.DISPLAY_BOTTOM)
            player_death_timer = 300
            player.alive = True
            player_invincible = True

    if player_invincible:
        player_invincibility_timer -= 1

        if player_invincibility_timer == 0:
            player_invincible = False
            player_invincibility_timer = 200

    # Refreshing the screen.
    window.fill(color.BLACK)

    # Drawing sprite groups.
    player_group.draw(window)

    asteroid_timer.spawner.group.draw(window)
    player.projectile.group.draw(window)

    score_text = font.render(f"Score: {score}", False, color.LIGHT_GREY)
    window.blit(score_text, (c.DISPLAY_LEFT + 30, c.DISPLAY_TOP + 20))

    lives_text = font.render(f"Lives: {lives}", False, color.LIGHT_GREY)
    window.blit(lives_text, (c.DISPLAY_RIGHT - 160, c.DISPLAY_TOP + 20))

    # Updating sprite groups.
    player_group.update()
    asteroid_timer.update()
    pygame.display.update()
