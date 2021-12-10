from argparse import ArgumentParser
from enum import Enum
from typing import List, Optional


class Delim(Enum):
    Round = '('
    Square = '['
    Curly = '{'
    Compare = '<'

    CloseRound = ')'
    CloseSquare = ']'
    CloseCurly = '}'
    CloseCompare = '>'

    @property
    def is_closing(self) -> bool:
        return self.closing() is None

    @property
    def points(self) -> int:
        value_map = {
            self.CloseRound: 3,
            self.CloseSquare: 57,
            self.CloseCurly: 1197,
            self.CloseCompare: 25137,
        }
        return value_map.get(self, 0)

    def opening(self) -> Optional["Delim"]:
        opening_map = {
            self.CloseRound: self.Round,
            self.CloseSquare: self.Square,
            self.CloseCurly: self.Curly,
            self.CloseCompare: self.Compare,
        }
        return opening_map.get(self)

    def closing(self) -> Optional["Delim"]:
        closing_map = {
            self.Round: self.CloseRound,
            self.Square: self.CloseSquare,
            self.Curly: self.CloseCurly,
            self.Compare: self.CloseCompare,
        }
        return closing_map.get(self)


class CorruptedLine(RuntimeError):

    def __init__(self, chunk: Delim, line: str, idx: int):
        self.delim = chunk
        self.line = line
        self.index = idx
        super(CorruptedLine, self).__init__(f'CorruptedLine: unexpected "{chunk.value}" at offset {idx}')

    @property
    def points(self) -> int:
        return self.delim.points


def syntax_check(line: str) -> bool:
    """Return false if the line is incomplete. Raises CorruptedLine when the line is corrupted"""
    opened_chunks: List[Delim] = []
    for i, char in enumerate(line):
        delim = Delim(char)  # raise ValueError if invalid char
        if opened_chunks and delim == opened_chunks[-1].closing():
            opened_chunks.pop(-1)  # close last chunk
        elif not delim.is_closing:
            opened_chunks.append(delim)
        else:
            raise CorruptedLine(delim, line, i)

    return len(opened_chunks) == 0


def load_file(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        return [
            line.replace('\n', '')
            for line in f
        ]


def skip_corrupted_lines(lines: List[str]) -> int:
    score = []
    for l in lines:
        try:
            syntax_check(l)
        except CorruptedLine as e:
            score.append(e.points)
    print(f'Found {len(score)} corrupted lines')
    return sum(score)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    args = parser.parse_args()

    lines = load_file(args.input)
    print(f'Loaded {len(lines)} from {args.input}')

    corruption_score = skip_corrupted_lines(lines)
    print(f'Q1: corruption score: {corruption_score}')
