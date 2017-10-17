import random
import time

import matplotlib.pyplot as pplt

import kdtree
import measures
import accuracy


class DataItem:
    def __init__(self, x, y, type):
        self.x, self.y, self.type = x, y, int(type)


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

    def draw(self):
        for i in range(len(self.items)):
            if self.items[i].type == 0:
                clr = (0, 0, 0)
            else:
                clr = (1, 1, 1)
            pplt.plot([self.items[i].x], [self.items[i].y],
                      'ro',
                      color=clr)

    def new_plot(self):
        pplt.cla()
        pplt.clf()

    def make_kd_tree(self, split_n, type_cnt_func, fold_borders):
        self.kd_tree = kdtree.KdTree(
            self.items[:fold_borders[0]] + self.items[fold_borders[1]:],
            split_n, type_cnt_func)

    def shuffle(self):
        random.shuffle(self.items)


def main():
    keeper = ItemsKeeper("data")
    keeper.read()
    keeper.shuffle()

    fold_range = {}
    for fold_step in range(5, 10, 1):
        l_fld_brd, r_fld_brd = 0, fold_step
        errors = []
        while r_fld_brd < len(keeper.items):
            keeper.make_kd_tree(7, measures.border_independent_cnt_type, (l_fld_brd, r_fld_brd))
            for item in keeper.items:
                # adding 1 'cause -0 is eq to 0
                if keeper.kd_tree.search(item.x, item.y) == item.type:
                    errors.append(item.type + 1)
                else:
                    errors.append(-(item.type + 1))

            l_fld_brd += fold_step
            r_fld_brd += fold_step
            keeper.new_plot()

        acc = accuracy.f_measure(errors)
        print 'for fold step = ', fold_step, ' f-measure is ', acc
        fold_range[acc] = fold_step

    print 'maximum accuracy was with step = ', fold_range[max(fold_range.keys())]

    keeper.make_kd_tree(7, measures.border_independent_cnt_type, (0, 0))
    keeper.draw()

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


if __name__ == "__main__":
    main()
