from tracking.dataset_registry import register_dataset, get_dataset

dataset_id = register_dataset(
    name="credit_card_fraud",
    version="v1",
    dataset_hash=None
)

print("Registered dataset ID:", dataset_id)

dataset = get_dataset(
    name="credit_card_fraud",
    version="v1"
)

print("Fetched dataset:", dataset)
