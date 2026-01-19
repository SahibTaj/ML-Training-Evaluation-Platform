from tracking.regression_checker import check_regression

# Use a real experiment_id from your DB
passed, reasons = check_regression(
    model_name="fraud_detector",
    candidate_experiment_id=2
)

print("Passed:", passed)
print("Reasons:", reasons)
