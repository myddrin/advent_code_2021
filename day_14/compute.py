import dataclasses
import re
from argparse import ArgumentParser
from operator import itemgetter
from time import time
from typing import List, Dict, Tuple, Iterator, Union, Set


@dataclasses.dataclass(frozen=True)
class Rule:
    input: str
    output: str

    @property
    def replace_str(self) -> str:
        # Ignore `self.output[-1]` because we would not need it yet
        return self.output[:-1]

    @classmethod
    def from_str(cls, value: str) -> "Rule":
        pair, insert = value.split(' -> ')
        return cls(pair, pair[0] + insert + pair[1])

    def output_pairs(self) -> List[str]:
        assert len(self.output) == 3
        return [
            self.output[:2],
            self.output[1:]
        ]


@dataclasses.dataclass
class Bench:
    # initial polymer
    polymer: str = dataclasses.field()
    rules: Dict[str, Rule] = dataclasses.field(default_factory=dict)

    # map character -> number of entries
    _polymer_map: Dict[str, int] = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        self._update_map()

    # @property
    # def polymer(self) -> str:
    #     return ''.join([
    #         pair[0] for pair in self.polymer_pairs
    #     ]) + self.polymer_pairs[-1][-1]

    def _update_map(self):
        start = time()
        self._polymer_map.clear()
        for l in self.polymer:
            if l not in self._polymer_map:
                self._polymer_map[l] = 0
            self._polymer_map[l] += 1
        return time() - start

    def _add_rule(self, rule: Rule):
        self.rules[rule.input] = rule

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
        sorted_elems = sorted(self._polymer_map.items(), key=itemgetter(1))  # type: List[Tuple[str, int]]
        print(f'Most common element: {sorted_elems[-1]}, least common element: {sorted_elems[0]}')
        return sorted_elems[-1][1] - sorted_elems[0][1]

    @classmethod
    def from_file(cls, filename: str) -> "Bench":
        with open(filename, 'r') as f:
            load_rules = False
            rv = None
            for line in f:
                line = line.replace('\n', '')
                if not line:
                    load_rules = True
                    continue  # on first empty line move to load rules

                if load_rules:
                    rv._add_rule(Rule.from_str(line))
                else:
                    rv = cls(polymer=line)

            print(f'Loaded {len(rv.rules)} rules from {filename}, start polymer is {rv.polymer}')
            return rv

    @classmethod
    def pairs(cls, value: Union[List[str], str]) -> Iterator[str]:
        return [
            value[i - 1] + value[i]
            for i in range(1, len(value))
        ]

    def simulate_reaction(self, turns: int = 10) -> Tuple[str, str]:
        """This is SLOW but outputs the result polymer."""
        start_polymer = self.polymer
        rule_stats: Dict[int, int] = {}
        for t in range(1, turns + 1):
            start = time()
            prev = self.polymer
            self.polymer = ''

            current = 0
            while current < len(prev) - 1:
                for word in sorted(self.rules, key=lambda r:len(r), reverse=True):
                    print(f'current={current}/{len(prev) - 1} rule of size {len(word)}          ', end='\r')
                    # biggest rules are last
                    if prev[current:].startswith(word):
                        size = len(word)
                        if size not in rule_stats:
                            rule_stats[size] = 0
                        rule_stats[size] += 1
                        rule = self.rules[word]
                        self.polymer += rule.replace_str
                        current += size - 1
                        # self._add_rule(Rule(prev[:current + 1], self.polymer + word[-1]))
                        break
            # once finished we add the last base
            self.polymer += prev[-1]
            # self._add_rule(Rule(prev, self.polymer))

            print(f'Step {t} took {time() - start:.2f}s for {len(prev)} bases ({len(self.rules)} rules)')
            print(f'Rule hits: {rule_stats}')

        updated = self._update_map()
        print(f'Map updated in {updated:.2f} sec')
        return start_polymer, self.polymer

    def fast_simulate(self, turns: int = 40) -> float:
        """This is fast but only computes the polymer map"""
        # To do a long simulation and only get the score, since it's too long to get the actual polymer
        start = time()
        # Map Pair -> number of time it's present
        pair_map: Dict[str, int] = {}
        for pair in self.pairs(self.polymer):
            if pair not in pair_map:
                pair_map[pair] = 0
            pair_map[pair] += 1
        # last character to not forget it when we will compute _polymer_map
        left_over = self.polymer[-1]  # single character

        for t in range(1, turns + 1):
            new_pair_map = {}
            for pair, count in pair_map.items():
                rule = self.rules.get(pair)
                if rule is not None:
                    for new_pair in rule.output_pairs():
                        if new_pair not in new_pair_map:
                            new_pair_map[new_pair] = 0
                        new_pair_map[new_pair] += count
                else:
                    new_pair_map[pair] = count  # unknown rule
            pair_map = new_pair_map

        # and now update the polymer map
        self._polymer_map.clear()
        for pair, count in pair_map.items():
            l = pair[0]  # take the first letter only
            if l not in self._polymer_map:
                self._polymer_map[l] = 0
            self._polymer_map[l] += count
        if left_over not in self._polymer_map:
            self._polymer_map[left_over] = 0
        self._polymer_map[left_over] += 1

        return time() - start



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    parser.add_argument('--steps', type=int, default=10,
                        help='Number of steps to simulate, default=%(default)s. Use 10 for Q1 and 40 for Q2')
    parser.add_argument('--slow', action='store_true',
                        help='Compute the result polymer, this is slow and should not be used for steps > 15')
    args = parser.parse_args()

    bench = Bench.from_file(args.input)

    print(f'Simulating for {args.steps} steps')
    if args.slow:
        start = time()
        bench.simulate_reaction(args.steps)
        print(f'Simulating {args.steps} steps took {time() - start:.2f} seconds')
        print(f'Result poly is {len(bench.polymer)} long')
    else:
        print('Doing a fast simulation')
        duration = bench.fast_simulate(args.steps)
        print(
            f'Compute the polymer map for {args.steps} steps took {duration:.2f} seconds. '
            'The result polymer is unknown.'
        )

    print(f'Score: {bench.score()}')
