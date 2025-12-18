

def is_missing(value: str|None)->bool:
 value = value.strip()
 result = False
 if value.strip().casefold() in ["", "na", "n/a", "null", "none", "nan"]:
  result = True
 return result

def try_float(value: float)->float|None:
 try: 
  return float(value)
 except Exception as E:
  return None

def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "number"
def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
    return [row.get(col, "") for row in rows]

def numeric_stats(values: list[str]) -> dict:
    """Compute stats for numeric column values (strings)."""
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    nums: list[float] = []
    for v in usable:
        x = try_float(v)
        if x is None:
            raise ValueError(f"Non-numeric value found: {v!r}")
        nums.append(x)     
    count = len(nums)
    unique = len(set(nums))
    minv = min(nums)
    maxv = max(nums)
    avg = sum(nums)/count
    report = {
          "count: ": count,
          "unique values:": unique,
          "missing": missing,
          "minmum value:": minv,
          "maximum value:": maxv,
          "average:": avg
      }
    return report
from collections import Counter

def is_missing(v: str | None) -> bool:
    return v is None or str(v).strip() == ""

def basic_profile(rows: list[dict[str, str]]) -> dict:
    """Basic profiling: row/col counts, missing per column, unique per column."""
    if not rows:
        return {"n_rows": 0, "n_cols": 0, "columns": []}

    columns = list(rows[0].keys())
    n_rows = len(rows)

    col_reports: list[dict] = []
    for col in columns:
        values = [r.get(col, "") for r in rows]
        usable = [v for v in values if not is_missing(v)]
        missing = len(values) - len(usable)

        report = {
            "name": col,
            "missing": missing,
            "missing_pct": (missing / n_rows * 100.0) if n_rows else 0.0,
            "unique": len(set(usable)),
        }
        col_reports.append(report)

    return {"n_rows": n_rows, "n_cols": len(columns), "columns": col_reports}

numeric_stats(["1", "2", "3", "4", "5"])

# def text_stats(values: list[str], top_k: int = 5) -> dict:
#     """Compute stats for text column values (strings)."""
#     from collections import Counter
#     usable=[v for v in values if not is_missing(v)]
#     missing = len(values)- len()usable
