import dataclasses
import re
from argparse import ArgumentParser
from operator import itemgetter
from time import time
from typing import List, Dict, Tuple, Iterator


@dataclasses.dataclass(frozen=True)
class Rule:
    pair: str
    insert: str

    @property
    def replace(self):
        # Ignore {self.pair[1]} because we would not need it yet
        return f"{self.pair[0]}{self.insert}"

    @classmethod
    def from_str(cls, value: str) -> "Rule":
        pair, insert = value.split(' -> ')
        return cls(pair, insert)


@dataclasses.dataclass
class Bench:
    rules: Dict[str, Rule] = dataclasses.field(default_factory=dict)
    polymer_pairs: List[str] = dataclasses.field(default_factory=list)

    _polymer_map: Dict[str, int] = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        self._update_map()

    @property
    def polymer(self) -> str:
        return ''.join([
            pair[0] for pair in self.polymer_pairs
        ]) + self.polymer_pairs[-1][-1]

    def _update_map(self) -> float:
        start = time()
        self._polymer_map.clear()
        for l in self.polymer:
            if l not in self._polymer_map:
                self._polymer_map[l] = 0
            self._polymer_map[l] += 1
        return time() - start

    # old way when polymer was List[str]
    # def simulate_reaction(self, steps: int = 10) -> Tuple[str, str]:
    #     start_polymer = self.polymer
    #
    #     for t in range(1, steps + 1):
    #         start = time()
    #         old_polymer = self.polymer
    #         self.polymer = []
    #         for i in range(1, len(old_polymer)):
    #             current = ''.join(old_polymer[i-1:i+1])
    #             if current in self.rules:
    #                 # ignore the last letter
    #                 self.polymer += self.rules[current].replace
    #                 # self._update_map(self.rules[current].insert)
    #             else:
    #                 # matched no rules, insert only the 1st letter
    #                 self.polymer.append(old_polymer[i-1])
    #         print(f'After step {t} the polymer is {len(self.polymer)} elements long (step took {time() - start:.3f}s)')
    #         self.polymer.append(old_polymer[-1])
    #
    #     updated = self._update_map()
    #     print(f'Updated polymer map in {updated:.2f}s')
    #
    #     return ''.join(start_polymer), ''.join(self.polymer)

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
                cls.pairs(start_polymer),
            )

    @classmethod
    def pairs(cls, value: List[str]) -> Iterator[str]:
        return [
            value[i - 1] + value[i]
            for i in range(1, len(value))
        ]

    def simulate_reaction(self, turns: int = 10):
        start_polymer = self.polymer
        for t in range(1, turns + 1):
            start = time()
            prev = self.polymer_pairs
            self.polymer_pairs = []

            # TODO(tr) write a cache for every initial polymer to the next? check with regex?

            for pair in prev:
                if pair in self.rules:
                    new_pair = self.rules[pair].replace
                    self.polymer_pairs.append(new_pair)
                    self.polymer_pairs.append(new_pair[1] + pair[-1])
                else:
                    self.polymer_pairs.append(pair)
            print(f'Step {t} took {time() - start:.2f}s for {len(prev)} pairs')

        self._update_map()
        return start_polymer, self.polymer


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    parser.add_argument('--steps', type=int, default=10,
                        help='Number of steps to simulate, default=%(default)s.')
    args = parser.parse_args()

    bench = Bench.from_file(args.input)

    print(f'Simulating for {args.steps} steps')
    start = time()
    bench.simulate_reaction(args.steps)
    print(f'Simulating {args.steps} steps took {time() - start:.2f} seconds')

    print(f'Result poly is {len(bench.polymer)} long')
    print(f'Q1: {bench.score()}')
