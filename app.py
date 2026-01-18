import streamlit as st
import tabula
import pandas as pd
from io import BytesIO

st.title("PDF to Excel Converter")
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    try:
        tables = tabula.read_pdf(uploaded_file, pages='all', multiple_tables=True, lattice=True)
        if tables:
            df = pd.concat(tables, ignore_index=True)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button(label="Download Excel File", data=output.getvalue(), file_name="converted.xlsx")
    except:
        st.error("Error! Please try another PDF.")
