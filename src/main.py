import pygame
import constants as c
import ultracolors as color
from sys import exit
from random import randrange
from player import Player
from dweller import Dweller
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
dark_asteroid_group = pygame.sprite.Group()
dweller_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
hud_group = pygame.sprite.Group()
hud_group.add(hud)

# Sound effects.
explosion_sound = SoundEffects(c.EXPLOSION_SOUND, 0.3)
hit_hurt_sound = SoundEffects(c.HIT_HURT_SOUND, 0.6)

# Text variables.
score = 0
#font = pygame.font.Font("freesansbold.ttf", 25)
font = pygame.font.Font(c.FONT, 21)
player_death_timer = 200


def title_screen():
    global ultracolor, constants, game
    running = True

    while running:
        # Setting the framerate.
        clock.tick(c.FPS)
        keystate = pygame.key.get_pressed()
        title_text = font.render("Generic Space Shooter V3", True, color.LIGHT_GREY)
        title_text_position = (c.DISPLAY_CENTER)
        title_text_rect = title_text.get_rect(center=title_text_position)

        press_start = font.render("Press ENTER to start or ESC to quit.", True, color.LIGHT_GREY)
        press_start_position = (c.DISPLAY_WIDTH_CENTER, c.DISPLAY_HEIGHT_CENTER + 50)
        press_start_rect = press_start.get_rect(center=press_start_position)

        controlls = font.render("Move with arrow keys and shoot lasers with 'Z' key.", True, color.LIGHT_GREY)
        controlls_position = (c.DISPLAY_WIDTH_CENTER, c.DISPLAY_HEIGHT_CENTER + 120)
        controlls_rect = controlls.get_rect(center=controlls_position)

        window.fill(color.BLACK)

        window.blit(title_text, title_text_rect)
        window.blit(press_start, press_start_rect)
        window.blit(controlls, controlls_rect)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if keystate[pygame.K_RETURN]:
                running = False
                in_game()

            if keystate[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

        pygame.display.update()

def game_over():
    global score, player_death_timer
    running = True

    while running:
        # Setting the framerate.
        clock.tick(c.FPS)
        keystate = pygame.key.get_pressed()
        game_over_text = font.render(f"Game Over", True, color.LIGHT_GREY)
        game_over_text_position = c.DISPLAY_CENTER
        game_over_text_rect = game_over_text.get_rect(center=game_over_text_position)
        press_start = font.render("Press ENTER to play again or ESC to quit.", True, color.LIGHT_GREY)
        press_start_position = (c.DISPLAY_WIDTH_CENTER, c.DISPLAY_HEIGHT_CENTER + 50)
        press_start_rect = press_start.get_rect(center=press_start_position)

        window.fill(color.BLACK)

        window.blit(game_over_text, game_over_text_rect)
        window.blit(press_start, press_start_rect)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if keystate[pygame.K_RETURN]:
                asteroid_group.empty()
                asteroid_timer.asteroid_spawner.group.empty()
                dark_asteroid_group.empty()
                asteroid_timer.dark_asteroid_spawner.group.empty()
                projectile_group.empty()
                dweller_group.empty()
                score = 0
                player_death_timer = 1
                player.lives = 3
                player.invincibility_timer = 1
                player.is_alive = False
                player.is_invincible = True
                asteroid_timer.spawn_timer = randrange(30, 120)
                running = False
                in_game()

            if keystate[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

        pygame.display.update()


def in_game():
    global score, player_death_timer
    running = True
    paused = False
    pause_text = font.render(f"Paused", True, color.LIGHT_GREY)
    pause_text_position = c.DISPLAY_CENTER
    pause_text_rect = pause_text.get_rect(center=pause_text_position)

    while running:
        # Setting the framerate.
        clock.tick(c.FPS)

        window.fill(color.BLACK)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    paused = not paused

        for asteroid, colls in pygame.sprite.groupcollide(asteroid_group, projectile_group, True, True).items():

            if colls:
                hit_hurt_sound.play()
                explosion = Explosion(c.EXPLOSION, asteroid.rect.center, 30, 30)
                explosion_group.add(explosion)
                explosion_sound.play()
                score += 1

        for asteroid, colls in pygame.sprite.groupcollide(dark_asteroid_group, projectile_group, True, True).items():

            if colls:
                hit_hurt_sound.play()
                explosion = Explosion(c.EXPLOSION, asteroid.rect.center, 30, 30)
                explosion_group.add(explosion)
                dweller = Dweller(c.DWELLER, asteroid.rect.center, 20, 30, player)
                dweller_group.add(dweller)
                explosion_sound.play()
                score += 2

        for dw, colls in pygame.sprite.groupcollide(dweller_group, projectile_group, True, True).items():

            if colls:
                hit_hurt_sound.play()
                explosion = Explosion(c.EXPLOSION, dw.rect.center, 30, 30)
                explosion_group.add(explosion)
                explosion_sound.play()
                score += 5

        if score >= 999:
            score = 999

        if not player.is_invincible:

            for p, colls in pygame.sprite.groupcollide(player_group, asteroid_group, False, True).items():
                player.get_hit()

            for p, colls in pygame.sprite.groupcollide(player_group, dark_asteroid_group, False, True).items():
                player.get_hit()

            for p, colls in pygame.sprite.groupcollide(player_group, dweller_group, False, True).items():
                player.get_hit()

        if player.is_invincible:

            for asteroid, colls in pygame.sprite.groupcollide(asteroid_group, player_group, True, False).items():
                hit_hurt_sound.play()
                explosion = Explosion(c.EXPLOSION, asteroid.rect.center, 30, 30)
                explosion_group.add(explosion)
                explosion_sound.play()

            for asteroid, colls in pygame.sprite.groupcollide(dark_asteroid_group, player_group, True, False).items():
                hit_hurt_sound.play()
                explosion = Explosion(c.EXPLOSION, asteroid.rect.center, 30, 30)
                explosion_group.add(explosion)
                explosion_sound.play()

            for dw, colls in pygame.sprite.groupcollide(dweller_group, player_group, True, False).items():
                hit_hurt_sound.play()
                explosion = Explosion(c.EXPLOSION, dw.rect.center, 30, 30)
                explosion_group.add(explosion)
                explosion_sound.play()

        if player_death_timer > 0 and not player.is_alive and player.lives > 0:

            if not paused:
                player_death_timer -= 1

            if player_death_timer == 0:
                player_group.add(player)
                player.rect.center = (c.DISPLAY_WIDTH_CENTER, c.DISPLAY_BOTTOM)
                player_death_timer = 300
                player.is_alive = True

        if player.lives == 0:

            if not explosion_group and not player.explosion.group:
                running = False

        # Bringing sprite group from other classes' files into main.
        asteroid_group.add(asteroid_timer.asteroid_spawner.group)
        dark_asteroid_group.add(asteroid_timer.dark_asteroid_spawner.group)
        projectile_group.add(player.projectile.group)

        # Drawing sprite groups.
        player_group.draw(window)
        asteroid_group.draw(window)
        dark_asteroid_group.draw(window)
        projectile_group.draw(window)
        explosion_group.draw(window)
        player.explosion.group.draw(window)
        dweller_group.draw(window)

        hud_group.draw(window)

        score_text = font.render(f"Score: {score}", True, color.LIGHT_GREY)
        window.blit(score_text, (c.DISPLAY_LEFT + 98, c.DISPLAY_TOP + 33))

        lives_text = font.render(f"Lives: {player.lives}", True, color.LIGHT_GREY)
        window.blit(lives_text, (c.DISPLAY_RIGHT - 255, c.DISPLAY_TOP + 33))

        if paused:
            window.blit(pause_text, pause_text_rect)

        # Updating sprite groups.
        if not paused:
            player_group.update()
            asteroid_timer.update()
            projectile_group.update()
            explosion_group.update()
            player.explosion.group.update()
            dweller_group.update()

        pygame.display.update()


title_screen()

while True:
    game_over()
