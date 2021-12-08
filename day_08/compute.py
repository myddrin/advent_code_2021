import dataclasses
from argparse import ArgumentParser
from enum import Enum
from typing import List, Dict


class Pattern(Enum):
    """
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
    """
    Zero = 'abcefg'
    One = 'cf'  # unique with 2 segments
    Two = 'acdeg'
    Three = 'acdfg'
    Four = 'bcdf'  # unique with 4 segments
    Five = 'abdfg'
    Six = 'abdefg'
    Seven = 'acf'  # unique with 3 segments
    Eight = 'abcdefg'  # unique with 7 segments
    Nine = 'abcdfg'

    @property
    def digit(self) -> int:
        if self == self.Zero:
            return 0
        elif self == self.One:
            return 1
        elif self == self.Two:
            return 2
        elif self == self.Three:
            return 3
        elif self == self.Four:
            return 4
        elif self == self.Five:
            return 5
        elif self == self.Six:
            return 6
        elif self == self.Seven:
            return 7
        elif self == self.Eight:
            return 8
        elif self == self.Nine:
            return 9
        raise ValueError()


@dataclasses.dataclass
class Panel:
    patterns: List[str]  # the 10 patterns seen on the pannel
    output: List[str]  # the output to translate with the patterns
    digit_match: Dict[int, List[str]] = dataclasses.field(default_factory=dict)

    def easy_match(self) -> int:
        """
        Filter easy matches that have a unique number of segments (1, 4, 7 and 8).
        Add them to the digit match and count the number that were in the output for Q1.
        """
        rv = 0
        for pattern in (Pattern.One, Pattern.Four, Pattern.Seven, Pattern.Eight):
            for p in self.patterns:
                if len(p) == len(pattern.value):
                    if pattern.digit not in self.digit_match:
                        self.digit_match[pattern.digit] = []
                    self.digit_match[pattern.digit].append(p)

            for o in self.output:
                if len(o) == len(pattern.value):
                    if pattern.digit not in self.digit_match:
                        self.digit_match[pattern.digit] = []
                    self.digit_match[pattern.digit].append(o)
                    rv += 1

        return rv

    @classmethod
    def from_str(cls, value: str) -> "Panel":
        patterns, output = value.split(' | ')
        return cls(
            patterns.split(' '),
            output.split(' '),
        )

    @classmethod
    def from_file(cls, filename: str) -> List["Panel"]:
        rv = []
        with open(filename, 'r') as f:
            for line in f:
                rv.append(cls.from_str(line.replace('\n', '')))
        return rv

    @classmethod
    def count_easy_match(cls, data: List["Panel"]) -> int:
        return sum((
            p.easy_match()
            for p in data
        ))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    args = parser.parse_args()

    data = Panel.from_file(args.input)
    print(f'Loaded {len(data)} from {args.input}')

    q1 = Panel.count_easy_match(data)
    print(f'Q1: number of 1, 4, 7 or 8 in data: {q1}')
