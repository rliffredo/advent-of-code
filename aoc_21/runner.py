import re
import sys
from importlib import import_module
from pathlib import Path
from time import perf_counter_ns

p = Path('.')
day_names = sorted([f.stem for f in p.glob(r"*.py") if re.match(r"\d\d.py", f.name)])


def execute_part(file_name, day_module, part_number, skip_slow):
    f = getattr(day_module, f"part_{part_number}")
    expected_result = getattr(day_module, f"SOLUTION_{part_number}")
    is_slow = getattr(day_module, f"IS_SOLUTION_{part_number}_SLOW", False)
    if is_slow and skip_slow:
        result = expected_result
        elapsed_time_ms = 0
        status = "SKIPPED"
    else:
        start_time = perf_counter_ns()
        result = f(False)
        elapsed_time_ms = (perf_counter_ns() - start_time) / 1_000_000
        status = "OK" if result == expected_result else "ERROR"
    print(f"2021 Day {file_name} Part {part_number}:  {result:>38} [{elapsed_time_ms: >9.3f} ms] {status}")


def run_all_days(skip_slow):
    start_time = perf_counter_ns()
    for file_name in day_names:
        day_module = import_module(file_name)
        execute_part(file_name, day_module, 1, skip_slow)
        execute_part(file_name, day_module, 2, skip_slow)
    elapsed_time_ms = (perf_counter_ns() - start_time) / 1_000_000
    if not skip_slow:
        print(f"\n2021 Total execution time: {elapsed_time_ms: >9.3f} ms")


if __name__ == "__main__":
    run_all_days("all" not in sys.argv)
