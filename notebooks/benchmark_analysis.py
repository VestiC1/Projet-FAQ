import marimo

__generated_with = "0.19.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    from pathlib import Path

    ROOT = Path(__file__).parent.parent

    sys.path.insert(0, str(ROOT))
    return


@app.cell
def _():
    from config import BENACHLMARK_RESULTS
    import pandas as pd
    return BENACHLMARK_RESULTS, pd


@app.cell
def _(BENACHLMARK_RESULTS, pd):
    df = pd.read_parquet(BENACHLMARK_RESULTS)
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
