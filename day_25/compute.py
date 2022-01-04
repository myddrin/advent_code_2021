import dataclasses
import enum
from argparse import ArgumentParser
from typing import Dict, List


class Direction(enum.Enum):
    East = '>'
    South = 'v'


@dataclasses.dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __str__(self):
        return f'({self.x}, {self.y})'


@dataclasses.dataclass
class Cucumber:
    where: Position
    herd: Direction

    def next_position(self, max_x: int = None, max_y: int = None) -> Position:
        if self.herd == Direction.East:
            n = self.where.x + 1
            if max_x is not None and n >= max_x:
                n = 0
            return Position(n, self.where.y)
        elif self.herd == Direction.South:
            n = self.where.y + 1
            if max_y is not None and n >= max_y:
                n = 0
            return Position(self.where.x, n)
        raise RuntimeError(f'Unexpected herd value {self.herd}')

    def __str__(self):
        return f'C({self.herd.value}, {self.where})'


@dataclasses.dataclass
class Map:
    cucumbers: Dict[Position, Cucumber] = dataclasses.field(default_factory=dict)
    width: int = dataclasses.field(default=0)
    height: int = dataclasses.field(default=0)

    @classmethod
    def _read_line(cls, cucumbers: Dict[Position, Cucumber], line: str, y: int):
        x = 0
        for x, v in enumerate(line):
            try:
                herd = Direction(v)
            except ValueError:
                pass  # empty spot or unknown herd
            else:
                current = Cucumber(Position(x, y), herd)
                cucumbers[current.where] = current
        return x + 1

    @classmethod
    def from_file(cls, filename: str):
        cucumbers = {}
        with open(filename, 'r') as f:
            y = 0
            for line in f:
                x = cls._read_line(cucumbers, line.replace('\n', ''), y)
                y += 1
        print(f'Loaded {len(cucumbers)} on a {x}x{y} grid from {filename}')
        return cls(cucumbers, x, y)

    def render(self) -> List[str]:
        rv = []
        for y in range(self.height):
            line = ''
            for x in range(self.width):
                current = self.cucumbers.get(Position(x, y))
                if current is None:
                    line += '.'
                else:
                    line += current.herd.value
            rv.append(line)
        return rv

    def move(self) -> int:
        moved = 0

        for d in Direction:
            # Move East first
            next_cucumber = {}
            for p, c in self.cucumbers.items():
                if c.herd == d:
                    next_pos = c.next_position(self.width, self.height)
                    if next_pos not in self.cucumbers:
                        # this cucumber moves!
                        moved += 1
                        # print(f'{c} goes to {next_pos}')
                        c.where = next_pos
                    # else:
                    #     print(f'{c} is still as a cucumber')
                # moved or not, correct herd or not
                next_cucumber[c.where] = c
            self.cucumbers = next_cucumber

        return moved

    def find_stop(self, until: int = None) -> int:
        t = 1
        while until is None or t < until:
            moved = self.move()
            if moved == 0:
                break
            t += 1
        return t

    def to_file(self, filename: str):
        print(f'Writing {self.width}x{self.height} state to {filename}')
        with open(filename, 'w') as f:
            for l in self.render():
                f.write(l + '\n')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file.')
    parser.add_argument('--output', type=str, default=None, help='If provided write the current map as output.')
    args = parser.parse_args()

    floor_map = Map.from_file(args.input)

    q1 = floor_map.find_stop()
    print(f'Q1: stabilises after {q1} turns')

    if args.output is not None:
        floor_map.to_file(args.output)
