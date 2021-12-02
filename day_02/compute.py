import dataclasses
from functools import reduce
from typing import List


@dataclasses.dataclass
class Action:
    horizontal: int = 0
    depth: int = 0
    aim: int = 0

    @classmethod
    def from_str(cls, content: str) -> "Action":
        action, value = content.split(' ')
        if action == 'forward':
            return cls(int(value), 0)
        elif action == 'down':
            return cls(0, int(value))
        elif action == 'up':
            return cls(0, -int(value))

    @property
    def location(self):
        return self.horizontal * self.depth

    def naive_reduce(self, other: "Action") -> "Action":
        return Action(self.horizontal + other.horizontal, self.depth + other.depth)

    def complex_reduce(self, other: "Action") -> "Action":
        if other.depth > 0:
            # "down"
            self.aim += other.depth
        elif other.depth < 0:
            # "up"
            self.aim += other.depth
        else:
            # "forward"
            self.horizontal += other.horizontal
            self.depth += self.aim * other.horizontal

        return self

    def __str__(self):
        return f"({self.horizontal}, {self.depth})->{self.location}"


def load_input(filename: str) -> List[Action]:
    rv = []
    with open(filename, 'r') as f:
        for line in f:
            try:
                rv.append(Action.from_str(line))
            except:
                raise ValueError(f'Could not unpack an action from "{line}"')
    return rv


def reduce_q1(data: List[Action]) -> Action:
    return reduce(Action.naive_reduce, data, Action())


def reduce_q2(data: List[Action]) -> Action:
    return reduce(Action.complex_reduce, data, Action())


if __name__ == '__main__':

    data = load_input('input.txt')

    final_position = reduce_q1(data)
    print(f"Q1: final position: {final_position}")

    complete_position = reduce_q2(data)
    print(f"Q2: complete position: {complete_position}")
