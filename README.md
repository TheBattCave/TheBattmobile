User: Academic Researchers:

Data visualization of KCM datasets aims to explore potential correlations between battery module replacements, operational time, spatial locations of modules, bus routes, and dataset features (voltage, current, power, temperature).
Component Design:
1. Understanding datasets: Identify dataset features and current organization.
2. Data cleaning: Transform data into a usable dataframe, identify individual modules, handle repeats, determine time intervals between data collection, segment data by bus and module, and detect instances of module replacement.
3. Data visualization: Utilize numpy, matplotlib, seaborn, and pandas libraries to visualize relationships among modules, operational time, spatial locations, bus routes, and dataset features.


User: King County Metro
To minimize downtime and expenses associated with unscheduled maintenance, the aim is to predict the current health status and remaining usable life of battery modules for proactive maintenance.

Data Analysis:
- Assess the adequacy of available data for training and testing a predictive model.

Model Training:
- Develop a model to forecast the replacement timing of battery modules in hybrid bus fleets, considering variables such as voltage, temperature, and bus route.

Component Design:
- Utilize machine learning techniques to anticipate the end-of-life for battery modules.


User: Battery System Management Software Users
Enhancing comprehension of battery operations through data visualization and predictive modeling.





# TheBattmobile
* This repos is still a WORK IN PROGRESS


The purpose of this repository is to provide a software program that will allow for the analysis of battery pack data. This anaylsis will sort raw data and provide an output of clean data. This clean data will be found in two differemt folders, sorted data and vis_bus. Eventually the goal is to run a Principle Compnent Analysis (PCA) on the cleaned data in order to find which components produce the largest change.

For any questions, please contact the contributors.
