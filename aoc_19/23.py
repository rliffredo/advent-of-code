import queue
import threading
from time import sleep

from common import read_data, intcode


class NetworkShutdown(Exception):
    pass


class NetworkInterface:

    def __init__(self, nic_id, mq):
        self.computer = intcode.IntCode(self.provide_input, self.collect_output, debug=True)
        self.nic_id = nic_id
        self.computer.load(read_data("23"))
        self.all_queues = mq
        self.own_queue = mq[nic_id]
        self.out_message = []
        self.in_message = [nic_id]
        self.thread = None
        self.terminated = False

    @property
    def is_idle(self):
        return len(self.in_message) == 0 and self.own_queue.empty()

    def run(self):
        def try_run():
            try:
                self.computer.execute()
            except NetworkShutdown:
                pass

        self.thread = threading.Thread(target=try_run)
        self.thread.start()

    def collect_output(self, value):
        if self.terminated:
            raise NetworkShutdown()
        self.out_message.append(value)
        if len(self.out_message) == 3:
            address = self.out_message[0]
            message = self.out_message[1:]
            self.all_queues[address].put(message)
            self.out_message.clear()

    def provide_input(self):
        if self.terminated:
            raise NetworkShutdown()

        sleep(0.0001)  # Let other thread wake-up and do some work
        if not self.own_queue.empty():
            message = self.own_queue.get()
            self.in_message.append(message[0])
            self.in_message.append(message[1])

        ret = self.in_message.pop(0) if self.in_message else -1
        return ret


def start_network(nat_function):
    all_queues = {nic_id: queue.Queue() for nic_id in range(50)}
    all_queues[255] = queue.Queue()  # nat queue
    all_nic = [NetworkInterface(nic_id, all_queues) for nic_id in range(50)]

    for nic in all_nic:
        nic.run()

    return nat_function(all_queues[255], all_nic)


def stop_network(all_nic):
    for nic in all_nic:
        nic.terminated = True
        nic.thread.join()


################
# ## PART 1 ## #
################

def get_first_y_to_nat():
    def stopping_nat(nat_queue, all_nic):
        while True:
            msg = nat_queue.get(block=True)
            stop_network(all_nic)
            return msg[1]

    return start_network(stopping_nat)


print(f'NAT received Y {get_first_y_to_nat()}')  # 22877


################
# ## PART 2 ## #
################


def get_first_double_wake_message():
    def monitoring_nat(nat_queue, all_nic):
        wake_message = None
        last_message = nat_queue.get(block=True)
        while True:
            sleep(0.1)
            while not nat_queue.empty():
                last_message = nat_queue.get()

            # Check all cards
            network_idle = all(nic.is_idle for nic in all_nic)
            if network_idle:
                if wake_message == last_message:
                    stop_network(all_nic)
                    return last_message
                wake_message = last_message
                all_nic[0].own_queue.put(wake_message)

    return start_network(monitoring_nat)


print(f'NAT waked network twice with {get_first_double_wake_message()}')  # 15210
