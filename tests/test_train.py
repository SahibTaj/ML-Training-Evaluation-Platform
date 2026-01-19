from train import run_training

run_training(
    experiment_name="fraud_baseline_db",
    dataset_name="credit_card_fraud",
    dataset_version="v1",
    threshold=0.5
)
