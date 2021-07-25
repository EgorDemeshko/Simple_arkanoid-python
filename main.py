from tkinter import *
import time
import random


tk = Tk()
tk.title('Simple arkanoid')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)

canvas = Canvas(tk, width=500, height=400, highlightthickness=0)
canvas.pack()

tk.update()


class Ball:
    def __init__(self, canvas, paddle, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score

        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)

        starts_ball = [-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2]
        random.shuffle(starts_ball)
        self.x = starts_ball[0]
        self.y = -2

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

        self.hit_bottom = False

        canvas.create_text(250, 380, text='Для начала игры нажмите Enter', font=('Courier', 8), fill='green')
        canvas.create_text(250, 390, text='Для управления платформой используйте стрелки <- и ->', font=('Courier', 8), fill='green')

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if (pos[2] >= paddle_pos[0]) and (pos[0] <= paddle_pos[2]):
            if (pos[3] >= paddle_pos[1]) and (pos[3] <= paddle_pos[3]):
                self.score.hit()
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)

        if pos[1] <= 0:
            self.y = int(score.score)//10 + 2
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            canvas.create_text(250, 120, text='Вы проиграли', font=('Courier', 30), fill='red')
            canvas.create_text(250, 160, text='Ваш счёт:', font=('Courier', 20), fill='orange')
            canvas.create_text(250, 190, text=str(score.score), font=('Courier', 20), fill='orange')
        if self.hit_paddle(pos) is True:
            self.y = -(int(score.score)//10 + 2)
        if pos[0] <= 0:
            self.x = int(score.score)//10 + 2
        if pos[2] >= self.canvas_width:
            self.x = -(int(score.score)//10 + 2)


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas

        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)

        starts_paddle = [40, 60, 90, 120, 150, 180, 200]
        random.shuffle(starts_paddle)
        self.starting_point_x = starts_paddle[0]
        self.canvas.move(self.id, self.starting_point_x, 300)
        self.x = 0

        self.canvas_width = self.canvas.winfo_width()

        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)

        self.started = False
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)

    def turn_right(self, event):
        self.x = int(score.score)//10 + 2

    def turn_left(self, event):
        self.x = -(int(score.score) // 10 + 2)

    def start_game(self, event):
        self.started = True

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)

        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0


class Score:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.score = 0

        self.id = canvas.create_text(450, 10, text=self.score, font=('Corier', 15), fill=color)

    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)


score = Score(canvas, 'green')

paddle = Paddle(canvas, 'gray')

ball = Ball(canvas, paddle, score, 'yellow')

while not ball.hit_bottom:
    if paddle.started is True:
        ball.draw()
        paddle.draw()

    tk.update_idletasks()
    tk.update()

    time.sleep(0.005)


print(score.score)
time.sleep(3)
