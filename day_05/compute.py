import dataclasses
from typing import Dict, Iterable, List


@dataclasses.dataclass()
class Point:
    x: int
    y: int

    @classmethod
    def from_str(cls, value: str) -> "Point":
        x, y = value.split(',')
        return cls(int(x), int(y))

    def __str__(self):
        return f"{self.x},{self.y}"

    def __hash__(self):
        # TODO(tr) Dataclass thinks 2 ints are unsafe hash, why?
        return hash(str(self))

    def straight_line(self, other: "Point") -> Iterable["Point"]:
        if self.y == other.y:
            min_x = min(self.x, other.x)
            max_x = max(self.x, other.x)
            for x in range(min_x, max_x + 1):
                yield Point(x, self.y)
        elif self.x == other.x:
            min_y = min(self.y, other.y)
            max_y = max(self.y, other.y)
            for y in range(min_y, max_y + 1):
                yield Point(self.x, y)
        else:
            raise ValueError()


@dataclasses.dataclass
class Map:
    points: Dict[Point, int] = dataclasses.field(default_factory=dict)

    def set(self, point: Point):
        if point not in self.points:
            self.points[point] = 0
        self.points[point] += 1

    def count_more_than(self, n: int = 1) -> int:
        return sum((
            1
            for v in self.points.values()
            if v > n
        ))

    def map_str(self) -> List[str]:
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for p in self.points.keys():
            min_x = min(min_x, p.x)
            max_x = max(max_x, p.x)
            min_y = min(min_y, p.y)
            max_y = max(max_y, p.y)

        lines = []
        for y in range(min_y, max_y + 1):
            line = ''
            for x in range(min_x, max_x + 1):
                count = self.points.get(Point(x, y), 0)
                if count == 0:
                    line += '.'
                elif count >= 10:
                    line += '+'  # unlikely to have more than 2 digit
                else:
                    line += str(count)
            lines.append(line)

        return lines

    @classmethod
    def load_map(cls, filename: str, straight=True):
        rv = Map()
        ignored = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.replace('\n', '')
                start, end = map(Point.from_str, line.split(' -> '))  # type: Point

                if straight:
                    try:
                        for p in start.straight_line(end):
                            rv.set(p)
                    except ValueError:
                        ignored.append(line)
                else:
                    raise NotImplementedError()

        if ignored:
            print(f'Ignored {len(ignored)} lines')
        return rv


if __name__ == '__main__':
    data = Map.load_map('input.txt', straight=True)

    print(f'Loaded map with {len(data.points)} points')
    with open('output_q1.txt', 'w') as f:
        for l in data.map_str():
            f.write(l + '\n')

    straight = data.count_more_than(1)
    print(f'Q1: there {straight} position with more than 1 vent')
