from tracking.model_registry import (
    register_model,
    promote_model,
    get_active_model,
    list_models
)

# Register a model from an existing experiment ID
model_id = register_model(
    model_name="fraud_detector",
    experiment_id=1,   # use a real experiment_id from DB
    stage="staging"
)

print("Registered model ID:", model_id)

# Promote to production
promote_model(model_id, "production")

# Fetch active model
active = get_active_model("fraud_detector")
print("Active model:", active)

# List all versions
all_models = list_models("fraud_detector")
print("All models:", all_models)
