import pygame
pygame.init()

V_HITS_COUNT = 0
H_HITS_COUNT = 0
HORIZONTAL_HITS_COUNT = 0
WIDTH = 1200
HEIGHT = 600
BORDER = 10
BORDER_COLOR = pygame.Color('RED')
BALL_COLOR = pygame.Color('WHITE')
BACKGROUND_COLOR = pygame.Color('BLACK')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
SPEED = 1
EXIT = False
SCORE = 0


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

    def update(self):
        global BACKGROUND_COLOR, BALL_COLOR, WIDTH, HEIGHT, BORDER, V_HITS_COUNT, H_HITS_COUNT
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
    def __init__(self, x=80, y=20):
        self.width = x
        self.height = y
        self.start_position_x = [WIDTH/2 + self.height/2, HEIGHT - 2 * BORDER]
        self.start_position_y = [WIDTH/2 - self.height/2, HEIGHT - 2 * BORDER]

    def show(self, color):
        global screen
        pygame.draw.line(screen, color, self.start_position_x,
                         self.start_position_y, 10)

    def update(self, how_much):
        self.show(BACKGROUND_COLOR)
        self.start_position_x[0] += how_much
        self.start_position_y[0] += how_much
        self.show(BALL_COLOR)


BALL = Ball(WIDTH - BORDER, HEIGHT//2, SPEED, SPEED)

PADDLE = Paddle(200, 40)

pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect((0, 0), (WIDTH, BORDER)))

pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(0, 0, BORDER, HEIGHT))

pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(WIDTH - BORDER, 0, BORDER, HEIGHT))

pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(0, HEIGHT - BORDER, WIDTH, BORDER))

while not EXIT:
    for event in pygame.event.get():
        if 'mod' in event.__dir__():
            if event.unicode == 'a':
                print(event.unicode, 'EVENT UNICODE')
                PADDLE.update(-20)
            elif event.unicode == 'd':
                print(event.unicode, 'EVENT UNICODE')
                PADDLE.update(20)
            else:
                pass

        elif event.type == 32787:
            EXIT = True
            break
        else:
            break
    PADDLE.update(0)
    BALL.update()
    pygame.display.flip()
