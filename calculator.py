import pygame
from sprites import Layer, Button, DisplayBack, Display
from mapping import jogging

button = [['c', 'del', 'e', 'π'],
          ['^', 'ln', 'log', '±'],
          ['sin', 'cos', 'tan', '!'],
          ['7', '8', '9', '÷'],
          ['4', '5', '6', '×'],
          ['1', '2', '3', '-'],
          ['0', '.', '=', '+']]


def running():
    width, height = 480, 760
    ind = '0'
    f, run, check1, check2, c = False, True, False, True, False
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Calculator")
    all_sprites = pygame.sprite.Group()
    spr = []
    for x in range(7):
        spr.append([])
        for y in range(4):
            spr[x].append(Layer())
            spr[x][y].center(y + 1, x + 1)
    all_sprites.add(spr[i][j] for i in range(7) for j in range(4))
    but = Button()
    display1 = DisplayBack()
    display2 = Display()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                c = True
                if check2:
                    check2 = False
                    check1 = True
            if event.type == pygame.MOUSEBUTTONUP:
                check2 = True
                c = False
        for i in range(7):
            for j in range(4):
                spr[i][j].update(j + 1, i + 1, button[i][3 - j], c)
        but.update('FM')
        all_sprites.add(spr[i][j] for i in range(7) for j in range(4))
        all_sprites.add(but, display1, display2)
        display2.update(jogging(check1, 1))
        all_sprites.draw(screen)
        pygame.display.flip()
        screen.fill((50, 50, 50))
        check1 = jogging(check1, 0)
        if jogging(check1, 0) == 'The end':
            run = False
            f = True
    pygame.quit()
    if f:
        ind = '1'
    return ind
