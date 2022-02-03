import pygame
from mapping import racing
from sprites import Layer, Button,\
    GraphBack, Graph, ExtraButton, TabletBack,\
    Tablet

A = ['.', '+', '-', '*', '/', '**']
B = ['(', ')', 'dif']
button = [['c', 'del', 'e', 'π'],
          ['^', 'ln', 'lg', 'log'],
          ['sin', 'cos', 'tan', '±'],
          ['7', '8', '9', '÷'],
          ['4', '5', '6', '×'],
          ['1', '2', '3', '-'],
          ['0', '.', 'x', '+']]


def graphing():
    width, height, index, bracket = 560, 760, 0, 0
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Calculator")
    all_sprites = pygame.sprite.Group()
    win0, win1, win2, win3, ind = '', '', '', '', '0'
    f, g, run, check1, check2, c = False, False, True, False, True, False
    spr, ext, tablet = [], [], []
    for x in range(7):
        spr.append([])
        for y in range(4):
            spr[x].append(Layer())
            spr[x][y].center(y + 1, x + 1)
    for i in range(3):
        ext.append(Layer())
        ext[i].center(0, i + 1)
    for i in range(2):
        tablet.append([])
        for j in range(3):
            if i == 0:
                tablet[i].append(TabletBack())
            else:
                tablet[i].append(Tablet())
            tablet[i][j].center(120 + j * 160, 130)
    but1 = Button()
    but2 = ExtraButton()
    display1 = GraphBack()
    display2 = Graph()
    all_sprites.add(spr[i][j] for i in range(7) for j in range(4))
    all_sprites.add(tablet[0][i] for i in range(3))
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
        for i in range(3):
            ext[i].update(0, i + 1, B[i], c)
        but1.update('CM')
        but2.update('Enter')
        all_sprites.add(spr[i][j] for i in range(7) for j in range(4))
        all_sprites.add(ext[i] for i in range(3))
        all_sprites.add(tablet[1][i] for i in range(3))
        all_sprites.add(but1, but2, display1, display2)
        if racing(check1, 1) == 0:
            index = 0
        if racing(check1, 1) == 1:
            index = 1
        if racing(check1, 1) == 2:
            index = 2
        if racing(check1, 1) == 3:
            index = 3
        if index == 0:
            display2.update(racing(check1, 1))
        elif index == 1:
            tablet[1][0].update(racing(check1, 1))
        elif index == 2:
            tablet[1][1].update(racing(check1, 1))
        elif index == 3:
            tablet[1][2].update(racing(check1, 1))
        all_sprites.draw(screen)
        pygame.display.flip()
        screen.fill((50, 50, 50))
        check1 = racing(check1, 0)
        if racing(check1, 1) == 'The end':
            run = False
            f = True
        win0, win1 = display2.output(), tablet[1][0].output()
        win2, win3 = tablet[1][1].output(), tablet[1][2].output()
        if racing(check1, 1) == 'enter' and float(win3) > 0:
            if float(win1) < float(win2) and (float(win2) - float(win1)) / float(win3) > 1:
                run = False
                g = True
    pygame.quit()
    if f:
        return '2'
    elif g:
        if win0[-1] in A:
            win0 += '0'
        for i in win0:
            if i == '(':
                bracket += 1
            elif i == ')':
                bracket -= 1
        if bracket != 0:
            win0 += ')' * bracket
        return win0, float(win1), float(win2), float(win3)
    return ind
