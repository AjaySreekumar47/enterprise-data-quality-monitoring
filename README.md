# 🧪 Enterprise Data Quality & Governance Monitoring System

This project simulates a full-stack data quality monitoring system designed for modern enterprise data lakes. It combines synthetic data ingestion, manual and automated validation, report generation, and Airflow-based orchestration to create a scalable and modular governance framework.

---

## 📁 Project Structure

```

data\_governance\_project/
├── ingestion/                    # Raw input files (CSV/XLSX)
├── data\_lake/raw/year=2023/month=07/   # Partitioned Parquet files
├── quality/                      # (Optional) Intermediate validation results
├── profiling/                    # (Optional) Data profiling outputs
├── catalog/                      # (Optional) Schema/catalog metadata
├── logs/                         # Text logs from manual checks
├── reports/                      # HTML reports from Great Expectations
├── great\_expectations/          # GE suite configuration & data docs
├── dags/                         # Airflow DAGs for orchestration
└── validate\_\*.py                 # Validation scripts for each dataset

````

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| ✅ Synthetic Data Simulation | Generates realistic datasets for `customers`, `products`, and `sales` using `Faker` |
| ✅ Ingestion to Data Lake | Converts CSV/XLSX to partitioned `.parquet` files for raw data lake storage |
| ✅ Manual Data Quality Checks | Uses `pandas` to validate nulls, duplicates, schema, and outliers |
| ✅ Automated Validation | Uses `Great Expectations` to run expectation suites and build HTML data docs |
| ✅ Streamlit Dashboard | Launches a local dashboard for viewing validation logs and GE reports |
| ✅ Airflow Orchestration | Runs modular DAGs per table and a master DAG to chain validation workflows |

---

## 🛠️ Tools & Technologies

- **Python 3.9 (virtualenv)**
- [Faker](https://faker.readthedocs.io/) – for data generation  
- [pandas + pyarrow](https://pandas.pydata.org/docs/) – for ingestion and Parquet conversion  
- [Great Expectations](https://greatexpectations.io/) – for automated data validation and data docs  
- [Streamlit](https://streamlit.io/) + [ngrok](https://ngrok.com/) – for live dashboarding  
- [Apache Airflow](https://airflow.apache.org/) – for scheduling and orchestration  

---

## 🧪 Data Validation Workflow

### ✅ Manual (Pandas-based)
- Null value check
- Duplicate row check
- Schema/data type check
- Outlier detection (z-score)

Logs are saved under:  
```bash
/logs/customer_log.txt
/logs/product_log.txt
/logs/sales_log.txt
````

### ✅ Automated (Great Expectations)

* Email format validation (regex)
* Type expectations
* Row count boundaries
* Null expectations

HTML reports are generated at:

```
great_expectations/uncommitted/data_docs/local_site/index.html
```

---

## 🌐 Dashboard

Start the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

Expose it publicly:

```bash
ngrok http 8501
```

---

## 🌀 Airflow DAGs

Each table has its own DAG:

* `customer_validation_dag.py`
* `product_validation_dag.py`
* `sales_validation_dag.py`

A master orchestrator DAG runs them in sequence:

* `master_validation_dag.py`

All scripts trigger validations using:

```bash
/usr/local/envs/ge-env/bin/python3.9 validate_customer.py
```

---

## 📦 Setup Instructions

1. Clone the repo
2. Create virtualenv using Python 3.9
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up Great Expectations:

```bash
great_expectations init
```

5. Launch Airflow and Streamlit as needed

---

## 📌 Example Use Cases

* Building robust **data quality pipelines** for new data lakes
* Validating ETL jobs with **automated data contracts**
* Auditing schema drift and **compliance metrics**
* Running **governance dashboards** for business and technical stakeholders

---

## 👨‍💻 Author

**Ajay Sreekumar**
AI Research Engineer | Data Science & Platform Engineering | MLOps & Governance

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
