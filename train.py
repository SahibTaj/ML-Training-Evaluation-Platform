import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from tracking.experiment_tracker import (
    create_experiment,
    update_experiment_status,
    log_metrics
)


def run_training(
    experiment_name: str,
    dataset_name: str,
    dataset_version: str,
    threshold: float = 0.5
):
    
    experiment_id = create_experiment(
        experiment_name=experiment_name,
        dataset_version=dataset_version,
        model_type="logistic_regression"
    )

    print(f"🚀 Experiment created with ID: {experiment_id}")

    try:
        update_experiment_status(experiment_id, "RUNNING")

        data_path = f"data/versions/{dataset_version}/creditcard.csv"
        df = pd.read_csv(data_path)

        X = df.drop("Class", axis=1)
        y = df["Class"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        start_time = time.time()

        model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=3000, class_weight="balanced"))
])
        model.fit(X_train, y_train)

        training_time = time.time() - start_time

        y_prob = model.predict_proba(X_test)[:, 1]
        y_pred = (y_prob >= threshold).astype(int)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)

        log_metrics(
            experiment_id=experiment_id,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1=f1,
            roc_auc=roc_auc,
            training_time=training_time
        )

        update_experiment_status(experiment_id, "COMPLETED")

        print("✅ Experiment completed successfully.")

    except Exception as e:
        update_experiment_status(experiment_id, "FAILED")
        print("❌ Experiment failed:", str(e))
        raise
