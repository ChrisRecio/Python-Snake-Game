import pygame
import os
import random
import tkinter as tk
from tkinter import messagebox

# Centers Window
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
displayWidth = 500
displayHeight = 500
pygame.display.set_caption('Snake')
menu = pygame.display.set_mode((displayWidth, displayHeight))
title_font = pygame.font.SysFont("Comic Sans Ms", 60)
text_font = pygame.font.SysFont("Comic Sans Ms", 30)
Black = (0, 0, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)


def textObjects(msg, color):
    text_surface = title_font.render(msg, True, color)
    return text_surface, text_surface.get_rect()


def textCenterX(msg, color, y):
    text_surf, text_rect = textObjects(msg, color)
    text_rect.center = (int((displayWidth / 2)), int(y))
    menu.blit(text_surf, text_rect)


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, menu, outline=None):
        if outline:
            pygame.draw.rect(menu, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(menu, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = text_font.render(self.text, 1, Black)
            menu.blit(text, (int(self.x + (self.width / 2 - text.get_width() / 2)),
                            int(self.y + (self.height / 2 - text.get_height() / 2))))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def RedrawMenuWindow():
    menu.fill(Black)
    game_btn.draw(menu, Black)


class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, direction_x=1, direction_y=0, color=Green):
        self.pos = start
        self.direction_x = 1
        self.direction_y = 0
        self.color = color

    def move(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.pos = (self.pos[0] + self.direction_x, self.pos[1] + self.direction_y)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle = (i * dis + centre - radius, j * dis + 8)
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, Black, circle_middle, radius)
            pygame.draw.circle(surface, Black, circle_middle2, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):

        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 1

    def move(self):

        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            keys = pygame.key.get_pressed()

            # Inputs
            for key in keys:
                if keys[pygame.K_ESCAPE]:
                    self.reset((10, 10))
                    main()

                elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.direction_x = -1
                    self.direction_y = 0
                    self.turns[self.head.pos[:]] = [self.direction_x, self.direction_y]

                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.direction_x = 1
                    self.direction_y = 0
                    self.turns[self.head.pos[:]] = [self.direction_x, self.direction_y]

                elif keys[pygame.K_w] or keys[pygame.K_UP]:
                    self.direction_x = 0
                    self.direction_y = -1
                    self.turns[self.head.pos[:]] = [self.direction_x, self.direction_y]

                elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    self.direction_x = 0
                    self.direction_y = 1
                    self.turns[self.head.pos[:]] = [self.direction_x, self.direction_y]

        # Handles Movement
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:  # Turns
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:  # Handles Moving To Edge Of Screen
                if c.direction_x == -1 and c.pos[0] <= 0:
                    fail()
                    break
                elif c.direction_x == 1 and c.pos[0] >= c.rows - 1:
                    fail()
                    break
                elif c.direction_y == 1 and c.pos[1] >= c.rows - 1:
                    fail()
                    break
                elif c.direction_y == -1 and c.pos[1] <= 0:
                    fail()
                    break
                else:  # Handles Moving To Existing Direction
                    c.move(c.direction_x, c.direction_y)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_x = 0
        self.direction_y = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.direction_x, tail.direction_y

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].direction_x = dx
        self.body[-1].direction_y = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def fail():
    message_box("You Lost", "Length Of Snake: " + str(len(s.body)))
    s.reset((10, 10))


def redrawGameWindow(surface):
    global height, rows, s, snack
    surface.fill(Black)
    s.draw(surface)
    snack.draw(surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def game():
    global height, rows, s, snack
    height = 500
    rows = 20
    try:
        s.reset((10, 10))
    except NameError:
        s = Snake(Green, (10, 10))

    snack = Cube(randomSnack(rows, s), color=Red)
    redrawGameWindow(menu)
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(rows, s), color=Red)

        # Checks if snake runs into itself
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                fail()
                break

        redrawGameWindow(menu)

    pass


# def highScore():


def main():
    while True:
        global game_btn

        menu.fill(Black)

        textCenterX('Snake', Green, 40)

        game_btn.draw(menu, Black)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            # Quit Game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_btn.isOver(pos):
                    game()
            elif event.type == pygame.MOUSEMOTION:
                if game_btn.isOver(pos):
                    game_btn.color = Red
                else:
                    game_btn.color = Green

        pygame.display.update()
        RedrawMenuWindow()


# (color, x, y, width, height, text='')
game_btn = Button(Green, 165, 150, 175, 50, 'Play')

main()
