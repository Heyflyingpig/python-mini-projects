from tkinter import *
import random

snake_body = 3
Update_time = 100
Base_square = 50
Gamesize_wide = 700
Gamesize_length = 700
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.coordinate = []
        self.square = []
        self.body_square = snake_body

        for i in range(0, snake_body):
            self.coordinate.append([0, 0])

        for x, y in self.coordinate:
            square = canvas.create_rectangle(x, y, x + Base_square, y + Base_square, fill=SNAKE_COLOR, tag="snake")
            self.square.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, int(Gamesize_length / Base_square) - 1) * Base_square
        y = random.randint(0, int(Gamesize_wide / Base_square) - 1) * Base_square

        self.coordinate = [x, y]

        canvas.create_oval(x, y, x + Base_square, y + Base_square, fill=FOOD_COLOR, tag="food")

def logic (snake,food):
    x, y = snake.coordinate[0]

    global direction
    if direction == "right":
        x += Base_square
    if direction == "left":
        x -= Base_square
    if direction == "up":
        y -= Base_square
    if direction == "down":
        y += Base_square

    snake.coordinate.insert(0, (x,y))

    square = canvas.create_rectangle(x, y, x + Base_square, y + Base_square, fill=SNAKE_COLOR, )

    snake.square.insert(0,square)

    if x == food.coordinate[0] and y == food.coordinate[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()
    else:
        del snake.coordinate[-1]
        canvas.delete(snake.square[-1])
        del snake.square[-1]

    if check_snake(snake):
        game_over()

    else:
        window.after(Update_time, logic, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_snake(snake):
    x, y = snake.coordinate[0]
    if x < 0 or x >= Gamesize_wide:
        return True
    if y < 0 or y >= Gamesize_length:
        return True

    for Body in snake.coordinate[1:]:
        if x == Body[0] and y == Body[1]:
            return True

    return False

def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=Gamesize_length, width=Gamesize_wide)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

logic(snake, food)

window.mainloop()















