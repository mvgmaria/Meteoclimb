import os
import pandas as pd

# Directory where all your individual CSV files are stored
base_dir = os.path.dirname(os.path.abspath(__file__))

csv_directory = os.path.join(base_dir, "regions_csv")

# Initialize an empty DataFrame to hold all data
all_data = pd.DataFrame()

# Iterate through all files in the directory
for file in os.listdir(csv_directory):
    if file.endswith(".csv"):  # Check if the file is a CSV
        file_path = os.path.join(csv_directory, file)

        # Read each CSV into a DataFrame
        df = pd.read_csv(file_path, sep="\t")

        # Append to the all_data DataFrame
        all_data = pd.concat([all_data, df], ignore_index=True)

# Save the concatenated data to a new CSV file
output_file = os.path.join(csv_directory, "_combined_crags.csv")
all_data.to_csv(output_file, index=False, sep="\t")

print(f"All CSV files have been concatenated into: {output_file}")
