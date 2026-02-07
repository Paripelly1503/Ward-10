import streamlit as st
import pandas as pd

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Ward 10 Voter Search App",
    layout="wide"
)

st.title("🗳️ Ward 10 Voter Search App")

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_excel("voters_data.xlsx")

try:
    df = load_data()
    df.columns = df.columns.str.strip()
    st.success("Excel Loaded Successfully")
except:
    st.error("voters_data.xlsx not found")
    st.stop()

# ---------------------------
# TOTAL RECORDS
# ---------------------------
st.subheader(f"Total Records: {len(df)}")

# ---------------------------
# SEARCH BOX
# ---------------------------
query = st.text_input(
    "Enter Name / Relation Name / Door Number",
    placeholder="Type Name or Door Number and press Enter"
).lower()

if query:
    filtered = df[
        df["Name"].astype(str).str.lower().str.contains(query) |
        df["Relation Name"].astype(str).str.lower().str.contains(query) |
        df["Door No."].astype(str).str.lower().str.contains(query)
    ]
else:
    filtered = df

# ---------------------------
# DISPLAY TABLE
# ---------------------------
st.dataframe(filtered, use_container_width=True)

# ---------------------------
# PIE CHART (MALE vs FEMALE)
# ---------------------------
st.subheader("Male vs Female Percentage")

gender_counts = df["Sex"].value_counts()

pie_df = pd.DataFrame({
    "Gender": gender_counts.index,
    "Count": gender_counts.values
})

st.pyplot(
    pie_df.set_index("Gender").plot.pie(
        y="Count",
        autopct="%1.1f%%",
        legend=False,
        figsize=(4,4)
    ).figure
)

# ---------------------------
# DOWNLOAD BUTTON
# ---------------------------
st.download_button(
    "Download Filtered Data",
    filtered.to_csv(index=False),
    file_name="filtered_voters.csv",
    mime="text/csv"
)
