"""General information on your module and what it does."""
import coda_kids as coda
from init import *

def update(delta_time):
    """Update method for platform state."""
    for event in coda.event.listing():
        if coda.event.quit_game(event):
            coda.stop()
        elif coda.event.key_down(event, " ") and (MY.grounded or MY.level_num > 1):
            MY.player.velocity.y = -800
            MY.grounded = False

    if coda.event.key_held_down("a"): # move left
        MY.player.velocity.x = max(MY.player.velocity.x - PLAYER_ACCEL, -PLAYER_MAX_SPEED)
    elif coda.event.key_held_down("d"): # move right
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
    if coda.event.key_held_down("w"):
        for door in MY.doors:
            if MY.player.collides_with(door):
                load = True

    if load is True:
        MY.level_num += 1
        if MY.level_num < 4:
            load_level("level" + str(MY.level_num))
        else:
            coda.state.change(2)
        return

    # Gravity
    MY.player.velocity.y = min(MY.player.velocity.y + GRAVITY_ACCEL, PLAYER_TERMINAL_VEL)

    # Check for hazard collisions
    for hazard in MY.hazards:
        if MY.player.collides_with(hazard):
            MY.player_health -= 2
            if MY.player_health <= 0:
                coda.state.change(1)
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
            if MY.player.collision[coda.dir.DOWN]:
                MY.player.snap_to_object_y(wall, coda.dir.DOWN)
                MY.player.velocity.y = 0
                MY.grounded = touching = True
                continue
            if MY.player.collision[coda.dir.LEFT]:
                MY.player.snap_to_object_x(wall, coda.dir.LEFT)
                MY.player.velocity.x = 0
                touching = True
                continue
            if MY.player.collision[coda.dir.RIGHT]:
                MY.player.snap_to_object_x(wall, coda.dir.RIGHT)
                MY.player.velocity.x = 0
                touching = True
                continue
            if MY.player.collision[coda.dir.UP]:
                MY.player.snap_to_object_y(wall, coda.dir.UP)
                MY.player.velocity.y = 0
                touching = True
                continue
    if not touching:
        MY.grounded = False

# states
import CreepyChase
coda.state.Manager.register(CreepyChase)
import lose
coda.state.Manager.register(lose)
import win
coda.state.Manager.register(win)

# run the game!
coda.state.Manager.run(SCREEN, WINDOW, coda.color.BLUE)