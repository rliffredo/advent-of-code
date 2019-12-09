import intcode
from common import read_data


def execute_diag(system_id):
    computer = intcode.IntCode(lambda: system_id)
    computer.load(read_data("05"))
    computer.execute()


print('[Part 1] Diagnostics for system 1')
execute_diag(1)  # 12234644

print('[Part 2] Diagnostics for system 5')
execute_diag(5)  # 3508186
