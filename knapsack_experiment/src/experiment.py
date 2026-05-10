import random
from dataclasses import dataclass, asdict
from typing import Any

from src.exact import solve_exact_dp
from src.generator import generate_instance
from src.greedy import solve_greedy
from src.metrics import (
    approximation_ratio,
    is_solution_consistent,
    is_solution_feasible,
    profit_gap,
    relative_profit_gap,
)


@dataclass
class ExperimentConfig:
    """
    Конфигурация одной серии экспериментов.
    Все экземпляры в серии генерируются с одинаковыми параметрами.
    """
    n: int
    m: int
    density: str
    profit_type: str
    alpha: float
    num_instances: int
    min_weight: int = 1
    max_weight: int = 20
    min_profit: int = 1
    max_profit: int = 100
    sparse_zero_prob: float = 0.5
    noise_level: int = 5
    random_seed: int | None = None


@dataclass
class ExperimentResult:
    """
    Результат одного запуска на одном экземпляре задачи.
    """
    instance_id: int
    n: int
    m: int
    density: str
    profit_type: str
    alpha: float

    greedy_profit: int
    exact_profit: int

    approximation_ratio: float
    profit_gap: int
    relative_profit_gap: float

    greedy_feasible: bool
    exact_feasible: bool

    greedy_consistent: bool
    exact_consistent: bool


def run_single_experiment(
    config: ExperimentConfig,
    instance_id: int,
) -> ExperimentResult:
    """
    Генерирует один экземпляр задачи, решает его двумя алгоритмами
    и возвращает все основные метрики.
    """
    instance = generate_instance(
        n=config.n,
        m=config.m,
        density=config.density,
        profit_type=config.profit_type,
        alpha=config.alpha,
        min_weight=config.min_weight,
        max_weight=config.max_weight,
        min_profit=config.min_profit,
        max_profit=config.max_profit,
        sparse_zero_prob=config.sparse_zero_prob,
        noise_level=config.noise_level,
    )

    greedy_solution = solve_greedy(instance)
    exact_solution = solve_exact_dp(instance)

    result = ExperimentResult(
        instance_id=instance_id,
        n=config.n,
        m=config.m,
        density=config.density,
        profit_type=config.profit_type,
        alpha=config.alpha,

        greedy_profit=greedy_solution.total_profit,
        exact_profit=exact_solution.total_profit,

        approximation_ratio=approximation_ratio(greedy_solution, exact_solution),
        profit_gap=profit_gap(greedy_solution, exact_solution),
        relative_profit_gap=relative_profit_gap(greedy_solution, exact_solution),

        greedy_feasible=is_solution_feasible(instance, greedy_solution),
        exact_feasible=is_solution_feasible(instance, exact_solution),

        greedy_consistent=is_solution_consistent(instance, greedy_solution),
        exact_consistent=is_solution_consistent(instance, exact_solution),
    )

    return result


def run_experiment_series(config: ExperimentConfig) -> list[ExperimentResult]:
    """
    Запускает серию экспериментов с одинаковыми параметрами.
    Отличаются только случайно сгенерированные экземпляры задачи.
    """
    if config.num_instances <= 0:
        raise ValueError("num_instances должно быть положительным")

    if config.random_seed is not None:
        random.seed(config.random_seed)

    results = []

    for instance_id in range(1, config.num_instances + 1):
        result = run_single_experiment(config, instance_id)
        results.append(result)

    return results


def summarize_results(results: list[ExperimentResult]) -> dict[str, Any]:
    """
    Считает общие сводные статистики по всем результатам сразу.
    """
    if not results:
        raise ValueError("Список results пуст")

    ratios = [r.approximation_ratio for r in results]
    gaps = [r.profit_gap for r in results]
    relative_gaps = [r.relative_profit_gap for r in results]

    greedy_feasible_count = sum(1 for r in results if r.greedy_feasible)
    exact_feasible_count = sum(1 for r in results if r.exact_feasible)

    greedy_consistent_count = sum(1 for r in results if r.greedy_consistent)
    exact_consistent_count = sum(1 for r in results if r.exact_consistent)

    summary = {
        "num_results": len(results),

        "avg_ratio": sum(ratios) / len(ratios),
        "min_ratio": min(ratios),
        "max_ratio": max(ratios),

        "avg_profit_gap": sum(gaps) / len(gaps),
        "min_profit_gap": min(gaps),
        "max_profit_gap": max(gaps),

        "avg_relative_profit_gap": sum(relative_gaps) / len(relative_gaps),
        "min_relative_profit_gap": min(relative_gaps),
        "max_relative_profit_gap": max(relative_gaps),

        "greedy_feasible_count": greedy_feasible_count,
        "exact_feasible_count": exact_feasible_count,

        "greedy_consistent_count": greedy_consistent_count,
        "exact_consistent_count": exact_consistent_count,
    }

    return summary


def summarize_results_by_configuration(
    results: list[ExperimentResult],
) -> list[dict[str, Any]]:
    """
    Строит сводку по конфигурациям эксперимента.

    Одна конфигурация определяется полями:
    n, m, density, profit_type, alpha
    """
    if not results:
        raise ValueError("Список results пуст")

    grouped: dict[tuple, list[ExperimentResult]] = {}

    for result in results:
        key = (
            result.n,
            result.m,
            result.density,
            result.profit_type,
            result.alpha,
        )

        if key not in grouped:
            grouped[key] = []

        grouped[key].append(result)

    summary_rows = []

    for key, group in grouped.items():
        n, m, density, profit_type, alpha = key

        ratios = [r.approximation_ratio for r in group]
        gaps = [r.profit_gap for r in group]
        relative_gaps = [r.relative_profit_gap for r in group]

        summary_row = {
            "n": n,
            "m": m,
            "density": density,
            "profit_type": profit_type,
            "alpha": alpha,
            "num_instances": len(group),

            "avg_ratio": sum(ratios) / len(ratios),
            "min_ratio": min(ratios),
            "max_ratio": max(ratios),

            "avg_profit_gap": sum(gaps) / len(gaps),
            "min_profit_gap": min(gaps),
            "max_profit_gap": max(gaps),

            "avg_relative_profit_gap": sum(relative_gaps) / len(relative_gaps),
            "min_relative_profit_gap": min(relative_gaps),
            "max_relative_profit_gap": max(relative_gaps),

            "greedy_feasible_count": sum(1 for r in group if r.greedy_feasible),
            "exact_feasible_count": sum(1 for r in group if r.exact_feasible),

            "greedy_consistent_count": sum(1 for r in group if r.greedy_consistent),
            "exact_consistent_count": sum(1 for r in group if r.exact_consistent),
        }

        summary_rows.append(summary_row)

    summary_rows.sort(
        key=lambda row: (
            row["n"],
            row["m"],
            row["density"],
            row["profit_type"],
            row["alpha"],
        )
    )

    return summary_rows


def results_to_dicts(results: list[ExperimentResult]) -> list[dict[str, Any]]:
    """
    Преобразует список dataclass-результатов в список словарей.
    Полезно для сохранения в CSV или DataFrame позже.
    """
    return [asdict(result) for result in results]