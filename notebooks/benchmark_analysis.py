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
    from config import BENCHMARK_RESULTS
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    return BENCHMARK_RESULTS, pd, plt, sns


@app.cell
def _(BENCHMARK_RESULTS, pd):
    df = pd.read_parquet(BENCHMARK_RESULTS)
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _(df):
    df_inf_time = df.describe().transpose()
    df_inf_time
    return (df_inf_time,)


@app.cell
def _(df_inf_time, plt):

    plt.pie(df_inf_time['mean'], labels=df_inf_time.index, autopct='%1.1f%%')
    plt.title('Temps Inférence moyen')
    plt.show()
    return


@app.cell
def _(df_inf_time, plt):

    plt.pie(df_inf_time['std'], labels=df_inf_time.index, autopct='%1.1f%%')
    plt.title('Std. Temps Inférence')
    plt.show()
    return


@app.cell
def _(df_inf_time, plt):
    plt.pie(df_inf_time['50%'], labels=df_inf_time.index, autopct='%1.1f%%')
    plt.title('Temps Inférence médian')
    plt.show()
    return


@app.cell
def _():
    keys =  ['A', 'B', 'C']
    return (keys,)


@app.cell
def _(df, keys, plt, sns):
    for s in keys:
        sns.histplot(data=df, x=f'Strategy_{s}_time', binwidth=0.5, label=f"Strategie {s}")

    plt.xlabel("Temps d'inférence (s)")
    plt.legend()
    return


@app.cell
def _(df_inf_time, mo):
    table = mo.ui.table(df_inf_time)
    return (table,)


@app.cell
def _(table):
    table
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


@app.cell
def _(df, make_table):
    table_a, get_data_a = make_table(df, 'A')
    table_a
    return (get_data_a,)


@app.cell
def _(get_data_a):
    get_data_a()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
