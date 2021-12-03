import dataclasses
from typing import List, Tuple


@dataclasses.dataclass
class ReportBinary:
    value: int

    @property
    def bit_length(self) -> int:
        if self.value == 0:
            return 1
        return self.value.bit_length()

    def to_binary_str(self, bit_size: int) -> str:
        fmt = "{:>0%db}" % bit_size
        return fmt.format(self.value)

    @classmethod
    def from_str(cls, value: str) -> "ReportBinary":
        rv = 0
        for i, v_str in enumerate(reversed(value)):
            v = int(v_str)
            if v not in (0, 1):
                raise ValueError(f"Non binary digit found in {value}")
            rv += v << i
        return cls(rv)


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
    gama_rate = ReportBinary(0)  # most common bit
    epsilon_rate = ReportBinary(0)  # least common bit

    for b in range(bit_size):
        n_pos = 0
        n_neg = 0
        for v in data:
            bit = (v.value >> b) & 0x1
            n_pos += bit
            n_neg += ~bit & 0x1
        if n_pos > n_neg:
            gama_rate.value += 1 << b
        else:
            epsilon_rate.value += 1 << b

    return gama_rate, epsilon_rate


if __name__ == '__main__':
    report, bit_size = load_input('input.txt')
    print(f'Loaded {len(report)} entries (bit_size={bit_size})')
    gama, epsilon = extract_rates(report, bit_size)
    print(f'Q1: gama={gama.value} epsilon={epsilon.value} answer={gama.value * epsilon.value}')
