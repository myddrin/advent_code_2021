import dataclasses
from argparse import ArgumentParser
from typing import Iterator, Dict, List, Set


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def neighbours(self) -> Iterator["Point"]:
        yield Point(self.x, self.y - 1)
        yield Point(self.x - 1, self.y)
        yield Point(self.x + 1, self.y)
        yield Point(self.x, self.y + 1)


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
    basins: List[List[Point]] = dataclasses.field(default_factory=list)

    @classmethod
    def _compute_low_points(cls, locations: List[Location]) -> Dict[Point, Location]:
        rv = {
            l.where: l
            for l in locations
        }

        for l in locations:
            neighbours = sorted((
                rv[n].height
                for n in l.where.neighbours()
                if n in rv
            ))
            l.is_low_point = l.height < neighbours[0]

        return rv

    @classmethod
    def from_file(cls, filename: str) -> "Map":
        locations = []
        with open(filename, 'r') as f:
            y = 0
            for line in f:
                locations += Location.from_str(line.replace('\n', ''), y)
                y += 1

        points_dict = cls._compute_low_points(locations)
        return cls(points_dict)

    def _compute_basins(self, location: Location, mountain: int = 9) -> List[Point]:
        # by definition each low point is only in one basin
        basin: Set[Point] = set()
        marked: Set[Point] = set()  # for locations that made it into "pending"
        pending_locations: List[Location] = [location]

        while pending_locations:
            current = pending_locations.pop(0)
            if current.height < mountain:
                basin.add(current.where)

                for n in current.where.neighbours():
                    if n not in marked:
                        marked.add(n)
                        neighbour = self.points.get(n)
                        if neighbour is not None and neighbour.height < mountain:
                            pending_locations.append(neighbour)

        return list(basin)

    def __post_init__(self):
        if not self.basins:
            # compute the basins
            for l in self.points.values():
                if l.is_low_point:
                    self.basins.append(self._compute_basins(l))

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
        ))

    def largest_basins_risk(self, n: int = 3) -> int:
        basin_sizes = sorted(
            (
                len(b)
                for b in self.basins
            ),
            reverse=True,
        )
        rv = basin_sizes[0]
        for i in range(1, min(len(basin_sizes), n)):
            rv *= basin_sizes[i]
        return rv


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    args = parser.parse_args()

    map = Map.from_file(args.input)
    print(f'Loaded {len(map.points)} points of a {map.width}x{map.height} grid')
    print(f'Found {len(map.basins)} basins')

    q1 = map.risk_level()
    print(f'Q1: direct risk level: {q1}')

    q2 = map.largest_basins_risk()
    print(f'Q2: basin risk level: {q2}')
