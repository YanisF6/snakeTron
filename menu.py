import pygame
import pygame.locals
from pygame import mixer
from settings import Settings
from moviepy.editor import VideoFileClip
import os
import sys


class Main:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.x = 150
        pygame.init()
        mixer.init()
        self.load_screen_snake = False
        self.load_screen_tron = False
        self.size = (700, 700)
        self.window = pygame.display.set_mode((self.size))
        self.fps = 60
        self.nav_mus = mixer.Sound(r"data/music/navigation.wav")
        self.intro = pygame.image.load(r"data/images/template.png")
        self.played = False
        self.load_settings = False
        pygame.display.set_caption("SnakeTron")
        self.clock = pygame.time.Clock()

        video = VideoFileClip(r'data/videos/Snake_games_intro.mp4')
        video.preview()

        self.colors = {
            "white": (255, 255, 255),
            "red": (255, 0, 0),
            "black": (0, 0, 0),
            "blue": (0, 0, 255),
            "green": (0, 255, 0),
            "test": (100, 60, 40),
            "bg": (0, 215, 215)
        }

        self.locations = [
            (self.x, 60, self.width, self.height),
            (self.x, 160, self.width, self.height),
            (self.x, 260, self.width, self.height),
            (self.x, 360, self.width, self.height)
        ]

        self.append_rect()
        self.btn_clr = [
            self.colors["test"],
            self.colors["test"],
            self.colors["test"],
            self.colors["test"]
        ]

        self.cpy = self.btn_clr.copy()

        self.game_loop()

    def text(self, Text, color, x, y, s):
        font = pygame.font.Font(r"data\fonts\Debrosee-ALPnL.ttf", s)
        Txt = font.render(Text, True, self.colors[color])
        self.window.blit(Txt, (x, y))

    def append_rect(self):
        self.rects = {
            "play_Snake": pygame.Rect(self.x, 60, self.width, self.height),
            "play_Tron": pygame.Rect(self.x, 160, self.width, self.height),
            "settings_Rect": pygame.Rect(self.x, 260, self.width, self.height),
            "exit_Rect": pygame.Rect(self.x, 360, self.width, self.height)
        }
        self.len = len(self.rects)

    def chng_clr(self, locs, color1, color2, para=None):
        if not para:
            if self.pos_x > locs[0] and self.pos_x < locs[2]:
                if self.pos_y > locs[1] and self.pos_y < locs[3]:
                    color1 = color2
        elif para:
            if self.pos_x > 20 and self.pos_x < locs[2]:
                if self.pos_y > locs[1] and self.pos_y < locs[3]:
                    return True

    def check_mouse_pos(self):
        if self.chng_clr(self.locations[0], None, None, para=True):
            self.btn_clr[0] = (self.x, 60, 255)
            self.mus_play()

        elif self.chng_clr(self.locations[1], None, None, para=True):
            self.btn_clr[1] = (self.x, 160, 255)
            self.mus_play()

        elif self.chng_clr(self.locations[2], None, None, para=True):
            self.btn_clr[2] = (self.x, 260, 255)
            self.mus_play()

        elif self.chng_clr(self.locations[3], None, None, para=True):
            self.btn_clr[2] = (self.x, 360, 255)
            self.mus_play()
        else:
            self.btn_clr = self.cpy.copy()
            self.played = False

    def draw_rects(self):
        pygame.draw.rect(
            self.window, self.btn_clr[0], self.rects["play_Snake"])
        pygame.draw.rect(self.window, self.btn_clr[1], self.rects["play_Tron"])
        pygame.draw.rect(
            self.window, self.btn_clr[2], self.rects["settings_Rect"])
        pygame.draw.rect(self.window, self.btn_clr[3], self.rects["exit_Rect"])

    def blit_texts(self):
        self.text("PLAY SNAKE", "white", self.x+20, 70, 34)
        self.text("PLAY TRON", "white", self.x+20, 170, 34)
        self.text("SETTINGS", "white", self.x+20, 270, 34)
        self.text("EXIT", "white", self.x+20, 370, 34)

    def mus_play(self):
        if not self.played:
            self.nav_mus.play()
            self.played = True

    def game_loop(self):
        while True:
            self.pos_x, self.pos_y = pygame.mouse.get_pos()
            self.window.fill(self.colors["bg"])
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif self.event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pos_x > self.x and self.pos_x < self.width:
                        if self.pos_y > 60 and self.pos_y < 60+self.height:
                            self.load_screen_snake = True
                            break
                    if self.pos_x > self.x and self.pos_x < self.width:
                        if self.pos_y > 160 and self.pos_y < 160+self.height:
                            self.load_screen_tron = True
                            break
                    if self.pos_x > self.x and self.pos_x < self.width:
                        if self.pos_y > 260 and self.pos_y < 260+self.height:
                            self.load_settings = True
                    if self.pos_x > self.x and self.pos_x < self.width:
                        if self.pos_y > 360 and self.pos_y < 750:
                            pygame.quit()
                            sys.exit()
            if self.load_screen_snake:
                VideoFileClip(r'data/videos/loading.mp4').preview()
                self.load_screen_snake = False
                os.system('snake.py')
                # load_main

            if self.load_screen_tron:
                VideoFileClip(r'data/videos/loading.mp4').preview()
                self.load_screen_tron = False
                os.system('tron.py')
                # load_main

            elif self.load_settings:
                break
            self.clock.tick(self.fps)
            self.check_mouse_pos()
            self.draw_rects()
            self.blit_texts()
            pygame.display.update()


height = 70
width = 300
main = Main(width, height)

if main.load_settings:
    settings = Settings(main)
