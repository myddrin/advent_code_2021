import dataclasses
from copy import copy
from typing import List, Tuple, Callable


@dataclasses.dataclass
class ReportBinary:
    value: int

    @classmethod
    def from_str(cls, value: str) -> "ReportBinary":
        rv = 0
        for i, v_str in enumerate(reversed(value)):
            v = int(v_str)
            if v not in (0, 1):
                raise ValueError(f"Non binary digit found in {value}")
            rv += v << i
        return cls(rv)

    @classmethod
    def count_bit(cls, data: List["ReportBinary"], bit: int) -> Tuple[int, int]:
        """Return nunber of positive and number of negative bits from a report"""
        n_pos = 0
        n_neg = 0
        for v in data:
            bit_value = (v.value >> bit) & 0x1
            n_pos += bit_value
            n_neg += ~bit_value & 0x1

        return n_pos, n_neg

    @classmethod
    def o2_filter(cls, n_pos: int, n_neg: int) -> int:
        return int(n_pos >= n_neg)

    @classmethod
    def co2_filter(cls, n_pos: int, n_neg: int) -> int:
        return int(n_pos < n_neg)

    @property
    def bit_length(self) -> int:
        if self.value == 0:
            return 1
        return self.value.bit_length()

    def to_binary_str(self, bit_size: int) -> str:
        fmt = "{:>0%db}" % bit_size
        return fmt.format(self.value)

    def __repr__(self):
        return f"{self.to_binary_str(self.bit_length)}({self.value})"


def load_input(filename: str) -> Tuple[List[ReportBinary], int]:
    rv = []
    bit_size = 0
    with open(filename, 'r') as f:
        for line in f:
            # bit_size = len(line)
            v = ReportBinary.from_str(line.replace('\n', ''))
            rv.append(v)
            bit_size = max(bit_size, v.bit_length)

    return rv, bit_size


def extract_rates(data: List[ReportBinary], bit_size: int) -> Tuple[ReportBinary, ReportBinary]:
    """return gama rates and epsilon rate"""
    gama_rate = ReportBinary(0)  # most common bit
    epsilon_rate = ReportBinary(0)  # least common bit

    for b in range(bit_size):
        n_pos, n_neg = ReportBinary.count_bit(data, b)

        if n_pos > n_neg:
            gama_rate.value += 1 << b
        else:
            epsilon_rate.value += 1 << b

    return gama_rate, epsilon_rate


def filter_report(data: List[ReportBinary], bit_size: int, filter_fn: Callable[[int, int], int]) -> List[ReportBinary]:
    """return o2_rating=true: O2 generator rating, o2_rating=false: CO2 scrubber rating"""
    left_data = copy(data)

    # start comparing big-endian
    for bit in range(bit_size - 1, -1, -1):
        if len(left_data) == 1:
            break

        n_pos, n_neg = ReportBinary.count_bit(left_data, bit)
        filter = filter_fn(n_pos, n_neg)

        left_data = [
            v
            for v in left_data
            if (v.value >> bit) & 0x1 == filter
        ]

    return left_data


if __name__ == '__main__':
    report, bit_size = load_input('input.txt')
    print(f'Loaded {len(report)} entries (bit_size={bit_size})')
    gama, epsilon = extract_rates(report, bit_size)
    print(f'Q1: gama={gama.value} epsilon={epsilon.value} answer={gama.value * epsilon.value}')

    o2_rating = filter_report(report, bit_size, ReportBinary.o2_filter)[0]
    co2_rating = filter_report(report, bit_size, ReportBinary.co2_filter)[0]
    print(f'Q2: o2={o2_rating.value} co2={co2_rating.value} answer={o2_rating.value * co2_rating.value}')
