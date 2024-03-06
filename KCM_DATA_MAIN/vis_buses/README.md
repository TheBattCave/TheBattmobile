# Instructions for extracting and plotting graphs from sorted buses with module changes:

The build_data_vis package contains two main types of functions:
1. _Dataframe building functions:_ These functions parse the csv files dataframes of specific parameters targeted by the user. For example, the user can extract a dataframe of just the module 1 voltages for the same bus over time.
2. _Visualization functions_: These functions will use the dataframe building functions to extract portions of the csv files to be plotted to help the user notice any trends in the data.

## List of Dataframe building functions:

1. sort_bus_by_date: This function takes as input a directory and a string of the bus directory to be sorted. The function returns a dataframe with the file names within the bus folder sorted sequentially by date retrieved. The date retrieved is also a column in the dataframe.
2. build_bus_df: This function takes as input a directory, a string of the desired bus directory, and a keyword (selected from 'Current', 'Voltage', or 'Power'. The function returns a dataframe of the __entire bus__ current, voltage, or power over time, with the order of the rows being sequential by date. The columns of the dataframe correspond to the selected keyword, and the values in the rows are in seconds. For example, in a voltage dataframe the columns will be a range of voltages from 2 to 4 V, and the corresponding rows will be the number of seconds the battery spent at that total voltage. 
3. build_module_df: This function takes as input a directory, a string of the desired bus directory, and an integer module number (can be between 1 and 16). The function returns a dataframe of the module voltages with the rows sequential in time. Note that the module data within the csv files is further subdivided into 12 submodules. Therefore, this function will output 12 rows for each date retrieved within the bus folder. For example, running this function on bus 1 module 1 should return a dataframe with 216 rows. Rows 0-11 correspond to the first date in the bus folder, then rows 12-24 to the next date, etc.
4. build_module_average_df: This function is similar to the above function, but it averages the submodule data together to return only one row for each date for the module specified. This allows for easier visualization of voltages on the module level.
5. count_mod_changes: This function takes as an input a directory of data sorted by bus. The function will then return a dataframe showing the bus and module number as well as the number of times the module has been changed. 
6. find_replaced_modules: This function takes as an input a directory of data sorted by bus. The function will return a dictionary with the bus number as the key and the serial number of the modules that have been swapped as the values.
7. swapped_mod_dataframes: This function takes as an input a directory, a module serial number, and a keyword. The function then returns a dataframe of the input module characteristic. For example, inputting your directory with the serial number for bus 1 module 1 and the keyword 'balancers' will return a dataframe of the cell balancer data for that module, with the rows sequential by time.

## List of Visualization functions:
1. visualize_mod_changes: This function uses the count_mod_changes output to produce a heat map for all buses indicating when the modules have been changed (with a color change indicating the module has been changed). The heat map includes a drop down menu to select the desired bus.
	**here, you can manually go through the buses and see if there are any abnormalities (eg. too many module changes, all modules changed at once etc.)
	**here, you can also manually pick out the buses that contain modules with beginning and end of life date
2. mod_change_statistics: This function uses the count_mod_changes output to calculate and graph statistics on how often a given module is changed across all of the bus data. This allows us to see if module position has an effect on frequency of module failure.
3.  visualize_mod_time: This function uses the build_module_average_df output to visualize the distribution of time spent at each voltage in the voltage range for a given module. For example, running this function with the input of bus 1 and module 1 will return a graph with 12 plotted lines, one for each individual date in bus one, where the x axis is voltage and the y axis is time in seconds. A dropdown menu is available on the graph to select a specific date. The selected date will remain in color while the other dates will be rendered gray. The axes are also scalable by clicking and dragging and using your mouse scroll.

## Instructions on using the package:

Using the above descriptions, select which function produces the desired output. Import build_data_vis into your notebook and call the function by running build_data_vis.[desired_function]. For more information, see the example notebook in the main folder.
