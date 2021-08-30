#Runs the Init.py file and imports the libraries
import BossBattle
from init import *

def update(delta_time):
    # Checks if player collides with the walls
    if MY.player.location.x < MY.wall_height:
        MY.player.location.x = MY.wall_height
    if MY.player.location.x > WINDOW_WIDTH - MY.wall_height:
        MY.player.location.x = WINDOW_WIDTH - MY.wall_height
    #TODO: Uncomment Lines 12-13 to make sure that Paul doesn't walk through the wall on the top of the screen
    if MY.player.location.y < MY.wall_height:
        MY.player.location.y = MY.wall_height
    #TODO: Copy the code here to make sure that Paul doesn't walk through the wall on the bottom of the screen.
    if MY.player.location.y > WINDOW_LENGTH - (MY.wall_height + 15):
        MY.player.location.y = WINDOW_LENGTH - (MY.wall_height + 15)

    handle_pillar_collision()

    #TODO: Copy the code here for Paul to lose health if he collides with the Creeper
    if MY.player.collides_with(MY.boss):
        player_pain_anim()
        MY.player_health -= 1
        MY.player_hitbox.active = False

    if MY.player_dir == UP:
        MY.player_hitbox.location = pygame.math.Vector2(
            MY.player.location.x + 20, MY.player.location.y - 20)
    #TODO: Copy the code here, to add the hit box below Paul
    elif MY.player_dir == DOWN:
        MY.player_hitbox.location = pygame.math.Vector2(
            MY.player.location.x - 10, MY.player.location.y + 25)
    elif MY.player_dir == LEFT:
        MY.player_hitbox.location = pygame.math.Vector2(
            MY.player.location.x - 20, MY.player.location.y)
    elif MY.player_dir == RIGHT:
        MY.player_hitbox.location = pygame.math.Vector2(
            MY.player.location.x + 20, MY.player.location.y)

    if MY.player_hitbox.active and MY.boss.collides_with(MY.player_hitbox):
        MY.boss_health -= 1
        MY.player_hitbox.active = False

    player_attack_update()

    update_assets(delta_time)
    
    check_win()

    check_events()

# States
Manager.register(BossBattle)
Manager.register(GameOver)
Manager.register(PlayAgain)

# Run the game
Manager.run(SCREEN, WINDOW, BLACK)
