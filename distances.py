import math


def euclid_dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def manhattan_dist(x1, y1, x2, y2):
    return math.fabs(x2 - x1 + y2 - y1)


def chebishev_dist(x1, y1, x2, y2):
    return max([math.fabs(x2 - x1), math.fabs(y2 - y1)])
