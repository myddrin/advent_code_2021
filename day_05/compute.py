import dataclasses
from typing import Dict, Iterable, List


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def from_str(cls, value: str) -> "Point":
        x, y = value.split(',')
        return cls(int(x), int(y))

    def __str__(self):
        return f"{self.x},{self.y}"

    # def __hash__(self):
    #     # Dataclass thinks 2 ints are unsafe hash, because we're not immutable.
    #     # Let's add frozen=True and all will be solved.
    #     return hash(str(self))

    def line(self, other: "Point", straight: bool = True) -> Iterable["Point"]:
        step_x = 0
        step_y = 0
        if self.y != other.y:
            step_y = 1 if self.y < other.y else -1
        if self.x != other.x:
            step_x = 1 if self.x < other.x else -1

        if straight and step_x != 0 and step_y != 0:
            raise ValueError(f'Does not support not straight lines {str(self)}->{str(other)}')

        st = self
        while st != other:
            yield st
            st = Point(st.x + step_x, st.y + step_y)
        yield st  # last point


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

    def write_map(self, filename: str):
        print(f'Loaded map with {len(self.points)} points, writing it into "{filename}"')
        with open(filename, 'w') as f:
            for l in self.map_str():
                f.write(l + '\n')

    @classmethod
    def load_map(cls, filename: str, straight: bool = True):
        rv = Map()
        ignored = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.replace('\n', '')
                start, end = map(Point.from_str, line.split(' -> '))  # type: Point

                try:
                    for p in start.line(end, straight):
                        rv.set(p)
                except ValueError:
                    ignored.append(line)

        if ignored:
            print(f'Ignored {len(ignored)} lines')
        return rv


if __name__ == '__main__':
    data = Map.load_map('input.txt', straight=True)
    data.write_map('output_q1.txt')

    straight = data.count_more_than(1)
    print(f'Q1: there are {straight} positions with more than 1 vent (diagonals excl.)')

    data = Map.load_map('input.txt', straight=False)
    data.write_map('output_q2.txt')

    diag = data.count_more_than(1)
    print(f'Q2: there are {diag} positions with more than 1 vent (diagonals incl.)')
