"""Corrected CSV subscription import for the classroom example."""

from __future__ import annotations

import csv
import io
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

REQUIRED_COLUMNS = (
    "subscription_name",
    "vendor",
    "monthly_cost",
    "renewal_date",
)


class ImportError(ValueError):
    """Raised when the CSV does not satisfy the import contract."""


def import_subscriptions(csv_text: str) -> list[dict]:
    """Import subscriptions using an all-or-nothing validation model.

    Contract:
    - Required columns: subscription_name, vendor, monthly_cost, renewal_date
    - Required fields must be non-empty after stripping whitespace
    - monthly_cost is a decimal amount in USD (no currency column in this version)
    - renewal_date must use YYYY-MM-DD
    - Duplicate identity is (subscription_name, vendor), case-sensitive after strip
    - If any row or header is invalid, raise ImportError and import nothing
    """
    reader = csv.DictReader(io.StringIO(csv_text))
    if reader.fieldnames is None:
        raise ImportError("CSV has no header row")

    headers = [name.strip() if name is not None else "" for name in reader.fieldnames]
    missing = [column for column in REQUIRED_COLUMNS if column not in headers]
    if missing:
        raise ImportError(f"missing required column(s): {', '.join(missing)}")

    pending: list[dict] = []
    seen: set[tuple[str, str]] = set()

    for index, row in enumerate(reader, start=2):
        record = _parse_row(row, index)
        identity = (record["subscription_name"], record["vendor"])
        if identity in seen:
            raise ImportError(
                f"duplicate subscription on line {index}: "
                f"{record['subscription_name']} / {record['vendor']}"
            )
        seen.add(identity)
        pending.append(record)

    return pending


def _parse_row(row: dict, line_number: int) -> dict:
    name = (row.get("subscription_name") or "").strip()
    vendor = (row.get("vendor") or "").strip()
    cost_raw = (row.get("monthly_cost") or "").strip()
    renewal_raw = (row.get("renewal_date") or "").strip()

    if not name:
        raise ImportError(f"line {line_number}: subscription_name is required")
    if not vendor:
        raise ImportError(f"line {line_number}: vendor is required")
    if not cost_raw:
        raise ImportError(f"line {line_number}: monthly_cost is required")
    if not renewal_raw:
        raise ImportError(f"line {line_number}: renewal_date is required")

    try:
        cost = Decimal(cost_raw)
    except InvalidOperation as exc:
        raise ImportError(f"line {line_number}: invalid monthly_cost {cost_raw!r}") from exc

    if not cost.is_finite() or cost < 0:
        raise ImportError(f"line {line_number}: monthly_cost must be a non-negative decimal")

    try:
        renewal = datetime.strptime(renewal_raw, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ImportError(
            f"line {line_number}: renewal_date must be YYYY-MM-DD, got {renewal_raw!r}"
        ) from exc

    return {
        "subscription_name": name,
        "vendor": vendor,
        "monthly_cost": cost,
        "renewal_date": renewal,
        "currency": "USD",
    }


def load_csv_file(path: str) -> list[dict]:
    """Helper for local demos."""
    with open(path, encoding="utf-8") as handle:
        return import_subscriptions(handle.read())


if __name__ == "__main__":
    rows = load_csv_file("sample.csv")
    for row in rows:
        assert isinstance(row["monthly_cost"], Decimal)
        assert isinstance(row["renewal_date"], date)
        print(row)
