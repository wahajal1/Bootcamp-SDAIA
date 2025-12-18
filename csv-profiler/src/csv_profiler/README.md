# CSV Profiler

It generates a profiling report for a csv file (as in a whole run down of the csv file).

## Features
CLI: for the json + markdown report
Streamlit GUI: an interface for uploading a csv file then exporting the outcome report as markdown or json

## Setups required before running the project: 
uv venv -p 3.11
uv pip install -r requirements.txt

## Run CLI
# If you have a src/ folder:
#   Mac/Linux: export PYTHONPATH=src
#   Windows:   $env:PYTHONPATH="src"
uv run python -m csv_profiler.cli profile data/sample.csv --out-dir outputs

## Run GUI
# If you have a src/ folder:
#   Mac/Linux: export PYTHONPATH=src
#   Windows:   $env:PYTHONPATH="src"
uv run streamlit run app.py
The CLI writes:
 - `outputs/report.json`
 - `outputs/report.md`

The Streamlit app gives you the ability to:
- upload a csv file
- generate a report for it
- preview the report 
- download the report as JSON + Markdown

![Streamlit UI](./images/ui.png)

