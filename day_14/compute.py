import dataclasses
import re
from argparse import ArgumentParser
from operator import itemgetter
from typing import List, Dict, Tuple


@dataclasses.dataclass
class Rule:
    pair: str
    insert: str

    @property
    def replace(self):
        return f"{self.pair[0]}{self.insert}{self.pair[1]}"

    @classmethod
    def from_str(cls, value: str) -> "Rule":
        pair, insert = value.split(' -> ')
        return cls(pair, insert)


@dataclasses.dataclass
class Bench:
    rules: Dict[str, Rule] = dataclasses.field(default_factory=dict)
    polymer: str = ''

    _polymer_map: Dict[str, int] = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        self._update_map(self.polymer)

    def _update_map(self, value: str):
        for l in value:
            if l not in self._polymer_map:
                self._polymer_map[l] = 0
            self._polymer_map[l] += 1

    def simulate_reaction(self, steps: int = 10) -> Tuple[str, str]:
        start_polymer = self.polymer

        for t in range(1, steps + 1):
            old_polymer = self.polymer
            self.polymer = ''
            for i in range(1, len(old_polymer)):
                current = old_polymer[i-1:i+1]
                if current in self.rules:
                    # ignore the last letter
                    self.polymer += self.rules[current].replace[:-1]
                    self._update_map(self.rules[current].insert)
                else:
                    # matched no rules, insert only the 1st letter
                    self.polymer += current[0]
            self.polymer += old_polymer[-1]

        return start_polymer, self.polymer

    def score(self) -> int:
        sorted_elems = sorted(self._polymer_map.items(), key=itemgetter(1))
        print(f'Most common element: {sorted_elems[-1]}, least common element: {sorted_elems[0]}')
        return sorted_elems[-1][1] - sorted_elems[0][1]

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, 'r') as f:
            load_rules = False
            rules = []
            start_polymer = None
            for line in f:
                line = line.replace('\n', '')
                if not line:
                    load_rules = True
                    continue  # on first empty line move to load rules

                if load_rules:
                    rules.append(Rule.from_str(line))
                else:
                    start_polymer = line

            print(f'Loaded {len(rules)} from {filename}, start polymer is {start_polymer}')
            return cls(
                {
                    r.pair: r
                    for r in rules
                },
                start_polymer,
            )


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    parser.add_argument('--steps', type=int, default=10,
                        help='Number of steps to simulate, default=%(default)s.')
    args = parser.parse_args()

    bench = Bench.from_file(args.input)

    print(f'Simulating for {args.steps} steps')
    bench.simulate_reaction(args.steps)

    print(f'Result poly is {len(bench.polymer)} long')
    print(f'Q1: {bench.score()}')
