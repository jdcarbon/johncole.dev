"""Tests for the study-time tracker functions."""

import unittest

from study_tracker import (
    average_minutes,
    count_rest_days,
    days_meeting_goal,
    format_summary,
    longest_session,
    total_minutes,
    validate_minutes,
)


class TestStudyTracker(unittest.TestCase):
    def test_total_minutes_normal(self):
        self.assertEqual(total_minutes([10, 20, 30]), 60)

    def test_total_minutes_empty(self):
        self.assertEqual(total_minutes([]), 0)

    def test_average_minutes_normal(self):
        self.assertEqual(average_minutes([10, 20, 30]), 20)

    def test_average_minutes_empty(self):
        self.assertEqual(average_minutes([]), 0)

    def test_days_meeting_goal(self):
        self.assertEqual(days_meeting_goal([45, 30, 60, 0], 45), 2)

    def test_longest_session(self):
        self.assertEqual(longest_session([45, 30, 60, 0]), 60)
        self.assertEqual(longest_session([]), 0)

    def test_count_rest_days(self):
        self.assertEqual(count_rest_days([45, 0, 60, 0]), 2)

    def test_validate_minutes_rejects_negative(self):
        with self.assertRaises(ValueError):
            validate_minutes([10, -5, 20])

    def test_format_summary_contains_totals(self):
        summary = format_summary([45, 30, 60], goal=45)
        self.assertIn("Total: 135 minutes", summary)
        self.assertIn("Days meeting goal (45): 2", summary)


if __name__ == "__main__":
    unittest.main()
