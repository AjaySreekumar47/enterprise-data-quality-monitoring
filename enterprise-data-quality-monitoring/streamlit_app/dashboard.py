from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data_governance_project" / "data_lake" / "raw" / "year=2023"
LOG_DIR = ROOT_DIR / "data_governance_project" / "logs"
GE_REPORT_PATH = ROOT_DIR / "great_expectations" / "uncommitted" / "data_docs" / "index.html"

DATASETS = {
    "Customers": {
        "file": "customer.parquet",
        "log": "customer_log.txt",
        "id_col": "customer_id",
        "description": "Customer master data with identity, email, and age fields.",
    },
    "Products": {
        "file": "product.parquet",
        "log": "product_log.txt",
        "id_col": "product_id",
        "description": "Product reference data with product names and prices.",
    },
    "Sales": {
        "file": "sales.parquet",
        "log": "sales_log.txt",
        "id_col": "sale_id",
        "description": "Transaction-level sales records linked to customers and products.",
    },
}


st.set_page_config(
    page_title="Enterprise Data Quality Monitoring",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Enterprise Data Quality Monitoring System")
st.caption(
    "A local data quality and governance dashboard for synthetic enterprise datasets, "
    "manual quality logs, and Great Expectations validation reports."
)


@st.cache_data
def load_dataset(file_name: str) -> pd.DataFrame:
    files = sorted(DATA_DIR.glob(f"month=*/{file_name}"))
    if not files:
        return pd.DataFrame()

    frames = []
    for file_path in files:
        df = pd.read_parquet(file_path)
        df["partition_month"] = file_path.parent.name.replace("month=", "")
        frames.append(df)

    return pd.concat(frames, ignore_index=True)


@st.cache_data
def load_log(log_name: str) -> str:
    path = LOG_DIR / log_name
    if not path.exists():
        return f"Log file not found: {path}"
    return path.read_text(encoding="utf-8", errors="ignore")


def get_dataset_summary() -> pd.DataFrame:
    rows = []

    for display_name, config in DATASETS.items():
        df = load_dataset(config["file"])

        if df.empty:
            rows.append(
                {
                    "Dataset": display_name,
                    "Rows": 0,
                    "Columns": 0,
                    "Duplicate IDs": "N/A",
                    "Missing Values": "N/A",
                    "Partitions": "N/A",
                }
            )
            continue

        id_col = config["id_col"]
        duplicate_ids = int(df[id_col].duplicated().sum()) if id_col in df.columns else "N/A"
        missing_values = int(df.isna().sum().sum())
        partitions = ", ".join(sorted(df["partition_month"].astype(str).unique()))

        rows.append(
            {
                "Dataset": display_name,
                "Rows": len(df),
                "Columns": len(df.columns),
                "Duplicate IDs": duplicate_ids,
                "Missing Values": missing_values,
                "Partitions": partitions,
            }
        )

    return pd.DataFrame(rows)


summary_df = get_dataset_summary()
total_rows = int(summary_df["Rows"].sum())
total_datasets = len(DATASETS)
total_columns = int(summary_df["Columns"].sum())
available_logs = sum((LOG_DIR / config["log"]).exists() for config in DATASETS.values())
ge_report_available = GE_REPORT_PATH.exists()

tab_overview, tab_profiles, tab_logs, tab_ge = st.tabs(
    [
        "Executive Summary",
        "Dataset Profiles",
        "Validation Logs",
        "Great Expectations Report",
    ]
)

with tab_overview:
    st.subheader("Executive Summary")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Datasets Monitored", f"{total_datasets}")
    col2.metric("Rows Checked", f"{total_rows:,}")
    col3.metric("Columns Profiled", f"{total_columns}")
    col4.metric("Validation Logs", f"{available_logs}/{total_datasets}")
    col5.metric("GE Report", "Available" if ge_report_available else "Missing")

    st.markdown("### Dataset Health Snapshot")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.markdown("### Project Workflow")
    st.markdown(
        """
        1. Synthetic customer, product, and sales data are stored as raw ingestion files.
        2. Data is converted into partitioned Parquet files under a data-lake-style layout.
        3. Manual quality checks produce text logs for nulls, duplicates, schema issues, and value anomalies.
        4. Great Expectations suites validate the curated Parquet datasets.
        5. This dashboard provides a business-friendly summary plus access to the underlying GE technical report.
        """
    )

with tab_profiles:
    st.subheader("Dataset Profiles")

    selected_dataset = st.selectbox("Select dataset", list(DATASETS.keys()))
    config = DATASETS[selected_dataset]
    df = load_dataset(config["file"])

    st.markdown(f"**Description:** {config['description']}")

    if df.empty:
        st.warning(f"No Parquet files found for {selected_dataset}.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", f"{len(df):,}")
        c2.metric("Columns", f"{len(df.columns)}")
        c3.metric("Missing Values", f"{int(df.isna().sum().sum()):,}")
        id_col = config["id_col"]
        duplicate_ids = int(df[id_col].duplicated().sum()) if id_col in df.columns else 0
        c4.metric("Duplicate IDs", f"{duplicate_ids:,}")

        st.markdown("### Schema")
        schema_df = pd.DataFrame(
            {
                "Column": df.columns,
                "Data Type": [str(dtype) for dtype in df.dtypes],
                "Missing Values": [int(df[col].isna().sum()) for col in df.columns],
                "Unique Values": [int(df[col].nunique(dropna=True)) for col in df.columns],
            }
        )
        st.dataframe(schema_df, use_container_width=True, hide_index=True)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            st.markdown("### Numeric Summary")
            st.dataframe(df[numeric_cols].describe().T, use_container_width=True)

        st.markdown("### Sample Records")
        st.dataframe(df.head(25), use_container_width=True, hide_index=True)

with tab_logs:
    st.subheader("Manual Validation Logs")

    selected_log_dataset = st.selectbox("Select validation log", list(DATASETS.keys()))
    log_text = load_log(DATASETS[selected_log_dataset]["log"])

    st.markdown(f"### {selected_log_dataset} Log")
    st.code(log_text, language="text")

with tab_ge:
    st.subheader("Great Expectations Data Quality Report")
    st.caption(f"Report path: `{GE_REPORT_PATH}`")

    if GE_REPORT_PATH.exists():
        html = GE_REPORT_PATH.read_text(encoding="utf-8", errors="ignore")
        components.html(html, height=1000, scrolling=True)
    else:
        st.error("Great Expectations Data Docs not found. Run validations first.")
        st.code(str(GE_REPORT_PATH))