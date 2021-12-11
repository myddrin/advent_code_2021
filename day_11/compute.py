import dataclasses
from argparse import ArgumentParser
from typing import List, Dict, Iterator


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def neighbours(self) -> Iterator["Point"]:
        for y in range(self.y - 1, self.y + 2):
            for x in range(self.x - 1, self.x + 2):
                if self.x == x and self.y == y:
                    continue  # skip itself
                yield Point(x, y)


@dataclasses.dataclass
class Octopus:
    location: Point
    energy: int

    def increase_energy(self) -> bool:
        self.energy += 1
        return self.energy > 9

    @classmethod
    def from_str(cls, value: str, y: int) -> List["Octopus"]:
        return [
            cls(Point(x, y), v)
            for x, v in enumerate(map(int, value))
        ]


@dataclasses.dataclass
class Map:
    octopi: Dict[Point, Octopus]

    def simulate(self, turns: int) -> int:
        flashes = 0

        for t in range(turns):
            has_flashed = set()
            to_increase = []

            for o in self.octopi.values():
                if o.increase_energy():
                    has_flashed.add(o.location)
                    to_increase.extend(list(o.location.neighbours()))

            # print('Before flash')
            # for row in self.energy_grid():
            #     print(''.join((str(e) if e < 9 else '*' for e in row)))

            while to_increase:
                where = to_increase.pop(0)

                o = self.octopi.get(where)
                if o is not None and o.increase_energy():
                    if where not in has_flashed:
                        has_flashed.add(where)
                        to_increase.extend(list(where.neighbours()))

            # reset energy levels and count number of flashes
            for o in self.octopi.values():
                if o.energy > 9:
                    flashes += 1
                    o.energy = 0

        return flashes

    def energy_grid(self) -> List[List[int]]:
        points = list(self.octopi.keys())
        min_x = points[0].x
        max_x = points[0].x
        min_y = points[0].y
        max_y = points[0].y
        for p in points[1:]:
            min_x = min(p.x, min_x)
            max_x = max(p.x, max_x)
            min_y = min(p.y, min_y)
            max_y = max(p.y, max_y)

        rv = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                row.append(self.octopi[Point(x, y)].energy)
            rv.append(row)
        return rv

    def to_file(self, filename: str):
        with open(filename, 'w') as f:
            for line in self.energy_grid():
                f.write(''.join(map(str, line)) + '\n')

    @classmethod
    def from_str(cls, value: str, y: int) -> Dict[Point, Octopus]:
        rv = {}
        for o in Octopus.from_str(value, y):
            rv[o.location] = o
        return rv

    @classmethod
    def from_file(cls, filename: str) -> "Map":
        rv = {}
        with open(filename, 'r') as f:
            for y, line in enumerate(f):
                rv.update(cls.from_str(line.replace('\n', ''), y))

        return cls(rv)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    parser.add_argument('--turns', type=int, default=100,
                        help='Number of turns to run the simulation for, default is %(default)s.')
    parser.add_argument('--output', type=str, default=None, help='Output file (all correct lines)')
    args = parser.parse_args()

    data = Map.from_file(args.input)
    print(f'Loaded {len(data.octopi)} octopi from {args.input}')

    flashes = data.simulate(args.turns)
    print(f'Generated {flashes} in {args.turns} turns')

    if args.output is not None:
        print(f'Writing final state in {args.output}')
        data.to_file(args.output)
