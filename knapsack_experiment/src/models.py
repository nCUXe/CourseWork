from dataclasses import dataclass, field
from typing import List


@dataclass
class KnapsackInstance:
    """
    Один экземпляр многомерной целочисленной задачи о ранце.

    n - число типов предметов
    m - число ограничений (ресурсов)

    A[j][i] - расход ресурса j на одну единицу предмета i
    b[j]    - ёмкость ресурса j
    c[i]    - прибыль от одной единицы предмета i
    """
    n: int
    m: int
    A: List[List[int]]
    b: List[int]
    c: List[int]

    def validate(self) -> None:
        if self.n <= 0:
            raise ValueError("n должно быть положительным числом")

        if self.m <= 0:
            raise ValueError("m должно быть положительным числом")

        if len(self.A) != self.m:
            raise ValueError(
                f"Матрица A должна содержать {self.m} строк, получено {len(self.A)}"
            )

        for j, row in enumerate(self.A):
            if len(row) != self.n:
                raise ValueError(
                    f"Строка A[{j}] должна содержать {self.n} элементов, "
                    f"получено {len(row)}"
                )

        if len(self.b) != self.m:
            raise ValueError(
                f"Вектор b должен содержать {self.m} элементов, получено {len(self.b)}"
            )

        if len(self.c) != self.n:
            raise ValueError(
                f"Вектор c должен содержать {self.n} элементов, получено {len(self.c)}"
            )

        for j, row in enumerate(self.A):
            for i, value in enumerate(row):
                if value < 0:
                    raise ValueError(
                        f"Элемент A[{j}][{i}] не может быть отрицательным"
                    )

        for j, value in enumerate(self.b):
            if value < 0:
                raise ValueError(f"Элемент b[{j}] не может быть отрицательным")

        for i, value in enumerate(self.c):
            if value < 0:
                raise ValueError(f"Элемент c[{i}] не может быть отрицательным")

    def item_resource_usage(self, item_index: int) -> List[int]:
        """
        Возвращает расходы всех ресурсов на одну единицу предмета.
        """
        if not (0 <= item_index < self.n):
            raise IndexError("Некорректный индекс предмета")

        return [self.A[j][item_index] for j in range(self.m)]

    def total_weight_of_item(self, item_index: int) -> int:
        """
        Возвращает суммарный расход всех ресурсов на одну единицу предмета.
        """
        return sum(self.item_resource_usage(item_index))

    def max_count_for_item(self, item_index: int) -> int:
        """
        Возвращает максимальное количество единиц предмета item_index,
        которое можно взять, если брать только этот предмет.

        Формула соответствует алгоритму из статьи:

        k_i = min по j, где A[j][i] > 0, floor(b[j] / A[j][i])
        """
        if not (0 <= item_index < self.n):
            raise IndexError("Некорректный индекс предмета")

        limits = []

        for j in range(self.m):
            resource_usage = self.A[j][item_index]

            if resource_usage > 0:
                limits.append(self.b[j] // resource_usage)

        if not limits:
            return 0

        return min(limits)


@dataclass
class KnapsackSolution:
    """
    Решение целочисленной задачи о ранце.

    algorithm_name    - название алгоритма
    x[i]              - сколько единиц предмета i взято
    total_profit      - суммарная прибыль
    used_resources[j] - сколько ресурса j использовано
    is_feasible       - допустимо ли решение
    """
    algorithm_name: str
    x: List[int]
    total_profit: int
    used_resources: List[int]
    is_feasible: bool = True
    extra_info: dict = field(default_factory=dict)

    def validate_for_instance(self, instance: KnapsackInstance) -> None:
        if len(self.x) != instance.n:
            raise ValueError(
                f"x должен содержать {instance.n} элементов, получено {len(self.x)}"
            )

        if len(self.used_resources) != instance.m:
            raise ValueError(
                f"used_resources должен содержать {instance.m} элементов, "
                f"получено {len(self.used_resources)}"
            )

        for i, value in enumerate(self.x):
            if value < 0:
                raise ValueError(
                    f"x[{i}] не может быть отрицательным, получено {value}"
                )

        for j, value in enumerate(self.used_resources):
            if value < 0:
                raise ValueError(
                    f"used_resources[{j}] не может быть отрицательным"
                )

        if self.total_profit < 0:
            raise ValueError("total_profit не может быть отрицательным")

    def chosen_indices(self) -> List[int]:
        """
        Возвращает индексы предметов, которые взяты хотя бы один раз.
        """
        return [i for i, count in enumerate(self.x) if count > 0]

    def chosen_items_with_counts(self) -> List[tuple[int, int]]:
        """
        Возвращает пары:
        (индекс предмета, количество)
        """
        return [(i, count) for i, count in enumerate(self.x) if count > 0]