import marimo

__generated_with = "0.19.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    from pathlib import Path
    import marimo as mo
    ROOT = Path(__file__).parent.parent

    sys.path.insert(0, str(ROOT))
    return (mo,)


@app.cell
def _():
    from config import BENCHMARK_RESULTS, DATA_DIR
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    return BENCHMARK_RESULTS, pd


@app.cell
def _(BENCHMARK_RESULTS, pd):
    df = pd.read_parquet(BENCHMARK_RESULTS)
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _(mo, pd):
    def make_table(df, strategy):
        cols = ['Exactitude', 'Pertinence', 'Hallucination']

        rows = []
        editables = {col: [] for col in cols}

        for i in range(len(df)):
            inputs = {col: mo.ui.text(placeholder=col) for col in cols}
            for col in cols:
                editables[col].append(inputs[col])

            row = mo.hstack([
                mo.vstack([
                    mo.md(f"**Question:** {df['question'].iloc[i]}"),
                    mo.md(f"**Expected:** {df['expected_answer_summary'].iloc[i]}"),
                    mo.md(f"**Generated:** {df[f'Strategy_{strategy}'].iloc[i]}"),
                    mo.md(f"**Référence:** {df[f'faq_id_reference'].iloc[i]}"),
                    mo.md(f"**Keywords:** {df[f'expected_keywords'].iloc[i]}"),
                ]),
                mo.vstack([mo.md(f"**{col}:**"), inputs[col]] for col in cols),
            ])
            rows.append(row)
            rows.append(mo.md("---"))  # horizontal line separator

        display = mo.vstack(rows)

        def get_data():
            return pd.DataFrame({
                "question": df["question"],
                **{col: [inp.value for inp in editables[col]] for col in cols},
            })

        return display, get_data
    return (make_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stratégie A
    """)
    return


@app.cell
def _(df, make_table):
    table_a, get_data_a = make_table(df, 'A')
    table_a
    return (get_data_a,)


@app.cell
def _(get_data_a):
    df_a = get_data_a()
    df_a
    return


@app.cell
def _():

    # df_a.to_csv(DATA_DIR / "annotation_a.csv")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stratégie B
    """)
    return


@app.cell
def _(df, make_table):
    table_b, get_data_b = make_table(df, 'B')
    table_b
    return (get_data_b,)


@app.cell
def _(get_data_b):
    df_b = get_data_b()
    df_b
    return


@app.cell
def _():

    # df_b.to_csv(DATA_DIR / "annotation_b.csv")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stratégie C
    """)
    return


@app.cell
def _(df, make_table):
    table_c, get_data_c = make_table(df, 'C')
    table_c
    return (get_data_c,)


@app.cell
def _(get_data_c):
    df_c = get_data_c()
    df_c
    return


@app.cell
def _():
    #df_c.to_csv(DATA_DIR / "annotation_c.csv")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
