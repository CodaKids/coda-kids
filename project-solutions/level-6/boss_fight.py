"""General information on your module and what it does."""
import coda_kids as coda

#load sprites constants
BOSS_IMAGE = coda.Image("boss.png")
PROJECTILE_IMAGE = coda.Image("projectile.png")
PLAYER_ATTACK_1_IMAGE = coda.Image("attack_1.png")
PLAYER_ATTACK_2_IMAGE = coda.Image("attack_2.png")
PLAYER_ATTACK_3_IMAGE = coda.Image("attack_3.png")

#constants
PLAYER = 0
BOSS = 1
GRASS = 4
TILE_SIZE = 32

class Data:
    """Modifiable data"""
    tilesheet = coda.SpriteSheet("tileset.png", (32, 32))
    player_sheet = coda.SpriteSheet("player_sheet.png", (42, 48))
    tilemap = []
    floors = []
    walls = []
    player_start_position = coda.Vector2(0, 0)
    boss_start_position = coda.Vector2(0, 0)
    player = coda.Object(tilesheet.image_at(0))
    boss = coda.Object(BOSS_IMAGE)
    player_health = 100
    boss_health = 300
    player_dir = coda.dir.UP
    timer1 = coda.CountdownTimer(0.1)
    timer3 = coda.CountdownTimer(0.1)
    numberOfBullets = 0
    bullets = []
    bullet_owner = []
    rotation_speed = 180
    state = 0
    last_state = 2
    player_text = coda.TextObject(coda.color.BLACK, 24, "Player: ")
    player_hitbox = coda.Object(PROJECTILE_IMAGE)
    index = 0
    boss_logic = coda.StateMachine()
    player_logic = coda.StateMachine()

MY = Data()

def health_bar(screen, health, max_health, max_size, location):
    """Creates a health bar at the given position."""
    if health > max_health - max_health * 0.25:
        bar_color = coda.color.GREEN
    elif health > max_health - max_health * 0.5:
        bar_color = coda.color.YELLOW
    else:
        bar_color = coda.color.RED

    width = max_size[0] * (health / max_health)
    coda.draw_rect(screen, bar_color, location, (width, max_size[1]))

def load_level(level_name_as_string):
    """Cleans up resources and loads a specified level. Can be used to reload the same level."""
    cleanup()
    MY.tilemap = coda.utilities.read_file(level_name_as_string + ".txt")
    obj = MY.player
    for row in range(len(MY.tilemap)):
        for column in range(len(MY.tilemap[row])):
            tile_value = int(MY.tilemap[row][column])
            obj = coda.Object(MY.tilesheet.image_at(tile_value))
            obj.location = coda.Vector2(column * TILE_SIZE + 16, row * TILE_SIZE + 16)
            if tile_value == GRASS:
                MY.floors.append(obj)
            else:
                MY.walls.append(obj)

def fire_bullet(player_number, degrees, speed):
    """fire a bullet for the player"""
    index = -1
    for i in range(len(MY.bullets)):
        if not MY.bullets[i].active:
            index = i
            break
    if index >= 0:
        MY.bullets[index].active = True
        if player_number == 1:
            MY.bullets[index].location = MY.boss.location
            MY.bullets[index].set_velocity(degrees, speed)
        else:
            MY.bullets[index].location = MY.player.location
            MY.bullets[index].set_velocity(degrees, speed)
        MY.bullet_owner[index] = player_number

def boss_wait_init(state, delta_time):
    state.timer = coda.CountdownTimer(3)
    state.previous = state.owner.previous_state

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

def player_attack_init(state, delta_time):
    state.timer = coda.CountdownTimer(0.2)
    MY.player_hitbox.active = True

def player_attack_update(state, delta_time):
    if state.timer.tick(delta_time):
        state.owner.current_state = 0
        MY.player_hitbox.active = False
    if state.timer.current_time > state.timer.max_time * 0:
        MY.player.sprite = PLAYER_ATTACK_1_IMAGE
    if state.timer.current_time > state.timer.max_time * 1/3:
        MY.player.sprite = PLAYER_ATTACK_2_IMAGE
    if state.timer.current_time > state.timer.max_time * 2/3:
        MY.player.sprite = PLAYER_ATTACK_3_IMAGE

def player_move_init(state, delta_time):
    state.timer = coda.CountdownTimer(0.1)
    state.index = 0
    state.offset = 0

def player_move_update(state, delta_time):
    if coda.event.key_held_down("w"):
        MY.player.location.y -= 200 * delta_time
        MY.player_dir = coda.dir.UP
        state.offset = 0
    elif coda.event.key_held_down("s"):
        MY.player.location.y += 200 * delta_time
        MY.player_dir = coda.dir.DOWN
        state.offset = 6

    if coda.event.key_held_down("a"):
        MY.player.location.x -= 200 * delta_time
        MY.player_dir = coda.dir.LEFT
        state.offset = 4
    elif coda.event.key_held_down("d"):
        MY.player.location.x += 200 * delta_time
        MY.player_dir = coda.dir.RIGHT
        state.offset = 2

    moving = (coda.event.key_held_down("d") or coda.event.key_held_down("a") or
              coda.event.key_held_down("s") or coda.event.key_held_down("w"))

    if moving and state.timer.tick(delta_time):
        state.index = (state.index + 1) % 2
        state.timer = coda.CountdownTimer(0.1)
    elif not moving:
        state.timer = coda.CountdownTimer(0.1)

    MY.player.sprite = MY.player_sheet.image_at(state.index + state.offset)

def initialize(window):
    """Initializes the Introduction class."""
    MY.boss_logic.add_state(None, boss_explosion_update)
    MY.boss_logic.add_state(None, boss_laser_update)
    MY.boss_logic.add_state(boss_wait_init, boss_wait_update)

    MY.player_logic.add_state(player_move_init, player_move_update)
    MY.player_logic.add_state(player_attack_init, player_attack_update)

    load_level("level1")
    MY.player.location = (window.x / 2, window.y / 4)
    MY.boss.location = window / 2
    count = 0
    while count < 100:
        MY.bullets.append(coda.Object(PROJECTILE_IMAGE))
        MY.bullet_owner.append(BOSS)
        count += 1

def update(delta_time):
    """Update method for boss battle state."""
    for event in coda.event.listing():
        if coda.event.quit_game(event):
            coda.stop()
        elif coda.event.key_down(event, " "):
            MY.player_logic.current_state = 1

    x_value = 0
    y_value = 0
    temp = 35

    MY.boss_logic.update(delta_time)
    MY.player_logic.update(delta_time)

    if MY.player_dir == coda.dir.UP:
        x_value = MY.player.location.x
        y_value = MY.player.location.y - temp
    elif MY.player_dir == coda.dir.DOWN:
        x_value = MY.player.location.x
        y_value = MY.player.location.y + temp
    elif MY.player_dir == coda.dir.LEFT:
        x_value = MY.player.location.x - temp
        y_value = MY.player.location.y
    elif MY.player_dir == coda.dir.RIGHT:
        x_value = MY.player.location.x + temp
        y_value = MY.player.location.y

    MY.player_hitbox.location = coda.Vector2(x_value, y_value)

    for wall in MY.walls:
        if MY.player.collides_with(wall):
            if MY.player.collision[coda.dir.DOWN]:
                MY.player.snap_to_object_y(wall, coda.dir.DOWN)
                continue
            if MY.player.collision[coda.dir.LEFT]:
                MY.player.snap_to_object_x(wall, coda.dir.LEFT)
                continue
            if MY.player.collision[coda.dir.RIGHT]:
                MY.player.snap_to_object_x(wall, coda.dir.RIGHT)
                continue
            if MY.player.collision[coda.dir.UP]:
                MY.player.snap_to_object_y(wall, coda.dir.UP)
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

def draw(screen):
    """Draws the state to the given screen."""
    for floor in MY.floors:
        floor.draw(screen)

    for wall in MY.walls:
        wall.draw(screen)

    for bullet in MY.bullets:
        if  bullet.active:
            bullet.draw(screen)

    MY.player.draw(screen)
    if MY.player_hitbox.active:
        MY.player_hitbox.draw(screen)

    MY.boss.draw(screen)
    MY.player_text.draw(screen)
    health_bar(screen, MY.player_health, 100, (100, 20), (70, 30))
    health_bar(screen, MY.boss_health, 300, (MY.boss.width(), 20), MY.boss.location - (MY.boss.width() / 2, MY.boss.height() / 2))

def cleanup():
    """Cleans up the Intro State."""

