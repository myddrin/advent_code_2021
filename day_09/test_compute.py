import pytest

from day_09.compute import Map, Location, Point


class TestPoint:
    @pytest.mark.parametrize('p, diag, exp', (
        (Point(0, 0), True, [
            Point(-1, -1),
            Point(0, -1),
            Point(1, -1),
            #
            Point(-1, 0),
            #Point(0, 0),  # itself
            Point(1, 0),
            #
            Point(-1, 1),
            Point(0, 1),
            Point(1, 1),
        ]),
        (Point(3, 3), True, [
            Point(2, 2),
            Point(3, 2),
            Point(4, 2),
            Point(2, 3),
            # Point(3, 3),  # itself
            Point(4, 3),
            Point(2, 4),
            Point(3, 4),
            Point(4, 4),
        ]),
        (Point(0, 0), False, [
            Point(0, -1),
            #
            Point(-1, 0),
            # Point(0, 0),  # itself
            Point(1, 0),
            #
            Point(0, 1),
        ]),
        (Point(3, 3), False, [
            Point(3, 2),
            Point(2, 3),
            # Point(3, 3),  # itself
            Point(4, 3),
            Point(3, 4),
        ]),
    ))
    def test_neighbour(self, p, diag, exp):
        rv = list(p.neighbours(diag))
        assert len(rv) == len(exp), f'got: {rv}'
        assert rv == exp


class TestLocation:
    @pytest.mark.parametrize('y', (
        0,
        1,
    ))
    def test_from_str(self, y):
        rv = Location.from_str('3987894921', y)
        assert len(rv) == 10
        assert [
            l.height
            for l in rv
        ] == [3, 9, 8, 7, 8, 9, 4, 9, 2, 1]
        assert [
            l.where
            for l in rv
        ] == [
            Point(x, y)
            for x in range(0, 10)
        ]


class TestMap:
    def test_compute_low_points(self):
        rv = Map._compute_low_points(
            [
                Location(Point(0, 0), 2),
                Location(Point(1, 0), 1),  # low point
                Location(Point(2, 0), 9),
                #
                Location(Point(0, 1), 3),
                Location(Point(1, 1), 9),
                Location(Point(2, 1), 8),  # low point
            ]
        )
        for w, l in rv.items():
            assert l.where == w
            if w in (Point(1, 0), Point(2, 1)):
                assert l.is_low_point
            else:
                assert not l.is_low_point

    def test_from_file(self):
        map = Map.from_file('example.txt')
        for l in map.points.values():
            if l.where in (Point(1, 0), Point(9, 0), Point(2, 2), Point(6, 4)):
                assert l.is_low_point
                assert l.risk_level == l.height + 1
            else:
                assert not l.is_low_point
                assert l.risk_level == 0


def test_q1_example():
    assert Map.from_file('example.txt').risk_level() == 15


def test_q1():
    assert Map.from_file('input.txt').risk_level() == 516
