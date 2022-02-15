import numpy as np
import pygame
import snakeparts as sp
import foods


class game():

    def __init__(self, snake_size=20, win_width=20*40, win_height=20*30,
                 multiplayer=False, tron_mode=True,
                 collision_with_head=True):
        "Given Variables"
        self.snake_size = snake_size
        self.win_width = win_width  # only multiples of snake_size
        self.win_height = win_height

        self.multiplayer = multiplayer
        self.tron_mode = tron_mode
        self.collision_with_head = collision_with_head
        "Info"
        self.num_action = 4

    def setup(self):
        "-------Create Snakes and food------"
        self.snake = sp.snakeparts(self.snake_size*4, self.snake_size*4, self.snake_size,
                                   self.snake_size, self.snake_size, 0)  # pos_x,pos_y,witdh,height,v_x,v_y
        self.snake.num_parts = 0
        self.parts = list()
        self.food = foods.foods(self.snake_size, self.snake_size, self.win_width,
                                self.win_height, self.snake_size, self.snake.num_parts,
                                self.snake.x, self.snake.y, self.parts)
        if self.multiplayer:
            self.snake2 = sp.snakeparts(
                self.snake_size*5, self.snake_size*12, self.snake_size, self.snake_size, self.snake_size, 0)
        self.parts2 = list()
        "-----Set useful variables-----"
        self.add_part = False
        self.add_part2 = False
        self.run = True
        self.add_food = False
        self.wait_for_part = False

        "IA"
        # *2 because 2 position arguments
        self.observation = np.zeros(
            int(2*self.win_height*self.win_width/self.snake_size**2))
        self.reward = 0
        self.done = False
        if self.multiplayer:
            self.reward2 = 0

    "-------Run one frame of game-----------"

    def step(self, action, action2=0):
        self.action = action
        self.action2 = action2
        "-----Input------"
        self.snake = self.bot_input(self.snake, self.action)
        if self.multiplayer:
            self.snake2 = self.bot_input(self.snake2, self.action2)
            self.reward2 = 0
        self.reward = 0

        "---Computation---"
        if self.add_food:
            self.add_food = False
            self.food = foods.foods(self.snake_size, self.snake_size, self.win_width,
                                    self.win_height, self.snake_size, self.snake.num_parts,
                                    self.snake.x, self.snake.y, self.parts)  # creates new food if food has been eaten
        [self.snake, self.parts] = self.update_snake(self.snake, self.parts)
        [self.snake, self.parts] = self.periodic_limites(
            self.snake, self.parts)
        [self.snake, self.food, self.reward] = self.food_eaten_check(
            self.snake, self.food)
        [self.snake, self.parts, self.reward] = self.collision_check(
            self.snake, self.parts)  # Check if snake collides with itself
        if self.multiplayer:
            [self.snake2, self.parts2] = self.update_snake(
                self.snake2, self.parts2)
            [self.snake2, self.parts2] = self.periodic_limites(
                self.snake2, self.parts2)
            [self.snake2, self.food, self.reward2] = self.food_eaten_check(
                self.snake2, self.food)
            [self.snake2, self.parts2, self.reward2] = self.collision_check(
                self.snake2, self.parts2)
            if self.tron_mode:
                [self.snake, self.parts2, self.reward2] = self.collision_check(
                    self.snake, self.parts2)
                [self.snake2, self.parts, self.reward2] = self.collision_check(
                    self.snake2, self.parts)
                if self.collision_with_head:
                    if self.snake.x == self.snake2.x and self.snake.y == self.snake2.y:
                        self.snake.lost = True
                        self.snake2.lost = True
                        self.run = False
                        self.done = True
            reward2_temp = self.reward2
            self.reward2 -= self.reward
            self.reward -= reward2_temp

        "--Observation--and return"
        if self.multiplayer == False:
            self.observation[0:7] = [self.snake.x, self.snake.y, self.snake.v_x, self.snake.v_y,
                                     self.food.x, self.food.y, len(self.parts)]
            for i in range(0, len(self.parts)):
                self.observation[7+i] = self.parts[i].x
                # write at end because doesn't matter where in list
                self.observation[-i-1] = self.parts[i].y
            return self.observation, self.reward, self.done
        else:
            self.observation[0:12] = [self.snake.x, self.snake.y, self.snake.v_x, self.snake.v_y,
                                      self.food.x, self.food.y, len(
                                          self.parts), self.snake2.x, self.snake2.y,
                                      self.snake2.v_x, self.snake2.v_y, len(self.parts2)]
            for i in range(0, len(self.parts)):
                self.observation[12+2*i] = self.parts[i].x
                self.observation[-2*i-1] = self.parts[i].y
            for i in range(0, len(self.parts2)):
                self.observation[13+2*i] = self.parts2[i].x
                self.observation[-2*i-2] = self.parts2[i].y

            return self.observation, self.reward, self.reward2, self.done

    def bot_input(self, snake, action):
        if action == 0 and snake.v_x == 0:  # 0,1,2,3 <-> l,u,r,d
            snake.v_x = -self.snake_size
            snake.v_y = 0
        elif action == 1 and snake.v_y == 0:
            snake.v_y = -self.snake_size
            snake.v_x = 0
        elif action == 2 and snake.v_x == 0:
            snake.v_x = self.snake_size
            snake.v_y = 0
        elif action == 3 and snake.v_y == 0:
            snake.v_y = self.snake_size
            snake.v_x = 0
        return snake

    def update_snake(self, s, p):
        if s.add_part:
            s.num_parts += 1
            s.add_part = False
            [s, p] = self.add_part_to_snake(s, p)
        s.x += s.v_x
        s.y += s.v_y
        s.mov_x.append(s.v_x)
        s.mov_y.append(s.v_y)
        for i in range(s.num_parts):
            p[i].v_x = s.mov_x[-i-2]
            p[i].v_y = s.mov_y[-i-2]
        for i in range(s.num_parts):
            p[i].x += p[i].v_x
            p[i].y += p[i].v_y
        del s.mov_x[0]
        del s.mov_y[0]
        return s, p

    def add_part_to_snake(self, sn, pa):
        if sn.num_parts == 1:
            sn.mov_x.append(sn.v_x)
            sn.mov_y.append(sn.v_y)
            pa.append(sp.snakeparts(sn.x-sn.v_x, sn.y-sn.v_y,
                      sn.width, sn.height, sn.v_x, sn.v_y))
        if sn.num_parts > 1:
            sn.mov_x.insert(0, sn.mov_x[0])
            sn.mov_y.insert(0, sn.mov_y[0])
            pa.append(sp.snakeparts(
                pa[-1].x-pa[-1].v_x, pa[-1].y-pa[-1].v_y, sn.width, sn.height, pa[-1].v_x, pa[-1].v_y))
        return sn, pa

    def periodic_limites(self, snake, parts):
        if snake.x < 0:
            snake.x = self.win_width-snake.width
        if snake.x > self.win_width-snake.width:
            snake.x = 0
        if snake.y < 0:
            snake.y = self.win_height-snake.height
        if snake.y > self.win_height-snake.height:
            snake.y = 0
        for k in range(snake.num_parts):
            if parts[k].x < 0:
                parts[k].x = self.win_width-snake.width
            if parts[k].x > self.win_width-snake.width:
                parts[k].x = 0
            if parts[k].y < 0:
                parts[k].y = self.win_height-snake.height
            if parts[k].y > self.win_height-snake.height:
                parts[k].y = 0
        return snake, parts

    def food_eaten_check(self, snake, food):
        reward = 0
        if snake.x == food.x and snake.y == food.y:
            snake.add_part = True
            reward = 1
            self.add_food = True
        return snake, food, reward

    def collision_check(self, snake, parts):
        reward = 0
        for i in range(len(parts)):
            if snake.x == parts[i].x and snake.y == parts[i].y:
                snake.lost = True
                self.run = False
                reward = -5
                self.done = True
        return snake, parts, reward
