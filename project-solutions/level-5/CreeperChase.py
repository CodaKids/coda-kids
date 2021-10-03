#Runs the Init.py file and imports the libraries
from init import *

def update(delta_time):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop()
        elif key_down(event, " ") and (MY.grounded or MY.level_num > 1):
            MY.player.velocity.y = -700
            MY.grounded = False
    if key_held_down(pygame.K_LEFT): 
        #TODO: Uncomment the two lines below
        MY.player.velocity.x = max(MY.player.velocity.x - PLAYER_ACCEL, -PLAYER_MAX_SPEED)
        MY.player.sprite = MY.paul_run_left
    #TODO: Copy the elif statement here for the player's righthand movement
    elif key_held_down(pygame.K_RIGHT): 
        #TODO: Copy the code here to set the player's velocity 
        MY.player.velocity.x = min(MY.player.velocity.x + PLAYER_ACCEL, PLAYER_MAX_SPEED)
        #TODO: Write the code here to set Paul's righthand movement animation
        MY.player.sprite = MY.paul_run_right
    else:
        if MY.grounded: 
            #TODO: Copy the code here to track and control velocity when grounded
            if MY.player.velocity.x > 0:
                MY.player.velocity.x = max(0, MY.player.velocity.x - PLAYER_DECEL)
            elif MY.player.velocity.x < 0:
                MY.player.velocity.x = min(0, MY.player.velocity.x + PLAYER_DECEL)
            #TODO: Copy the code here to set Paul's movement to idle
            else:
                MY.player.sprite = MY.paul_idle_right
        #TODO: Write code here to track and control velocity when falling
        else:
            if MY.player.velocity.x > 0:
                MY.player.velocity.x = max(0, MY.player.velocity.x - PLAYER_AIR_DECEL)
            elif MY.player.velocity.x < 0:
                MY.player.velocity.x = min(0, MY.player.velocity.x + PLAYER_AIR_DECEL)
    
    #TODO: Write the code here to track and control velocity when flying
    if not MY.grounded:
        if MY.player.velocity.x > 0:
            MY.player.sprite = MY.paul_jetpack_right
        elif MY.player.velocity.x < 0:
            MY.player.sprite = MY.paul_jetpack_left


    #Gravity
    MY.player.velocity.y = min(MY.player.velocity.y + GRAVITY_ACCEL, PLAYER_TERMINAL_VEL)

    #Check for hazard collisions
    for hazard in MY.hazards:
        if MY.player.collides_with(hazard):
            MY.player_health -= 2
            if MY.player_health <= 0:
                change(1)
            else:
                MY.player.location = MY.player_start_position
                MY.player.set_velocity(0, 0)
                MY.player.sprite = MY.paul_pain_right
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
    
    update_level(delta_time)

# states
import CreeperChase
Manager.register(CreeperChase)

Manager.register(Lose)
Manager.register(Win)

# run the game!
Manager.run(SCREEN, WINDOW, BLUE)