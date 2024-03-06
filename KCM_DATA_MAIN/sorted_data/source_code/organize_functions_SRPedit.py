#!/usr/bin/env python
# coding: utf-8

# In[52]:


import matplotlib.pyplot as plt
import numpy as np
import os
from os import listdir
import pandas as pd 
import shutil
from shutil import copyfile
get_ipython().run_line_magic('matplotlib', 'inline')
import re

import pathlib
import csv


# ## Instructions For Use

# 1. Import file organize_functions.py
# 2. Use organize_functions.find_directory() to get your directory as a string (store as directory variable)
# 3. Use organize_functions.group_files(directory, 'Mfg Data (ASCII)') to group files.

# ## Functions

# In[2]:


def find_directory():
    '''
    Assuming your python file is in the directory containing KCM data files, returns a path to that directory with an additional
    forward slash for future concatenation processes.
    '''
    path = pathlib.Path().absolute()
    directory = str(path) + '/'
    return directory


# In[3]:


def grab_csv(directory):
    '''
    Returns a list of all csv files in an existing directory.
    Ignoring the lone xlsx file for now, as reader fails to read this file.
    '''
    list_of_csv = []
    for filename in listdir(directory):
        if (filename.endswith('.csv')): #or filename.endswith('.xlsx')):
            list_of_csv.append(filename)
        else:
            pass
    return list_of_csv


# In[91]:


def group_files(directory, keyword):
    '''
    Finds serial numbers for all modules of a each file in a directory and groups CSV files with matching serials into 
    individual bus directories.
    '''
    count = 1
    list_of_csv = grab_csv(directory)
    moved_files = []
    serial_start = 17
    for filename in list_of_csv:
        list_matches = []
        if filename in moved_files:
            pass
        else:
            module_list = []
            source = os.path.join(directory, filename)
            print('Source file: ', source)
            with open(directory + filename) as file_1:
                reader = csv.reader(file_1)
                for row in reader:
                    for element in row:
                        if keyword in element:
                            mod_num = re.sub(r'\W+', '', element[serial_start:]).lower()
                            if mod_num != '':
                                module_list.append(mod_num)
                            else:
                                pass
            if len(module_list) >= 16:
                bus_folder = 'bus_' + str(count) + '/'
                if not os.path.exists(os.path.join(directory, bus_folder)):
                    os.makedirs(os.path.join(directory, bus_folder))
                else:
                    pass
                destination = os.path.join(directory, bus_folder + filename)
                module_list.pop(0)
                moved_files.append(filename)
                shutil.move(source, destination)
                # Finish moving complete source file to new directory

                for otherfile in list_of_csv:
                    if otherfile in moved_files:
                        pass
                    else:
                        print('Other file', otherfile)
                        other_modules = []
                        with open(directory + otherfile) as file_2:
                            reader = csv.reader(file_2)
                            for row in reader:
                                for element in row:
                                    if keyword in element:
                                        mod_num = re.sub(r'\W+', '', element[serial_start:]).lower()
                                        if mod_num != '':
                                            other_modules.append(mod_num)
                                        else:
                                            pass
                            if (any(module_num in module_list for module_num in other_modules)):
                                list_matches.append(otherfile)
                                moved_files.append(otherfile)
                            else:
                                pass
                for match in list_matches:  # Modified from before because generally not safe to modify list as we loop
                    source = directory + match
                    destination = os.path.join(directory, bus_folder + match)
                    print("trying to move")
                    shutil.move(source, destination)
                count += 1
            else:
                moved_files.append(filename)
                incomplete = os.path.join(directory + 'incomplete/')
                if not os.path.exists(incomplete):
                    os.makedirs(os.path.join(incomplete))
                destination = incomplete + filename
                shutil.move(source, destination)


# In[93]:


directory = find_directory()
group_files(directory, 'Mfg Data (ASCII)')


# ## Testing Individual Files

# In[26]:


keyword = 'Mfg Data (ASCII)'
directory = find_directory()
test_csv = grab_csv(directory)
file_1 = directory + 'Raw data/' + '!3J0018_ProfileData_20170920082828.csv'
file_2 = directory + 'Raw data/' + '14H0220_ProfileData_20181218082248.csv'
file_1_mods = []
file_2_mods = []
list_matches = []
with open(file_1) as file:  # Iterating through all remaining files in list of files
    reader = csv.reader(file)
    for row in reader:
        for element in row:
            if keyword in element:
                file_1_mods.append(element.lower())
with open(file_2) as file:  # Iterating through all remaining files in list of files
    reader = csv.reader(file)
    for row in reader:
        for element in row:
            if keyword in element:
                file_2_mods.append(element.lower())
# any(module_num in file_1_mods for module_num in file_2_mods)
# print('File 1: ' , file_1_mods, '\n File 2: ', file_2_mods)


# In[44]:


keyword = 'Mfg Data (ASCII)'
directory = find_directory()
test_csv = grab_csv(directory)
file_1 = directory + '/Raw data/' + '!3J0018_ProfileData_20170920082828.csv'
# file_2 = directory + '/Raw data/' + '13j0016_ProfileData_20190121101408.csv'
file_1_mods = []
list_matches = []
with open(file_1) as file:  # Iterating through all remaining files in list of files
    reader = csv.reader(file)
    for row in reader:
        for element in row:
            if keyword in element:
                file_1_mods.append(element[19:44].lower())
    file_1_mods.pop(0)
# with open(file_2) as file:  # Iterating through all remaining files in list of files
#     reader = csv.reader(file)
#     for row in reader:
#         for element in row:
#             if keyword in element:
#                 file_2_mods.append(element.lower())
# any(module_num in file_1_mods for module_num in file_2_mods)
for filename in test_csv:
    file_2_mods = []
    with open(filename) as file:  # Iterating through all remaining files in list of files
        reader = csv.reader(file)
        for row in reader:
            for element in row:
                if keyword in element:
                    file_2_mods.append(element[19:44].lower())
    if(any(module_num in file_1_mods for module_num in file_2_mods)):
        list_matches.append(filename)


# In[45]:


list_matches


# In[46]:


len(list_matches)


# In[47]:


#type(os.path.join(directory, filename))


# In[81]:


mod = 'Mfg Data (ASCII): 364A1583G100      -13L0049............'
mod[17:]


# In[82]:


re.sub(r'\W+', '', mod[17:]).lower()


# In[101]:


keyword = 'Mfg Data (ASCII)'
directory = find_directory()
test_csv = grab_csv(directory)
file_1 = directory + '/Raw data/' + '14F0168_ProfileData_20180607122634.csv'
file_2 = directory + '/Raw data/' + '13L0309_ProfileData_20180607062937.csv'
file_1_mods = []
file_2_mods = []
list_matches = []
with open(file_1) as file:  # Iterating through all remaining files in list of files
    reader = csv.reader(file)
    for row in reader:
        for element in row:
            if keyword in element:
                mod_num = re.sub(r'\W+', '', element[17:]).lower()
                file_1_mods.append(mod_num)
with open(file_2) as file:  # Iterating through all remaining files in list of files
    reader = csv.reader(file)
    for row in reader:
        for element in row:
            if keyword in element:
                mod_num = re.sub(r'\W+', '', element[17:]).lower()
                file_2_mods.append(mod_num)
# for i in range(len(file_1_mods)):
#     print('\n', file_1_mods[i], file_2_mods[i], '\n')
# print(len(file_1_mods), len(file_2_mods))
# d = {'file1': file_1_mods, 'file2':file_2_mods}
# df = pd.DataFrame(data=d)
# df
file_2_mods.pop(0)
any(module_num in file_1_mods for module_num in file_2_mods)


# In[102]:


print(file_1_mods)


# In[103]:


print(file_2_mods)


# In[106]:


temp = set(file_1_mods)
res = [i for i, val in enumerate(file_2_mods) if val in temp]
print(str(res))
# print(file_2_mods)


# In[109]:


for i in range(len(file_1_mods)):
    if file_1_mods[i] in file_2_mods:
        print(file_1_mods[i])

