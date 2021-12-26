import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))

while True:
    for event in pygame.event.get():
        if 'mod' in event.__dir__():
            if event.unicode == 'a':
                print(event.unicode, 'EVENT UNICODE')
                print(event.key, 'EVENT KEY')
                print(event.mod, 'MOD EVENT')
                print(event.type, 'TYPE EVENT')
                print(event.scancode, 'SCAN CODE')

