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

def circumcenter(points):
    """
    Calculate the circumcenter of a set of points in barycentric coordinates.

    Args:
      points: An `N`x`K` array of points which define an (`N`-1) simplex in K
        dimensional space.  `N` and `K` must satisfy 1 <= `N` <= `K` and
        `K` >= 1.

    Returns:
      The circumcenter of a set of points in barycentric coordinates.
    """
    points = np.asarray(points)
    num_rows, num_columns = points.shape
    A = np.bmat([[2 * np.dot(points, points.T),
                  np.ones((num_rows, 1))],
                 [np.ones((1, num_rows)), np.zeros((1,1))]])
    b = np.hstack((np.sum(points * points, axis=1),
                   np.ones((1))))
    return np.linalg.solve(A, b)[:-1]

def circumradius(points):
    """
    Calculte the circumradius of a given set of points.

    Args:
      points: An `N`x`K` array of points which define an (`N`-1) simplex in K
        dimensional space.  `N` and `K` must satisfy 1 <= `N` <= `K` and
        `K` >= 1.

    Returns:
      The circumradius of a given set of points.
    """
    points = np.asarray(points)
    return np.linalg.norm(points[0,:] - np.dot(circumcenter(points), points))

def alphasimplices(points):
    """
    Returns an iterator of simplices and their circumradii of the given set of
    points.

    Args:
      points: An `N`x`M` array of points.

    Yields:
      A simplex, and its circumradius as a tuple.
    """
    coords = np.asarray(points)
    tri = Delaunay(coords)

    for simplex in tri.simplices:
        simplex_points = coords[simplex]
        yield simplex, circumradius(simplex_points)


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
    edges = set()
    perimeter_edges = set()

    for point_indices, circumradius in alphasimplices(coords):
        # Radius filter
        if callable(alpha):
            alpha = alpha(point_indices, circumradius)
        if circumradius < 1.0 / alpha:
            for edge in itertools.combinations(
                    point_indices, r=coords.shape[-1]):
                if all([e not in edges for e in itertools.combinations(
                        edge, r=len(edge))]):
                    edges.add(edge)
                    perimeter_edges.add(edge)
                else:
                    perimeter_edges -= set(itertools.combinations(edge,
                        r=len(edge)))

    if coords.shape[-1] > 3:
        return perimeter_edges
    elif coords.shape[-1] == 3:
        import trimesh
        result = trimesh.Trimesh(vertices=coords, faces=list(perimeter_edges))
        trimesh.repair.fix_normals(result)
        return result

    # Create the resulting polygon from the edge points
    m = MultiLineString([coords[np.array(edge)] for edge in perimeter_edges])
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
