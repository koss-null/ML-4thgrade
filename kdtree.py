import math

import matplotlib.pyplot as pplt

def draw_rectangle(brd1, type):
    if type == 0:
        clr = (0, 1, 0)
    elif type == 1:
        clr = (1, 0, 0)

    if type != -2:
        pplt.plot([brd1.leftx, brd1.leftx, brd1.rightx, brd1.rightx, brd1.leftx],
                  [brd1.lefty, brd1.righty, brd1.righty, brd1.lefty, brd1.lefty],
                  color=clr)

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
        splits = 80
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
