
============================================================
PERFORMANCE MODELLING OF A STUDENT REGISTRATION SYSTEM
============================================================

System:
    Student Registration Queue

Model:
    M/M/4 Queueing Model
    What-if Capacity Analysis

Dataset:
    500 student registration records
    4 registration officers

Outputs:
    - Performance metrics
    - Officer analysis
    - Hourly analysis
    - M/M/4 queueing results
    - Capacity what-if analysis
    - Service improvement analysis
    - 8 performance graphs
    - CSV result files
"""

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math
import os


# ============================================================
# 2. SYSTEM DESCRIPTION AND PERFORMANCE GOALS
# ============================================================

"""
System Chosen:
    Student Registration Queue

Description:
    Students arrive at the registration system, wait if all
    registration officers are busy, receive registration
    service, and then leave the system.

Performance Goals:
    1. Minimize student waiting time.
    2. Maximize registration throughput.
    3. Measure officer utilization.
    4. Identify high-congestion periods.
    5. Identify bottlenecks.
    6. Evaluate whether four officers provide sufficient capacity.
    7. Evaluate the effect of increasing registration capacity.
    8. Evaluate the effect of faster service.
"""


# ============================================================
# 3. CREATE OUTPUT FOLDER
# ============================================================

output_folder = "registration_model_results"

os.makedirs(
    output_folder,
    exist_ok=True
)

print("\nOutput folder created:")
print(os.path.abspath(output_folder))


# ============================================================
# 4. DATA LOADING
# ============================================================

file_path = r"C:\Users\Admin\Desktop\6373 MP\Excel Data\Registration_Queue_Simulation.csv"

try:

    df = pd.read_csv(file_path)

    print("\nDataset loaded successfully.")
    print("Number of records:", len(df))

except FileNotFoundError:

    print("\nERROR: Dataset file was not found.")
    print("Please check the file path:")
    print(file_path)

    raise


print("\nOriginal columns:")
print(df.columns.tolist())


# ============================================================
# 5. CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
)

print("\nCleaned columns:")
print(df.columns.tolist())


# ============================================================
# 6. DATA OVERVIEW
# ============================================================

print("\n============================================================")
print("DATA INFORMATION")
print("============================================================")

df.info()


print("\n============================================================")
print("DESCRIPTIVE STATISTICS")
print("============================================================")

print(
    df.describe(include="all")
)


# ============================================================
# 7. CONVERT TIME COLUMNS
# ============================================================

required_time_columns = [
    "Arrival_Time",
    "Service_Start_Time",
    "Service_End_Time"
]

for column in required_time_columns:

    if column not in df.columns:

        raise ValueError(
            f"Required column '{column}' was not found in dataset."
        )


df["Arrival_Time"] = pd.to_datetime(
    df["Arrival_Time"],
    format="%H:%M",
    errors="coerce"
)

df["Service_Start_Time"] = pd.to_datetime(
    df["Service_Start_Time"],
    format="%H:%M",
    errors="coerce"
)

df["Service_End_Time"] = pd.to_datetime(
    df["Service_End_Time"],
    format="%H:%M",
    errors="coerce"
)


# ============================================================
# 8. CHECK FOR INVALID TIME VALUES
# ============================================================

print("\n============================================================")
print("TIME DATA VALIDATION")
print("============================================================")

print(
    "Missing Arrival Times:",
    df["Arrival_Time"].isna().sum()
)

print(
    "Missing Service Start Times:",
    df["Service_Start_Time"].isna().sum()
)

print(
    "Missing Service End Times:",
    df["Service_End_Time"].isna().sum()
)


# ============================================================
# 9. CALCULATE SERVICE TIME
# ============================================================

df["Calculated_Service_Time"] = (
    df["Service_End_Time"]
    - df["Service_Start_Time"]
).dt.total_seconds() / 60


# ============================================================
# 10. CALCULATE WAITING TIME
# ============================================================

df["Calculated_Wait_Time"] = (
    df["Service_Start_Time"]
    - df["Arrival_Time"]
).dt.total_seconds() / 60


# ============================================================
# 11. CALCULATE TOTAL TIME IN SYSTEM
# ============================================================

df["Calculated_Time_in_System"] = (
    df["Service_End_Time"]
    - df["Arrival_Time"]
).dt.total_seconds() / 60


# ============================================================
# 12. HANDLE MIDNIGHT / NEGATIVE TIME VALUES
# ============================================================

df.loc[
    df["Calculated_Service_Time"] < 0,
    "Calculated_Service_Time"
] += 24 * 60


df.loc[
    df["Calculated_Wait_Time"] < 0,
    "Calculated_Wait_Time"
] += 24 * 60


df.loc[
    df["Calculated_Time_in_System"] < 0,
    "Calculated_Time_in_System"
] += 24 * 60


# ============================================================
# 13. USE CALCULATED VALUES
# ============================================================

df["Service_Time"] = (
    df["Calculated_Service_Time"]
)

df["Wait_Time"] = (
    df["Calculated_Wait_Time"]
)

df["Time_in_System"] = (
    df["Calculated_Time_in_System"]
)


# ============================================================
# 14. BASIC PERFORMANCE METRICS
# ============================================================

print("\n============================================================")
print("SYSTEM PERFORMANCE")
print("============================================================")

total_students = len(df)

average_wait = (
    df["Wait_Time"].mean()
)

maximum_wait = (
    df["Wait_Time"].max()
)

average_service = (
    df["Service_Time"].mean()
)

maximum_service = (
    df["Service_Time"].max()
)

average_system_time = (
    df["Time_in_System"].mean()
)

maximum_system_time = (
    df["Time_in_System"].max()
)


print(
    "Total Students:",
    total_students
)

print(
    f"Average Waiting Time: "
    f"{average_wait:.2f} minutes"
)

print(
    f"Maximum Waiting Time: "
    f"{maximum_wait:.2f} minutes"
)

print(
    f"Average Service Time: "
    f"{average_service:.2f} minutes"
)

print(
    f"Maximum Service Time: "
    f"{maximum_service:.2f} minutes"
)

print(
    f"Average Time in System: "
    f"{average_system_time:.2f} minutes"
)

print(
    f"Maximum Time in System: "
    f"{maximum_system_time:.2f} minutes"
)


# ============================================================
# 15. REGISTRATION OFFICER ANALYSIS
# ============================================================

print("\n============================================================")
print("OFFICER ANALYSIS")
print("============================================================")


officer_analysis = df.groupby(
    "Officer_ID"
).agg(

    Students_Served=(
        "Student_ID",
        "count"
    ),

    Average_Service_Time=(
        "Service_Time",
        "mean"
    ),

    Average_Wait_Time=(
        "Wait_Time",
        "mean"
    ),

    Total_Service_Time=(
        "Service_Time",
        "sum"
    )

)


print(
    officer_analysis.round(2)
)


# ============================================================
# 16. OFFICER UTILIZATION
# ============================================================

first_arrival = (
    df["Arrival_Time"].min()
)

last_departure = (
    df["Service_End_Time"].max()
)


observation_time = (
    last_departure
    - first_arrival
).total_seconds() / 60


print(
    "\nObservation Period:",
    round(observation_time, 2),
    "minutes"
)


# Utilization
#
# Total busy time of officer
# --------------------------
# Total observation time
#

officer_analysis["Utilization"] = (
    officer_analysis["Total_Service_Time"]
    / observation_time
)


print("\n============================================================")
print("OFFICER UTILIZATION")
print("============================================================")


print(
    officer_analysis[
        [
            "Students_Served",
            "Average_Service_Time",
            "Average_Wait_Time",
            "Utilization"
        ]
    ].round(3)
)


# ============================================================
# 17. SYSTEM THROUGHPUT
# ============================================================

observation_hours = (
    observation_time / 60
)


throughput = (
    total_students
    / observation_hours
)


print("\n============================================================")
print("SYSTEM THROUGHPUT")
print("============================================================")


print(
    f"System Throughput: "
    f"{throughput:.2f} students/hour"
)


# ============================================================
# 18. HOURLY LOAD ANALYSIS
# ============================================================

df["Arrival_Hour"] = (
    df["Arrival_Time"].dt.hour
)


hourly_analysis = df.groupby(
    "Arrival_Hour"
).agg(

    Students_Arrived=(
        "Student_ID",
        "count"
    ),

    Average_Wait_Time=(
        "Wait_Time",
        "mean"
    ),

    Maximum_Wait_Time=(
        "Wait_Time",
        "max"
    ),

    Average_Service_Time=(
        "Service_Time",
        "mean"
    ),

    Average_Time_in_System=(
        "Time_in_System",
        "mean"
    )

).reset_index()


print("\n============================================================")
print("HOURLY PERFORMANCE")
print("============================================================")


print(
    hourly_analysis.round(2)
)


# ============================================================
# 19. PEAK LOAD PERIOD
# ============================================================

peak_hour = hourly_analysis.loc[
    hourly_analysis["Students_Arrived"].idxmax()
]


print("\n============================================================")
print("PEAK LOAD PERIOD")
print("============================================================")


print(
    f"Peak Arrival Hour: "
    f"{int(peak_hour['Arrival_Hour'])}:00"
)


print(
    f"Students Arrived: "
    f"{int(peak_hour['Students_Arrived'])}"
)


print(
    f"Average Waiting Time: "
    f"{peak_hour['Average_Wait_Time']:.2f} minutes"
)


# ============================================================
# 20. M/M/4 QUEUEING MODEL PARAMETERS
# ============================================================

"""
M/M/4 Queue:

First M:
    Markovian / stochastic arrivals

Second M:
    Exponential service times

4:
    Four parallel registration officers

Parameters:

lambda = arrival rate
mu     = service rate per officer
c      = number of officers
rho    = system utilization
"""


number_of_servers = 4


arrival_rate = (
    total_students
    / observation_hours
)


mean_service_hours = (
    average_service / 60
)


service_rate = (
    1 / mean_service_hours
)


rho = (
    arrival_rate
    /
    (
        number_of_servers
        * service_rate
    )
)


print("\n============================================================")
print("M/M/4 PARAMETERS")
print("============================================================")


print(
    f"Arrival Rate λ: "
    f"{arrival_rate:.2f} students/hour"
)


print(
    f"Service Rate μ: "
    f"{service_rate:.2f} students/hour/officer"
)


print(
    f"Number of Officers: "
    f"{number_of_servers}"
)


print(
    f"System Utilization ρ: "
    f"{rho:.3f}"
)


# ============================================================
# 21. M/M/C QUEUEING FUNCTION
# ============================================================

def mmc_queue(lam, mu, c):

    rho = (
        lam
        /
        (c * mu)
    )


    # --------------------------------------------------------
    # Unstable system
    # --------------------------------------------------------

    if rho >= 1:

        return {

            "rho": rho,

            "P0": np.inf,

            "Lq": np.inf,

            "Wq_hours": np.inf,

            "Wq_minutes": np.inf,

            "L": np.inf,

            "W_hours": np.inf,

            "W_minutes": np.inf

        }


    # --------------------------------------------------------
    # Traffic intensity
    # --------------------------------------------------------

    a = (
        lam / mu
    )


    # --------------------------------------------------------
    # Summation
    # --------------------------------------------------------

    summation = 0


    for n in range(c):

        summation += (
            a ** n
        ) / math.factorial(n)


    # --------------------------------------------------------
    # Final term
    # --------------------------------------------------------

    final_term = (

        (a ** c)

        /

        (
            math.factorial(c)
            *
            (1 - rho)
        )

    )


    # --------------------------------------------------------
    # Probability zero customers
    # --------------------------------------------------------

    P0 = 1 / (
        summation
        +
        final_term
    )


    # --------------------------------------------------------
    # Average queue length
    # --------------------------------------------------------

    Lq = (

        P0
        *
        (a ** c)
        *
        rho

        /

        (
            math.factorial(c)
            *
            (1 - rho) ** 2
        )

    )


    # --------------------------------------------------------
    # Average waiting time
    # --------------------------------------------------------

    Wq_hours = (
        Lq / lam
    )


    # --------------------------------------------------------
    # Average number in system
    # --------------------------------------------------------

    L = (
        Lq + a
    )


    # --------------------------------------------------------
    # Average time in system
    # --------------------------------------------------------

    W_hours = (
        L / lam
    )


    return {

        "rho": rho,

        "P0": P0,

        "Lq": Lq,

        "Wq_hours": Wq_hours,

        "Wq_minutes":
            Wq_hours * 60,

        "L": L,

        "W_hours": W_hours,

        "W_minutes":
            W_hours * 60

    }


# ============================================================
# 22. CURRENT M/M/4 RESULTS
# ============================================================

queue_results = mmc_queue(
    arrival_rate,
    service_rate,
    number_of_servers
)


print("\n============================================================")
print("M/M/4 RESULTS")
print("============================================================")


for key, value in queue_results.items():

    if np.isinf(value):

        print(
            f"{key}: INFINITY"
        )

    else:

        print(
            f"{key}: {value:.4f}"
        )


# ============================================================
# 23. DISTRIBUTION VALIDATION
# ============================================================

"""
The M/M/4 model assumes exponential service times.

A Kolmogorov-Smirnov test is used to examine whether the
observed service-time data is consistent with an exponential
distribution.

H0:
    Service times follow an exponential distribution.

H1:
    Service times do not follow an exponential distribution.

Significance level:
    alpha = 0.05
"""


service_data = (
    df["Service_Time"]
    .dropna()
)


exponential_scale = (
    service_data.mean()
)


ks_statistic, p_value = stats.kstest(

    service_data,

    "expon",

    args=(
        0,
        exponential_scale
    )

)


print("\n============================================================")
print("EXPONENTIAL DISTRIBUTION TEST")
print("============================================================")


print(
    f"KS Statistic: "
    f"{ks_statistic:.4f}"
)


print(
    f"P-Value: "
    f"{p_value:.4f}"
)


if p_value >= 0.05:

    print(
        "Result: The exponential assumption "
        "is not rejected at the 5% significance level."
    )

else:

    print(
        "Result: The exponential assumption "
        "is rejected at the 5% significance level."
    )


# ============================================================
# 24. BOTTLENECK ANALYSIS
# ============================================================

print("\n============================================================")
print("BOTTLENECK ANALYSIS")
print("============================================================")


bottleneck_officer = (
    officer_analysis[
        "Average_Wait_Time"
    ].idxmax()
)


highest_utilization_officer = (
    officer_analysis[
        "Utilization"
    ].idxmax()
)


print(
    "Officer with highest average waiting time:",
    bottleneck_officer
)


print(
    "Officer with highest utilization:",
    highest_utilization_officer
)


# ============================================================
# 25. WAITING TIME CATEGORIES
# ============================================================

def classify_waiting_time(wait):

    if wait == 0:

        return "No Wait"

    elif wait <= 2:

        return "Low Wait"

    elif wait <= 5:

        return "Moderate Wait"

    else:

        return "High Wait"


df["Waiting_Category"] = (
    df["Wait_Time"]
    .apply(
        classify_waiting_time
    )
)


waiting_categories = (
    df["Waiting_Category"]
    .value_counts()
)


print("\n============================================================")
print("WAITING TIME CATEGORIES")
print("============================================================")


print(
    waiting_categories
)


# ============================================================
# 26. CAPACITY WHAT-IF ANALYSIS
# ============================================================

"""
Capacity scenarios:

3 officers
4 officers
5 officers
6 officers

The same observed arrival and service rates are used.
"""


scenario_results = []


for officers in [3, 4, 5, 6]:

    result = mmc_queue(

        arrival_rate,

        service_rate,

        officers

    )


    scenario_results.append({

        "Officers":
            officers,

        "Utilization":
            result["rho"],

        "Average_Queue_Length":
            result["Lq"],

        "Average_Waiting_Time_Min":
            result["Wq_minutes"],

        "Average_System_Time_Min":
            result["W_minutes"]

    })


scenario_df = pd.DataFrame(
    scenario_results
)


print("\n============================================================")
print("CAPACITY WHAT-IF ANALYSIS")
print("============================================================")


print(
    scenario_df.round(3)
)


# ============================================================
# 27. SERVICE IMPROVEMENT WHAT-IF ANALYSIS
# ============================================================

"""
Service improvement scenarios:

0%
10%
20%
30%

Four registration officers are maintained.
"""


service_scenarios = []


for improvement in [
    0,
    0.10,
    0.20,
    0.30
]:

    improved_service_rate = (

        service_rate

        /

        (1 - improvement)

    )


    result = mmc_queue(

        arrival_rate,

        improved_service_rate,

        4

    )


    service_scenarios.append({

        "Service_Improvement":
            improvement * 100,

        "Service_Rate":
            improved_service_rate,

        "Utilization":
            result["rho"],

        "Average_Waiting_Time":
            result["Wq_minutes"]

    })


service_df = pd.DataFrame(
    service_scenarios
)


print("\n============================================================")
print("SERVICE IMPROVEMENT ANALYSIS")
print("============================================================")


print(
    service_df.round(3)
)


# ============================================================
# 28. VISUALIZATION 1
# WAITING TIME DISTRIBUTION
# ============================================================

print("\nGenerating Graph 1...")


plt.figure(
    figsize=(10, 6)
)


plt.hist(

    df["Wait_Time"],

    bins=15,

    edgecolor="black"

)


plt.xlabel(
    "Waiting Time (minutes)"
)

plt.ylabel(
    "Number of Students"
)

plt.title(
    "Distribution of Student Waiting Times"
)


plt.grid(
    axis="y",
    alpha=0.3
)


plt.tight_layout()


plt.savefig(

    os.path.join(

        output_folder,

        "01_waiting_time_distribution.png"

    ),

    dpi=300,

    bbox_inches="tight"

)


plt.close()


# ============================================================
# 29. VISUALIZATION 2
# SERVICE TIME DISTRIBUTION
# ============================================================

print("Generating Graph 2...")


plt.figure(
    figsize=(10, 6)
)


plt.hist(

    df["Service_Time"],

    bins=10,

    edgecolor="black"

)


plt.xlabel(
    "Service Time (minutes)"
)

plt.ylabel(
    "Number of Students"
)

plt.title(
    "Distribution of Registration Service Times"
)


plt.grid(
    axis="y",
    alpha=0.3
)


plt.tight_layout()


plt.savefig(

    os.path.join(

        output_folder,

        "02_service_time_distribution.png"

    ),

    dpi=300,

    bbox_inches="tight"

)


plt.close()


# ============================================================
# 30. VISUALIZATION 3
# HOURLY ARRIVAL LOAD
# ============================================================

print("Generating Graph 3...")


plt.figure(
    figsize=(10, 6)
)


plt.bar(

    hourly_analysis["Arrival_Hour"],

    hourly_analysis["Students_Arrived"]

)


plt.xlabel(
    "Arrival Hour"
)

plt.ylabel(
    "Number of Students"
)

plt.title(
    "Student Arrival Load by Hour"
)


plt.grid(
    axis="y",
    alpha=0.3
)


plt.tight_layout()


plt.savefig(

    os.path.join(

        output_folder,

        "03_hourly_arrival_load.png"

    ),

    dpi=300,

    bbox_inches="tight"

)


plt.close()


# ============================================================
# 31. VISUALIZATION 4
# AVERAGE WAITING TIME BY HOUR
# ============================================================

print("Generating Graph 4...")


plt.figure(
    figsize=(10, 6)
)


plt.plot(

    hourly_analysis["Arrival_Hour"],

    hourly_analysis["Average_Wait_Time"],

    marker="o"

)


plt.xlabel(
    "Arrival Hour"
)

plt.ylabel(
    "Average Waiting Time (minutes)"
)

plt.title(
    "Average Waiting Time by Arrival Hour"
)


plt.grid(
    True,
    alpha=0.3
)


plt.tight_layout()


plt.savefig(

    os.path.join(

        output_folder,

        "04_average_waiting_time_by_hour.png"

    ),

    dpi=300,

    bbox_inches="tight"

)


plt.close()


# ============================================================
# 32. VISUALIZATION 5
# OFFICER UTILIZATION
# ============================================================

print("Generating Graph 5...")


plt.figure(
    figsize=(8, 6)
)


plt.bar(

    officer_analysis.index.astype(str),

    officer_analysis["Utilization"]

)


plt.axhline(

    y=1.0,

    linestyle="--"

)


plt.xlabel(
    "Registration Officer"
)

plt.ylabel(
    "Utilization"
)

plt.title(
    "Registration Officer Utilization"
)


plt.grid(
    axis="y",
    alpha=0.3
)


plt.tight_layout()


plt.savefig(

    os.path.join(

        output_folder,

        "05_officer_utilization.png"

    ),

    dpi=300,

    bbox_inches="tight"

)


plt.close()


# ============================================================
# 33. VISUALIZATION 6
# CAPACITY SCENARIO COMPARISON
# ============================================================

print("Generating Graph 6...")


plt.figure(
    figsize=(9, 6)
)


plt.plot(

    scenario_df["Officers"],

    scenario_df[
        "Average_Waiting_Time_Min"
    ],

    marker="o"

)


plt.xlabel(
    "Number of Registration Officers"
)

plt.ylabel(
    "Average Waiting Time (minutes)"
)

plt.title(
    "Impact of Registration Capacity on Waiting Time"
)


plt.grid(
    True,
    alpha=0.3
)


plt.tight_layout()


plt.savefig(

    os.path.join(

        output_folder,

        "06_capacity_scenario_comparison.png"

    ),

    dpi=300,

    bbox_inches="tight"

)


plt.close()


# ============================================================
# 34. VISUALIZATION 7
# SERVICE IMPROVEMENT
# ============================================================

print("Generating Graph 7...")


plt.figure(
    figsize=(9, 6)
)


plt.plot(

    service_df["Service_Improvement"],

    service_df["Average_Waiting_Time"],

    marker="o"

)


plt.xlabel(
    "Service Speed Improvement (%)"
)

plt.ylabel(
    "Average Waiting Time (minutes)"
)

plt.title(
    "Impact of Faster Registration Service on Waiting Time"
)


plt.grid(
    True,
    alpha=0.3
)


plt.tight_layout()


plt.savefig(

    os.path.join(

        output_folder,

        "07_service_improvement.png"

    ),

    dpi=300,

    bbox_inches="tight"

)


plt.close()


# ============================================================
# 35. VISUALIZATION 8
# OFFICER SERVICE TIME
# ============================================================

print("Generating Graph 8...")


plt.figure(
    figsize=(8, 6)
)


plt.bar(

    officer_analysis.index.astype(str),

    officer_analysis[
        "Average_Service_Time"
    ]

)


plt.xlabel(
    "Registration Officer"
)

plt.ylabel(
    "Average Service Time (minutes)"
)

plt.title(
    "Average Registration Service Time by Officer"
)


plt.grid(
    axis="y",
    alpha=0.3
)


plt.tight_layout()


plt.savefig(

    os.path.join(

        output_folder,

        "08_officer_service_time.png"

    ),

    dpi=300,

    bbox_inches="tight"

)


plt.close()


# ============================================================
# 36. SYSTEM MODEL DIAGRAM
# ============================================================

print(
    """

============================================================
SYSTEM MODEL
============================================================

Student Arrivals
       |
       v
+-------------------+
| Registration Queue|
+-------------------+
       |
       v
+------+------+------+------+
|      |      |      |      |
O_01  O_02   O_03   O_04
|      |      |      |
+------+------+------+------+
       |
       v
Registration Completed
       |
       v
Student Departure

Model:
M/M/4 Queue

Arrival Process
       |
       v
Registration Queue
       |
       v
4 Parallel Registration Officers
       |
       v
Registration Completed
       |
       v
Student Departure

"""
)


# ============================================================
# 37. SAVE CLEANED DATA
# ============================================================

df.to_csv(

    os.path.join(

        output_folder,

        "cleaned_registration_data.csv"

    ),

    index=False

)


# ============================================================
# 38. SAVE OFFICER PERFORMANCE
# ============================================================

officer_analysis.to_csv(

    os.path.join(

        output_folder,

        "officer_performance.csv"

    )

)


# ============================================================
# 39. SAVE HOURLY ANALYSIS
# ============================================================

hourly_analysis.to_csv(

    os.path.join(

        output_folder,

        "hourly_analysis.csv"

    ),

    index=False

)


# ============================================================
# 40. SAVE CAPACITY SCENARIOS
# ============================================================

scenario_df.to_csv(

    os.path.join(

        output_folder,

        "capacity_scenarios.csv"

    ),

    index=False

)


# ============================================================
# 41. SAVE SERVICE IMPROVEMENT SCENARIOS
# ============================================================

service_df.to_csv(

    os.path.join(

        output_folder,

        "service_improvement_scenarios.csv"

    ),

    index=False

)


# ============================================================
# 42. SAVE M/M/4 RESULTS
# ============================================================

queue_results_df = pd.DataFrame({

    "Metric": list(
        queue_results.keys()
    ),

    "Value": list(
        queue_results.values()
    )

})


queue_results_df.to_csv(

    os.path.join(

        output_folder,

        "mm4_queue_results.csv"

    ),

    index=False

)


# ============================================================
# 43. SAVE SUMMARY RESULTS
# ============================================================

summary_df = pd.DataFrame({

    "Metric": [

        "Total Students",

        "Registration Officers",

        "System Throughput (students/hour)",

        "Average Waiting Time (minutes)",

        "Maximum Waiting Time (minutes)",

        "Average Service Time (minutes)",

        "Maximum Service Time (minutes)",

        "Average Time in System (minutes)",

        "Maximum Time in System (minutes)",

        "M/M/4 Utilization",

        "Arrival Rate (students/hour)",

        "Service Rate (students/hour/officer)",

        "Peak Arrival Hour",

        "Peak Hour Student Count",

        "Peak Hour Average Waiting Time"

    ],

    "Value": [

        total_students,

        number_of_servers,

        throughput,

        average_wait,

        maximum_wait,

        average_service,

        maximum_service,

        average_system_time,

        maximum_system_time,

        rho,

        arrival_rate,

        service_rate,

        f"{int(peak_hour['Arrival_Hour'])}:00",

        int(
            peak_hour["Students_Arrived"]
        ),

        peak_hour[
            "Average_Wait_Time"
        ]

    ]

})


summary_df.to_csv(

    os.path.join(

        output_folder,

        "final_model_summary.csv"

    ),

    index=False

)


# ============================================================
# 44. FINAL SUMMARY
# ============================================================

print("\n")
print("============================================================")
print("FINAL MODEL SUMMARY")
print("============================================================")


print(
    f"Students analyzed          : "
    f"{total_students}"
)


print(
    f"Registration officers      : "
    f"{number_of_servers}"
)


print(
    f"System throughput          : "
    f"{throughput:.2f} students/hour"
)


print(
    f"Average waiting time       : "
    f"{average_wait:.2f} minutes"
)


print(
    f"Maximum waiting time       : "
    f"{maximum_wait:.2f} minutes"
)


print(
    f"Average service time       : "
    f"{average_service:.2f} minutes"
)


print(
    f"Average time in system     : "
    f"{average_system_time:.2f} minutes"
)


print(
    f"M/M/4 utilization          : "
    f"{rho:.3f}"
)


print(
    f"Peak arrival hour          : "
    f"{int(peak_hour['Arrival_Hour'])}:00"
)


print(
    f"Peak-hour student count    : "
    f"{int(peak_hour['Students_Arrived'])}"
)


# ============================================================
# 45. OUTPUT FILE LIST
# ============================================================

print("\n============================================================")
print("GENERATED OUTPUT FILES")
print("============================================================")


output_files = os.listdir(
    output_folder
)


for file in sorted(output_files):

    print(
        "✓",
        file
    )


print("\n============================================================")
print("PERFORMANCE MODELLING COMPLETED SUCCESSFULLY")
print("============================================================")


print(
    "\nAll 8 graphs have been generated and saved in:"
)


print(
    os.path.abspath(output_folder)
)
