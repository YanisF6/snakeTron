import pygame
import game as g


def in_player(keys):
    # Action=0, 1, 2 or 3 corresponding to left, up, right, down
    global action
    if keys[pygame.K_LEFT]:
        action = 0
    elif keys[pygame.K_UP]:
        action = 1
    elif keys[pygame.K_RIGHT]:
        action = 2
    elif keys[pygame.K_DOWN]:
        action = 3
    return action


def reflexAgent(obs, player):  # input observation
    #obs[0]=snake.x,obs[1]=snake.y, obs[4]=food.x, obs[5]=food.y
    if player == 1:
        i = 7
    elif player == 2:
        i = 0
    else:
        print("Invalid Player!")
    action = 2
    if obs[4] == obs[7-i]:
        action = 1
    return action


"------------Main-------------"
opponent_is_Bot = True
player1_is_Bot = False
env = g.game(multiplayer=False)
vel = 5
delay_penultimate_frame = 1000
delay_last_frame = 1000
time_delay = 120

pygame.init()
pygame.display.set_caption("Snake")
win = pygame.display.set_mode((env.win_width, env.win_height))  # define window
pygame.time.delay(500)

env.setup()
observation = env.observation
done = False
action = 2
action2 = 2
while not done:
    pygame.time.delay(time_delay-vel*10)
    "-----Input------"
    keys = pygame.key.get_pressed()
    if player1_is_Bot:
        action = reflexAgent(observation, 1)
    else:
        in_player(keys)
    if not env.multiplayer:
        [observation, reward, done] = env.step(action)
    else:
        [observation, reward, reward2, done] = env.step(action, action2)

    pygame.draw.rect(win, (0, 0, 0), (0, 0, env.win_width, env.win_height))
    env.food.draw(win)
    env.snake.draw(win, r=180, g=70, b=0)
    for i in range(env.snake.num_parts):
        env.parts[i].draw(win, r=200, g=100, b=0)
    pygame.display.update()
    time_temp = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close window if X is pressed
            done = True

print("==============================")
print("\nSnake Game: ")
print("\nSnake Length Player 1: ", len(env.parts))
print("==============================")

pygame.time.delay(delay_last_frame)
pygame.quit()
