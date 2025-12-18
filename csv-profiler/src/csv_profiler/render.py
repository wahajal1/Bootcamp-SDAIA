from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

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
from datetime import datetime

def render_markdown(report: dict) -> str:
    lines: list[str] = []

    lines.append("# CSV Profiling Report")
    lines.append("")
    lines.append(f"- **Generated:** {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"- **Rows:** {report.get('n_rows', 0)}")
    lines.append(f"- **Columns:** {report.get('n_cols', 0)}")
    if "timing_ms" in report:
        lines.append(f"- **Timing:** {report['timing_ms']:.2f} ms")
    lines.append("")

    
    lines.append("## Columns")
    lines.append("")
    lines.append("| name | missing | missing % | unique |")
    lines.append("|---|---:|---:|---:|")

    for c in report.get("columns", []):
        lines.append(
            f"| {c.get('name','')} | "
            f"{c.get('missing',0)} | "
            f"{c.get('missing_pct',0.0):.1f}% | "
            f"{c.get('unique',0)} |"
        )

    lines.append("")
    lines.append("## Notes")
    lines.append("- Missing values are empty strings or nulls")

    return "\n".join(lines)
