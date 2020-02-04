from random import choice, randint, uniform
from string import ascii_letters


def rand_string(length: int):
    accepted = ascii_letters + " "
    output = ""
    for _ in range(length):
        output += choice(accepted)
    return output


def test_params(pars: tuple, min_val: int, max_val: int):
    output = tuple()
    for par in pars:
        if par == str:
            length = randint(min_val, max_val)
            output += (rand_string(length),)
        elif par == int:
            output += (randint(min_val, max_val),)
        elif par == float:
            output += (uniform(min_val, max_val),)
    return output
