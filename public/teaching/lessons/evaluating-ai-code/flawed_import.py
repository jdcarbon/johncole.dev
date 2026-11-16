"""Illustrative generated implementation — intentionally imperfect.

This is not an actual transcript from a specific model. It is a classroom
example of plausible AI-generated code that works on a happy path and fails
important requirements.

Known instructional defects include:
- binary floating-point for money
- empty required fields accepted
- invalid rows skipped instead of failing the whole import
- no duplicate detection
- missing columns handled inconsistently / silently
- little useful error reporting
"""

import csv
import io
from datetime import datetime


def import_subscriptions(csv_text: str) -> list[dict]:
    """Import subscription rows from CSV text.

    Appears to work for a basic valid file. Does not implement the lesson's
    all-or-nothing contract.
    """
    reader = csv.DictReader(io.StringIO(csv_text))
    results = []

    for row in reader:
        try:
            name = (row.get("subscription_name") or "").strip()
            vendor = (row.get("vendor") or "").strip()
            # Defect: float for money; missing/blank cost becomes 0.0
            cost = float(row.get("monthly_cost") or 0)
            renewal = datetime.strptime(row.get("renewal_date", ""), "%Y-%m-%d").date()
            results.append(
                {
                    "subscription_name": name,
                    "vendor": vendor,
                    "monthly_cost": cost,
                    "renewal_date": renewal,
                }
            )
        except Exception:
            # Defect: skip bad rows and keep earlier ones (not all-or-nothing)
            continue

    return results
