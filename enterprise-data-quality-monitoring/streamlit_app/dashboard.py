import streamlit as st
import os

# Define the path to the GE HTML report
ge_report_path = "/content/drive/MyDrive/data_governance_project/great_expectations/uncommitted/data_docs/local_site/index.html"

st.set_page_config(layout="wide")
st.title("📊 Great Expectations Data Quality Report")

# Check if file exists
if os.path.exists(ge_report_path):
    # Load and display the HTML report
    with open(ge_report_path, "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=1000, scrolling=True)
else:
    st.error("❌ Data Docs not found. Please validate first and check the path.")
