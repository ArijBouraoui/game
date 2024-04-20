import tkinter as tk
from tkinter import messagebox
import pygame
import math
import copy
from borders import *
import pygame as pg
import sys
import numpy as np

class GameSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Selector")
        self.geometry("1032x622")

        # Load background image
        self.background_image = tk.PhotoImage(file="image.png")  # Replace "boy.png" with your image file
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_image_resized = self.background_image.subsample(3, 3)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_form()

    def create_form(self):
        self.form_label = tk.Label(self, text="Welcome to the Hero_Children Game Selector!", font=("Arial", 24, "bold"))
        self.form_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.name_label = tk.Label(self, text="Name:", font=("Arial", 16))
        self.name_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        self.name_entry = tk.Entry(self, font=("Arial", 16))
        self.name_entry.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        self.age_label = tk.Label(self, text="Age:", font=("Arial", 16))
        self.age_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        self.age_entry = tk.Entry(self, font=("Arial", 16))
        self.age_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.submit_button = tk.Button(self, text="Submit", font=("Arial", 16), command=self.redirect_to_game_page)
        self.submit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def redirect_to_game_page(self):
        name = self.name_entry.get()
        age = self.age_entry.get()

        # Validate inputs
        if not name or not age:
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
            return

        # Destroy current window
        self.destroy()

        # Redirect to game selection page
        game_selection_page = GameSelectionPage(name, age)
        game_selection_page.mainloop()

class GameSelectionPage(tk.Tk):
    def __init__(self, name, age):
        super().__init__()
        self.title("Game Selection")
        self.geometry("1032x622")

        # Load background image
        self.background_image = tk.PhotoImage(file="image.png")  # Replace "background_image.png" with your image file
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.name = name
        self.age = age

        self.create_game_buttons()

    def create_game_buttons(self):
        self.welcome_label = tk.Label(self, text=f"Hello, {self.name}!", font=("Arial", 14, "bold"))
        self.welcome_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.game_label = tk.Label(self, text="Choose a game to play:")
        self.game_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        

        self.memory_card_button = tk.Button(self, text="PacMan", font=("Arial", 16), command=self.play_PacMan)
        self.memory_card_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.flag_matching_button = tk.Button(self, text="Flag Matching Game", font=("Arial", 16), command=self.play_flag_matching_game)
        self.flag_matching_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.capital_guessing_button = tk.Button(self, text="Capital Guessing Game", font=("Arial", 16), command=self.play_capital_guessing_game)
        self.capital_guessing_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.balloon_catching_button = tk.Button(self, text="Balloon Catching Game", font=("Arial", 16), command=self.play_balloon_catching_game)
        self.balloon_catching_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
#*********************************************************            PacMan                    ******************************************************************
    def play_PacMan(self):
    
        class Ghost:
            def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
                self.x_pos = x_coord
                self.y_pos = y_coord
                self.center_x = self.x_pos + 22
                self.center_y = self.y_pos + 22
                self.target = target
                self.speed = speed
                self.img = img
                self.direction = direct
                self.dead = dead
                self.in_box = box
                self.id = id
                self.turns, self.in_box = self.check_collisions()
                self.rect = self.draw()

            def draw(self):
                if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
                    screen.blit(self.img, (self.x_pos, self.y_pos))
                elif powerup and not self.dead and not eaten_ghost[self.id]:
                    screen.blit(spooked_img, (self.x_pos, self.y_pos))
                else:
                    screen.blit(dead_img, (self.x_pos, self.y_pos))
                ghost_rect = pygame.rect.Rect(
                    (self.center_x - 18, self.center_y - 18), (36, 36))
                return ghost_rect

            def check_collisions(self):
                num1 = ((HEIGHT - 50) // 32)
                num2 = (WIDTH // 30)
                num3 = 15
                self.turns = [False, False, False, False]
                if 0 < self.center_x // 30 < 29:
                    if level[(self.center_y - num3) //
                            num1][self.center_x // num2] == 9:
                        self.turns[2] = True
                    if level[self.center_y //
                            num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y //
                                    num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y //
                            num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y //
                                    num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
                    if level[(self.center_y + num3) //
                            num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) //
                                    num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) //
                            num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) //
                                    num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True

                    if self.direction == 2 or self.direction == 3:
                        if 12 <= self.center_x % num2 <= 18:
                            if level[(self.center_y + num3) //
                                    num1][self.center_x // num2] < 3 \
                                    or (level[(self.center_y + num3) //
                                            num1][self.center_x // num2] == 9 and (
                                    self.in_box or self.dead)):
                                self.turns[3] = True
                            if level[(self.center_y - num3) //
                                    num1][self.center_x // num2] < 3 \
                                    or (level[(self.center_y - num3) //
                                            num1][self.center_x // num2] == 9 and (
                                    self.in_box or self.dead)):
                                self.turns[2] = True
                        if 12 <= self.center_y % num1 <= 18:
                            if level[self.center_y // num1][(
                                self.center_x - num2) // num2] < 3 \
                                    or (level[self.center_y // num1][(
                                        self.center_x - num2) // num2] == 9 and (
                                        self.in_box or self.dead)):
                                self.turns[1] = True
                            if level[self.center_y // num1][(self.center_x + num2) //
                                                            num2] < 3 or (level[self.center_y //
                                                                                num1][(self.center_x + num2) // num2] == 9 and (
                                                                self.in_box or self.dead)):
                                self.turns[0] = True

                    if self.direction == 0 or self.direction == 1:
                        if 12 <= self.center_x % num2 <= 18:
                            if level[(self.center_y + num3) //
                                    num1][self.center_x // num2] < 3 \
                                    or (level[(self.center_y + num3) //
                                            num1][self.center_x // num2] == 9 and (
                                    self.in_box or self.dead)):
                                self.turns[3] = True
                            if level[(self.center_y - num3) //
                                    num1][self.center_x // num2] < 3 \
                                    or (level[(self.center_y - num3) //
                                            num1][self.center_x // num2] == 9 and (
                                    self.in_box or self.dead)):
                                self.turns[2] = True
                        if 12 <= self.center_y % num1 <= 18:
                            if level[self.center_y // num1][(
                                self.center_x - num3) // num2] < 3 \
                                    or (level[self.center_y // num1][(
                                        self.center_x - num3) // num2] == 9 and (
                                    self.in_box or self.dead)):
                                self.turns[1] = True
                            if level[self.center_y // num1][(
                                self.center_x + num3) // num2] < 3 \
                                    or (level[self.center_y // num1][(
                                        self.center_x + num3) // num2] == 9 and (
                                    self.in_box or self.dead)):
                                self.turns[0] = True
                else:
                    self.turns[0] = True
                    self.turns[1] = True
                if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
                    self.in_box = True
                else:
                    self.in_box = False
                return self.turns, self.in_box

            def move_yellow(self):
                if self.direction == 0:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.x_pos += self.speed
                    elif not self.turns[0]:
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                    elif self.turns[0]:
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        if self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        else:
                            self.x_pos += self.speed
                elif self.direction == 1:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.x_pos -= self.speed
                    elif not self.turns[1]:
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                    elif self.turns[1]:
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        if self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        else:
                            self.x_pos -= self.speed
                elif self.direction == 2:
                    if self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif not self.turns[2]:
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                    elif self.turns[2]:
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        else:
                            self.y_pos -= self.speed
                elif self.direction == 3:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.y_pos += self.speed
                    elif not self.turns[3]:
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                    elif self.turns[3]:
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        else:
                            self.y_pos += self.speed
                if self.x_pos < -30:
                    self.x_pos = 900
                elif self.x_pos > 900:
                    self.x_pos -= 30
                return self.x_pos, self.y_pos, self.direction

            def move_red(self):
                if self.direction == 0:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.x_pos += self.speed
                    elif not self.turns[0]:
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                    elif self.turns[0]:
                        self.x_pos += self.speed
                elif self.direction == 1:
                    if self.target[0] < self.x_pos and self.turns[1]:
                        self.x_pos -= self.speed
                    elif not self.turns[1]:
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                    elif self.turns[1]:
                        self.x_pos -= self.speed
                elif self.direction == 2:
                    if self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif not self.turns[2]:
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                    elif self.turns[2]:
                        self.y_pos -= self.speed
                elif self.direction == 3:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.y_pos += self.speed
                    elif not self.turns[3]:
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.y_pos += self.speed
                if self.x_pos < -30:
                    self.x_pos = 900
                elif self.x_pos > 900:
                    self.x_pos -= 30
                return self.x_pos, self.y_pos, self.direction

            def move_blue(self):
                if self.direction == 0:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.x_pos += self.speed
                    elif not self.turns[0]:
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                    elif self.turns[0]:
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        if self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        else:
                            self.x_pos += self.speed
                elif self.direction == 1:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.x_pos -= self.speed
                    elif not self.turns[1]:
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                    elif self.turns[1]:
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        if self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        else:
                            self.x_pos -= self.speed
                elif self.direction == 2:
                    if self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif not self.turns[2]:
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                    elif self.turns[2]:
                        self.y_pos -= self.speed
                elif self.direction == 3:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.y_pos += self.speed
                    elif not self.turns[3]:
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                    elif self.turns[3]:
                        self.y_pos += self.speed
                if self.x_pos < -30:
                    self.x_pos = 900
                elif self.x_pos > 900:
                    self.x_pos -= 30
                return self.x_pos, self.y_pos, self.direction

            def move_green(self):
                if self.direction == 0:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.x_pos += self.speed
                    elif not self.turns[0]:
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                    elif self.turns[0]:
                        self.x_pos += self.speed
                elif self.direction == 1:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.x_pos -= self.speed
                    elif not self.turns[1]:
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                    elif self.turns[1]:
                        self.x_pos -= self.speed
                elif self.direction == 2:
                    if self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif not self.turns[2]:
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                    elif self.turns[2]:
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        else:
                            self.y_pos -= self.speed
                elif self.direction == 3:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.y_pos += self.speed
                    elif not self.turns[3]:
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                    elif self.turns[3]:
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        else:
                            self.y_pos += self.speed
                if self.x_pos < -30:
                    self.x_pos = 900
                elif self.x_pos > 900:
                    self.x_pos -= 30
                return self.x_pos, self.y_pos, self.direction


        def draw_misc():
            score_text = font.render(f'Score: {score}', True, '#00e6fc')
            screen.blit(score_text, (10, 920))
            if powerup:
                pygame.draw.circle(screen, '#d52b1e', (140, 930), 15)
            for i in range(lives):
                screen.blit(pygame.transform.scale(
                    player_images[0], (30, 30)), (650 + i * 40, 915))
            if game_over:
                pygame.draw.rect(screen, '#00e6fc',
                                [265, 215, 370, 120], 0, 10)
                pygame.draw.rect(screen, "#0d1117",
                                [270, 220, 360, 110], 0, 10)
                gameover_text = font.render(
                    'Game over! Space bar to restart!', True, '#d52b1e')
                screen.blit(gameover_text, (290, 265))
            if game_won:
                pygame.draw.rect(screen, '#00e6fc',
                                [265, 215, 370, 120], 0, 10)
                pygame.draw.rect(screen, '#151515',
                                [270, 220, 360, 110], 0, 10)
                gameover_text = font.render(
                    'Victory! Space bar to restart!', True, '#00ff00')
                screen.blit(gameover_text, (307, 265))


        def check_collisions(scor, power, power_count, eaten_ghosts):
            num1 = (HEIGHT - 50) // 32
            num2 = WIDTH // 30
            if 0 < player_x < 870:
                if level[center_y // num1][center_x // num2] == 1:
                    level[center_y // num1][center_x // num2] = 0
                    scor += 10
                if level[center_y // num1][center_x // num2] == 2:
                    level[center_y // num1][center_x // num2] = 0
                    scor += 50
                    power = True
                    power_count = 0
                    eaten_ghosts = [False, False, False, False]
            return scor, power, power_count, eaten_ghosts


        def draw_borders():
            num1 = ((HEIGHT - 50) // 32)
            num2 = (WIDTH // 30)
            for i in range(len(level)):
                for j in range(len(level[i])):
                    if level[i][j] == 1:
                        pygame.draw.circle(screen, '#faeb7f',
                                        (j * num2 + (0.5 * num2),
                                            i * num1 + (0.5 * num1)),
                                        4)
                    if level[i][j] == 2 and not flicker:
                        pygame.draw.circle(screen, '#faeb7f',
                                        (j * num2 + (0.5 * num2),
                                            i * num1 + (0.5 * num1)),
                                        10)
                    if level[i][j] == 3:
                        pygame.draw.line(screen, color,
                                        (j * num2 + (0.5 * num2),
                                        i * num1),
                                        (j * num2 + (0.5 * num2),
                                        i * num1 + num1), 3)
                    if level[i][j] == 4:
                        pygame.draw.line(screen, color,
                                        (j * num2, i * num1 + (0.5 * num1)),
                                        (j * num2 + num2,
                                        i * num1 + (0.5 * num1)), 3)
                    if level[i][j] == 5:
                        pygame.draw.arc(screen, color,
                                        [(j * num2 - (num2 * 0.4)) - 2,
                                        (i * num1 + (0.5 * num1)),
                                        num2, num1],
                                        0, PI / 2, 3)
                    if level[i][j] == 6:
                        pygame.draw.arc(screen, color,
                                        [(j * num2 + (num2 * 0.5)),
                                        (i * num1 + (0.5 * num1)),
                                        num2, num1], PI / 2, PI, 3)
                    if level[i][j] == 7:
                        pygame.draw.arc(screen, color,
                                        [(j * num2 + (num2 * 0.5)),
                                        (i * num1 - (0.4 * num1)),
                                        num2, num1], PI,
                                        3 * PI / 2, 3)
                    if level[i][j] == 8:
                        pygame.draw.arc(screen, color,
                                        [(j * num2 - (num2 * 0.4)) - 2,
                                        (i * num1 - (0.4 * num1)),
                                        num2, num1], 3 * PI / 2,
                                        2 * PI, 3)
                    if level[i][j] == 9:
                        pygame.draw.line(screen, '#faeb7f',
                                        (j * num2, i * num1 + (0.5 * num1)),
                                        (j * num2 + num2,
                                        i * num1 + (0.5 * num1)), 3)


        def draw_player():
            if direction == 0:
                screen.blit(player_images[counter // 5],
                            (player_x, player_y))
            elif direction == 1:
                screen.blit(pygame.transform.flip(
                    player_images[counter // 5], True, False),
                    (player_x, player_y))
            elif direction == 2:
                screen.blit(pygame.transform.rotate(
                    player_images[counter // 5], 90),
                    (player_x, player_y))
            elif direction == 3:
                screen.blit(pygame.transform.rotate(
                    player_images[counter // 5], 270),
                    (player_x, player_y))


        def check_position(centerx, centery):
            turns = [False, False, False, False]
            num1 = (HEIGHT - 50) // 32
            num2 = (WIDTH // 30)
            num3 = 15
            if centerx // 30 < 29:
                if direction == 0:
                    if level[centery // num1][(centerx - num3) // num2] < 3:
                        turns[1] = True
                if direction == 1:
                    if level[centery // num1][(centerx + num3) // num2] < 3:
                        turns[0] = True
                if direction == 2:
                    if level[(centery + num3) // num1][centerx // num2] < 3:
                        turns[3] = True
                if direction == 3:
                    if level[(centery - num3) // num1][centerx // num2] < 3:
                        turns[2] = True

                if direction == 2 or direction == 3:
                    if 12 <= centerx % num2 <= 18:
                        if level[(centery + num3) // num1][centerx // num2] < 3:
                            turns[3] = True
                        if level[(centery - num3) // num1][centerx // num2] < 3:
                            turns[2] = True
                    if 12 <= centery % num1 <= 18:
                        if level[centery // num1][(centerx - num2) // num2] < 3:
                            turns[1] = True
                        if level[centery // num1][(centerx + num2) // num2] < 3:
                            turns[0] = True
                if direction == 0 or direction == 1:
                    if 12 <= centerx % num2 <= 18:
                        if level[(centery + num1) // num1][centerx // num2] < 3:
                            turns[3] = True
                        if level[(centery - num1) // num1][centerx // num2] < 3:
                            turns[2] = True
                    if 12 <= centery % num1 <= 18:
                        if level[centery // num1][(centerx - num3) // num2] < 3:
                            turns[1] = True
                        if level[centery // num1][(centerx + num3) // num2] < 3:
                            turns[0] = True
            else:
                turns[0] = True
                turns[1] = True

            return turns


        def move_player(play_x, play_y):
            if direction == 0 and turns_allowed[0]:
                play_x += player_speed
            elif direction == 1 and turns_allowed[1]:
                play_x -= player_speed
            if direction == 2 and turns_allowed[2]:
                play_y -= player_speed
            elif direction == 3 and turns_allowed[3]:
                play_y += player_speed
            return play_x, play_y


        def get_targets(red_x, red_y, blue_x, blue_y,
                        green_x, green_y, yellow_x, yellow_y):
            if player_x < 450:
                runaway_x = 900
            else:
                runaway_x = 0
            if player_y < 450:
                runaway_y = 900
            else:
                runaway_y = 0
            return_target = (380, 400)
            if powerup:
                if not red.dead and not eaten_ghost[0]:
                    red_target = (runaway_x, runaway_y)
                elif not red.dead and eaten_ghost[0]:
                    if 340 < red_x < 560 and 340 < red_y < 500:
                        red_target = (400, 100)
                    else:
                        red_target = (player_x, player_y)
                else:
                    red_target = return_target
                if not blue.dead and not eaten_ghost[1]:
                    blue_target = (runaway_x, player_y)
                elif not blue.dead and eaten_ghost[1]:
                    if 340 < blue_x < 560 and 340 < blue_y < 500:
                        blue_target = (400, 100)
                    else:
                        blue_target = (player_x, player_y)
                else:
                    blue_target = return_target
                if not green.dead:
                    green_target = (player_x, runaway_y)
                elif not green.dead and eaten_ghost[2]:
                    if 340 < green_x < 560 and 340 < green_y < 500:
                        green_target = (400, 100)
                    else:
                        green_target = (player_x, player_y)
                else:
                    green_target = return_target
                if not yellow.dead and not eaten_ghost[3]:
                    yellow_target = (450, 450)
                elif not yellow.dead and eaten_ghost[3]:
                    if 340 < yellow_x < 560 and 340 < yellow_y < 500:
                        yellow_target = (400, 100)
                    else:
                        yellow_target = (player_x, player_y)
                else:
                    yellow_target = return_target
            else:
                if not red.dead:
                    if 340 < red_x < 560 and 340 < red_y < 500:
                        red_target = (400, 100)
                    else:
                        red_target = (player_x, player_y)
                else:
                    red_target = return_target
                if not blue.dead:
                    if 340 < blue_x < 560 and 340 < blue_y < 500:
                        blue_target = (400, 100)
                    else:
                        blue_target = (player_x, player_y)
                else:
                    blue_target = return_target
                if not green.dead:
                    if 340 < green_x < 560 and 340 < green_y < 500:
                        green_target = (400, 100)
                    else:
                        green_target = (player_x, player_y)
                else:
                    green_target = return_target
                if not yellow.dead:
                    if 340 < yellow_x < 560 and 340 < yellow_y < 500:
                        yellow_target = (400, 100)
                    else:
                        yellow_target = (player_x, player_y)
                else:
                    yellow_target = return_target
            return [red_target, blue_target,
                    green_target, yellow_target]


        if __name__ == '__main__':
            pygame.init()
            WIDTH = 900
            HEIGHT = 950
            screen = pygame.display.set_mode([WIDTH, HEIGHT])
            timer = pygame.time.Clock()
            
            fps = 60
            font = pygame.font.Font('freesansbold.ttf', 20)
            level = copy.deepcopy(borders)
            color = '#0000cc'
            PI = math.pi
            player_images = []
            for i in range(1, 5):
                player_images.append(pygame.transform.scale(pygame.image.load(
                    f'C:\\Users\\White Devil\\Desktop\\PacMan\\img\\{i}.png'), (45, 45)))
            red_img = pygame.transform.scale(pygame.image.load(
                f'C:\\Users\\White Devil\\Desktop\\PacMan\\img\\red.png'), (45, 45))
            green_img = pygame.transform.scale(pygame.image.load(
                f'C:\\Users\\White Devil\\Desktop\\PacMan\\img\\green.png'), (45, 45))
            blue_img = pygame.transform.scale(pygame.image.load(
                f'C:\\Users\\White Devil\\Desktop\\PacMan\\img\\blue.png'), (45, 45))
            yellow_img = pygame.transform.scale(pygame.image.load(
                f'C:\\Users\\White Devil\\Desktop\\PacMan\\img\\yellow.png'), (45, 45))
            spooked_img = pygame.transform.scale(pygame.image.load(
                f'C:\\Users\\White Devil\\Desktop\\PacMan\\img\\powerup.png'), (45, 45))
            dead_img = pygame.transform.scale(pygame.image.load(
                f'C:\\Users\\White Devil\\Desktop\\PacMan\\img\\dead.png'), (45, 45))

            player_x = 450
            player_y = 663
            direction = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            green_x = 440
            green_y = 400
            green_direction = 2
            yellow_x = 440
            yellow_y = 438
            yellow_direction = 2
            counter = 0
            flicker = False

            turns_allowed = [False, False, False, False]
            direction_command = 0
            player_speed = 2
            score = 0
            powerup = False
            power_counter = 0
            eaten_ghost = [False, False, False, False]
            targets = [(player_x, player_y),
                    (player_x, player_y),
                    (player_x, player_y),
                    (player_x, player_y)]
            red_dead = False
            blue_dead = False
            yellow_dead = False
            green_dead = False
            red_box = False
            blue_box = False
            yellow_box = False
            green_box = False
            moving = False
            ghost_speeds = [2, 2, 2, 2]
            startup_counter = 0
            lives = 3
            game_over = False
            game_won = False

            run = True
            while run:
                timer.tick(fps)
                if counter < 19:
                    counter += 1
                    if counter > 3:
                        flicker = False
                else:
                    counter = 0
                    flicker = True
                if powerup and power_counter < 600:
                    power_counter += 1
                elif powerup and power_counter >= 600:
                    power_counter = 0
                    powerup = False
                    eaten_ghost = [False, False, False, False]
                if startup_counter < 180 and not game_over and not game_won:
                    moving = False
                    startup_counter += 1
                else:
                    moving = True

                screen.fill('#151515')
                draw_borders()
                center_x = player_x + 23
                center_y = player_y + 24
                if powerup:
                    ghost_speeds = [1, 1, 1, 1]
                else:
                    ghost_speeds = [2, 2, 2, 2]
                if eaten_ghost[0]:
                    ghost_speeds[0] = 2
                if eaten_ghost[1]:
                    ghost_speeds[1] = 2
                if eaten_ghost[2]:
                    ghost_speeds[2] = 2
                if eaten_ghost[3]:
                    ghost_speeds[3] = 2
                if red_dead:
                    ghost_speeds[0] = 4
                if blue_dead:
                    ghost_speeds[1] = 4
                if green_dead:
                    ghost_speeds[2] = 4
                if yellow_dead:
                    ghost_speeds[3] = 4

                game_won = True
                for i in range(len(level)):
                    if 1 in level[i] or 2 in level[i]:
                        game_won = False

                player_circle = pygame.draw.circle(screen, '#0d1117',
                                                (center_x, center_y), 20, 2)
                draw_player()
                red = Ghost(red_x, red_y, targets[0],
                            ghost_speeds[0], red_img,
                            red_direction, red_dead,
                            red_box, 0)
                blue = Ghost(blue_x, blue_y, targets[1],
                            ghost_speeds[1], blue_img,
                            blue_direction, blue_dead,
                            blue_box, 1)
                green = Ghost(green_x, green_y, targets[2],
                            ghost_speeds[2], green_img,
                            green_direction, green_dead,
                            green_box, 2)
                yellow = Ghost(yellow_x, yellow_y, targets[3],
                            ghost_speeds[3], yellow_img,
                            yellow_direction, yellow_dead,
                            yellow_box, 3)
                draw_misc()
                targets = get_targets(red_x, red_y, blue_x, blue_y,
                                    green_x, green_y, yellow_x, yellow_y)

                turns_allowed = check_position(center_x, center_y)
                if moving:
                    player_x, player_y = move_player(player_x, player_y)
                    if not red_dead and not red.in_box:
                        red_x, red_y, red_direction = red.move_red()
                    else:
                        red_x, red_y, red_direction = red.move_yellow()
                    if not green_dead and not green.in_box:
                        green_x, green_y, green_direction = green.move_green()
                    else:
                        green_x, green_y, green_direction = green.move_yellow()
                    if not blue_dead and not blue.in_box:
                        blue_x, blue_y, blue_direction = blue.move_blue()
                    else:
                        blue_x, blue_y, blue_direction = blue.move_yellow()
                    yellow_x, yellow_y, yellow_direction = yellow.move_yellow()
                score, powerup, power_counter, eaten_ghost = check_collisions(
                    score, powerup,
                    power_counter, eaten_ghost)

                if not powerup:
                    if (player_circle.colliderect(
                        red.rect) and not red.dead) or \
                            (player_circle.colliderect(
                                blue.rect) and not blue.dead) or \
                            (player_circle.colliderect(green.rect) and not green.dead) or \
                            (player_circle.colliderect(yellow.rect) and not yellow.dead):
                        if lives > 0:
                            lives -= 1
                            startup_counter = 0
                            powerup = False
                            power_counter = 0
                            player_x = 450
                            player_y = 663
                            direction = 0
                            direction_command = 0
                            red_x = 56
                            red_y = 58
                            red_direction = 0
                            blue_x = 440
                            blue_y = 388
                            blue_direction = 2
                            green_x = 440
                            green_y = 438
                            green_direction = 2
                            yellow_x = 440
                            yellow_y = 438
                            yellow_direction = 2
                            eaten_ghost = [False, False,
                                        False, False]
                            red_dead = False
                            blue_dead = False
                            yellow_dead = False
                            green_dead = False
                        else:
                            game_over = True
                            moving = False
                            startup_counter = 0
                if powerup and player_circle.colliderect(red.rect) and\
                        eaten_ghost[0] and not red.dead:
                    if lives > 0:
                        powerup = False
                        power_counter = 0
                        lives -= 1
                        startup_counter = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        red_x = 56
                        red_y = 58
                        red_direction = 0
                        blue_x = 440
                        blue_y = 388
                        blue_direction = 2
                        green_x = 440
                        green_y = 438
                        green_direction = 2
                        yellow_x = 440
                        yellow_y = 438
                        yellow_direction = 2
                        eaten_ghost = [False, False,
                                    False, False]
                        red_dead = False
                        blue_dead = False
                        yellow_dead = False
                        green_dead = False
                    else:
                        game_over = True
                        moving = False
                        startup_counter = 0
                if powerup and player_circle.colliderect(blue.rect) and\
                        eaten_ghost[1] and not blue.dead:
                    if lives > 0:
                        powerup = False
                        power_counter = 0
                        lives -= 1
                        startup_counter = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        red_x = 56
                        red_y = 58
                        red_direction = 0
                        blue_x = 440
                        blue_y = 388
                        blue_direction = 2
                        green_x = 440
                        green_y = 438
                        green_direction = 2
                        yellow_x = 440
                        yellow_y = 438
                        yellow_direction = 2
                        eaten_ghost = [False, False,
                                    False, False]
                        red_dead = False
                        blue_dead = False
                        yellow_dead = False
                        green_dead = False
                    else:
                        game_over = True
                        moving = False
                        startup_counter = 0
                if powerup and player_circle.colliderect(green.rect) and\
                        eaten_ghost[2] and not green.dead:
                    if lives > 0:
                        powerup = False
                        power_counter = 0
                        lives -= 1
                        startup_counter = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        red_x = 56
                        red_y = 58
                        red_direction = 0
                        blue_x = 440
                        blue_y = 388
                        blue_direction = 2
                        green_x = 440
                        green_y = 438
                        green_direction = 2
                        yellow_x = 440
                        yellow_y = 438
                        yellow_direction = 2
                        eaten_ghost = [False, False,
                                    False, False]
                        red_dead = False
                        blue_dead = False
                        yellow_dead = False
                        green_dead = False
                    else:
                        game_over = True
                        moving = False
                        startup_counter = 0
                if powerup and player_circle.colliderect(yellow.rect) and\
                        eaten_ghost[3] and not yellow.dead:
                    if lives > 0:
                        powerup = False
                        power_counter = 0
                        lives -= 1
                        startup_counter = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        red_x = 56
                        red_y = 58
                        red_direction = 0
                        blue_x = 440
                        blue_y = 388
                        blue_direction = 2
                        green_x = 440
                        green_y = 438
                        green_direction = 2
                        yellow_x = 440
                        yellow_y = 438
                        yellow_direction = 2
                        eaten_ghost = [False, False,
                                    False, False]
                        red_dead = False
                        blue_dead = False
                        yellow_dead = False
                        green_dead = False
                    else:
                        game_over = True
                        moving = False
                        startup_counter = 0
                if powerup and player_circle.colliderect(red.rect) and not\
                        red.dead and not eaten_ghost[0]:
                    red_dead = True
                    eaten_ghost[0] = True
                    score += (2 ** eaten_ghost.count(True)) * 100
                if powerup and player_circle.colliderect(blue.rect) and not\
                        blue.dead and not eaten_ghost[1]:
                    blue_dead = True
                    eaten_ghost[1] = True
                    score += (2 ** eaten_ghost.count(True)) * 100
                if powerup and player_circle.colliderect(green.rect) and not\
                        green.dead and not eaten_ghost[2]:
                    green_dead = True
                    eaten_ghost[2] = True
                    score += (2 ** eaten_ghost.count(True)) * 100
                if powerup and player_circle.colliderect(yellow.rect) and not\
                        yellow.dead and not eaten_ghost[3]:
                    yellow_dead = True
                    eaten_ghost[3] = True
                    score += (2 ** eaten_ghost.count(True)) * 100

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            direction_command = 0
                        if event.key == pygame.K_LEFT:
                            direction_command = 1
                        if event.key == pygame.K_UP:
                            direction_command = 2
                        if event.key == pygame.K_DOWN:
                            direction_command = 3
                        if event.key == pygame.K_SPACE and\
                                (game_over or game_won):
                            powerup = False
                            power_counter = 0
                            lives -= 1
                            startup_counter = 0
                            player_x = 450
                            player_y = 663
                            direction = 0
                            direction_command = 0
                            red_x = 56
                            red_y = 58
                            red_direction = 0
                            blue_x = 440
                            blue_y = 388
                            blue_direction = 2
                            green_x = 440
                            green_y = 438
                            green_direction = 2
                            yellow_x = 440
                            yellow_y = 438
                            yellow_direction = 2
                            eaten_ghost = [False, False,
                                        False, False]
                            red_dead = False
                            blue_dead = False
                            yellow_dead = False
                            green_dead = False
                            score = 0
                            lives = 3
                            level = copy.deepcopy(borders)
                            game_over = False
                            game_won = False

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RIGHT and\
                                direction_command == 0:
                            direction_command = direction
                        if event.key == pygame.K_LEFT and\
                                direction_command == 1:
                            direction_command = direction
                        if event.key == pygame.K_UP and\
                                direction_command == 2:
                            direction_command = direction
                        if event.key == pygame.K_DOWN and\
                                direction_command == 3:
                            direction_command = direction

                if direction_command == 0 and turns_allowed[0]:
                    direction = 0
                if direction_command == 1 and turns_allowed[1]:
                    direction = 1
                if direction_command == 2 and turns_allowed[2]:
                    direction = 2
                if direction_command == 3 and turns_allowed[3]:
                    direction = 3

                if player_x > 900:
                    player_x = -47
                elif player_x < -50:
                    player_x = 897

                if red.in_box and red_dead:
                    red_dead = False
                if blue.in_box and blue_dead:
                    blue_dead = False
                if green.in_box and green_dead:
                    green_dead = False
                if yellow.in_box and yellow_dead:
                    yellow_dead = False

                pygame.display.flip()
            pygame.quit()
        # Placeholder function for playing Memory Card Game
        
        messagebox.showinfo("Memory Card Game", "You are playing Memory Card Game. Click OK to finish the game.")

        # After playing the game, display score
        self.display_score()

# **************************************   end PacMan       *********************************************   

# **************************************  start Soduku       *********************************************  

import pygame as pg
import sys
import numpy as np

# Dimensions de la fenêtre et des cases
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700  # Ajuster la hauteur pour inclure la zone de message
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE

# Dimensions de la zone de message
MESSAGE_AREA_HEIGHT = 100
MESSAGE_AREA_COLOR = (200, 200, 200)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Exemple de grille Sudoku (0 représente une case vide)
EXAMPLE_BOARD = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])

class SudokuGame:
    def __init__(self):
        self.grid = EXAMPLE_BOARD.copy()
        self.selected = None
        self.error_message = ""  # Initialiser le message d'erreur comme une chaîne vide
    def draw(self, screen):
        screen.fill(WHITE)
        # Dessiner la zone de jeu
        self.draw_board(screen)
        # Dessiner la zone de message
        self.draw_message_area(screen)
    def draw_board(self, screen):
        for i in range(GRID_SIZE + 1):
            thickness = 4 if i % 3 == 0 else 1
            pg.draw.line(screen, BLACK, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), thickness)
            pg.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT - CELL_SIZE), thickness)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                if value != 0:
                    self.draw_number(screen, value, (j, i))
        if self.selected:
            pg.draw.rect(screen, BLUE, (self.selected[0] * CELL_SIZE, self.selected[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
    def draw_message_area(self, screen):
        pg.draw.rect(screen, MESSAGE_AREA_COLOR, (0, SCREEN_HEIGHT - MESSAGE_AREA_HEIGHT, SCREEN_WIDTH, MESSAGE_AREA_HEIGHT))
        font = pg.font.Font(None, 25)
        text = font.render(self.error_message, True, BLUE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - MESSAGE_AREA_HEIGHT // 2))
        screen.blit(text, text_rect)
    def draw_number(self, screen, value, pos):
        font = pg.font.Font(None, 40)
        text = font.render(str(value), True, BLACK)
        text_rect = text.get_rect(center=(pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2))
        screen.blit(text, text_rect)
    def is_valid_move(self, value, pos):
        row, col = pos
        if value == 0:
            return True
        # Check row
        if value in self.grid[row, :]:
            return False
        # Check column
        if value in self.grid[:, col]:
            return False
        # Check 3x3 grid
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        if value in self.grid[start_row:start_row + 3, start_col:start_col + 3]:
            return False
        return True
    def input_number(self, number):
        if self.selected:
            col, row = self.selected
            if self.is_valid_move(number, (row, col)):
                self.grid[row][col] = number
                self.error_message = ""  
            else:
                self.error_message = "Mouvement invalide"
    def click(self, pos):
        if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT - MESSAGE_AREA_HEIGHT:
            col = pos[0] // CELL_SIZE
            row = pos[1] // CELL_SIZE
            self.selected = (col, row)
        else:
            self.selected = None
def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("ARIJ Game")
    sudoku_game = SudokuGame()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                sudoku_game.click(pos)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    sudoku_game.input_number(1)
                elif event.key == pg.K_2:
                    sudoku_game.input_number(2)
                elif event.key == pg.K_3:
                    sudoku_game.input_number(3)
                elif event.key == pg.K_4:
                    sudoku_game.input_number(4)
                elif event.key == pg.K_5:
                    sudoku_game.input_number(5)
                elif event.key == pg.K_6:
                    sudoku_game.input_number(6)
                elif event.key == pg.K_7:
                    sudoku_game.input_number(7)
                elif event.key == pg.K_8:
                    sudoku_game.input_number(8)
                elif event.key == pg.K_9:
                    sudoku_game.input_number(9)
                elif event.key == pg.K_DELETE or event.key == pg.K_BACKSPACE:
                    sudoku_game.input_number(0)
        screen.fill(WHITE)
        sudoku_game.draw(screen)
        pg.display.flip()
    pg.quit()
    sys.exit()
if __name__ == "__main__":
    main()


# **************************************   end Soduku       *********************************************   
    
# ***************            other game......    
    def play_flag_matching_game(self):
        # Placeholder function for playing Flag Matching Game
        messagebox.showinfo("Flag Matching Game", "You are playing Flag Matching Game. Click OK to finish the game.")

        # After playing the game, display score
        self.display_score()

    def play_capital_guessing_game(self):
        # Placeholder function for playing Capital Guessing Game
        messagebox.showinfo("Capital Guessing Game", "You are playing Capital Guessing Game. Click OK to finish the game.")

        # After playing the game, display score
        self.display_score()

    def play_balloon_catching_game(self):
        # Placeholder function for playing Balloon Catching Game
        messagebox.showinfo("Balloon Catching Game", "You are playing Balloon Catching Game. Click OK to finish the game.")

        # After playing the game, display score
        self.display_score()

    def display_score(self):
        # Placeholder function to display score
        score = 50  # Placeholder score, you can replace it with actual score
        messagebox.showinfo("Score", f"Your score is: {score}")

if __name__ == "__main__":
    app = GameSelector()
    app.mainloop()
