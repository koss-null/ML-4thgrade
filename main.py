import math

import matplotlib.pyplot as pplt


class DataItem:
    def __init__(self, x, y, type):
        self.x, self.y, self.type = x, y, int(type)


def draw_rectangle(brd1, type):
    if type == 0:
        clr = (0, 1, 0)
    elif type == 1:
        clr = (1, 0, 0)

    if type != -2:
        pplt.plot([brd1.leftx, brd1.leftx, brd1.rightx, brd1.rightx, brd1.leftx],
                  [brd1.lefty, brd1.righty, brd1.righty, brd1.lefty, brd1.lefty],
                  color=clr)


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
        for i in range(len(self.items)):
            if self.items[i].type == 0:
                clr = (0, 0, 0)
            else:
                clr = (1, 1, 1)
            pplt.plot([self.items[i].x], [self.items[i].y],
                      'ro',
                      color=clr)

    def make_kd_tree(self, split_n, type_cnt_func):
        self.kd_tree = KdTree(self.items, split_n, type_cnt_func)


class KdTree:
    class Border:
        def __init__(self, leftx, lefty, rightx, righty):
            # left lower, right, upper
            self.leftx, self.lefty, self.rightx, self.righty = leftx, lefty, rightx, righty

        def contains(self, x, y):
            return self.rightx >= x >= self.leftx and self.righty >= y >= self.lefty

    class Node:
        def __init__(self, brd):
            self.brd = brd
            self.left = None
            self.right = None
            self.type = -1

    def __init__(self, items, split_n, type_cnt_func):
        self.items = items
        self.type_cnt_func = type_cnt_func
        eps = 0.00001
        self.headNode = self.Node(
            self.Border(
                min([i.x for i in items]) + eps, min([i.y for i in items]) + eps,
                max([i.x for i in items]) + eps, max([i.y for i in items]) + eps
            ))
        self.make_boarding(False, self.headNode.brd, self.headNode, split_n)

    # implements SAH heruistic
    def do_sah(self, init_border, is_horisontal):
        splits = 40
        step, cur, stop = 0, 0, 0
        if not is_horisontal:
            step = math.fabs(init_border.rightx - init_border.leftx) / splits
            cur = init_border.leftx
            stop = init_border.rightx
        else:
            step = math.fabs(init_border.righty - init_border.lefty) / splits
            cur = init_border.lefty
            stop = init_border.righty

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
            cur = init_border.leftx
            cur += step * item_i
            return [self.Border(init_border.leftx, init_border.lefty, cur, init_border.righty),
                    self.Border(cur, init_border.lefty, init_border.rightx, init_border.righty)]
        else:
            cur = init_border.lefty
            cur += step * item_i
            return [self.Border(init_border.leftx, init_border.lefty, init_border.rightx, cur),
                    self.Border(init_border.leftx, cur, init_border.rightx, init_border.righty)]

    def make_boarding(self, isHorisontal, initBorder, node, splitN):
        newBorders = self.do_sah(initBorder, isHorisontal)
        node.left, node.right = self.Node(newBorders[0]), self.Node(newBorders[1])
        splitN -= 1

        if splitN > 0:
            self.make_boarding(not isHorisontal, newBorders[0], node.left, splitN)
            self.make_boarding(not isHorisontal, newBorders[1], node.right, splitN)
        else:
            node.left.type = self.type_cnt_func(self, node.left.brd)
            node.right.type = self.type_cnt_func(self, node.right.brd)
            draw_rectangle(newBorders[0], node.left.type)
            draw_rectangle(newBorders[1], node.right.type)

    # return only type of node
    def search(self, x, y):
        node = self.headNode
        while node.type == -1:
            if node.left.brd.contains(x, y):
                node = node.left
            else:
                node = node.right
        if node.type == 0:
            clr = (0, 1, 0)
        elif node.type == 1:
            clr = (1, 0, 0)
        else:
            clr = (0.8, 0.8, 0.8)
        pplt.plot([x], [y], 'ro', color=clr)
        return node.type


# here comes different variable functions

# counting distance

def euclid_dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# counting border type
# in some of this functions we are using cnt_dist_func
# it's necessary to set default cnt_dist_func
# in case it is not to be provided inside k-tree

def naive_cnt_type(self, brd):
    first, second = 0, 0
    for item in self.items:
        if brd.contains(item.x, item.y):
            if item.type == 0:
                first += 1
            else:
                second += 1
    if first > second:
        return 0
    elif second > first:
        return 1
    else:
        return -2


# if naive returns -2 we are counting more carefully
def mediana_cnt_type(self, brd, cnt_dist_func=euclid_dist):
    naive = naive_cnt_type(self, brd)
    if naive == -2:
        first, second = 0, 0
        middle_x, middle_y = (brd.rightx - brd.leftx) / 2, (brd.righty - brd.lefty) / 2
        for item in self.items:
            if brd.contains(item.x, item.y):
                if item.type == 0:
                    first += cnt_dist_func(middle_x, middle_y, item.x, item.y)
                else:
                    second += cnt_dist_func(middle_x, middle_y, item.x, item.y)
        if first < second:
            return 0
        elif second < first:
            return 1
        else:
            return -2
    else:
        return naive


# count middle of brd and take first n nearest dots from each type
# and sums their distance
# TODO: make n average dot number inside of border
# TODO: fix it, doesnt work
def border_independent_cnt_type(self, brd, cnt_dist_func=euclid_dist, n=4):
    middle_x, middle_y = (brd.rightx - brd.leftx) / 2, (brd.righty - brd.lefty) / 2

    dist_first_type = map(lambda a: cnt_dist_func(a.x, a.y, middle_x, middle_y), filter(lambda item: item.type == 0, self.items))
    dist_first_type.sort()

    dist_second_type = map(lambda a: cnt_dist_func(a.x, a.y, middle_x, middle_y), filter(lambda item: item.type == 1, self.items))
    dist_second_type.sort()

    print(dist_first_type)
    print(dist_second_type)

    diff = sum(dist_first_type[:n]) - sum(dist_second_type[:n])

    if diff < 0:
        return 0
    elif diff > 0:
        return 1
    else:
        return -2


keeper = ItemsKeeper("data")
keeper.read()
keeper.make_kd_tree(6, border_independent_cnt_type)
keeper.read()
if False:
    x, y = -0.9, -0.7
    for i in range(50):
        for j in range(50):
            keeper.kd_tree.search(x, y)
            x += 0.04
        y += 0.04
        x = -0.9
keeper.draw()
pplt.show()
