from src.experiment import ExperimentConfig


RANDOM_SEED = 42

NUM_INSTANCES = 30

N_VALUES = [5, 6, 7, 8, 9, 10, 12]
M_VALUES = [1, 2, 3]

DENSITY_VALUES = ["dense", "sparse"]
PROFIT_TYPES = ["random", "correlated", "anticorrelated"]
ALPHA_VALUES = [0.3, 0.8]

MIN_WEIGHT = 1
MAX_WEIGHT = 3

MIN_PROFIT = 1
MAX_PROFIT = 100

SPARSE_ZERO_PROB = 0.5
NOISE_LEVEL = 5

RESULTS_DIR = "data/results"
DETAILED_RESULTS_FILE = f"{RESULTS_DIR}/experiment_results.csv"
SUMMARY_RESULTS_FILE = f"{RESULTS_DIR}/experiment_summary.csv"
GROUPED_SUMMARY_FILE = f"{RESULTS_DIR}/grouped_summary.csv"
WORST_CASE_FILE = f"{RESULTS_DIR}/worst_case_summary.csv"
PLOTS_DIR = f"{RESULTS_DIR}/plots"


def build_experiment_configs() -> list[ExperimentConfig]:
    """
    Строит список конфигураций эксперимента
    по всем комбинациям параметров.
    """
    configs = []

    for n in N_VALUES:
        for m in M_VALUES:
            for density in DENSITY_VALUES:
                for profit_type in PROFIT_TYPES:
                    for alpha in ALPHA_VALUES:
                        config = ExperimentConfig(
                            n=n,
                            m=m,
                            density=density,
                            profit_type=profit_type,
                            alpha=alpha,
                            num_instances=NUM_INSTANCES,
                            min_weight=MIN_WEIGHT,
                            max_weight=MAX_WEIGHT,
                            min_profit=MIN_PROFIT,
                            max_profit=MAX_PROFIT,
                            sparse_zero_prob=SPARSE_ZERO_PROB,
                            noise_level=NOISE_LEVEL,
                            random_seed=RANDOM_SEED,
                        )
                        configs.append(config)

    return configs