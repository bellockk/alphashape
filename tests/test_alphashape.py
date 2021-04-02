#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `alphashape` package."""


import unittest
from click.testing import CliRunner
import itertools

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
        alphashape([(0., 1.), (0., 1.)], 0)
        assert shapely.geometry.Point([0., 1.]) == alphashape(
            [(0., 1.), (0., 1.)], 0)

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

    def test_given_a_four_point_polygon_with_small_alpha_return_input(self):
        """
        Given a polygon with four points, and an alpha value of zero, return
        the input as a polygon.
        """
        assert shapely.geometry.Polygon([
            (0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.)]).equals(
                alphashape([(0., 0.), (0., 1.), (1., 1.), (1., 0.)], 1.e-9))

    def test_given_a_four_point_polygon_with_no_alpha_return_input(self):
        """
        Given a polygon with four points, return the input as a polygon.
        """
        assert shapely.geometry.Polygon([
            (0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.)]).equals(
                alphashape([(0., 0.), (0., 1.), (1., 1.), (1., 0.)]))

    def test_3_dimensional_regression_with_dynamic_alpha(self):
        """
        Given a 3-dimensional data set, return an expected set of edges.
        """
        points_3d = [
            (0., 0., 0.), (0., 0., 1.), (0., 1., 0.),
            (1., 0., 0.), (1., 1., 0.), (1., 0., 1.),
            (0., 1., 1.), (1., 1., 1.), (.25, .5, .5),
            (.5, .25, .5), (.5, .5, .25), (.75, .5, .5),
            (.5, .75, .5), (.5, .5, .75)
        ]
        expected = {
        }
        expected_vertices = [
            [0., 0., 0.], [0., 0., 1.], [0., 1., 0.],
            [0., 1., 1.], [1., 0., 0.], [1., 0., 1.],
            [1., 1., 0.], [1., 1., 1.], [0.25, 0.5, 0.5],
            [0.5, 0.25, 0.5], [0.5, 0.5, 0.25], [0.5, 0.5, 0.75],
            [0.5, 0.75, 0.5], [0.75, 0.5, 0.5]]
        expected_faces = [
            (13, 10, 6), (13, 9, 4), (6, 12, 13),
            (13, 12, 7), (5, 11, 9), (8, 10, 0),
            (3, 12, 8), (0, 10, 9), (5, 9, 13),
            (12, 11, 7), (9, 10, 4), (8, 9, 1),
            (12, 10, 2), (13, 11, 5), (1, 11, 8),
            (4, 10, 13), (9, 11, 1), (2, 10, 8),
            (8, 12, 2), (3, 11, 12), (0, 9, 8),
            (7, 11, 13), (6, 10, 12), (8, 11, 3)]
        results = alphashape(points_3d, lambda a, b: 2.1)
        self.assertTrue(len(results.vertices) == len(expected_vertices))
        self.assertTrue(len(points_3d) == len(expected_vertices))
        self.assertTrue(len(results.faces) == len(expected_faces))
        vertex_map = {i: expected_vertices.index(
            list(vertex)) for i,vertex in enumerate(results.vertices)}
        for edge in list(results.faces):
           self.assertTrue(any([(
               vertex_map[e[0]],
               vertex_map[e[1]],
               vertex_map[e[2]]) in expected_faces \
                    for e in itertools.combinations(edge, r=len(edge))]))

    def test_3_dimensional_regression(self):
        """
        Given a 3-dimensional data set, return an expected set of edges.
        """
        points_3d = [
            (0., 0., 0.), (0., 0., 1.), (0., 1., 0.),
            (1., 0., 0.), (1., 1., 0.), (1., 0., 1.),
            (0., 1., 1.), (1., 1., 1.), (.25, .5, .5),
            (.5, .25, .5), (.5, .5, .25), (.75, .5, .5),
            (.5, .75, .5), (.5, .5, .75)
        ]
        expected = {
        }
        expected_vertices = [
            [0., 0., 0.], [0., 0., 1.], [0., 1., 0.],
            [0., 1., 1.], [1., 0., 0.], [1., 0., 1.],
            [1., 1., 0.], [1., 1., 1.], [0.25, 0.5, 0.5],
            [0.5, 0.25, 0.5], [0.5, 0.5, 0.25], [0.5, 0.5, 0.75],
            [0.5, 0.75, 0.5], [0.75, 0.5, 0.5]]
        expected_faces = [
            (13, 10, 6), (13, 9, 4), (6, 12, 13),
            (13, 12, 7), (5, 11, 9), (8, 10, 0),
            (3, 12, 8), (0, 10, 9), (5, 9, 13),
            (12, 11, 7), (9, 10, 4), (8, 9, 1),
            (12, 10, 2), (13, 11, 5), (1, 11, 8),
            (4, 10, 13), (9, 11, 1), (2, 10, 8),
            (8, 12, 2), (3, 11, 12), (0, 9, 8),
            (7, 11, 13), (6, 10, 12), (8, 11, 3)]
        results = alphashape(points_3d, 2.1)
        self.assertTrue(len(results.vertices) == len(expected_vertices))
        self.assertTrue(len(points_3d) == len(expected_vertices))
        self.assertTrue(len(results.faces) == len(expected_faces))
        vertex_map = {i: expected_vertices.index(
            list(vertex)) for i,vertex in enumerate(results.vertices)}
        for edge in list(results.faces):
           self.assertTrue(any([(
               vertex_map[e[0]],
               vertex_map[e[1]],
               vertex_map[e[2]]) in expected_faces \
                    for e in itertools.combinations(edge, r=len(edge))]))

    def test_4_dimensional_regression(self):
        """
        Given a 4-dimensional data set, return an expected set of edges.
        """
        points_4d = [
           (0., 0., 0., 0.), (0., 0., 0., 1.), (0., 0., 1., 0.),
           (0., 1., 0., 0.), (0., 1., 1., 0.), (0., 1., 0., 1.),
           (0., 0., 1., 1.), (0., 1., 1., 1.), (1., 0., 0., 0.),
           (1., 0., 0., 1.), (1., 0., 1., 0.), (1., 1., 0., 0.),
           (1., 1., 1., 0.), (1., 1., 0., 1.), (1., 0., 1., 1.),
           (1., 1., 1., 1.), (.25, .5, .5, .5), (.5, .25, .5, .5),
           (.5, .5, .25, .5), (.5, .5, .5, .25), (.75, .5, .5, .5),
           (.5, .75, .5, .5), (.5, .5, .75, .5), (.5, .5, .5, .75)
        ]
        expected = {
            (16, 1, 2, 0), (16, 1, 3, 0), (16, 2, 3, 0),
            (16, 4, 2, 3), (16, 4, 7, 2), (16, 4, 7, 3),
            (16, 5, 1, 3), (16, 5, 7, 1), (16, 5, 7, 3),
            (16, 6, 1, 2), (16, 6, 7, 1), (16, 6, 7, 2),
            (17, 1, 2, 0), (17, 1, 8, 0), (17, 2, 8, 0),
            (17, 6, 1, 2), (17, 6, 14, 1), (17, 6, 14, 2),
            (17, 9, 1, 8), (17, 9, 14, 1), (17, 9, 14, 8),
            (17, 10, 2, 8), (17, 10, 14, 2), (17, 10, 14, 8),
            (18, 1, 3, 0), (18, 1, 8, 0), (18, 3, 8, 0),
            (18, 5, 1, 3), (18, 5, 13, 1), (18, 5, 13, 3),
            (18, 9, 1, 8), (18, 9, 13, 1), (18, 9, 13, 8),
            (18, 11, 3, 8), (18, 11, 13, 3), (18, 11, 13, 8),
            (19, 2, 3, 0), (19, 2, 8, 0), (19, 3, 8, 0),
            (19, 4, 2, 3), (19, 4, 12, 2), (19, 4, 12, 3),
            (19, 10, 2, 8), (19, 10, 12, 2), (19, 10, 12, 8),
            (19, 11, 3, 8), (19, 11, 12, 3), (19, 11, 12, 8),
            (20, 9, 13, 8), (20, 9, 14, 8), (20, 9, 14, 13),
            (20, 10, 12, 8), (20, 10, 14, 8), (20, 10, 14, 12),
            (20, 11, 12, 8), (20, 11, 13, 8), (20, 11, 13, 12),
            (20, 13, 12, 15), (20, 14, 12, 15), (20, 14, 13, 15),
            (21, 4, 7, 3), (21, 4, 7, 12), (21, 4, 12, 3),
            (21, 5, 7, 3), (21, 5, 7, 13), (21, 5, 13, 3),
            (21, 7, 12, 15), (21, 7, 13, 15), (21, 11, 12, 3),
            (21, 11, 13, 3), (21, 11, 13, 12), (21, 13, 12, 15),
            (22, 4, 7, 2), (22, 4, 7, 12), (22, 4, 12, 2),
            (22, 6, 7, 2), (22, 6, 7, 14), (22, 6, 14, 2),
            (22, 7, 12, 15), (22, 7, 14, 15), (22, 10, 12, 2),
            (22, 10, 14, 2), (22, 10, 14, 12), (22, 14, 12, 15),
            (23, 5, 7, 1), (23, 5, 7, 13), (23, 5, 13, 1),
            (23, 6, 7, 1), (23, 6, 7, 14), (23, 6, 14, 1),
            (23, 7, 13, 15), (23, 7, 14, 15), (23, 9, 13, 1),
            (23, 9, 14, 1), (23, 9, 14, 13), (23, 14, 13, 15)}
        results = alphashape(points_4d, 1.0)
        self.assertTrue(len(results) == len(expected))
        for edge in list(results):
           self.assertTrue(any([e in expected for e in itertools.combinations(
                edge, r=len(edge))]))

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output
