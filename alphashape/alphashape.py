"""
Tools for working with alpha shapes.
"""
__all__ = ['alphashape']

import itertools
import math
from shapely.ops import cascaded_union, polygonize
from shapely.geometry import MultiPoint, MultiLineString
from scipy.spatial import Delaunay
import numpy as np
try:
    import geopandas
    USE_GP = True
except ImportError:
    USE_GP = False


def alphashape(points, alpha=None):
    """
    Compute the alpha shape (concave hull) of a set of points.  If the number
    of points in the input is three or less, the convex hull is returned to the
    user.  For two points, the convex hull collapses to a `LineString`; for one
    point, a `Point`.

    Args:

      points (list or ``shapely.geometry.MultiPoint`` or \
          ``geopandas.GeoDataFrame``): an iterable container of points
      alpha (float): alpha value

    Returns:

      ``shapely.geometry.Polygon`` or ``shapely.geometry.LineString`` or
      ``shapely.geometry.Point`` or ``geopandas.GeoDataFrame``: \
          the resulting geometry
    """
    # If given a geodataframe, extract the geometry
    if USE_GP and isinstance(points, geopandas.GeoDataFrame):
        crs = points.crs
        points = points['geometry']
    else:
        crs = None

    if not isinstance(points, MultiPoint):
        points = MultiPoint(list(points))

    # If given a triangle for input, or an alpha value of zero or less,
    # return the convex hull.
    if len(points) < 4 or (alpha is not None and alpha <= 0):
        result = points.convex_hull
        if crs:
            gdf = geopandas.GeoDataFrame(geopandas.GeoSeries(result)).rename(
                columns={0: 'geometry'}).set_geometry('geometry')
            gdf.crs = crs
            return gdf
        else:
            return result

    # Determine alpha parameter if one is not given
    if alpha is None:
        try:
            from optimizealpha import optimizealpha
        except ImportError:
            from .optimizealpha import optimizealpha
        alpha = optimizealpha(points)

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
        # Precompute value inside square root to avoid unbound math error in
        # case of 0 area triangles.
        area = s * (s - a) * (s - b) * (s - c)

        if area > 0:
            area = math.sqrt(area)

            # Radius Filter
            if a * b * c / (4.0 * area) < 1.0 / alpha:
                for i, j in itertools.combinations([ia, ib, ic], r=2):
                    if (i, j) not in edges and (j, i) not in edges:
                        edges.add((i, j))
                        edge_points.append(coords[[i, j]])

    # Create the resulting polygon from the edge points
    m = MultiLineString(edge_points)
    triangles = list(polygonize(m))
    result = cascaded_union(triangles)

    # Convert to pandas geodataframe object if that is what was an input
    if crs:
        gdf = geopandas.GeoDataFrame(geopandas.GeoSeries(result)).rename(
            columns={0: 'geometry'}).set_geometry('geometry')
        gdf.crs = crs
        return gdf
    else:
        return result
