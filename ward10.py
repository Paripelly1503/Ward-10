import streamlit as st
import pandas as pd

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(page_title="Ward 10 Voter Search", layout="wide")
st.title("🗳️ Ward 10 Voter Search App")

# ---------------------------
# LOAD EXCEL
# ---------------------------
FILE_PATH = "voters_data.xlsx"

try:
    df = pd.read_excel(FILE_PATH)
    st.success("Excel Loaded Successfully")
except:
    st.error("Cannot load Excel file")
    st.stop()

# ---------------------------
# CLEAN COLUMN NAMES
# ---------------------------
df.columns = df.columns.str.strip().str.lower()

# ---------------------------
# COLUMN MAPPING
# ---------------------------
column_map = {}

for col in df.columns:

    c = col.lower()

    if "name" == c:
        column_map[col] = "Name"

    elif "relation" in c:
        column_map[col] = "Relation Name"

    elif "age" in c:
        column_map[col] = "Age"

    elif "door" in c:
        column_map[col] = "Door No."

    elif "epic" in c or "voter" in c or "elector" in c:
        column_map[col] = "Epic"

df = df.rename(columns=column_map)

# ---------------------------
# REQUIRED COLUMNS CHECK
# ---------------------------
needed = ["Name", "Relation Name", "Age", "Door No.", "Epic"]

missing = [c for c in needed if c not in df.columns]
if missing:
    st.error(f"Missing columns in Excel: {missing}")
    st.stop()

df = df[needed]

# Convert all to string
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
query = st.text_input(
    "🔍 Search by Name / Relation Name / Door Number / Epic"
)

# ---------------------------
# FILTER
# ---------------------------
if query:

    mask = (
        df["Name"].str.contains(query, case=False) |
        df["Relation Name"].str.contains(query, case=False) |
        df["Door No."].str.contains(query, case=False) |
        df["Epic"].str.contains(query, case=False)
    )

    result = df[mask]

    st.success(f"{len(result)} Records Found")
    st.dataframe(result, use_container_width=True)

else:
    st.info("👆 Start typing Name / Door Number / Epic")
