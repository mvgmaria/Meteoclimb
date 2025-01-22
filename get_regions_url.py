from bs4 import BeautifulSoup
import requests
import pandas as pd
import os


# Lists to store URLs
region_urls = []


# Scrape region URLs
def get_region_urls():
    page = requests.get("https://www.thecrag.com/climbing/spain")
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find_all("div", class_="node-listview hide-archived")

    for row in table:
        class_name = row.find_all("div", class_="name")
        # print(class_name)
        for line in class_name:
            a_tag = line.find_all("a")
            # print(a_tag)
            for line2 in a_tag:
                region_url = line2.get("href")
                complete_region_url = "https://www.thecrag.com" + region_url
                region_urls.append(complete_region_url)
    return region_urls


# Scraping process
print("Scraping region URLs...")


if __name__ == "__main__":
    region_urls = get_region_urls()

    # Creating DataFrames
    df_regions = pd.DataFrame({"Region URLs": region_urls})

    # Defining file paths
    output_dir = r"C:\Users\María\Dropbox\PYTHON\PY\CLIMB\.climbproject"
    region_file = os.path.join(output_dir, "spain_region_urls.csv")

    # Saving to CSV
    df_regions.to_csv(region_file, index=False, sep="\t")

    # Printing for verification
    print(f"Region URLs saved to: {region_file}")
