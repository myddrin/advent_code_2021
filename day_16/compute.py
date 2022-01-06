import abc
import dataclasses
import enum
from argparse import ArgumentParser
from functools import reduce
from operator import mul
from typing import List


@dataclasses.dataclass
class HexSource:
    hex_string: str
    _consumed: int = dataclasses.field(default=0)
    _left_over_binary: str = dataclasses.field(default='')

    def sub_source(self, n_bits: int) -> "HexSource":
        self._consume_bits(n_bits)

        binary_str = self._left_over_binary[:n_bits]
        self._left_over_binary = self._left_over_binary[n_bits:]

        return HexSource('', _left_over_binary=binary_str)

    @classmethod
    def from_file(cls, filename: str) -> "HexSource":
        hex_source = ''
        with open(filename, 'r') as f:
            for line in f:
                hex_source += line.replace('\n', '')
        return cls(hex_source)

    def _consume_bits(self, n_bits: int):
        while len(self._left_over_binary) < n_bits:
            if self._consumed >= len(self.hex_string):
                raise RuntimeError('Trying to consume more bits than available')
            self._left_over_binary += f'{int(self.hex_string[self._consumed], 16):>04b}'
            self._consumed += 1

    def consume(self, n_bits: int) -> int:
        self._consume_bits(n_bits)

        value = self._left_over_binary[:n_bits]
        self._left_over_binary = self._left_over_binary[n_bits:]
        return int(value, 2)


class TypeID(enum.Enum):
    Sum = 0
    Product = 1
    Minimum = 2
    Maximum = 3
    LiteralValue = 4
    GreaterThan = 5  # only for pairs
    LessThan = 6  # only for pairs
    EqualTo = 7  # only for pairs

    @property
    def is_operator(self) -> bool:
        return self != TypeID.LiteralValue


@dataclasses.dataclass
class PacketHeader:
    version: int
    typeID: TypeID

    @classmethod
    def from_str(cls, hex_src: HexSource) -> "PacketHeader":
        version = hex_src.consume(3)
        type_id = TypeID(hex_src.consume(3))
        return cls(version, type_id)


@dataclasses.dataclass
class Packet(metaclass=abc.ABCMeta):
    main_header: PacketHeader

    def version_sum(self) -> int:
        return self.main_header.version

    @abc.abstractmethod
    def process(self) -> int:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def factory(cls, hex_src: HexSource, main_header: PacketHeader) -> "Packet":
        raise NotImplementedError()

    @classmethod
    def from_src(cls, hex_src: HexSource) -> "Packet":
        header = PacketHeader.from_str(hex_src)
        if header.typeID == TypeID.LiteralValue:
            return LiteralValue.factory(hex_src, header)
        elif header.typeID.is_operator:
            return Operator.factory(hex_src, header)
        raise RuntimeError(f'Unexpected typeID {header.typeID}')

    @classmethod
    def from_file(cls, filename: str) -> List["Packet"]:
        hex_src = HexSource.from_file(filename)
        packets = []
        while True:
            try:
                packets.append(cls.from_src(hex_src))
            except RuntimeError:
                break
        print(f'Loaded {len(packets)} packet from {filename}')
        return packets


@dataclasses.dataclass
class LiteralValue(Packet):
    value: int

    def process(self) -> int:
        return self.value

    @classmethod
    def factory(cls, hex_src: HexSource, main_header: PacketHeader) -> "LiteralValue":
        need_more = True
        value = 0
        while need_more:
            need_more = hex_src.consume(1) == 1
            current = hex_src.consume(4)
            value = (value << 4) + current

        return cls(main_header, value)


@dataclasses.dataclass
class Operator(Packet):
    packet_content: List[Packet] = dataclasses.field(default_factory=list)

    def version_sum(self) -> int:
        return super(Operator, self).version_sum() + sum(packet.version_sum() for packet in self.packet_content)

    def process(self) -> int:
        values = [
            packet.process()
            for packet in self.packet_content
        ]
        if self.main_header.typeID == TypeID.Sum:
            return sum(values)
        elif self.main_header.typeID == TypeID.Product:
            return reduce(mul, values, 1)
        elif self.main_header.typeID == TypeID.Minimum:
            return min(values)
        elif self.main_header.typeID == TypeID.Maximum:
            return max(values)
        elif self.main_header.typeID == TypeID.GreaterThan:
            return int(values[0] > values[1])
        elif self.main_header.typeID == TypeID.LessThan:
            return int(values[0] < values[1])
        elif self.main_header.typeID == TypeID.EqualTo:
            return int(values[0] == values[1])
        raise RuntimeError(f'Unexpected operator packet {self.main_header.typeID}')

    @classmethod
    def _binary_from_str(cls, hex_src: HexSource, main_header: PacketHeader) -> "Operator":
        size = hex_src.consume(15)

        sub_source = hex_src.sub_source(size)
        packets = []

        # Consume as many packets from the sub source as possible
        print(f'Loading packets from a {size} bits sub-source')
        while True:
            try:
                packets.append(Packet.from_src(sub_source))
            except RuntimeError:
                break

        return cls(main_header, packet_content=packets)

    @classmethod
    def _packets_from_str(cls, hex_src: HexSource, main_header: PacketHeader) -> "Operator":
        size = hex_src.consume(11)
        packets = []
        print(f'Loading {size} sub packets')
        while len(packets) < size:
            packets.append(Packet.from_src(hex_src))
            print(f'Loaded {len(packets)}/{size} sub packets')

        return cls(
            main_header,
            packet_content=packets,
        )

    @classmethod
    def factory(cls, hex_src: HexSource, main_header: PacketHeader) -> "Operator":
        contains_packets = hex_src.consume(1) == 1
        if contains_packets:
            return cls._packets_from_str(hex_src, main_header)
        return cls._binary_from_str(hex_src, main_header)


def q1_version_sum(packets: List[Packet]) -> int:
    return sum((
        p.version_sum()
        for p in packets
    ))


def q2_process(packets: List[Packet]) -> List[int]:
    return [
        packet.process()
        for packet in packets
    ]


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    args = parser.parse_args()

    transmission = Packet.from_file(args.input)

    q1 = q1_version_sum(transmission)
    print(f'Q1: version sum: {q1}')

    q2 = q2_process(transmission)
    print(f'Q2: process: {q2}')
