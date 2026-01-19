from tracking.experiment_tracker import (
    create_experiment,
    update_experiment_status,
    log_metrics
)

# 1. Create experiment
exp_id = create_experiment(
    experiment_name="fraud_baseline_test",
    dataset_version="v1",
    model_type="logistic_regression"
)

print("Created experiment ID:", exp_id)

# 2. Update status
update_experiment_status(exp_id, "RUNNING")
update_experiment_status(exp_id, "COMPLETED")

# 3. Log dummy metrics
log_metrics(
    experiment_id=exp_id,
    accuracy=0.9,
    precision=0.1,
    recall=0.8,
    f1=0.18,
    roc_auc=0.95,
    training_time=1.2
)

print("Metrics logged successfully.")
