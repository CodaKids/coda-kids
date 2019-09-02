import coda_kids as coda
import pygame
from types import ModuleType
import sys

#coda_kids constant
WHITE = [225, 225, 225]
BLACK = [0, 0, 0]
YELLOW = [255, 255, 0]
RED = [255, 0, 0]
GREEN = [0, 128, 0, 128]
BLUE = [0, 192, 255, 128]

#coda_kids framework
class TextObject:
    """
    Create an object that renders text. Assumes that the default font 
    freesansbold exists in the project directory as a true type font.
        #create a text object
        title = TextObject(coda.color.RED, 12, "example");
    """

    def __init__(self, color_value, font_size, text):
        self.location = pygame.math.Vector2(0, 0)
        self.color = color_value
        self.font_size = font_size
        self.text = text
        self.centered = False

    def __setattr__(self, name, value):
        if name == "location":
            self.__dict__[name] = pygame.math.Vector2(value[0], value[1])
        elif name == "font_size":
            self.__dict__[name] = value
            self.font = pygame.font.Font('freesansbold.ttf', int(self.font_size))
        else:
            self.__dict__[name] = value

    def draw(self, screen):
        """
        Draws the object text to the screen.
            text.draw(SCREEN);
        """

        obj = self.font.render(self.text, 1, self.color)
        loc = pygame.math.Vector2(self.location.x, self.location.y)
        if self.centered is True:
            loc.x -= obj.get_rect().width / 2
        screen.blit(obj, loc)


class Machine:
    """Game state machine class."""
    def __init__(self):
        self.current = 0
        self.previous = 0
        self.states = []

    def register(self, module):
        """Registers the state's init, update, draw, and cleanup functions."""
        self.states.append({'initialize': module.initialize,
                            'update': module.update,
                            'draw': module.draw,
                            'cleanup': module.cleanup})

    def run(self, screen, window, fill_color):
        """Runs the state given machine."""
        clock = pygame.time.Clock()
        # first run initialize!
        self.states[self.current]['initialize'](window)

        while True:
            delta_time = clock.tick(60) / 1000
            if self.current != self.previous:
                self.states[self.current]['cleanup']()
                self.states[self.current]['initialize'](window)
                self.previous = self.current

            coda.actions.update(delta_time)
            self.states[self.current]['update'](delta_time)
            screen.fill(fill_color)
            self.states[self.current]['draw'](screen)
            pygame.display.flip()

Manager = Machine()

# setup
WINDOW = pygame.math.Vector2(900, 500)
SCREEN = coda.start(WINDOW, "Space Wars Tournament")

#load sprites
IMAGE_BACKGROUND = coda.Image("assets/Background.jpg")
IMAGE_PLAYER1 = coda.Image("assets/Player1.png")
IMAGE_PLAYER2 = coda.Image("assets/Player2.png")
IMAGE_ASTEROID = coda.Image("assets/AsteroidLarge.png")
IMAGE_ASTEROID_2 = coda.Image("assets/AsteroidSmall.png")
sound_explosions = [coda.Sound("assets/Explosion1.wav"),
                    coda.Sound("assets/Explosion2.wav")]

SOUND_LASER = [coda.Sound("assets/LaserShoot1.wav"),
               coda.Sound("assets/LaserShoot2.wav")]

SPRITESHEET_PROJECTILE = [None,
                          coda.SpriteSheet("assets/Player1Projectile.png", (36, 24)),
                          coda.SpriteSheet("assets/Player2Projectile.png", (48, 48))]
PROJECTILE_ANIMATION = [None,
                        coda.Animator(SPRITESHEET_PROJECTILE[1], 0.4),
                        coda.Animator(SPRITESHEET_PROJECTILE[2], 0.4)]
IMAGE_GAMEOVER = coda.Image("assets/GameOverBackground.png")
IMAGE_BUTTON = coda.Image("assets/ReplayButton.png")

# constants
SHIP_ROTATE = 120
SHIP_MAX_SPEED = 500
SHIP_ACCEL = 10
BULLET_SPEED = 1000
PLAYER_MAX_HP = 10

# setup
WINDOW = pygame.math.Vector2(900, 500)
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
    window = pygame.math.Vector2(10, 10)
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
                PLAYER_MAX_HP, pygame.math.Vector2(rect.width, 10), rect.topleft)
    rect = MY.player2.sprite.surface().get_rect()
    rect.center = MY.player2.location
    health_bar(screen, MY.player2_hp,
                PLAYER_MAX_HP, pygame.math.Vector2(rect.width, 10), rect.topleft)
    
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


class restarter_player1:
    # load sprites
    IMAGE_GAMEOVER = coda.Image("assets/GameOverBackground.png")
    IMAGE_BUTTON = coda.Image("assets/ReplayButton.png")

    # modifiable data
    class Data:
        """place changable state variables here."""
        gameoverbackground = coda.Object(IMAGE_GAMEOVER)
        restart_button = coda.Object(IMAGE_BUTTON)
        display_text = coda.TextObject(coda.color.WHITE, 24, "Player 1 wins! Play again?")

    MY = Data()

    def initialize(window):
        """Initializes the restart menu state."""
        MY.gameoverbackground.location = window / 2
        MY.restart_button.location = window / 2

    def update(delta_time):
        """Updates the restart menu state."""
        for event in coda.event.listing():
            if coda.event.quit_game(event):
                coda.stop()
            if coda.event.mouse_l_button_down(event):
                if MY.restart_button.collides_with_point(coda.event.mouse_position()):
                    Manager.current = 0

    def draw(screen):
        """Draws the restart menu state."""
        MY.gameoverbackground.draw(screen)
        MY.restart_button.draw(screen)
        MY.display_text.draw(screen)

    def cleanup():
        """Cleans up the restart menu state."""

class restarter_player2:
    """General information on your module and what it does."""    

    # load sprites
    IMAGE_GAMEOVER = coda.Image("assets/GameOverBackground.png")
    IMAGE_BUTTON = coda.Image("assets/ReplayButton.png")

    # modifiable data
    class Data:
        """place changable state variables here."""
        gameoverbackground = coda.Object(IMAGE_GAMEOVER)
        restart_button = coda.Object(IMAGE_BUTTON)
        display_text = coda.TextObject(coda.color.WHITE, 24, "Player 2 wins! Play again?")

    MY = Data()

    def initialize(window):
        """Initializes the restart menu state."""
        MY.gameoverbackground.location = window / 2
        MY.restart_button.location = window / 2

    def update(delta_time):
        """Updates the restart menu state."""
        for event in coda.event.listing():
            if coda.event.quit_game(event):
                coda.stop()
            if coda.event.mouse_l_button_down(event):
                if MY.restart_button.collides_with_point(coda.event.mouse_position()):
                    Manager.current = 0

    def draw(screen):
        """Draws the restart menu state."""
        MY.gameoverbackground.draw(screen)
        MY.restart_button.draw(screen)
        MY.display_text.draw(screen)

    def cleanup():
        """Cleans up the restart menu state."""

r1=restarter_player1()
r2=restarter_player2()