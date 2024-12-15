import os
import pandas as pd
import requests
import random

# import get_region_crag_names as gr
from bs4 import BeautifulSoup

# Paths

base_dir = os.path.dirname(os.path.abspath(__file__))
regions_csv = os.path.join(base_dir, "spain_region_urls.csv")
output_file = regions_csv.replace(
    "spain_region_urls.csv", "spain_regions_urls_names.csv"
)

df = pd.read_csv(regions_csv)
df_ = pd.DataFrame(df)
print(df_)

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
print(df_)

df_.to_csv(output_file)
