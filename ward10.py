import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ward 10 Voter Search App", layout="wide")

st.title("🗳️ Ward 10 Voter Search App")

# -----------------------
# LOAD EXCEL
# -----------------------
FILE = "voters_data.xlsx"

try:
    df = pd.read_excel(FILE)
    st.success("Excel Loaded Successfully")
except Exception as e:
    st.error(f"Excel load failed: {e}")
    st.stop()

# -----------------------
# CLEAN COLUMN NAMES
# -----------------------
df.columns = df.columns.str.strip()

# Auto-rename Epic column
for col in df.columns:
    if "epic" in col.lower():
        df.rename(columns={col: "Epic"}, inplace=True)

# -----------------------
# REQUIRED COLUMNS
# -----------------------
required_columns = ["Name", "Relation Name", "Age", "Door No.", "Epic"]

missing = [c for c in required_columns if c not in df.columns]

if missing:
    st.error(f"Missing columns in Excel: {missing}")
    st.stop()

df = df[required_columns]

# Convert all to string
for col in df.columns:
    df[col] = df[col].astype(str)

# -----------------------
# TOTAL RECORDS
# -----------------------
st.markdown(f"### Total Records: {len(df)}")

# -----------------------
# SEARCH
# -----------------------
query = st.text_input("🔍 Search by Name / Relation Name / Door Number / Epic")

if query:

    result = df[
        df["Name"].str.contains(query, case=False, na=False) |
        df["Relation Name"].str.contains(query, case=False, na=False) |
        df["Door No."].str.contains(query, case=False, na=False) |
        df["Epic"].str.contains(query, case=False, na=False)
    ]

    st.markdown(f"### Records Found: {len(result)}")
    st.dataframe(result, use_container_width=True)

    csv = result.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered Data",
        csv,
        "ward10_filtered.csv",
        "text/csv"
    )

else:
    st.info("Start typing Name, Relation Name, Door Number or Epic")
