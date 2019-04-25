#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `alphashape` package."""


import unittest
import logging
from click.testing import CliRunner

import shapely
from alphashape.alphashape import alphashape
from alphashape import cli


class TestAlphashape(unittest.TestCase):
    """Tests for `alphashape` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_given_a_point_return_a_point(self):
        """
        Given a point, the alphashape function should return the same point
        """
        assert shapely.geometry.Point([0., 0.]) == alphashape([(0., 0.)], 0)
        assert shapely.geometry.Point([1., 0.]) == alphashape([(1., 0.)], 0)
        assert shapely.geometry.Point([0., 1.]) == alphashape([(0., 1.)], 0)
        assert shapely.geometry.Point([0., 0.]) == alphashape([(0., 0.)], 99)
        assert shapely.geometry.Point([1., 0.]) == alphashape([(1., 0.)], 99)
        assert shapely.geometry.Point([0., 1.]) == alphashape([(0., 1.)], 99)

    def test_given_a_line_with_dupicate_points_return_a_point(self):
        """
        Given a line with duplicate points, the alphashape function should
        return a point
        """
        print(alphashape)
        logging.info(alphashape)
        alphashape([(0., 1.), (0., 1.)], 0)
        assert shapely.geometry.Point([0., 1.]) == alphashape([(0., 1.), (0., 1.)], 0)

    def test_given_a_line_with_unique_points_return_a_line(self):
        """
        Given a line with unique points, the alphashape function should return
        the same line
        """
        assert shapely.geometry.LineString([(0., 0.), (0., 1.)]) == alphashape(
            [(0., 0.), (0., 1.)], 0)
        assert shapely.geometry.LineString([(1., 0.), (0., 1.)]) == alphashape(
            [(1., 0.), (0., 1.)], 0)

    def test_given_a_triangle_with_duplicate_points_returns_a_point(self):
        """
        Given a triangle with two unique points, the alphashape function should
        return a point
        """
        assert shapely.geometry.Point((0., 1.)) == alphashape(
            [(0., 1.), (0., 1.), (0., 1.)], 0)

    def test_given_a_triangle_with_two_duplicate_points_returns_a_line(self):
        """
        Given a line with two unique points, the alphashape function should
        return a line with the unique points
        """
        assert shapely.geometry.LineString([(1., 0.), (0., 1.)]) == alphashape(
            [(1., 0.), (0., 1.), (0., 1.)], 0)

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'alphashape.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
