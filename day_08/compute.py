import dataclasses
from argparse import ArgumentParser
from copy import deepcopy
from enum import Enum
from itertools import product
from typing import List, Dict, Optional


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


def all_matches() -> Dict[str, List[str]]:
    return {
        l: ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        for l in 'abcdefg'
    }


@dataclasses.dataclass
class Panel:
    easy_patterns = (Pattern.One, Pattern.Four, Pattern.Seven, Pattern.Eight)
    hard_patterns = (Pattern.Zero, Pattern.Two, Pattern.Three, Pattern.Five, Pattern.Six, Pattern.Nine)

    patterns: List[str]  # the 10 patterns seen on the pannel
    output: List[str]  # the output to translate with the patterns
    digit_match: Dict[str, Pattern] = dataclasses.field(default_factory=dict)

    segment_match: Dict[str, List[str]] = dataclasses.field(default_factory=all_matches)

    output_value: Optional[int] = None

    @classmethod
    def update_segment(cls, match_dict: Dict[str, List[str]], pattern: str, value: str):
        for l in pattern:
            new_match = []
            for old_match in match_dict[l]:
                if old_match in value:
                    new_match.append(old_match)
            if len(new_match) == 0:
                raise ValueError()
            match_dict[l] = new_match

            if len(new_match) == 1:
                # remove from all entries, we have an exact match!
                for k, v in match_dict.items():
                    if k == l:
                        continue  # don't remove it from its own!
                    match_dict[k] = [l for l in v if l != new_match[0]]
                    if len(match_dict[k]) == 0:
                        raise ValueError()

    def _add_match(self, pattern: Pattern, value: str):
        if value not in self.digit_match:
            self.digit_match[value] = pattern
            # Keep only the intersection of the 2

            self.update_segment(self.segment_match, pattern.value, value)

    def easy_match(self) -> int:
        """
        Filter easy matches that have a unique number of segments (1, 4, 7 and 8).
        Add them to the digit match and count the number that were in the output for Q1.
        """
        rv = 0
        for pattern in self.easy_patterns:
            for p in self.patterns:
                if len(p) == len(pattern.value):
                    self._add_match(pattern, p)

            for o in self.output:
                if len(o) == len(pattern.value):
                    self._add_match(pattern, o)
                    rv += 1

        return rv

    @classmethod
    def potential(cls, size=3) -> List[List[int]]:
        rv = []
        entries = list(range(size))
        for i in entries:
            v = [i]
            for j in entries:
                if j not in v:
                    v.append(j)
                    for k in entries:
                        if k not in v:
                            v.append(k)
                            rv.append([e for e in v])
                            v.pop(-1)
                    v.pop(-1)  # reset to 1 element
        return rv

    @classmethod
    def hard_match(cls, patterns: List[str], init_match: Dict[str, List[str]]) -> Dict[str, Pattern]:
        fives: List[Pattern] = [p for p in Pattern if len(p.value) == 5]
        sixes: List[Pattern] = [p for p in Pattern if len(p.value) == 6]

        size_five: List[str] = [s for s in patterns if len(s) == 5]
        size_six: List[str] = [s for s in patterns if len(s) == 6]

        # all potential match from fives -> size_five
        potential = product(cls.potential(), cls.potential())

        for p in potential:
            current = deepcopy(init_match)
            match = {}
            for i_five, m_five in enumerate(p[0]):
                match[size_five[m_five]] = fives[i_five]
                for i_six, m_six in enumerate(p[1]):
                    match[size_six[m_six]] = sixes[i_six]
            try:
                for k, v in match.items():
                    cls.update_segment(current, v.value, k)
            except ValueError:
                continue  # wrong potential match
            else:
                # We found a valid combination!
                return match

    def _decode_output(self):
        v = 0
        for i, o in enumerate(reversed(self.output)):
            if o not in self.digit_match:
                raise ValueError(f'No translation for {o}')
            v += self.digit_match[o].digit * pow(10, i)
        return v

    def value(self) -> int:
        if self.output_value is not None:
            return self.output_value

        # Otherwise we have to compute it
        self.easy_match()
        for k, v in self.hard_match(self.patterns, self.segment_match).items():
            self._add_match(v, k)

        # We have to match all other patterns
        self.output_value = self._decode_output()
        return self.output_value

    @classmethod
    def sort_entries(cls, *args: str) -> List[str]:
        return list(map(
            lambda s: ''.join(sorted(s)),
            args
        ))

    @classmethod
    def from_str(cls, value: str) -> "Panel":
        patterns, output = value.split(' | ')
        return cls(
            cls.sort_entries(*patterns.split(' ')),
            cls.sort_entries(*output.split(' ')),
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

    @classmethod
    def all_values(cls, data: List["Panel"]) -> int:
        return sum((
            p.value()
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

    q2 = Panel.all_values(data)
    print(f'Q2: sum of all values: {q2}')
