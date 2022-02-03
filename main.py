import pyqtgraph as pg
from function import graphing
from calculator import running
import math


def chart(func, left, right, accuracy):
    # define the data
    the_title = 'Your graph:'
    mas = []
    while left <= right:
        try:
            x = left
            eval(func)
        except ZeroDivisionError:
            left += accuracy
        except ValueError:
            left += accuracy
        else:
            mas.append(left)
            left += accuracy
    y = []
    for x in mas:
        y.append(eval(func))

    # create plot
    plt = pg.plot(mas, y, title=the_title, pen='r')
    plt.showGrid(x=True, y=True)

    # start Qt event loop.
    if __name__ == 'main':
        import sys
        if sys.flags.interactive != 1 or not hasattr(pg.QtCore, ''):
            pg.QtGui.QApplication.exec()


ind, n, a, b, c = '2', '0', 0, 50, 1
while ind != '0':
    if ind == '2':
        ind = running()
    elif ind == '1':
        ind = graphing()
        if len(ind) > 1:
            n, a, b, c = ind[0], ind[1], ind[2], ind[3]
            ind = '3'
    elif ind == '3':
        chart(n, a, b, c)
        ind = '1'
