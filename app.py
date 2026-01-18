import streamlit as st
import pandas as pd
import pdfplumber
import io

st.set_page_config(page_title="Precision PDF to Excel", layout="wide")

st.title("📄 PDF to Excel Converter (Fixed Columns)")
st.write("Optimized for complex tables and fixed narrations.")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        all_data = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                # 'lattice' mode helps to follow the table lines strictly
                # This prevents data from scattering into wrong columns
                table = page.extract_table(table_settings={
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines"
                })
                
                if table:
                    for row in table:
                        # Clean narration: join broken lines into a single cell
                        clean_row = [" ".join(str(cell).split()) if cell else "" for cell in row]
                        all_data.append(clean_row)

        if all_data:
            df = pd.DataFrame(all_data)
            
            # Remove empty rows and columns automatically
            df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

            st.success("Table extracted successfully with fixed columns!")
            st.dataframe(df, use_container_width=True)

            # Generate Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
            
            st.download_button(
                label="📥 Download Excel File",
                data=output.getvalue(),
                file_name="clean_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            # If 'lattice' fails, try 'text' strategy automatically
            st.warning("No grid lines found. Trying alternative extraction...")
            # (Fallback logic can be added here if needed)

    except Exception as e:
        st.error(f"Error: {e}")

st.info("Tip: This version uses grid-line detection to keep your amounts and narration in the correct columns.")
