class Instruction:
    MODE_INDIRECT = '0'
    MODE_DIRECT = '1'
    MODE_RELATIVE = '2'

    def __init__(self, computer, instruction_info, amt_parameters):
        self.instruction_info = instruction_info
        self.size = amt_parameters + 1  # add opcode
        self.computer = computer
        self.mem = computer.memory
        self.ip = computer.ip
        self.r1 = computer.r1
        self.next_ip = None
        self.stop = False

    def advance_ip(self):
        return self.ip + self.size if self.next_ip is None else self.next_ip

    def fetch(self, i):
        param_address = self.data_address(i)
        if param_address not in self.mem:
            self.mem[param_address] = 0
        param_value = self.mem[param_address]
        return param_value

    def store(self, i, value):
        output_addr = self.data_address(i)
        self.mem[output_addr] = value

    def data_address(self, i):
        mode = self.instruction_info[i - 1]
        if mode == Instruction.MODE_INDIRECT:
            address = self.mem[self.ip + i]
        elif mode == Instruction.MODE_DIRECT:
            address = self.ip + i
        elif mode == Instruction.MODE_RELATIVE:
            address = self.r1 + self.mem[self.ip + i]
        else:
            assert False, 'Invalid mode'
        return address

    def __repr__(self):
        return f'[{type(self).__name__.ljust(8)}] ip: {self.ip}, r1: {self.r1}, size: {self.size}, ' \
               f'mem: {[self.mem[self.ip + m] for m in range(self.size)]}'


class Stop(Instruction):
    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info, 0)
        self.stop = True

    def apply(self):
        pass


class Add(Instruction):
    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info, 3)

    def apply(self):
        self.store(3, self.fetch(1) + self.fetch(2))


class Mul(Instruction):
    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info, 3)

    def apply(self):
        self.store(3, self.fetch(1) * self.fetch(2))


class Input(Instruction):
    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info, 1)

    def apply(self):
        self.store(1, self.computer.input_provider())


class Output(Instruction):
    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info, 1)

    def apply(self):
        self.computer.output_provider(self.fetch(1))


class JumpTrue(Instruction):
    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info, 2)

    def apply(self):
        if self.fetch(1):
            self.next_ip = self.fetch(2)


class JumpFalse(Instruction):
    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info, 2)

    def apply(self):
        if not self.fetch(1):
            self.next_ip = self.fetch(2)


class LessThan(Instruction):
    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info, 3)

    def apply(self):
        self.store(3, 1 if self.fetch(1) < self.fetch(2) else 0)


class Equals(Instruction):
    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info, 3)

    def apply(self):
        self.store(3, 1 if self.fetch(1) == self.fetch(2) else 0)


class AdjustR1(Instruction):
    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info, 1)

    def apply(self):
        self.computer.r1 += self.fetch(1)


class IntCode:
    INSTRUCTIONS = {
        '01': Add,
        '02': Mul,
        '03': Input,
        '04': Output,
        '05': JumpTrue,
        '06': JumpFalse,
        '07': LessThan,
        '08': Equals,
        '09': AdjustR1,
        '99': Stop,
    }

    MAX_PARAMETERS = 4

    def fetch(self, code_data):
        full_opcode = str(code_data).rjust(IntCode.MAX_PARAMETERS + 2, '0')
        if self.debug:
            print(full_opcode)
        opcode = full_opcode[-2:]
        param_modes = list(reversed(full_opcode[:-2]))
        return IntCode.INSTRUCTIONS[opcode], param_modes

    def __init__(self, input_provider=None, output_provider=None, debug=False):
        self.debug = debug
        self.memory = {}
        self.input_provider = input_provider if input_provider else lambda: 999_999_999
        self.output_provider = output_provider if output_provider else print
        # registers
        self.ip = 0
        self.r1 = 0
        # snapshots
        self.mem_backup = {}
        self.ip_backup = 0
        self.r1_backup = 0

    def load(self, program):
        self.memory = {i: int(c) for i, c in enumerate(program.split(','))}
        self.ip = 0
        self.r1 = 0

    def snapshot(self):
        self.mem_backup = {i: k for i, k in self.memory.items()}
        self.ip_backup = self.ip
        self.r1_backup = self.r1

    def restore_snapshot(self):
        self.memory = {i: k for i, k in self.mem_backup.items()}
        self.ip = self.ip_backup
        self.r1 = self.r1_backup

    def set_params(self, noun, verb):
        self.memory[1] = noun
        self.memory[2] = verb

    def execute(self):
        self.ip = 0
        while True:
            # print(self)
            instruction_info = self.memory[self.ip]
            opcode, param_modes = self.fetch(instruction_info)
            instruction = opcode(self, param_modes)
            if self.debug:
                print(instruction)
            if instruction.stop:
                break
            instruction.apply()
            self.ip = instruction.advance_ip()

    def get_output(self):
        return self.memory[0]

    def dump_memory(self, max_values=50):
        return list(self.memory.values())[:max_values]

    def __repr__(self):
        return f'IntCode ip: {self.ip}, r1: {self.r1}, mem: [{self.dump_memory(20)} ...]'
