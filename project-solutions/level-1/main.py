"""Turtle graphics project file."""
import turtle

# Create our screen
SCREEN = turtle.Screen()
SCREEN.title("Napster Spacebook")
SCREEN.setup(1280, 800)
SCREEN.bgpic("assets/Background.png")

SCREEN.register_shape("car", ((-4, 10), (4, 10), (4, -10), (-4, -10)))
turtle.shape("car")

# Code is explained by the book
turtle.penup()
turtle.setx(460)
turtle.sety(-275)
turtle.pendown()

# Easy
if True:
    # Student uncomments
    turtle.left(180)
    turtle.forward(510)

    # Student copies from the book
    turtle.right(90)
    turtle.forward(220)

    # Student follows instructions from the book
    turtle.left(90)
    turtle.forward(490)
    turtle.right(90)
    turtle.forward(250)

#Medium
if False:
    turtle.left(180)
    turtle.forward(125)

    turtle.right(90)
    turtle.forward(105)

    turtle.right(90)
    turtle.forward(185)

    turtle.left(90)
    turtle.forward(385)

    turtle.left(90)
    turtle.forward(65)

    turtle.right(90)
    turtle.forward(105)

    turtle.left(90)
    turtle.forward(435)

    turtle.left(90)
    turtle.forward(105)

    turtle.right(90)
    turtle.forward(195)

    turtle.right(90)
    turtle.forward(80)

    turtle.left(90)
    turtle.forward(170)

#Hard
if False:
    for i in range(5):
        turtle.left(180)
        turtle.forward(510)

        turtle.right(90)
        turtle.forward(220)

        turtle.left(90)
        turtle.forward(490)
        turtle.right(90)
        turtle.forward(250)

        # Reached the school

        turtle.left(180)
        turtle.forward(250)
        turtle.left(90)
        turtle.forward(490)
        turtle.right(90)

        turtle.forward(220)
        turtle.left(90)

        turtle.forward(510)


turtle.done()
