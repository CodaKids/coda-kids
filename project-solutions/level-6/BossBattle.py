"""Runs the Init.py file and imports the libraries"""
import BossBattle
from init import *

def update(delta_time):
    # Checks if player collides with the walls
    if MY.player.location.x < MY.wall_height:
        MY.player.location.x = MY.wall_height
    if MY.player.location.x > WINDOW_WIDTH - MY.wall_height:
        MY.player.location.x = WINDOW_WIDTH - MY.wall_height
    if MY.player.location.y < MY.wall_height:
        MY.player.location.y = MY.wall_height
    if MY.player.location.y > WINDOW_LENGTH - (MY.wall_height + 20):
        MY.player.location.y = WINDOW_LENGTH - (MY.wall_height + 20)

    if MY.player.collides_with(MY.boss):
        player_pain_anim()
        MY.player_health -= 1
        MY.player_hitbox.active = False

    if MY.player_dir == UP:
        MY.player_hitbox.location = pygame.math.Vector2(
            MY.player.location.x + 20, MY.player.location.y - 20)
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

    update_player(delta_time)

    update_boss(delta_time)

    check_win()

    check_events()

# States
Manager.register(BossBattle)
Manager.register(GameOver)

# Run the game
Manager.run(SCREEN, WINDOW, BLACK)
