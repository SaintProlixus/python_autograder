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
    "function_name2": {
        "call": solutions.function_name2,
        "range": (0, 1000),
        "pars": (int, float),
        "acc_type": (float,)
        },
}


def generate_tests(funcs, num):  # Do not alter this function
    test_battery = dict()
    for func in funcs.keys():
        test_battery[func] = dict()
        test_battery[func]["tests"] = dict()
        for i in range(num):
            test_name = f"test{i}"
            params = test_helper.test_params(funcs[func]["pars"], *funcs[func]["range"])
            expected = funcs[func]["call"](*params)
            acc_type = funcs[func]["acc_type"]
            test_battery[func]["tests"][test_name] = {"params": params, "expected": expected, "acc_type": acc_type}
    return test_battery


funcs = generate_tests(func_table, 1000)  # The number in this parameter set can be altered to adjust number of tests
