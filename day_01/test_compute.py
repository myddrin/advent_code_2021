import pytest

from day_01.compute import load_input, count_increase, sum_as_window


def test_load_input():
    assert load_input('example.txt') == [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


@pytest.mark.parametrize('data, exp', (
    ([199, 200, 208, 210, 200, 207, 240, 269, 260, 263], 7),
    ([607, 618, 618, 617, 647, 716, 769, 792], 5)
))
def test_count_increase(data, exp):
    assert count_increase(data) == exp


def test_sum_as_window():
    assert sum_as_window(
        [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    ) == [
        199 + 200 + 208,
        200 + 208 + 210,
        208 + 210 + 200,
        210 + 200 + 207,
        200 + 207 + 240,
        207 + 240 + 269,
        240 + 269 + 260,
        269 + 260 + 263,
    ]


def test_q1():
    assert count_increase(load_input('input.txt')) == 1722


def test_q2():
    assert count_increase(sum_as_window(load_input('input.txt'))) == 1748
