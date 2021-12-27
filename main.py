import pandas
import pygame
from cpu_player import *
from sklearn.neighbors import KNeighborsRegressor

pygame.init()

V_HITS_COUNT = 0
H_HITS_COUNT = 0
HORIZONTAL_HITS_COUNT = 0
WIDTH = 1200
HEIGHT = 800
BORDER = 10
BORDER_COLOR = pygame.Color('yellow')
BALL_COLOR = pygame.Color('WHITE')
BACKGROUND_COLOR = pygame.Color('blue')
screen = pygame.display.set_mode((WIDTH + 200, HEIGHT))
screen.fill('blue')
pygame.display.set_caption('PyPong by Fuzz')
SPEED = 0.5
EXIT = False
SCORE = 0
PADDLE_SPEED = 50
SCORE_COUNTER_FONT = pygame.font.SysFont('arial', 20)
SCORE_TEXT = SCORE_COUNTER_FONT.render('YOUR SCORE: ' + str(SCORE), True, 'black', 'white')
SCORE_TEXT_RECT = SCORE_TEXT.get_rect()
SCORE_TEXT_RECT.center = (WIDTH + 90, HEIGHT//2)
LEARN_MODE = False


class Ball:
    def __init__(self,  wp, hp, speed_x=-1, speed_y=0, radius=10, color=pygame.Color('red')):
        self.radius = radius
        self.color = color
        self.WIDTH_POSITION = wp - radius
        self.HEIGHT_POSITION = hp
        self.SPEED_X = -speed_x
        self.SPEED_Y = -speed_y

    def show(self, color):
        global screen
        pygame.draw.circle(screen, color, (self.WIDTH_POSITION, self.HEIGHT_POSITION), self.radius)

    def update(self, paddle):
        global BACKGROUND_COLOR, BALL_COLOR, WIDTH, HEIGHT, BORDER, V_HITS_COUNT, H_HITS_COUNT, SCORE
        self.show(BACKGROUND_COLOR)
        self.WIDTH_POSITION += self.SPEED_X
        self.HEIGHT_POSITION += self.SPEED_Y

        vertical_condition = ((self.WIDTH_POSITION == (2 * BORDER)) or
                              (self.WIDTH_POSITION == (WIDTH - (2 * BORDER))) and V_HITS_COUNT > 0)

        horizontal_condition = ((self.HEIGHT_POSITION == (2 * BORDER)) or
                                (self.HEIGHT_POSITION == (HEIGHT - (2 * BORDER))) and H_HITS_COUNT > 0)

        patch_condition = (vertical_condition and horizontal_condition)

        if vertical_condition:
            self.SPEED_X *= -1
            V_HITS_COUNT += 1
        elif horizontal_condition:
            if self.WIDTH_POSITION in range(int(paddle.start_position_0[0]), int(paddle.start_position_1[0])):
                if self.HEIGHT_POSITION > (HEIGHT - 3 * BORDER):
                    SCORE += 1
                else:
                    pass
            else:
                if self.HEIGHT_POSITION > (HEIGHT - 3 * BORDER):
                    SCORE -= 1
            self.SPEED_Y *= -1
            H_HITS_COUNT += 1
        else:
            pass

        if patch_condition:
            self.SPEED_Y *= -1
            self.WIDTH_POSITION += 2 * BORDER
            self.SPEED_X *= -1
            V_HITS_COUNT += 1
            H_HITS_COUNT += 1
        else:
            pass
        self.show(BALL_COLOR)


class Paddle:
    def __init__(self, y=80, x=20):
        self.width = x
        self.height = y
        self.start_position_0 = [WIDTH/2 - self.height/2, HEIGHT - 2 * BORDER]
        self.start_position_1 = [WIDTH/2 + self.height/2, HEIGHT - 2 * BORDER]

    def show(self, color):
        global screen
        pygame.draw.line(screen, color, self.start_position_0,
                         self.start_position_1, 10)

    def update(self, how_much):
        self.show(BACKGROUND_COLOR)
        self.start_position_0[0] += how_much
        self.start_position_1[0] = self.start_position_0[0] + self.height
        self.show(BALL_COLOR)


BALL = Ball(WIDTH - BORDER, HEIGHT//2, SPEED, SPEED)

PADDLE = Paddle(200, 20)

CPU_PADDLE = Paddle(200, 20)
CPU_PADDLE.start_position_0[1] = 2 * BORDER
CPU_PADDLE.start_position_1[1] = 2 * BORDER

pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect((0, 0), (WIDTH, BORDER)))

pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(0, 0, BORDER, HEIGHT))

pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(WIDTH - BORDER, 0, BORDER, HEIGHT))

pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(0, HEIGHT - BORDER, WIDTH, BORDER))

clock = pygame.time.Clock()


def score_update():
    global SCORE_TEXT
    SCORE_TEXT = SCORE_COUNTER_FONT.render('YOUR SCORE: ' + str(SCORE) + '  ', True, 'black', 'white')


if LEARN_MODE:
    play_info_file = open("play.csv", "w")
    print("WIDTH_POSITION,HEIGHT_POSITION,SPEED_X,SPEED_Y,PADDLE.CENTRAL_POSITION", file=play_info_file)
else:
    CPU_DATA_PLAY = read_data()

    DATA_X = CPU_DATA_PLAY.drop(columns="PADDLE.CENTRAL_POSITION")
    DATA_Y = CPU_DATA_PLAY['PADDLE.CENTRAL_POSITION']

    CPU_IA = KNeighborsRegressor(n_neighbors=5)
    CPU_IA = CPU_IA.fit(DATA_X, DATA_Y)

    CPU_DATA_FRAME = pandas.DataFrame(columns=['WIDTH_POSITION', 'HEIGHT_POSITION', 'SPEED_X', 'SPEED_Y'])

while not EXIT:
    CPU_PADDLE.update(0)
    CPU_PADDLE.show('blue')
    BALL.update(PADDLE)
    screen.blit(SCORE_TEXT, SCORE_TEXT_RECT)
    for event in pygame.event.get((768, 769, 32787)):
        if event.type != 32787:
            if (event.unicode == 'a') or (event.unicode == 'A'):
                PADDLE.update(-PADDLE_SPEED)
            elif (event.unicode == 'd') or (event.unicode == 'D'):
                PADDLE.update(PADDLE_SPEED)
        elif event.type == 32787:
            EXIT = True
            break
        else:
            pass

    if LEARN_MODE:
        print("{},{},{},{},{}".format(BALL.WIDTH_POSITION, BALL.HEIGHT_POSITION, BALL.SPEED_X,
                                      BALL.SPEED_Y, PADDLE.start_position_0[0]), file=play_info_file)
    else:
        CPU_PADDLE_MOVE = CPU_DATA_FRAME.append({'WIDTH_POSITION': BALL.WIDTH_POSITION,
                                                'HEIGHT_POSITION': BALL.HEIGHT_POSITION,
                                                 'SPEED_X': BALL.SPEED_X,
                                                 'SPEED_Y': BALL.SPEED_Y}, ignore_index=True)
        CPU_POSITION = CPU_IA.predict(CPU_PADDLE_MOVE)
        CPU_PADDLE.start_position_0[0] = CPU_POSITION[0]
        CPU_PADDLE.start_position_1[0] = CPU_PADDLE.start_position_0[0] + CPU_PADDLE.height

    CPU_PADDLE.update(0)
    BALL.update(PADDLE)
    PADDLE.update(0)
    score_update()

    pygame.display.flip()
