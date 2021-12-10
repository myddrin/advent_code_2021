import dataclasses
from argparse import ArgumentParser
from enum import Enum
from typing import List, Optional, Tuple


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
    def corrupted_points(self) -> int:
        value_map = {
            self.CloseRound: 3,
            self.CloseSquare: 57,
            self.CloseCurly: 1197,
            self.CloseCompare: 25137,
        }
        return value_map.get(self, 0)

    @property
    def autocomplete_points(self) -> int:
        value_map = {
            self.CloseRound: 1,
            self.CloseSquare: 2,
            self.CloseCurly: 3,
            self.CloseCompare: 4,
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
        return self.delim.corrupted_points


@dataclasses.dataclass
class Parser:
    lines: List[str]
    corruption_score: int
    autocomplete_score: int

    def to_file(self, filename: str):
        print(f'Writing {len(self.lines)} lines into {filename}')
        with open(filename, 'w') as f:
            for l in self.lines:
                f.write(l + '\n')

    @classmethod
    def validate(cls, line: str) -> Tuple[str, int]:
        """Return autocompleted line and score for this line or raise CorruptedLine"""
        opened_chunks: List[Delim] = []
        for i, char in enumerate(line):
            delim = Delim(char)  # raise ValueError if invalid char
            if opened_chunks and delim == opened_chunks[-1].closing():
                opened_chunks.pop(-1)  # close last chunk
            elif not delim.is_closing:
                opened_chunks.append(delim)
            else:
                raise CorruptedLine(delim, line, i)

        rv = line
        score = 0
        for d in reversed(opened_chunks):
            close_with = d.closing()
            rv += close_with.value
            score = (score * 5) + close_with.autocomplete_points
        return rv, score

    @classmethod
    def from_file(cls, filename: str) -> "Parser":
        input_lines = 0
        corruption_score = []
        autocomplete_score = []
        final_lines = []

        with open(filename, 'r') as f:
            for line in f:
                input_lines += 1
                line = line.replace('\n', '')
                try:
                    validated_line, autoc_score = cls.validate(line)
                except CorruptedLine as e:
                    corruption_score.append(e.points)
                else:
                    final_lines.append(validated_line)
                    if autoc_score != 0:
                        autocomplete_score.append(autoc_score)

        print(f'Loaded {input_lines} lines from {filename}, '
              f'{len(corruption_score)} were corrupted, '
              f'{len(autocomplete_score)} were incomplete')
        # we want the middle score for autocompletion (size//2 + 1) but we're 0 base: -1 so size//2 is enough
        middle_autocomplete = sorted(autocomplete_score)[(len(autocomplete_score) // 2)]
        return cls(final_lines, sum(corruption_score), middle_autocomplete)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    parser.add_argument('--output', type=str, default=None, help='Output file (all correct lines)')
    args = parser.parse_args()

    data = Parser.from_file(args.input)
    print(f'Q1: corruption score: {data.corruption_score}')
    print(f'Q2: autocomplete score: {data.autocomplete_score}')

    if args.output is not None:
        data.to_file(args.output)
