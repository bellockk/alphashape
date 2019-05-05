__all__ = ['optimizealpha']
import sys
import logging
import shapely
from shapely.geometry import MultiPoint
import numpy
import alphashape


def _testalpha(alpha, points):
    """
    Test
    """
    polygon = alphashape.alphashape(points, alpha)
    if isinstance(polygon, shapely.geometry.polygon.Polygon) and all(
            [polygon.intersects(point) for point in points]):
        return polygon.area
    else:
        return float('inf')


def optimizealpha(points, max_iterations=10000):
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

    Returns:

        float: The optimized alpha parameter

    """
    if not isinstance(points, MultiPoint):
        points = MultiPoint(list(points))
    # Set the bounds
    lower = 0.

    # Ensure the upper limit bounds the solution
    upper = sys.float_info.max
    if _testalpha(upper, points) != float('inf'):
        logging.error('the max float value does not bound the alpha '
                      'parameter solution')
        return 0.
    counter = 0
    while (upper - lower) > numpy.finfo(float).eps * 2:
        test_alpha = (upper + lower) * .5
        if _testalpha(test_alpha, points) == float('inf'):
            upper = test_alpha
        else:
            lower = test_alpha
        counter += 1
        if counter > max_iterations:
            logging.warning('maximum allowed iterations reached while '
                            'optimizing the alpha parameter')
            break
    return lower
