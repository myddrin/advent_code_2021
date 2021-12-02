import pytest

from day_02.compute import Action, load_input


class TestAction:
    @pytest.mark.parametrize('input, expected', (
        ('forward 5', Action(5, 0)),
        ('down 5', Action(0, 5)),
        ('up 3', Action(0, -3)),
    ))
    def test_from_str(self, input, expected):
        assert Action.from_str(input) == expected

    def test_add(self):
        a = Action(0, -2)
        b = Action(4, 3)

        assert a + b == Action(4, 1)
        assert a.horizontal == 0, 'a should not have been modified'
        assert a.depth == -2, 'a should not have been modified'
        assert b.horizontal == 4, 'b should not have been modified'
        assert b.depth == 3, 'b should not have been modified'


def test_load_example():
    assert load_input('example.txt') == [
        Action(5, 0),
        Action(0, 5),
        Action(8, 0),
        Action(0, -3),
        Action(0, 8),
        Action(2, 0),
    ]


def test_q1():
    answer = sum(load_input('input.txt'), Action(0, 0))
    assert answer == Action(2085, 785)
    assert answer.location == 1636725
