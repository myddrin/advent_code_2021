import pytest

from day_02.compute import Action, load_input, reduce_q1, reduce_q2


class TestAction:
    @pytest.mark.parametrize('input, expected', (
        ('forward 5', Action(5, 0)),
        ('down 5', Action(0, 5)),
        ('up 3', Action(0, -3)),
    ))
    def test_from_str(self, input, expected):
        assert Action.from_str(input) == expected

    def test_naive_reduce(self):
        a = Action(0, -2)
        b = Action(4, 3)

        assert a.naive_reduce(b) == Action(4, 1)
        assert a.horizontal == 0, 'a should not have been modified'
        assert a.depth == -2, 'a should not have been modified'
        assert b.horizontal == 4, 'b should not have been modified'
        assert b.depth == 3, 'b should not have been modified'

    def test_complex_reduce(self):
        base = Action()

        a = base.complex_reduce(Action.from_str('forward 5'))
        assert a == base, 'complex reduce modifies inplace'
        assert base == Action(5, 0, 0)
        # no aim, depth did not change

        base.complex_reduce(Action.from_str('down 5'))
        assert base == Action(5, 0, 5)

        base.complex_reduce(Action.from_str('forward 8'))
        assert base == Action(13, 40, 5)

        base.complex_reduce(Action.from_str('up 3'))
        assert base == Action(13, 40, 2)


def test_load_example():
    assert load_input('example.txt') == [
        Action(5, 0),
        Action(0, 5),
        Action(8, 0),
        Action(0, -3),
        Action(0, 8),
        Action(2, 0),
    ]


def test_q1_example():
    answer = reduce_q1(load_input('example.txt'))
    assert answer == Action(15, 10)
    assert answer.location == 150


def test_q1():
    answer = reduce_q1(load_input('input.txt'))
    assert answer == Action(2085, 785)
    assert answer.location == 1636725


def test_q2_example():
    answer = reduce_q2(load_input('example.txt'))
    assert answer == Action(15, 60, 10)
    assert answer.location == 900
