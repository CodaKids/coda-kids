"""Runs the Init.py file and imports the libraries"""
from init import *
import pygame

def update(delta_time):
    # Checks if player collides with the walls
    if MY.player.location.x < MY.wall_height:
        MY.player.location.x = MY.wall_height
    if MY.player.location.x > window_width - MY.wall_height:
        MY.player.location.x = window_width - MY.wall_height
    if MY.player.location.y < MY.wall_height:
        MY.player.location.y = MY.wall_height
    if MY.player.location.y > window_length - (MY.wall_height + 20):
        MY.player.location.y = window_length - (MY.wall_height + 20)

    MY.player_hitbox.location = pygame.math.Vector2(MY.player.location.x, MY.player.location.y)
    timer = CountdownTimer(0.2)
    MY.player_hitbox.active = True

    if MY.player_hitbox.active and MY.boss.collides_with(MY.player_hitbox):
        MY.boss_health -= 1
        MY.player_hitbox.active = False
    
    if key_held_down(pygame.K_SPACE):
        if timer.tick(delta_time):
            MY.player_hitbox.active = False
        if timer.current_time > timer.max_time * 0:
            player_attack(delta_time)
        if timer.current_time > timer.max_time * 1/3:
            player_attack(delta_time)
        if timer.current_time > timer.max_time * 2/3:
            player_attack(delta_time)

    count = -1
    for bullet in MY.bullets:
        count += 1
        if bullet.active:
            if MY.bullet_owner[count] == BOSS and bullet.collides_with(MY.player):
                MY.player_health -= 5
                bullet.active = False
                continue
            elif MY.bullet_owner[count] == PLAYER and bullet.collides_with(MY.boss):
                MY.boss_health -= 5
                bullet.active = False
                continue
            for wall in MY.walls:
                if bullet.collides_with(wall):
                    bullet.active = False
                    continue

    update_player(delta_time)

    check_stop()

    check_win()

# States
import BossBattle
Manager.register(BossBattle)
Manager.register(GameOver)

# Run the game
Manager.run(SCREEN, WINDOW, BLACK)