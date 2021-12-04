import dataclasses
from typing import List, Iterator, Dict, Tuple, Optional

@dataclasses.dataclass
class Board:
    entries: List[List["Board.Entry"]] = dataclasses.field(default_factory=list)
    entry_map: Dict[int, Tuple[int, int]] = dataclasses.field(default_factory=dict)

    @dataclasses.dataclass
    class Entry:
        value: int
        selected: bool = False

        def __str__(self):
            if self.selected:
                return f"*{self.value:2d}*"
            return f" {self.value:2d} "

    def append(self, numbers: Iterator[int]):
        y = len(self.entries)
        line = [
            self.Entry(n)
            for n in numbers
        ]
        self.entries.append(line)
        for x, e in enumerate(line):
            self.entry_map[e.value] = (x, y)

    def _col_bingo(self, col: int) -> bool:
        v = []
        for line in self.entries:
            v.append(line[col].selected)
        return all(v)

    def _row_bingo(self, col: int) -> bool:
        v = [e.selected for e in self.entries[col]]
        return all(v)

    def unmarked_score(self) -> int:
        return sum((
            v.value
            for line in self.entries
            for v in line
            if not v.selected
        ))

    def check(self, value: int) -> Optional[Tuple[int, int]]:
        """Check number and return score if there was a bingo!"""
        if value in self.entry_map:
            x, y = self.entry_map[value]
            self.entries[y][x].selected = True

            if self._col_bingo(x) or self._row_bingo(y):
                return x, y

        return None

    def display(self) -> List[str]:
        rows = []
        for line in self.entries:
            rows.append(' '.join((str(e) for e in line)))
        return rows


@dataclasses.dataclass
class Game:
    numbers: List[int]
    boards: List[Board]

    @classmethod
    def load_game(cls, filename: str) -> "Game":
        numbers = []
        boards = []
        current_board = None

        with open(filename, 'r') as f:
            for line in f:
                line = line.replace('\n', '')
                if not numbers:
                    numbers = list(map(int, line.split(',')))
                    continue

                if not line:
                    # Start a new board on empty lines
                    current_board = Board()
                    boards.append(current_board)
                else:
                    current_board.append(map(int, (v for v in line.split(' ') if v)))

        return cls(numbers, boards)

    def play(self, st: int = 0, end: int = None) -> Optional[Tuple[int, int]]:
        if end is None:
            end = len(self.numbers)

        for turn, n in enumerate(self.numbers[st:end], start=st):
            for bi, b in enumerate(self.boards):
                v = b.check(n)
                if v is not None:
                    print(f"Bingo on {n}! (turn {turn} board {bi} location {v})")
                    return bi, b.unmarked_score() * n

        return None


if __name__ == '__main__':
    game = Game.load_game('input.txt')
    print(f"Loaded {len(game.boards)} boards and {len(game.numbers)} numbers")

    score = game.play()
    if score is None:
        print('Nobody won!')
    else:
        print(f"Q1: board {score[0]} wins with score of {score[1]}")
