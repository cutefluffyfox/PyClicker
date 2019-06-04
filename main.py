import pygame
from random import randint, random, shuffle, choice
from os.path import join
from os import getcwd, listdir
from time import time
from init import new_game
from pickle import load, dump
import ctypes
# init
pygame.mixer.init()
pygame.font.init()
# downloading last game
f = open("store.pckl", "rb")
fps = load(f)
volume = load(f)
f.close()
# finding display size
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# main valuables
width, height = screensize
theme_color = (200, 50, 50)
lines_color = (255, 255, 255)
next_level_color = (0, 255, 0)


class FPScounter:
    def __init__(self):
        self.count = 0
        self.start = None
        self.last = 0

    def draw(self):
        if self.start is None:
            self.start = time()
            return
        if time() - self.start < 1:
            self.count += 1
        else:
            self.last = self.count
            self.start = time()
            self.count = 0
        my_font = pygame.font.SysFont("Comic Sans MS", height // 30)
        text_surface = my_font.render(f"fps: {self.last}", False, lines_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (width // 8, height // 8)
        win.blit(text_surface, text_rect)


class Button:
    def __init__(self, x, y, w, h, color=lines_color, text="", outline=4):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = color
        self.text = text
        self.outline = outline
        self.my_font = pygame.font.SysFont("Comic Sans MS", self.height // 2)
        self.text_surface = self.my_font.render(self.text, False, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (self.x + self.width // 2 + 1, self.y + self.height // 2 - 1)

    def draw(self):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.width, self.height], self.outline)
        # if self.text:
        #     # my_font = pygame.font.SysFont("Comic Sans MS", self.height // 2)
        #     # text_surface = my_font.render(self.text, False, self.color)
        #     # text_rect = text_surface.get_rect()
        #     # text_rect.center = (self.x + self.width // 2 + 1, self.y + self.height // 2 - 1)
        win.blit(self.text_surface, self.text_rect)

    def click(self, cords):
        if self.x <= cords[0] <= self.x + self.width and self.y <= cords[1] <= self.y + self.height:
            self.color = (255 - self.color[0], 255 - self.color[1], 255 - self.color[2])


class GameSkeleton:
    def __init__(self, alpha=2, x_pos=0, y_pos=0, color=(255, 255, 255)):
        self.x = width // 3 * x_pos + width // 100 * alpha
        self.y = height // 2 * y_pos + height // 100 * alpha
        self.width = (width // 3 * (1 + x_pos) - width // 100 * alpha) - self.x
        self.height = (height // 2 * (1 + y_pos) - height // 100 * alpha) - self.y
        self.color = color
        self.outline = 4
        self.buttons = []
        self.numb = 6
        x_numb = y_numb = self.numb
        self.alpha = 0
        for x in range(x_numb):
            for y in range(y_numb):
                if x == 0:
                    game_x = int(self.width // x_numb * x + self.width // 100 * (self.alpha / 1))
                    game_width = int(self.width // x_numb * (1 + x) - self.width // 100 * (self.alpha / 2) - game_x)
                elif x + 1 == x_numb:
                    game_x = int(self.width // x_numb * x + self.width // 100 * (self.alpha / 2))
                    game_width = int(self.width // x_numb * (1 + x) - self.width // 100 * (self.alpha / 1) - game_x)
                else:
                    game_x = int(self.width // x_numb * x + self.width // 100 * (self.alpha / 2))
                    game_width = int(self.width // x_numb * (1 + x) - self.width // 100 * (self.alpha / 2) - game_x)
                game_x += self.x
                if y == 0:
                    game_y = int(self.height // y_numb * y + self.height // 100 * (self.alpha / 1))
                    game_height = int(self.height // y_numb * (1 + y) - self.height // 100 * (self.alpha / 2) - game_y)
                elif y + 1 == y_numb:
                    game_y = int(self.height // y_numb * y + self.height // 100 * (self.alpha / 2))
                    game_height = int(self.height // y_numb * (1 + y) - self.height // 100 * (self.alpha / 1) - game_y)
                else:
                    game_y = int(self.height // y_numb * y + self.height // 100 * (self.alpha / 2))
                    game_height = int(self.height // y_numb * (1 + y) - self.height // 100 * (self.alpha / 2) - game_y)
                game_y += self.y
                self.buttons.append(Button(game_x, game_y, game_width, game_height,
                                           text="", outline=self.outline, color=self.color))

    def init(self, x, y, this_width, this_height):
        self.x = x
        self.y = y
        self.width = this_width
        self.height = this_height
        self.buttons = []
        x_numb = y_numb = self.numb
        for x in range(x_numb):
            for y in range(y_numb):
                if x == 0:
                    game_x = int(self.width // x_numb * x + self.width // 100 * (self.alpha / 1))
                    game_width = int(self.width // x_numb * (1 + x) - self.width // 100 * (self.alpha / 2) - game_x)
                elif x + 1 == x_numb:
                    game_x = int(self.width // x_numb * x + self.width // 100 * (self.alpha / 2))
                    game_width = int(self.width // x_numb * (1 + x) - self.width // 100 * (self.alpha / 1) - game_x)
                else:
                    game_x = int(self.width // x_numb * x + self.width // 100 * (self.alpha / 2))
                    game_width = int(self.width // x_numb * (1 + x) - self.width // 100 * (self.alpha / 2) - game_x)
                game_x += self.x
                if y == 0:
                    game_y = int(self.height // y_numb * y + self.height // 100 * (self.alpha / 1))
                    game_height = int(self.height // y_numb * (1 + y) - self.height // 100 * (self.alpha / 2) - game_y)
                elif y + 1 == y_numb:
                    game_y = int(self.height // y_numb * y + self.height // 100 * (self.alpha / 2))
                    game_height = int(self.height // y_numb * (1 + y) - self.height // 100 * (self.alpha / 1) - game_y)
                else:
                    game_y = int(self.height // y_numb * y + self.height // 100 * (self.alpha / 2))
                    game_height = int(self.height // y_numb * (1 + y) - self.height // 100 * (self.alpha / 2) - game_y)
                game_y += self.y
                self.buttons.append(Button(game_x, game_y, game_width, game_height,
                                           text="a", outline=self.outline, color=self.color))

    def copy(self):
        return GameSkeleton()

    def draw(self):
        # pygame.draw.rect(win, self.color, [self.x, self.y, self.width, self.height], self.outline)
        for button in self.buttons:
            button.draw()

    def click(self, cords):
        for button in self.buttons:
            button.click(cords)


games = [GameSkeleton()]

clock = pygame.time.Clock()
win = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Lambda's Puzzles!")


def my_random(numb):
    return -numb + (numb + numb) * random()


class Rectangle:
    def __init__(self, color, data, outline=0, background_color=theme_color):
        self.color = color
        self.data = data
        self.outline = outline
        self.background_color = list(background_color)
        self.fill_speed = 4
        self.max = 150
        self.update_color = background_color

    def update(self):
        self.background_color = list(self.update_color)

    def draw(self):
        pygame.draw.rect(win, self.background_color, self.data)
        pygame.draw.rect(win, self.color, self.data, self.outline)

    def clicked(self, cords):
        return (self.data[0] <= cords[0] <= self.data[0] + self.data[2] and
                self.data[1] <= cords[1] <= self.data[1] + self.data[3])

    def is_in(self, cords):
        if (self.data[0] <= cords[0] <= self.data[0] + self.data[2] and
                self.data[1] <= cords[1] <= self.data[1] + self.data[3]):
            self.background_color[0] = min(self.background_color[0] + self.fill_speed, self.max)
            self.background_color[1] = min(self.background_color[1] + self.fill_speed, self.max)
            self.background_color[2] = min(self.background_color[2] + self.fill_speed, self.max)
        else:
            self.background_color[0] = max(self.background_color[0] - self.fill_speed, 0)
            self.background_color[1] = max(self.background_color[1] - self.fill_speed, 0)
            self.background_color[2] = max(self.background_color[2] - self.fill_speed, 0)


class StarBackground:
    class Star:
        def __init__(self):
            self.color = lines_color
            self.x = randint(0, width)
            self.y = randint(0, height)
            self.radius = randint(0, 5)

        def draw(self):
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

        def move(self, x_plus, y_plus):
            self.x = max(min(self.x + x_plus, width), 0)
            self.y = max(min(self.y + y_plus, height), 0)

    def __init__(self, numb=200, start_speed=0.5):
        self.stars = [StarBackground.Star() for _ in range(numb)]
        self.speed = start_speed

    def draw(self):
        for star in self.stars:
            star.move(my_random(self.speed), my_random(self.speed))
            star.draw()


class MusicPlayer:
    def __init__(self, mute=False, playing=True, now_ind=0):
        self.volume = volume
        self.mute = mute
        self.playing = playing
        self.now_ind = now_ind
        self.songs = listdir(join(getcwd(), "music"))
        shuffle(self.songs)

    def check_and_start_next(self):
        if not pygame.mixer.music.get_busy():
            self.now_ind = (self.now_ind + 1) % len(self.songs)
            pygame.mixer.music.load(join(getcwd(), "music", self.songs[self.now_ind]))
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(self.volume)

    def change_volume(self, numb):
        self.mute = False
        self.volume = min(max(self.volume + numb, 0), 1)
        pygame.mixer.music.set_volume(self.volume)

    def mute_song(self):
        if self.mute:
            pygame.mixer.music.set_volume(self.volume)
        else:
            pygame.mixer.music.set_volume(0)
        self.mute = not self.mute

    def stop_play(self):
        if not self.playing:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.playing = not self.playing

    def set_volume_directly(self, numb):
        self.volume = max(min(numb, 1), 0)
        pygame.mixer.music.set_volume(self.volume)


class ExitButton:
    def __init__(self, color=lines_color, outline=4, this_alpha=10):
        self.color = color
        self.outline = outline
        self.alpha = this_alpha
        self.x = this_alpha * 2
        self.y = height // (this_alpha ** 2)
        self.width = width // (2 * this_alpha) - self.x
        self.height = height // (2 * this_alpha) - self.y
        self.rectangle = Rectangle(self.color, (self.x, self.y, self.width, self.height),
                                   self.outline)
        self.last_cords = (0, 0)

    def draw(self):
        self.rectangle.draw()
        free_space = self.height - 2 * self.alpha
        for i in range(2):
            pygame.draw.line(win, self.color, (self.x + self.alpha, self.y + self.alpha + free_space * i),
                                              (self.x + self.width - self.alpha, self.y + self.alpha + free_space * i),
                             self.outline)

    def clicked(self, cords):
        return self.rectangle.clicked(cords)

    def is_in(self, cords):
        self.last_cords = cords
        self.rectangle.is_in(cords)


class InfoPage:
    def __init__(self, color=lines_color, background=theme_color):
        self.background = background
        self.exit_button = ExitButton()
        self.color = color

    def draw(self):
        win.fill(self.background)
        start_background.draw()
        my_font = pygame.font.SysFont("Comic Sans MS", width // 20)
        text_surface = my_font.render("I am lazy, so all info in info.txt", False, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (width // 2, height // 2)
        win.blit(text_surface, text_rect)
        # my_font = pygame.font.SysFont('Comic Sans MS', width // 20)
        # text_surface = my_font.render("(btw u r gay)", False, self.color)
        # text_rect = text_surface.get_rect()
        # text_rect.center = (width // 2, height // 4 * 3)
        # win.blit(text_surface, text_rect)
        self.exit_button.draw()

    def click(self, cords):
        if self.exit_button.clicked(cords):
            return "Pause"
        return ""

    @staticmethod
    def button_pressed(pressed_data: dict):
        del pressed_data
        return ""

    def update(self):
        self.exit_button.rectangle.update()


class SettingsPage:
    def __init__(self, color=lines_color, background=theme_color):
        self.background = background
        self.exit_button = ExitButton()
        self.color = color
        self.cords = (width // 2, height // 2)
        self.outline = 4

    def draw(self):
        win.fill(self.background)
        start_background.draw()
        # volume
        my_font = pygame.font.SysFont("Comic Sans MS", height // 100 * 8)
        text_surface = my_font.render(f"Volume: {int(music_player.volume * 100)}%", False, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (width // 2, height // 10)
        win.blit(text_surface, text_rect)
        # horizontal line
        pygame.draw.line(win, self.color, (width // 10 * 2, height // 100 * 20), (width // 10 * 8, height // 100 * 20),
                         self.outline)
        # vertical line
        x_pos = ((width // 10 * 8) - (width // 10 * 2)) * music_player.volume + width // 10 * 2
        pygame.draw.line(win, self.color, (x_pos, height // 100 * 15), (x_pos, height // 100 * 25), self.outline)
        # mute state
        my_font = pygame.font.SysFont("Comic Sans MS", height // 100 * 5)
        text_surface = my_font.render(f"Mute: {music_player.mute}", False, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (width // 10 * 9, height // 100 * 20)
        win.blit(text_surface, text_rect)
        # playing state
        my_font = pygame.font.SysFont("Comic Sans MS", height // 100 * 5)
        text_surface = my_font.render(f"Playing: {music_player.playing}", False, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (width // 10, height // 100 * 20)
        win.blit(text_surface, text_rect)

        # FPS
        my_font = pygame.font.SysFont("Comic Sans MS", height // 100 * 8)
        text_surface = my_font.render(f"FPS: {fps}", False, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (width // 2, height // 10 * 3)
        win.blit(text_surface, text_rect)
        # horizontal line
        pygame.draw.line(win, self.color, (width // 10, height // 100 * 40), (width // 10 * 9, height // 100 * 40),
                         self.outline)
        # vertical line
        x_pos = ((width // 10 * 9) - (width // 10 * 1)) * ((fps - 30) / (120 - 30)) + width // 10 * 1
        pygame.draw.line(win, self.color, (x_pos, height // 100 * 35), (x_pos, height // 100 * 45), self.outline)

        self.exit_button.draw()

    def click(self, cords):
        free = 4
        if self.exit_button.clicked(cords):
            return "Pause"
        elif width // 10 <= cords[0] <= width // 10 * 9 + free and height // 100 * 36 <= cords[1] <= height // 100 * 44:
            global fps
            fps = int(((cords[0] - width // 10) / (width // 10 * 9 - width // 10)) * (120 - 30) + 30)
        elif width // 10 * 2 <= cords[0] <= width // 10 * 8 + free and height // 100 * 16 <= cords[1] <= height // 100 * 24:
            music_player.set_volume_directly((cords[0] - width // 10 * 2) / (width // 10 * 8 - width // 10 * 2))
        return ""

    @staticmethod
    def button_pressed(pressed_data: dict):
        del pressed_data
        return ""

    def update(self):
        self.exit_button.rectangle.update()


class RestartPage:
    def __init__(self, color=lines_color, background=theme_color):
        self.color = color
        self.exit_button = ExitButton()
        self.background = background
        self.width = width // 7
        self.height = height // 7
        self.x = self.y = 0
        self.count = 0
        self.limit = 5
        self.text = None
        self.new_cords()

    def new_cords(self):
        self.x = randint(0, width - self.width)
        self.y = randint(self.exit_button.y + self.exit_button.height, height - self.height)

    def draw(self):
        win.fill(self.background)
        start_background.draw()
        self.exit_button.draw()
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        my_font = pygame.font.SysFont("Comic Sans MS", int(self.height * 0.2))
        text = f"Confirm {self.count}/{self.limit}" if self.text is None else self.text
        text_surface = my_font.render(text, False, self.background)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
        win.blit(text_surface, text_rect)

    def update(self):
        self.text = None
        self.count = 0
        self.exit_button.rectangle.update()

    def click(self, cords):
        if self.exit_button.clicked(cords):
            return "Pause"
        elif self.x <= cords[0] <= self.x + self.width and self.y <= cords[1] <= self.y + self.height:
            self.count += 1
            if self.count >= self.limit:
                self.count = 0
                new_game()
                self.text = "Confirmed!"
            self.new_cords()
        return ""

    @staticmethod
    def button_pressed(pressed_data: dict):
        del pressed_data
        return ""


class GamePage:
    def __init__(self, background=theme_color):
        self.background = background
        self.alpha = 2
        self.x_numb = 3
        self.y_numb = 2
        self.this_games = []
        # for i in range(self.y_numb):
        #     self.this_games.append([])
        #     for j in range(self.x_numb):
        #         self.this_games[i].append(GameSkeleton.copy())

    def new_game(self):
        x_numb = self.x_numb
        y_numb = self.y_numb
        for x in range(x_numb):
            for y in range(y_numb):
                if x == x_numb // 2 and y == 0:
                    continue
                game = choice(games).copy()
                if x == 0:
                    game_x = int(width // x_numb * x + width // 100 * (self.alpha / 1))
                    game_width = int(width // x_numb * (1 + x) - width // 100 * (self.alpha / 2) - game_x)
                elif x + 1 == x_numb:
                    game_x = int(width // x_numb * x + width // 100 * (self.alpha / 2))
                    game_width = int(width // x_numb * (1 + x) - width // 100 * (self.alpha / 1) - game_x)
                else:
                    game_x = int(width // x_numb * x + width // 100 * (self.alpha / 2))
                    game_width = int(width // x_numb * (1 + x) - width // 100 * (self.alpha / 2) - game_x)
                if y == 0:
                    game_y = int(height // y_numb * y + height // 100 * (self.alpha / 1))
                    game_height = int(height // y_numb * (1 + y) - height // 100 * (self.alpha / 2) - game_y)
                elif y + 1 == y_numb:
                    game_y = int(height // y_numb * y + height // 100 * (self.alpha / 2))
                    game_height = int(height // y_numb * (1 + y) - height // 100 * (self.alpha / 1) - game_y)
                else:
                    game_y = int(height // y_numb * y + height // 100 * (self.alpha / 2))
                    game_height = int(height // y_numb * (1 + y) - height // 100 * (self.alpha / 2) - game_y)
                game.init(game_x, game_y, game_width, game_height)
                self.this_games.append(game)

    def draw(self):
        win.fill(self.background)
        start_background.draw()
        for i in range(len(self.this_games)):
            self.this_games[i].draw()

    def click(self, cords):
        for game in self.this_games:
            game.click(cords)
        return ""

    def button_pressed(self, pressed_data: dict):
        if pressed_data[pygame.K_ESCAPE]:
            return "Pause"
        return ""

    def update(self):
        self.new_game()


class MainMenu:
    def __init__(self, color=lines_color, background=theme_color):
        self.color = color
        self.background = background
        self.average_height = height // 10
        self.average_width = width // 100 * 30
        self.outline = 4
        self.top_space = height // 5
        self.buttons = [["Play"],
                        ["Settings"],
                        ["Restart"],
                        ["Info"],
                        ["Exit"]]
        for i in range(len(self.buttons)):
            # self.buttons[i].extend([width // 2 - self.average_width // 2,
            #                         (height - 2 * self.top_space - self.average_height - 2 * self.outline) //
            #                         (len(self.buttons) - 1) * i + 2 * self.top_space - self.average_height // 3])
            x = width // 2 - self.average_width // 2
            y = ((height - 2 * self.top_space - self.average_height - 2 * self.outline) //
                 (len(self.buttons) - 1) * i + 2 * self.top_space - self.average_height // 3)
            self.buttons[i] = [self.buttons[i][0], Rectangle(self.color, [x, y,
                                                                          self.average_width,
                                                                          self.average_height],
                                                             self.outline)]

    def draw(self):
        win.fill(self.background)
        start_background.draw()
        my_font = pygame.font.SysFont("Comic Sans MS", int(self.top_space * 0.7))
        text_surface = my_font.render("Lambda's Puzzles!", False, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (width // 2, self.top_space)
        win.blit(text_surface, text_rect)
        my_font = pygame.font.SysFont("Comic Sans MS", int(self.average_height * 0.65))
        for text, rect in self.buttons:
            rect.draw()
            text_surface = my_font.render(text, False, self.color)
            text_rect = text_surface.get_rect()
            text_rect.center = (rect.data[0] + self.average_width // 2, rect.data[1] + self.average_height // 2)
            win.blit(text_surface, text_rect)

    @staticmethod
    def button_pressed(pressed_data: dict):
        del pressed_data
        return ""

    def click(self, cords) -> str:
        for text, rect in self.buttons:
            if rect.clicked(cords):
                return text
        return ""

    def is_in(self, cords):
        for text, rect in self.buttons:
            rect.is_in(cords)

    def update(self):
        for text, rect in self.buttons:
            rect.update()


class PagesStructure:
    def __init__(self):
        self.game_page = GamePage()
        self.main_menu = MainMenu()
        self.info_page = InfoPage()
        self.restart_page = RestartPage()
        self.settings_page = SettingsPage()
        self.this_page = self.main_menu

    def buttons_clicked(self, info):
        action = self.this_page.button_pressed(info)
        if type(self.this_page) == GamePage:
            if action == "Pause":
                self.this_page = self.main_menu
        elif type(self.this_page) == MainMenu:
            if action == "Exit":
                global mainloop
                mainloop = False

    def click(self, cords):
        action = self.this_page.click(cords)
        if type(self.this_page) == MainMenu:
            if action == "Exit":
                global mainloop
                mainloop = False
            elif action == "Play":
                self.this_page = self.game_page
                self.this_page.update()
            elif action == "Info":
                self.this_page = self.info_page
                self.this_page.update()
            elif action == "Settings":
                self.this_page = self.settings_page
                self.this_page.update()
            elif action == "Restart":
                self.this_page = self.restart_page
                self.this_page.update()
        elif type(self.this_page) == GamePage:
            if action == "Pause":
                self.this_page = self.main_menu
                self.this_page.update()
        elif type(self.this_page) == InfoPage:
            if action == "Pause":
                self.this_page = self.main_menu
                self.this_page.update()
        elif type(self.this_page) == RestartPage:
            if action == "Pause":
                self.this_page = self.main_menu
                self.this_page.update()
        elif type(self.this_page) == SettingsPage:
            if action == "Pause":
                self.this_page = self.main_menu
                self.this_page.update()

    def draw(self):
        self.this_page.draw()

    def mouse_in(self, cords):
        if type(self.this_page) not in [MainMenu, GamePage]:
            self.this_page.exit_button.is_in(cords)
        elif type(self.this_page) == MainMenu:
            self.this_page.is_in(cords)


class MouseClicksChecker:
    def __init__(self, state=False):
        self.state = state

    def condition(self, info):
        if type(navigator.this_page) == SettingsPage:
            return info
        if info and self.state:
            return not self.state
        elif not info and not self.state:
            return self.state
        self.state = not self.state
        return self.state


class KeyboardClicksChecker:
    def __init__(self):
        self.conditions = {}

    def get_state(self, state, name):
        if state and self.conditions.get(name, False):
            return False
        elif not state and not self.conditions.get(name, False):
            return False
        self.conditions[name] = not self.conditions.get(name, False)
        return self.conditions[name]


navigator = PagesStructure()
clicker = MouseClicksChecker()
music_player = MusicPlayer()
keyboard_clicker = KeyboardClicksChecker()
start_background = StarBackground()

pages_speed_info = FPScounter()

mainloop = True
while mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
    pressed = pygame.key.get_pressed()
    if keyboard_clicker.get_state(pressed[pygame.K_F1], "F1"):
        music_player.mute_song()
    if keyboard_clicker.get_state(pressed[pygame.K_F2], "F2"):
        music_player.change_volume(-0.05)
    if keyboard_clicker.get_state(pressed[pygame.K_F3], "F3"):
        music_player.change_volume(0.05)
    if keyboard_clicker.get_state(pressed[pygame.K_F5], "F5"):
        music_player.stop_play()
    # main things
    music_player.check_and_start_next()
    navigator.buttons_clicked(pressed)
    # кординаты
    left, middle, right = pygame.mouse.get_pressed()
    mouse_cords = pygame.mouse.get_pos()
    if clicker.condition(left):
        navigator.click(mouse_cords)
    navigator.mouse_in(mouse_cords)
    navigator.draw()

    if pressed[pygame.K_F12]:
        pages_speed_info.draw()

    pygame.display.flip()
    clock.tick(fps)
# save game
f = open("store.pckl", "wb")
dump(fps, f)
dump(music_player.volume, f)
f.close()
# print("\nSee you later! =^=\nLove,\nPinka")
