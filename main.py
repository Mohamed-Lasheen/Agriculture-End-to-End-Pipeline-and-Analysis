import re
import numpy as np
import pandas as pd
import logging
from scipy.stats import ttest_ind
from field_data_processor import FieldDataProcessor
from weather_data_processor import WeatherDataProcessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def filter_field_data(df, station_id, measurement):
    return df[(df['Weather_station'] == station_id)][measurement]

def filter_weather_data(df, station_id, measurement):
    return df[(df['Weather_station_ID'] == station_id) & (df['Measurement'] == 'Temperature')]['Value']

def run_ttest(Column_A, Column_B):  
    from scipy import stats  
    t_statistic, p_value = stats.ttest_ind(Column_A, Column_B, equal_var=False)

    return (t_statistic, p_value)

def print_ttest_results(station_id, measurement, p_val, alpha):
    if p_val < alpha:
        print(f"   Significant difference in {measurement} detected at Station  {station_id}, (P-Value: {p_val:.5f} < {alpha}). Null hypothesis rejected.")
    else:
        print(f"   No significant difference in {measurement} detected at Station  {station_id}, (P-Value: {p_val:.5f} > {alpha}). Null hypothesis not rejected.")

def hypothesis_results(field_df, weather_df, list_measurements_to_compare, alpha = 0.05):
    for station_id in field_df['Weather_station'].unique():
        print("-"*50)
        print(f"Station ID: {station_id}")
        for measurement in list_measurements_to_compare:
            # Get weather data for current station and measurement
            weather_data = filter_weather_data(weather_df, station_id, measurement)
            # Get field data for current station and measurement
            field_data = filter_field_data(field_df, station_id, measurement)
            
            # Perform t-test
            t_stat, p_val = run_ttest(weather_data, field_data)
            
            # Print results
            print_ttest_results(station_id, measurement, p_val, alpha)

patterns = {
    'Rainfall': r'(\d+(\.\d+)?)\s?mm',
    'Temperature': r'(\d+(\.\d+)?)\s?C',
    'Pollution_level': r'=\s*(-?\d+(\.\d+)?)|Pollution at \s*(-?\d+(\.\d+)?)'
}

config_params = {
    "sql_query": """
            SELECT *
            FROM geographic_features
            LEFT JOIN weather_features USING (Field_ID)
            LEFT JOIN soil_and_crop_features USING (Field_ID)
            LEFT JOIN farm_management_features USING (Field_ID)
            """,
    "db_path": 'sqlite:///Maji_Ndogo_farm_survey_small.db', 
    "columns_to_rename": {'Annual_yield': 'Crop_type', 'Crop_type': 'Annual_yield'},
    "values_to_rename": {'cassaval': 'cassava', 'wheatn': 'wheat', 'teaa': 'tea'}, 
    "weather_mapping_csv":"https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_data_field_mapping.csv",
    "weather_csv_path": "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_station_data.csv",
    "regex_patterns" : patterns
}

field_processor = FieldDataProcessor(config_params)
field_processor.process()
field_df = field_processor.df

weather_processor = WeatherDataProcessor(config_params)
weather_processor.process()
weather_df = weather_processor.weather_df

# Rename 'Ave_temps' in field_df to 'Temperature' to match weather_df
field_df.rename(columns={'Ave_temps': 'Temperature'}, inplace=True)

print(field_df.head())
print(weather_df['Measurement'].unique())
print(weather_df.head())
print(weather_df[weather_df['Measurement']== 'Pollution_level'])



# Now, the measurements_to_compare can directly use 'Temperature', 'Rainfall', and 'Pollution_level'
measurements_to_compare = ['Temperature', 'Rainfall', 'Pollution_level']
hypothesis_results(field_df, weather_df, measurements_to_compare)