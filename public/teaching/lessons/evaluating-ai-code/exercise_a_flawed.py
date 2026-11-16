"""Exercise A — find the defect.

This helper looks correct for ordinary lists, but mishandles a boundary case.
"""


def average_positive(numbers):
    """Return the average of values strictly greater than zero.

    Intended contract:
    - Ignore zeros and negative numbers.
    - If no positive numbers remain, return 0.
    """
    total = 0
    count = 0
    for value in numbers:
        if value > 0:
            total += value
            count += 1
    return total / count
