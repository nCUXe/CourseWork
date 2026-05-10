import csv
from pathlib import Path
from typing import Any


def ensure_directory(path: str | Path) -> Path:
    """
    Создаёт директорию, если она не существует.
    Возвращает объект Path.
    """
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def save_dicts_to_csv(
    rows: list[dict[str, Any]],
    file_path: str | Path,
) -> None:
    """
    Сохраняет список словарей в CSV-файл.

    Все словари должны иметь одинаковый набор ключей.
    """
    if not rows:
        raise ValueError("Список rows пуст, нечего сохранять")

    file_path = Path(file_path)
    ensure_directory(file_path.parent)

    fieldnames = list(rows[0].keys())

    with file_path.open(mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_summary_to_csv(
    summary: dict[str, Any],
    file_path: str | Path,
) -> None:
    """
    Сохраняет словарь со сводной статистикой в CSV-файл
    в формате: metric, value
    """
    if not summary:
        raise ValueError("Словарь summary пуст, нечего сохранять")

    file_path = Path(file_path)
    ensure_directory(file_path.parent)

    with file_path.open(mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["metric", "value"])

        for key, value in summary.items():
            writer.writerow([key, value])