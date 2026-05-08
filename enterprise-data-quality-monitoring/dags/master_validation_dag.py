from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_ROOT = Path(__file__).resolve().parents[1]

with DAG(
    dag_id="master_validation_dag",
    description="Run customer, product, and sales data quality validations in sequence.",
    start_date=datetime(2025, 7, 30),
    schedule_interval=None,
    catchup=False,
    tags=["data-quality", "great-expectations", "orchestration"],
) as dag:
    validate_customer = BashOperator(
        task_id="validate_customer",
        bash_command=f"cd {PROJECT_ROOT} && python scripts/validate_customer.py",
    )

    validate_product = BashOperator(
        task_id="validate_product",
        bash_command=f"cd {PROJECT_ROOT} && python scripts/validate_product.py",
    )

    validate_sales = BashOperator(
        task_id="validate_sales",
        bash_command=f"cd {PROJECT_ROOT} && python scripts/validate_sales.py",
    )

    validate_customer >> validate_product >> validate_sales