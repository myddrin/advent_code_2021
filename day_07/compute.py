import dataclasses
from operator import itemgetter
from typing import List, Dict, Tuple


@dataclasses.dataclass
class Crab:
    # class attributes:
    _exp_cost_cache = {}  # type: Dict[int, int]

    # object attributes:
    position: int = dataclasses.field()
    count: int = dataclasses.field(default=0)

    def cost_to(self, p: int, exponential: bool = False):
        cost = abs(p - self.position)
        if exponential:
            if cost not in self._exp_cost_cache:
                self._exp_cost_cache[cost] = sum(range(1, cost + 1))

            cost = self._exp_cost_cache[cost]

        return cost * self.count

    def __lt__(self, other: "Crab") -> bool:
        return self.position < other.position


@dataclasses.dataclass
class Swarm:
    crabs: List[Crab]  # crab sub positions, can have the same number multiple times

    @classmethod
    def from_str(cls, value: str) -> "Swarm":
        rv = {}
        for v in map(int, value.split(',')):
            if v not in rv:
                rv[v] = Crab(v)
            rv[v].count += 1
        return cls(sorted(rv.values()))

    @classmethod
    def from_file(cls, filename: str) -> "Swarm":
        with open(filename, 'r') as f:
            return cls.from_str(f.readline().replace('\n', ''))

    def count(self):
        return sum((c.count for c in self.crabs))

    def compute_position_cost(self, exponential: bool = False) -> Dict[int, int]:
        """Compute the cost for each position and return the dict"""
        all_position = [c.position for c in self.crabs]
        st = min(all_position)
        ed = max(all_position)

        rv = {
            p: 0
            for p in range(st, ed + 1)
            # We consider all locations where a crab is
        }
        for p in rv.keys():
            rv[p] = sum((
                c.cost_to(p, exponential)
                for c in self.crabs
            ))

        return rv

    def best_position(self, exponential: bool = False) -> Tuple[int, int]:
        """Return tuple position, cost"""
        for position, cost in sorted(self.compute_position_cost(exponential).items(), key=itemgetter(1)):
            # only return the first element since it's sorted
            return position, cost


if __name__ == '__main__':
    data = Swarm.from_file('input.txt')
    print(f'Loaded {data.count()} crabs at {len(data.crabs)} positions')

    best_linear, linear_cost = data.best_position()
    print(f'Q1: best position is {best_linear} for a cost of {linear_cost}')

    best_exponential, exponential_cost = data.best_position(exponential=True)
    print(f'Q2: best position is {best_exponential} for a cost of {exponential_cost}')
