from argparse import ArgumentParser
from typing import List


def load_input(filename: str) -> List[int]:
    rv = []
    with open(filename, 'r') as f:
        for line in f:
            rv.append(int(line))
    return rv


def count_increase(sonar_data: List[int]) -> int:
    rv = 0
    prev = sonar_data[0]
    for d in sonar_data[1:]:
        if d > prev:
            rv += 1
        prev = d
    return rv


def sum_as_window(sonar_data: List[int], window_size: int = 3) -> List[int]:
    rv = []

    for i in range(len(sonar_data)):
        if i + window_size <= len(sonar_data):
            rv.append(sum(sonar_data[i:i + window_size]))

    return rv


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    args = parser.parse_args()

    content = load_input(args.input)
    print(f"Loaded {len(content)} entries from {args.input}")

    depth_increase = count_increase(content)
    print(f"Q1: {depth_increase} depth increase")

    sum_increase = count_increase(sum_as_window(content))
    print(f"Q2: {sum_increase} depth increase (window=3)")
