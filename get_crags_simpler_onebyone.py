import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

base_url = "https://www.thecrag.com"

# Initialize lists to store URLs and failed URLs
crag_urls_list = []
to_scrape_urls = []
failed_urls = []


# Function to get the initial region URL from the file
def get_initial_region_url(file_path):
    df = pd.read_csv(file_path)
    # Get the URL from the specific row (index 16, in this case)
    region_url = df.iloc[16, 0]  # assuming the URL is in the first column
    return region_url


def scrape_urls(urls_to_scrape):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    retries = 5
    delay = 30  # Increase delay between retries to 30 seconds

    def scrape_page(url):
        for attempt in range(retries):
            try:
                print(f"Scraping URL: {url} (Attempt {attempt + 1}/{retries})")
                page = requests.get(url, headers=headers, timeout=30)
                page.raise_for_status()
                soup = BeautifulSoup(page.text, "html.parser")
                table = soup.find_all("div", class_="node-listview hide-archived")

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
                                    crag_urls_list.append(complete_url)
                                    print(
                                        f"{type_name.capitalize()} URL found:",
                                        complete_url,
                                    )
                                elif type_name == "region":
                                    # If it's a sub-region, add it to the list to scrape
                                    to_scrape_urls.append(complete_url)
                                    print(f"Sub-region URL found:", complete_url)
                        else:
                            print("No type span found in url:", url)  # Debug print

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

    for url in urls_to_scrape:
        scrape_page(url)
        time.sleep(1)  # Adding delay between requests to avoid overloading the server


def main():
    # Directory and file paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, "spain_region_urls.csv")
    output_dir = os.path.join(current_dir, "regions_csv")

    # Create output directory if it doesn't  (should not be necessary after first run)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the initial region URL from the file
    initial_region_url = get_initial_region_url(input_file)
    to_scrape_urls.append(initial_region_url)

    # while there are urls in the list, it creates a copy of the list and then clears the first one, it then executes the scrape urls function in the copy. We do this because we are adding and removing items from the list, so it makes sense to iterate through one and then append the newfound subregions to a blank one, because these new elements wouldn't be accounted for in the original list that is being processed
    while to_scrape_urls:
        current_urls_to_scrape = to_scrape_urls[:]
        to_scrape_urls.clear()
        scrape_urls(current_urls_to_scrape)

    # Prepare data for saving
    crag_data = pd.DataFrame(crag_urls_list, columns=["Crag URL"])

    # Save crag URLs to CSV
    df_crags = pd.DataFrame(crag_data)
    region_name = initial_region_url.split("/")[
        -1
    ]  # the [-1] is referring to the last part of the slice, typically the name of the crag that is part of the url
    crag_file = os.path.join(output_dir, f"{region_name}.csv")
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
