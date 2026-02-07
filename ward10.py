import streamlit as st
import pandas as pd

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Ward 10 Voter Search", layout="wide")

st.title("🗳️ Ward 10 Voter Search App")

# ---------------------------
# LOAD EXCEL
# ---------------------------
FILE_PATH = "voters_data.xlsx"   # Excel must be in same GitHub folder

try:
    df = pd.read_excel(FILE_PATH)
    st.success("Excel Loaded Successfully")
except Exception as e:
    st.error("Unable to load Excel file")
    st.stop()

# ---------------------------
# KEEP ONLY REQUIRED COLUMNS
# ---------------------------
required_columns = [
    "Name",
    "Relation Name",
    "Age",
    "Door No.",
    "Epic"
]

df = df[required_columns]

# Convert everything to string for safe searching
for col in df.columns:
    df[col] = df[col].astype(str)

# ---------------------------
# TOTAL RECORDS
# ---------------------------
st.markdown(f"### Total Records: {len(df)}")

st.divider()

# ---------------------------
# SEARCH BOX
# ---------------------------
search = st.text_input(
    "🔍 Search by Name / Relation Name / Door Number / Epic"
)

# ---------------------------
# FILTER LOGIC
# ---------------------------
if search:

    mask = (
        df["Name"].str.contains(search, case=False, na=False) |
        df["Relation Name"].str.contains(search, case=False, na=False) |
        df["Door No."].str.contains(search, case=False, na=False) |
        df["Epic"].str.contains(search, case=False, na=False)
    )

    filtered = df[mask]

    st.success(f"{len(filtered)} Records Found")

    st.dataframe(filtered, use_container_width=True)

else:
    st.info("👆 Start typing Name / Door Number / Epic to search")
