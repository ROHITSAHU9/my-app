import streamlit as st
import pandas as pd
import pdfplumber
import io

st.set_page_config(page_title="No-Java PDF Converter", layout="wide")

st.title("📄 PDF to Excel (Direct Converter)")
st.write("This version works without Java and fixes narration lines.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        all_data = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    for row in table:
                        # Cleaning logic: Removes extra line breaks within a cell
                        # This keeps amounts (8,10,000) and long narrations in one line
                        clean_row = [" ".join(str(cell).split()) if cell else "" for cell in row]
                        all_data.append(clean_row)

        if all_data:
            df = pd.DataFrame(all_data)
            st.success("Extracted Successfully!")
            st.dataframe(df)

            # Creating Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
            
            st.download_button("📥 Download Excel", output.getvalue(), "data.xlsx")
    except Exception as e:
        st.error(f"Error: {e}")
