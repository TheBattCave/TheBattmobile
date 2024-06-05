# TheBattmobile

## Motivation

The revolution in vehicle electrification is generating vast amounts of data from various sensors and systems embedded in electric vehicles (EVs). These data streams include information on a battery pack's temperature, voltage, current, and usage patterns, among other metrics. However, sorting through this data and extracting meaningful insights about a battery's health and performance is challenging due to the sheer volume and complexity of the information. Leveraging advanced analytics and machine learning techniques can help to interpret the data accurately, identify trends, and predict potential issues.

## Use Cases

### King County Metro Maintenance

Our primary use case is King County Metro, a local transit agency that operates the largest hybrid electric bus fleet in the country. Their fleet management primarily uses predictive maintenance to swap out battery modules that could be failing based only upon one indicator – voltage dwell time. Our tool for data organization and analysis can assist fleet maintenance in identifying a failing battery module from data-driven metrics that incorporate all of the variables collected, not just one. This could help reduce maintenance downtime, prolong battery pack usage, and cut costs.

### Academic/Industry R&D

As is, there is a sparsity in clean and open-source data from in-application battery packs. Parsing, cataloging, and analyzing the data collected from King County Metro’s large hybrid-electric bus fleet is useful work to the research and development community. This can aid in developing more efficient battery management systems, improved battery designs, and optimized usage strategies. For academic researchers, it provides a solid foundation for theoretical studies and innovations in battery technology, supporting advancements in energy storage solutions and sustainability.

## Component Design

### Extract, Transform, Load (etl.py)

Our etl.py module is designed to process and organize raw, unlabeled battery data from a zip file. It extracts files, reads their contents to identify key identifiers such as number of maintenance visits and bus IDs, and then sorts the data into a hierarchical folder structure based on these identifiers. By categorizing files into folders by visit numbers and bus IDs, the module facilitates easy access and targeted analysis of the data. With robust error handling and scalability for large datasets, this module streamlines the transformation of raw data into a well-organized format.

### Visualize (vis.py)

Our vis.py module is designed for exploring through the previously organized folders and files containing battery data. It can build data structures and generate visualizations based on key variables such as voltage, current, temperature, and power. It can also grab specific information from files by bus, module, submodule, and cell. Lastly, it provides additional tools to support other means of exploration, for example by labeling swapped modules or by organizing buses by date. These systematic tools provide an easy method for understanding the dataset and discovering present trends.

### Analyze (analysis.py)

Lastly, our analysis.py module offers a suite of tools for conducting Principal Component Analysis (PCA) on built data frames, currently supporting voltage analysis at the module level. With features including normalization through mean centering, visualization of explained variance to aid in component selection, plotting of principle component loadings, and scatterplot visualization of data points in terms of the first two principle components, it provides users with powerful analytical capabilities. Several checks are in place to ensure the accuracy and integrity of the analysis, offering confidence in the results obtained.

## Architecture



## Contributing


