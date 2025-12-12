import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from helper_functions import create_subplots, count_rows, clean_name, clean_titles_dictionary, filter_field_data, ranges
from plotly.offline import plot

#region Plots

def violin_plots(df, mode: str = None, x: str = "", y: str = "", z: str = ""):
    """
    Create violin plots for univariate, bivariate, or multivariate analysis.
    
    Args:
        df: DataFrame containing the data
        mode: Analysis type - 'univariate', 'bivariate', or 'multivariate'
        x: Variable for x-axis
        y: Variable for y-axis 
        z: Variable for grouping 
    """
    titles = {"x": x}
    fig = None
    if mode == "U":
        titles = clean_titles_dictionary(titles)
        fig = go.Figure()
        fig.add_trace(go.Violin(y=df[x], showlegend=False, name=x))
        title = f"Understanding the Spread of {titles['x']}"

    elif mode == "B":
        titles.update({"y": y})
        titles = clean_titles_dictionary(titles)
        unique_groups = df[x].unique()
        fig = go.Figure() 
        for index, item in enumerate(unique_groups):
            data = go.Violin(
                x=df[x][df[x] == item],
                y=df[y][df[x] == item],
                name=clean_name(str(item)),
            )
            fig.add_trace(data)
        title = f"Distribution of {titles['y']} by {titles['x']}"
        
    elif mode == "M":
        titles.update({"y": y, "z": z})
        titles = clean_titles_dictionary(titles)
        fig = px.violin(df, x=x, y=y, color=z)
        title = f"How {titles['z']} Affects {titles['y']} Across Different {titles['x']} Groups"
    
    fig.update_traces(box_visible=True, meanline_visible=True)
    fig.update_layout(
        height=600,
        title=title,
        showlegend=True
    )
    fig.update_xaxes(title_text=titles['x'])
    fig.update_yaxes(title_text=titles['y'] if mode != "U" else titles['x'])
    return fig
    
def count_plots(df, mode: str = None, x: str = "", y: str = "", z: str = "", order_dict: dict = None):
    """
    Create count plots for univariate, bivariate, or multivariate analysis.
    
    Args:
        df: DataFrame containing the data
        x: Variable for x-axis
        y: Variable for y-axis
        z: Variable for grouping
        mode: Analysis type - 'univariate', 'bivariate', or 'multivariate'
        """
    titles = {"x": x}
    fig = None
    if mode == "U":
        titles = clean_titles_dictionary(titles)
        fig = px.histogram(df, 
                    x=x, 
                    text_auto=True, 
                    color_discrete_sequence=px.colors.qualitative.Set2)
        title = f"Frequency of {titles['x']}"

    elif mode == "B":
        titles.update({"y": y})
        titles = clean_titles_dictionary(titles)
        fig = px.histogram(df, 
                        x=x, 
                        text_auto=True, 
                        color=y,
                        barmode='stack',
                        color_discrete_sequence=px.colors.qualitative.Set2)
        title = f"Frequency of {titles['y']} by {titles['x']}"
        
    fig.update_layout(
        height=600,
        title=title,
        showlegend=True
    )
    fig.update_xaxes(title_text=titles['x'], categoryorder="total descending")
    fig.update_yaxes(title_text=titles['y'] if mode != "U" else titles['x'])
    return fig
        
def scatter_plots(df, mode: str = None, x: str = "", y: str = "", z: str = "", order_dict: dict = None):
    titles = {"x": x, "y": y}
    fig = None
    if mode == "B":
        titles = clean_titles_dictionary(titles)
        fig = px.scatter(df, 
                        x=x,
                        y=y,  
                        color_discrete_sequence=px.colors.qualitative.Set2)
        title = f"The Distribution of {titles['y']} by {titles['x']}"

    elif mode == "M":
        titles.update({"z": z})
        titles = clean_titles_dictionary(titles)
        fig = px.scatter(df, 
                        x=x,
                        y=y,
                        color=z,
                        color_discrete_sequence=px.colors.qualitative.Set2)
        title = f"The Distribution of {titles['y']} by {titles['x']} Separated by {titles['z']}"
        
    fig.update_layout(
        height=600,
        title=title,
        showlegend=True
    )
    fig.update_xaxes(title_text=titles['x'])
    fig.update_yaxes(title_text=titles['y'])
    return fig
    
#endregion

def univariate_analysis(df):
    numeric_cols = [col for col in df.select_dtypes(exclude='object').columns]        
    categorical_cols = [col for col in df.select_dtypes(include='object').columns if col != 'Field_ID']
    
    subplot_titles = [f"Distribution of {clean_name(col)}" for col in numeric_cols]
    fig, num_subplots = setup_subplots(numeric_cols, subplot_titles)
    
    for i, column in enumerate(numeric_cols):
        subplot = px.box(df, y=column, color_discrete_sequence=px.colors.qualitative.Set2)
        for trace in subplot.data:
            fig.add_trace(trace, row=i+1, col=1)
        fig = figure_adjustment(fig, column, None, 'Feature Distributions', 
                                i, num_subplots, height=850)

    fig.show()

    subplot_titles = [f"Distribution of {clean_name(col)}" for col in categorical_cols]
    fig, num_subplots = setup_subplots(categorical_cols, subplot_titles)
    
    for i, column in enumerate(categorical_cols):
        grouped_df = df.groupby(by=[column]).size().reset_index(name="counts")
        subplot= px.bar(grouped_df, x=column, y="counts")    
        for trace in subplot.data:
            fig.add_trace(trace, row=i+1, col=1)
        fig = figure_adjustment(fig, column, None, 'Feature Distributions', 
                        i, num_subplots)
        fig.update_layout(bargap=0.2)
    fig.show()

def bivariate_analysis(df):
    numerical_column = [col for col in df.select_dtypes(exclude='object').columns]
    categorical_column = [col for col in df.select_dtypes(include='object').columns if col != 'Field_ID']
    
    for column in numerical_column:    
        numeric_cols = [col for col in numerical_column if col != column]    
        subplot_titles = [f"Distribution of {column} by {clean_name(col)}" for col in numeric_cols]
        fig, num_subplots = setup_subplots(numeric_cols, subplot_titles)
        
        for i, feature in enumerate(numeric_cols):
            subplot = px.scatter(df, x=feature, y=column, color_discrete_sequence=px.colors.qualitative.Set2)
            for trace in subplot.data:
                fig.add_trace(trace, row=i+1, col=1) 
            fig = figure_adjustment(fig, feature, column, f"Distribution of {column}", i, num_subplots)
        fig.show()
        
        subplot_titles = [f"Distribution of {column} by {clean_name(col)}" for col in categorical_cols]
        fig, num_subplots = setup_subplots(categorical_cols, subplot_titles)
        
        for i, feature in enumerate(categorical_cols):
            subplot = px.violin(df, y=column, x=feature)
            for trace in subplot.data:
                fig.add_trace(trace, row=i+1, col=1)
            fig = figure_adjustment(fig, feature, column, f"Distribution of {column}", i, num_subplots)
        fig.show()

    for column in categorical_column:    
        categorical_cols = [col for col in df.select_dtypes(include='object').columns 
                if col != 'Field_ID']
    
        subplot_titles = [f"Distribution of {column} by {clean_name(col)}" for col in numeric_cols]
        fig, num_subplots = setup_subplots(numeric_cols, subplot_titles)
        
        for i, feature in enumerate(numeric_cols):
            subplot = px.scatter(df, x=feature, y=column, color_discrete_sequence=px.colors.qualitative.Set2)
            for trace in subplot.data:
                fig.add_trace(trace, row=i+1, col=1) 
            fig = figure_adjustment(fig, feature, column, f"Distribution of {column}", i, num_subplots)
        fig.show()
        
        subplot_titles = [f"Distribution of {column} by {clean_name(col)}" for col in categorical_cols]
        fig, num_subplots = setup_subplots(categorical_cols, subplot_titles)
        
        for i, feature in enumerate(categorical_cols):
            subplot = px.violin(df, y=column, x=feature)
            for trace in subplot.data:
                fig.add_trace(trace, row=i+1, col=1)
            fig = figure_adjustment(fig, feature, column, f"Distribution of {column}", i, num_subplots)
        fig.show()
def multivariate_analysis(df):
    figure_list = []
    # Key triplets with Annual_yield as target
    figure_list.append(scatter_plots(df, "M", "Rainfall", "Annual_yield", "Crop_type"))
    figure_list.append(scatter_plots(df, "M", "Temperature", "Annual_yield", "Crop_type"))
    figure_list.append(scatter_plots(df, "M", "Soil_fertility", "Annual_yield", "Crop_type"))
    figure_list.append(scatter_plots(df, "M", "pH", "Annual_yield", "Soil_type"))
    figure_list.append(scatter_plots(df, "M", "Pollution_level", "Annual_yield", "Soil_type"))
    figure_list.append(scatter_plots(df, "M", "Elevation", "Annual_yield", "Location"))

    # Environmental relationships
    figure_list.append(scatter_plots(df, "M", "Rainfall", "Temperature", "Crop_type"))
    figure_list.append(scatter_plots(df, "M", "Elevation", "Temperature", "Location"))
    figure_list.append(scatter_plots(df, "M", "Latitude", "Rainfall", "Crop_type"))
    figure_list.append(scatter_plots(df, "M", "Soil_fertility", "pH", "Soil_type"))

    # Multi-category distributions
    figure_list.append(violin_plots(df, "M", "Crop_type", "Annual_yield", "Soil_type"))
    figure_list.append(violin_plots(df, "M", "Location", "Annual_yield", "Crop_type"))
    figure_list.append(violin_plots(df, "M", "Soil_type", "Annual_yield", "Crop_type"))
    figure_list.append(violin_plots(df, "M", "Crop_type", "Annual_yield", "Soil_type"))

    # Complex interactions
    figure_list.append(scatter_plots(df, "M", "Rainfall", "Soil_fertility", "Crop_type"))
    figure_list.append(scatter_plots(df, "M", "Temperature", "pH", "Soil_type"))
    figure_list.append(scatter_plots(df, "M", "Plot_size", "Annual_yield", "Crop_type"))
    figure_list.append(scatter_plots(df, "M", "Min_temperature_C", "Max_temperature_C", "Crop_type"))

    for fig in figure_list:
        fig.show()
        
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

def figure_adjustment(fig, x, y, plot_title, i, num_subplots, height=550, width=1000):
    

    fig.update_xaxes(title_text=clean_name(x), row=i+1, col=1)
    fig.update_yaxes(title_text=clean_name(y), row=i+1, col=1)
    
  
    fig.update_layout(
        height=height * num_subplots,
        width=width, 
        title_text=plot_title,
        showlegend=True
    )
    return fig

def setup_subplots(columns, subplot_titles):
    num_subplots = len(columns)
    fig = make_subplots(
    rows=num_subplots, 
    cols=1,
    subplot_titles=subplot_titles
    )
    return fig, num_subplots