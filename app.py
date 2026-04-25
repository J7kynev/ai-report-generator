# app.py
# Streamlit web interface for AI Report Generator

import streamlit as st
import plotly.express as px
import pandas as pd
import os
from src.reader import read_csv, preview
from src.analyzer import analyze
from src.generator import generate_pdf

# Page config
st.set_page_config(
    page_title="AI Report Generator",
    page_icon="📊",
    layout="wide"
)

# Header
st.title("📊 AI Report Generator")
st.markdown("Upload a CSV file to generate an AI-powered business report with insights and PDF export.")
st.divider()

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Save temp file
    temp_path = "data/uploaded.csv"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    # Read data
    df = pd.read_csv(temp_path)
    st.success(f"✅ File loaded — {len(df)} rows, {len(df.columns)} columns")
    st.divider()

    # Data preview
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Data Preview")
        st.dataframe(df, use_container_width=True)

    with col2:
        st.subheader("📈 Quick Charts")
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if len(numeric_cols) >= 2:
            x_col = st.selectbox("X axis", df.columns.tolist())
            y_col = st.selectbox("Y axis", numeric_cols)
            chart_type = st.selectbox("Chart type", ["Bar", "Line", "Scatter"])
            if chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col, color_discrete_sequence=["#6366f1"])
            elif chart_type == "Line":
                fig = px.line(df, x=x_col, y=y_col, color_discrete_sequence=["#6366f1"])
            else:
                fig = px.scatter(df, x=x_col, y=y_col, color_discrete_sequence=["#6366f1"])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add at least 2 numeric columns for charts.")

    st.divider()

    # Analysis
    st.subheader("🤖 AI Analysis")
    context = st.text_input(
        "Describe your data context (optional)",
        placeholder="e.g. monthly sales data for a retail business"
    )

    if st.button("Generate Analysis & Report", type="primary"):
        with st.spinner("Analyzing data with OpenAI..."):
            try:
                data_preview = preview(df)
                analysis = analyze(
                    data_preview,
                    context=context if context else "business data"
                )

                st.success("✅ Analysis complete")
                st.markdown("### 📝 AI Insights")
                st.markdown(analysis)
                st.divider()

                # PDF generation
                with st.spinner("Generating PDF report..."):
                    pdf_path = generate_pdf(analysis)

                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=pdf_file,
                        file_name="ai_business_report.pdf",
                        mime="application/pdf"
                    )

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure your OpenAI API key has available credits.")

else:
    st.info("👆 Upload a CSV file to get started.")