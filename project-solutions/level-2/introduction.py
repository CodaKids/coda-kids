"""General information on your module and what it does."""
import coda_kids as coda

#load sprites constants
IMAGE_BACKGROUND = coda.Image("assets/ClassroomBackground.png")
IMAGE_BUTTON = coda.Image("assets/button.png")
IMAGE_CHARACTER_1 = coda.Image("assets/Character_1.png")
IMAGE_CHARACTER_2 = coda.Image("assets/Character_2.png")
IMAGE_CHARACTER_3 = coda.Image("assets/Character_3.png")
IMAGE_CHARACTER_4 = coda.Image("assets/Character_4.png")
IMAGE_CHARACTER_5 = coda.Image("assets/Character_5.png")
IMAGE_CHARACTER_6 = coda.Image("assets/Character_6.png")
IMAGE_CHARACTER_7 = coda.Image("assets/Character_7.png")
IMAGE_CHARACTER_8 = coda.Image("assets/Character_8.png")
IMAGE_CHARACTER_9 = coda.Image("assets/Character_9.png")
IMAGE_CHARACTER_10 = coda.Image("assets/Character_10.png")
IMAGE_CHARACTER_11 = coda.Image("assets/Character_11.png")
IMAGE_CHARACTER_12 = coda.Image("assets/Character_12.png")

SOUND_CHARACTER = [
    [
        coda.Sound("assets/Select_1.wav"),
        coda.Sound("assets/Select_2.wav")
    ],
    [
        coda.Sound("assets/Select_1.wav"),
        coda.Sound("assets/Select_2.wav")
    ],
    [
        coda.Sound("assets/Select_1.wav"),
        coda.Sound("assets/Select_2.wav")
    ],
    [
        coda.Sound("assets/Select_1.wav"),
        coda.Sound("assets/Select_2.wav")
    ],
    [
        coda.Sound("assets/Select_1.wav"),
        coda.Sound("assets/Select_2.wav")
    ]
]

# text constants
TEXT_1  = "I am character 1!"
TEXT_2  = "I am character 2!"
TEXT_3  = "I am character 3!"
TEXT_4  = "I am character 4!"
TEXT_5  = "I am character 5!"
TEXT_6  = "I am character 6!"
TEXT_7  = "I am character 7!"
TEXT_8  = "I am character 8!"
TEXT_9  = "I am character 9!"
TEXT_10 = "I am character 10!"
TEXT_11 = "I am character 11!"
TEXT_12 = "I am character 12!"

class Data:
    """place changable state variables here."""
    info = coda.TextObject(coda.color.BLACK, 32, "")
    button = coda.Object(IMAGE_BUTTON)
    character = coda.Object(IMAGE_CHARACTER_1)
    background = coda.Object(IMAGE_BACKGROUND)
    selection = 1

MY = Data()

def play_sound(character):
    """plays a sound associated with a character."""
    sound = coda.utilities.rand(1, 2)
    SOUND_CHARACTER[character-1][sound-1].play()

def initialize(window):
    """Initializes the Introduction class."""
    MY.button.location = (window.x / 2, window.y * 7 / 8)
    MY.info.location = (235, 250)
    # Center the character and the background
    MY.character.location = window / 2
    MY.background.location = window / 2

def update(delta_time):
    """Update method for Intro state."""
    for event in coda.event.listing():
        if coda.event.quit_game(event):
            coda.stop()
        elif coda.event.mouse_l_button_down(event):
            if MY.button.collides_with_point(coda.event.mouse_position()):
                click_button()

def draw(screen):
    # Draw the background
    MY.background.draw(screen)

    """Draws the state to the given screen."""
    if MY.selection == 1:
        MY.character.sprite = IMAGE_CHARACTER_1
        MY.info.text = TEXT_1
    elif MY.selection == 2:
        MY.character.sprite = IMAGE_CHARACTER_2
        MY.info.text = TEXT_2
    elif MY.selection == 3:
        MY.character.sprite = IMAGE_CHARACTER_3
        MY.info.text = TEXT_3
    elif MY.selection == 4:
        MY.character.sprite = IMAGE_CHARACTER_4
        MY.info.text = TEXT_4
    elif MY.selection == 5:
        MY.character.sprite = IMAGE_CHARACTER_5
        MY.info.text = TEXT_5
    elif MY.selection == 6:
        MY.character.sprite = IMAGE_CHARACTER_6
        MY.info.text = TEXT_6
    elif MY.selection == 7:
        MY.character.sprite = IMAGE_CHARACTER_7
        MY.info.text = TEXT_7
    elif MY.selection == 8:
        MY.character.sprite = IMAGE_CHARACTER_8
        MY.info.text = TEXT_8
    elif MY.selection == 9:
        MY.character.sprite = IMAGE_CHARACTER_9
        MY.info.text = TEXT_9
    elif MY.selection == 10:
        MY.character.sprite = IMAGE_CHARACTER_10
        MY.info.text = TEXT_10
    elif MY.selection == 11:
        MY.character.sprite = IMAGE_CHARACTER_11
        MY.info.text = TEXT_11
    elif MY.selection == 12:
        MY.character.sprite = IMAGE_CHARACTER_12
        MY.info.text = TEXT_12
    MY.character.draw(screen)
    MY.info.draw(screen)
    MY.button.draw(screen)

def cleanup():
    """Cleans up the Intro State."""

def click_button():
    MY.selection += 1
    if MY.selection > 12:
        MY.selection = 1
    # play_sound(MY.selection)

