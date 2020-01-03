"""Runs the Init.py file and imports the libraries"""
from init import *
import pygame

def update(delta_time):
    """Update method for boss battle state."""
    for event in pygame.event.get():
        # Checks if you closed the window
        if event.type == pygame.QUIT:
            stop()
    
    x_value = 0
    y_value = 0
    velocity = 200

    # Moves the player forward and backward
    if key_held_down(pygame.K_UP):
        MY.player.location.y -= velocity * delta_time
    elif key_held_down(pygame.K_DOWN):
        MY.player.location.y += velocity * delta_time

    # Moves the player left and right
    if key_held_down(pygame.K_LEFT):
        MY.player.location.x -= velocity * delta_time
    elif key_held_down(pygame.K_RIGHT):
        MY.player.location.x += velocity * delta_time

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

    if MY.player_hitbox.active and MY.boss.collides_with(MY.player_hitbox):
        MY.boss_health -= 10
        MY.player_hitbox.active = False

    update_player(delta_time)

    update_boss(delta_time)

# States
import BossBattle
Manager.register(BossBattle)

# Run the game
Manager.run(SCREEN, WINDOW, BLACK)