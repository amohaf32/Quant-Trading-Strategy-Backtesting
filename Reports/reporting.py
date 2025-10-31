import os
from typing import Optional, Dict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

try:
    from Backtester.metrics import PerformanceMetrics
except ModuleNotFoundError:
    # Allow running this file directly by adding the project root to sys.path
    import sys
    from pathlib import Path
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.append(str(project_root))
    from Backtester.metrics import PerformanceMetrics


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def plot_equity_curve(results_df: pd.DataFrame, title: str = "Portfolio Equity Curve", save_path: Optional[str] = None):
    if 'TotalValue' not in results_df.columns:
        raise ValueError("results_df must include 'TotalValue' column")

    plt.figure(figsize=(12, 5))
    sns.lineplot(x=results_df.index, y=results_df['TotalValue'])
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Total Value")
    plt.tight_layout()

    if save_path:
        _ensure_dir(os.path.dirname(save_path))
        plt.savefig(save_path, dpi=150)

    return plt.gcf()


def plot_drawdown(results_df: pd.DataFrame, title: str = "Drawdown", save_path: Optional[str] = None):
    if 'TotalValue' not in results_df.columns:
        raise ValueError("results_df must include 'TotalValue' column")

    pm = PerformanceMetrics(results_df)
    dd = pm.max_drawdown()

    plt.figure(figsize=(12, 3.5))
    sns.lineplot(x=dd.index, y=dd.values, color='crimson')
    plt.fill_between(dd.index, dd.values, 0, color='crimson', alpha=0.2)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.tight_layout()

    if save_path:
        _ensure_dir(os.path.dirname(save_path))
        plt.savefig(save_path, dpi=150)

    return plt.gcf()


def export_performance_summary(results_df: pd.DataFrame, save_csv_path: Optional[str] = None) -> pd.DataFrame:
    pm = PerformanceMetrics(results_df)
    metrics: Dict[str, float] = pm.compute_all_metrics()
    df = pd.DataFrame([{k: v for k, v in metrics.items()}])

    # Nicely format percentage-like fields
    if 'Total Return' in df.columns:
        df['Total Return'] = (df['Total Return'] * 100).map(lambda x: f"{x:.2f}%")
    if 'Volatility (Annualized)' in df.columns:
        df['Volatility (Annualized)'] = (df['Volatility (Annualized)'] * 100).map(lambda x: f"{x:.2f}%")
    if 'Max Drawdown' in df.columns:
        df['Max Drawdown'] = (df['Max Drawdown'] * 100).map(lambda x: f"{x:.2f}%")

    if save_csv_path:
        _ensure_dir(os.path.dirname(save_csv_path))
        df.to_csv(save_csv_path, index=False)

    return df


def save_trade_log(trade_log_df: pd.DataFrame, save_csv_path: str) -> None:
    _ensure_dir(os.path.dirname(save_csv_path))
    trade_log_df.to_csv(save_csv_path, index=False)


