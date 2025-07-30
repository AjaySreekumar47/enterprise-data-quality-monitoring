import os
import pandas as pd
import great_expectations as ge
from great_expectations.data_context import DataContext
from great_expectations.core.batch import RuntimeBatchRequest

# Paths
project_path = "/content/drive/MyDrive/data_governance_project"
ge_path = os.path.join(project_path, "great_expectations")
data_base_path = os.path.join(project_path, "data_lake/raw/year=2023")
suite_name = "customer_suite"

# Load context
context = DataContext(context_root_dir=ge_path)

# Loop through July and August
for month in ["07", "08"]:
    print(f"\n📦 Validating data for month={month}")

    data_path = os.path.join(data_base_path, f"month={month}/customer.parquet")

    if not os.path.exists(data_path):
        print(f"⚠️ File not found: {data_path}")
        continue

    df = pd.read_parquet(data_path)

    batch_request = RuntimeBatchRequest(
        datasource_name="my_filesystem_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name=f"customer_month_{month}",  # logical name
        runtime_parameters={"batch_data": df},
        batch_identifiers={"default_identifier_name": f"month_{month}"}
    )

    # Get validator and attach expectations
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name
    )

    # Run validation
    context.run_validation_operator(
        "action_list_operator",
        assets_to_validate=[validator],
        run_id=f"validation_month_{month}"
    )

# Build final report
context.build_data_docs()
print("✅ All validations complete. Visit data_docs/local_site for the full report.")
