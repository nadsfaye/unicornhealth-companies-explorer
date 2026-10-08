# Unicorn Companies Explorer

A beginner-friendly Python data analysis project that explores where companies in a unicorn-company dataset are located. It includes a guided notebook, a command-line script, and a small sample dataset.

## Questions explored

- Which countries have the most companies in the loaded dataset?
- How are those companies distributed across continents?
- What percentage of the dataset does each country represent?

## Data and limits

The included sample was manually transcribed from 10 visible rows of a learning workspace screenshot supplied by the project owner. It is a small convenience sample, not a representative global dataset. Singapore's city was blank in the screenshot. No valuations, funding figures, industries, or dates were supplied, so this project makes no claims about them. Sample results describe those 10 rows only.

Use your own authorized full CSV for a broader analysis. Required columns: `company_id`, `company`, `country`, `continent`. An optional `city` column is preserved. Exact duplicate records are removed; conflicting records with the same ID produce an error; missing geographic fields are labeled `Unknown`.

## Run locally

Use Python 3.10 or newer. From this project folder:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python analyze.py
```

On Windows, activate with `.venv\Scripts\activate` instead. The script prints summaries and creates two CSV summaries and a PNG chart in `outputs/`.

To analyze your own data:

```bash
python analyze.py --input data/companies.csv
```

## Open the notebook

```bash
jupyter lab unicorn_analysis.ipynb
```

The notebook walks through loading, inspection, cleaning, country and continent summaries, visualization, and interpretation. GitHub can display the saved notebook, including its sample outputs.

## Use in the workspace shown in the screenshot

Your SQL cell already makes its results available as `df`. Add a Python cell below it and use the quick-start code from the accompanying chat. The current SQL query has `LIMIT 10`, so it analyzes only those 10 returned rows. To analyze all rows in the table, run `SELECT * FROM companies;` first.


## Skills demonstrated

Python functions, pandas DataFrames, data validation, grouping, percentages, chart creation, command-line arguments, and clear documentation.
