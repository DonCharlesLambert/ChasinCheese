from tkinter import *
import time
import random


class ChasinCheese(object):
    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=400, height=400)

        self.rat = Rat(self.canvas)
        self.cheese = Cheese(self.canvas)

        self.canvas.bind("<KeyPress>", self.keydown)
        self.canvas.bind("<KeyRelease>", self.keyup)
        self.canvas.pack()
        self.canvas.focus_set()
        self.root.after(0, self.animation)
        self.root.mainloop()

    def keydown(self, e):
        self.rat.move(e.char)

    def keyup(self, e):
        self.rat.stop()

    def animation(self):
        while True:
            self.rat.animate()
            time.sleep(0.1)
            if self.captured(self.rat, self.cheese):
                self.cheese.get_ate()
                self.cheese = Cheese(self.canvas)

    def captured(self, rat, cheese):
        if cheese.pos[0] <= rat.pos[0] <= cheese.pos[0] + cheese.size[0]:
            if cheese.pos[1] <= rat.pos[1] <= cheese.pos[1] + cheese.size[1]:
                return True
        return False


class Rat:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    LEFT_ANIMATION = ["3", "4", "5"]
    UP_ANIMATION = ["9", "10", "11"]
    DOWN_ANIMATION = ["0", "1", "2"]
    RIGHT_ANIMATION = ["6", "7", "8"]

    def __init__(self, canvas):
        sprite = PhotoImage(file=r'White\0.png')
        self.rat = canvas.create_image(0, 0, image=sprite, anchor="nw")
        self.pos = canvas.coords(self.rat)
        self.animation_number = 0
        self.direction = 3
        self.is_stopped = True
        self.canvas = canvas

    def move(self, button):
        if button in ['w', 's', 'a', 'd']:
            self.is_stopped = False
            x, y = 0, 0
            if button == 'w':
                x, y = 0, -10
                self.direction = self.UP
            elif button == 's':
                x, y = 0, 10
                self.direction = self.DOWN
            elif button == 'a':
                x, y = -10, 0
                self.direction = self.LEFT
            elif button == 'd':
                x, y = 10, 0
                self.direction = self.RIGHT
            self.change_direction(button)
            self.canvas.move(self.rat, x, y)
            self.pos = self.canvas.coords(self.rat)
            self.canvas.update()

    def stop(self):
        self.is_stopped = True

    def change_direction(self, button):
        if button == 'w' and not self.direction == self.UP:
            self.animation_number = 0
        elif button == 's' and not self.direction == self.DOWN:
            self.animation_number = 0
        elif button == 'a' and not self.direction == self.LEFT:
            self.animation_number = 0
        elif button == 'd' and not self.direction == self.RIGHT:
            self.animation_number = 0

    def animate(self):
        if self.direction == self.UP:
            sprite = PhotoImage(file=r"White\\" + self.UP_ANIMATION[self.animation_number] + ".png")
        elif self.direction == self.DOWN:
            sprite = PhotoImage(file=r"White\\" + self.DOWN_ANIMATION[self.animation_number] + ".png")
        elif self.direction == self.LEFT:
            sprite = PhotoImage(file=r"White\\" + self.LEFT_ANIMATION[self.animation_number] + ".png")
        elif self.direction == self.RIGHT:
            sprite = PhotoImage(file=r"White\\" + self.RIGHT_ANIMATION[self.animation_number] + ".png")

        if not self.is_stopped:
            self.animation_number = (self.animation_number + 1) % 3
        self.canvas.itemconfig(self.rat, image=sprite)
        self.canvas.update()


class Cheese:
    def __init__(self, canvas):
        self.sprite = PhotoImage(file=r'images\cheese.png')
        self.sprite = self.sprite.subsample(40, 40)
        self.cheese = canvas.create_image(random.randint(0, 375), random.randint(0, 375),
                                          image=self.sprite, anchor="nw")
        self.size = (self.sprite.width(), self.sprite.height())
        self.pos = canvas.coords(self.cheese)
        self.canvas = canvas

    def get_ate(self):
        self.canvas.delete(self.cheese)


ChasinCheese()
