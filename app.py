import streamlit as st
import pandas as pd
from data_cleaning import clean_data
from ai_suggestions import get_ai_suggestions
from utils import clean_data, generate_cleaning_report

st.title("AI Data Cleaning Tool")

# Upload file
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Original Data")
    st.dataframe(df)

    # Data Summary
    st.subheader("Dataset Summary")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    # Missing Values
    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    # Duplicate Rows
    st.subheader("Duplicate Rows")
    st.write(df.duplicated().sum())

    # AI Suggestions - Button ke peeche
    st.subheader("AI Cleaning Suggestions")
    if st.button("Get AI Suggestions"):
        with st.spinner("Generating suggestions..."):
            suggestions = get_ai_suggestions(df)
            for line in suggestions.split("\n"):
                if line.strip() != "":
                    st.write("•", line)

    # Clean Data Button
    if st.button("Clean Data"):
        cleaned_df = clean_data(df)

        st.subheader("Cleaned Data")
        st.dataframe(cleaned_df)

        report = generate_cleaning_report(df, cleaned_df)

        st.subheader("Cleaning Report")
        st.text(report)

        csv = cleaned_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv",
        )