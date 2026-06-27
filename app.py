import chardet
import streamlit as st
import pandas as pd
from data_cleaning import clean_data
from ai_suggestions import get_ai_suggestions
from utils import clean_data, generate_cleaning_report

st.set_page_config(page_title="AI Data Cleaning Tool", page_icon="✨", layout="wide")

st.markdown("""
<style>
    .metric-card {
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 0.5px solid rgba(128,128,128,0.2);
        background: rgba(128,128,128,0.05);
    }
    .metric-value {
        font-size: 28px;
        font-weight: 600;
        margin: 0;
    }
    .metric-label {
        font-size: 13px;
        opacity: 0.6;
        margin: 4px 0 0;
    }
    .stButton > button {
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-size: 14px;
    }
    .stDownloadButton > button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 8])
with col1:
    st.markdown("# ✨")
with col2:
    st.markdown("# AI Data Cleaning Tool")
    st.caption("Upload a CSV and let AI do the heavy lifting")

st.divider()

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"], label_visibility="collapsed")

if uploaded_file is not None:
    
    raw = uploaded_file.read()
    encoding = chardet.detect(raw)['encoding']
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file, encoding=encoding)

    missing = int(df.isnull().sum().sum())
    dupes = int(df.duplicated().sum())

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <p class="metric-value">{df.shape[0]:,}</p>
            <p class="metric-label">🗂 Rows</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <p class="metric-value">{df.shape[1]}</p>
            <p class="metric-label">📊 Columns</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        color = "#D85A30" if missing > 0 else "#1D9E75"
        st.markdown(f"""<div class="metric-card">
            <p class="metric-value" style="color:{color}">{missing}</p>
            <p class="metric-label">⚠️ Missing values</p>
        </div>""", unsafe_allow_html=True)
    with c4:
        color = "#BA7517" if dupes > 0 else "#1D9E75"
        st.markdown(f"""<div class="metric-card">
            <p class="metric-value" style="color:{color}">{dupes}</p>
            <p class="metric-label">🔁 Duplicates</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("📄 Original Data", expanded=True):
        st.dataframe(df, use_container_width=True)

    with st.expander("🔍 Missing Values by Column"):
        st.dataframe(df.isnull().sum().reset_index().rename(
            columns={"index": "Column", 0: "Missing Count"}
        ), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ✨ AI Cleaning Suggestions")

    if st.button("Get AI Suggestions", type="primary"):
        with st.spinner("Analyzing your dataset..."):
            suggestions = get_ai_suggestions(df)
            st.success("Suggestions ready!")
            for line in suggestions.split("\n"):
                if line.strip() != "":
                    st.markdown(f"- {line.strip()}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🧹 Clean Data")

    if st.button("Clean Data", type="secondary"):
        with st.spinner("Cleaning your data..."):
            cleaned_df = clean_data(df)

        st.success("Data cleaned successfully!")

        with st.expander("✅ Cleaned Data", expanded=True):
            st.dataframe(cleaned_df, use_container_width=True)

        report = generate_cleaning_report(df, cleaned_df)
        with st.expander("📋 Cleaning Report"):
            st.text(report)

        csv = cleaned_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv",
            type="primary"
        )