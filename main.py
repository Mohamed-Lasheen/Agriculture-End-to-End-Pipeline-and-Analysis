import re
import numpy as np
import pandas as pd
import logging
from scipy.stats import ttest_ind
from field_data_processor import FieldDataProcessor
from weather_data_processor import WeatherDataProcessor
from data_analysis import univariate_analysis, bivariate_analysis, multivariate_analysis

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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
    "values_to_rename": {'cassaval': 'cassava', 'wheatn': 'wheat', 'teaa': 'tea', 'tea ': 'tea', 'wheat ': 'wheat', 'cassava ': 'cassava'}, 
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
print(field_df.info())

#print(field_df.head())
#print(weather_df['Measurement'].unique())
#print(weather_df.head())
#print(weather_df[weather_df['Measurement']== 'Pollution_level'])



# Now, the measurements_to_compare can directly use 'Temperature', 'Rainfall', and 'Pollution_level'
#measurements_to_compare = ['Temperature', 'Rainfall', 'Pollution_level']
#hypothesis_results(field_df, weather_df, measurements_to_compare)

#bivariate_analysis
field_df.drop("Field_ID", axis=1, inplace=True)

print(field_df.info())
print(field_df.head())
univariate_analysis(field_df)
#bivariate_analysis(field_df)
#multivariate_analysis(field_df)
#print(field_df.describe())

