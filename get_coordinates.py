import os
import pandas as pd
import requests
import time
import random
from bs4 import BeautifulSoup

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))

csv_combined = os.path.join(base_dir, "regions_csv", "_combined_crags.csv")
output_file = csv_combined.replace("_combined_crags.csv", "_crag_names.csv") # the new outut path, replacing the name
proxy_file = os.path.join(base_dir, "valid_proxies.txt")

# Load proxies from file
def load_proxies():
    try:
        with open(proxy_file, "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print(f"Proxy file not found: {proxy_file}")
        return []


# List of user agents to rotate
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
]


# Get a random proxy
def get_random_proxy(proxies):
    if not proxies:
        return {}
    proxy = random.choice(proxies)
    parts = proxy.split(":")
    if len(parts) == 4:
        host, port, username, password = parts
        proxy_url = f"http://{username}:{password}@{host}:{port}"
        return {"http": proxy_url, "https": proxy_url}
    else:
        print("Invalid proxy format")
        return {}

# Function to scrape latitude and longitude from a URL
def scrape_coordinates_and_region_name(url, proxies):
    headers = {"User-Agent": random.choice(user_agents)}
    retries = 3
    delay = 30
    
    for attempt in range(retries):
        proxy = get_random_proxy(proxies)
        try:
            print(
                f"Scraping URL: {url} (Attempt {attempt + 1}/{retries}) using proxy: {proxy.get('http', 'None')}"
            )
            response = requests.get(url, headers=headers, proxies=proxy, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract latitude and longitude
            latitude_tag = soup.find("meta", {"property": "place:location:latitude"})
            longitude_tag = soup.find("meta", {"property": "place:location:longitude"})
            latitude = latitude_tag["content"] if latitude_tag else "unknown"
            longitude = longitude_tag["content"] if longitude_tag else "unknown"

            # Extract the region name (if available)
            region_name_tag = soup.find("span", class_="heading__t")
            region_name = (
                region_name_tag.get_text().strip() if region_name_tag else "unknown"
            )

            print(
                f"Coordinates found: Latitude: {latitude}, Longitude: {longitude}, Region Name: {region_name}"
            )
            return latitude, longitude, region_name

        except requests.exceptions.RequestException as e:
                print(f"Error while accessing {url}: {e}")
                time.sleep(delay)
            
        except Exception as e:
            print(f"An unexpected error occurred while accessing {url}: {e}")
            time.sleep(delay)


    print(f"Failed to scrape {url} after {retries} attempts.")
    return "unknown", "unknown", "unknown"


# Function to process URLs within a specified range
def process_urls(start_index=None, end_index=None):
    # Load existing data
    if os.path.exists(output_file):
        try:
            df_output = pd.read_csv(output_file, sep="\t", on_bad_lines="skip")
            if set(df_output.columns) != {
                "Initial Region URL",
                "Crag URL",
                "Region Name",
                "Latitude",
                "Longitude",
            }:
                print("Output file columns are incorrect. Reinitializing DataFrame.")
                df_output = pd.DataFrame(
                    columns=[
                        "Initial Region URL",
                        "Crag URL",
                        "Region Name",
                        "Latitude",
                        "Longitude",
                    ]
                )
        except pd.errors.ParserError as e:
            print(f"Error parsing output file: {e}")
            df_output = pd.DataFrame(
                columns=[
                    "Initial Region URL",
                    "Crag URL",
                    "Region Name",
                    "Latitude",
                    "Longitude",
                ]
            )
    else:
        df_output = pd.DataFrame(
            columns=[
                "Initial Region URL",
                "Crag URL",
                "Region Name",
                "Latitude",
                "Longitude",
            ]
        )

    # Load URLs to scrape
    try:
        df = pd.read_csv(csv_combined, sep="\t", on_bad_lines="skip")
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
        return

    if start_index is None:
        start_index = 0
    if end_index is None:
        end_index = len(df)

    proxies = load_proxies()
    updated_data_dict = {}

    for index in range(start_index, end_index):
        row = df.iloc[index]
        initial_region_url = row["Initial Region URL"]
        crag_url = row["Crag URL"]
        existing_row = df_output[df_output["Crag URL"] == crag_url]

        if not existing_row.empty:
            if (
                existing_row.iloc[0]["Latitude"] == "unknown"
                or existing_row.iloc[0]["Longitude"] == "unknown"
                or existing_row.iloc[0]["Region Name"] == "unknown"
            ):
                print(
                    f"Re-scraping URL: {crag_url} because coordinates or region were 'unknown'."
                )
            else:
                print(f"Skipping already processed URL: {crag_url}")
                continue

        latitude, longitude, region_name = scrape_coordinates_and_region_name(
            crag_url, proxies
        )
        updated_data_dict[crag_url] = {
            "Initial Region URL": initial_region_url,
            "Region Name": region_name,
            "Latitude": latitude,
            "Longitude": longitude,
        }

        print(
            f"Processed {crag_url}. Latitude: {latitude}, Longitude: {longitude}, Region Name: {region_name}"
        )

    if updated_data_dict:
        # Convert the updated data dictionary into a DataFrame
        new_df = pd.DataFrame.from_dict(updated_data_dict, orient="index").reset_index()
        new_df.columns = [
            "Crag URL",
            "Initial Region URL",
            "Region Name",
            "Latitude",
            "Longitude",
        ]

        # Find URLs that are completely new (i.e., not present in df_output)
        new_entries_df = new_df[~new_df["Crag URL"].isin(df_output["Crag URL"])]

        # Append new URLs to the existing df_output
        if not new_entries_df.empty:
            df_output = pd.concat([df_output, new_entries_df], ignore_index=True)

        # Now, update existing rows where coordinates or region name are "unknown"
        df_output = pd.merge(
            df_output, new_df, on="Crag URL", how="left", suffixes=("", "_new")
        )

        # Ensure "Initial Region URL", "Region Name", "Latitude", and "Longitude" are updated correctly
        df_output["Initial Region URL"] = df_output[
            "Initial Region URL_new"
        ].combine_first(df_output["Initial Region URL"])
        df_output["Region Name"] = df_output["Region Name_new"].combine_first(
            df_output["Region Name"]
        )
        df_output["Latitude"] = df_output["Latitude_new"].combine_first(
            df_output["Latitude"]
        )
        df_output["Longitude"] = df_output["Longitude_new"].combine_first(
            df_output["Longitude"]
        )

        # Drop temporary "_new" columns used for merging
        df_output.drop(
            columns=[
                "Initial Region URL_new",
                "Region Name_new",
                "Latitude_new",
                "Longitude_new",
            ],
            inplace=True,
        )

        # Save updated DataFrame to CSV
        df_output.to_csv(output_file, index=False, sep="\t")
        print("New data appended and saved.")

    print(
        f"URLs from {start_index} to {end_index} processed. Output saved to {output_file}"
    )



# Specify the range of URLs to process
start_index = 0  # Change this to the desired start index
end_index = 952  # Change this to the desired end index

# Run the process
process_urls(start_index, end_index)
