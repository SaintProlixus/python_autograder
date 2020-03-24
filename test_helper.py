from random import choice, randint, uniform
from string import ascii_letters
import contextlib
import io
import re


def rand_string(length: int):
    accepted = ascii_letters + ":?!@#$*)(&^" + " "
    output = ""
    for _ in range(length):
        output += choice(accepted)
    return output


def rand_iterable(iter_pars: tuple):
    for par in iter_pars:

        return


def build_param(par, min_val: int, max_val: int):
    if par == str:
        length = randint(min_val, max_val)
        return rand_string(length)
    elif par == int:
        return randint(min_val, max_val)
    elif par == float:
        return uniform(min_val, max_val)
    elif type(par) == list:
        full_par = list()
        for i in range(randint(min_val, max_val)):
            full_par.append(build_param(*par))
        return full_par
    elif type(par) == tuple:
        if par[0] == "choice":
            return build_param(choice(par[1]), min_val, max_val)
        else:
            full_par = tuple()
            for i in range(randint(min_val, max_val)):
                full_par += (build_param(*par),)
            return full_par


def test_params(pars: tuple, min_val=None, max_val=None):
    output = list()
    for par in pars.values():
        par_type = par["type"]
        min_val, max_val = par["range"]
        output.append(build_param(par_type, min_val, max_val))
    return tuple(output)


def check_print(func, params):
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        func(*params)
    output = f.getvalue()
    return re.findall(r'\d+', output)


def generate_tests(funcs, num):
    test_battery = dict()
    for func in funcs.keys():
        test_battery[func] = dict()
        test_battery[func]["tests"] = dict()
        for i in range(num):
            test_name = f"test{i}"
            params = tuple()
            if funcs[func]["include"] is None or i > len(funcs[func]["include"])-1:
                init_params = test_params(funcs[func]["pars"])
                acc_type = funcs[func]["acc_type"]
                for e in init_params:
                    if type(e) == list:
                        params += (e[:],)
                    else:
                        params += (e,)
                # params = tuple(params)
            else:
                params = funcs[func]["include"][i]
            try:
                if "print" in acc_type:
                    expected = check_print(funcs[func]["call"], params)
                else:
                    expected = funcs[func]["call"](*params)
            except Exception as e:
                expected = e
            test_battery[func]["tests"][test_name] = {"params": params, "expected": expected, "acc_type": acc_type}
    return test_battery
