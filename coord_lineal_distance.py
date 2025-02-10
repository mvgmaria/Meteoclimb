import pandas as pd
import numpy as np
import plotly.express as px

data = pd.read_csv(".txt")  # use the db

# we will have two sets of coords (lat and long) which would be the one from the crag and the one from my location (data type 'float')
# radius of the earth in km
R = 6371


# function to convert degree to radians
def deg_to_rad(degrees):
    return degrees * (np.pi / 180)


# function to calculate distance (1 or 2 could correspond to either of the locations)
def dist(lat1, lon1, lat2, lon2):
    # d stands for 'difference' in lat and in lon
    d_lat = deg_to_rad(lat2 - lat1)
    d_lon = deg_to_rad(lon2 - lon1)
    a = (
        np.sin(d_lat / 2) ** 2
        + np.cos(deg_to_rad(lat1)) * np.cos(deg_to_rad(lat2)) * np.sin(d_lon / 2) ** 2
    )
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c


# this creates another column in our data with the name distance, and the values in kilometers after the function
for i in range(len(data)):
    data.loc[i, "distance"] = (
        dist()
    )  # put the parameters in the function like so: data.loc[i, 'lat1 header name],  data.loc[i, 'lon1 header name], data.loc[i, 'lat2 header name],  data.loc[i, 'lon2 header name]
