import streamlit as st
import pandas as pd
import pdfplumber
import io

st.set_page_config(page_title="PDF to Excel Converter", layout="wide")

st.title("📄 PDF to Excel Converter")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        all_data = []
        with pdfplumber.open(uploaded_file) as pdf:
            # हर पेज से डाटा निकालना
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    for row in table:
                        # नरेशन फिक्स: यह लाइन सेल के अंदर के 'Enter' को हटाकर उसे एक लाइन में कर देगी
                        clean_row = [" ".join(str(cell).split()) if cell else "" for cell in row]
                        all_data.append(clean_row)

        if all_data:
            # डाटाफ्रेम बनाना
            df = pd.DataFrame(all_data)

            st.success("Success! Data extracted.")
            st.dataframe(df)

            # Excel डाउनलोड बटन
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
            
            st.download_button(
                label="📥 Download Excel File",
                data=output.getvalue(),
                file_name="converted_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
    except Exception as e:
        st.error(f"Error: {e}")
