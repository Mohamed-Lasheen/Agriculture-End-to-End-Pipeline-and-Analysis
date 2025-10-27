import pandas as pd
import numpy as np
import re
import os
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def filter_field_data(df, column: str, filter: str):
    return df[(df[column] == filter)]

def filter_weather_data(df, station_id, measurement):
    return df[(df['Weather_station_ID'] == station_id) & (df['Measurement'] == 'Temperature')]['Value']

def create_subplots(unique_groups: list, groups: str, n_rows: int, n_cols: int=2):    
    fig = make_subplots(
    rows=n_rows, 
    cols=n_cols,
    subplot_titles=[f"{groups}: {clean_name(group)}" for group in unique_groups]
    )
    return fig

def clean_name(name):
    if (name.endswith("_C")):
        name = name.replace("_C", " (C)")
    return name.replace("_", " ").title()

def clean_titles_dictionary(titles):
    for key, value in titles.items():
        if value != np.float64(0.5779643636557995):
            titles[key] = clean_name(value)
    return titles

def count_rows(n_groups: int, n_cols: int=2):
    n_rows = (n_groups + n_cols - 1) // n_cols 
    return n_rows

