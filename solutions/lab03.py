def listInsert(l2, x):
    l2.append(x)
    return sorted(l2, reverse=True)


def mailingCost(d):
    if d <= 50:
        return d * 5.0
    elif d > 50 and d <= 200:
        return d * 4.25
    elif d > 200 and d <= 500:
        return d * 3.95
    else:
        return d * 3.7


def str2tuple(s3, s4):
    return tuple(s3 + s4)


def tupleLast3(t2):
    assert len(t2) > 3
    return t2[-3]
