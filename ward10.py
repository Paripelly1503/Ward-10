import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Settings
# -----------------------------
st.set_page_config(page_title="Ward 10 Voter Dashboard", layout="wide")

st.title("🗳 Ward 10 Voters Search Dashboard")

# -----------------------------
# Load Excel
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_excel("voters_data.xlsx")

df = load_data()

# -----------------------------
# Sidebar Search
# -----------------------------
st.sidebar.header("Search Filters")

name_search = st.sidebar.text_input("Search Name")
relation_search = st.sidebar.text_input("Search Relation")
door_search = st.sidebar.text_input("Search Door Number")
voterid_search = st.sidebar.text_input("Search Voter ID")

filtered = df.copy()

if name_search:
    filtered = filtered[filtered["Name"].str.contains(name_search, case=False, na=False)]

if relation_search:
    filtered = filtered[filtered["Relation"].str.contains(relation_search, case=False, na=False)]

if door_search:
    filtered = filtered[filtered["Door Number"].astype(str).str.contains(door_search)]

if voterid_search:
    filtered = filtered[filtered["Voter ID"].astype(str).str.contains(voterid_search)]

# -----------------------------
# Results
# -----------------------------
st.subheader("📋 Search Results")

st.write(f"Total Records Found: {len(filtered)}")

st.dataframe(filtered, use_container_width=True)

# -----------------------------
# Download Button
# -----------------------------
st.download_button(
    label="⬇ Download Search Results",
    data=filtered.to_csv(index=False),
    file_name="filtered_voters.csv",
    mime="text/csv"
)

# -----------------------------
# Charts
# -----------------------------
st.subheader("📊 Statistics")

col1, col2 = st.columns(2)

# Gender Pie
with col1:
    gender_counts = df["Gender"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%")
    ax1.set_title("Gender Distribution")
    st.pyplot(fig1)

# Age Groups
with col2:
    bins = [0,18,30,45,60,120]
    labels = ["<18","18-30","31-45","46-60","60+"]
    df["Age Group"] = pd.cut(df["Age"], bins=bins, labels=labels)
    age_counts = df["Age Group"].value_counts().sort_index()

    fig2, ax2 = plt.subplots()
    ax2.bar(age_counts.index.astype(str), age_counts.values)
    ax2.set_title("Age Group Distribution")
    st.pyplot(fig2)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("Developed for Ward 10 Voter Data Analysis")