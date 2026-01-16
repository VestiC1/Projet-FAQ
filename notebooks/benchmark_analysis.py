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
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    return BENCHMARK_RESULTS, DATA_DIR, np, pd, plt, sns


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # JC
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    df_a_jc = pd.read_csv(DATA_DIR / 'annotation_a_JC.csv', index_col=0).describe().transpose()
    df_b_jc = pd.read_csv(DATA_DIR / 'annotation_b_JC.csv', index_col=0).describe().transpose()
    df_c_jc = pd.read_csv(DATA_DIR / 'annotation_c_JC.csv', index_col=0).describe().transpose()
    return df_a_jc, df_b_jc, df_c_jc


@app.cell
def _(df_a_jc):
    df_a_jc
    return


@app.cell
def _():
    target_latency  = 2.0
    return (target_latency,)


@app.cell
def _(df_a_jc, df_b_jc, df_c_jc, df_inf_time, keys, np, pd, target_latency):
    metrics_JC = pd.concat([df_a_jc['mean'], df_b_jc['mean'], df_c_jc['mean']], axis=1, keys=keys)
    metrics_JC.loc['No Hallucination'] = 1 - metrics_JC.loc['Hallucination']
    metrics_JC.loc['Simplicité'] = 1- np.array([1, 3, 2])/3 
    metrics_JC.loc['Pertinence'] = metrics_JC.loc['Pertinence'] / 2
    metrics_JC.loc['P75'] = df_inf_time['75%'].to_numpy()
    metrics_JC.loc['Latence'] = np.clip(target_latency / metrics_JC.loc['P75'],0,  1)
    metrics_JC.drop('P75', inplace=True)
    metrics_JC.drop('Hallucination', inplace=True)
    return (metrics_JC,)


@app.cell
def _(metrics_JC):
    metrics_JC
    return


@app.cell
def _(metrics_JC, plt, radar_plot):
    df_norm_JC =  metrics_JC#(metrics_JC - metrics_JC.min()) / (metrics_JC.max() - metrics_JC.min())
    fig, ax = radar_plot(df_norm_JC)
    plt.title('Compaison JC')
    plt.show()
    return


@app.cell
def _(global_score, metrics_JC):
    gs_JC = global_score(metrics_JC).transpose()
    gs_JC.columns = ['score']
    return (gs_JC,)


@app.cell
def _(gs_JC, plt, sns):
    sns.barplot(x=gs_JC['score'], y=gs_JC.index, hue=gs_JC.index)
    plt.title('Comparaison des scores globaux (JC)')
    plt.ylabel('Stratégies')
    plt.xlabel('Score Global')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SD
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    df_a_sd = pd.read_csv(DATA_DIR / 'annotation_a_SDS.csv', index_col=0).describe().transpose()
    df_b_sd = pd.read_csv(DATA_DIR / 'annotation_b_SDS.csv', index_col=0).describe().transpose()
    df_c_sd = pd.read_csv(DATA_DIR / 'annotation_c_SDS.csv', index_col=0).describe().transpose()
    return df_a_sd, df_b_sd, df_c_sd


@app.cell
def _(df_a_sd):
    df_a_sd
    return


@app.cell
def _(df_a_sd, df_b_sd, df_c_sd, df_inf_time, keys, np, pd, target_latency):
    metrics_SD = pd.concat([df_a_sd['mean'], df_b_sd['mean'], df_c_sd['mean']], axis=1, keys=keys)
    metrics_SD.loc['No Hallucination'] = 1 - metrics_SD.loc['Hallucination']
    metrics_SD.loc['Simplicité'] = 1- np.array([1, 3, 2])/3 
    metrics_SD.loc['Pertinence'] = metrics_SD.loc['Pertinence'] / 2
    metrics_SD.loc['P75'] = df_inf_time['75%'].to_numpy()
    metrics_SD.loc['Latence'] = np.clip(target_latency / metrics_SD.loc['P75'],0,  1)
    metrics_SD.drop('P75', inplace=True)
    metrics_SD.drop('Hallucination', inplace=True)
    return (metrics_SD,)


@app.cell
def _(metrics_SD):
    metrics_SD
    return


@app.cell
def _(metrics_SD, plt, radar_plot):
    fig2, ax2 = radar_plot(metrics_SD)
    plt.title('Comparaison SDS')
    plt.show()
    return


@app.cell
def _(global_score, metrics_SD):
    gs_SD = global_score(metrics_SD).transpose()
    gs_SD.columns = ['score']
    return (gs_SD,)


@app.cell
def _(gs_SD, plt, sns):
    sns.barplot(x=gs_SD['score'], y=gs_SD.index, hue=gs_SD.index)
    plt.title('Comparaison des scores globaux (SD)')
    plt.ylabel('Stratégies')
    plt.xlabel('Score Global')
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
