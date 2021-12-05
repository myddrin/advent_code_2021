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
        (Point(7, 0), Point(7, 4), list(map(Point.from_str, ('7,0', '7,1', '7,2', '7,3', '7,4')))),
    ))
    def test_straight_line(self, start, end, exp):
        assert list(start.line(end, straight=True)) == exp
        assert list(end.line(start, straight=True)) == list(reversed(exp))

    @pytest.mark.parametrize('start, end', (
        (Point(8, 0), Point(0, 8)),  # true diagonal
        (Point(0, 8), Point(8, 0)),  # true diagonal
        (Point(0, 1), Point(1, 8)),  # not a true diagonal
    ))
    def test_straight_line_invalid(self, start, end):
        with pytest.raises(ValueError):
            list(start.line(end, straight=True))  # need to consume to be called

    @pytest.mark.parametrize('start, end, exp', (
        (Point(0, 9), Point(5, 9), list(map(Point.from_str, ('0,9', '1,9', '2,9', '3,9', '4,9', '5,9')))),
        (Point(7, 0), Point(7, 4), list(map(Point.from_str, ('7,0', '7,1', '7,2', '7,3', '7,4')))),
        # but also diagonals
        (Point(1, 1), Point(3, 3), list(map(Point.from_str, ('1,1', '2,2', '3,3')))),
        (Point(9, 7), Point(7, 9), list(map(Point.from_str, ('9,7', '8,8', '7,9')))),
    ))
    def test_line(self, start, end, exp):
        assert list(start.line(end, straight=False)) == exp
        assert list(end.line(start, straight=False)) == list(reversed(exp))

    @pytest.mark.parametrize('start, end', (
        (Point(0, 1), Point(1, 8)),  # not a true diagonal
    ))
    def test_line_invalid(self, start, end):
        with pytest.raises(ValueError):
            list(start.line(end, straight=True))  # need to consume to be called


class TestMap:

    def test_load_q1_example(self):
        map = Map.load_map('example.txt', straight=True)
        assert len(map.points) == 21

        assert map.count_more_than(1) == 5

    def test_load_q2_example(self):
        map = Map.load_map('example.txt', straight=False)
        assert len(map.points) == 39

        assert map.count_more_than(1) == 12


def test_q1():
    assert Map.load_map('input.txt', straight=True).count_more_than(1) == 7438


def test_q2():
    assert Map.load_map('input.txt', straight=False).count_more_than(1) == 21406
