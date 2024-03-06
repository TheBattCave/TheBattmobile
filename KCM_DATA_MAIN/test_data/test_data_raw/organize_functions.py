#!/usr/bin/env python
# coding: utf-8

# In[52]:

import csv
import os
from os import listdir
import pathlib
import re


# ## Instructions For Use

# 1. Import file organize_functions.py
# 2. Use organize_functions.find_directory() to get your directory as a string (store as directory variable)
# 3. Use organize_functions.group_files(directory) to group files.
    # a.) Changed keyword argument into a string within function since we will never change this.

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


def group_files(directory):
    '''
    Finds serial numbers for all modules of a each file in a directory and groups CSV files with matching serials into 
    individual bus directories.
    '''
    keyword = 'Mfg Data (ASCII)'
    count = 1
    list_of_csv = grab_csv(directory)
    moved_files = []
    for filename in list_of_csv:
        list_matches = []
        if filename in moved_files:
            pass
        else:
            module_list = []
            source = os.path.join(directory, filename)
            with open(directory + filename) as file_1:
                reader = csv.reader(file_1)
                for row in reader:
                    for element in row:
                        if keyword in element:
                            mod_num = re.sub(r'\W+', '', element[17:]).lower()
                            module_list.append(mod_num)
                        else:
                            pass
            if not module_list:
                pass
            else:
                module_list.pop(0)
            if len(module_list) >= 16:
                bus_folder = 'bus_' + str(count) + '/'
                if not os.path.exists(os.path.join(directory, bus_folder)):
                    os.makedirs(os.path.join(directory, bus_folder))
                else:
                    pass
                destination = os.path.join(directory, bus_folder + filename)
                moved_files.append(filename)
                shutil.move(source, destination)
                # Finish moving complete source file to new directory

                for otherfile in list_of_csv:
                    if otherfile in moved_files:
                        pass
                    else:
                        other_modules = []
                        with open(directory + otherfile) as file_2:
                            reader = csv.reader(file_2)
                            for row in reader:
                                for element in row:
                                    if keyword in element:
                                        mod_num = re.sub(r'\W+', '', element[17:]).lower()
                                        other_modules.append(mod_num)
                                    else:
                                        pass
                        if not other_modules:
                            pass
                        else:
                            other_modules.pop(0)
                        if(len(other_modules) >= 16):
                            if (any(module_num in module_list for module_num in other_modules)):
                                list_matches.append(otherfile)
                                moved_files.append(otherfile)
                            else:
                                pass
                        else:
                            pass
                for match in list_matches:  # Modified from before because generally not safe to modify list as we loop
                    source = directory + match
                    destination = os.path.join(directory, bus_folder + match)
                    shutil.move(source, destination)
                count += 1
            else:
                moved_files.append(filename)
                incomplete = os.path.join(directory + 'incomplete/')
                if not os.path.exists(incomplete):
                    os.makedirs(os.path.join(incomplete))
                destination = incomplete + filename
                shutil.move(source, destination)
