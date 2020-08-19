__all__ = ['optimizealpha']
import sys
import logging
import shapely
from shapely.geometry import MultiPoint
import numpy
try:
    import geopandas
    USE_GP = True
except ImportError:
    USE_GP = False


def _testalpha(points, alpha):
    """
    Evaluates an alpha parameter.

    This helper function creates an alpha shape with the given points and alpha
    parameter.  It then checks that the produced shape is a Polygon and that it
    intersects all the input points.

    Args:
        points (``shapely.geometry.Multipoint``): data points
        alpha (float): alpha value

    Returns:
        bool: True if the resulting alpha shape is a single polygon that
            intersects all the input data points.
    """
    try:
        from alphashape import alphashape
    except ImportError:
        from .alphashape import alphashape
    polygon = alphashape(points, alpha)
    if isinstance(polygon, shapely.geometry.polygon.Polygon) and all(
            [polygon.intersects(point) for point in points]):
        return True
    else:
        return False


def optimizealpha(points, max_iterations: int = 10000, lower: float = 0.,
                  upper: float = sys.float_info.max, silent: bool = False):
    """
    Solve for the alpha parameter.

    Attempt to determine the alpha parameter that best wraps the given set of
    points in one polygon without dropping any points.

    Note:  If the solver fails to find a solution, a value of zero will be
    returned, which when used with the alphashape function will safely return a
    convex hull around the points.

    Args:

        points (list): an iterable container of points
        max_iterations (int): maximum number of iterations while finding the
            solution
        lower (float): lower limit for optimization
        upper (float): upper limit for optimization
        silent (bool): silence warnings

    Returns:

        float: The optimized alpha parameter

    """
    # Convert to a shapely multipoint object if not one already
    if USE_GP and isinstance(points, geopandas.GeoDataFrame):
        points = points['geometry']
    if not isinstance(points, MultiPoint):
        points = MultiPoint(list(points))

    # Set the bounds
    assert lower >= 0, "The lower bounds must be at least 0"
    # Ensure the upper limit bounds the solution
    assert upper <= sys.float_info.max, (
        f'The upper bounds must be less than or equal to {sys.float_info.max} '
        'on your system')

    if _testalpha(points, upper):
        if not silent:
            logging.error('the max float value does not bound the alpha '
                          'parameter solution')
        return 0.

    # Begin the bisection loop
    counter = 0
    while (upper - lower) > numpy.finfo(float).eps * 2:
        # Bisect the current bounds
        test_alpha = (upper + lower) * .5

        # Update the bounds to include the solution space
        if _testalpha(points, test_alpha):
            lower = test_alpha
        else:
            upper = test_alpha

        # Handle exceeding maximum allowed number of iterations
        counter += 1
        if counter > max_iterations:
            if not silent:
                logging.warning('maximum allowed iterations reached while '
                                'optimizing the alpha parameter')
            lower = 0.
            break
    return lower
