import streamlit as st
import pandas as pd
import pdfplumber
import io

st.set_page_config(page_title="Professional PDF to Excel", layout="wide")

st.title("📄 Professional PDF to Excel Converter")
st.subheader("High-Quality Extraction (Single-line Narration)")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        all_pages_data = []
        
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                # 'lattice' mode is better for clear grid lines
                table = page.extract_table({
                    "vertical_strategy": "lines", 
                    "horizontal_strategy": "lines",
                    "snap_tolerance": 3,
                })
                
                if table:
                    for row in table:
                        # Clean each cell: remove None and fix broken lines (Narration fix)
                        cleaned_row = [str(cell).replace('\n', ' ').strip() if cell else "" for cell in row]
                        all_pages_data.append(cleaned_row)

            if all_pages_data:
                # Convert to DataFrame
                df = pd.DataFrame(all_pages_data[1:], columns=all_pages_data[0])
                
                # Show on screen
                st.success(f"Successfully extracted {len(all_pages_data)} rows!")
                st.dataframe(df)

                # Export to Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Data')
                
                processed_data = output.getvalue()

                st.download_button(
                    label="📥 Download Clean Excel File",
                    data=processed_data,
                    file_name="clean_converted_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("No table structure found. Please check your PDF quality.")

    except Exception as e:
        st.error(f"Error: {e}")

st.info("Tip: This code automatically joins broken narration lines into a single line for better Excel reporting.")
