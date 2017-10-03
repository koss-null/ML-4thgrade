from matplotlib.colors import ListedColormap
import pylab as pl
import math
import numpy as np
import time


class DataItem:
    def __init__(self, x, y, type):
        self.x, self.y, self.type = x, y, int(type)


class ItemsCeeper:
    def __init__(self, filename):
        self.filename = filename
        self.items = []

    def read(self):
        file = open(self.filename, "r")
        lines = file.readlines()
        for line in lines:
            nums = map(lambda arr: float(arr), line.split(","))
            self.items.append(DataItem(nums[0], nums[1], nums[2]))
        return self.items

    def countDist(self, x, y):
        distFirstType, distSecondType = 0, 0
        for item in self.items:
            if item.type == 0:
                distFirstType += math.sqrt((item.x - x)**2 + (item.y - y)**2)
            else:
                distSecondType += math.sqrt((item.x - x)**2 + (item.y - y)**2)
        if distFirstType < distSecondType:
            return 0
        else:
            return 1

    def draw(self):
        classColormap = ListedColormap(['#FF0000', '#00FF00'])
        pl.scatter([self.items[i].x for i in range(len(self.items))],
                   [self.items[i].y for i in range(len(self.items))],
                   c=[self.items[i].type for i in range(len(self.items))],
                   cmap=classColormap)

    def addDot(self, x, y):
        type = self.countDist(x, y)
        classColormap = ListedColormap(['#FFAA00', '#AAFF00'])
        pl.scatter([x], [y], c=[type], cmap=classColormap)
        print("catigorised as", type)
        pl.show()


ceeper = ItemsCeeper("data")
ceeper.read()
ceeper.draw()
ceeper.addDot(0.111, -0.829)
time.sleep(1000)


