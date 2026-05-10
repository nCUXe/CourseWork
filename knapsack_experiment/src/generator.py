import random
from typing import List

from src.models import KnapsackInstance


def generate_matrix_A(
    n: int,
    m: int,
    density: str = "dense",
    min_weight: int = 1,
    max_weight: int = 20,
    sparse_zero_prob: float = 0.5,
) -> List[List[int]]:
    """
    Генерирует матрицу ограничений A размера m x n.

    A[j][i] = расход ресурса j на предмет i

    density:
        - "dense": почти все элементы положительные
        - "sparse": часть элементов заменяется на 0
    """
    if n <= 0:
        raise ValueError("n должно быть положительным")
    if m <= 0:
        raise ValueError("m должно быть положительным")
    if min_weight > max_weight:
        raise ValueError("min_weight не может быть больше max_weight")
    if not (0.0 <= sparse_zero_prob <= 1.0):
        raise ValueError("sparse_zero_prob должен быть в диапазоне [0, 1]")

    A = []

    for j in range(m):
        row = []
        for i in range(n):
            value = random.randint(min_weight, max_weight)

            if density == "sparse":
                if random.random() < sparse_zero_prob:
                    value = 0
            elif density != "dense":
                raise ValueError("density должен быть 'dense' или 'sparse'")

            row.append(value)

        A.append(row)

    return A


def generate_capacities_b(A: List[List[int]], alpha: float) -> List[int]:
    """
    Генерирует вектор ёмкостей b.

    Для каждого ресурса:
        b[j] = max(1, int(alpha * sum(A[j])))

    alpha:
        - маленькое значение -> жёсткие ограничения
        - большое значение -> слабые ограничения
    """
    if not A:
        raise ValueError("Матрица A не должна быть пустой")
    if alpha <= 0:
        raise ValueError("alpha должно быть положительным")

    b = []

    for row in A:
        total = sum(row)
        capacity = max(1, int(alpha * total))
        b.append(capacity)

    return b


def generate_profits_c(
    A: List[List[int]],
    profit_type: str = "random",
    min_profit: int = 1,
    max_profit: int = 100,
    noise_level: int = 5,
) -> List[int]:
    """
    Генерирует вектор прибыли c длины n.

    profit_type:
        - "random"         : случайные прибыли
        - "correlated"     : прибыль растёт вместе с суммарным расходом ресурсов
        - "anticorrelated" : прибыль убывает при росте суммарного расхода ресурсов
    """
    if not A:
        raise ValueError("Матрица A не должна быть пустой")
    if min_profit > max_profit:
        raise ValueError("min_profit не может быть больше max_profit")
    if noise_level < 0:
        raise ValueError("noise_level не может быть отрицательным")

    m = len(A)
    n = len(A[0])

    for row in A:
        if len(row) != n:
            raise ValueError("Все строки матрицы A должны иметь одинаковую длину")

    total_weights = []
    for i in range(n):
        total_weight = sum(A[j][i] for j in range(m))
        total_weights.append(total_weight)

    c = []

    if profit_type == "random":
        for _ in range(n):
            profit = random.randint(min_profit, max_profit)
            c.append(profit)

    elif profit_type == "correlated":
        for total_weight in total_weights:
            noise = random.randint(-noise_level, noise_level)
            profit = total_weight + noise
            c.append(max(1, profit))

    elif profit_type == "anticorrelated":
        max_total_weight = max(total_weights) if total_weights else 1
        C = max_total_weight + 10

        for total_weight in total_weights:
            noise = random.randint(-noise_level, noise_level)
            profit = C - total_weight + noise
            c.append(max(1, profit))

    else:
        raise ValueError(
            "profit_type должен быть 'random', 'correlated' или 'anticorrelated'"
        )

    return c


def generate_instance(
    n: int,
    m: int,
    density: str = "dense",
    profit_type: str = "random",
    alpha: float = 0.5,
    min_weight: int = 1,
    max_weight: int = 20,
    min_profit: int = 1,
    max_profit: int = 100,
    sparse_zero_prob: float = 0.5,
    noise_level: int = 5,
) -> KnapsackInstance:
    """
    Генерирует полный экземпляр многомерной задачи о рюкзаке.
    """
    A = generate_matrix_A(
        n=n,
        m=m,
        density=density,
        min_weight=min_weight,
        max_weight=max_weight,
        sparse_zero_prob=sparse_zero_prob,
    )

    b = generate_capacities_b(A=A, alpha=alpha)

    c = generate_profits_c(
        A=A,
        profit_type=profit_type,
        min_profit=min_profit,
        max_profit=max_profit,
        noise_level=noise_level,
    )

    instance = KnapsackInstance(n=n, m=m, A=A, b=b, c=c)
    instance.validate()

    return instance