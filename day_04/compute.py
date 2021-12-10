import dataclasses
from argparse import ArgumentParser
from typing import List, Iterator, Dict, Tuple, Optional

@dataclasses.dataclass
class Board:
    entries: List[List["Board.Entry"]] = dataclasses.field(default_factory=list)
    entry_map: Dict[int, Tuple[int, int]] = dataclasses.field(default_factory=dict)
    finished: bool = False  # when the board was won

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
class Score:
    board: int
    score: int
    turn: int
    value: int

    def __str__(self):
        return f"Bingo on {self.value}! turn {self.turn} board {self.board} score {self.score}"


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

    def play(self, start: int = 0, end: int = None) -> Optional[Score]:
        if end is None:
            end = len(self.numbers)

        for turn, n in enumerate(self.numbers[start:end], start=start):
            for bi, b in enumerate(self.boards):
                if b.finished:
                    continue

                v = b.check(n)
                if v is not None:
                    b.finished = True
                    return Score(
                        bi,
                        b.unmarked_score() * n,
                        turn,
                        n
                    )

        return None

    def finished_boards(self):
        return sum((
            1
            for b in self.boards
            if b.finished
        ))

    def until_last(self, start: int = 0) -> Optional[Score]:
        finished = self.finished_boards()
        turn = start
        score = None
        while finished != len(self.boards):
            score = self.play(turn)
            if score is None:
                return score
            turn = score.turn
            finished = self.finished_boards()
            # print(f"Found {str(score)} finished={finished}")

        return score


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    args = parser.parse_args()

    game = Game.load_game(args.input)
    print(f"Loaded {len(game.boards)} boards and {len(game.numbers)} numbers from {args.input}")

    score = game.play()
    if score is None:
        print('Nobody won!')
    else:
        print(f"Q1: {str(score)}")

    last_score = game.until_last(start=score.turn)
    if last_score is None:
        print('No last board!?')
    else:
        print(f"Q2: {str(last_score)}")
