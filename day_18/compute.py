import dataclasses
import math
from argparse import ArgumentParser
from copy import deepcopy
from typing import Union, Optional, List

Number = Union["Pair", int]


@dataclasses.dataclass
class Pair:
    left: Number
    right: Number

    _depth: Optional[int] = dataclasses.field(default=None)
    # Do not compare parents when doing __eq__ otherwise it's hell (it's comparing ref to other objects)
    parent: Optional["Pair"] = dataclasses.field(default=None, compare=False)

    @classmethod
    def from_file(cls, filename: str) -> List["Pair"]:
        rv = []
        with open(filename, 'r') as f:
            for line in f:
                rv.append(Pair.from_str(line.replace('\n', '')))
        print(f'Loaded {len(rv)} pairs from {filename}')
        return rv

    @classmethod
    def final_sum(cls, pairs: List["Pair"]) -> "Pair":
        rv = pairs[0]
        for p in pairs[1:]:
            rv = rv + p
        return rv

    @classmethod
    def largest_magnitude(cls, pairs: List["Pair"]) -> "Pair":
        largest_magnitude = 0
        rv = None

        for i, a in enumerate(pairs):
            for j, b in enumerate(pairs):
                if i == j:
                    continue
                current = a + b
                current_magnitude = current.magnitude
                if current_magnitude > largest_magnitude:
                    rv = current
                    largest_magnitude = current_magnitude
        return rv

    @classmethod
    def from_str(cls, source_str: str) -> "Pair":
        root = None
        current = root

        accumulated = ''
        for idx, char in enumerate(source_str):
            if char == '[':
                new_pair = cls(None, None, parent=current)
                if root is None:
                    root = new_pair
                elif current.left is None:
                    current.left = new_pair
                elif current.right is None:
                    current.right = new_pair
                else:
                    raise ValueError('Current is full but we found a new entry! idx={idx}')
                current = new_pair
            elif char == ',':
                if accumulated:
                    current.left = int(accumulated)
                    if current.left is None:
                        raise ValueError(f'Left entry without value. idx={idx}')
                accumulated = ''
            elif char == ']':
                if accumulated:
                    current.right = int(accumulated)
                accumulated = ''
                if current.right is None:
                    raise ValueError(f'Right entry without value. idx={idx}')
                current = current.parent
            else:
                accumulated += char

        if current is not None:
            raise ValueError('Last processed entry is not root.')
        if root is None:
            raise ValueError('Empty string provided')
        return root

    def __post_init__(self):
        if isinstance(self.left, Pair):
            self.left.parent = self
        if isinstance(self.right, Pair):
            self.right.parent = self

    def __str__(self):
        return f'[{self.left},{self.right}]'

    def __add__(self, other: Number) -> "Pair":
        # note: parent is attached in post-init
        # need deepcopy to not modify the original when calling reduce
        return Pair(
            deepcopy(self),
            deepcopy(other),
        ).reduce()

    @property
    def depth(self) -> int:
        if self._depth is None:
            depths = [0]
            if isinstance(self.left, Pair):
                depths.append(self.left.depth)
            if isinstance(self.right, Pair):
                depths.append(self.right.depth)
            self._depth = max(depths) + 1
        return self._depth

    @property
    def magnitude(self) -> int:
        rv = 0
        if isinstance(self.left, Pair):
            rv += 3 * self.left.magnitude
        else:
            rv += 3 * self.left

        if isinstance(self.right, Pair):
            rv += 2 * self.right.magnitude
        else:
            rv += 2 * self.right
        return rv

    def reset(self):
        self._depth = None
        if self.parent:
            self.parent.reset()

    def _add_first_left(self, prev: "Pair", value: int):
        if isinstance(self.left, int):
            # cannot be prev since it's an int!
            self.left += value
        else:
            if self.left is not prev:
                # We reached a point where prev is not on the right but left is not an integer
                # Find the right-most number and add it there
                current = self.left
                while True:
                    if isinstance(current.right, Pair):
                        current = current.right
                    else:
                        current.right += value
                        return
            elif self.parent:
                # Our current left is the previous entry, continue to go up if we can
                self.parent._add_first_left(self, value)

    def _add_first_right(self, prev: "Pair", value: int):
        if isinstance(self.right, int):
            # cannot be prev since it's an int!
            self.right += value
        else:
            if self.right is not prev:
                # Find the left-most number and add it there
                current = self.right
                while True:
                    if isinstance(current.left, Pair):
                        current = current.left
                    else:
                        current.left += value
                        return
            elif self.parent:
                # Our current right is the previous entry, continue to go up
                self.parent._add_first_right(self, value)

    def explode(self, current_depth: int = 1) -> bool:
        left_is_pair = isinstance(self.left, Pair)
        right_is_pair = isinstance(self.right, Pair)

        # if left it does not explode, try the right
        if left_is_pair and self.left.explode(current_depth + 1):
            return True
        elif right_is_pair:
            # Left did not explode, only right can.
            return self.right.explode(current_depth + 1)

        # On a value only pair can explode if the depth > 4
        if not (left_is_pair and right_is_pair) and current_depth > 4:
            # We explode!
            # Add self.left to the first left number we find
            self.parent._add_first_left(self, self.left)
            # Add self.right to the first right number we find
            self.parent._add_first_right(self, self.right)

            # Remove ourselves from our parent (we must have one with current_depth>1)
            if self is self.parent.left:
                self.parent.left = 0
            else:
                self.parent.right = 0
            self.parent.reset()

            return True
        return False

    def split(self) -> bool:
        if isinstance(self.left, Pair):
            if self.left.split():
                return True
            # if it does not split, try the right
        elif self.left >= 10:
            # split the number: left is half rounded down, right is half rounded up
            self.left = Pair(
                self.left // 2,
                int(math.ceil(self.left / 2.0)),
                parent=self,
            )
            self.reset()
            return True

        if isinstance(self.right, Pair):
            # left did not split, only the right can (or cannot)
            return self.right.split()
        elif self.right >= 10:
            self.right = Pair(
                self.right // 2,
                int(math.ceil(self.right / 2.0)),
                parent=self,
            )
            self.reset()
            return True

        return False

    def reduce(self) -> "Pair":
        unstable = True
        while unstable:
            unstable = False
            if self.depth > 4 and self.explode():
                # print(f'after explode: {self}')
                unstable = True
                continue  # we do not try split yet
            if self.split():
                unstable = True
                # print(f'after split: {self}')
        return self


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file.')
    args = parser.parse_args()

    exercise = Pair.from_file(args.input)
    final_sum = Pair.final_sum(exercise)
    print(f'Final pair is: {final_sum}')
    print(f'Q1: magnitude is {final_sum.magnitude}')

    largest = Pair.largest_magnitude(exercise)
    print(f'Q2: largest magnitude from a single addition: {largest}')
    print(f'Q2: i.e: {largest.magnitude}')
