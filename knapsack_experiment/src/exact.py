from src.models import KnapsackInstance, KnapsackSolution


def solve_exact_dp(instance: KnapsackInstance) -> KnapsackSolution:
    """
    Точное решение целочисленной многомерной задачи о ранце методом ДП.

    Задача: max cx, x ∈ Z+^n, Ax ≤ b  (unbounded integer knapsack).

    Алгоритм: top-down ДП с мемоизацией.
        dp(r) = максимальная прибыль при оставшихся ёмкостях r = (r_0,...,r_{m-1})
        dp(r) = max_{j: A[:,j] ≤ r} ( c[j] + dp(r - A[:,j]) )
        dp((0,...,0)) = 0

    Сложность: O(n * prod(b[i]+1)).
    """
    instance.validate()

    n, m, A, b, c = instance.n, instance.m, instance.A, instance.b, instance.c
    # Предметы с нулевым потреблением всех ресурсов пропускаем:
    # они не уменьшают remaining и вызывают бесконечную рекурсию.
    valid_items = [j for j in range(n) if any(A[i][j] > 0 for i in range(m))]

    memo: dict[tuple, int] = {}

    def dp(remaining: tuple) -> int:
        if remaining in memo:
            return memo[remaining]

        best = 0
        for j in valid_items:
            if all(A[i][j] <= remaining[i] for i in range(m)):
                new_rem = tuple(remaining[i] - A[i][j] for i in range(m))
                val = c[j] + dp(new_rem)
                if val > best:
                    best = val

        memo[remaining] = best
        return best

    initial = tuple(b)
    dp(initial)

    # Восстановление решения — трассировка по DP-таблице
    x = [0] * n
    remaining = list(b)

    while True:
        best_j = -1
        best_val = 0

        for j in valid_items:
            if all(A[i][j] <= remaining[i] for i in range(m)):
                new_rem = tuple(remaining[i] - A[i][j] for i in range(m))
                val = c[j] + memo.get(new_rem, 0)
                if val > best_val:
                    best_val = val
                    best_j = j

        if best_j == -1:
            break

        x[best_j] += 1
        remaining = [remaining[i] - A[i][best_j] for i in range(m)]

    total_profit = sum(c[j] * x[j] for j in range(n))
    used_resources = [sum(A[i][j] * x[j] for j in range(n)) for i in range(m)]
    is_feasible = all(used_resources[i] <= b[i] for i in range(m))

    solution = KnapsackSolution(
        algorithm_name="exact_dp",
        x=x,
        total_profit=total_profit,
        used_resources=used_resources,
        is_feasible=is_feasible,
        extra_info={"memo_states": len(memo)},
    )

    solution.validate_for_instance(instance)
    return solution
