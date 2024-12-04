import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

base_url = "https://www.thecrag.com"

# Initialize dictionaries to store URLs and list to store failed URLs
crag_urls_dict = {}
to_scrape_urls = []
failed_urls = []


# Function to get the initial region URL from the file
def get_initial_region_url(file_path):
    df = pd.read_csv(file_path)
    # Get the URL from the second row (index 1)
    region_url = df.iloc[16, 0]
    # assuming the URL is in the first column, first number is changed manually
    return region_url


def scrape_urls(urls_to_scrape):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    retries = 5
    delay = 30  # Increase delay between retries to 30 seconds

    def scrape_page(url, parent_region_url):
        for attempt in range(retries):
            try:
                print(f"Scraping URL: {url} (Attempt {attempt + 1}/{retries})")
                page = requests.get(url, headers=headers, timeout=30)
                page.raise_for_status()
                soup = BeautifulSoup(page.text, "html.parser")
                table = soup.find_all("div", class_="node-listview hide-archived")

                found_crag_or_area = False

                for row in table:
                    class_name = row.find_all("div", class_="name")
                    for line in class_name:
                        a_tag = line.find("a")
                        type_span = line.find("span", class_="type")
                        if type_span:
                            type_name = type_span.get_text().strip().lower()
                            if a_tag:
                                href = a_tag.get("href")
                                complete_url = base_url + href
                                if type_name in ["crag", "area"]:
                                    found_crag_or_area = True
                                    if parent_region_url not in crag_urls_dict:
                                        crag_urls_dict[parent_region_url] = []
                                    crag_urls_dict[parent_region_url].append(
                                        complete_url
                                    )
                                    print(
                                        f"{type_name.capitalize()} URL found:",
                                        complete_url,
                                    )  # Debug print
                                elif type_name == "region":
                                    # If it's not a crag, area, or unknown area, it's a sub-region
                                    to_scrape_urls.append(
                                        (complete_url, parent_region_url)
                                    )
                                    print(f"Sub-region URL found:", complete_url)
                                    print(
                                        f"Adding sub-region URL to scrape list: {complete_url}"
                                    )
                        else:
                            print("No type span found in url:", url)  # Debug print

                # If found crag or area, break out of retry loop
                if found_crag_or_area:
                    break

                # # Handle pagination (not necessary in my case)
                # next_page = soup.find("a", class_="next")
                # if next_page and next_page.get("href"):
                #     next_url = base_url + next_page.get("href")
                #     print(f"Found next page: {next_url}")
                #     scrape_page(next_url, parent_region_url)
                # break  # If successful, break out of retry loop
            except (requests.ConnectionError, requests.Timeout) as e:
                print(
                    f"Error while accessing {url}: {e}. Retrying... ({attempt + 1}/{retries})"
                )
                time.sleep(delay)
            except requests.exceptions.HTTPError as e:
                if page.status_code == 503:
                    print(
                        f"503 Error while accessing {url}: {e}. Retrying... ({attempt + 1}/{retries})"
                    )
                    time.sleep(delay)
                else:
                    print(f"HTTP error occurred while accessing {url}: {e}")
                    break
            except Exception as e:
                print(f"An unexpected error occurred while accessing {url}: {e}")
                break
        else:
            print(f"Failed to retrieve data from {url} after {retries} attempts.")
            failed_urls.append(url)

    # this for loop is the responsible for the iterations until the urls_to scrape is empty, using the scrape_page function logic
    for url, parent_region_url in urls_to_scrape:
        scrape_page(url, parent_region_url)
        time.sleep(1)  # Adding delay between requests to avoid overloading the server


def main():
    # Directory and file paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # __file__ is the current file being executed, the os.path.abspath() returns the abs path of that, and the os.path.dirname extracts the directory in which it is located
    input_file = os.path.join(current_dir, "spain_region_urls.csv")
    # the .join gets the full path with the correspondent "/"s, so it has the path to the regions csv file
    output_dir = os.path.join(current_dir, "regions_csv")
    # same for the output, it signals the folder in which it will locate the files created

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the initial region URL from the file
    initial_region_url = get_initial_region_url(input_file)
    to_scrape_urls.append((initial_region_url, initial_region_url))

    while to_scrape_urls:
        current_urls_to_scrape = to_scrape_urls[:]
        to_scrape_urls.clear()
        scrape_urls(current_urls_to_scrape)

    # Prepare data for saving
    crag_data = []
    for region, crags in crag_urls_dict.items():
        for crag in crags:
            crag_data.append({"Initial Region URL": region, "Crag URL": crag})

    # Save crag URLs to CSV
    df_crags = pd.DataFrame(crag_data)
    region_name = initial_region_url.split("/")[-1]
    crag_file = os.path.join(output_dir, f"{region_name}_crag_urls.csv")
    df_crags.to_csv(crag_file, index=False, sep="\t")
    print(f"Crag URLs saved to: {crag_file}")

    # Save failed URLs to CSV
    failed_file = os.path.join(output_dir, "failed_urls.csv")
    if os.path.exists(failed_file):
        df_failed = pd.read_csv(failed_file)
        df_failed_new = pd.DataFrame({"Failed URLs": failed_urls})
        df_failed_combined = (
            pd.concat([df_failed, df_failed_new])
            .drop_duplicates()
            .reset_index(drop=True)
        )
    else:
        df_failed_combined = pd.DataFrame({"Failed URLs": failed_urls})

    df_failed_combined.to_csv(failed_file, index=False, sep="\t")
    print(f"Failed URLs saved to: {failed_file}")


if __name__ == "__main__":
    main()
