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
                distFirstType += math.sqrt((item.x - x) ** 2 + (item.y - y) ** 2)
            else:
                distSecondType += math.sqrt((item.x - x) ** 2 + (item.y - y) ** 2)
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


class kdTree:
    class border:
        def __init__(self, leftx, lefty, rightx, righty):
            # left lower, right, upper
            self.leftx, self.lefty, self.rightx, self.righty = leftx, lefty, rightx, righty
            self.decision = -1

        def contains(self, x, y):
            return self.rightx >= x >= self.leftx and self.righty >= y >= self.lefty

        def setDecision(self, decision):
            self.decision = decision

    class node:
        def __init__(self, brd):
            self.brd = brd
            self.left = None
            self.right = None
            self.type = -1

    def __init__(self, items, splitN):
        self.items = items
        eps = 0.00001
        self.headNode = self.node(
            self.border(
                min([i.x for i in items]) + eps, min([i.y for i in items]) + eps,
                max([i.x for i in items]) + eps, max([i.y for i in items]) + eps
            ))
        self.makeBoarding(False, self.headNode.brd, self.headNode, splitN)

    # implements SAH heruistic
    def doSAH(self, items, initBorder, isHorisonal):
        splits = 20
        step = 0
        cur = 0
        stop = 0
        if isHorisonal:
            step = math.fabs(initBorder.rightx - initBorder.leftx) / splits
            cur = min(initBorder.rightx, initBorder.leftx)
            stop = max(initBorder.rightx, initBorder.leftx)
        else:
            step = math.fabs(initBorder.righty - initBorder.lefty) / splits
            cur = min(initBorder.righty, initBorder.lefty)
            stop = max(initBorder.righty, initBorder.lefty)

        #shows (dots from left side of line) - (dots from right side)
        leftGreaterThenRight = []
        while cur < stop:
            if isHorisonal:
                leftGreaterThenRight.append(
                    sum(1 for item in self.items if item.x < cur and initBorder.contains(item.x, item.y)) -
                    sum(1 for item in self.items if item.x >= cur and initBorder.contains(item.x, item.y))
                )
            else:
                leftGreaterThenRight.append(
                    sum(1 for item in self.items if item.y < cur and initBorder.contains(item.x, item.y)) -
                    sum(1 for item in self.items if item.y >= cur and initBorder.contains(item.x, item.y))
                )
            cur += step

        i = 0
        minDif = 100000000.0
        itemI = 0
        for item in leftGreaterThenRight:
            if item < minDif:
                minDif = item
                itemI = i
            i += 1

        if isHorisonal:
            cur = min(initBorder.rightx, initBorder.leftx)
            cur += step * itemI
            return [self.border(initBorder.leftx, initBorder.lefty, initBorder.rightx, cur),
                    self.border(initBorder.leftx, cur, initBorder.rightx, initBorder.righty)]
        else:
            cur = min(initBorder.righty, initBorder.lefty)
            cur += step * itemI
            return [self.border(initBorder.leftx, initBorder.lefty, cur, initBorder.righty),
                    self.border(cur, initBorder.lefty, initBorder.rightx, initBorder.righty)]

    def cntType(self, brd):
        first, second = 0,0
        for item in self.items:
            if brd.contains(item.x, item.y):
                if item.type == 0:
                    first += 1
                else:
                    second += 1
        if first > second:
            return 0
        else:
            return 1

    def makeBoarding(self, isHorisontal, initBorder, node, splitN):
            newBorders = self.doSAH(self.items, initBorder, isHorisontal)
            node.left, node.right = self.node(newBorders[0]), self.node(newBorders[1])
            splitN -= 1
            if splitN > 0:
                self.makeBoarding(not isHorisontal, newBorders[0], node.left, splitN)
                self.makeBoarding(not isHorisontal, newBorders[1], node.right, splitN)
            else:
                node.left.type, node.right.type = self.cntType(node.left.brd), self.cntType(node.right.brd)

    #return only type of node
    def search(self, x, y):
        node = self.headNode
        while node.type == -1:
            if node.left.brd.contains(x, y):
                node = node.left
            else:
                node = node.right
        return node.type


ceeper = ItemsCeeper("data")
ceeper.read()
tree = kdTree(ceeper.items, 5)
ceeper.read()
ceeper.draw()
ceeper.addDot(0.111, -0.829)
time.sleep(1000)
