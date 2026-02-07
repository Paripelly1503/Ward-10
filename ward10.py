import streamlit as st
import pandas as pd

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(page_title="Ward 10 Voter Search App", layout="wide")

st.title("🗳️ Ward 10 Voter Search App")

# -----------------------------
# LOAD EXCEL
# -----------------------------
EXCEL_FILE = "voters_data.xlsx"

try:
    df = pd.read_excel(EXCEL_FILE)
    st.success("Excel Loaded Successfully")
except Exception as e:
    st.error(f"Error loading Excel: {e}")
    st.stop()

# -----------------------------
# REQUIRED COLUMNS
# -----------------------------
required_columns = [
    "Name",
    "Relation Name",
    "Age",
    "Door No.",
    "Epic"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"Missing columns in Excel: {missing}")
    st.stop()

# Keep only needed columns
df = df[required_columns]

# Convert everything to string (important)
for col in df.columns:
    df[col] = df[col].astype(str)

# -----------------------------
# TOTAL RECORDS
# -----------------------------
st.markdown(f"### Total Records: {len(df)}")

# -----------------------------
# SEARCH BOX
# -----------------------------
query = st.text_input(
    "🔍 Search by Name / Relation Name / Door Number / Epic"
)

# -----------------------------
# FILTER LOGIC
# -----------------------------
if query:

    filtered = df[
        df["Name"].fillna("").str.contains(query, case=False) |
        df["Relation Name"].fillna("").str.contains(query, case=False) |
        df["Door No."].fillna("").str.contains(query, case=False) |
        df["Epic"].fillna("").str.contains(query, case=False)
    ]

    st.markdown(f"### Records Found: {len(filtered)}")

    st.dataframe(filtered, use_container_width=True)

    # Download Button
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered Data",
        csv,
        "ward10_filtered.csv",
        "text/csv"
    )

else:
    st.info("Start typing Name, Relation Name, Door Number or Epic")
