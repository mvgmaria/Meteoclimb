import os
import pandas as pd


# This script is an addition that i made after all of the scraping, to get a more clear view of the regions csv (it gets the name of the regions and puts it in the second column)

base_dir = os.path.dirname(os.path.abspath(__file__))
main_csv = os.path.join(base_dir, "regions_csv\_crag_coordinates.csv")
output_file = main_csv.replace("_crag_coordinates.csv", "_crag_coordinates_new.csv")
regions_csv = os.path.join(base_dir, "spain_regions_urls_names.csv")

df_main = pd.read_csv(main_csv, sep="\t")
df_region = pd.read_csv(regions_csv)
df_main_ = pd.DataFrame(df_main)
df_region_ = pd.DataFrame(df_region)


region_dict = df_region_.set_index("Region URLs")["Initial region Names"].to_dict()
print(region_dict)

region_name_list = []

for i, row in df_main_.iterrows():
    # print(f"This is i: {str(i)}")
    # print(f"This is row: {str(row)}")
    url = row["Initial Region URL"]
    # print(url)
    if url in region_dict:
        # print("True")
        region_name_list.append(region_dict[url])

print(region_name_list)

df_main_.insert(0, "Initial Region Name", region_name_list)

df_main_.to_csv(output_file, index=False)
