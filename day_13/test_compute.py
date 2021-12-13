import pytest

from day_13.compute import Point, Paper, Instruction, Direction, load_data


@pytest.fixture
def example() -> Paper:
    rv = Paper()
    for pv in (
        '6,10',
        '0,14',
        '9,10',
        '0,3',
        '10,4',
        '4,11',
        '6,0',
        '6,12',
        '4,1',
        '0,13',
        '10,12',
        '3,4',
        '3,0',
        '8,4',
        '1,10',
        '2,14',
        '8,10',
        '9,0',
    ):
        rv.add(Point.from_str(pv))
    return rv


class TestPaper:
    # TODO(tr) example fold even
    def test_content(self, example):
        expected = [
            '...#..#..#.',
            '....#......',
            '...........',
            '#..........',
            '...#....#.#',
            '...........',
            '...........',
            '...........',
            '...........',
            '...........',
            '.#....#.##.',
            '....#......',
            '......#...#',
            '#..........',
            '#.#........',
        ]
        assert example.width == len(expected[0])
        assert example.height == len(expected)

        assert example.content() == expected

    def test_fold_up(self, example):
        expected = [
            '#.##..#..#.',
            '#...#......',
            '......#...#',
            '#...#......',
            '.#.#..#.###',
            '...........',
            '...........',
        ]

        actual = example.fold_up(7)
        assert actual.width == len(expected[0])
        assert actual.height == len(expected)
        assert actual.content() == expected

    def test_fold_left(self, example):
        expected = [
            '#####',
            '#...#',
            '#...#',
            '#...#',
            '#####',
            '.....',
            '.....',
        ]

        # assuming fold_up is correct
        actual = example.fold_up(7).fold_left(5)
        assert actual.width == len(expected[0])
        assert actual.height == len(expected)
        assert actual.content() == expected


class TestInstruction:
    @pytest.mark.parametrize('value, expected', (
        ('fold along y=7', Instruction(Direction.Up, 7)),
        ('fold along x=5', Instruction(Direction.Left, 5)),
    ))
    def test_from_str(self, value, expected):
        assert Instruction.from_str(value) == expected


def test_q1_example():
    paper, instructions = load_data('example.txt')
    actual = paper.perform(instructions[:1])
    assert len(actual.dots) == 17
    assert actual.content() == [
        '#.##..#..#.',
        '#...#......',
        '......#...#',
        '#...#......',
        '.#.#..#.###',
        '...........',
        '...........',
    ]


def test_q1():
    paper, instructions = load_data('input.txt')
    assert len(paper.perform(instructions[:1]).dots) == 795


def test_q2():
    paper, instructions = load_data('input.txt')
    assert paper.perform(instructions).content() == [
        '.##..####...##.#..#.#....#..#..##....##.',
        '#..#.#.......#.#.#..#....#..#.#..#....#.',
        '#....###.....#.##...#....#..#.#.......#.',
        '#....#.......#.#.#..#....#..#.#.##....#.',
        '#..#.#....#..#.#.#..#....#..#.#..#.#..#.',
        '.##..####..##..#..#.####..##...###..##..',
    ]  # CEJKLUGJ
