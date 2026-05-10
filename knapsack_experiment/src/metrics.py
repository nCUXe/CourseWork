from src.models import KnapsackInstance, KnapsackSolution


def compute_used_resources(
    instance: KnapsackInstance,
    solution: KnapsackSolution,
) -> list[int]:
    """
    Пересчитывает фактический расход ресурсов по вектору количеств x.
    """
    return [
        sum(instance.A[j][i] * solution.x[i] for i in range(instance.n))
        for j in range(instance.m)
    ]


def compute_total_profit(
    instance: KnapsackInstance,
    solution: KnapsackSolution,
) -> int:
    """
    Пересчитывает фактическую суммарную прибыль по вектору количеств x.
    """
    return sum(instance.c[i] * solution.x[i] for i in range(instance.n))


def is_solution_feasible(
    instance: KnapsackInstance,
    solution: KnapsackSolution,
) -> bool:
    """
    Проверяет, удовлетворяет ли решение ограничениям задачи.
    """
    used_resources = compute_used_resources(instance, solution)

    for j in range(instance.m):
        if used_resources[j] > instance.b[j]:
            return False

    return True


def is_solution_consistent(
    instance: KnapsackInstance,
    solution: KnapsackSolution,
) -> bool:
    """
    Проверяет согласованность сохранённых в решении полей:
    - совпадает ли total_profit с фактическим
    - совпадает ли used_resources с фактическими
    """
    actual_profit = compute_total_profit(instance, solution)
    actual_used_resources = compute_used_resources(instance, solution)

    if solution.total_profit != actual_profit:
        return False

    if solution.used_resources != actual_used_resources:
        return False

    return True


def approximation_ratio(
    algorithm_solution: KnapsackSolution,
    optimal_solution: KnapsackSolution,
) -> float:
    """
    Вычисляет отношение качества решения:
        f(ALG) / f(OPT)

    Предполагается, что optimal_solution - точное оптимальное решение.
    """
    opt_profit = optimal_solution.total_profit
    alg_profit = algorithm_solution.total_profit

    if opt_profit < 0:
        raise ValueError("Прибыль оптимального решения не может быть отрицательной")

    if alg_profit < 0:
        raise ValueError("Прибыль алгоритмического решения не может быть отрицательной")

    if opt_profit == 0:
        return 1.0

    return alg_profit / opt_profit


def profit_gap(
    algorithm_solution: KnapsackSolution,
    optimal_solution: KnapsackSolution,
) -> int:
    """
    Абсолютное отставание от оптимума:
        f(OPT) - f(ALG)
    """
    return optimal_solution.total_profit - algorithm_solution.total_profit


def relative_profit_gap(
    algorithm_solution: KnapsackSolution,
    optimal_solution: KnapsackSolution,
) -> float:
    """
    Относительное отставание от оптимума:
        (f(OPT) - f(ALG)) / f(OPT)
    """
    opt_profit = optimal_solution.total_profit
    gap = profit_gap(algorithm_solution, optimal_solution)

    if opt_profit == 0:
        return 0.0

    return gap / opt_profit