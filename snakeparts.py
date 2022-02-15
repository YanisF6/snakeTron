import pygame


class snakeparts:

    def __init__(self, x, y, width, height, v_x, v_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.v_x = v_x
        self.v_y = v_y
        self.mov_x = []  # remember moves
        self.mov_y = []
        self.mov_x.append(self.v_x)
        self.mov_y.append(self.v_y)
        self.num_parts = 0
        self.add_part = False
        self.lost = False

    def draw(self, win, reshape_factor=1, r=255, g=0, b=0):
        pygame.draw.rect(win, (r, g, b), (self.x, self.y,
                                          self.width*reshape_factor, self.height*reshape_factor))
