import re
from functools import reduce
import math

def sum_numbers(a_string):
    """Calculates the sum of integers in a whitespace-separated string.

    The input string must consist only of integers separated by spaces. Any invalid
    format (letters, punctuation, etc.) should be caught by the caller if needed.

    Args:
        a_string (str): A string containing integers separated by spaces.

    Returns:
        int: The sum of all integers in the string.
    """
    return reduce(lambda a, b: a + b, map(int, a_string.split()))


def sum_from_file(filename):
    """Calculates the sum of all integers in a whitespace-separated text file.

    Each line in the file should contain integers separated by spaces. The function
    reads the entire file, checks that the content only contains integers and whitespace,
    and returns the sum of all integers.

    Args:
        filename (str): The path to the text file to be processed.

    Returns:
        int: The sum of all integers in the file.
        None: If the file does not exist.

    Raises:
        ValueError: If the file content includes invalid (non-integer or punctuation) values.
    """
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        return None

    if not re.fullmatch(r'(\d+\s*)*', content):
        raise ValueError("Invalid format: only integers and whitespace allowed.")

    return sum_numbers(content)




def track_points(time, eventParameters):
    """
    Calculate the number of points earned in a timed event.

    The score is determined using the formula:
        points = a * (b - time) ** c
    where `a`, `b`, and `c` are parameters provided in `eventParameters`.

    The result is floored to the nearest integer and clamped at zero if negative.

    Parameters
    ----------
    time : float or int
        The elapsed time of the event.
    eventParameters : list or tuple of length 3
        The parameters `[a, b, c]` defining the scoring formula.

    Returns
    -------
    int
        The number of points, floored to an integer and never less than 0.

    Raises
    ------
    ValueError
        If `eventParameters` does not contain exactly 3 elements.
    """
    if len(eventParameters) != 3:
        raise ValueError
    a, b, c = eventParameters
    points = a * (b - time) ** c
    return math.floor(points) if points >= 0 else 0

def rasterise(list_1D, width):
    """
    Convert a 1D list into a 2D list (matrix) with the given row width.

    The function splits the input list into consecutive chunks of size `width`.
    If the list length is not divisible by `width`, a BufferError is raised.

    Parameters
    ----------
    list_1D : list
        The one-dimensional list to be converted into rows.
    width : int
        The number of elements per row. Must be at least 1.

    Returns
    -------
    list of list
        A two-dimensional list (list of rows) where each row has length `width`.

    Raises
    ------
    ValueError
        If `width` is less than 1.
    BufferError
        If the length of `list_1D` is not divisible by `width`.

    Examples
    --------
    >>> rasterise([1, 2, 3, 4, 5, 6], 2)
    [[1, 2], [3, 4], [5, 6]]

    >>> rasterise([1, 2, 3, 4, 5, 6], 3)
    [[1, 2, 3], [4, 5, 6]]
    """
    if width < 1:
        raise ValueError("ValueError: width must be at least 1!")
    if len(list_1D) % width != 0:
        raise BufferError("BufferError: invalid width!")
    
    list_2D = []
    while list_1D:
        list_2D.append(list_1D[0:width])
        list_1D = list_1D[width:]
    
    return list_2D