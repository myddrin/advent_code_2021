from typing import List

import pytest

from day_08.compute import Panel, Pattern


class TestPannel:
    small_example = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'

    @classmethod
    def make_panel(cls, patterns: List[str], output: List[str]) -> Panel:
        return Panel(
            Panel.sort_entries(*patterns),
            Panel.sort_entries(*output),
        )

    def test_from_str(self):
        assert Panel.from_str(self.small_example) == self.make_panel(
            ['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab'],
            ['cdfeb', 'fcadb', 'cdfeb', 'cdbaf'],
        )

    def test_from_file(self):
        data = Panel.from_file('example.txt')
        assert len(data) == 10

        assert data[4] == self.make_panel(
            ['aecbfdg', 'fbg', 'gf', 'bafeg', 'dbefa', 'fcge', 'gcbea', 'fcaegb', 'dgceab', 'fcbdga'],
            ['gecf', 'egdcabf', 'bgf', 'bfgea'],
        )

    @pytest.mark.parametrize('value, exp_count, exp_match', (
        (
            'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
            2,
            {
                'be': Pattern.One,
                'abcdefg': Pattern.Eight,
                'bceg': Pattern.Four,
                'bde': Pattern.Seven,
            },
        ),
        (
            small_example,
            0,
            {
                'abcdefg': Pattern.Eight,
                'abd': Pattern.Seven,
                'abef': Pattern.Four,
                'ab': Pattern.One,
            },
        ),
    ))
    def test_easy_match(self, value, exp_count, exp_match):
        panel = Panel.from_str(value)
        assert panel.easy_match() == exp_count
        assert panel.digit_match == exp_match

    def test_add_match(self):
        all_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

        panel = Panel.from_str(self.small_example)
        assert panel.segment_match == {
            'a': all_letters,
            'b': all_letters,
            'c': all_letters,
            'd': all_letters,
            'e': all_letters,
            'f': all_letters,
            'g': all_letters,
        }

        # panel.easy_match()
        # assert panel.digit_match == {
        #     'abcdefg': Pattern.Eight,
        #     'abd': Pattern.Seven,
        #     'abef': Pattern.Four,
        #     'ab': Pattern.One,
        # }
        panel._add_match(Pattern.Eight, ''.join(all_letters))
        assert panel.segment_match == {
            'a': all_letters,
            'b': all_letters,
            'c': all_letters,
            'd': all_letters,
            'e': all_letters,
            'f': all_letters,
            'g': all_letters,
        }

        panel._add_match(Pattern.Seven, 'abd')  # 7: acf
        assert panel.segment_match == {
            'a': ['a', 'b', 'd'],
            'b': all_letters,
            'c': ['a', 'b', 'd'],
            'd': all_letters,
            'e': all_letters,
            'f': ['a', 'b', 'd'],
            'g': all_letters,
        }

        panel._add_match(Pattern.Four, 'abef')  # 4: bcdf
        assert panel.segment_match == {
            'a': ['a', 'b', 'd'],
            'b': ['a', 'b', 'e', 'f'],
            'c': ['a', 'b'],  # not d, e, f
            'd': ['a', 'b', 'e', 'f'],
            'e': all_letters,
            'f': ['a', 'b'],  # not d, e, f
            'g': all_letters,
        }

        panel._add_match(Pattern.One, 'ab')  # 1: cf
        assert panel.segment_match == {
            'a': ['a', 'b', 'd'],
            'b': ['a', 'b', 'e', 'f'],
            'c': ['a', 'b'],  # not d, e, f
            'd': ['a', 'b', 'e', 'f'],
            'e': all_letters,
            'f': ['a', 'b'],  # not d, e, f
            'g': all_letters,
        }

    def test_update_segment_invalid_assumption(self):
        all_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        current = {
            'a': ['a', 'b', 'd'],
            'b': ['a', 'b', 'e', 'f'],
            'c': ['a', 'b'],  # not d, e, f
            'd': ['a', 'b', 'e', 'f'],
            'e': all_letters,
            'f': ['a', 'b'],  # not d, e, f
            'g': all_letters,
        }
        # 2: acdeg
        Panel.update_segment(current, 'a', 'cdefh')
        assert current == {
            'a': ['d'],
            'b': ['a', 'b', 'e', 'f'],
            'c': ['a', 'b'],
            'd': ['a', 'b', 'e', 'f'],
            'e': ['a', 'b', 'c', 'e', 'f', 'g'],
            'f': ['a', 'b'],
            'g': ['a', 'b', 'c', 'e', 'f', 'g'],
        }
        with pytest.raises(ValueError):
            Panel.update_segment(current, 'c', 'cdefh')

    def test_potential(self):
        assert Panel.potential(3) == [
            [0, 1, 2],
            [0, 2, 1],
            [1, 0, 2],
            [1, 2, 0],
            [2, 0, 1],
            [2, 1, 0],
        ]

    def test_hard_match(self):
        panel = Panel.from_str(self.small_example)

        panel.easy_match()
        rv = panel.hard_match(panel.patterns, panel.segment_match)
        assert rv is not None
        assert len(rv) == 6
        expected = {
            # 'ab': Pattern.One,
            'acdfg': Pattern.Two,
            'abcdf': Pattern.Three,
            # 'abef': Pattern.Four,
            'bcdef': Pattern.Five,
            'bcdefg': Pattern.Six,
            # 'bad': Pattern.Seven,
            # 'abcdefg': Pattern.Eight,
            'abcdef': Pattern.Nine,
            'abcdeg': Pattern.Zero,
        }
        for k, v in expected.items():
            assert k in rv, f'Not in {rv.keys()}'
            assert rv[k] == v

    @pytest.mark.parametrize('value, exp', (
        (small_example, 5353),
        ('be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe', 8394),
    ))
    def test_value(self, value, exp):
        panel = Panel.from_str(value)
        assert panel.value() == exp

    def test_value_from_example(self):
        data = Panel.from_file('example.txt')
        assert [
            d.value()
            for d in data
        ] == [
            8394,
            9781,
            1197,
            9361,
            4873,
            8418,
            4548,
            1625,
            8717,
            4315,
        ]


def test_example_q1():
    assert Panel.count_easy_match(Panel.from_file('example.txt')) == 26


def test_q1():
    assert Panel.count_easy_match(Panel.from_file('input.txt')) == 367


def test_example_q2():
    assert Panel.all_values(Panel.from_file('example.txt')) == 61229


def test_q2():
    assert Panel.all_values(Panel.from_file('input.txt')) == 974512
