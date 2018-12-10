import re
from datetime import datetime
from collections import defaultdict
from collections import Counter

def parse(line):
    guard_match = re.match('\[(.*)\] Guard #(\d+).*', line)
    if guard_match:
        parse.current_state = {}
        parse.current_state['date'] = datetime.strptime(guard_match.groups()[0], '%Y-%m-%d %H:%M')
        parse.current_state['guard'] = int(guard_match.groups()[1])
        return None
    asleep_match = re.match('\[(.*)\] falls asleep', line)
    if asleep_match:
        assert 'guard' in parse.current_state
        parse.current_state['start_sleep'] = datetime.strptime(asleep_match.groups()[0], '%Y-%m-%d %H:%M')
        return None
    awake_match = re.match('\[(.*)\] wakes up', line)
    if awake_match:
        assert 'start_sleep' in parse.current_state and parse.current_state['start_sleep'] is not None
        end_sleep = datetime.strptime(awake_match.groups()[0], '%Y-%m-%d %H:%M')
        start_sleep = parse.current_state['start_sleep']
        parse.current_state['start_sleep'] = None
        sleep_time = end_sleep - start_sleep
        return parse.current_state['guard'], sleep_time, start_sleep, end_sleep
    assert False
parse.current_state = {}


data = open('input_04.txt').readlines()
sleep_intervals = [interval for interval in 
                   (parse(d) for d in sorted(data))
                   if interval is not None]
sleep_counter = defaultdict(int)
for c in sleep_intervals:
    sleep_counter[c[0]] += (c[1].total_seconds() / 60)

max_sleep = max(sleep_counter.keys(), key=(lambda key: sleep_counter[key]))

elf_sleep_intervals = [interval for interval in sleep_intervals if interval[0]==max_sleep]

def minute_generator(interval):
    return [minute for minute in range(interval[2].minute, interval[3].minute)]

minute_counter = Counter()
for interval in elf_sleep_intervals:
    minute_counter.update(minute_generator(interval))

max_minute = max(minute_counter.keys(), key=(lambda key: minute_counter[key]))

print(f'Elf sleeping the most is {max_sleep} '
      f'sleeping on minute  {max_minute} '
      f'with checksum {max_minute * max_sleep}')

##############
all_elf_sleep_intervals = defaultdict(list)
for interval in sleep_intervals:
    all_elf_sleep_intervals[interval[0]].append(interval)

max_minute_per_elf = {}
for elf in all_elf_sleep_intervals:
    elf_minute_counter = Counter()
    for interval in all_elf_sleep_intervals[elf]:
        elf_minute_counter.update(minute_generator(interval))
    max_elf_minute = max(elf_minute_counter.keys(), key=(lambda key: elf_minute_counter[key]))
    max_minute_per_elf[elf] = max_elf_minute, elf_minute_counter[max_elf_minute]

max_elf_on_minute = max(max_minute_per_elf.keys(), key=(lambda key: max_minute_per_elf[key][1]))

print(f'Elf sleeping the most on a certain minute is {max_elf_on_minute} '
      f'sleeping on minute {max_minute_per_elf[max_elf_on_minute][0]} '
      f'with checksum {max_elf_on_minute * max_minute_per_elf[max_elf_on_minute][0]}')
