"""Turtle graphics project file."""
import turtle

# Create our screen
SCREEN = turtle.Screen()
SCREEN.setup(500, 500)
SCREEN.bgpic("Background.png")
turtle.penup()
#turtle.setx(-230)
#turtle.sety(-230)
turtle.pendown()
RUNNING = True

#Happens once.
#turtle.right(90)
#turtle.forward(100)
#turtle.left(45)
#turtle.forward(100)

#Happens every frame.
while RUNNING:
    turtle.forward(2)
    turtle.right(2)

