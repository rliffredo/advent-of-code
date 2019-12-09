import itertools
import queue
import threading

import intcode
from common import read_data


class Amplifier:
    def __init__(self, amp_id, program, phase_setting):
        self.phase_setting = phase_setting
        self.amplifier_output = 0
        self.amplifier_input = 0
        self.sent_settings = False
        self.computer = intcode.IntCode(input_provider=self._get_input, output_provider=self._capture_output)
        self.computer.load(program)
        self.amp_id = amp_id
        self.input_line = queue.Queue()
        self.next_amp = None
        self.thread = threading.Thread(target=self.computer.execute)

    def start(self):
        self.thread.start()

    def _capture_output(self, value):
        self.amplifier_output = value
        if self.next_amp:
            self.next_amp.input_line.put(self.amplifier_output)

    def _get_input(self):
        if not self.sent_settings:
            self.sent_settings = True
            return self.phase_setting
        else:
            self.amplifier_input = self.input_line.get()
            return self.amplifier_input

    def __repr__(self):
        return f'[Amp {self.amp_id}] / {self.phase_setting}] i: {self.amplifier_input} o: {self.amplifier_output}'


def best_amp_output(program, phase_range):
    best_output = 0
    best_phases = None
    for phase_values in itertools.permutations(range(*phase_range)):
        amplifiers = []
        for amp_id, phase_value in enumerate(phase_values):
            amplifier = Amplifier(amp_id, program, phase_value)
            amplifiers.append(amplifier)
            if amp_id:
                amplifiers[amp_id - 1].next_amp = amplifier
        amplifiers[-1].next_amp = amplifiers[0]

        for amplifier in amplifiers:
            amplifier.start()

        amplifiers[0].input_line.put(0)

        for amplifier in amplifiers:
            amplifier.thread.join()

        thrust = amplifiers[-1].amplifier_output
        best_output, best_phases = (thrust, phase_values) if thrust > best_output else (best_output, best_phases)

    return best_output, best_phases


final_output = best_amp_output(read_data("07"), (0, 5))
print(final_output)  # 116680

feedback_output = best_amp_output(read_data("07"), (5, 10))
print(feedback_output)  # 89603079
