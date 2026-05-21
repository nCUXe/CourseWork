from config import (
    DETAILED_RESULTS_FILE,
    GROUPED_SUMMARY_FILE,
    PLOTS_DIR,
    SUMMARY_RESULTS_FILE,
    WORST_CASE_FILE,
    build_experiment_configs,
)
from src.experiment import (
    results_to_dicts,
    run_experiment_series,
    summarize_results,
    summarize_results_by_configuration,
)
from src.utils import save_dicts_to_csv, save_summary_to_csv
from src.visualization import (
    build_all_extended_plots,
    plot_accuracy_spread_by_m,
    plot_accuracy_spread_by_m_and_profit_type,
    plot_exact_rate_by_n,
    plot_worst_case_by_config,
)


def main():
    configs = build_experiment_configs()

    all_results = []

    print(f"Количество конфигураций: {len(configs)}")

    for config_index, config in enumerate(configs, start=1):
        print(
            f"Запуск конфигурации {config_index}/{len(configs)}: "
            f"n={config.n}, m={config.m}, density={config.density}, "
            f"profit_type={config.profit_type}, alpha={config.alpha}"
        )

        results = run_experiment_series(config)
        all_results.extend(results)

    summary = summarize_results(all_results)
    grouped_summary = summarize_results_by_configuration(all_results)

    result_rows = results_to_dicts(all_results)

    save_dicts_to_csv(result_rows, DETAILED_RESULTS_FILE)
    save_summary_to_csv(summary, SUMMARY_RESULTS_FILE)
    save_dicts_to_csv(grouped_summary, GROUPED_SUMMARY_FILE)

    build_all_extended_plots(GROUPED_SUMMARY_FILE, PLOTS_DIR)
    plot_accuracy_spread_by_m(DETAILED_RESULTS_FILE, PLOTS_DIR)
    plot_accuracy_spread_by_m_and_profit_type(DETAILED_RESULTS_FILE, PLOTS_DIR)
    plot_exact_rate_by_n(GROUPED_SUMMARY_FILE, PLOTS_DIR)
    plot_worst_case_by_config(DETAILED_RESULTS_FILE, PLOTS_DIR, WORST_CASE_FILE)

    print("\nЭксперимент завершён.")
    print(f"Подробные результаты: {DETAILED_RESULTS_FILE}")
    print(f"Общая сводка: {SUMMARY_RESULTS_FILE}")
    print(f"Сводка по конфигурациям: {GROUPED_SUMMARY_FILE}")
    print(f"Графики: {PLOTS_DIR}")

    print("\nИтоговая сводка:")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()