from typing import List

import pytest

from day_11.compute import Map, Point


class TestPoint:
    @pytest.mark.parametrize('where, expected', (
        (Point(0, 0), [
            Point(-1, -1),
            Point(0, -1),
            Point(1, -1),
            Point(-1, 0),
            # Point(0, 0),  # itself
            Point(1, 0),
            Point(-1, 1),
            Point(0, 1),
            Point(1, 1),
        ]),
    ))
    def test_neighbours(self, where, expected):
        assert list(where.neighbours()) == expected


class TestMap:

    @pytest.mark.parametrize('init, grid, exp_flashes', (
        (['123', '456', '543'], ['234', '567', '654'], 0),
        (['123', '494', '567'], ['345', '606', '789'], 1),
        (['111', '191', '191'], ['333', '404', '404'], 2),
        (['11111', '19991', '19191', '19991', '11111'], ['34543', '40004', '50005', '40004', '34543'], 9),
        (['34543', '40004', '50005', '40004', '34543'], ['45654', '51115', '61116', '51115', '45654'], 0),
        ([
            '4334',
            '5822',
            '7284',
            '7257',
            '6589',
        ], [
            '6555',
            '7054',
            '9608',
            '8600',
            '7800',
        ], 6),
    ))
    def test_simulate(self, init: List[str], grid: List[str], exp_flashes: int):
        data = Map({})
        for y, l in enumerate(init):
            data.octopi.update(Map.from_str(l, y))
        expected_grid = [
            list(map(int, line))
            for line in grid
        ]

        actual_flash = data.simulate(1)
        assert data.energy_grid() == expected_grid
        assert actual_flash == exp_flashes

    @pytest.mark.parametrize('turns, exp_flashes', (
        (1, 0),
        (5, 0 + 35 + 45 + 16 + 8),
        (10, 204),
        (100, 1656),
    ))
    def test_example(self, turns, exp_flashes):
        data = Map.from_file('example.txt')
        assert data.simulate(turns) == exp_flashes

    def test_q2_example(self):
        assert Map.from_file('example.txt').simulate_until_synchronous() == 195


def test_q1():
    assert Map.from_file('input.txt').simulate(100) == 1615


def test_q2():
    assert Map.from_file('input.txt').simulate_until_synchronous() == 249
