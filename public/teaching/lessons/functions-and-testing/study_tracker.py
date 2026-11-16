"""Weekly study-time tracker — decomposed into focused functions."""


def total_minutes(minutes):
    """Return the sum of study minutes for the week."""
    return sum(minutes)


def average_minutes(minutes):
    """Return the average daily study minutes, or 0 for an empty list."""
    if not minutes:
        return 0
    return total_minutes(minutes) / len(minutes)


def days_meeting_goal(minutes, goal):
    """Return how many days meet or exceed the study goal."""
    return sum(1 for value in minutes if value >= goal)


def longest_session(minutes):
    """Return the longest single session, or 0 for an empty list."""
    if not minutes:
        return 0
    return max(minutes)


def count_rest_days(minutes):
    """Return how many days have zero study minutes."""
    return sum(1 for value in minutes if value == 0)


def validate_minutes(minutes):
    """Raise ValueError if any duration is negative."""
    for value in minutes:
        if value < 0:
            raise ValueError(f"study minutes cannot be negative: {value}")


def format_summary(minutes, goal):
    """Return a readable summary string for the week."""
    validate_minutes(minutes)
    total = total_minutes(minutes)
    average = average_minutes(minutes)
    met_goal = days_meeting_goal(minutes, goal)
    return (
        f"Total: {total} minutes\n"
        f"Daily average: {average:.1f} minutes\n"
        f"Days meeting goal ({goal}): {met_goal}"
    )


if __name__ == "__main__":
    study_minutes = [45, 30, 60, 0, 25, 50, 40]
    print(format_summary(study_minutes, goal=45))
