import dataclasses
from typing import Optional, List


@dataclasses.dataclass
class Lanternfish:
    reproduce_reset = 7  # in days, remember to do -1 when setting it because 0 counts.
    reproduce_new = 2

    reproduce_in: int = dataclasses.field(default=reproduce_reset - 1)

    def age(self) -> Optional["Lanternfish"]:
        self.reproduce_in -= 1
        if self.reproduce_in < 0:
            self.reproduce_in = self.reproduce_reset - 1
            return Lanternfish(self.reproduce_reset + self.reproduce_new - 1)


@dataclasses.dataclass
class School:
    fish: List[Lanternfish] = dataclasses.field(default_factory=list)

    @classmethod
    def load_school(cls, filename: str) -> "School":
        with open(filename, 'r') as f:
            return cls.from_str(f.readline().replace('\n', ''))

    @classmethod
    def from_str(cls, value: str) -> "School":
        return cls([
            Lanternfish(fish_age)
            for fish_age in map(int, value.split(','))
        ])

    def __len__(self):
        return len(self.fish)

    def __getitem__(self, item: int) -> Lanternfish:
        return self.fish[item]

    def age(self) -> int:
        new_fish = []
        for f in self.fish:
            baby = f.age()
            if baby is not None:
                new_fish.append(baby)

        self.fish += new_fish
        return len(new_fish)

    def simulate(self, days: int, verbose: bool = False) -> int:
        if verbose:
            print(f'Initial state: {len(self)} fish')
        for i in range(1, days + 1):
            v = self.age()
            if verbose:
                print(f'After {i} day, {v} new fish, total is {len(self)}')

        return len(self)


if __name__ == '__main__':
    school = School.load_school('input.txt')
    print(f'Loaded a school of {len(school)} fish')

    total = school.simulate(80)
    print(f'Q1: after 80 days there are {total} fish in the school')
