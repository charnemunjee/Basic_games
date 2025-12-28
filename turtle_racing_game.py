from turtle import Turtle, Screen
import random

is_race_on = False
screen = Screen()
colors = ['red', 'blue', 'green', 'yellow', 'purple', 'cyan']
y_positions = [100, 70, 40, 10, -20, -50, -80]
user_bet = None

while user_bet not in colors:
    user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color:")

screen.setup(width=500, height=400)

turtles_list = []

for i in range(len(colors)):
    temp_turtle = Turtle(shape='turtle')
    temp_turtle.color(colors[i])
    temp_turtle.penup()
    temp_turtle.goto(x=-240,y=y_positions[i])
    turtles_list.append(temp_turtle)

if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in turtles_list:
        random_distance = random.randint(0,10)
        turtle.forward(random_distance)
        if turtle.xcor() > 230:
            winning_turtle = turtle.pencolor()
            if winning_turtle == user_bet:
                print(f'You Win! The {winning_turtle} turtle is the winner')
            else:
                print(f'You Lose! The {winning_turtle} turtle is the winner')
            is_race_on = False
screen.exitonclick()