import argparse
import yaml
import sys

from tracking.dataset_registry import get_dataset
from train import run_training


def load_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def validate_dataset(dataset_cfg: dict):
    dataset = get_dataset(
        name=dataset_cfg["name"],
        version=dataset_cfg["version"]
    )

    if dataset is None:
        raise ValueError(
            f"Dataset {dataset_cfg['name']}:{dataset_cfg['version']} not registered"
        )


def main():
    parser = argparse.ArgumentParser(description="Run ML experiment")
    parser.add_argument(
        "--config",
        required=True,
        help="Path to experiment config YAML"
    )

    args = parser.parse_args()

    try:
        config = load_config(args.config)

        validate_dataset(config["dataset"])

        run_training(
            experiment_name=config["experiment_name"],
            dataset_name=config["dataset"]["name"],
            dataset_version=config["dataset"]["version"],
            threshold=config["model"]["threshold"]
        )

    except Exception as e:
        print("❌ Experiment orchestration failed:")
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
