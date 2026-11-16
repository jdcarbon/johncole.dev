"""Acceptance tests for the subscription CSV import contract.

Run against the corrected implementation:

    python3 -m unittest test_import.py

To observe failures in the flawed illustrative implementation, change the
import below to:

    from flawed_import import import_subscriptions
    class ImportError(ValueError):
        pass
"""

from __future__ import annotations

import unittest
from datetime import date
from decimal import Decimal

from corrected_import import ImportError, import_subscriptions

HEADER = "subscription_name,vendor,monthly_cost,renewal_date\n"


class TestImportSubscriptions(unittest.TestCase):
    def test_valid_single_row(self):
        csv_text = HEADER + "App Hosting,CloudHost,49.00,2026-12-01\n"
        rows = import_subscriptions(csv_text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["subscription_name"], "App Hosting")
        self.assertEqual(rows[0]["vendor"], "CloudHost")
        self.assertEqual(rows[0]["monthly_cost"], Decimal("49.00"))
        self.assertIsInstance(rows[0]["monthly_cost"], Decimal)
        self.assertEqual(rows[0]["renewal_date"], date(2026, 12, 1))

    def test_valid_multiple_rows(self):
        csv_text = (
            HEADER
            + "App Hosting,CloudHost,49.00,2026-12-01\n"
            + "Transactional Email,MailCo,29.00,2026-11-20\n"
        )
        rows = import_subscriptions(csv_text)
        self.assertEqual(len(rows), 2)

    def test_empty_required_field_rejected(self):
        csv_text = HEADER + ",CloudHost,49.00,2026-12-01\n"
        with self.assertRaises(ImportError):
            import_subscriptions(csv_text)

    def test_invalid_date_rejected(self):
        csv_text = HEADER + "App Hosting,CloudHost,49.00,12/01/2026\n"
        with self.assertRaises(ImportError):
            import_subscriptions(csv_text)

    def test_invalid_money_rejected(self):
        csv_text = HEADER + "App Hosting,CloudHost,abc,2026-12-01\n"
        with self.assertRaises(ImportError):
            import_subscriptions(csv_text)

    def test_duplicate_subscription_rejected(self):
        csv_text = (
            HEADER
            + "App Hosting,CloudHost,49.00,2026-12-01\n"
            + "App Hosting,CloudHost,59.00,2026-12-15\n"
        )
        with self.assertRaises(ImportError):
            import_subscriptions(csv_text)

    def test_missing_required_column_rejected(self):
        csv_text = "subscription_name,vendor,monthly_cost\nApp Hosting,CloudHost,49.00\n"
        with self.assertRaises(ImportError):
            import_subscriptions(csv_text)

    def test_failure_after_valid_rows_imports_nothing(self):
        csv_text = (
            HEADER
            + "App Hosting,CloudHost,49.00,2026-12-01\n"
            + "Broken Row,MailCo,not-a-number,2026-11-20\n"
            + "Asset Library,DesignKit,39.00,2026-11-28\n"
        )
        with self.assertRaises(ImportError):
            import_subscriptions(csv_text)

    def test_empty_csv_with_headers_returns_empty_list(self):
        rows = import_subscriptions(HEADER)
        self.assertEqual(rows, [])

    def test_decimal_preserves_cents(self):
        csv_text = HEADER + "App Hosting,CloudHost,49.10,2026-12-01\n"
        rows = import_subscriptions(csv_text)
        self.assertEqual(rows[0]["monthly_cost"], Decimal("49.10"))


class TestFlawedImplementationExpectations(unittest.TestCase):
    """Optional checks documenting how the flawed example misbehaves.

    These import flawed_import directly and assert the defective behaviors
    students are meant to discover.
    """

    def test_flawed_uses_float_and_accepts_empty_name(self):
        from flawed_import import import_subscriptions as flawed

        csv_text = HEADER + ",CloudHost,49.00,2026-12-01\n"
        rows = flawed(csv_text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["subscription_name"], "")
        self.assertIsInstance(rows[0]["monthly_cost"], float)

    def test_flawed_returns_partial_results(self):
        from flawed_import import import_subscriptions as flawed

        csv_text = (
            HEADER
            + "App Hosting,CloudHost,49.00,2026-12-01\n"
            + "Broken Row,MailCo,not-a-number,2026-11-20\n"
            + "Asset Library,DesignKit,39.00,2026-11-28\n"
        )
        rows = flawed(csv_text)
        self.assertEqual(len(rows), 2)

    def test_flawed_allows_duplicates(self):
        from flawed_import import import_subscriptions as flawed

        csv_text = (
            HEADER
            + "App Hosting,CloudHost,49.00,2026-12-01\n"
            + "App Hosting,CloudHost,59.00,2026-12-15\n"
        )
        rows = flawed(csv_text)
        self.assertEqual(len(rows), 2)


if __name__ == "__main__":
    unittest.main()
