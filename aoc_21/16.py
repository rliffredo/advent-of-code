import math

from common import read_data


class BitsPacket:
    HEADER_SIZE = 6

    def __new__(cls, *args, **kwargs):
        bit_data = args[0] or kwargs.get("bit_data")
        packet_type = int(bit_data[3:6], base=2)
        if packet_type == 4:
            cls = BitsLiteral
        elif packet_type == 0:
            cls = BitsSum
        elif packet_type == 1:
            cls = BitsProduct
        elif packet_type == 2:
            cls = BitsMinimum
        elif packet_type == 3:
            cls = BitsMaximum
        elif packet_type == 5:
            cls = BitsGreaterThan
        elif packet_type == 6:
            cls = BitsLessThan
        elif packet_type == 7:
            cls = BitsEqual

        return super().__new__(cls)

    def __init__(self, bit_data: str):
        self.version = int(bit_data[:3], base=2)
        self.type = int(bit_data[3:6], base=2)

    def value(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def version_sum(self):
        raise NotImplementedError


class BitsLiteral(BitsPacket):

    def version_sum(self):
        return self.version

    def __init__(self, bit_data: str):
        super().__init__(bit_data)
        literal_bit_data = ''
        dp = BitsPacket.HEADER_SIZE
        self.segments = 0
        while True:
            self.segments += 1
            current_segment = bit_data[dp:dp+5]
            literal_bit_data += current_segment[1:]
            if current_segment[0] == "0":
                break
            dp += 5

        total_data_len = dp + 5
        padding = 4 - (total_data_len % 4)
        padded_data = ""  # bit_data[total_data_len:total_data_len+padding]
        self._bit_data = literal_bit_data + padded_data
        self._value = int(literal_bit_data, base=2)

    def value(self):
        return self._value

    def __len__(self):
        return BitsPacket.HEADER_SIZE + self.segments * 5


class BitsOperator(BitsPacket):

    def version_sum(self):
        return self.version + sum(p.version_sum() for p in self.packets)

    def __init__(self, bit_data: str):
        super().__init__(bit_data)
        self.length_type = bit_data[BitsPacket.HEADER_SIZE]
        if self.length_type == "0":
            binary_packet_data_len = bit_data[BitsPacket.HEADER_SIZE+1:BitsPacket.HEADER_SIZE+16]
            packet_data_len = int(binary_packet_data_len, base=2)
            packet_data = bit_data[BitsPacket.HEADER_SIZE+16:BitsPacket.HEADER_SIZE+16+packet_data_len]
            self.packets = self.get_all_packets_in_data(packet_data)
        else:
            binary_packets_amount = bit_data[BitsPacket.HEADER_SIZE+1:BitsPacket.HEADER_SIZE+12]
            packets_amount = int(binary_packets_amount, base=2)
            self.packets = self.get_packets_by_number(bit_data[BitsPacket.HEADER_SIZE+12:], packets_amount)

    def __len__(self):
        header_size = BitsPacket.HEADER_SIZE + (16 if self.length_type == "0" else 12)
        return header_size + sum(len(p) for p in self.packets)

    @staticmethod
    def get_all_packets_in_data(packet_data):
        dp = 0
        packets = []
        while dp < len(packet_data):
            packet = BitsPacket(packet_data[dp:])
            packets.append(packet)
            dp += len(packet)
        return packets

    @staticmethod
    def get_packets_by_number(packets_data, packets_amount):
        dp = 0
        packets = []
        while len(packets) < packets_amount:
            packet = BitsPacket(packets_data[dp:])
            packets.append(packet)
            dp += len(packet)
        return packets


class BitsSum(BitsOperator):
    def value(self):
        return sum(p.value() for p in self.packets)


class BitsProduct(BitsOperator):
    def value(self):
        return math.prod(p.value() for p in self.packets)


class BitsMinimum(BitsOperator):
    def value(self):
        return min(p.value() for p in self.packets)


class BitsMaximum(BitsOperator):
    def value(self):
        return max(p.value() for p in self.packets)


class BitsGreaterThan(BitsOperator):
    def value(self):
        return int(self.packets[0].value() > self.packets[1].value())


class BitsLessThan(BitsOperator):
    def value(self):
        return int(self.packets[0].value() < self.packets[1].value())


class BitsEqual(BitsOperator):
    def value(self):
        return int(self.packets[0].value() == self.packets[1].value())


def parse_data():
    raw_data = read_data("16", False)
    binary_integer = int(raw_data, base=16)
    bit_string = bin(binary_integer)[2:]
    padding = (8 - (len(bit_string) % 8)) % 8
    padded_bit_string = ("0" * padding) + bit_string
    return padded_bit_string


def part_1(print_result: bool = True) -> int:
    binary_string = parse_data()
    parsed_message = BitsPacket(binary_string)
    return parsed_message.version_sum()


def part_2(print_result: bool = True) -> int:
    binary_string = parse_data()
    parsed_message = BitsPacket(binary_string)
    return parsed_message.value()


SOLUTION_1 = 949
SOLUTION_2 = 1114600142730

if __name__ == "__main__":
    print(part_1())
    print(part_2())
