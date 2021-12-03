import pytest

from day_03.compute import ReportBinary, load_input, extract_rates, filter_report


class TestReoportBinary:

    @pytest.mark.parametrize('value, exp', (
        ('00100', 4),
        ('01001', 9),
    ))
    def test_from_str(self, value, exp):
        assert ReportBinary.from_str(value) == ReportBinary(exp)

    @pytest.mark.parametrize('value', (
        '00100',
        '01001',
        '1111',
    ))
    def test_to_binary_str(self, value):
        assert ReportBinary.from_str(value).to_binary_str(len(value)) == value

    @pytest.mark.parametrize('value, exp', (
        ('100', 3),
        ('1001', 4),
        ('11111', 5),
        ('0', 1)
    ))
    def test_binary_digit(self, value, exp):
        assert ReportBinary.from_str(value).bit_length == exp


def test_q2_example_o2():
    report, bit_size = load_input('example.txt')

    o2_report = filter_report(report, bit_size, ReportBinary.o2_filter)
    assert len(o2_report) == 1
    assert o2_report == [ReportBinary.from_str('10111')]


def test_q2_example_co2():
    report, bit_size = load_input('example.txt')

    co2_report = filter_report(report, bit_size, ReportBinary.co2_filter)
    assert len(co2_report) == 1
    assert co2_report == [ReportBinary.from_str('01010')]


def test_q1_example():
    report, bit_size = load_input('example.txt')
    gama, epsilon = extract_rates(report, bit_size)
    assert gama.value == 22
    assert epsilon.value == 9


def test_q1():
    gama, epsilon = extract_rates(*load_input('input.txt'))
    assert gama.value == 284
    assert epsilon.value == 3811
    assert gama.value * epsilon.value == 1082324


def test_q2():
    report, bit_size = load_input('input.txt')
    o2_rating = filter_report(report, bit_size, ReportBinary.o2_filter)
    assert len(o2_rating) == 1
    assert o2_rating[0].value == 486

    co2_rating = filter_report(report, bit_size, ReportBinary.co2_filter)
    assert len(co2_rating) == 1
    assert co2_rating[0].value == 2784

    assert o2_rating[0].value * co2_rating[0].value == 1353024
