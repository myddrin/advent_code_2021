import dataclasses
from argparse import ArgumentParser
from enum import Enum
from typing import Set, List, Tuple


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def from_str(cls, value: str):
        x, y = map(int, value.split(','))
        return Point(x, y)


@dataclasses.dataclass
class Paper:
    width: int = dataclasses.field(default=0)
    height: int = dataclasses.field(default=0)
    dots: Set[Point] = dataclasses.field(default_factory=set)

    def __len__(self):
        return len(self.dots)

    def add(self, point: Point):
        self.width = max(self.width, point.x + 1)
        self.height = max(self.height, point.y + 1)
        self.dots.add(point)

    def fold_up(self, y: int) -> "Paper":
        new_paper = Paper(self.width, self.height // 2)

        for p in self.dots:
            if p.y < y:
                new_p = p
            elif p.y > y:
                ny = self.height - p.y - (self.height % 2)
                new_p = Point(p.x, ny)
            else:
                raise RuntimeError(f'There should be no dots on line y={y}')
            new_paper.add(new_p)

        return new_paper

    def fold_left(self, x: int) -> "Paper":
        new_paper = Paper(self.width // 2, self.height)

        for p in self.dots:
            if p.x < x:
                new_p = p
            elif p.x > x:
                nx = self.width - p.x - (self.width % 2)
                new_p = Point(nx, p.y)
            else:
                raise RuntimeError(f'There should be no dots on line x={x}')
            new_paper.add(new_p)

        return new_paper

    def content(self) -> List[str]:
        rv = []
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                if Point(x, y) in self.dots:
                    row += '#'
                else:
                    row += '.'
            rv.append(row)
        return rv

    def to_file(self, filename: str):
        with open(filename, 'w') as f:
            rows = self.content()
            for row in rows:
                f.write(row + '\n')
            print(f'{len(rows)} rows written to {filename}')

    def perform(self, instructions: List["Instruction"]) -> "Paper":
        current = self
        for i in instructions:
            # print(f'Folding {i.direction.value} on {i.value}')
            if i.direction == Direction.Up:
                current = current.fold_up(i.value)
            elif i.direction == Direction.Left:
                current = current.fold_left(i.value)
            else:
                raise ValueError(f'Unexpected direction={i.direction}')
        return current


class Direction(Enum):
    Up = 'up'
    Left = 'left'


@dataclasses.dataclass
class Instruction:
    direction: Direction
    value: int

    @classmethod
    def from_str(cls, value: str) -> "Instruction":
        direction, line = value.split('=')
        if direction == 'fold along y':
            return cls(Direction.Up, int(line))
        elif direction == 'fold along x':
            return cls(Direction.Left, int(line))


def load_data(filename: str) -> Tuple[Paper, List[Instruction]]:
    with open(filename, 'r') as f:
        load_points = True  # changes to False on first blank line
        paper = Paper()
        instructions = []
        for line in f:
            line = line.replace('\n', '')
            if not line:
                load_points = False
                continue  # from now on we will load Instructions

            if load_points:
                p = Point.from_str(line)
                paper.add(p)
            else:
                instructions.append(Instruction.from_str(line))

        print(f'Loaded {len(paper.dots)} on a {paper.width}x{paper.height} grid '
              f'and {len(instructions)} instructions from {filename}')
        return paper, instructions


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    parser.add_argument('--output', type=str, default=None, help='Output file with all paths')
    parser.add_argument('--max-fold', type=int, default=None,
                        help='Maximum number of instructions to perform, for q1 say 1, default=%(default)s.')
    args = parser.parse_args()

    paper, instructions = load_data(args.input)

    if args.max_fold is not None:
        instructions = instructions[:args.max_fold]
        print(f'Limiting to {len(instructions)} folds')

    first = paper.perform(instructions)
    print(f'There are {len(first.dots)} dots visible after folding {len(instructions)} times')

    if args.output:
        first.to_file(args.output)
