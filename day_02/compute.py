import dataclasses
from argparse import ArgumentParser
from enum import Enum
from typing import List


class ActionType(Enum):
    Forward = 'forward'
    Down = 'down'
    Up = 'up'


@dataclasses.dataclass
class Action:
    move: "ActionType"
    value: int

    @classmethod
    def from_str(cls, content: str) -> "Action":
        action, value = content.split(' ')
        return cls(ActionType(action), int(value))


@dataclasses.dataclass()
class Location:
    horizontal: int = 0
    depth: int = 0
    aim: int = 0

    @classmethod
    def naive_reduce(cls, data: List[Action]) -> "Location":
        rv = Location()
        for d in data:
            rv.naive_reduce_action(d)
        return rv

    @classmethod
    def complex_reduce(cls, data: List[Action]) -> "Location":
        rv = Location()
        for d in data:
            rv.complex_reduce_action(d)
        return rv

    @property
    def location(self) -> int:
        return self.horizontal * self.depth

    def __str__(self):
        return f"(horiz={self.horizontal}, depth={self.depth}, aim={self.aim}) location={self.location}"

    def naive_reduce_action(self, action: "Action") -> "Location":
        if action.move == ActionType.Forward:
            self.horizontal += action.value
        elif action.move == ActionType.Down:
            self.depth += action.value
        elif action.move == ActionType.Up:
            self.depth -= action.value
        else:
            raise ValueError(f'Unexpected ActionType in {action}')

        return self

    def complex_reduce_action(self, action: "Action") -> "Location":
        if action.move == ActionType.Forward:
            self.horizontal += action.value
            self.depth += self.aim * action.value
        elif action.move == ActionType.Down:
            self.aim += action.value
        elif action.move == ActionType.Up:
            self.aim -= action.value
        else:
            raise ValueError(f'Unexpected ActionType in {action}')

        return self


def load_input(filename: str) -> List[Action]:
    rv = []
    with open(filename, 'r') as f:
        for line in f:
            try:
                rv.append(Action.from_str(line))
            except:
                raise ValueError(f'Could not unpack an action from "{line}"')
    return rv


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    args = parser.parse_args()

    input_data = load_input(args.input)
    print(f'Loaded {len(input_data)} actions from {args.input}')

    final_position = Location.naive_reduce(input_data)
    print(f"Q1: final position: {final_position}")

    complete_position = Location.complex_reduce(input_data)
    print(f"Q2: complete position: {complete_position}")
