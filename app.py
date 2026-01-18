import streamlit as st
import pandas as pd
import pdfplumber
import io

st.set_page_config(page_title="PDF Narration Fixer", layout="wide")

st.title("📄 PDF to Excel: Smart Narration Merger")
st.write("This version merges split narration lines into a single cell automatically.")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        raw_rows = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    raw_rows.extend(table)

        if raw_rows:
            final_data = []
            previous_row = None

            for row in raw_rows:
                # Clean the data in each cell
                clean_row = [" ".join(str(cell).split()) if cell else "" for cell in row]
                
                # Check if this is a NEW entry or a CONTINUATION
                # Logic: If the first cell (usually Date/Sr No) is empty, it's a continuation
                if clean_row[0] != "" or previous_row is None:
                    # It's a new entry, save the previous one and start new
                    if previous_row:
                        final_data.append(previous_row)
                    previous_row = clean_row
                else:
                    # It's a continuation! Merge this text into the previous row's cells
                    for i in range(len(clean_row)):
                        if clean_row[i]:
                            # Adding a space and the new text to the existing cell
                            previous_row[i] = (previous_row[i] + " " + clean_row[i]).strip()

            # Don't forget to add the very last row
            if previous_row:
                final_data.append(previous_row)

            # Create DataFrame
            df = pd.DataFrame(final_data)

            st.success("Successfully merged split narrations!")
            st.dataframe(df, use_container_width=True)

            # Excel Export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
            
            st.download_button(
                label="📥 Download Fixed Excel",
                data=output.getvalue(),
                file_name="fixed_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
    except Exception as e:
        st.error(f"Error: {e}")

st.info("How it works: If a line doesn't have a value in the first column, the system assumes it is part of the narration above and merges it.")
