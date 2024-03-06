## Instructions for sorting raw data into bus folders:

Ensure you have the correct directory architecture, using the repository architecture as reference. Your current directory should contain the auto_sort_data.py file as well as a folder titled 'Raw Data' that contains a zip file of the data to be sorted. The zip file should be titled "KCM-Raw-Data.zip".

```
|   auto_sort_data.py
|   build_data_vis.py
|   Example_notebook.ipynb
+---Raw Data 
|   |   KCM-Raw-Data.zip
```

Import auto_sort_data.py. The package is automated and will run the commands needed to sort the csv files from your zipped file. 

This package works in the following way:

1. Unzip "KCM-Raw-Data.zip". This folder contains raw csv's obtained from KCM from 2015-2019 for hybrid electric bus fleet.
2. Iterate through all csv's in the raw data and group them as a bus folder "bus_x" if they have a module serial number in common.
3. Iterate through all bus folders and moves buses to "vis_data" folder if it experienced a module swap.

After running the package, your directory should now contain two new folders. One is titled "sorted_data" and contains folders of the buses that have __not experienced module changes__. The second folder is titled 'vis_data' and contains the buses that have experienced module swaps. If you choose to use our visualization package, this folder is what wil be called.

The new directory architecture is shown below:

```
|   auto_sort_data.py
|   build_data_vis.py
|   Example_notebook.ipynb
+---Raw Data 
|   |   KCM-Raw-Data.zip
+---sorted_data
|   |   bus_.../
+---vis_data
|   |   bus_.../
```
