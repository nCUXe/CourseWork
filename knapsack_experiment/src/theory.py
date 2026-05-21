"""
Теоретические гарантии точности приближённого алгоритма из статьи

  A. Yu. Chirkov, D. V. Gribanov, N. Yu. Zolotykh.
  "On the Proximity of the Optimal Values of the Multi-Dimensional
   Knapsack Problem with and without the Cardinality Constraint",
  arXiv:2004.08589v1 (2020).

Одномерный случай (m = 1), Section 3 статьи:

    δ_n = δ_{n-1}·(δ_{n-1} + 1),     δ_1 = 1
    ε_n = 1 + ε_{n-1}·(δ_{n-1} + 1), ε_1 = 1
    α_1n = δ_n / ε_n

Последовательность α_1n монотонно убывает к
    α₁∞ = 0.591355492056890…

Многомерный случай, Theorem 1 (формула (2)):

    α_mn = α_1q / ( m + r·(α_1q/α_{1,q+1} − 1) ),
    где n = q·m + r,  q = ⌊n/m⌋.
"""

# Предел α₁∞ из статьи (Table 1 / Section 3).
ALPHA_1_INF = 0.591355492056890


# Кэш точных значений α_1q (q → float).
_delta_cache: dict[int, int] = {1: 1}
_eps_cache: dict[int, int] = {1: 1}


def _delta(n: int) -> int:
    if n not in _delta_cache:
        prev = _delta(n - 1)
        _delta_cache[n] = prev * (prev + 1)
    return _delta_cache[n]


def _eps(n: int) -> int:
    if n not in _eps_cache:
        _eps_cache[n] = 1 + _eps(n - 1) * (_delta(n - 1) + 1)
    return _eps_cache[n]


def alpha_1q(q: int) -> float:
    """
    Точная гарантированная точность одномерной задачи (m = 1)
    при q типах предметов: α_1q = δ_q / ε_q.
    """
    if q < 1:
        raise ValueError("q должно быть >= 1")
    return _delta(q) / _eps(q)


def asymptotic_bound(m: int) -> float:
    """
    Асимптотическая нижняя граница (Corollary 3):
        α_mn → α₁∞ / m   при n → ∞.

    Горизонтальная опорная линия на spread-графиках.
    """
    if m <= 0:
        raise ValueError("m должно быть положительным")
    return ALPHA_1_INF / m


def guaranteed_ratio(m: int, n: int) -> float | None:
    """
    Точная гарантированная точность α_mn по формуле (2) статьи.

    n = q·m + r, q = ⌊n/m⌋. Возвращает None, если q < 1
    (n < m — для исследуемых параметров не встречается).
    """
    if m <= 0:
        raise ValueError("m должно быть положительным")
    if n <= 0:
        raise ValueError("n должно быть положительным")

    q, r = divmod(n, m)
    if q < 1:
        return None

    a_q = alpha_1q(q)
    a_q1 = alpha_1q(q + 1)

    denominator = m + r * (a_q / a_q1 - 1)
    if denominator <= 0:
        return None

    return a_q / denominator
