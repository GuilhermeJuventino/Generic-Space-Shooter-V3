import pygame
import constants as c
import ultracolors as color
from sys import exit
from player import Player
from asteroid_timer import AsteroidTimer
from object_collider import ObjectCollider
from sound_effects import SoundEffects
from explosion import Explosion
from hud import HUD

pygame.init()
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)

# Game window
window = pygame.display.set_mode(c.DISPLAY_SIZE)
pygame.display.set_caption("Generic Space Shooter V3")
pygame.display.set_icon(c.ICON)

# Classes.
player = Player(c.SHIP, (c.DISPLAY_WIDTH_CENTER, c.DISPLAY_BOTTOM), 26, 37)
asteroid_timer = AsteroidTimer()
collider = ObjectCollider()
hud = HUD(c.HUD, (60, c.DISPLAY_TOP + 20), 92, 14)

# Sprite groups.
player_group = pygame.sprite.Group()
player_group.add(player)
asteroid_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
hud_group = pygame.sprite.Group()
hud_group.add(hud)

# Sound effects.
explosion_sound = SoundEffects(c.EXPLOSION_SOUND, 0.3)
hit_hurt_sound = SoundEffects(c.HIT_HURT_SOUND, 0.6)

# Text variables.
score = 0
lives = 3
font = pygame.font.Font("freesansbold.ttf", 25)
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

    for asteroid, colls in pygame.sprite.groupcollide(asteroid_group, projectile_group, True, True).items():

        if colls:
            hit_hurt_sound.play()
            explosion = Explosion(c.EXPLOSION, asteroid.rect.center, 30, 30)
            explosion_group.add(explosion)
            explosion_sound.play()
            score += 1

            if score >= 999:
                score = 999

    if not player_invincible:
        for p, colls in pygame.sprite.groupcollide(player_group, asteroid_group, True, True).items():
            hit_hurt_sound.play()
            explosion = Explosion(c.EXPLOSION, p.rect.center, 30, 30)
            explosion_group.add(explosion)
            explosion_sound.play()
            lives -= 1
            player.alive = False

    if player_invincible:
        for asteroid, colls in pygame.sprite.groupcollide(asteroid_group, player_group, True, False).items():
            hit_hurt_sound.play()
            explosion = Explosion(c.EXPLOSION, asteroid.rect.center, 30, 30)
            explosion_group.add(explosion)
            explosion_sound.play()

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

    window.fill(color.BLACK)

    # Bringing sprite group from other classes' files into main.
    asteroid_group.add(asteroid_timer.spawner.group)
    projectile_group.add(player.projectile.group)

    # Drawing sprite groups.
    player_group.draw(window)
    asteroid_group.draw(window)
    projectile_group.draw(window)
    explosion_group.draw(window)

    hud_group.draw(window)

    score_text = font.render(f"Score: {score}", False, color.LIGHT_GREY)
    window.blit(score_text, (c.DISPLAY_LEFT + 98, c.DISPLAY_TOP + 39))

    lives_text = font.render(f"Lives: {lives}", False, color.LIGHT_GREY)
    window.blit(lives_text, (c.DISPLAY_RIGHT - 255, c.DISPLAY_TOP + 39))

    # Updating sprite groups.
    player_group.update()
    asteroid_timer.update()
    projectile_group.update()
    explosion_group.update()
    pygame.display.update()
