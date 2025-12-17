
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
import duckdb
from datetime import datetime
import re

st.set_page_config(
    page_title="InsightPilot - Professional Data Analytics Platform",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #1E1B4B 0%, #0F172A 100%);
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
}
.main-header h1 {
    color: #14F1C5;
    font-size: 2.4rem;
    margin: 0;
}
.main-header p {
    color: #E5E7EB;
}
.stButton>button {
    background: #14F1C5;
    color: #0F172A;
    border-radius: 8px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🧭 InsightPilot</h1>
    <p>Professional Data Analytics Automation Platform</p>
</div>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state.data = None
if 'cleaned_data' not in st.session_state:
    st.session_state.cleaned_data = None

st.sidebar.title("InsightPilot")
page = st.sidebar.radio("Navigation", ["Upload Data", "EDA", "SQL", "Reports"])

if page == "Upload Data":
    file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    if file:
        if file.name.endswith("csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        st.session_state.data = df
        st.success("File uploaded successfully")
        st.dataframe(df.head())

elif page == "EDA":
    if st.session_state.data is None:
        st.warning("Upload data first")
    else:
        df = st.session_state.data
        st.write(df.describe())
        num_cols = df.select_dtypes(include=np.number).columns
        if len(num_cols) > 0:
            fig = px.histogram(df, x=num_cols[0], color_discrete_sequence=["#14F1C5"])
            st.plotly_chart(fig, use_container_width=True)

elif page == "SQL":
    if st.session_state.data is None:
        st.warning("Upload data first")
    else:
        df = st.session_state.data
        conn = duckdb.connect()
        conn.register("data", df)
        q = st.text_area("Ask a question")
        if st.button("Run Query"):
            sql = "SELECT * FROM data LIMIT 10"
            if "count" in q.lower():
                sql = "SELECT COUNT(*) FROM data"
            res = conn.execute(sql).fetchdf()
            st.code(sql, language="sql")
            st.dataframe(res)

elif page == "Reports":
    if st.session_state.data is None:
        st.warning("Upload data first")
    else:
        df = st.session_state.data
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df.to_excel(w, index=False)
        st.download_button(
            "Download Excel Report",
            data=buf.getvalue(),
            file_name=f"InsightPilot_Report_{datetime.now().strftime('%Y%m%d')}.xlsx"
        )
