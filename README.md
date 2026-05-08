# Enterprise Data Quality & Governance Monitoring System

A local, portfolio-ready data quality monitoring project for synthetic enterprise datasets. The project demonstrates raw data ingestion, Parquet-based data lake storage, manual quality logs, Great Expectations validation suites, a Streamlit monitoring dashboard, and optional Airflow DAG orchestration.

---

## Project Overview

This project simulates a small enterprise data quality workflow across three business datasets:

- `customers`
- `products`
- `sales`

The pipeline validates raw/curated data assets using both manual quality logs and Great Expectations expectation suites. A Streamlit dashboard provides an executive-friendly view of dataset health, schema profiles, validation logs, and the generated Great Expectations Data Docs.

---

## Repository Structure

```text
enterprise-data-quality-monitoring/
├── data_governance_project/
│   ├── ingestion/
│   │   ├── customer.csv
│   │   ├── product.xlsx
│   │   └── sales.csv
│   ├── data_lake/
│   │   └── raw/year=2023/month=07/
│   │       ├── customer.parquet
│   │       ├── product.parquet
│   │       └── sales.parquet
│   └── logs/
│       ├── customer_log.txt
│       ├── product_log.txt
│       └── sales_log.txt
├── great_expectations/
│   ├── great_expectations.yml
│   ├── expectations/
│   │   ├── customer_suite.json
│   │   ├── product_suite.json
│   │   └── sales_suite.json
│   └── uncommitted/data_docs/
├── scripts/
│   ├── validate_customer.py
│   ├── validate_product.py
│   ├── validate_sales.py
│   └── run_all_validations.py
├── streamlit_app/
│   └── dashboard.py
├── dags/
│   ├── customer_validation_dag.py
│   ├── product_validation_dag.py
│   ├── sales_validation_dag.py
│   └── master_validation_dag.py
├── notebooks/
│   └── enterprise_data_quality_monitoring.ipynb
├── requirements.txt
└── README.md
````

---

## Features

| Capability                     |      Status | Description                                                                                    |
| ------------------------------ | ----------: | ---------------------------------------------------------------------------------------------- |
| Synthetic enterprise datasets  | Implemented | Customer, product, and sales data are included as CSV/XLSX ingestion files                     |
| Data lake storage              | Implemented | Curated datasets are stored as partitioned Parquet files                                       |
| Manual quality logs            | Implemented | Text logs capture basic checks such as missing values, duplicates, schema checks, and outliers |
| Great Expectations validation  | Implemented | Separate expectation suites exist for customer, product, and sales datasets                    |
| End-to-end validation runner   | Implemented | `scripts/run_all_validations.py` runs all table validations                                    |
| Streamlit monitoring dashboard | Implemented | Dashboard summarizes dataset health, schemas, logs, and GE report output                       |
| Airflow DAG orchestration      |    Optional | DAGs are provided for Linux/WSL/Docker-based Airflow execution                                 |

---

## Dataset Summary

| Dataset   |   Rows | Columns | Format  |
| --------- | -----: | ------: | ------- |
| Customers |  5,000 |       4 | Parquet |
| Products  |    200 |       3 | Parquet |
| Sales     | 50,000 |       5 | Parquet |

Total monitored rows: **55,200**

---

## Tech Stack

* Python
* pandas
* pyarrow
* Great Expectations
* Streamlit
* Apache Airflow DAG definitions
* Parquet data lake layout
* Synthetic enterprise-style data

---

## Setup

Python 3.10 is recommended.

```bash
git clone https://github.com/AjaySreekumar47/enterprise-data-quality-monitoring.git
cd enterprise-data-quality-monitoring/enterprise-data-quality-monitoring
python -m venv .venv
```

Activate the environment.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install core dependencies:

```bash
python -m pip install --upgrade pip setuptools wheel
pip install pandas==1.5.3 numpy==1.23.5 pyarrow openpyxl faker great_expectations==0.16.8 streamlit
```

Airflow is listed as an optional orchestration dependency. It is best installed and run in Linux, WSL, or Docker rather than native Windows.

---

## Run Validations

Run all table-level validations:

```bash
python scripts/run_all_validations.py
```

Or run each validation independently:

```bash
python scripts/validate_customer.py
python scripts/validate_product.py
python scripts/validate_sales.py
```

The validation scripts automatically discover available monthly Parquet partitions under:

```text
data_governance_project/data_lake/raw/year=2023/month=*/
```

---

## Launch Dashboard

```bash
streamlit run streamlit_app/dashboard.py
```

The dashboard includes:

* Executive summary metrics
* Dataset health snapshot
* Dataset schema profiles
* Numeric summaries
* Manual validation log viewer
* Embedded Great Expectations Data Docs

---

## Great Expectations Reports

After validation, the dashboard reads the generated GE report from:

```text
great_expectations/uncommitted/data_docs/index.html
```

The project uses Great Expectations suites for:

```text
customer_suite
product_suite
sales_suite
```

---

## Optional Airflow Orchestration

The `dags/` folder contains optional Airflow DAGs:

| DAG                          | Purpose                                                   |
| ---------------------------- | --------------------------------------------------------- |
| `customer_validation_dag.py` | Runs customer validation                                  |
| `product_validation_dag.py`  | Runs product validation                                   |
| `sales_validation_dag.py`    | Runs sales validation                                     |
| `master_validation_dag.py`   | Runs customer, product, and sales validations in sequence |

For local Windows use, prefer:

```bash
python scripts/run_all_validations.py
```

For Airflow execution, use a Linux, WSL, or Docker environment and point Airflow’s DAG folder to this repo’s `dags/` directory.

---

## What This Project Demonstrates

This project demonstrates practical data engineering and governance skills:

* Designing a small enterprise-style data lake structure
* Validating datasets with Great Expectations
* Building reusable validation scripts
* Creating business-friendly monitoring dashboards
* Separating validation logic from orchestration logic
* Providing optional Airflow DAGs for scheduled execution
* Making Colab-originated code portable for local execution

---

## Known Limitations

* The included data is synthetic and intended for demonstration.
* The current data lake contains one monthly partition: `month=07`.
* Airflow DAGs are included as optional orchestration definitions and are best run in Linux/WSL/Docker.
* Great Expectations is pinned to a legacy-compatible version for this project.

---

## Author

Ajay Sreekumar

---

## License

This project is open-source and available under the MIT License.
