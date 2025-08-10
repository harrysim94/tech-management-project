import os
import pandas as pd
import matplotlib.pyplot as plt

directory = os.path.dirname(os.path.abspath(__file__))

# Update file names to CSV files
files = ["intel_rev.csv", "amd_rev.csv", "nvidia_rev.csv"]

# Adjust figure size for half an A4 page
plt.figure(
    figsize=(8.27, 5.85)
)  # A4 dimensions in inches: 8.27 x 11.69, half page height

for file in files:
    path = os.path.join(directory, file)
    try:
        # Read CSV instead of Excel
        df = pd.read_csv(path)

        # Convert Year to numeric if it's not already
        df["Year"] = pd.to_numeric(df["Year"])

        # Get company name from filename
        company_name = os.path.splitext(file)[0].replace("_rev", "").upper()

        # Plot with improved styling
        plt.plot(df["Year"], df["Revenue"], marker="o", linewidth=2, label=company_name)

    except Exception as e:
        print(f"Error reading file {file}: {e}")

# Update font sizes for better readability
plt.xlabel("Year", fontsize=14)
plt.ylabel("Revenue (Billion USD)", fontsize=14)
plt.title("Company Revenue Comparison (2009-2024)", fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12)

# Improve grid visibility
plt.grid(True, linestyle="--", alpha=0.8)

# Tighten layout for better fit
plt.tight_layout(pad=2.0)

# Save the figure
plt.savefig(os.path.join(directory, "revenue_comparison.png"), dpi=300)

# Create a second figure for the percentage plot
plt.figure(
    figsize=(8.27, 5.85)
)  # A4 dimensions in inches: 8.27 x 11.69, half page height

# Dictionary to store dataframes by company
company_data = {}

# Read all data files first
for file in files:
    path = os.path.join(directory, file)
    try:
        df = pd.read_csv(path)
        df["Year"] = pd.to_numeric(df["Year"])
        company_name = os.path.splitext(file)[0].replace("_rev", "")
        company_data[company_name] = df
    except Exception as e:
        print(f"Error reading file {file}: {e}")

# Calculate percentage shares if we have all necessary data
if "intel" in company_data and "amd" in company_data and "nvidia" in company_data:
    # Find common years across all datasets
    intel_years = set(company_data["intel"]["Year"])
    amd_years = set(company_data["amd"]["Year"])
    nvidia_years = set(company_data["nvidia"]["Year"])
    common_years = sorted(intel_years.intersection(amd_years, nvidia_years))

    intel_percentages = []
    nvidia_percentages = []
    years = []

    for year in common_years:
        intel_rev = float(
            company_data["intel"]
            .loc[company_data["intel"]["Year"] == year, "Revenue"]
            .iloc[0]
        )
        amd_rev = float(
            company_data["amd"]
            .loc[company_data["amd"]["Year"] == year, "Revenue"]
            .iloc[0]
        )
        nvidia_rev = float(
            company_data["nvidia"]
            .loc[company_data["nvidia"]["Year"] == year, "Revenue"]
            .iloc[0]
        )

        total_rev = intel_rev + amd_rev + nvidia_rev

        if total_rev > 0:
            intel_percentage = (intel_rev / total_rev) * 100
            nvidia_percentage = (nvidia_rev / total_rev) * 100
        else:
            intel_percentage = nvidia_percentage = 0

        years.append(year)
        intel_percentages.append(intel_percentage)
        nvidia_percentages.append(nvidia_percentage)

    # Add AMD data to the plot
    amd_percentages = []

    for year in common_years:
        amd_rev = float(
            company_data["amd"]
            .loc[company_data["amd"]["Year"] == year, "Revenue"]
            .iloc[0]
        )
        total_rev = intel_rev + amd_rev + nvidia_rev

        if total_rev > 0:
            amd_percentage = (amd_rev / total_rev) * 100
        else:
            amd_percentage = 0

        amd_percentages.append(amd_percentage)

    # Update bar width and positions
    bar_width = 0.25
    x = range(len(years))

    # Create bars for AMD
    plt.bar(
        [i - bar_width for i in x],
        intel_percentages,
        bar_width,
        color="#0071C5",
        label="INTEL",
    )  # Intel blue
    plt.bar(
        x,
        amd_percentages,
        bar_width,
        color="grey",
        label="AMD",
    )  # AMD grey
    plt.bar(
        [i + bar_width for i in x],
        nvidia_percentages,
        bar_width,
        color="#76B900",
        label="NVIDIA",
    )  # Nvidia green

    # Add value labels on top of Intel and NVIDIA bars only
    # Reduce text size on the labels above the bars to 10
    for i, v in enumerate(intel_percentages):
        plt.text(i - bar_width, v + 1, f"{v:.1f}%", ha="center", fontsize=9)
    for i, v in enumerate(nvidia_percentages):
        plt.text(i + bar_width, v + 1, f"{v:.1f}%", ha="center", fontsize=9)

    # Set x-axis ticks and labels
    plt.xticks([i for i in x], years)

    # Update font sizes for better readability
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Percentage of Combined Rev.(%)", fontsize=14)
    # plt.title("Intel vs NVIDIA Revenue Percentage of Combined Revenue", fontsize=16)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)

    # Improve grid visibility
    plt.grid(True, axis="y", linestyle="--", alpha=0.8)

    # Tighten layout for better fit
    plt.tight_layout(pad=2.0)

    # Save this figure
    plt.savefig(os.path.join(directory, "intel_nvidia_percentage.png"), dpi=300)

# Show all plots
plt.show()
