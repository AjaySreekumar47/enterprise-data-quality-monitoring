from pathlib import Path

import pandas as pd
from great_expectations.data_context import DataContext
from great_expectations.core.batch import RuntimeBatchRequest

ROOT_DIR = Path(__file__).resolve().parents[1]

ge_path = ROOT_DIR / "great_expectations"
data_base_path = ROOT_DIR / "data_governance_project" / "data_lake" / "raw" / "year=2023"
suite_name = "product_suite"

context = DataContext(context_root_dir=str(ge_path))

product_files = sorted(data_base_path.glob("month=*/product.parquet"))

if not product_files:
    raise FileNotFoundError(f"No product parquet files found under: {data_base_path}")

for data_path in product_files:
    month = data_path.parent.name.replace("month=", "")
    print(f"\n📦 Validating product data for month={month}")

    df = pd.read_parquet(data_path)

    batch_request = RuntimeBatchRequest(
        datasource_name="my_filesystem_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name=f"product_month_{month}",
        runtime_parameters={"batch_data": df},
        batch_identifiers={"default_identifier_name": f"product_month_{month}"},
    )

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name,
    )

    context.run_validation_operator(
        "action_list_operator",
        assets_to_validate=[validator],
        run_id=f"product_validation_month_{month}",
    )

context.build_data_docs()
print(f"✅ Product validations complete. Open: {ge_path / 'uncommitted' / 'data_docs' / 'index.html'}")