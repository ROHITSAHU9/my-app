import streamlit as st
import pandas as pd
import pdfplumber
import io

st.set_page_config(page_title="Simple PDF Converter", layout="wide")

st.title("📄 PDF to Excel Converter")
st.write("Fixed: No more Table-Setting errors")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        all_rows = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                # Sabse simple method bina kisi extra settings ke
                table = page.extract_table()
                if table:
                    for row in table:
                        # Har cell ko clean karega aur narration ko ek line mein layega
                        clean_row = []
                        for cell in row:
                            if cell:
                                # New lines hatakar single space dega
                                clean_val = " ".join(str(cell).split())
                                clean_row.append(clean_val)
                            else:
                                clean_row.append("")
                        all_rows.append(clean_row)

        if all_rows:
            df = pd.DataFrame(all_rows)
            st.success("Success! Data Extracted.")
            st.dataframe(df)

            # Excel download logic
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
            
            st.download_button(
                label="📥 Download Excel File",
                data=output.getvalue(),
                file_name="converted_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No data found in PDF.")
            
    except Exception as e:
        st.error(f"Error: {e}")
