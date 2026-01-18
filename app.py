import streamlit as st
import pandas as pd
import pdfplumber
import io

st.set_page_config(page_title="Accurate PDF to Excel", layout="wide")

st.title("📊 Precision PDF to Excel Converter")
st.markdown("### Perfect for Financial Statements & Large Amounts")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        all_data = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                # 'stream' mode is better for PDFs without visible grid lines
                table = page.extract_table({
                    "table_regions": None,
                    "row_tol": 10,
                    "join_tolerance": 3
                })
                
                if table:
                    for row in table:
                        # Clean: Removes extra enters and keeps amounts clean
                        clean_row = [" ".join(str(cell).split()) if cell else "" for cell in row]
                        all_data.append(clean_row)

        if all_data:
            # Create Table
            df = pd.DataFrame(all_data)
            
            # Remove empty columns or rows
            df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
            
            st.success("Data extracted! Please check the preview below:")
            st.dataframe(df, use_container_width=True)

            # High Quality Excel Export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False, sheet_name='Sheet1')
            
            st.download_button(
                label="📥 Download Corrected Excel File",
                data=output.getvalue(),
                file_name="fixed_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("Could not find any data. Try a different PDF.")
            
    except Exception as e:
        st.error(f"Error: {e}")
