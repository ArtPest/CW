from sympy import diff
import pygame
import math

width, height = 480, 760
white = (255, 255, 255)
black = (0, 0, 0)
light = (150, 150, 150)
azure = (98, 161, 240)
yellow = (225, 225, 3)
orange = (255, 171, 52)


def brackets(a):
    ind = 1
    i = 1
    while ind > 0:
        if a[i] == '(':
            ind += 1
        elif a[i] == ')':
            ind -= 1
        i += 1
    return i


def differ(fnc):
    ind = True
    while ind:
        if 'ln' in fnc:
            pos = fnc.index('ln')
            fnc = fnc[:pos] + 'log' + fnc[pos + 2:]
        elif 'lg' in fnc:
            pos_s = fnc.index('lg')
            pos_e = pos_s + 2 + brackets(fnc[pos_s + 2:])
            a = fnc[:pos_s] + 'log(' + fnc[pos_s + 3:pos_e - 1] + ', 10)' + fnc[pos_e:]
            fnc = a
        elif 'log2' in fnc:
            pos_s = fnc.index('log2')
            pos_e = pos_s + 4 + brackets(fnc[pos_s + 4:])
            fnc = fnc[:pos_s] + 'log(' + fnc[pos_s + 5:pos_e - 1] + ', 2)' + fnc[pos_e:]
        elif 'e' in fnc:
            pos = fnc.index('e')
            fnc = fnc[:pos] + 'E' + fnc[pos + 1:]
        else:
            ind = False
    return fnc


def helper(n, txt):
    while True:
        if n in txt:
            i = txt.index(n)
            if i == 0:
                return True
            elif txt[i - 1] != '.':
                return True
            else:
                txt = txt[i:len(n):]
        else:
            return False


def anti_differ(t):
    info = t
    ind = True
    while ind:
        if 'log' in t:
            pos = t.index('log')
            t = t[:pos] + 'ln' + t[pos + 3:]
            pos = info.index('log')
            info = info[:pos] + 'math.' + info[pos:]
        elif '**' in t:
            pos = t.index('**')
            t = t[:pos] + '^' + t[pos + 2:]
        elif 'sin' in info and helper('sin', info):
            pos = info.index('sin')
            info = info[:pos] + 'math.' + info[pos:]
        elif 'cos' in info and helper('cos', info):
            pos = info.index('cos')
            info = info[:pos] + 'math.' + info[pos:]
        elif 'tan' in info and helper('tan', info):
            pos = info.index('tan')
            info = info[:pos] + 'math.' + info[pos:]
        elif 'E' in info:
            pos = info.index('E')
            info = info[:pos] + 'math.e' + info[pos + 1:]
        elif 'pi' in info and helper('pi', info):
            pos = info.index('pi')
            info = info[:pos] + 'math.' + info[pos:]
        else:
            ind = False
    return t, info


def same(a, op, b):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/' and b != 0:
        return a / b
    elif op == 'log':
        return math.log(abs(a), b)
    elif op == '^':
        return pow(a, b)
    return b


def m(op):
    if op == '+':
        return 'Summarizing. First is '
    elif op == '-':
        return 'Subtraction. First is '
    elif op == '*':
        return 'Multiplication. First is '
    elif op == '/':
        return 'Division. Numerator is '
    elif op == 'log':
        return 'Logarithm. Argument is |'
    elif op == '^':
        return 'Power. Base is '
    return ''


class Layer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((78, 78))
        self.rect = self.image.get_rect()

    def center(self, x, y):
        self.rect.center = (width - 80 * x, 80 * y + 120)

    def update(self, x, y, z, inscription):
        pos = pygame.mouse.get_pos()
        if (pos[0] >= width - 76 * x - 38) and (pos[0] <= width - 76 * x + 38)\
                and (pos[1] >= 76 * (y - 0.5) + 120) and (pos[1] <= 76 * (y + 0.5) + 120):
            if inscription:
                self.image.fill(yellow)
            else:
                self.image.fill(light)
            color = black
        else:
            self.image.fill(black)
            color = white
        f = pygame.font.Font(None, 50)
        text = f.render(z, True, color)
        self.image.blit(text, (5, 18))


class Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((78, 558))
        self.rect = self.image.get_rect()
        self.rect.center = (80, 440)

    def update(self, txt):
        pos = pygame.mouse.get_pos()
        if (pos[0] >= 360 - 280 - 40) and (pos[0] <= 360 - 280 + 40)\
                and (pos[1] >= 440 - 280) and (pos[1] <= 440 + 280):
            self.image.fill(light)
            color = black
        else:
            self.image.fill(black)
            color = white
        f = pygame.font.Font(None, 60)
        text = f.render(txt, True, color)
        self.image.blit(text, (2, 255))


class DisplayBack(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((398, 118))
        self.image.fill(orange)
        self.rect = self.image.get_rect()
        self.rect.center = (240, 80)


class Display(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.buf = [0, 'n']
        self.t = '0'
        self.A = ['del', 'c', '+-']
        self.B = ['.', '!', 'sin', 'cos', 'tan', 'ln', 'pi', 'e']
        self.C = ['=', '+', '-', '*', '/', 'log', '^']
        self.image = pygame.Surface((390, 110))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.center = (240, 80)

    def update(self, txt):
        if txt is None:
            pass

        elif txt in self.A:
            if txt == 'del':
                self.t = self.t[:-1]
                if self.t == '-' or self.t == '':
                    self.t = '0'
            elif txt == 'c':
                self.t = '0'
                self.buf = [0, 'n']
            else:
                if self.t != 0:
                    self.t = str(float(self.t) * -1)

        elif txt in self.B:
            if txt == '!':
                if float(self.t) == float(self.t)//1 and '-' not in self.t and float(self.t) < 20:
                    self.t = str(math.factorial(float(self.t))//1)
            elif txt == 'sin':
                c = float(self.t)
                if abs(c) > 2 * math.pi:
                    c -= 2 * math.pi * (c // (2 * math.pi))
                self.t = str(math.sin(c))
            elif txt == '.':
                if '.' not in self.t:
                    self.t += '.'
            elif txt == 'cos':
                c = float(self.t)
                if abs(c) > 2 * math.pi:
                    c -= 2 * math.pi * (c // (2 * math.pi))
                self.t = str(math.cos(c))
            elif txt == 'tan':
                c = float(self.t)
                if abs(c) > 2 * math.pi:
                    c -= 2 * math.pi * (c // (2 * math.pi))
                self.t = str(math.tan(c))
            elif txt == 'ln':
                if float(self.t) > 0:
                    self.t = str(math.log(abs(float(self.t))))
            elif txt == 'pi':
                if self.t != '0':
                    self.t = str(float(self.t) * math.pi)
                else:
                    self.t = str(math.pi)
            else:
                if self.t != '0':
                    self.t = str(float(self.t) * math.e)
                else:
                    self.t = str(math.e)

        elif txt in self.C:
            if txt == '=':
                self.t = str(same(self.buf[0], self.buf[1], float(self.t)))
                self.buf[0] = 0
                self.buf[1] = 'n'
            else:
                self.buf[0] = same(self.buf[0], self.buf[1], float(self.t))
                self.buf[1] = txt
                self.t = '0'

        elif txt == 'The end':
            pass

        else:
            if 'e' not in self.t:
                if txt == '.' and '.' not in self.t:
                    self.t += txt
                else:
                    if self.t == '0':
                        if txt != '0' and txt != '.':
                            self.t = txt
                    elif len(self.t) < 20:
                        self.t += txt

        if 'e' in self.t:
            a = self.t.index('e')
            if self.t[a + 1] == '-':
                self.t = '0'

        f = pygame.font.Font(None, 40)
        text = f.render(self.t, True, white)
        self.image.fill(black)
        self.image.blit(text, (20, 20))

        if self.buf[0] != 0:
            g = pygame.font.Font(None, 30)
            if self.buf[1] != 'log':
                text = g.render((m(self.buf[1]) + str(self.buf[0])), True, orange)
            else:
                text = g.render((m(self.buf[1]) + str(self.buf[0]) + '|'), True, orange)
            self.image.blit(text, (20, 70))


class GraphBack(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((478, 78))
        self.image.fill(orange)
        self.rect = self.image.get_rect()
        self.rect.center = (280, 60)


class Graph(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.t, self.info = '0', '0'
        self.A = ['del', 'c', '+-', '.']
        self.B = ['sin(', 'cos(', 'tan(', 'ln(', 'lg(', 'log2(', 'e', '^', '+', '-', '*', '/', 'pi']
        self.B_1 = ['^', '+', '-', '*', '/']
        self.C = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.D = ['x', '(', ')']
        self.image = pygame.Surface((470, 70))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.center = (280, 60)

    def update(self, txt):
        if txt is None:
            pass

        elif txt in self.A:
            if txt == 'c':
                self.t = '0'
                self.info = '0'
            elif txt == 'del':
                if self.t[-1] == 'e':
                    self.t = self.t[:-1]
                    self.info = self.info[:-6]
                elif self.t[-2:] == 'pi':
                    self.t = self.t[:-2]
                    self.info = self.info[:-6]
                elif self.t[-4:] in self.B:
                    self.t = self.t[:-4]
                    self.info = self.t[:-9]
                elif self.t[-3:] == 'ln(':
                    self.t = self.t[:-3]
                    self.info = self.info[:-9]
                elif self.t[-3:] == 'lg(':
                    self.t = self.t[:-3]
                    self.info = self.info[:-11]
                else:
                    self.t = self.t[:-1]
                    self.info = self.info[:-1]
                    if self.t == '':
                        self.t = '0'
                        self.info = '0'
                if self.t == '':
                    self.t = '0'
                    self.info = '0'
            elif txt == '+-':
                if not self.t.isdigit():
                    if self.t[0] == '-':
                        self.t = self.t[1:]
                        self.info = self.info[5:]
                    else:
                        self.t = '-' + self.t
                        self.info = '(-1)*' + self.info
                elif float(self.t) != 0:
                    if self.t[0] == '-':
                        self.t = self.t[1:]
                        self.info = self.info[5:]
                    else:
                        self.t = '-' + self.t
                        self.info = '(-1)*' + self.info
            else:
                if self.t[-1] not in self.D and self.t[-1] not in self.B and self.t[-2:] != 'pi':
                    i = -1
                    while self.t[i] in self.C:
                        i -= 1
                        if abs(i) > len(self.t):
                            i += 1
                            break
                    if self.t[i] != '.':
                        self.t += '.'
                        self.info += '.'

        elif txt in self.B and self.t[-1] != '.':
            if self.t == '0':
                self.t = ''
                self.info = ''
            if txt == 'e' or txt == 'pi':
                if self.t != '':
                    if self.t[-1] != '.':
                        if self.t[-1] in self.B_1 or self.t[-1] == '(':
                            self.t += txt
                            self.info += 'math.' + txt
                        elif self.t[-1] == ')' or self.t[-1] in self.C:
                            self.t += '*' + txt
                            self.info += ' * math.' + txt
                else:
                    self.t += txt
                    self.info += 'math.' + txt
            elif len(txt) > 1:
                if self.t != '':
                    if self.t[-1] in self.C or self.t[-1] == 'e' or self.t[-2:] == 'pi':
                        self.t += '*'
                        self.info += '*'
                if txt == 'ln(':
                    self.t += txt
                    self.info += 'math.log('
                elif txt == 'lg(':
                    self.t += txt
                    self.info += 'math.log10('
                elif txt == 'log2(':
                    self.t += 'log2('
                    self.info += 'math.log2('
                else:
                    self.t += txt
                    self.info += 'math.' + txt
            elif self.t != '':
                if txt == '-':
                    if self.t[-1] == '(' or self.t[-1] == 'e' or self.t[-2:] == 'pi':
                        self.t += txt
                        self.info += txt
                    elif self.t[-1] == '-':
                        self.t = self.t[:-1]
                        self.info = self.t[:-1]
                elif (self.t[-1] not in self.B and self.t[-1] != '(') or self.t[-1] == 'e' or self.t[-2:] == 'pi':
                    self.t += txt
                    if txt == '^':
                        self.info += '**'
                    else:
                        self.info += txt

        elif txt in self.C:
            if self.t == '0':
                self.t = ''
                self.info = ''
            if self.t != '':
                if self.t[-1] == 'e' or self.t[-2:] == 'pi':
                    pass
                elif self.t[-1] == ')':
                    self.t += '' + txt
                    self.info += '' + txt
                else:
                    self.t += txt
                    self.info += txt
            else:
                self.t += txt
                self.info += txt

        elif txt in self.D:
            if txt == 'x' and (self.t[-1] == 'x' or self.t[-1] == '.'):
                pass
            elif txt == ')':
                if self.t[-1] != '(' and len(self.t) > 1 and self.t[-1] not in self.B:
                    ind = 0
                    for i in self.t:
                        if i == '(':
                            ind += 1
                        elif i == ')':
                            ind -= 1
                    if ind > 0:
                        self.t += txt
                        self.info += txt
            else:
                if self.t == '0':
                    self.t = ''
                    self.info = ''
                self.t += txt
                self.info += txt

        elif txt == 'dif':
            self.t, self.info = anti_differ(str(diff(differ(self.t))))

        if self.t == '':
            self.t = '0'
            self.info = '0'

        if len(self.t) > 36:
            f = pygame.font.Font(None, int((40 * 36 / len(self.t) // 1)))
        else:
            f = pygame.font.Font(None, 40)
        text = f.render(self.t, True, white)
        self.image.fill(black)
        self.image.blit(text, (20, 20))

    def output(self):
        return self.info


class ExtraButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((78, 318))
        self.rect = self.image.get_rect()
        self.rect.center = (480, 560)

    def update(self, txt):
        pos = pygame.mouse.get_pos()
        if (pos[0] >= 480 - 40) and (pos[0] <= 480 + 40)\
                and (pos[1] >= 520 - 200 + 80) and (pos[1] <= 520 + 200):
            self.image.fill(light)
            color = black
        else:
            self.image.fill(black)
            color = white
        f = pygame.font.Font(None, 30)
        text = f.render(txt, True, color)
        self.image.blit(text, (2, 255))


class TabletBack(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((158, 58))
        self.image.fill(azure)
        self.rect = self.image.get_rect()

    def center(self, x, y):
        self.rect.center = (x, y)


class Tablet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((150, 50))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.t, self.info = '0', '0'
        self.A = ['del', 'c', '+-', '.']
        self.C = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def center(self, x, y):
        self.rect.center = (x, y)

    def update(self, txt):
        if txt is None:
            pass

        elif txt in self.A:
            if txt == 'del':
                self.t = self.t[:-1]
                if self.t == '':
                    self.t = '0'
            elif txt == 'c':
                self.t = '0'
            elif txt == '+-' and self.t != '0':
                if self.t[0] == '-':
                    self.t = self.t[1:]
                else:
                    self.t = '-' + self.t
            else:
                if '.' not in self.t:
                    self.t += '.'

        elif txt in self.C:
            if self.t == '0':
                self.t = txt
            else:
                self.t += txt

        f = pygame.font.Font(None, 40)
        text = f.render(self.t, True, white)
        self.image.fill(black)
        self.image.blit(text, (20, 13))

    def output(self):
        return self.t
