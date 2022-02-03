import pygame


def jogging(check, sensor):
    pos = pygame.mouse.get_pos()
    if (pos[0] >= 360 - 280 - 40) and (pos[0] <= 360 - 280 + 40) \
            and (pos[1] >= 440 - 280) and (pos[1] <= 440 + 280) and check:
        return 'The end'
    if sensor == 0 and check:
        return False
    button = [['c', 'del', 'e', 'pi'],
              ['^', 'ln', 'log', '+-'],
              ['sin', 'cos', 'tan', '!'],
              ['7', '8', '9', '/'],
              ['4', '5', '6', '*'],
              ['1', '2', '3', '-'],
              ['0', '.', '=', '+']]
    if check and 0 <= (pos[1] - 160) // 80 <= 6 and 0 <= (pos[0] - 120) // 80 <= 3:
        return button[(pos[1] - 160) // 80][(pos[0] - 120) // 80]


def racing(check, sensor):
    pos = pygame.mouse.get_pos()
    if (pos[0] >= 360 - 280 - 40) and (pos[0] <= 360 - 280 + 40) \
            and (pos[1] >= 440 - 280) and (pos[1] <= 440 + 280) and check:
        return 'The end'
    elif (pos[0] >= 480 - 40) and (pos[0] <= 480 + 40) \
            and (pos[1] >= 520 - 200 + 80) and (pos[1] <= 520 + 200) and check:
        return 'enter'
    if sensor == 0 and check:
        return False
    elif (pos[0] >= 40) and (pos[0] <= 520) \
            and (pos[1] >= 20) and (pos[1] <= 100) and check:
        return 0
    elif (pos[0] >= 40) and (pos[0] <= 200) \
            and (pos[1] >= 100) and (pos[1] <= 160) and check:
        return 1
    elif (pos[0] >= 200) and (pos[0] <= 360) \
            and (pos[1] >= 100) and (pos[1] <= 160) and check:
        return 2
    elif (pos[0] >= 360) and (pos[0] <= 480) \
            and (pos[1] >= 100) and (pos[1] <= 160) and check:
        return 3
    button = [['c', 'del', 'e', 'pi', '('],
              ['^', 'ln(', 'lg(', 'log2(', ')'],
              ['sin(', 'cos(', 'tan(', '+-', 'dif'],
              ['7', '8', '9', '/', 'dif'],
              ['4', '5', '6', '*'],
              ['1', '2', '3', '-'],
              ['0', '.', 'x', '+']]
    if check and 0 <= (pos[1] - 160) // 80 <= 6 and 0 <= (pos[0] - 120) // 80 <= 4:
        return button[(pos[1] - 160) // 80][(pos[0] - 120) // 80]
