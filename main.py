import pygame
from random import randint, random
from os.path import join
from os import getcwd, listdir
from time import time
import pickle
import ctypes
# init
pygame.mixer.init()
pygame.font.init()
# downloading last game
f = open('store.pckl', 'rb')
score = pickle.load(f)
limit = pickle.load(f)
speed = pickle.load(f)
alpha = pickle.load(f)
f.close()
# finding display size
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# main valuables
width, height = screensize
fps = 120
theme_color = (0, 0, 0)
lines_color = (255, 255, 255)
next_level_color = (0, 255, 0)

clock = pygame.time.Clock()
win = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Lambda clicker")


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
    def __init__(self, volume=0.2, mute=False, playing=True, now_ind=0):
        self.volume = volume
        self.mute = mute
        self.playing = playing
        self.now_ind = now_ind
        self.songs = listdir(join(getcwd(), "music"))

    def check_and_start_next(self):
        if not pygame.mixer.music.get_busy():
            self.now_ind = (self.now_ind + 1) % len(self.songs)
            pygame.mixer.music.load(join(getcwd(), "music", self.songs[self.now_ind]))
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(self.volume)

    def change_volume(self, numb):
        self.volume = min(max(self.volume + numb, 0), 1)
        pygame.mixer.music.set_volume(self.volume)

    def set_volume_directly(self):
        if self.mute:
            pygame.mixer.music.set_volume(self.volume)
        else:
            pygame.mixer.music.set_volume(0)
        self.mute = not self.mute

    def stop_play(self):
        if self.playing:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.playing = not self.playing


class ProgressBar:
    def __init__(self, this_alpha=10, color=lines_color, outline=4):
        self.x1 = width // this_alpha * (this_alpha - 1)
        self.y1 = height // (this_alpha ** 2)
        self.x2 = width - (width // this_alpha ** 2)
        self.y2 = height // (2 * this_alpha)
        self.speed = speed
        self.color = color
        self.progress = score
        self.limit = limit
        self.outline = outline

    def make_faster(self, numb):
        self.speed += numb

    def fill(self):
        self.progress += self.speed

    def clicked(self, cords):
        return self.x1 <= cords[0] <= self.x2 and self.y1 <= cords[1] <= self.y2

    def draw(self):
        x_border = self.x1 + int(abs(self.x2 - self.x1) * (self.progress / self.limit))
        if self.progress >= self.limit:
            x_border = self.x2
            self.color = next_level_color
        else:
            self.color = lines_color
        pygame.draw.polygon(win, self.color, [(self.x1, self.y1),
                                              (self.x1, self.y2),
                                              (x_border, self.y2),
                                              (x_border, self.y1)])
        pygame.draw.polygon(win, self.color, [(self.x1, self.y1),
                                              (self.x1, self.y2),
                                              (self.x2, self.y2),
                                              (self.x2, self.y1)], self.outline)


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
        self.rectangle.is_in(cords)


class InfoPage:
    def __init__(self, color=lines_color, background=theme_color):
        self.background = background
        self.exit_button = ExitButton()
        self.color = color

    def draw(self):
        win.fill(self.background)
        start_background.draw()
        my_font = pygame.font.SysFont('Comic Sans MS', width // 20)
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
        my_font = pygame.font.SysFont('Comic Sans MS', int(self.height * 0.2))
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
                global score, limit, speed, alpha
                file = open('store.pckl', 'wb')
                pickle.dump(0, file)  # score
                pickle.dump(100, file)  # limit
                pickle.dump(1, file)  # speed
                pickle.dump(1.7, file)  # alpha
                file.close()
                navigator.game_page.cookie.score = 0
                navigator.game_page.cookie.limit = 100
                navigator.game_page.cookie.speed = 1
                navigator.game_page.cookie.alpha = 1.7
                self.text = "Confirmed!"
            self.new_cords()
        return ""

    @staticmethod
    def button_pressed(pressed_data: dict):
        del pressed_data
        return ""


class Cookie:
    def __init__(self, color=lines_color):
        self.score = score
        self.speed = speed
        self.limit = limit
        self.alpha = alpha
        self.color = color
        self.radius = width // 10
        self.x = width // 2
        self.y = height // 2
        self.last = time()
        self.default = 1

    def next_level(self):
        self.score = self.score - self.limit
        self.speed += 1
        self.limit = int(self.limit * self.alpha)
        self.alpha += self.alpha * 0.05

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        if time() - self.last >= 1:
            self.last = time()
            self.score += self.speed
            # if self.score > self.limit:
            #     self.next_level()
        my_font = pygame.font.SysFont('Comic Sans MS', width // 20)
        text_surface = my_font.render(f"{self.score}", False, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (width // 2, height // 4)
        win.blit(text_surface, text_rect)

    def check_in(self, cords):
        if (cords[0] - self.x) ** 2 + (cords[1] - self.y) ** 2 <= self.radius ** 2:
            self.score += self.speed
            # if self.score > self.limit:
            #     self.next_level()


class GamePage:
    def __init__(self, background=theme_color):
        self.background = background
        self.bar = ProgressBar()
        self.exit_button = ExitButton()
        self.cookie = Cookie()

    def draw(self):
        win.fill(self.background)
        start_background.draw()
        self.bar.progress = self.cookie.score
        self.bar.limit = self.cookie.limit
        self.bar.draw()
        self.exit_button.draw()
        self.cookie.draw()

    def click(self, cords):
        if self.exit_button.clicked(cords):
            return "Pause"
        elif self.bar.clicked(cords):
            if self.cookie.score >= self.cookie.limit:
                self.cookie.next_level()
        self.cookie.check_in(cords)
        return ""

    def button_pressed(self, pressed_data: dict):
        if pressed_data[pygame.K_ESCAPE]:
            return "Pause"
        elif pressed_data[pygame.K_f]:
            self.cookie.score += self.cookie.limit // 4
        return ""

    def update(self):
        self.exit_button.background_color = list(theme_color)


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
        my_font = pygame.font.SysFont('Comic Sans MS', int(self.top_space * 0.8))
        text_surface = my_font.render("Lambda clicker", False, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (width // 2, self.top_space)
        win.blit(text_surface, text_rect)
        my_font = pygame.font.SysFont('Comic Sans MS', int(self.average_height * 0.65))
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

    def draw(self):
        self.this_page.draw()

    def mouse_in(self, cords):
        if type(self.this_page) != MainMenu:
            self.this_page.exit_button.is_in(cords)
        elif type(self.this_page) == MainMenu:
            self.this_page.is_in(cords)


class MouseClicksChecker:
    def __init__(self, state=False):
        self.state = state

    def condition(self, info):
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

mainloop = True
while mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
    pressed = pygame.key.get_pressed()
    if keyboard_clicker.get_state(pressed[pygame.K_F1], "F1"):
        music_player.set_volume_directly()
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
    pygame.display.flip()
    clock.tick(fps)
# save game
f = open('store.pckl', 'wb')
pickle.dump(navigator.game_page.cookie.score, f)
pickle.dump(navigator.game_page.cookie.limit, f)
pickle.dump(navigator.game_page.cookie.speed, f)
pickle.dump(navigator.game_page.cookie.alpha, f)
f.close()
# print("\nSee you later! =^=\nLove,\nPinka")
