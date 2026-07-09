# ==========================================================
# SMART HOSPITAL EMERGENCY ROOM ANALYTICS SYSTEM
# PART 1
# Dataset Creation + Validation + Priority Analysis
# ==========================================================

import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

# ----------------------------------------------------------
# CREATE REQUIRED FOLDERS
# ----------------------------------------------------------

os.makedirs("data", exist_ok=True)
os.makedirs("charts", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ----------------------------------------------------------
# DATASET GENERATION
# ----------------------------------------------------------

print("Generating Dataset...")

records = []

for i in range(1000):

    patient_id = f"P{i+1:04d}"

    age = random.randint(1, 90)

    gender = random.choice([
        "Male",
        "Female"
    ])

    arrival = (
        datetime(2026, 6, 1)
        +
        timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
    )

    arrival_time = arrival.strftime("%H:%M")

    heart_rate = random.randint(50, 180)

    oxygen_level = random.randint(75, 100)

    temperature = round(
        random.uniform(97, 104),
        1
    )

    systolic = random.randint(90, 180)

    diastolic = random.randint(60, 110)

    blood_pressure = f"{systolic}/{diastolic}"

    severity_score = random.randint(1, 10)

    waiting_time = random.randint(1, 180)

    treatment_required = random.choice([
        "Yes",
        "No"
    ])

    records.append([
        patient_id,
        age,
        gender,
        arrival_time,
        heart_rate,
        oxygen_level,
        temperature,
        blood_pressure,
        severity_score,
        waiting_time,
        treatment_required
    ])

# ----------------------------------------------------------
# DATAFRAME
# ----------------------------------------------------------

columns = [

    "Patient_ID",
    "Age",
    "Gender",
    "Arrival_Time",
    "Heart_Rate",
    "Oxygen_Level",
    "Temperature",
    "Blood_Pressure",
    "Severity_Score",
    "Waiting_Time",
    "Treatment_Required"
]

df = pd.DataFrame(
    records,
    columns=columns
)

# ----------------------------------------------------------
# SAVE CSV
# ----------------------------------------------------------

csv_file = "data/hospital_patients.csv"

df.to_csv(
    csv_file,
    index=False
)

print("CSV Dataset Saved")

# ----------------------------------------------------------
# DATA VALIDATION
# ----------------------------------------------------------

print("Running Validation...")

invalid_age = df[
    df["Age"] < 0
]

invalid_oxygen = df[
    (df["Oxygen_Level"] < 0)
    |
    (df["Oxygen_Level"] > 100)
]

invalid_heart_rate = df[
    (df["Heart_Rate"] < 20)
    |
    (df["Heart_Rate"] > 250)
]

missing_values = (
    df.isnull()
    .sum()
    .sum()
)

validation_report = pd.DataFrame({

    "Metric": [

        "Invalid Age",

        "Invalid Oxygen",

        "Invalid Heart Rate",

        "Missing Values"

    ],

    "Count": [

        len(invalid_age),

        len(invalid_oxygen),

        len(invalid_heart_rate),

        missing_values

    ]

})

print("\nValidation Report")
print(validation_report)

# ----------------------------------------------------------
# PRIORITY SCORE CALCULATION
# ----------------------------------------------------------

print("\nCalculating Priority Scores...")

def calculate_priority(row):

    score = 0

    if row["Oxygen_Level"] < 90:
        score += 30

    if row["Heart_Rate"] > 120:
        score += 20

    if row["Temperature"] > 102:
        score += 15

    if row["Age"] > 65:
        score += 10

    score += row["Severity_Score"] * 5

    return score


df["Priority_Score"] = df.apply(
    calculate_priority,
    axis=1
)

# ----------------------------------------------------------
# PATIENT CLASSIFICATION
# ----------------------------------------------------------

def classify_patient(score):

    if score <= 25:
        return "Normal"

    elif score <= 50:
        return "Moderate"

    elif score <= 75:
        return "High Priority"

    else:
        return "Critical"


df["Priority_Category"] = df[
    "Priority_Score"
].apply(
    classify_patient
)

# ----------------------------------------------------------
# CATEGORY COUNTS
# ----------------------------------------------------------

category_counts = (
    df["Priority_Category"]
    .value_counts()
)

print("\nPatient Categories")

print(category_counts)

# ----------------------------------------------------------
# AVERAGE WAITING TIME
# ----------------------------------------------------------

avg_waiting = (
    df.groupby(
        "Priority_Category"
    )["Waiting_Time"]
    .mean()
)

print("\nAverage Waiting Time")

print(avg_waiting)

# ----------------------------------------------------------
# SAVE UPDATED DATASET
# ----------------------------------------------------------

df.to_csv(
    csv_file,
    index=False
)

print("\nPART 1 COMPLETED SUCCESSFULLY")

# ==========================================================
# PART 2
# Queue Analysis + Doctor Requirement + Bed Occupancy
# Peak Hour Detection + Statistics + Alert System
# ==========================================================

import math

print("\nStarting Part 2...")

# ----------------------------------------------------------
# QUEUE MANAGEMENT ANALYSIS
# ----------------------------------------------------------

queue_analysis = df.groupby(
    "Priority_Category"
).agg(
    Patient_Count=("Patient_ID", "count"),
    Average_Waiting_Time=("Waiting_Time", "mean")
)

print("\nQueue Analysis")
print(queue_analysis)

# ----------------------------------------------------------
# DOCTOR REQUIREMENT ANALYSIS
# ----------------------------------------------------------

total_patients = len(df)

doctors_required_per_day = math.ceil(
    total_patients / 20
)

hour_series = df["Arrival_Time"].str[:2]

peak_hour_patient_count = (
    hour_series.value_counts().max()
)

doctors_required_peak_hour = math.ceil(
    peak_hour_patient_count / 20
)

print("\nDoctor Requirement")

print(
    f"Doctors Required Per Day: "
    f"{doctors_required_per_day}"
)

print(
    f"Doctors Required During Peak Hour: "
    f"{doctors_required_peak_hour}"
)

# ----------------------------------------------------------
# BED OCCUPANCY PREDICTION
# ----------------------------------------------------------

beds_required_daily = int(
    total_patients * 0.30
)

beds_required_weekly = (
    beds_required_daily * 7
)

print("\nBed Occupancy")

print(
    f"Beds Required Daily: "
    f"{beds_required_daily}"
)

print(
    f"Beds Required Weekly: "
    f"{beds_required_weekly}"
)

# ----------------------------------------------------------
# PEAK HOUR DETECTION
# ----------------------------------------------------------

hourly_stats = (
    hour_series
    .value_counts()
    .sort_index()
)

busiest_hour = (
    hourly_stats.idxmax()
)

least_busy_hour = (
    hourly_stats.idxmin()
)

average_patients_per_hour = round(
    hourly_stats.mean(),
    2
)

print("\nPeak Hour Analysis")

print(
    f"Busiest Hour: "
    f"{busiest_hour}:00"
)

print(
    f"Least Busy Hour: "
    f"{least_busy_hour}:00"
)

print(
    f"Average Patients Per Hour: "
    f"{average_patients_per_hour}"
)

# ----------------------------------------------------------
# STATISTICAL ANALYSIS
# ----------------------------------------------------------

print("\nStatistical Analysis")

mean_age = round(
    df["Age"].mean(),
    2
)

median_age = round(
    df["Age"].median(),
    2
)

std_age = round(
    df["Age"].std(),
    2
)

avg_oxygen = round(
    df["Oxygen_Level"].mean(),
    2
)

avg_heart_rate = round(
    df["Heart_Rate"].mean(),
    2
)

avg_temperature = round(
    df["Temperature"].mean(),
    2
)

avg_waiting = round(
    df["Waiting_Time"].mean(),
    2
)

max_waiting = (
    df["Waiting_Time"].max()
)

min_waiting = (
    df["Waiting_Time"].min()
)

print(f"Mean Age: {mean_age}")
print(f"Median Age: {median_age}")
print(f"Age Std Dev: {std_age}")

print(f"Average Oxygen: {avg_oxygen}")
print(f"Average Heart Rate: {avg_heart_rate}")
print(f"Average Temperature: {avg_temperature}")

print(f"Average Waiting Time: {avg_waiting}")
print(f"Maximum Waiting Time: {max_waiting}")
print(f"Minimum Waiting Time: {min_waiting}")

# ----------------------------------------------------------
# EMERGENCY ALERT SYSTEM
# ----------------------------------------------------------

critical_patients = len(
    df[
        df["Priority_Category"]
        == "Critical"
    ]
)

if critical_patients < 20:

    alert_level = "GREEN"

elif critical_patients <= 50:

    alert_level = "YELLOW"

elif critical_patients <= 100:

    alert_level = "ORANGE"

else:

    alert_level = "RED"

print("\nEmergency Alert System")

print(
    f"Critical Patients: "
    f"{critical_patients}"
)

print(
    f"Alert Level: "
    f"{alert_level}"
)

# ----------------------------------------------------------
# RESOURCE FORECASTING
# ----------------------------------------------------------

next_day_doctors = round(
    doctors_required_per_day * 1.05
)

next_day_beds = round(
    beds_required_daily * 1.05
)

next_day_emergency_staff = (
    next_day_doctors * 2
)

print("\nResource Forecasting")

print(
    f"Next Day Doctors: "
    f"{next_day_doctors}"
)

print(
    f"Next Day Beds: "
    f"{next_day_beds}"
)

print(
    f"Next Day Emergency Staff: "
    f"{next_day_emergency_staff}"
)

print("\nPART 2 COMPLETED SUCCESSFULLY")

# ==========================================================
# PART 3
# Charts + KPI Dashboard + Excel Report + AI Recommendations
# ==========================================================

import matplotlib.pyplot as plt
import seaborn as sns

print("\nStarting Part 3...")

# ----------------------------------------------------------
# CHART 1 : AGE DISTRIBUTION
# ----------------------------------------------------------

plt.figure(figsize=(8,5))

sns.histplot(
    df["Age"],
    bins=20,
    kde=True
)

plt.title("Patient Age Distribution")

plt.xlabel("Age")

plt.ylabel("Count")

plt.tight_layout()

plt.savefig(
    "charts/age_distribution.png"
)

plt.close()

# ----------------------------------------------------------
# CHART 2 : OXYGEN DISTRIBUTION
# ----------------------------------------------------------

plt.figure(figsize=(8,5))

sns.histplot(
    df["Oxygen_Level"],
    bins=15,
    kde=True
)

plt.title("Oxygen Level Distribution")

plt.xlabel("Oxygen Level")

plt.ylabel("Count")

plt.tight_layout()

plt.savefig(
    "charts/oxygen_distribution.png"
)

plt.close()

# ----------------------------------------------------------
# CHART 3 : PRIORITY CATEGORY
# ----------------------------------------------------------

plt.figure(figsize=(8,5))

sns.countplot(
    x="Priority_Category",
    data=df
)

plt.title(
    "Priority Category Distribution"
)

plt.tight_layout()

plt.savefig(
    "charts/priority_distribution.png"
)

plt.close()

# ----------------------------------------------------------
# CHART 4 : HOURLY ARRIVALS
# ----------------------------------------------------------

hourly_stats.plot(
    kind="bar",
    figsize=(10,5)
)

plt.title(
    "Hourly Patient Arrivals"
)

plt.xlabel("Hour")

plt.ylabel("Patients")

plt.tight_layout()

plt.savefig(
    "charts/hourly_arrivals.png"
)

plt.close()

# ----------------------------------------------------------
# CHART 5 : WAITING TIME ANALYSIS
# ----------------------------------------------------------

plt.figure(figsize=(8,5))

sns.boxplot(
    y=df["Waiting_Time"]
)

plt.title(
    "Waiting Time Analysis"
)

plt.tight_layout()

plt.savefig(
    "charts/waiting_time_analysis.png"
)

plt.close()

# ----------------------------------------------------------
# CHART 6 : BED OCCUPANCY
# ----------------------------------------------------------

bed_chart = pd.DataFrame({

    "Category": [
        "Daily Beds",
        "Weekly Beds"
    ],

    "Beds": [
        beds_required_daily,
        beds_required_weekly
    ]
})

plt.figure(figsize=(7,5))

sns.barplot(
    x="Category",
    y="Beds",
    data=bed_chart
)

plt.title(
    "Bed Occupancy Analysis"
)

plt.tight_layout()

plt.savefig(
    "charts/bed_occupancy.png"
)

plt.close()

print("Charts Generated")

# ----------------------------------------------------------
# KPI DASHBOARD DATA
# ----------------------------------------------------------

bed_utilization_rate = round(
    (
        beds_required_daily
        / total_patients
    ) * 100,
    2
)

doctor_utilization_rate = round(
    (
        doctors_required_per_day
        / 50
    ) * 100,
    2
)

dashboard_df = pd.DataFrame({

    "Metric":[

        "Total Patients",

        "Critical Patients",

        "Average Waiting Time",

        "Bed Utilization Rate",

        "Doctor Utilization Rate"

    ],

    "Value":[

        total_patients,

        critical_patients,

        avg_waiting,

        bed_utilization_rate,

        doctor_utilization_rate

    ]

})

# ----------------------------------------------------------
# DOCTOR DATAFRAME
# ----------------------------------------------------------

doctor_df = pd.DataFrame({

    "Metric":[

        "Doctors Required Per Day",

        "Doctors Required During Peak Hour",

        "Next Day Doctors"

    ],

    "Value":[

        doctors_required_per_day,

        doctors_required_peak_hour,

        next_day_doctors

    ]

})

# ----------------------------------------------------------
# BED DATAFRAME
# ----------------------------------------------------------

bed_df = pd.DataFrame({

    "Metric":[

        "Beds Daily",

        "Beds Weekly",

        "Next Day Beds"

    ],

    "Value":[

        beds_required_daily,

        beds_required_weekly,

        next_day_beds

    ]

})

# ----------------------------------------------------------
# EXCEL REPORT GENERATION
# ----------------------------------------------------------

excel_file = (
    "reports/"
    "hospital_analytics_report.xlsx"
)

with pd.ExcelWriter(
    excel_file,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Patient Records",
        index=False
    )

    queue_analysis.to_excel(
        writer,
        sheet_name="Priority Analysis"
    )

    doctor_df.to_excel(
        writer,
        sheet_name="Doctor Requirement",
        index=False
    )

    bed_df.to_excel(
        writer,
        sheet_name="Bed Occupancy",
        index=False
    )

    dashboard_df.to_excel(
        writer,
        sheet_name="Summary Dashboard",
        index=False
    )

print(
    "Excel Report Generated"
)

# ----------------------------------------------------------
# AI RECOMMENDATION SYSTEM
# ----------------------------------------------------------

recommendations = [

    "Increase doctors during peak hours",

    "Increase ICU beds",

    "Reduce waiting time",

    "Improve emergency workflow",

    "Deploy more night shift doctors",

    "Monitor oxygen critical patients",

    "Improve triage process",

    "Increase emergency staff",

    "Optimize bed allocation",

    "Use predictive analytics"
]

print("\nAI Recommendations\n")

for i, rec in enumerate(
    recommendations,
    start=1
):

    print(
        f"{i}. {rec}"
    )

print(
    "\nPART 3 COMPLETED SUCCESSFULLY"
)