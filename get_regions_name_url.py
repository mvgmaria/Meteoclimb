import os
import pandas as pd


# This script is an addition that i made after all of the scraping, to get a more clear view of the regions csv (it gets the name of the regions and puts it in the second column)

base_dir = os.path.dirname(os.path.abspath(__file__))
regions_csv = os.path.join(base_dir, "spain_region_urls.csv")
output_file = regions_csv.replace(
    "spain_region_urls.csv", "spain_regions_urls_names.csv"
)

df = pd.read_csv(regions_csv)
df_ = pd.DataFrame(df)

region_names = [
    "Andalucia",
    "Aragon",
    "Asturias",
    "Islas Baleares",
    "Islas Canarias",
    "Cantabria",
    "Castilla y Leon",
    "Castilla la Mancha",
    "Cataluña",
    "Comunidad Valenciana",
    "Extremadura",
    "Galicia",
    "Madrid",
    "Murcia",
    "Navarra",
    "Pais Vasco",
    "La Rioja",
]

df_.insert(1, "Initial region Names", region_names)

df_.to_csv(output_file, index=False)
