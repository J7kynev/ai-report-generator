# app.py
# Streamlit web interface for AI Report Generator
# Full redesign with professional purple palette and enhanced features

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime
from src.reader import read_csv, preview
from src.analyzer import analyze
from src.generator import generate_pdf

# ─────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────
st.set_page_config(
    page_title="AI Report Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700;800&display=swap');

:root {
    --color-primary:   #6C2DC7;
    --color-secondary: #3B2A6D;
    --color-accent:    #F0DC28;
    --color-bg:        #11121A;
    --color-bg-card:   rgba(17,18,26,0.85);
    --color-bg-hover:  rgba(108,45,199,0.10);
    --color-border:    rgba(109,45,199,0.22);
    --color-text:      #EDEFF6;
    --color-muted:     rgba(237,239,246,0.55);
    --radius-md: 8px; --radius-lg: 12px; --radius-xl: 16px; --radius-full: 9999px;
    --transition: 200ms ease-in-out;
    --shadow-purple: 0 8px 32px rgba(108,45,199,0.25);
}
html, body, .stApp {
    font-family: 'Inter', -apple-system, sans-serif;
    background-color: var(--color-bg) !important;
    color: var(--color-text) !important;
}
::-webkit-scrollbar { width: 7px; }
::-webkit-scrollbar-track { background: #0d0d16; }
::-webkit-scrollbar-thumb { background: var(--color-primary); border-radius: var(--radius-full); }
::-webkit-scrollbar-thumb:hover { background: var(--color-accent); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #130d28 0%, #0f0a1e 100%) !important;
    border-right: 1px solid var(--color-border) !important;
}
[data-testid="stSidebar"] * { color: var(--color-text) !important; }
[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: rgba(108,45,199,0.12) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 12px 16px !important;
    margin-bottom: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: var(--color-accent) !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}
.main .block-container { padding: 2rem 2.5rem !important; max-width: 1200px !important; }
h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-weight: 700 !important;
    color: var(--color-text) !important;
    line-height: 1.2 !important;
}
h1 { font-size: clamp(1.8rem,3vw,2.4rem) !important; }
h2 { font-size: clamp(1.3rem,2.5vw,1.7rem) !important; }
.stButton > button {
    border-radius: var(--radius-lg) !important;
    font-weight: 600 !important;
    transition: all var(--transition) !important;
}
button[kind="primary"], [data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary)) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(108,45,199,0.30) !important;
}
button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: var(--shadow-purple) !important; }
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: rgba(17,18,26,0.60) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--color-text) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--color-accent) !important;
    box-shadow: 0 0 0 3px rgba(240,220,40,0.12) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label,
.stCheckbox label, .stSlider label {
    color: var(--color-text) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}
[data-testid="stMetric"] {
    background: var(--color-bg-card) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-xl) !important;
    padding: 20px 24px !important;
    transition: border-color var(--transition) !important;
}
[data-testid="stMetric"]:hover { border-color: rgba(108,45,199,0.50) !important; }
[data-testid="stMetricLabel"] {
    color: var(--color-muted) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
[data-testid="stMetricValue"] { color: var(--color-accent) !important; font-size: 1.9rem !important; font-weight: 700 !important; }
[data-testid="stDataFrame"] { border: 1px solid var(--color-border) !important; border-radius: var(--radius-xl) !important; overflow: hidden !important; }
[data-testid="stFileUploader"] {
    background: var(--color-bg-card) !important;
    border: 2px dashed var(--color-border) !important;
    border-radius: var(--radius-xl) !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--color-primary) !important; }
[data-testid="stDownloadButton"] > button {
    background: rgba(108,45,199,0.15) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-lg) !important;
    color: var(--color-text) !important;
    font-weight: 600 !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(108,45,199,0.28) !important;
    border-color: var(--color-primary) !important;
    color: var(--color-accent) !important;
}
.stSuccess { background: rgba(16,185,129,0.12) !important; border-left: 4px solid #10B981 !important; border-radius: var(--radius-md) !important; }
.stError   { background: rgba(239,68,68,0.10)  !important; border-left: 4px solid #EF4444 !important; border-radius: var(--radius-md) !important; }
.stInfo    { background: rgba(108,45,199,0.12) !important; border-left: 4px solid var(--color-primary) !important; border-radius: var(--radius-md) !important; }
.stWarning { background: rgba(245,158,11,0.12) !important; border-left: 4px solid #F59E0B !important; border-radius: var(--radius-md) !important; }
hr { border-color: var(--color-border) !important; margin: 1.5rem 0 !important; }
.stProgress > div > div { background: linear-gradient(90deg, var(--color-primary), var(--color-accent)) !important; border-radius: var(--radius-full) !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
</style>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────
if "report_history" not in st.session_state:
    st.session_state.report_history = []
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None
if "current_df" not in st.session_state:
    st.session_state.current_df = None
if "report_count" not in st.session_state:
    st.session_state.report_count = 0
if "total_rows_processed" not in st.session_state:
    st.session_state.total_rows_processed = 0

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/bar-chart.png", width=55)
st.sidebar.title("AI Report Generator")
st.sidebar.markdown("*Transform raw data into professional AI-powered reports*")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    ["📊 Generate Report", "📈 Data Explorer", "📋 Report History", "⚙️ Settings"],
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.markdown("**Session Stats**")
st.sidebar.metric("Reports Generated", st.session_state.report_count)
st.sidebar.metric("Rows Processed", st.session_state.total_rows_processed)

if st.session_state.report_history:
    st.sidebar.divider()
    st.sidebar.markdown("**Recent Reports**")
    for i, report in enumerate(reversed(st.session_state.report_history[-3:])):
        st.sidebar.markdown(f"📄 `{report['filename']}` — {report['rows']} rows")

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────
def render_data_quality(df: pd.DataFrame):
    """Render a data quality summary panel with metrics and warnings."""
    total_cells = df.shape[0] * df.shape[1]
    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()
    completeness = round((1 - missing / total_cells) * 100, 1) if total_cells > 0 else 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{df.shape[0]:,}")
    col2.metric("Columns", df.shape[1])
    col3.metric("Completeness", f"{completeness}%")
    col4.metric("Duplicates", duplicates)

    if missing > 0:
        st.warning(f"⚠️ {missing} missing values detected across {df.isnull().any().sum()} columns. The AI will account for gaps in its analysis.")
    if duplicates > 0:
        st.warning(f"⚠️ {duplicates} duplicate rows detected. Consider cleaning your data before generating the report.")
    if completeness == 100 and duplicates == 0:
        st.success("✅ Data quality check passed — no missing values or duplicates found.")


def render_column_summary(df: pd.DataFrame):
    """Render a detailed column-by-column summary with types and sample values."""
    summary_data = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].notna().sum()
        unique = df[col].nunique()
        sample = str(df[col].dropna().iloc[0]) if non_null > 0 else "N/A"
        if len(sample) > 30:
            sample = sample[:30] + "..."
        summary_data.append({
            "Column": col,
            "Type": dtype,
            "Non-Null": f"{non_null}/{len(df)}",
            "Unique Values": unique,
            "Sample": sample
        })
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True)


def render_auto_charts(df: pd.DataFrame):
    """Automatically generate the most relevant charts based on column types."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    date_cols = [c for c in df.columns if "date" in c.lower() or "time" in c.lower()]

    charts_rendered = 0

    if len(numeric_cols) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📊 Correlation Heatmap**")
            corr = df[numeric_cols].corr()
            fig = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns.tolist(),
                y=corr.columns.tolist(),
                colorscale=[[0, "#0f0a1e"], [0.5, "#6C2DC7"], [1, "#F0DC28"]],
                text=corr.round(2).values,
                texttemplate="%{text}",
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#EDEFF6"),
                margin=dict(l=0, r=0, t=20, b=0),
            )
            st.plotly_chart(fig, use_container_width=True)
            charts_rendered += 1

        with col2:
            st.markdown(f"**📈 Distribution: {numeric_cols[0]}**")
            fig = px.histogram(
                df, x=numeric_cols[0], nbins=20,
                color_discrete_sequence=["#6C2DC7"],
                title=""
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#EDEFF6"),
                xaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                yaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                margin=dict(l=0, r=0, t=20, b=0),
            )
            st.plotly_chart(fig, use_container_width=True)
            charts_rendered += 1

    if date_cols and numeric_cols:
        st.markdown(f"**📉 Trend: {numeric_cols[0]} over {date_cols[0]}**")
        try:
            df_sorted = df.copy()
            df_sorted[date_cols[0]] = pd.to_datetime(df_sorted[date_cols[0]])
            df_sorted = df_sorted.sort_values(date_cols[0])
            fig = px.line(
                df_sorted, x=date_cols[0], y=numeric_cols[0],
                color_discrete_sequence=["#F0DC28"],
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#EDEFF6"),
                xaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                yaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                margin=dict(l=0, r=0, t=20, b=0),
            )
            st.plotly_chart(fig, use_container_width=True)
            charts_rendered += 1
        except Exception:
            pass

    if categorical_cols and numeric_cols:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**🥧 Breakdown by {categorical_cols[0]}**")
            try:
                top_cats = df[categorical_cols[0]].value_counts().head(8)
                fig = px.pie(
                    values=top_cats.values,
                    names=top_cats.index,
                    color_discrete_sequence=["#6C2DC7","#8B47E8","#3B2A6D","#F0DC28","#9D6FFF","#130d28","#F5E75C","#1a0f35"],
                    hole=0.4,
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#EDEFF6"),
                    margin=dict(l=0, r=0, t=20, b=0),
                    legend=dict(font=dict(color="#EDEFF6")),
                )
                st.plotly_chart(fig, use_container_width=True)
                charts_rendered += 1
            except Exception:
                pass

        with col2:
            st.markdown(f"**📊 {numeric_cols[0]} by {categorical_cols[0]}**")
            try:
                agg = df.groupby(categorical_cols[0])[numeric_cols[0]].mean().sort_values(ascending=False).head(10)
                fig = px.bar(
                    x=agg.index, y=agg.values,
                    color=agg.values,
                    color_continuous_scale=["#3B2A6D", "#6C2DC7", "#F0DC28"],
                    labels={"x": categorical_cols[0], "y": f"Avg {numeric_cols[0]}"},
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#EDEFF6"),
                    xaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                    yaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                    margin=dict(l=0, r=0, t=20, b=0),
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)
                charts_rendered += 1
            except Exception:
                pass

    if charts_rendered == 0:
        st.info("No numeric columns detected for automatic chart generation. Upload a dataset with numeric data to enable visualizations.")


def render_numeric_summary(df: pd.DataFrame):
    """Render descriptive statistics for all numeric columns."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        st.info("No numeric columns found in this dataset.")
        return
    desc = df[numeric_cols].describe().round(2)
    st.dataframe(desc, use_container_width=True)


# ─────────────────────────────────────────
# PAGE: GENERATE REPORT
# ─────────────────────────────────────────
if page == "📊 Generate Report":
    st.title("📊 AI Report Generator")
    st.markdown("Upload a CSV file to generate an AI-powered business report with visualizations, insights, and a downloadable PDF.")
    st.divider()

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        temp_path = "data/uploaded.csv"
        os.makedirs("data", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        try:
            df = pd.read_csv(temp_path, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(temp_path, encoding="latin-1")

        st.session_state.current_df = df
        st.session_state.total_rows_processed += len(df)

        st.success(f"✅ **{uploaded_file.name}** loaded successfully — {len(df):,} rows, {len(df.columns)} columns.")
        st.divider()

        # Data quality
        st.subheader("🔍 Data Quality Check")
        render_data_quality(df)
        st.divider()

        # Preview and charts
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)

        with col2:
            st.subheader("📈 Quick Charts")
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if len(numeric_cols) >= 2:
                x_col = st.selectbox("X axis", df.columns.tolist(), key="quick_x")
                y_col = st.selectbox("Y axis", numeric_cols, key="quick_y")
                chart_type = st.selectbox("Chart type", ["Bar", "Line", "Scatter", "Area"], key="quick_chart")

                if chart_type == "Bar":
                    fig = px.bar(df, x=x_col, y=y_col, color_discrete_sequence=["#6C2DC7"])
                elif chart_type == "Line":
                    fig = px.line(df, x=x_col, y=y_col, color_discrete_sequence=["#F0DC28"])
                elif chart_type == "Scatter":
                    fig = px.scatter(df, x=x_col, y=y_col, color_discrete_sequence=["#9D6FFF"])
                else:
                    fig = px.area(df, x=x_col, y=y_col, color_discrete_sequence=["#6C2DC7"])

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#EDEFF6"),
                    xaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                    yaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                    margin=dict(l=0, r=0, t=20, b=0),
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Add at least 2 numeric columns to enable chart selection.")

        st.divider()

        # Auto charts
        st.subheader("🤖 Automatic Visualizations")
        st.markdown("Charts generated automatically based on your data structure.")
        render_auto_charts(df)
        st.divider()

        # Analysis configuration
        st.subheader("⚙️ Report Configuration")
        col1, col2 = st.columns(2)
        with col1:
            context = st.text_input(
                "Data context",
                placeholder="e.g. monthly sales data for a retail business in Chile",
                help="Describe what your data represents to improve AI accuracy."
            )
            report_title = st.text_input(
                "Report title",
                placeholder="e.g. Q1 2025 Sales Performance Report",
            )
        with col2:
            analysis_depth = st.selectbox(
                "Analysis depth",
                ["Standard — key insights and recommendations",
                 "Detailed — deep dive with trend analysis",
                 "Executive — high-level summary for stakeholders"]
            )
            include_charts = st.checkbox("Include chart descriptions in PDF", value=True)

        if st.button("🚀 Generate Analysis & Report", type="primary", use_container_width=True):
            with st.status("🤖 Analyzing data with GPT-4o...", expanded=True) as status:
                st.write("Preparing data preview for AI analysis...")
                data_preview = preview(df)
                depth_instruction = {
                    "Standard — key insights and recommendations": "Provide a standard analysis with key insights and 2-3 actionable recommendations.",
                    "Detailed — deep dive with trend analysis": "Provide a detailed analysis including trend identification, anomalies, and 5+ specific recommendations.",
                    "Executive — high-level summary for stakeholders": "Provide a concise executive summary suitable for C-level stakeholders, focusing on business impact and strategic recommendations."
                }.get(analysis_depth, "")

                full_context = f"{context} — {depth_instruction}" if context else depth_instruction

                st.write("Sending data to GPT-4o for analysis...")
                try:
                    analysis = analyze(data_preview, context=full_context or "business data")
                    st.session_state.current_analysis = analysis
                    status.update(label="✅ Analysis complete", state="complete")
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                    st.info("Ensure your OpenAI API key has available credits.")
                    st.stop()

            st.divider()
            st.subheader("📝 AI Insights")

            col1, col2, col3 = st.columns(3)
            col1.metric("Data Rows", f"{len(df):,}")
            col2.metric("Columns", len(df.columns))
            col3.metric("Analysis Depth", analysis_depth.split("—")[0].strip())

            st.markdown(analysis)
            st.divider()

            with st.status("📄 Generating PDF report...", expanded=True) as status:
                st.write("Building professional PDF layout...")
                try:
                    final_title = report_title if report_title else f"AI Business Report — {datetime.now().strftime('%B %d, %Y')}"
                    pdf_path = generate_pdf(analysis, filename=f"outputs/{final_title.replace(' ', '_')[:40]}.pdf")
                    status.update(label="✅ PDF generated", state="complete")

                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="⬇️ Download PDF Report",
                            data=pdf_file,
                            file_name=f"{final_title}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )

                    st.session_state.report_count += 1
                    st.session_state.report_history.append({
                        "filename": uploaded_file.name,
                        "title": final_title,
                        "rows": len(df),
                        "columns": len(df.columns),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "analysis": analysis,
                    })
                    st.success(f"✅ Report **{final_title}** saved successfully.")

                except Exception as e:
                    st.error(f"PDF generation failed: {str(e)}")
    else:
        st.markdown("""
        <div style="
            background: rgba(108,45,199,0.08);
            border: 2px dashed rgba(109,45,199,0.35);
            border-radius: 16px;
            padding: 48px 32px;
            text-align: center;
            margin-top: 16px;
        ">
            <div style="font-size: 3rem; margin-bottom: 16px;">📂</div>
            <h3 style="color: #EDEFF6; margin-bottom: 8px;">Upload your CSV file to get started</h3>
            <p style="color: rgba(237,239,246,0.55); font-size: 0.95rem;">
                Supported format: CSV · Max size: 200MB<br>
                The AI will automatically analyze your data and generate a professional PDF report.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# PAGE: DATA EXPLORER
# ─────────────────────────────────────────
elif page == "📈 Data Explorer":
    st.title("📈 Data Explorer")
    st.markdown("Deep dive into your dataset with interactive visualizations and statistical summaries.")
    st.divider()

    if st.session_state.current_df is None:
        st.info("No dataset loaded. Go to **Generate Report** and upload a CSV file first.")
    else:
        df = st.session_state.current_df

        tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "📊 Statistics", "🔍 Column Detail", "🔗 Relationships"])

        with tab1:
            st.subheader("Dataset Overview")
            render_data_quality(df)
            st.divider()
            st.subheader("Column Summary")
            render_column_summary(df)

        with tab2:
            st.subheader("Descriptive Statistics")
            render_numeric_summary(df)
            st.divider()
            st.subheader("Automatic Visualizations")
            render_auto_charts(df)

        with tab3:
            st.subheader("Column Deep Dive")
            col_selected = st.selectbox("Select a column to analyze", df.columns.tolist())
            if col_selected:
                col_data = df[col_selected]
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Non-Null", col_data.notna().sum())
                c2.metric("Null", col_data.isnull().sum())
                c3.metric("Unique", col_data.nunique())
                c4.metric("Type", str(col_data.dtype))

                if col_data.dtype in ["int64", "float64"]:
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Min", round(col_data.min(), 2))
                    c2.metric("Max", round(col_data.max(), 2))
                    c3.metric("Mean", round(col_data.mean(), 2))
                    c4.metric("Std Dev", round(col_data.std(), 2))
                    st.divider()
                    fig = px.histogram(df, x=col_selected, nbins=25, color_discrete_sequence=["#6C2DC7"])
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#EDEFF6"),
                        xaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                        yaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    top_values = col_data.value_counts().head(15)
                    fig = px.bar(
                        x=top_values.index, y=top_values.values,
                        color=top_values.values,
                        color_continuous_scale=["#3B2A6D","#6C2DC7","#F0DC28"],
                        labels={"x": col_selected, "y": "Count"},
                    )
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#EDEFF6"),
                        xaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                        yaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                        showlegend=False,
                    )
                    st.plotly_chart(fig, use_container_width=True)

        with tab4:
            st.subheader("Column Relationships")
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if len(numeric_cols) < 2:
                st.info("At least 2 numeric columns are required to explore relationships.")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    x_rel = st.selectbox("X axis", numeric_cols, key="rel_x")
                with col2:
                    y_rel = st.selectbox("Y axis", numeric_cols, index=min(1, len(numeric_cols)-1), key="rel_y")

                fig = px.scatter(
                    df, x=x_rel, y=y_rel,
                    trendline="ols",
                    color_discrete_sequence=["#9D6FFF"],
                    title=f"{x_rel} vs {y_rel}",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#EDEFF6"),
                    xaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                    yaxis=dict(gridcolor="rgba(109,45,199,0.15)"),
                )
                st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────
# PAGE: REPORT HISTORY
# ─────────────────────────────────────────
elif page == "📋 Report History":
    st.title("📋 Report History")
    st.markdown("Review all reports generated in this session.")
    st.divider()

    if not st.session_state.report_history:
        st.info("No reports generated yet in this session. Go to **Generate Report** to create your first report.")
    else:
        st.success(f"✅ {len(st.session_state.report_history)} report(s) generated this session.")
        for i, report in enumerate(reversed(st.session_state.report_history)):
            with st.expander(f"📄 {report['title']} — {report['timestamp']}"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Source File", report["filename"])
                col2.metric("Rows", f"{report['rows']:,}")
                col3.metric("Columns", report["columns"])
                st.divider()
                st.markdown("**AI Analysis:**")
                st.markdown(report["analysis"])

# ─────────────────────────────────────────
# PAGE: SETTINGS
# ─────────────────────────────────────────
elif page == "⚙️ Settings":
    st.title("⚙️ Settings & Configuration")
    st.divider()

    st.subheader("🤖 OpenAI Configuration")
    st.markdown("The system uses GPT-4o for data analysis. Ensure your API key is configured in the `.env` file.")
    api_status = "✅ Configured" if os.getenv("OPENAI_API_KEY") else "❌ Not configured"
    st.info(f"API Key Status: **{api_status}**")

    st.divider()
    st.subheader("📁 Output Directory")
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_files = [f for f in os.listdir(output_dir) if f.endswith(".pdf")]
    st.metric("PDF Reports Saved", len(output_files))
    if output_files:
        st.markdown("**Saved reports:**")
        for f in sorted(output_files, reverse=True)[:10]:
            filepath = os.path.join(output_dir, f)
            size_kb = round(os.path.getsize(filepath) / 1024, 1)
            col1, col2 = st.columns([3, 1])
            col1.markdown(f"📄 `{f}` — {size_kb} KB")
            with col2:
                with open(filepath, "rb") as pdf:
                    st.download_button(
                        label="⬇️",
                        data=pdf,
                        file_name=f,
                        mime="application/pdf",
                        key=f"dl_{f}"
                    )

    st.divider()
    st.subheader("🗑️ Clear Session")
    if st.button("Clear session data", type="secondary"):
        st.session_state.report_history = []
        st.session_state.current_analysis = None
        st.session_state.current_df = None
        st.session_state.report_count = 0
        st.session_state.total_rows_processed = 0
        st.success("Session data cleared.")
        st.rerun()

    st.divider()
    st.subheader("ℹ️ About")
    st.markdown("""
    **AI Report Generator** — Built by J7kynev

    This tool transforms raw CSV data into professional AI-powered business reports using GPT-4o.
    It automatically performs data quality checks, generates interactive visualizations, and
    produces a downloadable PDF with actionable insights tailored to your business context.

    **Stack:** Python · Streamlit · OpenAI GPT-4o · ReportLab · Plotly · Pandas
    """)