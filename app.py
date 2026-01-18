import streamlit as st
import pandas as pd
import pdfplumber
import io

st.set_page_config(page_title="Professional PDF Fixer", layout="wide")

st.title("📊 Precision PDF to Excel Converter")
st.write("Fixed: Narration Merging Logic (One row per entry)")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        raw_data = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    raw_data.extend(table)

        if raw_data:
            final_rows = []
            current_row = None

            for row in raw_data:
                # Clean the cells
                clean_row = [str(cell).strip() if cell else "" for cell in row]
                
                # मान लीजिये पहला कॉलम 'Date' या 'ID' है। 
                # अगर पहली सेल खाली नहीं है, तो यह एक नई एंट्री है।
                if clean_row[0] != "": 
                    if current_row:
                        final_rows.append(current_row)
                    current_row = clean_row
                else:
                    # अगर पहली सेल खाली है, तो यह ऊपर वाली एंट्री की बची हुई नरेशन है।
                    if current_row:
                        for i in range(len(clean_row)):
                            if clean_row[i]:
                                current_row[i] = current_row[i] + " " + clean_row[i]
            
            # आखिरी रो को जोड़ें
            if current_row:
                final_rows.append(current_row)

            df = pd.DataFrame(final_rows)
            
            st.success("Narration Merged Successfully!")
            st.dataframe(df, use_container_width=True)

            # Excel Export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
            
            st.download_button(
                label="📥 Download Clean Excel",
                data=output.getvalue(),
                file_name="merged_narration.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"Error: {e}")
