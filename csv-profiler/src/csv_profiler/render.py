from __future__ import annotations

import json
from pathlib import Path

def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    cols = report.get("columns", [])
    missing = report.get("missing", {})

    lines: list[str] = []
    lines.append("# CSV Profiling Report\n")
    lines.append(f"- Rows: **{report.get('row_count', 0)}**\n")
    if cols:
        lines.append("\n## Columns\n")
        for c in cols:
            lines.append(f"- `{c}` (missing: {missing.get(c, 0)})\n")

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)