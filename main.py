import random
import time

import matplotlib.pyplot as pplt

import kdtree
import measures
import accuracy
import spatial_transforms as st
import kernel
import distances


class DataItem:
    def __init__(self, x, y, type, transform):
        recnt_coords = transform(x, y)
        self.x, self.y, self.type = recnt_coords[0], recnt_coords[1], int(type)


class ItemsKeeper:
    def __init__(self, filename, st_func):
        self.filename = filename
        self.items = []
        self.kd_tree = None
        self.st_func = st_func

    def read(self):
        file = open(self.filename, "r")
        lines = file.readlines()
        for line in lines:
            nums = map(lambda arr: float(arr), line.split(","))
            self.items.append(DataItem(nums[0], nums[1], nums[2], self.st_func))
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

    def make_kd_tree(self, split_n, type_cnt_func, fold_borders, dist_func=distances.chebishev_dist):
        self.kd_tree = kdtree.KdTree(
            self.items[:fold_borders[0]] + self.items[fold_borders[1]:],
            split_n, type_cnt_func, dist_func)

    def shuffle(self):
        random.shuffle(self.items)


def main():
    keeper = ItemsKeeper("data", st.mult)
    keeper.read()
    keeper.shuffle()

    msrs = [measures.naive_cnt_type, measures.border_independent_cnt_type, measures.median_cnt_type]
    dists = [distances.chebishev_dist, distances.euclid_dist, distances.manhattan_dist, distances.minkowski_distance]

    if True:
        fold_range = {}
        for fold_step in range(7, 15, 1):
            l_fld_brd, r_fld_brd = 0, fold_step
            errors = []
            for msr in msrs:
                for dist in dists:
                    print 'msr type = ', msr
                    print 'dist type = ', dist
                    while r_fld_brd < len(keeper.items):
                        keeper.make_kd_tree(5, msr, (l_fld_brd, r_fld_brd), dist)
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
                    fold_range[acc] = [fold_step, msr, dist, kernel.gaussian_kernel]

        print 'maximum accuracy was with fold = ', fold_range[max(fold_range.keys())]

    keeper.make_kd_tree(7, measures.border_independent_cnt_type, (0, 0))
    keeper.draw()

    if True:
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
