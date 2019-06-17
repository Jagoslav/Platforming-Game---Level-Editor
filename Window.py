import pygame
import os
import time
from Color import *
import tkinter
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()


class Window:
    def __init__(self, width, height, title):
        self.fps_font = pygame.font.SysFont(None, 32)
        self.width = width
        self.height = height
        self.title = title
        pygame.display.set_caption(self.title)
        self.display = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.tk_root = tkinter.Tk()
        self.tk_root.withdraw()
        self.tk_root.wm_attributes('-topmost', 1)
        self.c_sec = 0
        self.c_frame = 0
        self.fps = 0
        self.delta_time = 1

    def __del__(self):
        self.tk_root.destroy()

    def show_fps(self):
        """
        displays current fps
        :return:
        """
        fps_overlay = self.fps_font.render(str(self.fps), True, color.yellow)
        self.display.blit(fps_overlay, (0, 0))

    def get_fps(self):
        """
        calculates the fps and deltatime of the window
        :return:
        """
        if self.c_sec == time.strftime("%S"):
            self.c_frame += 1
        else:
            fps = self.c_frame
            self.c_frame = 0
            self.c_sec = time.strftime("%S")
            if fps > 0:
                self.delta_time = 100 / fps
            else:
                self.delta_time = 0


window_frame = Window(800, 600, "Projekt 1")