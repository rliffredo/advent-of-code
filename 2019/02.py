import intcode


################
# ## PART 1 ## #
################


def execute_1202():
    computer = intcode.IntCode()
    computer.load(intcode.read_data("data/02.txt"))
    computer.set_params(12, 2)
    computer.execute()
    return computer.get_output()


print(f'Memory at position 0: {execute_1202()}')  # 4023471


################
# ## PART 2 ## #
################

def find_params_for_19_690_720():
    computer = intcode.IntCode()
    computer.load(intcode.read_data('data/02.txt'))
    computer.snapshot()
    for noun in range(100):
        for verb in range(100):
            computer.set_params(noun, verb)
            computer.execute()
            result = computer.get_output()
            if result == 19_690_720:
                return noun * 100 + verb
            computer.reset()
    return None


print(f'Parameter to get 19_690_720: {find_params_for_19_690_720()}')  # 8051
