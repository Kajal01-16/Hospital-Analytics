import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------------
# PAGE CONFIG
# -------------------------------------

st.set_page_config(
    page_title="Smart Hospital ER Analytics",
    page_icon="🏥",
    layout="wide"
)

# -------------------------------------
# LOAD DATA
# -------------------------------------

df = pd.read_csv(
    "data/hospital_patients.csv"
)

# -------------------------------------
# TITLE
# -------------------------------------

st.title(
    "🏥 Smart Hospital Emergency Room Analytics System"
)

st.markdown("---")

# -------------------------------------
# KPI CALCULATIONS
# -------------------------------------

total_patients = len(df)

critical_patients = len(
    df[df["Priority_Category"] == "Critical"]
)

avg_waiting = round(
    df["Waiting_Time"].mean(),
    2
)

bed_utilization = round(
    (total_patients * 0.30),
    0
)

# -------------------------------------
# KPI CARDS
# -------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Patients",
    total_patients
)

col2.metric(
    "Critical Patients",
    critical_patients
)

col3.metric(
    "Average Waiting",
    avg_waiting
)

col4.metric(
    "Beds Required",
    bed_utilization
)

st.markdown("---")

# -------------------------------------
# PATIENT TABLE
# -------------------------------------

st.subheader("Patient Records")

st.dataframe(df.head(50))

# -------------------------------------
# PRIORITY DISTRIBUTION
# -------------------------------------

st.subheader(
    "Priority Category Distribution"
)

fig1, ax1 = plt.subplots()

sns.countplot(
    x="Priority_Category",
    data=df,
    ax=ax1
)

st.pyplot(fig1)

# -------------------------------------
# AGE DISTRIBUTION
# -------------------------------------

st.subheader(
    "Age Distribution"
)

fig2, ax2 = plt.subplots()

sns.histplot(
    df["Age"],
    bins=20,
    kde=True,
    ax=ax2
)

st.pyplot(fig2)

# -------------------------------------
# OXYGEN DISTRIBUTION
# -------------------------------------

st.subheader(
    "Oxygen Distribution"
)

fig3, ax3 = plt.subplots()

sns.histplot(
    df["Oxygen_Level"],
    bins=15,
    kde=True,
    ax=ax3
)

st.pyplot(fig3)

# -------------------------------------
# PEAK HOUR DETECTION
# -------------------------------------

st.subheader(
    "Hourly Patient Arrivals"
)

hour_series = (
    df["Arrival_Time"]
    .str[:2]
)

hourly_stats = (
    hour_series
    .value_counts()
    .sort_index()
)

fig4, ax4 = plt.subplots(
    figsize=(10,4)
)

hourly_stats.plot(
    kind="bar",
    ax=ax4
)

st.pyplot(fig4)

# -------------------------------------
# WAITING TIME ANALYSIS
# -------------------------------------

st.subheader(
    "Waiting Time Analysis"
)

fig5, ax5 = plt.subplots()

sns.boxplot(
    y=df["Waiting_Time"],
    ax=ax5
)

st.pyplot(fig5)

# -------------------------------------
# RECOMMENDATIONS
# -------------------------------------

st.subheader(
    "AI Recommendations"
)

recommendations = [

    "Increase doctors during peak hours",

    "Increase ICU beds",

    "Reduce waiting times",

    "Improve triage process",

    "Deploy additional emergency staff",

    "Improve night shift coverage",

    "Monitor oxygen critical patients",

    "Optimize bed allocation",

    "Use predictive analytics",

    "Improve patient routing"
]

for rec in recommendations:

    st.success(rec)

st.markdown("---")

st.write(
    "Smart Hospital ER Analytics Dashboard"
)