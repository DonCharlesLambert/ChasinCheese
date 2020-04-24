from tkinter import *
import time
import random
import winsound


class ChasinCheese:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(self.root, width=400, height=400)

        self.images = []
        self.scoreboard()
        self.rat = Rat(self.canvas)
        self.AI = AIRat(self.canvas)
        self.cheese = Cheese(self.canvas)

        winsound.PlaySound(r'music\flex.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)

        self.canvas.bind("<KeyPress>", self.keydown)
        self.canvas.bind("<KeyRelease>", self.keyup)
        self.canvas.pack()
        self.canvas.focus_set()
        self.animation()

    def scoreboard(self):
        bg_image = PhotoImage(file=r'images\floor.png')
        background = self.canvas.create_image(0, 0, image=bg_image, anchor="nw")

        white_image = PhotoImage(file=r'images\white.png').subsample(10, 10)
        white = self.canvas.create_image(10, 330, image=white_image, anchor="nw")
        black_image = PhotoImage(file=r'images\black.png').subsample(10, 10)
        black = self.canvas.create_image(360, 330, image=black_image, anchor="nw")

        self.score_me = self.canvas.create_text(60, 350, text=0, font=("Purisa", 32), fill="white")
        self.score_AI = self.canvas.create_text(350, 350, text=0, font=("Purisa", 32), fill="white")

        self.images.append([bg_image, background, white_image, white, black_image, black])

    def keydown(self, e):
        self.rat.move(e.char)

    def keyup(self, e):
        self.rat.stop()

    def animation(self):
        while True:
            self.rat.animate()
            self.AI.animate(self.cheese)
            time.sleep(0.1)
            rat_cap = self.captured(self.rat, self.cheese)
            ai_cap = self.captured(self.AI, self.cheese)
            if rat_cap or ai_cap:
                self.cheese.get_ate()
                self.cheese = Cheese(self.canvas)
                if rat_cap:
                    self.rat.eat_cheese()
                else:
                    self.AI.eat_cheese()
                self.update_score()

    def update_score(self):
        self.canvas.itemconfig(self.score_me, text=self.rat.score)
        self.canvas.itemconfig(self.score_AI, text=self.AI.score)

    def captured(self, rat, cheese):
        if cheese.pos[0] - 15 <= rat.pos[0] <= cheese.pos[0] + cheese.size[0] + 15:
            if cheese.pos[1] - 15 <= rat.pos[1] <= cheese.pos[1] + cheese.size[1] + 15:
                return True
        return False


class AbstractRat:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    LEFT_ANIMATION = ["3", "4", "5"]
    UP_ANIMATION = ["9", "10", "11"]
    DOWN_ANIMATION = ["0", "1", "2"]
    RIGHT_ANIMATION = ["6", "7", "8"]

    def __init__(self, canvas, colour, pos):
        self.sprite = PhotoImage(file=colour + r'\0.png')
        self.colour = colour
        self.rat = canvas.create_image(pos, image=self.sprite, anchor="nw")
        self.pos = canvas.coords(self.rat)
        self.animation_number = 0
        self.direction = 3
        self.speed = 7.5
        self.score = 0
        self.is_stopped = True
        self.canvas = canvas

    def eat_cheese(self):
        self.score += 1

    def move(self):
        pass

    def stop(self):
        self.is_stopped = True
        self.animation_number = 0
    
    def animate(self):
        if self.direction == self.UP:
            self.sprite = PhotoImage(file=self.colour + r'\\' + self.UP_ANIMATION[self.animation_number] + ".png")
        elif self.direction == self.DOWN:
            self.sprite = PhotoImage(file=self.colour + r'\\' + self.DOWN_ANIMATION[self.animation_number] + ".png")
        elif self.direction == self.LEFT:
            self.sprite = PhotoImage(file=self.colour + r'\\' + self.LEFT_ANIMATION[self.animation_number] + ".png")
        elif self.direction == self.RIGHT:
            self.sprite = PhotoImage(file=self.colour + r'\\' + self.RIGHT_ANIMATION[self.animation_number] + ".png")

        if not self.is_stopped:
            self.animation_number = (self.animation_number + 1) % 3
        self.canvas.itemconfig(self.rat, image=self.sprite)
        self.canvas.update()


class Rat(AbstractRat):
    def __init__(self, canvas):
        super(Rat, self).__init__(canvas, "White", (0, 0))

    def move(self, button):
        if button in ['w', 's', 'a', 'd']:
            self.is_stopped = False
            x, y = 0, 0
            self.change_direction(button)
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
            self.canvas.move(self.rat, x, y)
            self.pos = self.canvas.coords(self.rat)
            self.canvas.update()

    def change_direction(self, button):
        if button == 'w' and not self.direction == self.UP:
            self.animation_number = 0
        elif button == 's' and not self.direction == self.DOWN:
            self.animation_number = 0
        elif button == 'a' and not self.direction == self.LEFT:
            self.animation_number = 0
        elif button == 'd' and not self.direction == self.RIGHT:
            self.animation_number = 0


class AIRat(AbstractRat):
    def __init__(self, canvas):
        super(AIRat, self).__init__(canvas, "Black", (350, 350))

    def move(self, cheese):
        self.is_stopped = False
        x, y = 0, 0
        if cheese.pos[1] + 15 < self.pos[1]:
            x, y = 0, -self.speed
            self.direction = self.UP
        elif cheese.pos[1] - 15 > self.pos[1]:
            x, y = 0, self.speed
            self.direction = self.DOWN
        elif cheese.pos[0] + 15 < self.pos[0]:
            x, y = -self.speed, 0
            self.direction = self.LEFT
        elif cheese.pos[0] - 15 > self.pos[0]:
            x, y = self.speed, 0
            self.direction = self.RIGHT
        self.canvas.move(self.rat, x, y)
        self.pos = self.canvas.coords(self.rat)
        self.canvas.update()

    def animate(self, cheese):
        self.move(cheese)
        super(AIRat, self).animate()


class Cheese:
    def __init__(self, canvas):
        self.sprite = PhotoImage(file=r'images\cheese.png')
        self.sprite = self.sprite.subsample(35, 35)
        self.cheese = canvas.create_image(random.randint(0, 375), random.randint(0, 375),
                                          image=self.sprite, anchor="nw")
        self.size = (self.sprite.width(), self.sprite.height())
        self.pos = canvas.coords(self.cheese)
        self.canvas = canvas

    def get_ate(self):
        self.canvas.delete(self.cheese)


root = Tk()
# add a menu?
ChasinCheese(root)
# add a multiplayer option to og game
# add a single player maze game
root.mainloop()
