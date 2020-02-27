"""General information on your module and what it does."""
from init import *
import sys
import pygame

def update(delta_time):
    """Update method for platform state."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop()
        elif key_down(event, " ") and (MY.grounded or MY.level_num > 1):
            MY.player.velocity.y = -800
            MY.grounded = False

    if key_held_down(pygame.K_LEFT): # move left
        MY.player.velocity.x = max(MY.player.velocity.x - PLAYER_ACCEL, -PLAYER_MAX_SPEED)
    elif key_held_down(pygame.K_RIGHT): # move right
        MY.player.velocity.x = min(MY.player.velocity.x + PLAYER_ACCEL, PLAYER_MAX_SPEED)
    else:
        if MY.grounded: # decel
            if MY.player.velocity.x > 0:
                MY.player.velocity.x = max(0, MY.player.velocity.x - PLAYER_DECEL)
            elif MY.player.velocity.x < 0:
                MY.player.velocity.x = min(0, MY.player.velocity.x + PLAYER_DECEL)
        else:
            if MY.player.velocity.x > 0:
                MY.player.velocity.x = max(0, MY.player.velocity.x - PLAYER_AIR_DECEL)
            elif MY.player.velocity.x < 0:
                MY.player.velocity.x = min(0, MY.player.velocity.x + PLAYER_AIR_DECEL)
    
    load = False
    print(MY.grounded)
    if key_held_down(pygame.K_UP):
        for door in MY.doors:
            if MY.player.collides_with(door):
                load = True

    if load is True:
        MY.level_num += 1
        if MY.level_num < 4:
            load_level("level" + str(MY.level_num))
        else:
            change(2)
        return

    # Gravity
    MY.player.velocity.y = min(MY.player.velocity.y + GRAVITY_ACCEL, PLAYER_TERMINAL_VEL)

    # Check for hazard collisions
    for hazard in MY.hazards:
        if MY.player.collides_with(hazard):
            MY.player_health -= 2
            if MY.player_health <= 0:
                change(1)
            else:
                MY.player.location = MY.player_start_position
                MY.player.set_velocity(0, 0)
                break
    for coin in MY.coins:
        if MY.player.collides_with(coin):
            MY.coins.remove(coin)
            MY.player_health += 1
    
    MY.player.update(delta_time)

    # check for wall collisions
    touching = False
    for wall in MY.walls:
        if MY.player.collides_with(wall):
            if MY.player.collision[DOWN]:
                MY.player.snap_to_object_y(wall, DOWN)
                MY.player.velocity.y = 0
                MY.grounded = touching = True
                continue
            if MY.player.collision[LEFT]:
                MY.player.snap_to_object_x(wall, LEFT)
                MY.player.velocity.x = 0
                touching = True
                continue
            if MY.player.collision[RIGHT]:
                MY.player.snap_to_object_x(wall, RIGHT)
                MY.player.velocity.x = 0
                touching = True
                continue
            if MY.player.collision[UP]:
                MY.player.snap_to_object_y(wall, UP)
                MY.player.velocity.y = 0
                touching = True
                continue
    if not touching:
        MY.grounded = False

# states
import CreeperChase
Manager.register(CreeperChase)

Manager.register(Lose)
Manager.register(Win)

# run the game!
Manager.run(SCREEN, WINDOW, BLUE)