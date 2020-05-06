"""Runs the Init.py file and imports the libraries"""
from Init import *
import pygame

def update(delta_time):
    timer = CountdownTimer(100)   

    # Checks if player collides with the walls
    if MY.player.location.x < MY.wall_height:
        MY.player.location.x = MY.wall_height
    if MY.player.location.x > window_width - MY.wall_height:
        MY.player.location.x = window_width - MY.wall_height
    if MY.player.location.y < MY.wall_height:
        MY.player.location.y = MY.wall_height
    if MY.player.location.y > window_length - (MY.wall_height + 20):
        MY.player.location.y = window_length - (MY.wall_height + 20) 

    if MY.player.collides_with(MY.boss):
        player_pain_anim()
        MY.player_health -= 1
        MY.player_hitbox.active = False

    if MY.player_dir == UP:
        MY.player_hitbox.location = pygame.math.Vector2(MY.player.location.x + 20, MY.player.location.y - 20)
    elif MY.player_dir == DOWN:
        MY.player_hitbox.location = pygame.math.Vector2(MY.player.location.x - 10, MY.player.location.y + 25)
    elif MY.player_dir == LEFT:
        MY.player_hitbox.location = pygame.math.Vector2(MY.player.location.x - 20, MY.player.location.y)
    elif MY.player_dir == RIGHT:
        MY.player_hitbox.location = pygame.math.Vector2(MY.player.location.x + 20, MY.player.location.y)

    if MY.player_hitbox.active and MY.boss.collides_with(MY.player_hitbox):
        boss_pain_anim()
        MY.boss_health -= 1
        MY.player_hitbox.active = False

'''
    def boss_wait_init(delta_time):
        timer = CountdownTimer(3)

    def boss_wait_update(state, delta_time):
        """wait between attacks."""
        if state.timer.tick(delta_time):
            if state.previous == 0:
                state.owner.current_state = 1
            else:
                state.owner.current_state = 0

    def boss_explosion_update(state, delta_time):
        """shoot out lots of projectiles."""
        num_projectiles = 15
        fraction = 360 / num_projectiles
        count = 0
        while count < num_projectiles:
            fire_bullet(BOSS, fraction * count, 15)
            count += 1

        state.owner.current_state = 2

    def boss_laser_update(state, delta_time):
        """laser attack."""
        MY.boss.add_rotation(MY.rotation_speed * delta_time)
        fire_bullet(BOSS, MY.boss.rotation, 30)
        if MY.boss.rotation >= 355:
            MY.boss.rotation = 0
            state.owner.current_state = 2

    attack_time = timer.max_time * 5
    for i in range(attack_time):
        if timer.tick(1) == True:
            #MY.boss_attacking = True
            #print(MY.boss_attacking)
            #boss_attack(1)
        else:
            #MY.boss_attacking = False
            #print(MY.boss_attacking)
            #boss_idle_anim()

    count = -1
    for projectile in MY.projectiles:
        count += 1
        if projectile.active:
            if MY.projectile_owner[count] == BOSS and projectile.collides_with(MY.player):
                MY.player_health -= 1
                projectile.active = False
                continue
            for wall in MY.walls:
                if projectile.collides_with(wall):
                    projectile.active = False
                    continue
'''
    update_player(delta_time)

    update_boss(delta_time)

    update_projectiles(delta_time)

    check_stop()

    check_win()

# States
import BossBattle
Manager.register(BossBattle)
Manager.register(GameOver)

# Run the game
Manager.run(SCREEN, WINDOW, BLACK)