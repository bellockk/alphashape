__all__ = ['optimizealpha']
from .alphashape import alphashape
import shapely
from scipy.optimize import minimize_scalar


def _testalpha(alpha, points):
    """
    Test
    """
    polygon = alphashape(points, alpha)
    if isinstance(polygon, shapely.geometry.polygon.Polygon) and all(
            [polygon.contains(shapely.geometry.Point(
                *point)) for point in points]):
        return polygon.area
    else:
        return float('inf')


def optimizealpha(points):
    """
    Solve for the alpha parameter.

    Attempt to determine the alpha parameter that best wraps the given set of
    points in one polygon without dropping any points.

    Note:  If the solver fails to find a solution, a value of zero will be
    returned, which when used with the alphashape function will safely return a
    convex hull around the points.

    Args:

        points (list): an iterable container of points

    Returns:

        float: The optimized alpha parameter

    """
    result = minimize_scalar(_testalpha, args=(points))
    if result.success and result.x != float('inf'):
        return result.x
    else:
        return 0.
