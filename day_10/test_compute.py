import pytest

from day_10.compute import syntax_check, Delim, CorruptedLine, load_file, skip_corrupted_lines


class TestDelim:
    @pytest.mark.parametrize('delim', list(Delim))
    def test_all(self, delim):
        if delim.is_closing:
            assert delim.points != 0
            assert delim.opening() is not None
            assert delim.closing() is None
            assert delim.opening().closing() == delim
        else:
            assert delim.points == 0
            assert delim.opening() is None
            assert delim.closing() is not None
            assert delim.closing().opening() == delim


class TestSyntaxCheck:
    @pytest.mark.parametrize('value', (
        '()',
        '[]',
        '{}',
        '<>',
        '([])',
        '{()()()}',
        '<([{}])>',
        '[<>({}){}[([])<>]]',
        '(((((((((())))))))))',
    ))
    def test_valid_syntax(self, value):
        assert syntax_check(value) is True

    @pytest.mark.parametrize('value, exp_delim, exp_idx', (
        ('(]', Delim.CloseSquare, 1),
        ('{()()()>', Delim.CloseCompare, 7),
        ('(((()))}', Delim.CloseCurly, 7),
        ('<([]){()}[{}])', Delim.CloseRound, 13),
    ))
    def test_corrupted_lines(self, value, exp_delim, exp_idx):
        try:
            syntax_check(value)
        except CorruptedLine as e:
            assert e.delim == exp_delim
            assert e.index == exp_idx
            assert e.line == value
        else:
            assert False, 'Should have raised'


def test_q1_example():
    assert skip_corrupted_lines(load_file('example.txt')) == 26397


def test_q1():
    assert skip_corrupted_lines(load_file('input.txt')) == 318081
