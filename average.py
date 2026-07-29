import math
from collections.abc import Sequence


def _is_numeric(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate_numeric_sequence(
    values: Sequence[float | int] | None,
    name: str = "numbers",
) -> Sequence[float | int]:
    if values is None:
        raise TypeError(f"{name} cannot be None")
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise TypeError(f"{name} must be a sequence of numbers")

    for i, value in enumerate(values):
        if not _is_numeric(value):
            raise ValueError(
                f"{name} must contain only numeric values; invalid value at index {i}: {value!r}"
            )
    return values


def average(numbers: Sequence[float | int]) -> float:
    """Calculate the arithmetic mean (average) of all numbers in the sequence.

    Args:
        numbers: A non-empty sequence of int or float values.

    Raises:
        TypeError: If numbers is None or not a sequence of numbers.
        ValueError: If numbers is empty or contains non-numeric values.
    """
    validated = _validate_numeric_sequence(numbers)
    if not validated:
        raise ValueError("Cannot compute average of an empty sequence")
    return math.fsum(validated) / len(validated)


def weighted_average(
    numbers: Sequence[float | int],
    weights: Sequence[float | int],
) -> float:
    """Return the weighted average of a sequence of numbers.

    Args:
        numbers: A non-empty sequence of int or float values.
        weights: Weights corresponding to each number; must sum to a non-zero value.

    Raises:
        TypeError: If either argument is None or not a sequence of numbers.
        ValueError: If sequences are empty, mismatched in length, contain
            non-numeric values, or if weights sum to zero.
    """
    validated_numbers = _validate_numeric_sequence(numbers)
    validated_weights = _validate_numeric_sequence(weights, name="weights")

    if not validated_numbers:
        raise ValueError("Cannot compute weighted average of an empty sequence")
    if len(validated_numbers) != len(validated_weights):
        raise ValueError("Numbers and weights must have the same length")

    total_weight = math.fsum(validated_weights)
    if total_weight == 0:
        raise ValueError("Sum of weights must be non-zero")

    weighted_sum = math.fsum(
        n * w for n, w in zip(validated_numbers, validated_weights)
    )
    return weighted_sum / total_weight


def standard_deviation(numbers: Sequence[float | int]) -> float:
    """Return the sample standard deviation of a sequence of numbers.

    Uses Bessel's correction (divides by n - 1), suitable for sample data.

    Args:
        numbers: A sequence of at least two int or float values.

    Raises:
        TypeError: If numbers is None or not a sequence of numbers.
        ValueError: If numbers has fewer than 2 values or contains non-numeric values.
    """
    validated = _validate_numeric_sequence(numbers)
    n = len(validated)
    if n < 2:
        raise ValueError("Cannot compute standard deviation with fewer than 2 values")

    mean = math.fsum(validated) / n
    variance = math.fsum((x - mean) ** 2 for x in validated) / (n - 1)
    return math.sqrt(variance)

def variance(numbers: Sequence[float | int]) -> float:
    """Return the sample variance of a sequence of numbers."""
    validated = _validate_numeric_sequence(numbers)
    n = len(validated)
    if n < 2:
        raise ValueError("Cannot compute variance with fewer than 2 values")
    mean = math.fsum(validated) / n
    return math.fsum((x - mean) ** 2 for x in validated) / (n - 1)