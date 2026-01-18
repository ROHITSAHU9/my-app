import streamlit as st
import pandas as pd
import pdfplumber
import io

# Page settings
st.set_page_config(page_title="PDF to Excel Converter", layout="wide")

st.title("📄 PDF to Excel Converter")
st.write("Upload your PDF to convert it into a clean Excel file.")

# File Uploader
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        all_data = []
        with pdfplumber.open(uploaded_file) as pdf:
            # Process each page
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    for row in table:
                        # NARRATION FIX: This cleans the text and keeps it in one line
                        clean_row = [" ".join(str(cell).split()) if cell else "" for cell in row]
                        all_data.append(clean_row)

        if all_data:
            # Create a Table (DataFrame)
            df = pd.DataFrame(all_data)

            st.success("Extraction Successful!")
            st.dataframe(df) # Preview of your data

            # Excel Download logic
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
            
            # Download Button
            st.download_button(
                label="📥 Download Excel File",
                data=output.getvalue(),
                file_name="converted_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
    except Exception as e:
        st.error(f"Error occurred: {e}")

st.info("Note: Long descriptions will now appear in a single row.")
