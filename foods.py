import numpy as np
import pygame


class foods:
    def __init__(self, width, height, win_width, win_height, snake_size, num_parts, x, y, parts):

        self.width = width
        self.height = height
        new_food = True

        while new_food:
            x = np.random.randint(
                0, (win_width-snake_size)//snake_size)*snake_size
            y = np.random.randint(
                0, (win_height-snake_size)//snake_size)*snake_size
            new_food = False
            for i in range(num_parts):
                if x == parts[i].x and y == parts[i].y:
                    new_food = True
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.rect(win, (0, 150, 0),
                         (self.x, self.y, self.width, self.height))
