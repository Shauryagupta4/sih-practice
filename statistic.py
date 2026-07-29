import math
from collections import Counter
from collections.abc import Sequence

from average import _validate_numeric_sequence


def _require_non_empty(validated: Sequence[float | int], operation: str) -> None:
    if not validated:
        raise ValueError(f"Cannot compute {operation} of an empty sequence")


def _percentile(sorted_values: list[float | int], p: float) -> float:
    """Return the p-th percentile using linear interpolation."""
    n = len(sorted_values)
    if n == 1:
        return float(sorted_values[0])

    k = (n - 1) * p / 100
    lower = math.floor(k)
    upper = math.ceil(k)
    if lower == upper:
        return float(sorted_values[int(k)])

    lower_value = sorted_values[lower]
    upper_value = sorted_values[upper]
    return float(lower_value + (upper_value - lower_value) * (k - lower))


def median(numbers: Sequence[float | int]) -> float:
    """Return the median of a sequence of numbers.

    For an even-length sequence, returns the average of the two middle values.

    Args:
        numbers: A non-empty sequence of int or float values.

    Raises:
        TypeError: If numbers is None or not a sequence of numbers.
        ValueError: If numbers is empty or contains non-numeric values.
    """
    validated = _validate_numeric_sequence(numbers)
    _require_non_empty(validated, "median")

    sorted_values = sorted(validated)
    n = len(sorted_values)
    mid = n // 2

    if n % 2 == 1:
        return float(sorted_values[mid])

    return (sorted_values[mid - 1] + sorted_values[mid]) / 2


def mode(numbers: Sequence[float | int]) -> float | int:
    """Return the most frequently occurring value in a sequence of numbers.

    Args:
        numbers: A non-empty sequence of int or float values.

    Raises:
        TypeError: If numbers is None or not a sequence of numbers.
        ValueError: If numbers is empty, contains non-numeric values, or has
            no unique mode.
    """
    validated = _validate_numeric_sequence(numbers)
    _require_non_empty(validated, "mode")

    counts = Counter(validated)
    max_count = max(counts.values())
    modes = [value for value, count in counts.items() if count == max_count]

    if len(modes) > 1:
        raise ValueError("No unique mode found")

    return modes[0]


def quartiles(numbers: Sequence[float | int]) -> tuple[float, float, float]:
    """Return the first, second, and third quartiles of a sequence of numbers.

    Quartiles are computed using linear interpolation (Q1 at 25%, Q2 at 50%,
    Q3 at 75%).

    Args:
        numbers: A non-empty sequence of int or float values.

    Returns:
        A tuple of (Q1, Q2, Q3), where Q2 is the median.

    Raises:
        TypeError: If numbers is None or not a sequence of numbers.
        ValueError: If numbers is empty or contains non-numeric values.
    """
    validated = _validate_numeric_sequence(numbers)
    _require_non_empty(validated, "quartiles")

    sorted_values = sorted(validated)
    q1 = _percentile(sorted_values, 25)
    q2 = _percentile(sorted_values, 50)
    q3 = _percentile(sorted_values, 75)
    return q1, q2, q3
