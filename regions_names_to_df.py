import os
import pandas as pd


# This script is an addition that i made after all of the scraping, to get a more clear view of the regions csv (it gets the name of the regions and puts it in the second column)

base_dir = os.path.dirname(os.path.abspath(__file__))
main_csv = os.path.join(base_dir, "regions_csv\_crag_coordinates.csv")
output_file = main_csv.replace("_crag_coordinates.csv", "_crag_coordinates_new.csv")
regions_csv = os.path.join(base_dir, "spain_regions_urls_names.csv")

df_main = pd.read_csv(main_csv)
df_region = pd.read_csv(regions_csv)
df_main_ = pd.DataFrame(df_main)
df_region_ = pd.DataFrame(df_region)
print(df_region_.columns)

region_dict = df_region_.set_index("Initial region Names")["Region URLs"].to_dict()

for i, row in df_main_.iterrows():
    url = row[
        "Initial Region URL"
    ]  # Asumiendo que esta columna contiene las URLs en df_main
    if url in region_dict:
        df_main_.at[i, "Region Name"] = region_dict[
            url
        ]  # Asignar el nombre de la región

df_main_.to_csv(output_file, index=False)
