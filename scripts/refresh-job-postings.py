#!/usr/bin/env python3
"""
Refresh JobPosting datePosted to first of current month.
Keeps Google Jobs freshness signal alive (Google may de-list postings older than ~30 days).
Run monthly via GitHub Actions (.github/workflows/refresh-jobs.yml).
"""
import re
import sys
from datetime import date
from pathlib import Path

VACANCIES = Path(__file__).resolve().parent.parent / "vacancies.html"


def main() -> int:
    today = date.today()
    first_of_month = today.replace(day=1).isoformat()

    content = VACANCIES.read_text(encoding="utf-8")
    new_content, n = re.subn(
        r'"datePosted":"\d{4}-\d{2}-\d{2}"',
        f'"datePosted":"{first_of_month}"',
        content,
    )

    if n == 0:
        print("No JobPosting datePosted fields found — nothing to update.")
        return 0

    if new_content == content:
        print(f"All {n} datePosted fields already set to {first_of_month}.")
        return 0

    VACANCIES.write_text(new_content, encoding="utf-8")
    print(f"Updated {n} JobPosting.datePosted → {first_of_month}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
