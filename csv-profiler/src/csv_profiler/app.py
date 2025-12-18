import streamlit as st
from pathlib import Path
from io import StringIO
from csv import DictReader
import json 
#from csv_profiler.io import read_csv_rows

def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    """Read a CSV as a list of rows (each row is a dict of strings)."""
    path = Path(path)
    with open(path, newline="", encoding="utf-8") as file:
        reader = DictReader(file)
        return list(reader)
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

def render_markdown(report: dict) -> str:
    """Generates the Markdown string content from the report."""
    cols = report.get("columns", [])
    missing = report.get("missing", {})

    lines: list[str] = []
    lines.append("# CSV Profiling Report\n")
    lines.append(f"- Rows: **{report.get('row_count', 0)}**\n")
    
    if cols:
        lines.append("\n## Columns\n")
        for c in cols:
            lines.append(f"- `{c}` (missing: {missing.get(c, 0)})\n")
            
    # Join list of strings into one single string for display/download
    return "".join(lines)

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.caption("Upload a CSV → profile it → export JSON + Markdown")
st.sidebar.header("Inputs")
source = st.sidebar.selectbox("Data source", ["Upload"])
st.write("Selected:", source)

ar = read_csv_rows("data/sample.csv")

uploaded = st.file_uploader("Upload a csv", type = ["csv"])
preview = st.checkbox("Show preview", value = False)
try:
    if uploaded is not None:
        text = uploaded.getvalue().decode("utf-8-sig")
        rows = list(DictReader(StringIO(text)))
        st.write("Filename:", uploaded.name)
        st.write("Size (bytes):", uploaded.size)
        
        if st.button("Generate Report"):
         st.session_state["report"] = basic_profile(rows)
    else:
        st.info("Please upload a CSV file to proceed.")
    report = st.session_state.get("report")
    if report is not None: 
        st.subheader("Markdown preview")
        st.write("Rows:", report["row_count"])
        st.write("Columns:", report["columns"])
        render_markdown(report)
        st.markdown(render_markdown(report))
    
    report_name = st.sidebar.text_input("Report name", value ="report")
    json_file = report_name + ".json"
    json_text = json.dumps(report, indent=2, ensure_ascii=False)
    md_file = report_name +".md"
    md_text = render_markdown(report)
    jsoncol, mdcol = st.columns(2)
    jsoncol.download_button("Download json", json_text, json_file)
    mdcol.download_button("Download Markdown", md_text, md_file)
    if st.button("save to outputs/"):
        path = Path("outputs/")
        path.parent.mkdir(parents = True, exist_ok = True)
        (path/json_file).write_text(json_text, encoding = "utf-8")
        st.success(f"Report saved to {path/json_file}")
       
    if preview == True: 
        st.write(ar[:5])
        st.write("Rows:", len(ar))

except Exception as E:
    st.error(f"Error processing file: {E}")

