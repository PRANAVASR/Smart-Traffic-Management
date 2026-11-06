"""
Smart Traffic Management - Data Analysis
----------------------------------------
Keep this Python file in the same folder as:
    Cleaned_Smart_Traffic (2).xlsx

Required packages:
    pip install pandas openpyxl matplotlib

Run:
    python Data_analysis.py

The script prints key findings and saves all charts in a folder named
"traffic_analysis_outputs".
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Locate the Excel file beside this script.
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Cleaned_Smart_Traffic.xlsx.xlsx"
OUTPUT_DIR = BASE_DIR / "traffic_analysis_outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Could not find: {DATA_FILE}\n"
        "Place 'Cleaned_Smart_Traffic (2).xlsx' in the same folder as this script."
    )

# 1. Load dataset
df = pd.read_excel(DATA_FILE)

required_columns = [
    "City", "Intersection", "Number_of_Roads", "Number_of_Lanes",
    "Vehicles_Observed", "Traffic_Level", "Time_Period"
]
missing_columns = [column for column in required_columns if column not in df.columns]
if missing_columns:
    raise ValueError(f"The dataset is missing these columns: {missing_columns}")

print("=" * 55)
print("SMART TRAFFIC MANAGEMENT - DATA ANALYSIS")
print("=" * 55)
print("\nFirst five rows:")
print(df.head().to_string(index=False))

# 2. Inspect and clean data
print("\nDataset information:")
print(df.info())

print("\nMissing values before cleaning:")
print(df.isnull().sum())

print("\nDuplicate rows before cleaning:", df.duplicated().sum())

# Standardize text columns and convert numeric columns safely.
for column in ["City", "Intersection", "Traffic_Level", "Time_Period"]:
    df[column] = df[column].astype("string").str.strip()

for column in ["Number_of_Roads", "Number_of_Lanes", "Vehicles_Observed"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Remove exact duplicates and rows missing essential values.
df = df.drop_duplicates()
df = df.dropna(subset=required_columns)

# Remove impossible negative/zero road and lane counts, and negative vehicle counts.
df = df[
    (df["Number_of_Roads"] > 0)
    & (df["Number_of_Lanes"] > 0)
    & (df["Vehicles_Observed"] >= 0)
].copy()

print("\nDataset shape after checks:", df.shape)
print("Missing values after cleaning:", int(df.isnull().sum().sum()))
print("Duplicate rows after cleaning:", int(df.duplicated().sum()))

# Save the validated dataset used for this analysis.
cleaned_output = OUTPUT_DIR / "Cleaned_Smart_Traffic_validated.xlsx"
df.to_excel(cleaned_output, index=False)
print(f"\nValidated dataset saved to: {cleaned_output}")

# 3. Descriptive statistics
print("\nNumeric summary:")
print(df[["Number_of_Roads", "Number_of_Lanes", "Vehicles_Observed"]].describe())

traffic_count = df["Traffic_Level"].value_counts()
city_vehicles = df.groupby("City")["Vehicles_Observed"].sum().sort_index()
time_traffic = df.groupby("Time_Period")["Vehicles_Observed"].sum().sort_index()
intersection_traffic = df.groupby("Intersection")["Vehicles_Observed"].sum().sort_index()
average_vehicles = df.groupby("City")["Vehicles_Observed"].mean().sort_index()
city_traffic = pd.crosstab(df["City"], df["Traffic_Level"])
time_level = pd.crosstab(df["Time_Period"], df["Traffic_Level"])

# Helper to save each chart consistently.
def save_chart(filename):
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# 4. Traffic level analysis
print("\nTraffic level counts:")
print(traffic_count)
traffic_count.plot(kind="bar", figsize=(7, 5))
plt.title("Traffic Level Analysis")
plt.xlabel("Traffic Level")
plt.ylabel("Number of Observations")
save_chart("01_traffic_level_analysis.png")

# 5. City-wise vehicle count
print("\nCity-wise total vehicles:")
print(city_vehicles)
city_vehicles.plot(kind="bar", figsize=(7, 5))
plt.title("City-wise Vehicle Count")
plt.xlabel("City")
plt.ylabel("Total Vehicles Observed")
save_chart("02_city_wise_vehicle_count.png")

# 6. Peak vs Off-Peak traffic
print("\nVehicles by time period:")
print(time_traffic)
time_traffic.plot(kind="bar", figsize=(7, 5))
plt.title("Peak vs Off-Peak Traffic")
plt.xlabel("Time Period")
plt.ylabel("Total Vehicles Observed")
save_chart("03_peak_vs_off_peak_traffic.png")

# 7. Intersection-wise traffic
print("\nIntersection-wise vehicle count:")
print(intersection_traffic)
intersection_traffic.plot(kind="bar", figsize=(10, 5))
plt.title("Intersection-wise Traffic Analysis")
plt.xlabel("Intersection")
plt.ylabel("Vehicles Observed")
plt.xticks(rotation=45, ha="right")
save_chart("04_intersection_wise_traffic.png")

# 8. Average vehicles by city
print("\nAverage vehicles by city:")
print(average_vehicles)
average_vehicles.plot(kind="bar", figsize=(7, 5))
plt.title("Average Vehicles by City")
plt.xlabel("City")
plt.ylabel("Average Vehicles")
save_chart("05_average_vehicles_by_city.png")

# 9. Traffic level by city
print("\nTraffic level by city:")
print(city_traffic)
city_traffic.plot(kind="bar", figsize=(8, 5))
plt.title("Traffic Level by City")
plt.xlabel("City")
plt.ylabel("Number of Observations")
plt.xticks(rotation=0)
plt.legend(title="Traffic Level")
save_chart("06_traffic_level_by_city.png")

# 10. Roads vs observed vehicles
plt.figure(figsize=(7, 5))
plt.scatter(df["Number_of_Roads"], df["Vehicles_Observed"])
plt.title("Number of Roads vs Vehicles Observed")
plt.xlabel("Number of Roads")
plt.ylabel("Vehicles Observed")
save_chart("07_roads_vs_vehicles.png")

correlation = df["Number_of_Roads"].corr(df["Vehicles_Observed"])
print("\nCorrelation between number of roads and vehicles observed:", correlation)
print("Note: Correlation describes association; it does not prove causation.")

# 11. Traffic level distribution
traffic_count.plot(kind="pie", autopct="%1.1f%%", figsize=(7, 5))
plt.title("Traffic Level Distribution")
plt.ylabel("")
save_chart("08_traffic_level_distribution.png")

# 12. Traffic level vs time period
time_level.plot(kind="bar", figsize=(8, 5))
plt.title("Traffic Level vs Time Period")
plt.xlabel("Time Period")
plt.ylabel("Number of Observations")
plt.xticks(rotation=0)
plt.legend(title="Traffic Level")
save_chart("09_traffic_level_vs_time_period.png")

# 13. Final summary
summary = [
    "SMART TRAFFIC MANAGEMENT - ANALYSIS SUMMARY",
    f"Total records analysed: {len(df)}",
    f"Cities covered: {df['City'].nunique()}",
    f"Intersections represented: {df['Intersection'].nunique()}",
    f"Average vehicles observed: {df['Vehicles_Observed'].mean():.2f}",
    f"Maximum vehicles observed: {df['Vehicles_Observed'].max():.0f}",
    f"Minimum vehicles observed: {df['Vehicles_Observed'].min():.0f}",
    f"Correlation (roads and vehicles): {correlation:.3f}",
    "",
    "Traffic level counts:",
    traffic_count.to_string(),
    "",
    "City-wise vehicle totals:",
    city_vehicles.to_string(),
    "",
    "Vehicles by time period:",
    time_traffic.to_string(),
]
summary_text = "\n".join(summary)
print("\n" + summary_text)

summary_file = OUTPUT_DIR / "analysis_summary.txt"
summary_file.write_text(summary_text, encoding="utf-8")

print(f"\nAll charts and summary saved in: {OUTPUT_DIR}")
print("DATA ANALYSIS COMPLETED SUCCESSFULLY!")
