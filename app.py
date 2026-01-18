import streamlit as st
import pandas as pd
import pdfplumber
import io

st.set_page_config(page_title="Pro Report Converter", layout="wide")

st.title("📊 Enterprise PDF to Excel Converter")
st.write("Using Coordinate-based extraction (Similar to Pro Tools)")

uploaded_file = st.file_uploader("Upload your report PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        all_data = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                # Pro Tools use high 'tolerance' to keep columns aligned
                # This logic mimics high-end reporting tools
                table = page.extract_table(table_settings={
                    "vertical_strategy": "text",
                    "horizontal_strategy": "text",
                    "snap_y_tolerance": 6,
                    "intersection_x_tolerance": 20,
                })
                
                if table:
                    for row in table:
                        # Clean each cell and keep multi-line narration in one cell
                        clean_row = [" ".join(str(cell).split()) if cell else "" for cell in row]
                        # Remove empty or junk rows
                        if any(field.strip() for field in clean_row):
                            all_data.append(clean_row)

        if all_data:
            df = pd.DataFrame(all_data)
            
            # Remove purely empty columns
            df = df.dropna(how='all', axis=1)

            st.success("Analysis Complete!")
            st.dataframe(df, use_container_width=True)

            # Excel Export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
            
            st.download_button(
                label="📥 Download Professional Excel",
                data=output.getvalue(),
                file_name="Report_Export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"System Error: {e}")
