"""Turtle graphics project file."""
import turtle

# Create our screen
SCREEN = turtle.Screen()
SCREEN.title("Napster Spacebook")
SCREEN.setup(1280, 800)
SCREEN.bgpic("assets/Background.png")

# Set the shape to be a car.
SCREEN.register_shape("car", ((-4, 10), (4, 10), (4, -10), (-4, -10)))
turtle.shape("car")

# This code moves the turtle to its starting location.
turtle.penup()
turtle.setx(460)
turtle.sety(-275)
turtle.pendown()

# Write a loop to go back and forth 5 times.
# If you don't know what to do, come back after you learn loops.
for i in range(5):
    # Write code to go to the school and then back
    # (You can use your easy solution for a lot of this!)
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
# End the loop here.

# This line stops the window from closing once we make it to the end.
turtle.done()
