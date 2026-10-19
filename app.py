import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Data Cleaner & Formatter", layout="wide")

st.title("📊 Excel & CSV Data Cleaner")
st.write("Upload your spreadsheet to clean, deduplicate, and export in seconds.")

uploaded_file = st.file_uploader(
    "Choose an Excel (.xlsx, .xls) or CSV file", type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    # Read uploaded file
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    st.subheader("Raw Data Preview")
    st.dataframe(df.head(10))

    st.sidebar.header("Cleaning Options")

    # Option 1: Remove duplicates
    drop_duplicates = st.sidebar.checkbox("Remove duplicate rows", value=True)

    # Option 2: Fill or drop empty rows/values
    handle_na = st.sidebar.selectbox(
        "Handle missing values (NaNs)",
        ["Keep as is", "Drop rows with any missing values", "Fill missing text with 'N/A' and numbers with 0"]
    )

    # Option 3: Clean column names
    clean_cols = st.sidebar.checkbox("Standardize column names (lowercase & snake_case)", value=True)

    # Option 4: Strip whitespace
    strip_spaces = st.sidebar.checkbox("Strip leading/trailing whitespace from text", value=True)

    # Processing logic
    processed_df = df.copy()

    if clean_cols:
        processed_df.columns = (
            processed_df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace(r"[^\w_]", "", regex=True)
        )

    if strip_spaces:
        for col in processed_df.select_dtypes(include="object").columns:
            processed_df[col] = processed_df[col].astype(str).str.strip()

    if drop_duplicates:
        processed_df = processed_df.drop_duplicates()

    if handle_na == "Drop rows with any missing values":
        processed_df = processed_df.dropna()
    elif handle_na == "Fill missing text with 'N/A' and numbers with 0":
        for col in processed_df.columns:
            if processed_df[col].dtype in ["int64", "float64"]:
                processed_df[col] = processed_df[col].fillna(0)
            else:
                processed_df[col] = processed_df[col].fillna("N/A")

    st.subheader("Cleaned Data Preview")
    st.dataframe(processed_df.head(10))

    # Metrics summary
    col1, col2, col3 = st.columns(3)
    col1.metric("Original Rows", len(df))
    col2.metric("Cleaned Rows", len(processed_df))
    col3.metric("Rows Removed", len(df) - len(processed_df))

    # Download Buttons
    st.subheader("Export Clean File")
    download_format = st.radio("Select format:", ["Excel (.xlsx)", "CSV (.csv)"], horizontal=True)

    if download_format == "CSV (.csv)":
        csv_data = processed_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Clean CSV",
            data=csv_data,
            file_name="cleaned_data.csv",
            mime="text/csv",
        )
    else:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            processed_df.to_excel(writer, index=False, sheet_name="CleanData")
        excel_data = output.getvalue()
        st.download_button(
            label="📥 Download Clean Excel",
            data=excel_data,
            file_name="cleaned_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
