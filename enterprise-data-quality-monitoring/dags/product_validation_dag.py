from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_ROOT = Path(__file__).resolve().parents[1]

with DAG(
    dag_id="product_validation_dag",
    description="Run Great Expectations validation for product data.",
    start_date=datetime(2025, 7, 30),
    schedule_interval=None,
    catchup=False,
    tags=["data-quality", "great-expectations", "products"],
) as dag:
    validate_product = BashOperator(
        task_id="validate_product",
        bash_command=f"cd {PROJECT_ROOT} && python scripts/validate_product.py",
    )