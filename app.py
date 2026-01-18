import streamlit as st
import pandas as pd
import pdfplumber
import io

# Page setup for a professional look
st.set_page_config(page_title="PDF to Excel Pro", layout="wide")

st.title("📄 Professional PDF to Excel Converter")
st.write("Optimized to prevent data scattering and fix broken narration lines.")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        all_data = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                # Advanced table extraction settings to keep columns aligned
                table = page.extract_table(table_settings={
                    "vertical_strategy": "text",      # Aligns columns based on text position
                    "horizontal_strategy": "text",    # Aligns rows based on text position
                    "snap_y_tolerance": 4,           # Keeps narration in the same row
                    "intersection_x_tolerance": 15    # Prevents amounts from mixing with text
                })
                
                if table:
                    for row in table:
                        # CLEANING: Joins multi-line narration and removes extra spaces
                        clean_row = [" ".join(str(cell).split()) if cell else "" for cell in row]
                        
                        # Only add rows that are not completely empty
                        if any(field.strip() for field in clean_row):
                            all_data.append(clean_row)

        if all_data:
            df = pd.DataFrame(all_data)
            
            # Auto-remove empty columns that might have been created during extraction
            df = df.dropna(how='all', axis=1)

            st.success("Extraction Successful! Review your data below.")
            st.dataframe(df, use_container_width=True)

            # Convert the final table to Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
            
            st.download_button(
                label="📥 Download Clean Excel File",
                data=output.getvalue(),
                file_name="Converted_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No data found. Please ensure the PDF contains a text-based table.")

    except Exception as e:
        st.error(f"Error: {e}")

st.info("System Tip: This version uses 'Text-Based Strategy' which is best for PDFs without visible grid lines.")
