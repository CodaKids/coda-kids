"""General information on your module and what it does."""
import coda
from init import *

def update(delta_time):
    """Update method for platform state."""
    for event in coda.listing():
        if coda.quit_game(event):
            coda.stop()
        elif coda.key_down(event, " ") and (MY.grounded or MY.level_num > 1):
            MY.player.velocity.y = -800
            MY.grounded = False

    if coda.key_held_down("a"): # move left
        MY.player.velocity.x = max(MY.player.velocity.x - PLAYER_ACCEL, -PLAYER_MAX_SPEED)
    elif coda.key_held_down("d"): # move right
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
    if coda.key_held_down("w"):
        for door in MY.doors:
            if MY.player.collides_with(door):
                load = True

    if load is True:
        MY.level_num += 1
        if MY.level_num < 4:
            load_level("level" + str(MY.level_num))
        else:
            coda.change(2)
        return

    # Gravity
    MY.player.velocity.y = min(MY.player.velocity.y + GRAVITY_ACCEL, PLAYER_TERMINAL_VEL)

    # Check for hazard collisions
    for hazard in MY.hazards:
        if MY.player.collides_with(hazard):
            MY.player_health -= 2
            if MY.player_health <= 0:
                coda.change(1)
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
            if MY.player.collision[coda.DOWN]:
                MY.player.snap_to_object_y(wall, coda.DOWN)
                MY.player.velocity.y = 0
                MY.grounded = touching = True
                continue
            if MY.player.collision[coda.LEFT]:
                MY.player.snap_to_object_x(wall, coda.LEFT)
                MY.player.velocity.x = 0
                touching = True
                continue
            if MY.player.collision[coda.RIGHT]:
                MY.player.snap_to_object_x(wall, coda.RIGHT)
                MY.player.velocity.x = 0
                touching = True
                continue
            if MY.player.collision[coda.UP]:
                MY.player.snap_to_object_y(wall, coda.UP)
                MY.player.velocity.y = 0
                touching = True
                continue
    if not touching:
        MY.grounded = False

# states
import CreeperChase
coda.Manager.register(CreeperChase)
import lose
coda.Manager.register(lose)
import win
coda.Manager.register(win)

# run the game!
coda.Manager.run(SCREEN, WINDOW, coda.BLUE)