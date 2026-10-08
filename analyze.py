"""Explore company geography from a CSV. Run with --help for options."""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Save charts even on computers without a display.
import matplotlib.pyplot as plt
import pandas as pd


def clean_companies(df):
    """Validate fields, clean text, and keep one record per company ID."""
    required = {"company_id", "company", "country", "continent"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    data = df.copy()
    for column in ["company_id", "company", "country", "continent"]:
        data[column] = data[column].astype("string").str.strip().replace("", pd.NA)
    if data[["company_id", "company"]].isna().any().any():
        raise ValueError("Every row needs a company_id and company name.")
    # Reject conflicting identities rather than silently discard information.
    unique_rows = data.drop_duplicates().copy()
    if unique_rows["company_id"].duplicated().any():
        raise ValueError("A company ID has conflicting records. Resolve these before analysis.")
    for column in ["country", "continent"]:
        unique_rows[column] = unique_rows[column].fillna("Unknown")
    return unique_rows.reset_index(drop=True)


def summarize(data, column):
    """Count companies and calculate their share of the loaded dataset."""
    result = data.groupby(column).size().rename("companies").reset_index()
    result = result.sort_values(["companies", column], ascending=[False, True])
    result["share_percent"] = (result["companies"] / len(data) * 100).round(1)
    return result.reset_index(drop=True)


def save_chart(summary, output_path):
    top = summary.head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(top["country"], top["companies"], color="#5965D8")
    ax.set_title("Companies by country • loaded dataset", loc="left", pad=16)
    ax.set_xlabel("Number of companies")
    ax.xaxis.get_major_locator().set_params(integer=True)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).parent / "data/sample_companies.csv")
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    try:
        data = clean_companies(pd.read_csv(args.input))
        if data.empty:
            raise ValueError("The dataset has no companies.")
        args.output.mkdir(parents=True, exist_ok=True)
        print(f"Companies analyzed: {len(data)}")
        for column in ["country", "continent"]:
            summary = summarize(data, column)
            summary.to_csv(args.output / f"companies_by_{column}.csv", index=False)
            print(f"\nCompanies by {column}:\n{summary.to_string(index=False)}")
        save_chart(summarize(data, "country"), args.output / "companies_by_country.png")
        print(f"\nResults saved to {args.output.resolve()}")
    except (ValueError, OSError, pd.errors.ParserError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
