import pytest

from day_08.compute import Panel


class TestPannel:
    small_example = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'

    def test_from_str(self):
        assert Panel.from_str(self.small_example) == Panel(
            ['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab'],
            ['cdfeb', 'fcadb', 'cdfeb', 'cdbaf'],
        )

    def test_from_file(self):
        data = Panel.from_file('example.txt')
        assert len(data) == 10

        assert data[4] == Panel(
            ['aecbfdg', 'fbg', 'gf', 'bafeg', 'dbefa', 'fcge', 'gcbea', 'fcaegb', 'dgceab', 'fcbdga'],
            ['gecf', 'egdcabf', 'bgf', 'bfgea'],
        )

    @pytest.mark.parametrize('value, exp_count, exp_match', (
        (
            'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
            2,
            {
                1: ['be'],
                8: ['cfbegad', 'fdgacbe'],
                4: ['cgeb', 'gcbe'],
                7: ['edb'],
            },
        ),
    ))
    def test_easy_match(self, value, exp_count, exp_match):
        panel = Panel.from_str(value)
        assert panel.easy_match() == exp_count
        assert panel.digit_match == exp_match


def test_example_q1():
    assert Panel.count_easy_match(Panel.from_file('example.txt')) == 26


def test_q1():
    assert Panel.count_easy_match(Panel.from_file('input.txt')) == 367