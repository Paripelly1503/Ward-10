import streamlit as st
import pandas as pd

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Ward 10 Voters Dashboard",
    layout="wide"
)

st.title("🗳️ Ward 10 Voters Dashboard")

# ------------------------------
# LOAD EXCEL
# ------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("voters_data.xlsx")

try:
    df = load_data()
    df.columns = df.columns.str.strip()   # remove hidden spaces
    st.success("Excel Loaded Successfully")
except Exception as e:
    st.error("Excel file not found or error reading file.")
    st.stop()

# ------------------------------
# SHOW TOTAL RECORDS
# ------------------------------
st.subheader(f"Total Records: {len(df)}")

# ------------------------------
# SEARCH BOX
# ------------------------------
search = st.text_input(
    "Enter Name / Relation Name / Door Number",
    placeholder="Type Name or Door Number and press Enter"
).lower()

# ------------------------------
# FILTER LOGIC
# ------------------------------
if search:
    results = df[
        df["Name"].astype(str).str.lower().str.contains(search) |
        df["Relation Name"].astype(str).str.lower().str.contains(search) |
        df["Door No."].astype(str).str.lower().str.contains(search)
    ]
else:
    results = df

# ------------------------------
# DISPLAY TABLE
# ------------------------------
st.dataframe(results, use_container_width=True)

# ------------------------------
# GENDER DISTRIBUTION
# ------------------------------
st.subheader("Gender Distribution")
gender_counts = df["Sex"].value_counts()
st.bar_chart(gender_counts)

# ------------------------------
# AGE DISTRIBUTION
# ------------------------------
st.subheader("Age Distribution")
st.histogram = st.bar_chart(df["Age"].value_counts().sort_index())

# ------------------------------
# DOWNLOAD FILTERED DATA
# ------------------------------
st.download_button(
    label="Download Filtered Data",
    data=results.to_csv(index=False),
    file_name="filtered_voters_data.csv",
    mime="text/csv"
)
