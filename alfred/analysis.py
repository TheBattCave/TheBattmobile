import altair as alt
import csv
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import re
import shutil
import numpy as np
import os
from os import listdir
from sklearn.decomposition import PCA 

from .vis import label_bad_module, build_module_average_df

def count_swapped_modules(directory):
    """
    This function counts the number of swapped modules in a given directory.

    Parameters:
    directory (str): The directory where the modules are located.

    Returns:
    dict: A dictionary with keys as '0' and '1' representing good and bad modules respectively, 
          and values as the count of each type of module.
    """
    
    # Label modules that got swapped
    mod_labels = label_bad_module(directory) 

    # Track counts for module labels in vis_buses
    # Initialize a dictionary to store counts
    change_counts = {0: 0, 1: 0}

    # Iterate through each row in the DataFrame
    for index, row in mod_labels.iterrows():
        change_value = row['Change']
        if change_value in change_counts:
            change_counts[change_value] += 1

    # Print the total amount of module changes
    print("COUNT OF SWAPPED MODULES")
    for change_value, count in change_counts.items():
        print(f"Count of '{change_value}': {count}")
    print(" 0 = healthy and 1 = swapped")


def find_problem_buses(directory):
    """
    This function identifies problematic buses in a given directory, prints their file names
    and deletes them.

    Parameters:
    directory (str): The directory where the buses are located.

    Returns:
    tuple: A tuple containing two lists. The first list contains the problematic buses. 
           The second list contains the buses that are not problematic.
    """

    # Generate the list of bus numbers from the directory
    list_bus_nums = []
    for file in os.listdir(directory):
        if file.startswith('bus'):
            list_bus_nums.append(file)

    # Label modules that got swapped
    mod_labels = label_bad_module(directory)

    # Grab the whole "Bus" column from the target variable dataframe, as a list
    bus_list = mod_labels['Bus'].unique().tolist()

    # Check if this list of buses matches all of the buses in the directory
    if bus_list == list_bus_nums:
        print("VERIFIED: buses match healthy/swapped labels")
    else:
        print("UNVERIFIED: buses do not match healthy/swapped labels")

    # Find problem buses... ones that don't work with build_module_average_df
    prob_buses = []
    count = 0
    for bus in bus_list:
        for i in range(1, 17):
            try:
                result = build_module_average_df(directory, bus + '/', i)
            except Exception as e:
                count += 1
                prob_buses.append(bus)  # Add the problematic bus to the list
                break  # Stop further attempts for this bus and move to the next one

    print("Problematic buses:", prob_buses)
    print("Number of Problem Bus Instances: " + str(count))

    # Delete the directories of the problematic buses
    for bus in prob_buses:
        shutil.rmtree(os.path.join(directory, bus))


def standardize_columns(df):
        """
        This function standardizes the column names of a DataFrame.

        Parameters:
        df (pandas.DataFrame): The DataFrame whose columns need to be standardized.

        Returns:
        pandas.DataFrame: The DataFrame with standardized column names.
        """
        
        df.columns = df.columns.astype(str)  # Convert column names to strings
        df.columns = df.columns.str.replace('.0$', '', regex=True)  # Remove .0 at the end of column names
        
        return df


def build_all_voltages_df(directory):
    """
    This function builds a DataFrame containing all voltages for each bus and module in a given directory.

    Parameters:
    directory (str): The directory where the buses and modules are located.

    Returns:
    pandas.DataFrame: A DataFrame where each row corresponds to a voltage reading. The DataFrame includes 'Bus' and 'Module' columns.
    """
    
    # Grab the whole "Bus" column from the target variable dataframe, as a list
    mod_labels = label_bad_module(directory)
    bus_list = mod_labels['Bus'].unique().tolist()

    # Add 'Bus' and 'Module' columns
    volts = []
    bus_i_pairs = []

    # Iterate over each bus and module
    for bus in bus_list:
        for i in range(1, 17):
            ex = build_module_average_df(directory, bus + '/', i)
            standardize_columns(ex)
            volts.append(ex)
            # Get the number of rows in the DataFrame returned by build_module_average_df
            num_rows = ex.shape[0]
            
            # Create a list of (bus, i) pairs corresponding to the number of rows
            bus_i_pairs.extend([(bus, i)] * num_rows)

    # Concatenate all DataFrames in the list
    concatd = pd.concat(volts, ignore_index=True)
    concatd['Bus'] = [pair[0] for pair in bus_i_pairs]
    concatd['Module'] = [pair[1] for pair in bus_i_pairs]

    return concatd


def check_rows(mean_cent, tolerance=0.05):
    """
    This function checks for rows in a DataFrame that don't add up to one.

    Parameters:
    mean_cent (pandas.DataFrame): The DataFrame to be checked.
    tolerance (float, optional): The tolerance within which a row sum is considered to be roughly equal to 1. Defaults to 0.05.

    Returns:
    list: A list of row indices where the sum is not roughly equal to 1 within the specified tolerance.
    """
    
    # Check for rows that don't add up to one... they all contain zeros so everything is good
    check_for_zeros = mean_cent.copy()

    # List of voltage columns
    voltage_columns = ['< 2', '2', '2.2', '2.4', '2.6', '2.8', '3', '3.2', '3.4', '3.6', '3.8', '>= 4']

    # Calculate the sum of specified columns for each row
    row_sums = check_for_zeros[voltage_columns].sum(axis=1)

    # List to store row indices where sum is not roughly equal to 1
    false_rows = []

    # Check each row sum and collect indices where the condition is not met
    for idx, row_sum in enumerate(row_sums):
        is_roughly_equal_to_one = (row_sum >= (1 - tolerance)) and (row_sum <= (1 + tolerance))
        if not is_roughly_equal_to_one:
            false_rows.append(idx)

    # Print the contents of rows where the sum is not roughly equal to 1 within tolerance
    print("Contents of rows where sum is not roughly equal to 1 within tolerance:")
    for row_idx in false_rows:
        print(f"Row {row_idx + 1}:")
        print(check_for_zeros.iloc[row_idx])  # Access row by integer location (zero-based index)
        print()  # Print a blank line for separation

    return false_rows


def mean_center(directory):
    """
    This function performs mean centering on a DataFrame. It divides all second values in voltage columns by total seconds.

    Parameters:
    directory (str): The directory where the data files are located.

    Returns:
    tuple: A tuple containing three elements. The first element is a DataFrame where each row corresponds to a voltage reading. 
           The second element is an array of module labels. The third element is a list of labels ("Good" and "Bad").
    """
    
    # Generate DataFrame using build_all_voltages_df function
    concatd = build_all_voltages_df(directory)

    # Make a copy first
    mean_cent = concatd.copy()

    # List of voltage columns
    voltage_columns = ['< 2', '2', '2.2', '2.4', '2.6', '2.8', '3', '3.2', '3.4', '3.6', '3.8', '>= 4']

    # Perform data transformation: divide voltage columns by total seconds if total is not zero
    for idx, total_value in enumerate(mean_cent['TOTAL']):
        if total_value != 0:
            mean_cent.loc[idx, voltage_columns] = mean_cent.loc[idx, voltage_columns].div(total_value)

    # Label modules that got swapped
    mod_labels = label_bad_module(directory)

    return mean_cent, mod_labels, voltage_columns



def prepare_for_pca(directory):
    """
    This function prepares the data for Principal Component Analysis (PCA).

    Parameters:
    directory (str): The directory where the data files are located.

    Returns:
    tuple: A tuple containing three elements. The first element is a DataFrame where each row corresponds to a voltage reading. 
           The second element is an array of module labels. The third element is a list of labels ("Good" and "Bad").
    """
    
    # Call the mean_center function to get the DataFrame and module labels
    mean_cent, mod_labels, _ = mean_center(directory)

    # List of voltage columns
    voltage_columns = ['< 2', '2', '2.2', '2.4', '2.6', '2.8', '3', '3.2', '3.4', '3.6', '3.8', '>= 4']

    # Voltages for bus modules
    voltage_df = mean_cent[voltage_columns].copy()

    # Module labels
    label_array = mod_labels["Change"].values

    # 0 is good, 1 is bad
    labels = ["Healthy", "Swapped"]

    return voltage_df, label_array, labels


def find_num_components(directory, n_components=8):
    """
    This function performs Principal Component Analysis (PCA) on a given DataFrame and plots the cumulative explained variance.

    Parameters:
    voltage_df (pandas.DataFrame): The DataFrame on which PCA is to be performed.
    n_components (int, optional): The number of principal components to keep. Defaults to 4.

    Returns:
    tuple: A tuple containing two elements. The first element is the transformed data. 
           The second element is the cumulative explained variance.
    """
    # Call the prepare_for_pca function to get the DataFrame
    voltage_df, _, _ = prepare_for_pca(directory)
    
    # PCA initialization
    pca = PCA(n_components=n_components)

    # Fit the PCA model to the mean centered data 
    pca.fit(voltage_df)
    x_pca = pca.transform(voltage_df)

    # Calculate the cumulative explained variance
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)

    # Plot cumulative explained variance
    plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o', linestyle='--')
    plt.xlabel('Number of Components') 
    plt.ylabel('Cumulative Explained Variance') 
    plt.title('Explained Variance vs. Number of Components') 
    plt.show()



def perform_pca(directory, n_components=2):
    """
    This function performs Principal Component Analysis (PCA) on a given DataFrame.

    Parameters:
    directory (str): The directory where the data files are located.
    n_components (int, optional): The number of principal components to keep. Defaults to 2.

    Returns:
    tuple: A tuple containing three elements. The first element is the transformed data. 
           The second element is the explained variance ratio. 
           The third element is a DataFrame of component loadings.
    """
    
    # Call the prepare_for_pca function to get the DataFrame
    voltage_df, _, _ = prepare_for_pca(directory)

    # PCA initialization
    pca = PCA(n_components=n_components)

    # Fit the PCA model to the mean centered data 
    pca.fit(voltage_df)
    x_pca = pca.transform(voltage_df)

    # Explained variance ratio of the principal components
    explained_variance_ratio = pca.explained_variance_ratio_

    # Dynamically generate the column names for the component loadings
    component_names = [f'PC{i+1}' for i in range(n_components)]
    
    # Analyze principal component loadings
    component_loadings = pd.DataFrame(pca.components_.T, columns=component_names, index=voltage_df.columns)

    return x_pca, explained_variance_ratio, component_loadings


def visualize_pca(directory):
    """
    This function visualizes the results of Principal Component Analysis (PCA) using a scatter plot and a bar chart.

    Parameters:
    directory (str): The directory where the data files are located.

    Returns:
    altair.vegalite.v4.api.Chart: An Altair chart that visualizes the principal component loadings.
    """
    
    # Define the number of components for PCA
    n_components = 2

    # Call the perform_pca function to get the transformed data and component loadings
    x_pca, _, component_loadings = perform_pca(directory, n_components)

    # Call the prepare_for_pca function to get the module labels
    _, label_array, labels = prepare_for_pca(directory)

    # Plot scatterplot of PCA1 vs. PCA2
    plt.figure(figsize=(8,8))

    # Scatter plot of PCA-transformed data
    scatter=plt.scatter(x_pca[:,0],x_pca[:,1],c = label_array, alpha=0.5)

    # Create a legend for the scatter plot using target labels
    plt.legend(handles=scatter.legend_elements()[0], labels=labels, title="Module Health")
    plt.xlabel("Principle Component 1")
    plt.ylabel("Principle Component 2")
    plt.xlim(-0.1, 0.1)  # Set x-axis
    plt.ylim(-0.05, 0.05)  # Set y-axis
    plt.savefig('PreliminaryPCAvoltages.png')

    # Reset index to convert index (feature names) into a column
    component_loadings = component_loadings.reset_index().rename(columns={'index': 'Feature'})

    # Melt the dataframe to long format for Altair visualization
    component_loadings_long = pd.melt(component_loadings, id_vars=['Feature'], var_name='Principal Component', value_name='Loading')

    color_scheme = alt.Scale(domain=['PC1', 'PC2'], range=['#874ca1', '#5b9140'])  # Example colors

    # Create an Altair chart to visualize principal component loadings
    chart = alt.Chart(component_loadings_long).mark_bar().encode(
        x=alt.X('Feature:N', title='Feature'),
        y=alt.Y('Loading:Q', title='Loading Value'),
        color=alt.Color('Principal Component:N', scale=color_scheme),  # Apply the custom color scale
        column='Principal Component:N'
    ).properties(
        width=200,
        height=300,
        title='Principal Component Loadings'
    )

    return chart
