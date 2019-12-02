class Instruction:
    def __init__(self, mem, ip, size, output_offset, operation, input_params):
        self.input_params = input_params
        self.output_offset = output_offset
        self.size = size
        self.mem = mem
        self.ip = ip
        self.operation = operation

    def apply(self):
        if not self.operation:
            return False
        op_params = [self.mem[self.mem[self.ip + i]] for i in self.input_params]
        output_addr = self.mem[self.ip + self.output_offset]
        new_value = self.operation(*op_params)
        self.mem[output_addr] = new_value
        return True


class Add(Instruction):
    def __init__(self, mem, ip):
        super().__init__(mem, ip, 4, 3, lambda x, y: x + y, [1, 2])


class Mul(Instruction):
    def __init__(self, mem, ip):
        super().__init__(mem, ip, 4, 3, lambda x, y: x * y, [1, 2])


class Stop(Instruction):
    def __init__(self, mem, ip):
        super().__init__(mem, ip, 0, 0, None, [])


class IntCode:
    INSTRUCTIONS = {
        1: Add,
        2: Mul,
        99: Stop,
    }

    def __init__(self):
        self.program = []
        self.backup = []

    def load(self, program):
        self.program = [int(c) for c in program.split(',')]

    def snapshot(self):
        self.backup = [n for n in self.program]

    def reset(self):
        self.program = [n for n in self.backup]

    def set_params(self, noun, verb):
        self.program[1] = noun
        self.program[2] = verb

    def execute(self):
        ip = 0
        while True:
            opcode = self.program[ip]
            instruction = IntCode.INSTRUCTIONS[opcode](self.program, ip)
            if not instruction.apply():
                break
            ip += instruction.size

    def get_output(self):
        return self.program[0]
