import math


def polynomal_kernel(x, alpha, degree=2, c=5):
    return (math.cos(alpha) * x) ** degree + c


def gaussian_kernel(x):
    return 1 / math.sqrt(2 * math.pi) * (math.e ** (-0.5 * x ** 2))


def logistic_kernel(x):
    return 1 / (math.e ** x * 2 * math.e ** (-x))
