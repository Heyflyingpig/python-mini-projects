from tkinter import *
import random

snake_body = 3
Update_time = 150
Ai_update_time = 250
Base_square = 50
Gamesize_wide = 800
Gamesize_length = 800
game_condition = False
SNAKE_COLOR = "#00FF00"
AI_COLOR = "#FFFF33"
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




class AISnake:
    def __init__(self):
        self.coordinate = []
        self.square = []
        self.body_square = snake_body

        for i in range(0,snake_body):
            origin_x = Gamesize_wide - Base_square
            origin_y = Gamesize_length - Base_square
            self.coordinate.append([origin_x,origin_y])

        for x,y in self.coordinate:
            square = canvas.create_rectangle(x, y, x + Base_square , y+ Base_square, fill=AI_COLOR, tag="ai" )
            self.square.append(square)

    def ai_move(self,food):
        ai_x, ai_y = self.coordinate[0]
        food_x = food.coordinate[0]
        food_y = food.coordinate[1]

        if ai_x < food_x:
            new_x, new_y = ai_x + Base_square, ai_y
        elif ai_x > food_x:
            new_x, new_y = ai_x - Base_square, ai_y
        elif ai_y < food_y:
            new_x, new_y = ai_x, ai_y + Base_square
        else:
            new_x, new_y = ai_x, ai_y - Base_square
        return new_x,new_y


class Food:
    def __init__(self):
        x = random.randint(0, int(Gamesize_length / Base_square) - 1) * Base_square
        y = random.randint(0, int(Gamesize_wide / Base_square) - 1) * Base_square

        self.coordinate = [x, y]

        canvas.create_oval(x, y, x + Base_square, y + Base_square, fill=FOOD_COLOR, tag="food")

def logic (snake):
    global food
    if game_condition:  # 如果游戏结束，停止运行
        return
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
    square = canvas.create_rectangle(x, y, x + Base_square, y + Base_square, fill=SNAKE_COLOR)

    snake.square.insert(0,square)

    if x == food.coordinate[0] and y == food.coordinate[1]:
        print("touch")
        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()
    else:
        del snake.coordinate[-1]
        canvas.delete(snake.square[-1])
        del snake.square[-1]

    if check_snake(snake, ai_snake):
        game_over()

    else:
        window.after(Update_time, logic, snake)

def ai_logic(ai_snake):
    global food
    if game_condition:  # 如果游戏结束，停止运行
        return
    ai_x, ai_y = ai_snake.ai_move(food)
    ai_snake.coordinate.insert(0, (ai_x, ai_y))
    square = canvas.create_rectangle(ai_x, ai_y, ai_x + Base_square, ai_y + Base_square, fill=AI_COLOR)
    ai_snake.square.insert(0, square)

    if ai_x == food.coordinate[0] and ai_y == food.coordinate[1]:

        canvas.delete("food")
        food = Food()
    else:
        del ai_snake.coordinate[-1]
        canvas.delete(ai_snake.square[-1])
        del ai_snake.square[-1]

    if check_snakes(ai_snake, snake):
        ai_restrat()

    else:
        window.after(Ai_update_time,ai_logic,ai_snake)


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

def check_snake(snake,ai_snake):
    x, y = snake.coordinate[0]
    if x < 0 or x >= Gamesize_wide:
        return True
    if y < 0 or y >= Gamesize_length:
        return True

    for Body in snake.coordinate[1:]:
        if x == Body[0] and y == Body[1]:
            return True
    for ai_body in ai_snake.coordinate[0:]:
        if x == ai_body[0] and y == ai_body[1]:
            return True

    return False
def check_snakes(ai_snake,snake):
    ai_x, ai_y = ai_snake.coordinate[0]

    if ai_x < 0 or ai_x >= Gamesize_wide:
        return True
    elif ai_y < 0 or ai_y >= Gamesize_length:
        return True

    for body_part in snake.coordinate[1:]:
        if ai_x == body_part[0] and ai_y == body_part[1]:
            return True
    for ai_body in ai_snake.coordinate[1:]:
        if ai_x == ai_body[0] and ai_y == ai_body[1]:
            return True

    return False


def game_over():
    global game_condition
    game_condition = True
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 30), text="GAME OVER\nplease press 'Enter' to continue", fill="red", tag="gameover")

    window.bind('<Return>', restart_game)  # 绑定回车键重启游戏



def restart_game(event):
    global score, direction, snake, food,game_condition,ai_snake
    game_condition = False
    score = 0
    direction = 'down'
    label.config(text="Score: {}".format(score))  # 重置分数标签
    canvas.delete(ALL)

    snake = Snake()
    food = Food()
    ai_snake = AISnake()

    logic(snake)
    ai_logic(ai_snake)
    window.unbind('<Return>')

def ai_restrat():
    global ai_snake,game_condition,score

    score += 1
    label.config(text="Score: {}".format(score))
    game_condition = False
    for square in ai_snake.square:
        canvas.delete(square)  # 删除AI蛇的所有方块
    canvas.delete("ai")
    ai_snake = AISnake()
    ai_logic(ai_snake)


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
ai_snake = AISnake()

logic(snake)
ai_logic(ai_snake)

window.mainloop()















