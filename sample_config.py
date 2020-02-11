import importlib.util
import test_helper


GLOB_STR = "*.py"  # This will be a general way to id submission files. Alter as needed.
ASSIGNMENT = "assignment_name"  # This should be changed and be consistent with across assignment.

#  Do not change any of the 3 lines below
spec = importlib.util.spec_from_file_location("sub", f"solutions/{ASSIGNMENT}.py")
solutions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solutions)


func_table = {  # Change values below as needed
    "function_name1": {  # The name of a function
        "call": solutions.function_name1,  # Should match function_name
        "pars": (float,),  # Tuple representation of parameter types (note: single parameter needs a comma after)
        "range": (-1000, 1000),  # Range of randomized parameter (range for numbers/length of str)
        "acc_type": (float, int)  # What return types are accepted by the function
        },
    "listSample": {
        "call": solutions.listSample,
        "range": (1, 5),  # Here, the range specifies number of items in the list
        "pars": ([int, 2, 5], float),  # Inside the list/tuple setup is [type, min_val, max_val]
        "acc_type": (list,)
        },
}


def generate_tests(funcs, num):  # Do not alter this function!!!
    test_battery = dict()
    for func in funcs.keys():
        test_battery[func] = dict()
        test_battery[func]["tests"] = dict()
        for i in range(num):
            test_name = f"test{i}"
            init_params = test_helper.test_params(funcs[func]["pars"], *funcs[func]["range"])
            params = list()
            for e in init_params:
                if type(e) == list:
                    params.append(e[:])
                else:
                    params.append(e)
            params = tuple(params)
            try:
                expected = funcs[func]["call"](*params)
            except Exception as e:
                expected = e
            acc_type = funcs[func]["acc_type"]
            test_battery[func]["tests"][test_name] = {"params": init_params, "expected": expected, "acc_type": acc_type}
    return test_battery


funcs = generate_tests(func_table, 10000)  # The number in this parameter set can be altered to adjust number of tests
