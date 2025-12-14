def basic_profile(rows: list[dict[str, str]]) -> dict:
    """Compute row count, column names, and missing values per column."""
    if not rows:
        return {
            "row_count": 0,
            "columns": [],
            "missing": {},
        }

    columns = list(rows[0].keys())
    missing = {c: 0 for c in columns}

    for row in rows:
        for c in columns:
            v = (row.get(c) or "").strip()
            if v == "":
                missing[c] += 1

    return {
        "row_count": len(rows),
        "columns": columns,
        "missing": missing,
    }
