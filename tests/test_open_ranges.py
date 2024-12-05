"""
This module tests open ranges in rangy, and it's worth fleashing it out becaused it gets a bit tricky.

What we want is to have:
a label (i.e. open any min, singular, open at least one max
three parts: open vs closed, singular vs range, min vs max

For each label, we want to have multiple accepatable representations.
We then want to have the internal representation (i.e. the tuple) that we expect to get from the input. This represention is an int for fixed values and one of the special characters for open ranges.

We want to test the Range(x).validate(Y), where we a list of valid and invalid values.
"""

import pytest
from rangy import Rangy

class TestOpenRanges:

    @pytest.mark.parametrize("representation", ["*-10", ("*", 10), ("*", "10")])
    def test_open_any_max(self, representation):
        r = Rangy(representation)
        assert r.min == "*"
        assert r.max == 10
        for i in range(0, 11):
            assert r.validates(i)
        assert not r.validates(11)


    @pytest.mark.parametrize("representation", ["3-*", (3, "*"), ("3", "*")])
    def test_open_any_min(self, representation):
        r = Rangy(representation)
        assert r.min == 3
        assert r.max == "*"
        for i in range(3, 100):  # Test a range of values
            assert r.validates(i)
        for i in range(3):
            assert not r.validates(i)


    @pytest.mark.parametrize("representation", ["+-10", ("+", 10), ("+", "10")])
    def test_open_at_least_one_max(self, representation):
        r = Rangy(representation)
        assert r.min == "+"
        assert r.max == 10
        for i in range(1, 11):
            assert r.validates(i)
        assert not r.validates(0)
        assert not r.validates(11)

    @pytest.mark.parametrize("representation", ["3-+", (3, "+"), ("3", "+")])
    def test_open_at_least_one_min(self, representation):
        r = Rangy(representation)
        assert r.min == 3
        assert r.max == "+"
        for i in range(4, 100): #test a range of values.
            assert r.validates(i)
        for i in range(4):
            assert not r.validates(i)



    @pytest.mark.parametrize("representation", ["*-*", ("*", "*")])
    def test_open_any_min_any_max(self, representation):
      r = Rangy(representation)
      assert r.min == "*"
      assert r.max == "*"
      for i in range(-100, 100): # Check negative and positive
        assert r.validates(i)

    @pytest.mark.parametrize("representation", ["*+", ("*", "+")])
    def test_open_any_min_atleastone_max(self, representation):
      r = Rangy(representation)
      assert r.min == "*"
      assert r.max == "+"
      for i in range(1, 100): # Check positive, skip 0
        assert r.validates(i)
      assert not r.validates(0)

    @pytest.mark.parametrize("representation", ["+-*", ("+", "*")])
    def test_open_atleastone_min_any_max(self, representation):
      r = Rangy(representation)
      assert r.min == "+"
      assert r.max == "*"
      for i in range(1, 100): # Check positive
        assert r.validates(i)
      assert not r.validates(0)

    @pytest.mark.parametrize("representation", ["++", ("+", "+")])
    def test_open_atleastone_min_atleastone_max(self, representation):
      r = Rangy(representation)
      assert r.min == "+"
      assert r.max == "+"
      for i in range(2, 100): # Start checking from 2
        assert r.validates(i)
      for i in range(2):
        assert not r.validates(i)


