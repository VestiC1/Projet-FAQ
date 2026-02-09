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
    from config import BENCHMARK_RESULTS, RAGAS_METRICS
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    return BENCHMARK_RESULTS, RAGAS_METRICS, np, pd, plt, sns


@app.cell
def _():
    hash = {'Strategy_A': {'faithfulness': 0.2900, 'answer_relevancy': 0.5768, 'answer_correctness': 0.2228},
     'Strategy_B': {'faithfulness': 0.9679, 'answer_relevancy': 0.5270, 'answer_correctness': 0.5710},
     'Strategy_C': {'faithfulness': 0.6722, 'answer_relevancy': 0.2336, 'answer_correctness': 0.2958}}
    return


@app.cell
def _(BENCHMARK_RESULTS, RAGAS_METRICS, pd):
    df = pd.read_parquet(BENCHMARK_RESULTS)
    df_f = pd.read_parquet(RAGAS_METRICS)
    #df_f = pd.DataFrame.from_dict(hash, orient='index')
    return df, df_f


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Complexité


    Stratégie	Facilité de maintenance
    A	1 (très facile)
    B	2 (moyenne)
    C	3 (plus difficile)
    A (1) : Un seul prompt à modifier, pas de dépendances externes.

    B (2) : Vector store à maintenir + documents à réindexer si màj, mais un seul modèle à gérer.

    C (3) : Deux modèles distincts à maintenir/mettre à jour + synchronisation entre les deux étapes + debugging plus complexe si erreur (quel modèle a échoué ?).
    """)
    return


@app.cell
def _(df_f, np):
    df_f['complexité'] = np.array([3, 2, 1]) / 3.0
    return


@app.cell
def _(df_f):
    df_f
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Latence
    """)
    return


@app.cell
def _(df):
    df_inf_time = df.describe().transpose()
    df_inf_time
    return (df_inf_time,)


@app.cell
def _():
    target_latency  = 2.0
    return (target_latency,)


@app.cell
def _(df_f, df_inf_time, np, target_latency):
    df_f['Latence'] = np.clip(target_latency / df_inf_time['75%'].to_numpy(),0,  1)
    return


@app.cell
def _(df_f):
    df_f
    return


@app.cell
def _(df_f):
    df_f.columns = ['No Hallucination', 'Pertinence', 'Exactitude', 'Simplicité', 'Latence']
    return


@app.cell
def _(np, pd):
    def global_score(df):
        df_weight = {
            'Exactitude' : 0.3,
            'Pertinence' : 0.2,
            'No Hallucination' : 0.2, 
            'Simplicité' : 0.15,
            'Latence' : 0.15,
        }
        df_gs = pd.DataFrame({
            strategy : [] for strategy in df.columns
        })

        for s in df.columns:
            df_gs.loc[0, s] = np.sum([ df_weight[k] * df.loc[k, s]for k in df_weight.keys()])

        return df_gs
    return (global_score,)


@app.cell
def _(df_f, global_score):
    df_gs = global_score(df_f.transpose()).transpose()
    df_gs.columns = ['score']
    df_gs.index = df_gs.index.str.split('_').str[-1]
    df_gs
    return (df_gs,)


@app.cell
def _(df_gs, plt, sns):
    sns.barplot(x=df_gs['score'], y=df_gs.index, hue=df_gs.index)
    plt.title('Comparaison des scores globaux')
    plt.ylabel('Stratégies')
    plt.xlabel('Score Global')
    return


@app.cell
def _(np, plt):
    def radar_plot(df):
        metrics = df.index.tolist()
        strategies = df.columns.tolist()

        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(subplot_kw=dict(polar=True))

        for strategy in strategies:
            values = df[strategy].tolist()
            values += values[:1]
            ax.plot(angles, values, label=strategy)
            ax.fill(angles, values, alpha=0.1)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics)

        # Move radial labels (0.2, 0.4, etc.) to avoid overlap
        ax.set_rlabel_position(30)

        # Add padding to metric labels
        ax.tick_params(axis='x', pad=15)

        # Start from top instead of right
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

        plt.tight_layout()
        return fig, ax
    return (radar_plot,)


@app.cell
def _(df_f, plt, radar_plot):
    fig, ax = radar_plot(df_f.transpose())
    plt.title('Métriques')
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
