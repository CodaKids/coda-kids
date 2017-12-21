"""General information on your module and what it does."""
import coda_kids as coda

# Load Sprites
IMAGE_BUTTON = coda.Image("Button.png")

# Constants
ANSWERS = coda.utilities.read_file("answers.txt")
QUESTIONS = coda.utilities.read_file("questions.txt")
FAKE_ANSWERS = coda.utilities.read_file("fake_answers.txt")

# Modifiable Data
class Data:
    """place changable state variables here."""
    question_text = coda.TextObject(coda.color.WHITE, 16, "")
    grade_text = coda.TextObject(coda.color.WHITE, 16, "")
    buttons = []
    button_text = []
    correct_answer_index = 0
    question_number = 0
    answered_correctly = 0
    last_answered_question = -1

MY = Data()

def initialize(window):
    """Initialize Quiz State."""
    for index in range(4):
        MY.buttons.append(coda.Object(IMAGE_BUTTON))
        MY.buttons[index].location = (window.x / 2, window.y / 2 + index * 64)
        obj = coda.TextObject(coda.color.BLACK, 16, "")
        obj.centered = True
        obj.location = MY.buttons[index].location
        MY.button_text.append(obj)
    MY.question_text.location = (window.x / 2, 64)
    MY.question_text.centered = True
    set_up_question()

def set_up_question():
    """Function called by init to set up a question."""
    MY.correct_answer_index = coda.utilities.rand(0, 3)
    condition = True

    while condition: # medium difficulty
        question_index = coda.utilities.rand(0, len(QUESTIONS) - 1)
        condition = Data.last_answered_question == question_index

    Data.last_answered_question = question_index
    MY.question_number = MY.question_number + 1
    MY.question_text.text = QUESTIONS[question_index]
    for index in range(4):
        if index != MY.correct_answer_index:
            rand_index = coda.utilities.rand(0, len(FAKE_ANSWERS) - 1)
            MY.button_text[index].text = FAKE_ANSWERS[rand_index]
        else:
            MY.button_text[index].text = ANSWERS[question_index]

def update(delta_time):
    """update method for the quiz game. involves button logic and events."""
    for event in coda.event.listing():
        if coda.event.quit_game(event):
            coda.stop()
        elif coda.event.mouse_l_button_down(event):
            for index in range(len(MY.buttons)):
                if MY.buttons[index].collides_with_point(coda.event.mouse_position()):
                    if index == MY.correct_answer_index:
                        MY.answered_correctly = MY.answered_correctly + 1

                    # hard difficulty
                    MY.grade_text.text = "Grade: " + str(int(MY.answered_correctly / MY.question_number * 100)) + "%"
                    set_up_question()
                    break

def draw(screen):
    """Draws all of the objects for the quiz state."""
    for button in MY.buttons:
        button.draw(screen)
    MY.question_text.draw(screen)
    if MY.question_number > 1:
        MY.grade_text.draw(screen)
    for text in MY.button_text:
        text.draw(screen)

def cleanup():
    """Cleanup the quiz class."""
    MY.buttons = []
    MY.button_text = []
