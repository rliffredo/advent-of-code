from common import read_data, intcode


class SpringDroidProgrammer:

    def __init__(self):
        self.computer = intcode.IntCode(self.provide_input, self.collect_output)
        self.computer.load(read_data("21"))
        self.springscript = None
        self.hull_picture = []
        self.hull_damage = 0

    def run(self, script: str):
        assert script[-5:] == 'WALK\n' or script[-4:] == "RUN\n"
        assert len(script.split('\n')) < 16
        self.springscript = (c for c in script)
        self.computer.execute()

    def collect_output(self, value):
        if value > 128:
            # Success!
            self.hull_damage = value
        else:
            # Getting a map
            self.hull_picture.append(chr(value))

    def provide_input(self):
        return ord(next(self.springscript))

    def report(self):
        if self.hull_damage > 0:
            print(f"The measured damaga to the hull was {self.hull_damage}")
        else:
            print('Unfortunately, the mission failed. We have the last view:')
        print("".join(self.hull_picture))


################
# ## PART 1 ## #
################

# (d and not a) or (d and not b) or (d and not c)
# d and not (a and b and c)
springscript = """
NOT A T
NOT T T
AND B T
AND C T
NOT T T
AND D T
NOT T T
NOT T J
WALK
"""[1:]

programmer = SpringDroidProgrammer()
programmer.run(springscript)
programmer.report()  # 19347868


################
# ## PART 2 ## #
################

# ((d and h) and not (a and b and c)) or ((d and h) and not (a and b and c))
# ((d and h) or (d and e)) and not (a and b and c)
# (d and (h or e)) and not (a and b and c)
springscript = """
NOT A T
NOT T T
AND B T
AND C T
NOT T T
NOT E J
NOT J J
OR H J
AND D J
AND T J
RUN
"""[1:]


programmer = SpringDroidProgrammer()
programmer.run(springscript)
programmer.report()  # 1142479667


