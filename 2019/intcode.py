class Instruction:
    def __init__(self, computer, ip, instruction_info, amt_parameters):
        self.instruction_info = instruction_info
        self.size = amt_parameters + 1  # add opcode
        self.computer = computer
        self.mem = computer.program
        self.ip = ip
        self.next_ip = None
        self.stop = False

    def advance_ip(self):
        return self.ip + self.size if self.next_ip is None else self.next_ip

    def fetch(self, i):
        param_address = self.data_address(i)
        param_value = self.mem[param_address]
        return param_value

    def store(self, i, value):
        output_addr = self.data_address(i)
        self.mem[output_addr] = value

    def data_address(self, i):
        mode_indirect = self.instruction_info[i-1] == '0'
        param_address = self.mem[self.ip + i] if mode_indirect else self.ip + i
        return param_address

    def __repr__(self):
        return f'[{type(self).__name__.ljust(8)}] ip: {self.ip}, size: {self.size},' \
               f'mem: {[self.mem[self.ip+m] for m in range(self.size)]}'


class Stop(Instruction):
    def __init__(self, computer, ip, instruction_info):
        super().__init__(computer, ip, instruction_info, 0)
        self.stop = True

    def apply(self):
        pass


class Add(Instruction):
    def __init__(self, computer, ip, instruction_info):
        super().__init__(computer, ip, instruction_info, 3)

    def apply(self):
        self.store(3, self.fetch(1) + self.fetch(2))


class Mul(Instruction):
    def __init__(self, computer, ip, instruction_info):
        super().__init__(computer, ip, instruction_info, 3)

    def apply(self):
        self.store(3, self.fetch(1) * self.fetch(2))


class Input(Instruction):
    def __init__(self, computer, ip, instruction_info):
        super().__init__(computer, ip, instruction_info, 1)

    def apply(self):
        self.store(1, self.computer.input_provider())


class Output(Instruction):
    def __init__(self, computer, ip, instruction_info):
        super().__init__(computer, ip, instruction_info, 1)

    def apply(self):
        print(self.fetch(1))


class JumpTrue(Instruction):
    def __init__(self, computer, ip, instruction_info):
        super().__init__(computer, ip, instruction_info, 2)

    def apply(self):
        if self.fetch(1):
            self.next_ip = self.fetch(2)


class JumpFalse(Instruction):
    def __init__(self, computer, ip, instruction_info):
        super().__init__(computer, ip, instruction_info, 2)

    def apply(self):
        if not self.fetch(1):
            self.next_ip = self.fetch(2)


class LessThan(Instruction):
    def __init__(self, computer, ip, instruction_info):
        super().__init__(computer, ip, instruction_info, 3)

    def apply(self):
        self.store(3, 1 if self.fetch(1) < self.fetch(2) else 0)


class Equals(Instruction):
    def __init__(self, computer, ip, instruction_info):
        super().__init__(computer, ip, instruction_info, 3)

    def apply(self):
        self.store(3, 1 if self.fetch(1) == self.fetch(2) else 0)


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

    def __init__(self, input_provider=None, debug=False):
        self.debug = debug
        self.program = {}
        self.backup = {}
        self.input_provider = input_provider if input_provider else lambda: 999_999_999

    def load(self, program):
        self.program = {i: int(c) for i, c in enumerate(program.split(','))}

    def snapshot(self):
        self.backup = {i: k for i, k in self.program.items()}

    def reset(self):
        self.program = {i: k for i, k in self.backup.items()}

    def set_params(self, noun, verb):
        self.program[1] = noun
        self.program[2] = verb

    def execute(self):
        ip = 0
        while True:
            instruction_info = self.program[ip]
            opcode, param_modes = self.fetch(instruction_info)
            instruction = opcode(self, ip, param_modes)
            if self.debug:
                print(instruction)
            if instruction.stop:
                break
            instruction.apply()
            ip = instruction.advance_ip()

    def get_output(self):
        return self.program[0]

    def dump_memory(self, max_values=50):
        return list(self.program.values())[:max_values]
