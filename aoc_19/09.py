from common import read_data, intcode

program = read_data('09')

################
# ## PART 1 ## #
################
computer = intcode.IntCode(lambda: 1)  # 2204990589
computer.load(program)
computer.execute()

################
# ## PART 2 ## #
################
computer = intcode.IntCode(lambda: 2)  # 50008
computer.load(program)
computer.execute()
