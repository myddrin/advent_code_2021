import dataclasses
from argparse import ArgumentParser
from typing import Dict


@dataclasses.dataclass
class Lanternfish:
    reproduce_reset = 7  # in days, remember to do -1 when setting it because 0 counts.
    reproduce_new = 2

    reproduce_in: int = dataclasses.field(default=reproduce_reset - 1)
    count: int = dataclasses.field(default=1)

    @classmethod
    def make_baby(cls, count: int = 1):
        return cls(cls.reproduce_reset + cls.reproduce_new - 1, count=count)

    def age(self) -> int:
        self.reproduce_in -= 1
        if self.reproduce_in < 0:
            self.reproduce_in = self.reproduce_reset - 1
            return self.count
        return 0


@dataclasses.dataclass
class School:
    fish_by_age: Dict[int, Lanternfish] = dataclasses.field(default_factory=dict)

    @classmethod
    def load_school(cls, filename: str) -> "School":
        with open(filename, 'r') as f:
            return cls.from_str(f.readline().replace('\n', ''))

    @classmethod
    def from_str(cls, value: str) -> "School":
        by_age: Dict[int, Lanternfish] = {}
        for fish_age in map(int, value.split(',')):
            if fish_age not in by_age:
                by_age[fish_age] = Lanternfish(reproduce_in=fish_age, count=0)
            by_age[fish_age].count += 1

        return cls(by_age)

    def __len__(self):
        return sum((f.count for f in self.fish_by_age.values()))

    def age(self) -> int:
        new_fish = 0
        new_fish_by_age: Dict[int, Lanternfish] = {}

        for f in self.fish_by_age.values():
            new_fish += f.age()
            if f.reproduce_in not in new_fish_by_age:
                new_fish_by_age[f.reproduce_in] = f
            else:
                new_fish_by_age[f.reproduce_in].count += f.count

        f = Lanternfish.make_baby(new_fish)
        new_fish_by_age[f.reproduce_in] = f
        self.fish_by_age = new_fish_by_age
        return new_fish

    def simulate(self, days: int, verbose: bool = False) -> int:
        if verbose:
            print(f'Initial state: {len(self)} fish')
        for i in range(1, days + 1):
            v = self.age()
            if verbose:
                print(f'After {i} day, {v} new fish, total is {len(self)}')

        return len(self)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Initial state file, default is %(default)s')
    parser.add_argument('--days', type=int, default=80,
                        help='How many days to run the simulation for. 80 for q1, 256 for q2, default is %(default)s')
    args = parser.parse_args()

    school = School.load_school(args.input)
    print(f'Loaded a school of {len(school)} fish from {args.input}')

    total = school.simulate(args.days)
    print(f'After {args.days} days there are {total} fish in the school')
