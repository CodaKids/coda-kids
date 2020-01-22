"""Runs the Init.py file and imports the libraries"""
from init import *
import pygame

def update(delta_time):
    MY.player_hitbox.location = pygame.math.Vector2(x_value, y_value)

    for wall in MY.walls:
        if MY.player.collides_with(wall):
            if MY.player.collision[DOWN]:
                MY.player.snap_to_object_y(wall, DOWN)
                continue
            if MY.player.collision[LEFT]:
                MY.player.snap_to_object_x(wall, LEFT)
                continue
            if MY.player.collision[RIGHT]:
                MY.player.snap_to_object_x(wall, RIGHT)
                continue
            if MY.player.collision[UP]:
                MY.player.snap_to_object_y(wall, UP)
                continue
    
    if key_held_down(pygame.K_SPACE):
        pass

    if MY.player_hitbox.active and MY.boss.collides_with(MY.player_hitbox):
        MY.boss_health -= 10
        MY.player_hitbox.active = False

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

# States
import BossBattle
Manager.register(BossBattle)

# Run the game
Manager.run(SCREEN, WINDOW, BLACK)