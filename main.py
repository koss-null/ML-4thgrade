import math

import matplotlib.pyplot as pplt

import kdtree
import measures


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
        self.kd_tree = kdtree.KdTree(self.items, split_n, type_cnt_func)


def main():
    keeper = ItemsKeeper("data")
    keeper.read()
    keeper.make_kd_tree(7, measures.border_independent_cnt_type)
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


if __name__ == "__main__":
    main()
