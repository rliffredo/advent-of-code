import re
from importlib import import_module
from pathlib import Path
from time import perf_counter_ns

p = Path('.')
day_names = sorted([f.stem for f in p.glob(r"*.py") if re.match(r"\d\d.py", f.name)])


def execute_part(file_name, day_module, part_number):
    f = getattr(day_module, f"part_{part_number}")
    expected_result = getattr(day_module, f"SOLUTION_{part_number}")
    start_time = perf_counter_ns()
    res_1 = f(False)
    elapsed_time_ms = (perf_counter_ns() - start_time) / 1_000_000
    res_1_status = "OK" if res_1 == expected_result else "ERROR"
    print(f"2020 day {file_name} Part {part_number}:  {res_1:15} [{elapsed_time_ms: >8.3f}ms] {res_1_status}")


def run_all_days():
    for file_name in day_names:
        day_module = import_module(file_name)
        execute_part(file_name, day_module, 1)
        execute_part(file_name, day_module, 2)


if __name__ == "__main__":
    run_all_days()
