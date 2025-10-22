import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from helper_functions import create_subplots, count_rows, clean_name, clean_titles_dictionary, filter_field_data

#region Plots

def bivariate_violin_plots(df, x, y, n_rows: int = 2, n_cols: int = 1):
    titles = {"x": x, "y": y}
    titles = clean_titles_dictionary(titles)
    unique_groups = df[x].unique()
    fig = go.Figure() 
    for index, item in enumerate(unique_groups):
        unique_groups[index] = clean_name(item)
        data = go.Violin(x=df[x][df[x] == item],
                    y=df[y][df[x] == item],
                    showlegend=False
                    )
        fig.add_trace(data)
    fig.update_traces(box_visible=True, meanline_visible=True)
    fig.update_layout(
        height=300 * n_rows,
        title=f"Violin Plot of {titles['y']} by {titles['x']}",
        showlegend=False
    )
    fig.update_xaxes(title_text=titles['x'])
    fig.update_yaxes(title_text=titles['y'])

    fig.show()

def univariate_violin_plots(df, x, n_rows: int = 2, n_cols: int = 1):
    titles = {"x": x}
    titles = clean_titles_dictionary(titles)
    fig = go.Figure() 
    data = go.Violin(x=df[x],
                    showlegend=False
                    )
    fig.add_trace(data)
    fig.update_traces(box_visible=True, meanline_visible=True)
    fig.update_layout(
        height=300 * n_rows,
        title=f"Violin Plot of {titles['x']}",
        showlegend=False
    )
    fig.update_xaxes(ticktext=titles['x'])

    fig.show()
    
def univariate_count_plots(df, x, n_rows: int = 2, n_cols: int = 1):
    titles = {"x": x}
    titles = clean_titles_dictionary(titles)

    fig = px.histogram(df, x=x, text_auto=True)
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Frequency = %{y}<extra></extra>')
    fig.update_layout(
        height=300 * n_rows,
        title=f"Count Plot of {titles['x']}",
        showlegend=False,
        bargap=0.2
    )
    fig.update_xaxes(title_text=titles['x'])
    fig.update_yaxes(title_text='Frequency')
    fig.show()
    
def show_grouped_scatter(df, x, y, group_by, n_cols=2):
    
    titles = {"x": x, "y": y, "group_by": group_by}
    titles = clean_titles_dictionary(titles)
    
    unique_groups = df[group_by].unique()
    n_rows = count_rows(n_groups=len(unique_groups))
    
    fig = create_subplots(unique_groups=unique_groups,
                          groups=titles['group_by'],
                          n_rows=n_rows)

    
    for i, group in enumerate(unique_groups):
        row = i // n_cols + 1
        col = i % n_cols + 1
        
        group_data = df[df[group_by] == group]
        
        fig.add_trace(
            go.Scatter(
                x=group_data[x],
                y=group_data[y],
                mode='markers',
                name=str(clean_name(group)),
                showlegend=False
            ),
            row=row, 
            col=col
        )
    
    fig.update_layout(
        height=300 * n_rows,
        title=f"Scatter Plots of {titles['y']} vs {titles['x']} by {titles['group_by']}",
        showlegend=False
    )
    
    fig.update_xaxes(title_text=titles['x'])
    fig.update_yaxes(title_text=titles['y'])
    
    fig.show()

#endregion

def univariate_analysis(df):
    #show_grouped_histograms(df, 'Soil_type', 'Crop_type')
    """
    univariate_violin_plots(df, 'Standard_yield')
    univariate_violin_plots(df, 'Annual_yield')
    univariate_violin_plots(df, 'Min_temperature_C')
    univariate_violin_plots(df, 'Max_temperature_C')
    univariate_violin_plots(df, 'Temperature')
    univariate_violin_plots(df, 'pH')
    univariate_violin_plots(df, 'Rainfall')
    univariate_violin_plots(df, 'Soil_fertility')
    univariate_violin_plots(df, 'Slope')"""
    univariate_count_plots(df, 'Location')
    univariate_count_plots(df, 'Weather_station')
    univariate_count_plots(df, 'Crop_type')
    univariate_count_plots(df, 'Soil_type')

def bivariate_analysis(df):
    bivariate_violin_plots(df, 'Crop_type', 'Pollution_level')
    bivariate_violin_plots(df, 'Soil_type', 'Pollution_level')
    #show_grouped_scatter(df, 'Min_temperature_C', 'Standard_yield', 'Crop_type')
    #show_grouped_scatter(df, 'Max_temperature_C', 'Standard_yield', 'Crop_type')
    
    #show_grouped_scatter(df, 'Min_temperature_C', 'Annual_yield', 'Crop_type')
    #show_grouped_scatter(df, 'Max_temperature_C', 'Annual_yield', 'Crop_type')
    
    #show_grouped_scatter(df, 'Soil_type', 'Standard_yield', 'Crop_type')
    #show_grouped_scatter(df, 'Min_temperature_C', 'Standard_yield', 'Soil_type')
    #show_grouped_scatter(df, 'Max_temperature_C', 'Standard_yield', 'Soil_type')


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
            #weather_data = filter_weather_data(weather_df, station_id, measurement)
            # Get field data for current station and measurement
            field_data = filter_field_data(field_df, station_id, measurement)
            
            # Perform t-test
            #t_stat, p_val = run_ttest(weather_data, field_data)
            
            # Print results
            #print_ttest_results(station_id, measurement, p_val, alpha)