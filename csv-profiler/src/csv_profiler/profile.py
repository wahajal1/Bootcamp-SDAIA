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
    min = min(nums)
    max = max(nums)
    avg = sum(nums)/count
    report = {
          "count: ": count,
          "unique values:": unique,
          "minmum value:": min,
          "maximum value:": max,
          "average:": avg
      }
    return report
numeric_stats(["1", "2", "3", "4", "5"])

# def text_stats(values: list[str], top_k: int = 5) -> dict:
#     """Compute stats for text column values (strings)."""
#     from collections import Counter
#     usable=[v for v in values if not is_missing(v)]
#     missing = len(values)- len()usable
