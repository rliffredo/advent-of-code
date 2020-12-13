import itertools
from typing import List, Tuple

from common import read_data


def parse_data() -> Tuple[int, List[str]]:
    raw_data = read_data("13", True)
    timestamp = int(raw_data[0])
    bus_lines = raw_data[1].split(",")
    return timestamp, bus_lines


def part_1():
    first_time, bus_lines = parse_data()
    active_buses = sorted(int(bus_number) for bus_number in bus_lines if bus_number != "x")
    for bus_start_time in itertools.count(first_time):
        first_bus = next((bus for bus in active_buses if bus_start_time % bus == 0), None)
        if first_bus:
            break
    else:
        assert False, "intertools.count() is an infinite sequence"
    wait_time = bus_start_time - first_time
    print(f"Waiting {wait_time} minutes for bus {first_bus} -- code: {first_bus * wait_time}")


def part_2():
    _, bus_lines = parse_data()
    # General idea: first iterate only on the first item; as soon as we found
    # the second, let's increase the period.
    # Note that the order does not matter on performance. Initially I was
    # thinking that sorting from largest to smallest on the bus number could
    # help, but I found at least one case where it was not true.
    active_buses = [(int(bus), n) for n, bus in enumerate(bus_lines) if bus != "x"]
    bus_time = abs(active_buses[-1][0] - active_buses[-1][1])
    mcm_buses = 1
    while active_buses:
        next_bus, bus_position = active_buses.pop()
        print(f"Analyzing bus {next_bus} at position {bus_position}")
        # bus position might be greater than bus number, but we are reasoning
        # here in modulo bus_number, so we need to normalize it as well.
        required_time_for_bus = bus_position % next_bus
        # as a simple approach, iterate through all possible solutions for
        # all equations so far to check the first satisfying the current one.
        # We are reasoning in modulo arithmetic, so the solution space is not
        # too big
        for bus_time in itertools.count(bus_time, mcm_buses):
            candidate_bus_time = (next_bus - bus_time) % next_bus
            if candidate_bus_time == required_time_for_bus:
                break
        else:
            assert False, "intertools.count() is an infinite sequence"
        # Assume that all bus numbers are prime, to simplify calculating mcm
        mcm_buses *= next_bus
    print(f"Earliest timestamp is {bus_time}")


part_1()  # 5257
part_2()  # 538703333547789
