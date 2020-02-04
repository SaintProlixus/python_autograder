import math


def f(x):
    return 5 * x - 3


def areaCircle(r):
    return math.pi * r**2


def nSnookerBall(nRow):
    return (nRow * (nRow + 1)) // 2


def eApproximately(n):
    return (1 + 1/n)**n


def volCone(r, h):
    return 1/3 * math.pi * r**2 * h


def distOrigin(x, y):
    return math.sqrt(x**2 + y**2)


def lengthSegment(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
