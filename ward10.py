import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ward 10 Dashboard", layout="wide")

st.title("Ward 10 Voters Dashboard")

# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_excel("voters_data.xlsx")

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df

df = load_data()

# -----------------------
# Rename to standard form
# -----------------------
df = df.rename(columns={
    "name": "Name",
    "relation_name": "Relation Name",
    "relation_type": "Relation Type",
    "age": "Age",
    "sex": "Sex",
    "door_no.": "Door No",
    "door_no": "Door No",
    "epic_no": "Epic No"
})

st.success("Excel Loaded Successfully")

# -----------------------
# Search
# -----------------------
search = st.text_input("Search Name / Relation / Door / Epic")

if search:
    result = df[
        df.astype(str)
        .apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
    ]
else:
    result = df

st.subheader(f"Total Records: {len(result)}")
st.dataframe(result, use_container_width=True)

# -----------------------
# Charts
# -----------------------
st.subheader("Gender Distribution")
st.bar_chart(df["Sex"].value_counts())

st.subheader("Age Distribution")
st.bar_chart(df["Age"].value_counts().sort_index())

# -----------------------
# Download
# -----------------------
st.download_button(
    "Download Filtered Data",
    result.to_csv(index=False),
    "ward10_filtered.csv",
    "text/csv"
)
