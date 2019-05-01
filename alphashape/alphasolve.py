__all__ = ['alphasolve']
from .alphashape import alphashape


def alphasolve(points):
    """
    Solve for the alpha parameter.

    Attempt to determine the alpha parameter that best wraps the given set of
    points in one polygon without dropping any points.

    Args:

        points (list): an iterable container of points

    Returns:

        float or None: The optimized alpha parameter or None to indicate a solution could not be found.

    """
    pass
