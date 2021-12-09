import dataclasses
from argparse import ArgumentParser
from typing import Iterator, Dict, List


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def neighbours(self, diagonals: bool = False) -> Iterator["Point"]:
        for y in range(self.y - 1, self.y + 2):
            for x in range(self.x - 1, self.x + 2):
                if (x != self.x or y != self.y) and (diagonals or x == self.x or y == self.y):
                    yield Point(x, y)


@dataclasses.dataclass
class Location:
    where: Point
    height: int

    is_low_point: bool = False

    @classmethod
    def from_str(cls, value: str, y: int) -> List["Location"]:
        return [
            cls(Point(x, y), int(h))
            for x, h in enumerate(value)
        ]

    @property
    def risk_level(self) -> int:
        if self.is_low_point:
            return self.height + 1
        return 0  # not at risk?

    def __lt__(self, other: "Location") -> bool:
        return self.height < other.height


@dataclasses.dataclass
class Map:
    points: Dict[Point, Location]

    @classmethod
    def _compute_low_points(cls, points: List[Location]) -> Dict[Point, Location]:
        rv = {
            l.where: l
            for l in points
        }

        for l in points:
            neighbours = sorted((
                rv[n].height
                for n in l.where.neighbours()
                if n in rv
            ))
            l.is_low_point = l.height < neighbours[0]

        return rv

    @classmethod
    def from_file(cls, filename: str) -> "Map":
        points = []
        with open(filename, 'r') as f:
            y = 0
            for line in f:
                points += Location.from_str(line.replace('\n', ''), y)
                y += 1
        return cls(cls._compute_low_points(points))

    @property
    def width(self) -> int:
        return max((p.x for p in self.points)) + 1

    @property
    def height(self) -> int:
        return max((p.y for p in self.points)) + 1

    def risk_level(self) -> int:
        return sum((
            l.risk_level
            for l in self.points.values()
            # if l.is_low_point
        ))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    args = parser.parse_args()

    map = Map.from_file(args.input)
    print(f'Loaded {len(map.points)} points of a {map.width}x{map.height} grid')

    q1 = map.risk_level()
    print(f'Q1: direct risk level: {q1}')
