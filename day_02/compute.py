import dataclasses
from typing import List


@dataclasses.dataclass
class Action:
    horizontal: int
    depth: int

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

    def __add__(self, other: "Action") -> "Action":
        return Action(self.horizontal + other.horizontal, self.depth + other.depth)

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


if __name__ == '__main__':

    data = load_input('input.txt')

    final_position = sum(data, start=Action(0, 0))
    print(f"Q1: final position: {final_position}")
