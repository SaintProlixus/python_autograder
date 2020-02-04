import math


def f(x, y):
    return ((x + y) ** 3) / math.sqrt((x ** 2 + y ** 2))


def areaTriangle(b, h):
    return (b * h) / 2


def fahr2celsius(f):
    return (f - 32) * 5 / 9


def volumeSphere(r):
    return (4 / 3) * math.pi * r ** 3
