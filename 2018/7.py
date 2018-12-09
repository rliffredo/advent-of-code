import re

def parse(line):
    m = re.match('Step ([A-Z]) must be finished before step ([A-Z]) can begin', line)
    try:
        return tuple(m.groups())
    except:
        print(line)
        raise

def predecessors(step_to_check):
    return [step[0] for step in instructions if step[1]==step_to_check]

def remaining_predecessors(step):
    return (step for step in predecessors(step) if step not in ordered_steps)

def has_remaining_predecessors(step):
    return any(True for predecessor in remaining_predecessors(step))

def basic_order():
    return map(chr, range(ord('A'), ord('Z')+1))

data = open('input_7.txt').readlines()
instructions = [parse(d) for d in data]
ordered_steps = []
all_steps = list(basic_order())
while len(ordered_steps) < len(all_steps):
    for step in all_steps:
        if step in ordered_steps:
            continue
        if not has_remaining_predecessors(step):
            ordered_steps.append(step)
            break

steps_in_order = ''.join(ordered_steps)
print(f'Instructions are: {steps_in_order}')

##################

def successors(step_to_check):
    return [step[1] for step in instructions if step[0]==step_to_check]

def get_step_lenght(step):
    return 60 + ord(step) - ord('A') + 1

def is_completed(step_to_check, clock):
    task = next(t for t in all_tasks if t[0]==step_to_check)
    return task[1] is not None and task[1] <= clock

def is_taken(step_to_check):
    task = next(t for t in all_tasks if t[0]==step_to_check)
    return task[1] is not None

def is_task_available(step_to_check, clock):
    if is_taken(step_to_check):
        return False
    return all(is_completed(pred, clock) for pred in predecessors(step_to_check)) 

def get_next_task(clock):
    try:
        t = next(task for task in all_tasks if is_task_available(task[0], clock))
        return t, all_tasks.index(t)
    except StopIteration:
        return None, None

def get_next_worker():
    m = min(workers)
    w = workers.index(m)
    return w, m

def get_max_task_time():
    try:
        return max(t[1] for t in all_tasks if t[1] is not None)
    except:
        return 0

#print('worker\twclock\tclock\ttask\tfclock')
all_tasks = [(step, None) for step in ordered_steps]
workers = [0] * 5
while any(task[1] is None for task in all_tasks):
    worker, wclock = get_next_worker()
    assert 0 <= worker < 5
    task = None
    clock = wclock
    while not task:
        task, i = get_next_task(clock)
        if not task:
            clock += 1
    fclock = clock + get_step_lenght(task[0])
    all_tasks[i] = (all_tasks[i][0], fclock)
    workers[worker] = fclock
    #print(f'{worker}\t{wclock}\t{clock}\t{task[0]}\t{fclock}')

print(f'Last worker finishes at: {max(workers)}')

# 1147