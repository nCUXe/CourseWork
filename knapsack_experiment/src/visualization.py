from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def ensure_plots_directory(plots_dir: str | Path) -> Path:
    """
    Создаёт папку для графиков, если её нет.
    """
    plots_path = Path(plots_dir)
    plots_path.mkdir(parents=True, exist_ok=True)
    return plots_path


def load_grouped_summary(csv_path: str | Path) -> pd.DataFrame:
    """
    Загружает grouped_summary.csv в DataFrame.
    """
    return pd.read_csv(csv_path)


def plot_avg_ratio_by_n(
    df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    Базовый график: средний approximation ratio от n.
    Усреднение идёт по всем остальным параметрам.
    """
    grouped = df.groupby("n", as_index=False)["avg_ratio"].mean()

    plt.figure(figsize=(8, 5))
    plt.plot(grouped["n"], grouped["avg_ratio"], marker="o")
    plt.xlabel("n")
    plt.ylabel("Среднее approximation ratio")
    plt.title("Зависимость среднего approximation ratio от числа предметов n")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_avg_ratio_by_m(
    df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    Базовый график: средний approximation ratio от m.
    Усреднение идёт по всем остальным параметрам.
    """
    grouped = df.groupby("m", as_index=False)["avg_ratio"].mean()

    plt.figure(figsize=(8, 5))
    plt.plot(grouped["m"], grouped["avg_ratio"], marker="o")
    plt.xlabel("m")
    plt.ylabel("Среднее approximation ratio")
    plt.title("Зависимость среднего approximation ratio от числа ограничений m")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_avg_ratio_by_profit_type(
    df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    Базовая столбчатая диаграмма по типу прибыли.
    """
    grouped = df.groupby("profit_type", as_index=False)["avg_ratio"].mean()

    plt.figure(figsize=(8, 5))
    plt.bar(grouped["profit_type"], grouped["avg_ratio"])
    plt.xlabel("Тип прибыли")
    plt.ylabel("Среднее approximation ratio")
    plt.title("Среднее approximation ratio для разных типов прибыли")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_avg_ratio_by_n_for_density(
    df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    График avg_ratio от n отдельно для dense и sparse.
    """
    grouped = (
        df.groupby(["n", "density"], as_index=False)["avg_ratio"]
        .mean()
    )

    plt.figure(figsize=(8, 5))

    for density in sorted(grouped["density"].unique()):
        density_data = grouped[grouped["density"] == density]
        plt.plot(
            density_data["n"],
            density_data["avg_ratio"],
            marker="o",
            label=density,
        )

    plt.xlabel("n")
    plt.ylabel("Среднее approximation ratio")
    plt.title("avg_ratio от n для разных плотностей матрицы")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_avg_ratio_by_n_for_profit_type(
    df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    График avg_ratio от n отдельно для каждого profit_type.
    """
    grouped = (
        df.groupby(["n", "profit_type"], as_index=False)["avg_ratio"]
        .mean()
    )

    plt.figure(figsize=(8, 5))

    for profit_type in sorted(grouped["profit_type"].unique()):
        profit_data = grouped[grouped["profit_type"] == profit_type]
        plt.plot(
            profit_data["n"],
            profit_data["avg_ratio"],
            marker="o",
            label=profit_type,
        )

    plt.xlabel("n")
    plt.ylabel("Среднее approximation ratio")
    plt.title("avg_ratio от n для разных типов прибыли")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_avg_ratio_by_alpha(
    df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    График среднего approximation ratio от alpha.
    """
    grouped = df.groupby("alpha", as_index=False)["avg_ratio"].mean()

    plt.figure(figsize=(8, 5))
    plt.plot(grouped["alpha"], grouped["avg_ratio"], marker="o")
    plt.xlabel("alpha")
    plt.ylabel("Среднее approximation ratio")
    plt.title("Зависимость среднего approximation ratio от alpha")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_avg_ratio_by_m_for_profit_type(
    df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    График avg_ratio от m отдельно для каждого profit_type.
    """
    grouped = (
        df.groupby(["m", "profit_type"], as_index=False)["avg_ratio"]
        .mean()
    )

    plt.figure(figsize=(8, 5))

    for profit_type in sorted(grouped["profit_type"].unique()):
        profit_data = grouped[grouped["profit_type"] == profit_type]
        plt.plot(
            profit_data["m"],
            profit_data["avg_ratio"],
            marker="o",
            label=profit_type,
        )

    plt.xlabel("m")
    plt.ylabel("Среднее approximation ratio")
    plt.title("avg_ratio от m для разных типов прибыли")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_avg_profit_gap_by_n(
    df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    График среднего абсолютного отставания от оптимума по n.
    """
    grouped = df.groupby("n", as_index=False)["avg_profit_gap"].mean()

    plt.figure(figsize=(8, 5))
    plt.plot(grouped["n"], grouped["avg_profit_gap"], marker="o")
    plt.xlabel("n")
    plt.ylabel("Средний profit gap")
    plt.title("Зависимость среднего profit gap от числа предметов n")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def build_all_basic_plots(
    grouped_summary_path: str | Path,
    plots_dir: str | Path,
) -> None:
    """
    Строит базовый набор графиков.
    """
    plots_dir = ensure_plots_directory(plots_dir)
    df = load_grouped_summary(grouped_summary_path)

    plot_avg_ratio_by_n(
        df,
        plots_dir / "avg_ratio_by_n.png",
    )
    plot_avg_ratio_by_m(
        df,
        plots_dir / "avg_ratio_by_m.png",
    )
    plot_avg_ratio_by_profit_type(
        df,
        plots_dir / "avg_ratio_by_profit_type.png",
    )


def build_all_extended_plots(
    grouped_summary_path: str | Path,
    plots_dir: str | Path,
) -> None:
    """
    Строит расширенный набор графиков по grouped_summary.csv.
    """
    plots_dir = ensure_plots_directory(plots_dir)
    df = load_grouped_summary(grouped_summary_path)

    # Базовые
    plot_avg_ratio_by_n(
        df,
        plots_dir / "avg_ratio_by_n.png",
    )
    plot_avg_ratio_by_m(
        df,
        plots_dir / "avg_ratio_by_m.png",
    )
    plot_avg_ratio_by_profit_type(
        df,
        plots_dir / "avg_ratio_by_profit_type.png",
    )

    # Расширенные
    plot_avg_ratio_by_n_for_density(
        df,
        plots_dir / "avg_ratio_by_n_for_density.png",
    )
    plot_avg_ratio_by_n_for_profit_type(
        df,
        plots_dir / "avg_ratio_by_n_for_profit_type.png",
    )
    plot_avg_ratio_by_alpha(
        df,
        plots_dir / "avg_ratio_by_alpha.png",
    )
    plot_avg_ratio_by_m_for_profit_type(
        df,
        plots_dir / "avg_ratio_by_m_for_profit_type.png",
    )
    plot_avg_profit_gap_by_n(
        df,
        plots_dir / "avg_profit_gap_by_n.png",
    )