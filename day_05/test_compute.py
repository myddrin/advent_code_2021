import pytest

from day_05.compute import Point, Map


class TestPoint:

    @pytest.mark.parametrize('value, exp', (
        ('0,9', Point(0, 9)),
        ('8,0', Point(8, 0)),
    ))
    def test_from_str(self, value, exp):
        assert Point.from_str(value) == exp

    @pytest.mark.parametrize('start, end, exp', (
        (Point(0, 9), Point(5, 9), list(map(Point.from_str, ('0,9', '1,9', '2,9', '3,9', '4,9', '5,9')))),
        (Point(5, 9), Point(0, 9), list(map(Point.from_str, ('0,9', '1,9', '2,9', '3,9', '4,9', '5,9')))),
        (Point(7, 0), Point(7, 4), list(map(Point.from_str, ('7,0', '7,1', '7,2', '7,3', '7,4')))),
        (Point(7, 4), Point(7, 0), list(map(Point.from_str, ('7,0', '7,1', '7,2', '7,3', '7,4')))),
    ))
    def test_straight_line(self, start, end, exp):
        rv_s = list(start.straight_line(end))
        assert rv_s == exp

    @pytest.mark.parametrize('start, end', (
        (Point(8, 0), Point(0, 8)),
        (Point(0, 8), Point(8, 0)),
    ))
    def test_straight_line_invalid(self, start, end):
        with pytest.raises(ValueError):
            list(start.straight_line(end))  # need to consume to be called


class TestMap:

    def test_load_q1_example(self):
        map = Map.load_map('example.txt', straight=True)
        assert len(map.points) == 21

        assert map.count_more_than(1) == 5


def test_q1():
    assert Map.load_map('input.txt', straight=True).count_more_than(1) == 7438
