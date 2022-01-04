import pytest

from day_25.compute import Map, Direction, Position, Cucumber


class TestMap:

    def test_load_example(self):
        rv = Map.from_file('example.txt')
        expected = [
            'v...>>.vv>',
            '.vv>>.vv..',
            '>>.>v>...v',
            '>>v>>.>.v.',
            'v>v.vv.v..',
            '>.>>..v...',
            '.vv..>.>v.',
            'v.v..>>v.v',
            '....v..v.>',
        ]

        assert rv.width == len(expected[0])
        assert rv.height == len(expected)
        assert rv.render() == expected

    @pytest.mark.parametrize('moves, expected', (
        (1, [
            '....>.>v.>',
            'v.v>.>v.v.',
            '>v>>..>v..',
            '>>v>v>.>.v',
            '.>v.v...v.',
            'v>>.>vvv..',
            '..v...>>..',
            'vv...>>vv.',
            '>.v.v..v.v',
        ]),
        (58, [
            '..>>v>vv..',
            '..v.>>vv..',
            '..>>v>>vv.',
            '..>>>>>vv.',
            'v......>vv',
            'v>v....>>v',
            'vvv.....>>',
            '>vv......>',
            '.>v.vv.v..',
        ]),
    ))
    def test_move_example(self, moves, expected):
        rv = Map.from_file('example.txt')
        for _ in range(moves):
            rv.move()
        assert rv.render() == expected

    def test_q1_example(self):
        rv = Map.from_file('example.txt')
        rv = rv.find_stop()
        assert rv == 58


class TestCucumber:

    @pytest.mark.parametrize('cucumber, width, height, expected', (
        (Cucumber(Position(3, 0), Direction.East), 10, 9, Position(4, 0)),
        (Cucumber(Position(9, 0), Direction.East), 10, 9, Position(0, 0)),
        (Cucumber(Position(3, 0), Direction.South), 10, 9, Position(3, 1)),
        (Cucumber(Position(3, 8), Direction.South), 10, 9, Position(3, 0)),
    ))
    def test_next_position(self, cucumber: Cucumber, width: int, height: int, expected: Position):
        assert cucumber.next_position(width, height) == expected


def test_q1():
    assert Map.from_file('input.txt').find_stop() == 374
