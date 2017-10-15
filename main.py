import math

import matplotlib.pyplot as pplt


class DataItem:
    def __init__(self, x, y, type):
        self.x, self.y, self.type = x, y, int(type)


def draw_rectangle(brd1):
    pplt.plot([brd1.leftx, brd1.leftx, brd1.rightx, brd1.rightx, brd1.leftx],
              [brd1.lefty, brd1.righty, brd1.righty, brd1.lefty, brd1.lefty])


class ItemsKeeper:
    def __init__(self, filename):
        self.filename = filename
        self.items = []
        self.kd_tree = None

    def read(self):
        file = open(self.filename, "r")
        lines = file.readlines()
        for line in lines:
            nums = map(lambda arr: float(arr), line.split(","))
            self.items.append(DataItem(nums[0], nums[1], nums[2]))
        return self.items

    def count_dist(self, x, y):
        dist_first_type, dist_second_type = 0, 0
        for item in self.items:
            if item.type == 0:
                dist_first_type += math.sqrt((item.x - x) ** 2 + (item.y - y) ** 2)
            else:
                dist_second_type += math.sqrt((item.x - x) ** 2 + (item.y - y) ** 2)
        if dist_first_type < dist_second_type:
            return 0
        else:
            return 1

    def draw(self):
        pplt.plot([self.items[i].x for i in range(len(self.items))],
                  [self.items[i].y for i in range(len(self.items))],
                  c=[self.items[i].type for i in range(len(self.items))])

    def make_kd_tree(self, split_n):
        self.kd_tree = KdTree(self.items, split_n)


class KdTree:
    class Border:
        def __init__(self, leftx, lefty, rightx, righty):
            # left lower, right, upper
            self.leftx, self.lefty, self.rightx, self.righty = leftx, lefty, rightx, righty
            self.decision = -1

        def contains(self, x, y):
            return self.rightx >= x >= self.leftx and self.righty >= y >= self.lefty

        def set_decision(self, decision):
            self.decision = decision

    class Node:
        def __init__(self, brd):
            self.brd = brd
            self.left = None
            self.right = None
            self.type = -1

    def __init__(self, items, split_n):
        self.items = items
        eps = 0.00001
        self.headNode = self.Node(
            self.Border(
                min([i.x for i in items]) + eps, min([i.y for i in items]) + eps,
                max([i.x for i in items]) + eps, max([i.y for i in items]) + eps
            ))
        self.make_boarding(False, self.headNode.brd, self.headNode, split_n)

    # implements SAH heruistic
    def do_sah(self, items, init_border, is_horisontal):
        splits = 20
        step = 0
        cur = 0
        stop = 0
        if not is_horisontal:
            step = math.fabs(init_border.rightx - init_border.leftx) / splits
            cur = min(init_border.rightx, init_border.leftx)
            stop = max(init_border.rightx, init_border.leftx)
        else:
            step = math.fabs(init_border.righty - init_border.lefty) / splits
            cur = min(init_border.righty, init_border.lefty)
            stop = max(init_border.righty, init_border.lefty)

        # shows (dots from left side of line) - (dots from right side)
        left_greater_then_right = []
        while cur < stop:
            if not is_horisontal:
                left_greater_then_right.append(
                    sum(1 for item in self.items if item.x < cur and init_border.contains(item.x, item.y)) -
                    sum(1 for item in self.items if item.x >= cur and init_border.contains(item.x, item.y))
                )
            else:
                left_greater_then_right.append(
                    sum(1 for item in self.items if item.y < cur and init_border.contains(item.x, item.y)) -
                    sum(1 for item in self.items if item.y >= cur and init_border.contains(item.x, item.y))
                )
            cur += step

        i = 0
        min_dif = 100000000.0
        item_i = 0
        for item in left_greater_then_right:
            if item < math.fabs(min_dif):
                min_dif = item
                item_i = i
            i += 1

        if not is_horisontal:
            cur = min(init_border.rightx, init_border.leftx)
            cur += step * item_i
            return [self.Border(init_border.leftx, init_border.lefty, init_border.rightx, cur),
                    self.Border(init_border.leftx, cur, init_border.rightx, init_border.righty)]
        else:
            cur = min(init_border.righty, init_border.lefty)
            cur += step * item_i
            return [self.Border(init_border.leftx, init_border.lefty, cur, init_border.righty),
                    self.Border(cur, init_border.lefty, init_border.rightx, init_border.righty)]

    def cnt_type(self, brd):
        first, second = 0, 0
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

    def make_boarding(self, isHorisontal, initBorder, node, splitN):
        newBorders = self.do_sah(self.items, initBorder, isHorisontal)
        node.left, node.right = self.Node(newBorders[0]), self.Node(newBorders[1])
        splitN -= 1

        # print 'borders1: ', newBorders[0].leftx, newBorders[0].lefty, newBorders[0].rightx, newBorders[0].righty
        # print 'borders2: ', newBorders[1].leftx, newBorders[1].lefty, newBorders[1].rightx, newBorders[1].righty

        if splitN > 0:
            self.make_boarding(not isHorisontal, newBorders[0], node.left, splitN)
            self.make_boarding(not isHorisontal, newBorders[1], node.right, splitN)
        else:
            node.left.type, node.right.type = self.cnt_type(node.left.brd), self.cnt_type(node.right.brd)
        draw_rectangle(newBorders[0])
        draw_rectangle(newBorders[1])

    # return only type of node
    def search(self, x, y):
        node = self.headNode
        while node.type == -1:
            if node.left.brd.contains(x, y):
                node = node.left
            else:
                node = node.right
        return node.type


keeper = ItemsKeeper("data")
keeper.read()
keeper.make_kd_tree(3)
keeper.read()
keeper.draw()
i = 0.0
while i < 2.0:
    print keeper.kd_tree.search(i, 0.229)
    keeper.kd_tree.search(i, 0.229)
    i += 0.001
pplt.show()