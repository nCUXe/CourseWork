from src.models import KnapsackInstance, KnapsackSolution


def solve_greedy(instance: KnapsackInstance) -> KnapsackSolution:
    """
    Приближённый алгоритм из статьи Чиркова–Золотых.

    Для каждого предмета j вычисляет точку v_j из L(A, b):
        u_j     = min_{i: A[i][j] > 0} floor(b[i] / A[i][j])
        value_j = c[j] * u_j

    Возвращает решение v_{j*}, где j* = argmax_j(value_j):
    берём u_{j*} единиц предмета j*, все остальные предметы — 0.

    Сложность: O(n * m).
    """
    instance.validate()

    best_j = -1
    best_value = -1
    best_count = 0

    for j in range(instance.n):
        u_j = instance.max_count_for_item(j)
        value_j = instance.c[j] * u_j
        if value_j > best_value:
            best_value = value_j
            best_j = j
            best_count = u_j

    x = [0] * instance.n
    if best_j >= 0:
        x[best_j] = best_count

    total_profit = sum(instance.c[j] * x[j] for j in range(instance.n))
    used_resources = [
        sum(instance.A[i][j] * x[j] for j in range(instance.n))
        for i in range(instance.m)
    ]
    is_feasible = all(used_resources[i] <= instance.b[i] for i in range(instance.m))

    solution = KnapsackSolution(
        algorithm_name="greedy",
        x=x,
        total_profit=total_profit,
        used_resources=used_resources,
        is_feasible=is_feasible,
        extra_info={
            "best_item": best_j,
            "best_count": best_count,
            "best_value": best_value,
        },
    )

    solution.validate_for_instance(instance)
    return solution
