import streamlit as st
import pandas as pd
import tabula
import io

# Page Configuration
st.set_page_config(page_title="Professional PDF to Excel", layout="wide")

st.title("📄 PDF to Excel Converter")
st.subheader("High-Accuracy Extraction for Statements & Narrations")

# File Uploader
uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        # Using Tabula to extract tables with high precision
        # stream=True helps in keeping columns aligned correctly
        tables = tabula.read_pdf(uploaded_file, pages='all', multiple_tables=True, stream=True)
        
        if tables:
            # Merging all pages into one single table
            df = pd.concat(tables, ignore_index=True)
            
            # Cleaning: Fixing narration by removing extra line breaks (\r or \n)
            df = df.replace(r'\r+|\n+', ' ', regex=True)
            
            st.success(f"Success! Extracted {len(df)} rows.")
            
            # Displaying the data preview
            st.dataframe
