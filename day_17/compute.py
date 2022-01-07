import dataclasses
from argparse import ArgumentParser
from copy import copy
from operator import attrgetter
from time import time
from typing import List, Dict, Tuple


@dataclasses.dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __str__(self):
        return f'[{self.x}, {self.y}]'


@dataclasses.dataclass
class Velocity:
    dx: int
    dy: int

    def __str__(self):
        return f'd({self.dx}, {self.dy})'

    def stopped(self) -> bool:
        return self.dx == 0

    def update(self) -> "Velocity":
        self.dy -= 1
        if self.dx > 0:
            self.dx -= 1
        elif self.dx < 0:
            self.dx += 1
        return self


@dataclasses.dataclass
class Trajectory:
    velocity: Velocity = dataclasses.field()
    highest: int = dataclasses.field(default=0)
    initial_velocity: Velocity = dataclasses.field(default=None)
    _coordinates: List[Position] = dataclasses.field(default_factory=lambda: [Position(0, 0)])

    def __str__(self):
        return (
            f'T(init={self.initial_velocity}, '
            f'vel={self.velocity}, '
            f'len={len(self._coordinates)}, '
            f'highest={self.highest})'
        )

    def __post_init__(self):
        self.initial_velocity = copy(self.velocity)

    def last_position(self) -> Position:
        return self._coordinates[-1]

    def update(self) -> Position:
        new_position = Position(
            self.last_position().x + self.velocity.dx,
            self.last_position().y + self.velocity.dy,
        )
        self.velocity.update()

        self._coordinates.append(new_position)
        if new_position.y > self.highest:
            self.highest = new_position.y
        return new_position


@dataclasses.dataclass
class World:
    target_start: Position
    target_end: Position

    tried_trajectories: int = dataclasses.field(default=0)
    best_q1_trajectory: Trajectory = dataclasses.field(default=None)
    hit_trajectories: List[Trajectory] = dataclasses.field(default_factory=list)

    @classmethod
    def from_str(cls, target_str: str) -> "World":
        # "target area: x=X..X, y=Y..Y"
        action, value = target_str.split(':')
        assert action == 'target area'
        coordinates: Dict[str, List[int]] = {}
        for val in value.replace(' ', '').split(','):
            coord, coord_range = val.split('=')
            assert coord not in coordinates, f'Known coordinate {coord}'
            coordinates[coord] = list(map(int, coord_range.split('..')))
            assert len(coordinates[coord]) == 2, 'not enough data'
            assert coordinates[coord][0] < coordinates[coord][1], 'coord[0] must be < coord[1]'
        assert 'x' in coordinates and 'y' in coordinates

        return cls(
            Position(coordinates['x'][0], coordinates['y'][0]),
            Position(coordinates['x'][1], coordinates['y'][1]),
        )

    @classmethod
    def from_file(cls, filename: str) -> "World":
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('target area'):
                    obj = cls.from_str(line.replace('\n', ''))
                    print(f'Loaded {obj} from {filename}')
                    return obj
        raise RuntimeError(f'No "target area" token in {filename}')

    def __str__(self):
        return (
            f'W({self.target_start}->{self.target_end}, '
            f'tried={self.tried_trajectories} '
            f'hits={len(self.hit_trajectories)}'
            f')'
        )

    def in_area(self, position: Position) -> bool:
        return (
            self.target_start.x <= position.x <= self.target_end.x
            and
            self.target_start.y <= position.y <= self.target_end.y
        )

    def missed_area(self, position: Position) -> bool:
        return (
            position.x > self.target_end.x
            or
            # because y is negative otherwise do y < target_end.y
            position.y < self.target_start.y
        )

    def compute(self, velocity: Velocity) -> Tuple[Trajectory, bool]:
        current = Trajectory(velocity)
        while True:
            next_p = current.update()
            if self.in_area(next_p):
                # print(f'{current} (last={next_p}) hits!')
                return current, True
            elif self.missed_area(next_p):
                # print(f'{current} (last={next_p}) misses.')
                return current, False
            elif current.velocity.dx == 0:
                # Now the projectile will only fall, stop only if not above the target
                if not (self.target_start.x <= current.last_position().x <= self.target_end.x):
                    # print(f'{current} (last={next_p}) stalled not above target')
                    return current, False

    def simulate(self) -> Trajectory:
        # Only supports target locations that are on the right (i.e. positive start/end X)
        if self.best_q1_trajectory is not None:
            return self.best_q1_trajectory

        # For Q1 we used to fire the probe to be in the quadrant above the target but only with positive Y values
        # since we tried to find the highest curve x in (1, end.x) and y in (1, max(start.y, end.y))

        start_time = time()
        max_y = max(map(
            abs,
            (
                self.target_start.x,
                self.target_start.y,
                self.target_end.x,
                self.target_end.y,
            ),
        )) + 1

        start_x = 1
        max_x = max(abs(self.target_start.x), abs(self.target_end.x)) + 1
        start_y = -1 * max_y

        print(f'Computing x in {start_x, max_x} and y in {start_y, max_y}')
        for sx in range(start_x, max_x):
            # Find the highest Y value that hits
            for sy in range(start_y, max_y):
                current, hit = self.compute(Velocity(sx, sy))
                if hit:
                    self.hit_trajectories.append(current)
                    if self.best_q1_trajectory is None:
                        self.best_q1_trajectory = current
                    elif current.highest > self.best_q1_trajectory.highest:
                        self.best_q1_trajectory = current

                self.tried_trajectories += 1
                if self.tried_trajectories % 100 == 0:
                    print(
                        f'Tried {self.tried_trajectories}/{(max_x - start_x) * (max_y - start_y)} launches, '
                        f'{len(self.hit_trajectories)} hit, '
                        f'best is {self.best_q1_trajectory} '
                        f'in {time() - start_time:.2f} sec'
                    )

        print(f'Tried {self.tried_trajectories} ({len(self.hit_trajectories)} hit) in {time() - start_time:.2f} sec')
        return self.best_q1_trajectory

    def to_file(self, filename: str):
        print(f'Writing {len(self.hit_trajectories)} trajectories in {filename}')
        with open(filename, 'w') as f:
            f.write(
                f'target area: '
                f'x={self.target_start.x}..{self.target_end.x}, '
                f'y={self.target_start.y}..{self.target_end.y}\n'
            )
            for trajectory in sorted(self.hit_trajectories, key=attrgetter('highest'), reverse=True):
                f.write(
                    f'trajectory: '
                    f'd={trajectory.initial_velocity.dx}..{trajectory.initial_velocity.dy}, '
                    f'highest={trajectory.highest}\n'
                )


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt',
                        help='Input file')
    parser.add_argument('--output', type=str, default=None,
                        help='If provided writes all trajectory information in the output file')
    args = parser.parse_args()

    world = World.from_file(args.input)
    world.simulate()

    print(f'Q1: best is {world.best_q1_trajectory}')
    print(f'Q2: found {len(world.hit_trajectories)} hit')

    if args.output:
        world.to_file(args.output)
