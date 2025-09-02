# feature_plots.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# ---------- helpers ----------
def summarize_features_cat(df, feature, y_col, y_pred_col=None, levels=None, sort_levels=True):
    if levels is None:
        levels = df[feature].dropna().unique()
        if sort_levels:
            try:
                levels = sorted(levels, key=float)  # numeric-like categories
            except Exception:
                levels = sorted(levels)             # strings

    counts = df[feature].value_counts().reindex(levels, fill_value=0)
    obs = df.groupby(feature, observed=True)[y_col].mean().reindex(levels, fill_value=0.0)

    pred = None
    if y_pred_col and y_pred_col in df.columns:
        pred = df.groupby(feature, observed=True)[y_pred_col].mean().reindex(levels, fill_value=0.0)

    x_pos = levels
    bar_widths = None
    return counts, obs, pred, x_pos, bar_widths

def _interval_mids_and_widths(interval_index):
    left = np.array([iv.left for iv in interval_index], dtype=float)
    right = np.array([iv.right for iv in interval_index], dtype=float)
    mids = (left + right) / 2.0
    widths = right - left
    return mids, widths

def summarize_features_quant(df, feature, y_col, y_pred_col=None, bin_method="qcut", n_bins=10):
    series = df[feature].astype(float)
    if bin_method == "qcut":
        binned = pd.qcut(series, q=n_bins, duplicates='drop')
    else:
        binned = pd.cut(series, bins=n_bins, include_lowest=True)

    counts = binned.value_counts().sort_index()
    obs = df.groupby(binned, observed=True)[y_col].mean()

    pred = None
    if y_pred_col and y_pred_col in df.columns:
        pred = df.groupby(binned, observed=True)[y_pred_col].mean()

    x_pos, widths = _interval_mids_and_widths(counts.index)
    if widths.min() <= 0:
        m = np.median(widths[widths > 0])
        widths[widths <= 0] = m

    obs = obs.reindex(counts.index)
    if pred is not None:
        pred = pred.reindex(counts.index)

    return counts, obs, pred, x_pos, widths

def _plot_left(ax, x_pos, counts, obs, pred=None, feature="", bar_widths=None, y_col="y"):
    if bar_widths is None:
        ax.bar(x_pos, counts.values)
    else:
        ax.bar(x_pos, counts.values, width=bar_widths)

    ax.set_xlabel(feature)
    ax.set_ylabel('# of observations')
    ax.tick_params(axis='x', labelrotation=90)
    ax.set_title(f'{feature} vs. Percent {y_col}=1')

    ax_line = ax.twinx()
    ax_line.set_ylabel(f'Percent {y_col}=1')
    ax_line.set_ylim(0, 1)
    ax_line.yaxis.set_major_formatter(PercentFormatter(1.0))

    handles = []
    for series, label in [(obs, 'Observed'), (pred, 'Predicted')]:
        if series is None: 
            continue
        (ln,) = ax_line.plot(x_pos, series.values, marker='o', label=label, color = 'red')
        handles.append(ln)
    if handles:
        ax_line.legend(handles=handles, loc='upper left')

def _plot_boxplot(ax, df, feature, y_col):
    try:
        import seaborn as sns
        sns.boxplot(x=y_col, y=feature, data=df, ax=ax)
        ax.set_title(f'Distribution of {feature} by {y_col}')
    except Exception:
        ax.set_title("Boxplot requires seaborn; install seaborn or skip this.")

# ---------- main wrappers ----------
def plot_feature_vs_y(
    df, feature, y_col="y", y_pred_col=None,
    dtype="auto",                # "cat", "quant", or "auto"
    bin_method="qcut", n_bins=10,
    levels=None, sort_levels=True,
    show_boxplot=True, figsize=(10, 4)
):
    """
    Plot count bars + percent Y=1 (and optional predicted %).
    dtype:
      - "auto": numeric with many uniques -> "quant" else "cat"
      - "cat": treat as categorical
      - "quant": bin as continuous
    """
    series = df[feature]
    if dtype == "auto":
        if pd.api.types.is_numeric_dtype(series) and series.nunique() > 15:
            dtype_eff = "quant"
        else:
            dtype_eff = "cat"
    else:
        dtype_eff = dtype

    if dtype_eff == "cat":
        counts, obs, pred, x_pos, bar_widths = summarize_features_cat(
            df, feature, y_col, y_pred_col=y_pred_col, levels=levels, sort_levels=sort_levels
        )
    else:
        counts, obs, pred, x_pos, bar_widths = summarize_features_quant(
            df, feature, y_col, y_pred_col=y_pred_col, bin_method=bin_method, n_bins=n_bins
        )

    if show_boxplot:
        fig, (ax_left, ax_right) = plt.subplots(ncols=2, figsize=figsize)
    else:
        fig, ax_left = plt.subplots(figsize=(figsize[0]*0.65, figsize[1]))
        ax_right = None

    _plot_left(ax_left, x_pos, counts, obs, pred=pred, feature=feature, bar_widths=bar_widths, y_col=y_col)

    if show_boxplot and ax_right is not None:
        _plot_boxplot(ax_right, df, feature, y_col)

    plt.tight_layout()
    plt.show()

def plot_features_vs_y_grid(
    df, features, y_col="y", y_pred_col=None,
    dtype="auto",                # or dict per feature: {"age":"quant", "job":"cat"}
    bin_method="qcut", n_bins=10,
    levels_map=None,             # dict: {feature: [custom order]}
    sort_levels=True,
    cols=3, figsize_per=(4,3),
):
    import math
    dtype_is_dict = isinstance(dtype, dict)

    n = len(features)
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(figsize_per[0]*cols, figsize_per[1]*rows))
    if rows == 1 and cols == 1:
        axes = np.array([[axes]])
    elif rows == 1:
        axes = np.array([axes])
    elif cols == 1:
        axes = axes.reshape(-1, 1)

    k = 0
    for r in range(rows):
        for c in range(cols):
            ax = axes[r, c]
            if k >= n:
                ax.axis("off")
                continue

            feature = features[k]
            series = df[feature]
            dtype_eff = (dtype[feature] if dtype_is_dict else dtype)
            if dtype_eff == "auto":
                if pd.api.types.is_numeric_dtype(series) and series.nunique() > 15:
                    dtype_eff = "quant"
                else:
                    dtype_eff = "cat"

            levels = None
            if levels_map and feature in levels_map:
                levels = levels_map[feature]

            if dtype_eff == "cat":
                counts, obs, pred, x_pos, bar_widths = summarize_features_cat(
                    df, feature, y_col, y_pred_col=y_pred_col, levels=levels, sort_levels=sort_levels
                )
            else:
                counts, obs, pred, x_pos, bar_widths = summarize_features_quant(
                    df, feature, y_col, y_pred_col=y_pred_col, bin_method=bin_method, n_bins=n_bins
                )

            _plot_left(ax, x_pos, counts, obs, pred=pred, feature=feature, bar_widths=bar_widths, y_col=y_col)
            k += 1

    plt.tight_layout()
    plt.show()

