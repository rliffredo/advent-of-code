class Instruction:
    MODE_INDIRECT = 0
    MODE_DIRECT = 1
    MODE_RELATIVE = 2

    stop = False
    size = 1  # opcode at a very minimum

    __slots__ = ['instruction_info', 'computer', 'mem', 'next_ip']

    def __init__(self, computer, instruction_info):
        self.instruction_info = instruction_info
        self.computer = computer
        self.mem = computer.memory
        self.next_ip = None

    def advance_ip(self):
        return self.computer.ip + self.size if self.next_ip is None else self.next_ip

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
        if mode is Instruction.MODE_DIRECT:
            return self.computer.ip + i
        elif mode is Instruction.MODE_RELATIVE:
            return self.computer.r1 + self.mem[self.computer.ip + i]
        else:  # mode is Instruction.MODE_INDIRECT:
            return self.mem[self.computer.ip + i]

    def __repr__(self):
        return f'[{type(self).__name__.ljust(8)}] ip: {self.computer.ip}, r1: {self.computer.r1}, size: {self.size}, ' \
               f'mem: {[self.mem[self.computer.ip + m] for m in range(self.size)]}'


class Start(Instruction):
    def __init__(self, computer):
        super().__init__(computer, (0, 0, 0))
        self.next_ip = 0

    def apply(self):
        pass


class Stop(Instruction):
    stop = True

    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info)

    def apply(self):
        pass


class Add(Instruction):
    size = 4

    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info)

    def apply(self):
        self.store(3, self.fetch(1) + self.fetch(2))


class Mul(Instruction):
    size = 4

    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info)

    def apply(self):
        self.store(3, self.fetch(1) * self.fetch(2))


class Input(Instruction):
    size = 2

    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info)

    def apply(self):
        self.store(1, self.computer.input_provider())


class Output(Instruction):
    size = 2

    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info)

    def apply(self):
        self.computer.output_provider(self.fetch(1))


class JumpTrue(Instruction):
    size = 3

    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info)

    def apply(self):
        if self.fetch(1):
            self.next_ip = self.fetch(2)


class JumpFalse(Instruction):
    size = 3

    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info)

    def apply(self):
        if not self.fetch(1):
            self.next_ip = self.fetch(2)


class LessThan(Instruction):
    size = 4

    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info)

    def apply(self):
        self.store(3, 1 if self.fetch(1) < self.fetch(2) else 0)


class Equals(Instruction):
    size = 4

    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info)

    def apply(self):
        self.store(3, 1 if self.fetch(1) == self.fetch(2) else 0)


class AdjustR1(Instruction):
    size = 2

    def __init__(self, computer, instruction_info):
        super().__init__(computer, instruction_info)

    def apply(self):
        self.computer.r1 += self.fetch(1)


class IntCode:
    INSTRUCTIONS = {
        1: Add,
        2: Mul,
        3: Input,
        4: Output,
        5: JumpTrue,
        6: JumpFalse,
        7: LessThan,
        8: Equals,
        9: AdjustR1,
        99: Stop,
    }

    MAX_PARAMETERS = 4
    instructions_cache = {}

    def fetch(self, code_data):
        if code_data not in self.instructions_cache:
            opcode = code_data % 100
            p1 = (code_data // 100) % 10
            p2 = (code_data // 1000) % 10
            p3 = (code_data // 10000) % 10
            self.instructions_cache[code_data] = IntCode.INSTRUCTIONS[opcode], (p1, p2, p3)
        return self.instructions_cache[code_data]

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
        instruction = Start(self)
        while not instruction.stop:
            self.ip = instruction.advance_ip()
            instruction_info = self.memory[self.ip]
            opcode, param_modes = self.fetch(instruction_info)
            instruction = opcode(self, param_modes)
            instruction.apply()

    def get_output(self):
        return self.memory[0]

    def dump_memory(self, max_values=50):
        return list(self.memory.values())[:max_values]

    def __repr__(self):
        return f'IntCode ip: {self.ip}, r1: {self.r1}, mem: [{self.dump_memory(20)} ...]'
