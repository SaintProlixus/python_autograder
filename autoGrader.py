from pathlib import Path
import importlib.util
import math
import pandas as pd
import argparse


def get_func(func: str):
    try:
        func_call = getattr(mod, func)
    except AttributeError:
        func_call = None
    return func_call


def construct_df(funcs: list):
    columns = ["name", "blazer_id"]
    columns += funcs
    df = pd.DataFrame(columns=columns)
    return df


def get_student_info(mod, mod_path: str):
    try:
        student = mod.myName()
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
        import_status = True
        try:
            spec = importlib.util.spec_from_file_location("sub", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        except Exception:
            import_status = False
        func_feedback = get_student_info(mod, str(path))
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
                        expected = tests[test]["expected"]
                        try:
                            result = func_call(*params)
                            type_check = isinstance(result, tests[test]["acc_type"])
                            correct = "Correct"
                            if type_check is False:
                                correct = "Incorrect"
                                message = "Incorrect return type. "
                                if message not in feedback:
                                    feedback += message
                            elif type(expected) == float:
                                if math.isclose(expected, result, abs_tol=0.000001):
                                    correct = "Correct"
                            elif expected != result:
                                correct = "Incorrect"
                                message = "Incorrect result. "
                                if message not in feedback:
                                    feedback += message
                            if correct == "Correct":
                                test_results["num_passed"] += 1
                        except Exception as e:
                            test_results["num_passed"] = 0
                            feedback = f"{type(e)}: {str(e)}"
                    if test_results["num_passed"] == test_results["num_tests"]:
                        test_results["correct"] = "Correct"
                    else:
                        test_results["feedback"] = feedback
                else:
                    test_results["feedback"] = "Missing function/incorrect name"
            func_feedback.append(
                f"{test_results['correct']}; {test_results['num_passed']}/{test_results['num_tests']}; {test_results['feedback']}"
            )
        df.loc[i] = func_feedback
    df.to_excel(f"results/{config.ASSIGNMENT}.xlsx", freeze_panes=(1, 1), index=False)
