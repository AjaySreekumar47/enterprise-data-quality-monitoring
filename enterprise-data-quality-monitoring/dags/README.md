# Airflow DAGs

This folder contains optional Apache Airflow DAGs for orchestrating the data quality validation pipeline.

## DAGs

| DAG | Purpose |
|---|---|
| `customer_validation_dag.py` | Runs customer Great Expectations validation |
| `product_validation_dag.py` | Runs product Great Expectations validation |
| `sales_validation_dag.py` | Runs sales Great Expectations validation |
| `master_validation_dag.py` | Runs customer, product, and sales validations in sequence |

## Notes

The DAGs call the reusable validation scripts under `scripts/`. This keeps validation logic centralized and allows the same pipeline to run either manually or through Airflow.

Airflow is best run in a Linux, WSL, or Docker environment. For local Windows testing, use:

```bash
python scripts/run_all_validations.py
```

## What not to do yet

Do **not** try to install/run Airflow natively on Windows right now unless you want pain. It is enough for this repo to include real, valid DAGs and document that Airflow is optional.

For a stronger test, later we can add a `docker-compose.airflow.yml`, but that is a separate step.

## After creating files

Run this quick local sanity check from the repo root:

```powershell
python -m py_compile dags\customer_validation_dag.py dags\product_validation_dag.py dags\sales_validation_dag.py dags\master_validation_dag.py
```