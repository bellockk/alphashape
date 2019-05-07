#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `alphashape` package."""


import unittest

from alphashape import optimizealpha


class TestOptimizeAlapha(unittest.TestCase):
    """Tests for `alphashape` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_given_a_point_return_a_point(self):
        """
        Given a point, the alphashape function should return the same point
        """
        alpha = optimizealpha(
            [(0., 0.), (0., 1.), (1., 1.), (1., 0.),
             (0.5, 0.25), (0.5, 0.75), (0.25, 0.5), (0.75, 0.5)])
        assert alpha > 3. and alpha < 3.5
