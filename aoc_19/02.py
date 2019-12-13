from common import read_data, intcode


################
# ## PART 1 ## #
################

def execute_1202():
    computer = intcode.IntCode()
    computer.load(read_data("02"))
    computer.memory[1] = 12
    computer.memory[2] = 2
    computer.execute()
    return computer.memory[0]


print(f'Memory at position 0: {execute_1202()}')  # 4023471


################
# ## PART 2 ## #
################

def find_params_for_19_690_720():
    computer = intcode.IntCode()
    computer.load(read_data("02"))
    computer.snapshot()
    for noun in range(100):
        for verb in range(100):
            computer.memory[1] = noun
            computer.memory[2] = verb
            computer.execute()
            result = computer.memory[0]
            if result == 19_690_720:
                return noun * 100 + verb
            computer.restore_snapshot()
    return None


print(f'Parameter to get 19_690_720: {find_params_for_19_690_720()}')  # 8051
