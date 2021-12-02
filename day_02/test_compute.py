import pytest

from day_02.compute import Action, load_input, ActionType, Location


class TestAction:
    @pytest.mark.parametrize('input, expected', (
        ('forward 5', Action(ActionType.Forward, 5)),
        ('down 5', Action(ActionType.Down, 5)),
        ('up 3', Action(ActionType.Up, 3)),
    ))
    def test_from_str(self, input, expected):
        assert Action.from_str(input) == expected


class TestLocation:

    @pytest.mark.parametrize('action_str, exp', (
        ('forward 4', Location(6, 2)),
        ('down 3', Location(2, 5)),
        ('up 2', Location(2, 0)),
    ))
    def test_naive_reduce_action(self, action_str, exp):
        l = Location(2, 2, aim=0)
        assert l.naive_reduce_action(Action.from_str(action_str)) == exp

    @pytest.mark.parametrize('action_str, exp', (
        ('forward 4', Location(6, 10, aim=2)),
        ('down 3', Location(2, 2, aim=5)),
        ('up 2', Location(2, 2, aim=0)),
    ))
    def test_complex_reduce(self, action_str, exp):
        l = Location(2, 2, aim=2)
        assert l.complex_reduce_action(Action.from_str(action_str)) == exp


def test_load_example():
    assert load_input('example.txt') == [
        Action(ActionType.Forward, 5),
        Action(ActionType.Down, 5),
        Action(ActionType.Forward, 8),
        Action(ActionType.Up, 3),
        Action(ActionType.Down, 8),
        Action(ActionType.Forward, 2),
    ]


def test_q1_example():
    answer = Location.naive_reduce(load_input('example.txt'))
    assert answer == Location(15, 10)
    assert answer.location == 150


def test_q1():
    answer = Location.naive_reduce(load_input('input.txt'))
    assert answer == Location(2085, 785)
    assert answer.location == 1636725


def test_q2_example():
    answer = Location.complex_reduce(load_input('example.txt'))
    assert answer == Location(15, 60, 10)
    assert answer.location == 900


def test_q2():
    answer = Location.complex_reduce(load_input('input.txt'))
    assert answer == Location(2085, 898205, 785)
    assert answer.location == 1872757425
