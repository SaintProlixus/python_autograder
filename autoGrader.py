from pathlib import Path
import importlib.util
import math
import pandas as pd
import argparse
import test_helper
from contextlib import contextmanager
import sys, os


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def get_func(func: str):
    try:
        func_call = getattr(mod, func)
    except AttributeError:
        func_call = None
    return func_call


def construct_df(funcs: list):
    columns = ["name", "blazer_id", "num_correct"]
    columns += funcs
    df = pd.DataFrame(columns=columns)
    return df


def get_student_info(mod, mod_path: str):
    try:
        student = mod.myName().split()
        student = f"{student[-1]}, {' '.join(student[0:-1])}"
    except Exception:
        student = mod_path.split("_")[0].split("/")[2]
    try:
        blazer_id = mod.myBlazerID()
    except Exception:
        blazer_id = ""
    return [student, blazer_id]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file name")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("sub", f"configs/{args.config}")
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    pathlist = [p for p in Path("./submissions/" + config.ASSIGNMENT).glob(config.GLOB_STR)]
    funcs = config.funcs
    df = construct_df(funcs)
    for i in range(len(pathlist)):
        path = pathlist[i]
        print(f"{i+1}/{len(pathlist)}: {path}")
        import_status = True
        try:
            with suppress_stdout():
                spec = importlib.util.spec_from_file_location("sub", path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
        except Exception:
            import_status = False
        func_feedback = get_student_info(mod, str(path))
        grade = [0, len(funcs)]
        for func in funcs:
            func_data = funcs[func]
            tests = func_data["tests"]
            func_call = get_func(func)
            test_results = {
                "num_passed": 0,
                "num_tests": len(tests),
                "correct": "Incorrect",
                "feedback": "",
            }
            if not import_status:
                test_results = {
                    "num_passed": 0,
                    "num_tests": len(tests),
                    "correct": "Incorrect",
                    "feedback": "Import Error: Code execution is broken.",
                }
            else:
                if func_call and import_status:
                    feedback = ""
                    for test in tests:
                        params = tests[test]["params"]
                        # params = list()
                        # for e in init_params:
                        #     if type(e) == list:
                        #         params.append(e[:])
                        #     else:
                        #         params.append(e)
                        # params = tuple(params)
                        expected = tests[test]["expected"]
                        acc_type = tests[test]["acc_type"]
                        try:
                            if "print" in acc_type:
                                result = test_helper.check_print(func_call, params)
                                type_check = True
                            else:
                                result = func_call(*params)
                                type_check = type(result) == type(expected)
                            correct = "Correct"
                            if type_check is False:
                                correct = "Incorrect"
                                message = f"Incorrect return type. {type(result)} | {type(expected)}; Params: {params}; Expected: {expected}; Result: {result} "
                                if "Incorrect return type." not in feedback:
                                    feedback += message
                            elif type(expected) == float:
                                if math.isclose(expected, result, abs_tol=0.000001):
                                    correct = "Correct"
                                elif expected != result:
                                    correct = "Incorrect"
                                    message = f"Incorrect result. Params: {params}; Expected: {expected}; Result: {result} "
                                    if "Incorrect result." not in feedback:
                                        feedback += message
                            elif type(expected) == str:
                                if expected.strip() == result.strip():
                                    correct = "Correct"
                                else:
                                    correct = "Incorrect"
                                    message = f"Incorrect result. Params: {params}; Expected: {expected}; Result: {result} "
                                    if "Incorrect result." not in feedback:
                                        feedback += message
                            elif expected != result:
                                correct = "Incorrect"
                                message = f"Incorrect result. Params: {params}; Expected: {expected}; Result: {result} "
                                if "Incorrect result." not in feedback:
                                    feedback += message
                            if correct == "Correct":
                                test_results["num_passed"] += 1
                        except Exception as e:
                            if type(e) == type(expected):
                                test_results["num_passed"] += 1
                            else:
                                test_results["num_passed"] = 0
                                feedback = f"{type(e)}: {str(e)} Params: {params}"
                    if test_results["num_passed"] == test_results["num_tests"]:
                        test_results["correct"] = "Correct"
                        grade = [grade[0]+1, grade[1]]
                    else:
                        test_results["feedback"] = feedback
                else:
                    test_results["feedback"] = "Missing function/incorrect name. "
            func_feedback.append(
                f"{test_results['correct']}; {test_results['num_passed']}/{test_results['num_tests']}; {test_results['feedback']}"
            )
        func_feedback.insert(2, f"{grade[0]}/{grade[1]} correct")
        df.loc[i] = func_feedback
    df.to_excel(f"results/{config.ASSIGNMENT}.xlsx", freeze_panes=(1, 3), index=False)
