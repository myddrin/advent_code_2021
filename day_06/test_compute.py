import pytest

from day_06.compute import Lanternfish, School


class TestLanternfish:

    @pytest.mark.parametrize('init_age, exp', (
        (0, 1),
        (1, 0),
    ))
    def test_age(self, init_age, exp):
        fish = Lanternfish(init_age)
        assert fish.age() == exp

    def test_make_baby(self):
        fish = Lanternfish.make_baby()
        assert fish.reproduce_in == 8


class TestSchool:

    def test_age(self):
        school = School.from_str('3')
        assert len(school) == 1

        v = school.age()
        assert v == 0
        assert len(school) == 1
        for age, fish in school.fish_by_age.items():
            assert fish.reproduce_in == age
        assert school.fish_by_age[2].count == 1

        v = school.age()
        assert v == 0
        assert len(school) == 1
        for age, fish in school.fish_by_age.items():
            assert fish.reproduce_in == age
        assert school.fish_by_age[1].count == 1

        v = school.age()
        assert v == 0
        assert len(school) == 1
        for age, fish in school.fish_by_age.items():
            assert fish.reproduce_in == age
        assert school.fish_by_age[0].count == 1

        v = school.age()
        assert v == 1
        assert len(school) == 2
        for age, fish in school.fish_by_age.items():
            assert fish.reproduce_in == age
        assert school.fish_by_age[6].count == 1
        assert school.fish_by_age[8].count == 1

        v = school.age()
        assert v == 0
        assert len(school) == 2
        for age, fish in school.fish_by_age.items():
            assert fish.reproduce_in == age
        assert school.fish_by_age[5].count == 1
        assert school.fish_by_age[7].count == 1

    @pytest.mark.parametrize('value, exp', (
        ('3,4,3,1,2', {1: 1, 2: 1, 3: 2, 4: 1}),
        ('2,3,2,0,1', {0: 1, 1: 1, 2: 2, 3: 1}),
    ))
    def test_from_str(self, value, exp):
        school = School.from_str(value)
        assert len(school.fish_by_age) == len(exp)
        assert sum(exp.values()) == len(school)

        for k in sorted(school.fish_by_age):
            assert k in exp
            assert exp.pop(k) == school.fish_by_age[k].count


def test_example_1_q1():
    school = School.load_school('example.txt')
    total = school.simulate(18)
    assert total == 26


def test_example_2_q1():
    school = School.load_school('example.txt')
    total = school.simulate(80)
    assert total == 5934


def test_example_q2():
    school = School.load_school('example.txt')
    total = school.simulate(256)
    assert total == 26984457539


def test_q1():
    assert School.load_school('input.txt').simulate(80) == 385391


def test_q2():
    assert School.load_school('input.txt').simulate(256) == 1728611055389
