"""General information on your module and what it does."""
import coda_kids as coda
from init import *


def update(delta_time):
    """Update method for shooter state."""
    for event in coda.event.listing():
        #Checks if you closed the window.
        if coda.event.quit_game(event):
            coda.stop()
        #If you shoot, it plays a sound.
        elif coda.event.key_down(event, " "):
            SOUND_LASER[coda.utilities.rand(0, len(SOUND_LASER) - 1)].play()
            fire_bullet(1)
        elif coda.event.key_down(event, coda.pygame.K_RETURN):
            SOUND_LASER[coda.utilities.rand(0, len(SOUND_LASER) - 1)].play()
            fire_bullet(2)
        elif coda.event.mouse_l_button_down(event):
            if MY.restart_button.collides_with_point(coda.event.mouse_position()):
                print ( "button is pressed")
                coda.state.change(0)
                MY.state = 0                

    #Process rotation movement for player 1
    if coda.event.key_held_down("a"):
        MY.player1.add_rotation(SHIP_ROTATE * delta_time)
    elif coda.event.key_held_down("d"):
        MY.player1.add_rotation(-SHIP_ROTATE * delta_time)

    #Process forward and backward movement of player 1
    if coda.event.key_held_down("w"):
        MY.player1.add_velocity(MY.player1.rotation, SHIP_ACCEL, SHIP_MAX_SPEED)
    elif coda.event.key_held_down("s"):
        MY.player1.add_velocity(MY.player1.rotation, -SHIP_ACCEL, SHIP_MAX_SPEED)

    #Process rotation movement for player 2
    if coda.event.key_held_down(coda.pygame.K_LEFT):
        MY.player2.add_rotation(SHIP_ROTATE * delta_time)
    elif coda.event.key_held_down(coda.pygame.K_RIGHT):
        MY.player2.add_rotation(-SHIP_ROTATE * delta_time)

    #Process forward and backward movement of player 2
    if coda.event.key_held_down(coda.pygame.K_UP):
        MY.player2.add_velocity(MY.player2.rotation, SHIP_ACCEL, SHIP_MAX_SPEED)
    elif coda.event.key_held_down(coda.pygame.K_DOWN):
        MY.player2.add_velocity(MY.player2.rotation, -SHIP_ACCEL, SHIP_MAX_SPEED)

    MY.player1.update(delta_time)
    MY.player2.update(delta_time)

    for i in range(len(MY.asteroids)):
        if MY.asteroids[i].active:
            MY.asteroids[i].update(delta_time)
            screen_wrap(MY.asteroids[i], MY.window)

    # Check if players are outside of the screen!
    screen_wrap(MY.player1, MY.window)
    screen_wrap(MY.player2, MY.window)

    # Update bullets
    for i in range(len(MY.bullets)):
        # ignore if not active
        if MY.bullets[i].active:
            MY.bullets[i].update(delta_time)
            # Destroy bullets that hit the screen edge.
            if screen_wrap(MY.bullets[i], MY.window):
                MY.bullets[i].active = False
                continue

            for j in range(len(MY.asteroids)):
                if MY.bullets[i].collides_with(MY.asteroids[j]):
                    MY.bullets[i].active = False
            
            #check collisions
            if MY.bullet_owner[i] == 1 and MY.bullets[i].collides_with(MY.player2):
                MY.player2_hp = MY.player2_hp - 1
                MY.bullets[i].active = False
                SOUND_EXPLOSIONS[coda.utilities.rand(0, len(SOUND_EXPLOSIONS) - 1)].play()
            elif MY.bullet_owner[i] == 2 and MY.bullets[i].collides_with(MY.player1):
                MY.player1_hp = MY.player1_hp - 1
                MY.bullets[i].active = False
                SOUND_EXPLOSIONS[coda.utilities.rand(0, len(SOUND_EXPLOSIONS) - 1)].play()

    for asteroid in MY.asteroids:
        if MY.player1.collides_with(asteroid):
            MY.player1.velocity = coda.Vector2(0, 0)

        if MY.player2.collides_with(asteroid):
            MY.player2.velocity = coda.Vector2(0, 0)

    # Check win condition
    if MY.player1_hp < 1:
        coda.state.change(2)
        MY.state = 1
        MY.display_text = coda.TextObject(coda.color.WHITE, 24, "Player 2 wins! Play again?")
        
    elif MY.player2_hp < 1:
        coda.state.change(1)
        MY.state = 2
        MY.display_text = coda.TextObject(coda.color.WHITE, 24, "Player 1 wins! Play again?")

# states
import SpaceWars
coda.state.Manager.register(SpaceWars)
import restarter1
coda.state.Manager.register(restarter1)
import restarter2
coda.state.Manager.register(restarter2)


# run the game!
coda.state.Manager.run(SCREEN, WINDOW, coda.color.BLACK)
