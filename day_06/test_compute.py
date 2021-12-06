import pytest

from day_06.compute import Lanternfish, School


class TestLanternfish:

    @pytest.mark.parametrize('init_age, exp', (
        (0, Lanternfish(8)),
        (1, None),
    ))
    def test_age(self, init_age, exp):
        fish = Lanternfish(init_age)
        if exp is not None:
            assert fish.age() == exp
        else:
            assert fish.age() is None


class TestSchool:

    def test_age(self):
        school = School([Lanternfish(3)])
        assert len(school) == 1

        v = school.age()
        assert v == 0
        assert len(school) == 1
        assert school[0].reproduce_in == 2

        v = school.age()
        assert v == 0
        assert len(school) == 1
        assert school[0].reproduce_in == 1

        v = school.age()
        assert v == 0
        assert len(school) == 1
        assert school[0].reproduce_in == 0

        v = school.age()
        assert v == 1
        assert len(school) == 2
        assert school[0].reproduce_in == 6
        assert school[1].reproduce_in == 8

        v = school.age()
        assert v == 0
        assert len(school) == 2
        assert school[0].reproduce_in == 5
        assert school[1].reproduce_in == 7

    @pytest.mark.parametrize('value', (
        '3,4,3,1,2',
        '2,3,2,0,1',
    ))
    def test_from_str(self, value):
        school = School.from_str(value)
        assert [f.reproduce_in for f in school.fish] == list(map(int, value.split(',')))


def test_example_1_q1():
    school = School.load_school('example.txt')
    total = school.simulate(18)
    assert total == 26


def test_example_2_q1():
    school = School.load_school('example.txt')
    total = school.simulate(80)
    assert total == 5934


def test_q1():
    assert School.load_school('input.txt').simulate(80) == 385391
