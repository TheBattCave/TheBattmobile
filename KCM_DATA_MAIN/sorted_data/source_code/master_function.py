import os
import shutil
from os import listdir
import numpy as np
import pandas as pd
import organize_functions as of
import module_changes as mc
import sort_bus_by_date

def get_directory():
    directory = os.getcwd()
    print(directory)
    return directory

def count_bus_file():
    directory = get_directory()
    list=[]
    for file in listdir(directory):
        substring = 'bus_'
        fullstring = 'sort_bus_by_date'
        if fullstring in file:
            pass
        else:
            if substring in file:
                list.append(file)
    return len(list)

def fliter_false_module():
    file_list = []
    get_bus = mc.compare_file_mods(get_directory()+'/')
    bus_file_num = count_bus_file()
    for i in range(1,bus_file_num):
        num = 'bus_'+str(i) 
        bus = get_bus[num]                 # extract dataframe from dict
        for i in range(len(bus.columns)):  # for each bus, iterate through each columns
            if len(bus.columns) < 2:       # pass if only one data file in bus_file
                pass
            else:
                A=bus.columns[i]
                rslt_df = bus[A][(bus[A] == False)]
                if rslt_df.empty:
                    pass
                else:
                    file_list.append(num)
                    #print("This is "+ num )
                    #print(rslt_df)
    False_list = np.unique(file_list)
    return False_list

def move_false_bus():
    False_list = fliter_false_module()
    source = os.getcwd()
    print(source)
    destination = source + '/False_files'
    if not os.path.exists(destination):
            os.makedirs(destination)
    else:
        pass
    for bus_file in False_list:
        shutil.move(bus_file,destination)





# run following:
# directory = of.find_directory()
# of.group_files(directory)
# master_function.fliter_false_module()
# master_function.move_false_bus()
