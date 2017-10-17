import math
import kernel as kn


def euclid_dist(x1, y1, x2, y2, kernel=kn.gaussian_kernel):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def manhattan_dist(x1, y1, x2, y2, kernel=kn.gaussian_kernel):
    return math.fabs(x2 - x1 + y2 - y1)


def chebishev_dist(x1, y1, x2, y2, kernel=kn.gaussian_kernel):
    return max([math.fabs(x2 - x1), math.fabs(y2 - y1)])


def minkowski_distance(x, y, p=3, kernel=kn.gaussian_kernel):
    ret = 0
    for i in range(0, min(x.size, y.size)):
        ret += (abs(x[i] - y[i])) ** p
    return ret ** (1 / p)
