from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.theory import asymptotic_bound, guaranteed_ratio


def _add_theory_lines(ax, m_value: int, n_values) -> float:
    """
    Добавляет на ось теоретические линии гарантии из статьи:
    - горизонтальную асимптоту α₁∞/m;
    - точную кривую α_mn(n) (если значения α_1q заданы в src/theory).

    Возвращает минимальное значение Y среди нарисованных линий —
    нужно для подбора нижней границы оси.
    """
    sorted_n = sorted(n_values)

    asymptote = asymptotic_bound(m_value)
    ax.axhline(
        y=asymptote,
        linestyle="--",
        color="red",
        linewidth=1.5,
        label=f"асимптота α₁∞/m ≈ {asymptote:.3f}",
    )

    y_min = asymptote

    exact_n = []
    exact_y = []
    for n in sorted_n:
        value = guaranteed_ratio(m_value, n)
        if value is not None:
            exact_n.append(n)
            exact_y.append(value)

    if exact_n:
        ax.plot(
            exact_n,
            exact_y,
            linestyle="-.",
            color="darkorange",
            linewidth=1.8,
            marker="s",
            markersize=4,
            label="теор. гарантия α_mn",
        )
        y_min = min(y_min, min(exact_y))

    return y_min


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


def plot_accuracy_spread_by_m(
    results_csv: str | Path,
    output_dir: str | Path,
    accuracy_col: str = "approximation_ratio",
    n_col: str = "n",
    m_col: str = "m",
) -> None:
    """
    Строит отдельный график для каждого m:
    по X — n,
    по Y — точность greedy-алгоритма,
    для каждого n показывается разброс значений точности.

    На графике:
    - вертикальный отрезок: min..max точности;
    - точка: среднее значение точности.
    """

    results_csv = Path(results_csv)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(results_csv)

    required_cols = {n_col, m_col, accuracy_col}
    missing_cols = required_cols - set(df.columns)

    if missing_cols:
        raise ValueError(
            f"В CSV не найдены колонки: {missing_cols}. "
            f"Доступные колонки: {list(df.columns)}"
        )

    # На всякий случай убираем строки без точности
    df = df.dropna(subset=[n_col, m_col, accuracy_col])

    # Если точность вдруг записана в процентах, например 89.4,
    # можно раскомментировать:
    # df[accuracy_col] = df[accuracy_col] / 100

    grouped = (
        df.groupby([m_col, n_col])[accuracy_col]
        .agg(["min", "max", "mean", "median", "count"])
        .reset_index()
        .sort_values([m_col, n_col])
    )

    for m_value in sorted(grouped[m_col].unique()):
        data_m = grouped[grouped[m_col] == m_value]

        x = data_m[n_col]
        y_min = data_m["min"]
        y_max = data_m["max"]
        y_mean = data_m["mean"]

        fig, ax = plt.subplots(figsize=(9, 5))

        # Вертикальные отрезки разброса min..max
        ax.vlines(
            x=x,
            ymin=y_min,
            ymax=y_max,
            linewidth=2,
            label="Разброс точности: min..max",
        )

        # Маленькие горизонтальные засечки сверху и снизу
        cap_width = 0.12

        for xi, ymin_i, ymax_i in zip(x, y_min, y_max):
            ax.hlines(
                y=ymin_i,
                xmin=xi - cap_width,
                xmax=xi + cap_width,
                linewidth=2,
            )
            ax.hlines(
                y=ymax_i,
                xmin=xi - cap_width,
                xmax=xi + cap_width,
                linewidth=2,
            )

        # Среднее значение
        ax.scatter(
            x,
            y_mean,
            s=45,
            zorder=3,
            label="Средняя точность",
        )

        theory_y_min = _add_theory_lines(ax, m_value, data_m[n_col].unique())

        ax.set_title(f"Зависимость точности greedy-алгоритма от n при m = {m_value}")
        ax.set_xlabel("n — количество переменных")
        ax.set_ylabel("Точность greedy / exact")

        ax.set_xticks(sorted(data_m[n_col].unique()))
        ax.set_ylim(max(0.0, min(theory_y_min, float(y_min.min())) - 0.05), 1.05)

        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend()

        fig.tight_layout()

        output_path = output_dir / f"accuracy_spread_m_{m_value}.png"
        fig.savefig(output_path, dpi=300)
        plt.close(fig)

    # Дополнительно сохраним таблицу с min/max/mean по каждому m и n
    grouped.to_csv(output_dir / "accuracy_spread_summary.csv", index=False)


def plot_accuracy_spread_by_m_and_profit_type(
    results_csv: str | Path,
    output_dir: str | Path,
    accuracy_col: str = "approximation_ratio",
    n_col: str = "n",
    m_col: str = "m",
    profit_col: str = "profit_type",
) -> None:
    """
    Тот же формат, что и plot_accuracy_spread_by_m (для каждого n —
    вертикальный отрезок min..max + точка среднего + теоретические
    линии), но отдельный график на каждую пару (m, profit_type).

    Это ключевой график для поиска подкласса задач: видно, что,
    например, sparse+random даёт гораздо более широкий разброс,
    чем dense+correlated.
    """
    results_csv = Path(results_csv)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(results_csv)

    required_cols = {n_col, m_col, accuracy_col, profit_col}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"В CSV не найдены колонки: {missing_cols}. "
            f"Доступные колонки: {list(df.columns)}"
        )

    df = df.dropna(subset=[n_col, m_col, accuracy_col, profit_col])

    grouped = (
        df.groupby([m_col, profit_col, n_col])[accuracy_col]
        .agg(["min", "max", "mean", "count"])
        .reset_index()
        .sort_values([m_col, profit_col, n_col])
    )

    cap_width = 0.12

    for m_value in sorted(grouped[m_col].unique()):
        data_m = grouped[grouped[m_col] == m_value]

        for profit_type in sorted(data_m[profit_col].unique()):
            data = data_m[data_m[profit_col] == profit_type]

            x = data[n_col]
            y_min = data["min"]
            y_max = data["max"]
            y_mean = data["mean"]

            fig, ax = plt.subplots(figsize=(9, 5))

            ax.vlines(
                x=x,
                ymin=y_min,
                ymax=y_max,
                linewidth=2,
                label="Разброс точности: min..max",
            )

            for xi, ymin_i, ymax_i in zip(x, y_min, y_max):
                ax.hlines(
                    y=ymin_i,
                    xmin=xi - cap_width,
                    xmax=xi + cap_width,
                    linewidth=2,
                )
                ax.hlines(
                    y=ymax_i,
                    xmin=xi - cap_width,
                    xmax=xi + cap_width,
                    linewidth=2,
                )

            ax.scatter(
                x,
                y_mean,
                s=45,
                zorder=3,
                label="Средняя точность",
            )

            theory_y_min = _add_theory_lines(
                ax, m_value, data[n_col].unique()
            )

            ax.set_title(
                f"Точность greedy от n при m = {m_value}, "
                f"profit_type = {profit_type}"
            )
            ax.set_xlabel("n — количество переменных")
            ax.set_ylabel("Точность greedy / exact")

            ax.set_xticks(sorted(data[n_col].unique()))
            ax.set_ylim(
                max(0.0, min(theory_y_min, float(y_min.min())) - 0.05),
                1.05,
            )

            ax.grid(True, linestyle="--", alpha=0.4)
            ax.legend()

            fig.tight_layout()

            output_path = (
                output_dir / f"accuracy_spread_m{m_value}_{profit_type}.png"
            )
            fig.savefig(output_path, dpi=300)
            plt.close(fig)


def plot_exact_rate_by_n(
    grouped_summary_path: str | Path,
    plots_dir: str | Path,
) -> None:
    """
    Доля экземпляров, на которых greedy совпал с оптимумом (ratio = 1),
    в зависимости от n. Отдельная линия для каждого m.

    Отвечает на вопрос «на каких задачах алгоритм точен всегда».
    """
    plots_dir = ensure_plots_directory(plots_dir)
    df = pd.read_csv(grouped_summary_path)

    if "exact_rate" not in df.columns:
        raise ValueError(
            "В grouped_summary нет колонки 'exact_rate'. "
            f"Доступные колонки: {list(df.columns)}"
        )

    grouped = (
        df.groupby(["m", "n"], as_index=False)["exact_rate"].mean()
    )

    plt.figure(figsize=(8, 5))

    for m_value in sorted(grouped["m"].unique()):
        data_m = grouped[grouped["m"] == m_value].sort_values("n")
        plt.plot(
            data_m["n"],
            data_m["exact_rate"],
            marker="o",
            label=f"m = {m_value}",
        )

    plt.xlabel("n")
    plt.ylabel("Доля точных решений (ratio = 1.0)")
    plt.title("Частота совпадения greedy с оптимумом в зависимости от n")
    plt.ylim(-0.02, 1.02)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(plots_dir / "exact_rate_by_n.png", dpi=300)
    plt.close()


def plot_worst_case_by_config(
    results_csv: str | Path,
    plots_dir: str | Path,
    worst_case_csv: str | Path,
    accuracy_col: str = "approximation_ratio",
) -> None:
    """
    Худший случай (минимальный approximation ratio) по группам
    (m, profit_type, density). Столбчатая диаграмма + CSV-таблица.

    Показывает, на каком подклассе алгоритм проседает сильнее всего.
    """
    plots_dir = ensure_plots_directory(plots_dir)
    worst_case_csv = Path(worst_case_csv)

    df = pd.read_csv(results_csv)

    required_cols = {"m", "profit_type", "density", accuracy_col}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"В CSV не найдены колонки: {missing_cols}. "
            f"Доступные колонки: {list(df.columns)}"
        )

    worst = (
        df.groupby(["m", "profit_type", "density"])[accuracy_col]
        .agg(min_ratio="min", avg_ratio="mean", count="count")
        .reset_index()
        .sort_values(["m", "profit_type", "density"])
    )

    worst.to_csv(worst_case_csv, index=False)

    worst["label"] = (
        worst["profit_type"].astype(str)
        + "/"
        + worst["density"].astype(str)
    )

    m_values = sorted(worst["m"].unique())
    fig, axes = plt.subplots(
        len(m_values),
        1,
        figsize=(11, 4 * len(m_values)),
        squeeze=False,
    )

    for ax, m_value in zip(axes[:, 0], m_values):
        data_m = worst[worst["m"] == m_value]
        ax.bar(data_m["label"], data_m["min_ratio"])
        ax.set_title(f"Минимальный ratio по конфигурациям при m = {m_value}")
        ax.set_xlabel("profit_type / density")
        ax.set_ylabel("min approximation ratio")
        ax.set_ylim(0, 1.05)
        ax.grid(True, axis="y", linestyle="--", alpha=0.4)
        ax.tick_params(axis="x", rotation=30)

    fig.tight_layout()
    fig.savefig(plots_dir / "worst_case_by_config.png", dpi=300)
    plt.close(fig)