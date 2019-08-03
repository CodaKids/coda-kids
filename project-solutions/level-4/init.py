import coda_kids as coda

# setup
WINDOW = coda.Vector2(900, 500)
SCREEN = coda.start(WINDOW, "Space Wars Tournament")

#load sprites
IMAGE_BACKGROUND = coda.Image("assets/background.jpg")
IMAGE_PLAYER1 = coda.Image("assets/player1.png")
IMAGE_PLAYER2 = coda.Image("assets/player2.png")
IMAGE_ASTEROID = coda.Image("assets/asteroid.png")
IMAGE_ASTEROID_2 = coda.Image("assets/asteroid2.png")
SOUND_EXPLOSIONS = [coda.Sound("assets/Explosion1.wav"),
                    coda.Sound("assets/Explosion2.wav")]

SOUND_LASER = [coda.Sound("assets/Laser_Shoot1.wav"),
               coda.Sound("assets/Laser_Shoot2.wav")]

SPRITESHEET_PROJECTILE = [None,
                          coda.SpriteSheet("assets/player1_projectile.png", (36, 24)),
                          coda.SpriteSheet("assets/player2_projectile.png", (48, 48))]
PROJECTILE_ANIMATION = [None,
                        coda.Animator(SPRITESHEET_PROJECTILE[1], 0.4),
                        coda.Animator(SPRITESHEET_PROJECTILE[2], 0.4)]
IMAGE_GAMEOVER = coda.Image("assets/GameOverBackground.png")
IMAGE_BUTTON = coda.Image("assets/button.png")

# constants
SHIP_ROTATE = 120
SHIP_MAX_SPEED = 500
SHIP_ACCEL = 10
BULLET_SPEED = 1000
PLAYER_MAX_HP = 10

# setup
WINDOW = coda.Vector2(900, 500)
SCREEN = coda.start(WINDOW, "Space Wars Tournament")

class Data:
    """place changable state variables here."""
    player1 = coda.Object(IMAGE_PLAYER1)
    player1_hp = 1
    player2 = coda.Object(IMAGE_PLAYER2)
    player2_hp = 1
    bullets = []
    asteroids = []
    bullet_owner = []
    maxFrameTime = 0.05
    window = coda.Vector2(10, 10)
    background = coda.Object(IMAGE_BACKGROUND)
    """place changable state variables here."""
    gameoverbackground = coda.Object(IMAGE_GAMEOVER)
    restart_button = coda.Object(IMAGE_BUTTON)
    display_text = coda.TextObject(coda.color.WHITE, 24, "")
    state = 0

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

def screen_wrap(obj, window):
    """Wraps a given framework object around the screen, returns true if object is at edge."""
    flag = False

    # Wrap X direction
    if obj.location.x > window.x:
        obj.location.x = 0
        flag = True
    elif obj.location.x < 0:
        obj.location.x = window.x
        flag = True

    # Wrap Y direction
    if obj.location.y > window.y:
        obj.location.y = 0
        flag = True
    elif obj.location.y < 0:
        obj.location.y = window.y
        flag = True

    return flag

def initialize(window):
    """Initializes the shooter class."""
    MY.player1.location = window / 4
    MY.player1.rotation = 90
    MY.player1.set_velocity(MY.player1.rotation, 0)
    MY.player1_hp = PLAYER_MAX_HP
    MY.player2.location = window - window / 4
    MY.player2.rotation = -90
    MY.player2.set_velocity(MY.player2.rotation, 0)
    MY.player2_hp = PLAYER_MAX_HP
    count = 0
    MY.window = window
    MY.background.location = window / 2
    if MY.state!=0:
        MY.gameoverbackground.location = window / 2
        MY.restart_button.location = window / 2
        MY.display_text = coda.TextObject(coda.color.WHITE, 24, "")
    while count < 20:
        MY.bullets.append(coda.Object(PROJECTILE_ANIMATION[1]))
        MY.bullet_owner.append(1)
        count = count + 1

    count = 0
    while count < 5:
        if (coda.utilities.rand(0, 1) == 0):
            image = IMAGE_ASTEROID
        else:
            image = IMAGE_ASTEROID_2
        obj = coda.Object(image)
        obj.location = coda.utilities.rand_location(0, MY.window.x)
        obj.velocity = coda.utilities.rand_location(-50, 50)
        obj.scale = 2
        obj.active = True
        MY.asteroids.append(obj)
        count = count + 1

def fire_bullet(player_number):
    """fire a bullet for the player"""
    index = -1
    for i in range(len(MY.bullets)):
        if not MY.bullets[i].active:
            index = i
            break
    if index >= 0:
        MY.bullets[index].active = True
        if player_number == 1:
            MY.bullets[index].location = MY.player1.location
            MY.bullets[index].set_velocity(MY.player1.rotation, BULLET_SPEED)
            MY.bullets[index].rotation = MY.player1.rotation
        else:
            MY.bullets[index].location = MY.player2.location
            MY.bullets[index].set_velocity(MY.player2.rotation, BULLET_SPEED)
            MY.bullets[index].rotation = MY.player2.rotation

        MY.bullet_owner[index] = player_number
        MY.bullets[index].sprite = PROJECTILE_ANIMATION[player_number]


def draw(screen):
    """Draws the state to the given screen."""
    #if MY.state == 0:
    #    print ("draw functoin state==0")
    MY.background.draw(screen)
    MY.player1.draw(screen)
    MY.player2.draw(screen)
    rect = MY.player1.sprite.surface().get_rect()
    rect.center = MY.player1.location
    health_bar(screen, MY.player1_hp,
                PLAYER_MAX_HP, coda.Vector2(rect.width, 10), rect.topleft)
    rect = MY.player2.sprite.surface().get_rect()
    rect.center = MY.player2.location
    health_bar(screen, MY.player2_hp,
                PLAYER_MAX_HP, coda.Vector2(rect.width, 10), rect.topleft)
    
    for i in range(len(MY.bullets)):
        if MY.bullets[i].active:
            MY.bullets[i].draw(screen)

    for i in range(len(MY.asteroids)):
        if MY.asteroids[i].active:
            MY.asteroids[i].draw(screen)
    #else:
    #    print ("draw functoin state!=0")
    #    MY.gameoverbackground.draw(screen)
    #    MY.restart_button.draw(screen)
    #    MY.display_text.draw(screen)

def cleanup():
    """Cleans up the Intro State."""
    MY.bullets = []
    MY.asteroids = []



