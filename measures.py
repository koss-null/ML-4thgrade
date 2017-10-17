import distances


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
def median_cnt_type(self, brd, cnt_dist_func=distances.chebishev_dist):
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
def border_independent_cnt_type(self, brd, cnt_dist_func=distances.chebishev_dist, n=4):
    middle_x, middle_y = brd.leftx + (brd.rightx - brd.leftx) / 2, brd.lefty + (brd.righty - brd.lefty) / 2

    dist_first_type = map(lambda a: cnt_dist_func(a.x, a.y, middle_x, middle_y),
                          filter(lambda item: item.type == 0, self.items))
    dist_first_type.sort()

    dist_second_type = map(lambda a: cnt_dist_func(a.x, a.y, middle_x, middle_y),
                           filter(lambda item: item.type == 1, self.items))
    dist_second_type.sort()

    diff = sum(dist_first_type[:n]) - sum(dist_second_type[:n])

    if diff < 0:
        return 0
    elif diff > 0:
        return 1
    else:
        return -2
