from __future__ import annotations

from csv import DictReader
from pathlib import Path

def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    """Read a CSV as a list of rows (each row is a dict of strings)."""
    path = Path(path)
    if not path.exists():
     raise FileNotFoundError(f"CSV not found: {path}")
    with open(path, newline="", encoding="utf-8") as file:
        reader = DictReader(file)
        rows = list(reader)
    if not rows:
      raise ValueError("CSV has no data rows")
    return rows
    

     