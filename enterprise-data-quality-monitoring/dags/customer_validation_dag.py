from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_ROOT = Path(__file__).resolve().parents[1]

with DAG(
    dag_id="customer_validation_dag",
    description="Run Great Expectations validation for customer data.",
    start_date=datetime(2025, 7, 30),
    schedule_interval=None,
    catchup=False,
    tags=["data-quality", "great-expectations", "customers"],
) as dag:
    validate_customer = BashOperator(
        task_id="validate_customer",
        bash_command=f"cd {PROJECT_ROOT} && python scripts/validate_customer.py",
    )