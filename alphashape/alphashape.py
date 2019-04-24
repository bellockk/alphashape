# -*- coding: utf-8 -*-

import itertools
import math
from shapely.ops import cascaded_union, polygonize
from shapely.geometry import MultiPoint, MultiLineString
from scipy.spatial import Delaunay
import numpy as np

def get_alpha(points, alpha):
    """
    Compute the alpha shape (concave hull) of a set
    of points.

    @param points: Iterable container of points.

    @param alpha: alpha value to influence the
        gooeyness of the border. Smaller numbers
        don't fall inward as much as larger numbers.
        Too large, and you lose everything.

    Args:

        `points` (``list``): an iterable container of points

        `alpha` (``float``): alpha value

    Returns:

        ``Polygon``: the polygon of the concave hull
    """
    points = MultiPoint(list(points))

    # If given a triangle for input, or an alpha value of zero or less,
    # return the convex hull.
    if len(points) < 4 or alpha <= 0:
        return points.convex_hull

    coords = np.array([point.coords[0] for point in points])
    tri = Delaunay(coords)
    edges = set()
    edge_points = []

    # Loop over triangles
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]

        # Lengths of sides of triangle
        a = math.sqrt((pa[0] - pb[0])**2 + (pa[1] - pb[1])**2)
        b = math.sqrt((pb[0] - pc[0])**2 + (pb[1] - pc[1])**2)
        c = math.sqrt((pc[0] - pa[0])**2 + (pc[1] - pa[1])**2)

        # Semiperimeter of triangle
        s = (a + b + c) * 0.5

        # Area of triangle by Heron's formula
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))

        # Radius Filter
        if area > 0 and a * b * c / (4.0 * area) < 1.0 / alpha:
            for i, j in itertools.combinations([ia, ib, ic], r=2):
                if (i, j) not in edges and (j, i) not in edges:
                    edges.add((i, j))
                    edge_points.append(coords[[i, j]])

    m = MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles)
