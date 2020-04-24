from tkinter import *
import random
import time


class ChasinCheese:
    def __init__(self):
        root = Tk()
        self.canvas = Canvas(root, width=400, height=400)
        self.canvas.bind("<KeyPress>", self.keydown)
        self.canvas.bind("<KeyRelease>", self.keyup)
        self.bg_image = PhotoImage(file=r'images\floor.png')
        self.background = self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.white_image = PhotoImage(file=r'images\white.png').subsample(10, 10)
        self.white = self.canvas.create_image(25, 350, image=self.white_image)

        self.black_image = PhotoImage(file=r'images\black.png').subsample(10, 10)
        self.black = self.canvas.create_image(375, 350, image=self.black_image)

        self.score_me = self.canvas.create_text(60, 350, text=0, font=("Purisa", 32), fill="white")
        self.score_you = self.canvas.create_text(350, 350, text=0, font=("Purisa", 32), fill="white")

        self.generate_cheese()

        self.player_one = Rat(self.canvas, 150, 200, "White")
        self.player_two = Rat(self.canvas, 250, 200, "Black")
        self.canvas.focus_set()
        self.canvas.pack()
        self.gameloop()
        root.mainloop()

    def keydown(self, e):
        if e.char == "a":
            self.player_one.move("left")
        elif e.char == "w":
            self.player_one.move("up")
        elif e.char == "d":
            self.player_one.move("right")
        elif e.char == "s":
            self.player_one.move("down")

        if e.char == "j":
            self.player_two.move("left")
        elif e.char == "i":
            self.player_two.move("up")
        elif e.char == "l":
            self.player_two.move("right")
        elif e.char == "k":
            self.player_two.move("down")

    def keyup(self, e):
        print(e.char + " was released")

    def generate_cheese(self):
        self.sprite = PhotoImage(file=r'images\cheese.png')
        self.sprite = self.sprite.subsample(35, 35)
        self.cheese = self.canvas.create_image(random.randint(10, 365), random.randint(10, 365),
                                               image=self.sprite)

    def gameloop(self):
        while True:
            time.sleep(0.1)
            cheese_pos = self.canvas.coords(self.cheese)
            cheese_size = self.sprite.width(), self.sprite.height()

            if cheese_pos[0] - 15 <= self.player_one.pos()[0] <= cheese_pos[0] + cheese_size[0]:
                if cheese_pos[1] - 15 <= self.player_one.pos()[1] <= cheese_pos[1] + cheese_size[1]:
                    self.generate_cheese()
                    self.player_one.score += 1  # added line

            if cheese_pos[0] - 15 <= self.player_two.pos()[0] <= cheese_pos[0] + cheese_size[0]:
                if cheese_pos[1] - 15 <= self.player_two.pos()[1] <= cheese_pos[1] + cheese_size[1]:
                    self.generate_cheese()
                    self.player_two.score += 1  # added line

            self.canvas.itemconfig(self.score_me, text=self.player_one.score)   # added line
            self.canvas.itemconfig(self.score_you, text=self.player_two.score)  # added line
            self.canvas.update()


class Rat:
    # added variables
    LEFT_ANIMATION = ["3", "4", "5"]
    UP_ANIMATION = ["9", "10", "11"]
    DOWN_ANIMATION = ["0", "1", "2"]
    RIGHT_ANIMATION = ["6", "7", "8"]
    animation_number = 0

    def __init__(self, canvas, x, y, colour):
        self.sprite = PhotoImage(file=colour + r'\0.png')
        self.rat = canvas.create_image(x, y, image=self.sprite)
        self.canvas = canvas
        self.colour = colour
        self.score = 0  # added variables

    def move(self, direction):
        if direction == "left":
            self.canvas.move(self.rat, -10, 0)
        elif direction == "right":
            self.canvas.move(self.rat, 10, 0)
        elif direction == "up":
            self.canvas.move(self.rat, 0, -10)
        elif direction == "down":
            self.canvas.move(self.rat, 0, 10)
        self.animate(direction)  # added function call

    def pos(self):
        return self.canvas.coords(self.rat)

    # added function
    def animate(self, direction):
        if direction == "up":
            self.sprite = PhotoImage(file=self.colour + r'\\' + self.UP_ANIMATION[self.animation_number] + ".png")
        elif direction == "down":
            self.sprite = PhotoImage(file=self.colour + r'\\' + self.DOWN_ANIMATION[self.animation_number] + ".png")
        elif direction == "left":
            self.sprite = PhotoImage(file=self.colour + r'\\' + self.LEFT_ANIMATION[self.animation_number] + ".png")
        elif direction == "right":
            self.sprite = PhotoImage(file=self.colour + r'\\' + self.RIGHT_ANIMATION[self.animation_number] + ".png")
        self.animation_number = (self.animation_number + 1) % 3
        self.canvas.itemconfig(self.rat, image=self.sprite)


ChasinCheese()
