# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 15:01:26 2020

@author: mbexknm5
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import datetime, timedelta
import dateutil.relativedelta
import glob
import math
from datetime import date
import datetime
import shutil
import os, sys

sample_Freq = '5min'
av_Freq = '5min' #averaging frequency required of the data
data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v1.2' #version of the code
year_start = 2023 #input the year of study by number
month_start = 1 #input the month of study by number
default_start_day = 1 #default start date set
day_start = default_start_day
validity_status = 'Ratified' #Unratified or Unratified
process_type = 'Normal' #Normal, Level0 or Level1
column_check_no = 10 #what column do you want to check

status = np.where(validity_status == 'Unratified' , '_Unratified_', '_Ratified_')

today = date.today()
current_day = today.strftime("%Y%m%d")

start = datetime.datetime(year_start,month_start,day_start,0,0,00) #start time of the period 
month_After = start + dateutil.relativedelta.relativedelta(months=1)
default_end_date = month_After - timedelta(minutes=1) #last day of month more complex so established here

default_end_day = str(default_end_date.strftime("%Y")) + str(default_end_date.strftime("%m")) + str(default_end_date.strftime("%d"))

year_end = int(default_end_date.strftime("%Y")) #this converts the default_end_day into the end of time selected
month_end = int(default_end_date.strftime("%m"))
day_end = int(default_end_date.strftime("%d"))

end = datetime.datetime(year_end,month_end,day_end,23,59,59) #if new end date needed to can be changed here 

start_year_month_str = str(start.strftime("%y")) + str(start.strftime("%m")) # convert start and end months to strings
end_year_month_str = str(end.strftime("%y")) + str(end.strftime("%m"))

end_Date_Check = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

date_file_label = np.where(start_year_month_str == end_year_month_str, start_year_month_str, str(start_year_month_str) + "-" + str(end_year_month_str))

full_file_label = str(start.strftime("%Y")) + str(start.strftime("%m"))

prior_date_1 = start - dateutil.relativedelta.relativedelta(months=1)
prior_date_1_str = str(prior_date_1.strftime("%y")) + str(prior_date_1.strftime("%m"))

prior_date_2 = start - dateutil.relativedelta.relativedelta(months=2)
prior_date_2_str = str(prior_date_2.strftime("%y")) + str(prior_date_2.strftime("%m"))

prior_date_3 = start - dateutil.relativedelta.relativedelta(months=3)
prior_date_3_str = str(prior_date_3.strftime("%y")) + str(prior_date_3.strftime("%m"))

prior_date_4 = start - dateutil.relativedelta.relativedelta(months=4)
prior_date_4_str = str(prior_date_4.strftime("%y")) + str(prior_date_4.strftime("%m"))

later_date_1 = end + dateutil.relativedelta.relativedelta(months=1)
later_date_1_str = str(later_date_1.strftime("%y")) + str(later_date_1.strftime("%m"))

later_date_2 = end + dateutil.relativedelta.relativedelta(months=2)
later_date_2_str = str(later_date_2.strftime("%y")) + str(later_date_2.strftime("%m"))

later_date_3 = end + dateutil.relativedelta.relativedelta(months=3)
later_date_3_str = str(later_date_3.strftime("%y")) + str(later_date_3.strftime("%m"))

later_date_4 = end + dateutil.relativedelta.relativedelta(months=4)
later_date_4_str = str(later_date_4.strftime("%y")) + str(later_date_4.strftime("%m"))

folder = np.where((str(version_number) == 'v0.6'), 'Preliminary', str(validity_status))

if process_type == 'Normal':
    SMPS_Source = 'Processed_SMPS'
    file_type = '*.TXT'
else:
    SMPS_Source = 'Levelled_SMPS_Data'
    if process_type == 'Level0':
        file_type = 'Level0.TXT'
    else:
        file_type = 'Level1.TXT'

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/' + str(SMPS_Source) + '/', 'D:/FirsData/' + str(SMPS_Source) + '/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(folder) + '_' + str(version_number) + '/', 'D:/' + str(folder) + '_' + str(version_number) + '/')

Month_files = str(Data_Source_Folder) + 'Firs_SMPS_' + '*' + str(date_file_label) + '*' + str(file_type) # Needs to be address of data location - Collect CSV files

Prior_File_1 = str(Data_Source_Folder) + 'Firs_SMPS_' + '*' + str(prior_date_1_str) + '*' + str(file_type)
Prior_File_2 = str(Data_Source_Folder) + 'Firs_SMPS_' + '*' + str(prior_date_2_str) + '*' + str(file_type)
Prior_File_3 = str(Data_Source_Folder) + 'Firs_SMPS_' + '*' + str(prior_date_3_str) + '*' + str(file_type)
Prior_File_4 = str(Data_Source_Folder) + 'Firs_SMPS_' + '*' + str(prior_date_4_str) + '*' + str(file_type)
Later_File_1 = str(Data_Source_Folder) + 'Firs_SMPS_' + '*' + str(later_date_1_str) + '*' + str(file_type)
Later_File_2 = str(Data_Source_Folder) + 'Firs_SMPS_' + '*' + str(later_date_2_str) + '*' + str(file_type)
Later_File_3 = str(Data_Source_Folder) + 'Firs_SMPS_' + '*' + str(later_date_3_str) + '*' + str(file_type)
Later_File_4 = str(Data_Source_Folder) + 'Firs_SMPS_' + '*' + str(later_date_4_str) + '*' + str(file_type)

SMPS_csv_files = glob.glob(Month_files) + glob.glob(Prior_File_1) + glob.glob(Prior_File_2) + glob.glob(Prior_File_3) + glob.glob(Prior_File_4)+ glob.glob(Later_File_1) + glob.glob(Later_File_2) + glob.glob(Later_File_3) + glob.glob(Later_File_4)

# Create an empty list
frames = []

#  Iterate over csv_files
for csv in SMPS_csv_files:
    csv = open(csv, 'r', errors='ignore')
    df = pd.read_csv(csv, encoding= 'unicode_escape', index_col=False, header=None, error_bad_lines=False, skiprows=25)
    frames.append(df)

# Concatenate frames into a single DataFrame
smps = pd.concat(frames, sort=True)

smps = smps[0].str.split(';', expand=True)
#smps = smps.transpose()

smps['index no number'] = np.arange(len(smps))
smps['sample number'] = np.where(smps[0] == 'Sample #' , smps['index no number'], np.nan)

smps_sample_rows = smps[['sample number', 'index no number']]
smps_sample_rows = smps_sample_rows[smps_sample_rows['sample number'].notnull() ]
smps_sample_rows['sample number'] = smps_sample_rows['sample number'].astype(int)
smps_sample_rows['index no number'] = smps_sample_rows['index no number'].astype(int)
smps_sample_rows.index = np.arange(len(smps_sample_rows))
smps_sample_rows.rename(columns={'sample number' : 'sample_start'  }, inplace=True)
smps_sample_rows.rename(columns={'index no number' : 'sample_end'  }, inplace=True)
smps_sample_rows['sample_end'] += -1
smps_sample_rows['sample_end'] = smps_sample_rows['sample_end'].shift(periods=-1)
smps_sample_rows['sample_end'] = np.where(smps_sample_rows['sample_end'].isnull() , 1000000000, smps_sample_rows['sample_end'])
smps_sample_rows['sample_end'] = smps_sample_rows['sample_end'].astype(int)
smps_sample_rows['row number'] = np.arange(len(smps_sample_rows))
smps_sample_rows['row number'] += 1
smps_sample_rows.index = smps_sample_rows['row number']
smps_sample_rows = smps_sample_rows.drop(columns=['row number'])
smps_sample_rows=smps_sample_rows[smps_sample_rows['sample_end'].notnull() ]

#smps_sample_rows.to_csv(str(Data_Output_Folder) + 'maqs-SMPS-CPC_titles_20' + str(date_file_label)  + str(status) + str(version_number) + '.csv')
smps.index = np.arange(len(smps))
smps = smps.drop(columns=['sample number'])


if len(smps_sample_rows.index) == 1:
    pass
else:
    sample_begin = 0 
    current_num_data_set = sample_begin
    row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
    row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
    current_data_set = smps.iloc[int(row_begin):int(row_end)]
    current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
    current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
    current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
    current_data_set.columns = current_data_set.iloc[0]
    current_data_set = current_data_set.iloc[1:]
    current_data_set.index = np.arange(len(current_data_set))
    #current_data_set.drop(current_data_set[(current_data_set[0] == 'Sample #' )].index,inplace =True)
    current_data_set = current_data_set.drop(columns=[str(row_begin)])
    current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
    
    
    #if '14.6' in current_data_set.columns:
    #    pass
    #else:
    #    current_data_set['14.6'] = 0
    #if '685.4' in current_data_set.columns:
    #    pass
    #else:
    #    current_data_set['685.4'] = 0
    
    dataset_1 = current_data_set
    
    current_num_data_set += 1
    row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
    row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
    current_data_set = smps.iloc[int(row_begin):int(row_end)]
    current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
    current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
    current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
    current_data_set.columns = current_data_set.iloc[0]
    current_data_set = current_data_set.iloc[1:]
    current_data_set.index = np.arange(len(current_data_set))
    #current_data_set.drop(current_data_set[(current_data_set[0] == 'Sample #' )].index,inplace =True)
    current_data_set = current_data_set.drop(columns=[str(row_begin)])
    current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
    
    dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])
    
        
    current_num_data_set += 1
    if len(smps_sample_rows.index) <= current_num_data_set:
        pass
    else:
        row_begin = smps_sample_rows.iloc[int(current_num_data_set),0]
        row_end = smps_sample_rows.iloc[int(current_num_data_set),1]
        current_data_set = smps.iloc[int(row_begin):int(row_end)]
        current_data_set.iloc[0] = current_data_set.iloc[0].astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.lstrip().astype(str)
        current_data_set.iloc[0] = current_data_set.iloc[0].str.rstrip().astype(str)
        current_data_set.columns = current_data_set.iloc[0]
        current_data_set = current_data_set.iloc[1:]
        current_data_set.index = np.arange(len(current_data_set))
        current_data_set = current_data_set.drop(columns=[str(row_begin)])
        current_data_set = current_data_set.drop(current_data_set.filter(regex="None").columns, axis=1)
        dataset_1 = pd.concat([dataset_1, current_data_set])

    dataset_1 = dataset_1.shift(periods=1)
    dataset_1.iloc[0] = dataset_1.columns
    dataset_1 = dataset_1.rename(columns={x:y for x,y in zip(dataset_1.columns,range(0,len(dataset_1.columns)))})
    smps = dataset_1
    smps = smps.drop(current_data_set.filter(regex="number").columns, axis=1)



data_smps_1 = smps.drop(columns=[0])
data_smps_1.iloc[0] = data_smps_1.iloc[0].str.lstrip().astype(str) 
data_smps_labels = data_smps_1.iloc[0:1]
data_smps_1.columns = data_smps_1.iloc[0]

data_smps_1 = data_smps_1.iloc[1:]

data_smps_1['Date'] = data_smps_1['Date'].astype(str)
data_smps_1['Start Time'] = data_smps_1['Start Time'].astype(str)
data_smps_1['Date_length'] = data_smps_1['Date'].str.len()
data_smps_1['Time_length'] = data_smps_1['Start Time'].str.len()
data_smps_1=data_smps_1[data_smps_1.Date_length > 6]
data_smps_1=data_smps_1[data_smps_1.Date_length < 12]
data_smps_1=data_smps_1[data_smps_1.Time_length == 8]

data_smps_1['datetime'] = data_smps_1['Date'] + ' ' + data_smps_1['Start Time']
data_smps_1['datetime'] = [datetime.datetime.strptime(x,'%d/%m/%Y %H:%M:%S') for x in data_smps_1['datetime']] #converts the dateTime format from string to python dateTime
data_smps_1.index = data_smps_1['datetime']
data_smps_1 = data_smps_1.sort_index()

#data_smps_labels.to_csv(str(Data_Output_Folder) + 'maqs-SMPS-CPC_names_20' + str(date_file_label)  + str(status) + str(version_number) + '.csv')

data_smps_1 = data_smps_1.drop(columns=['Date', 'Start Time', 'Date_length', 'Time_length', 'datetime', 'Diameter Midpoint (nm)'])
data_smps_1 = data_smps_1.drop(columns=['Comment', 'Leak Test and Leakage Rate', 'Lab ID', 'Instrument ID', 'Sample ID' , 'Title', 'User Name'])

#data_smps_1.to_csv(str(Data_Output_Folder) + 'maqs-SMPS-CPC_aerosol-size-distribution_1_' + str(date_file_label)  + str(status) + str(version_number) + '.csv')

data_smps_1['datetime'] = data_smps_1.index

#data_smps_1.to_csv(str(Data_Output_Folder) + 'maqs-SMPS-CPC_other_2_20' + str(date_file_label)  + str(status) + str(version_number) + '.csv')

smps = data_smps_1
smps = smps.sort_index()
smps = smps[start:end]
smps['datetime'] = smps.index

first_rows = smps.iloc[0:2]
first_rows.iloc[0] = first_rows.columns
first_rows = first_rows.transpose()

#first_rows.rename(columns={0 : 'Column Titles'  }, inplace=True)
first_rows.iloc[0,0] = 'Column Titles'
first_rows.iloc[:,0] = first_rows.iloc[:,0].astype(str)
first_rows.drop(first_rows[((first_rows.iloc[:,0]) < '0' )].index,inplace =True)
first_rows.drop(first_rows[((first_rows.iloc[:,0]) > '999999'  )].index,inplace =True)
first_rows.iloc[:,0] = first_rows.iloc[:,0].astype(float)
first_rows.index = first_rows.iloc[:,0]
first_rows = first_rows.sort_index()
first_rows = first_rows.transpose()
first_rows.iloc[0] = first_rows.columns
first_rows.iloc[0] = first_rows.iloc[0].astype(str)
first_rows.columns = first_rows.iloc[0]
first_rows['datetime'] = first_rows.index
first_rows.index = first_rows['datetime']
first_rows = first_rows.drop(columns=['datetime'])

smps = pd.concat([first_rows, smps])

smps.drop(smps[((smps['Sample Temp (C)']) == 'Sample Temp (C)' )].index,inplace =True)

smps = smps.iloc[1:]
smps = smps.sort_index()

#smps.to_csv(str(Data_Output_Folder) + 'maqs-SMPS-CPC_other_2_20' + str(date_file_label)  + str(status) + str(version_number) + '.csv')

smps_Temp = smps.pop('Sample Temp (C)') 
smps_Pressure = smps.pop('Sample Pressure (kPa)') 
smps_Humidity = smps.pop('Relative Humidity (%)') 
smps_Free_Path = smps.pop('Mean Free Path (m)') 
smps_Viscosity = smps.pop('Gas Viscosity (Pa*s)') 
smps['Sample Temp (C)'] = smps_Temp 
smps['Sample Pressure (kPa)'] = smps_Pressure 
smps['Relative Humidity (%)'] = smps_Humidity 
smps['Mean Free Path (m)'] = smps_Free_Path 
smps['Gas Viscosity (Pa*s)'] = smps_Viscosity

smps['Sheath Flow (L/min)'] = smps['Sheath Flow (L/min)'].astype(float)
smps['Aerosol Flow (L/min)'] = smps['Aerosol Flow (L/min)'].astype(float)

smps['qc_Flags'] = 1
smps['qc_Flags'] = np.where(smps['Instrument Errors'] != 'Normal Scan', 2, smps['qc_Flags'])
smps['qc_Flags'] = np.where(smps['Sheath Flow (L/min)']>20, 2, smps['qc_Flags'])
smps['qc_Flags'] = np.where(smps['Sheath Flow (L/min)']<2, 2, smps['qc_Flags'])
smps['qc_Flags'] = np.where(smps['Aerosol Flow (L/min)']>2, 2, smps['qc_Flags'])
smps['qc_Flags'] = np.where(smps['Aerosol Flow (L/min)']<0.2, 2, smps['qc_Flags'])

CPC_3010_Detection_limit = 10000
CPC_3772_Detection_limit = 50000
CPC_3750_Detection_limit = 100000

smps['Sample Temp (C)'] = smps['Sample Temp (C)'].astype(float)
smps['Sample Temp (K)'] = smps['Sample Temp (C)'] + 273.15

#smps.to_csv(str(Data_Output_Folder) + 'maqs-SMPS-CPC_aerosol-size-distribution_20' + str(date_file_label)  + str(status) + str(version_number) + '.csv')

smps_Total = smps.filter(regex="Total Conc.")

#smps_Total.iloc[0,0] = 'Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'

spare_value = smps_Total.iloc[0,0]
smps_Total['datetime'] = smps_Total.index 
spare_date = smps_Total.iloc[0,1]
smps_Total.iloc[0,0] = 'Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'
smps_Total.iloc[0,1] = 'datetime'
smps_Total.columns = smps_Total.iloc[0]
smps_Total.iloc[0,0] = spare_value
smps_Total.iloc[0,1] = spare_date

smps_Total.index = smps_Total['datetime']
smps_Total = smps_Total.drop(columns=['datetime'])
Total_SMPS_Column = smps_Total['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)']

smps = smps.drop(smps.filter(regex="Total Conc.").columns, axis=1)
smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'] = Total_SMPS_Column

smps.rename(columns={'Geo. Mean (nm)' : 'Geometric Mean (nm)' , 'Geo. Std. Dev.' : 'Geometric Standard Deviation' }, inplace=True)

#smps = smps.drop(columns=[100])
#print(smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'])

smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'] = smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'].astype(float)
smps['qc_Flags'] = np.where((smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)']> float(CPC_3750_Detection_limit)), 2, smps['qc_Flags'])

smps = smps.drop(columns=['Instrument Errors', 'Sheath Flow (L/min)', 'Aerosol Flow (L/min)', 'Scan Time (s)', 'Retrace Time (s)' , 'Scan Resolution (Hz)'])
smps = smps.drop(columns=['Scans Per Sample', 'Bypass Flow (L/min)', 'Low Voltage (V)', 'High Voltage (V)', 'td + 0.5 (s)'])
smps = smps.drop(columns=['tf (s)', 'D50 (nm)', 'datetime', 'Relative Humidity (%)' ])
smps = smps.drop(smps.filter(regex='Density').columns, axis=1)
#smps = smps.drop(columns=['Median (nm)', 'Geometric Mean', 'Mode (nm)', 'Geo. Std. Dev.' ])

smps['Sample Pressure (kPa)'] = smps['Sample Pressure (kPa)'].astype(float)

Lower_Temperature_limit = 10
Upper_Temperature_limit = 40

Lower_Pressure_limit = 70
Upper_Pressure_limit = 125

smps['qc_Flags'] = np.where((smps['Sample Temp (C)']< float(Lower_Temperature_limit)), 2, smps['qc_Flags'])
smps['qc_Flags'] = np.where((smps['Sample Temp (C)']> float(Upper_Temperature_limit)), 2, smps['qc_Flags'])

smps['qc_Flags'] = np.where((smps['Sample Pressure (kPa)']< float(Lower_Pressure_limit)), 2, smps['qc_Flags'])
smps['qc_Flags'] = np.where((smps['Sample Pressure (kPa)']> float(Upper_Pressure_limit)), 2, smps['qc_Flags'])

smps_Flag = smps.pop('qc_Flags') 
smps['qc_Flags'] = smps_Flag 

start_Tarmac = datetime.datetime(2020,5,4,7,30,00)
end_Tarmac = datetime.datetime(2020,5,15,16,0,00)
smps.loc[start_Tarmac:end_Tarmac, 'qc_Flags'] = 2

start_Simon_1 = datetime.datetime(2018,12,1,0,0,00)
end_Simon_1 = datetime.datetime(2019,6,30,23,59,59)
smps.loc[start_Simon_1:end_Simon_1, 'qc_Flags'] = 2

start_PSL300nm_1 = datetime.datetime(2020,5,26,9,52,00)
end_PSL300nm_1 = datetime.datetime(2020,5,26,16,36,00)
smps.loc[start_PSL300nm_1:end_PSL300nm_1, 'qc_Flags'] = 2
smps.drop(smps.loc[start_PSL300nm_1:end_PSL300nm_1].index, inplace=True)

start_PSL200nm_1 = datetime.datetime(2021,6,24,15,10,00)
end_PSL200nm_1 = datetime.datetime(2021,6,24,15,30,00)
smps.loc[start_PSL200nm_1:end_PSL200nm_1, 'qc_Flags'] = 2
smps.drop(smps.loc[start_PSL200nm_1:end_PSL200nm_1].index, inplace=True)

start_PSL300nm_2 = datetime.datetime(2021,6,24,15,30,00)
end_PSL300nm_2 = datetime.datetime(2021,6,24,16,59,00)
smps.loc[start_PSL300nm_2:end_PSL300nm_2, 'qc_Flags'] = 2
smps.drop(smps.loc[start_PSL300nm_2:end_PSL300nm_2].index, inplace=True)

start_PSL300nm_3 = datetime.datetime(2021,6,24,16,59,00)
end_PSL300nm_3 = datetime.datetime(2021,6,24,17,20,00)
smps.loc[start_PSL300nm_3:end_PSL300nm_3, 'qc_Flags'] = 2
smps.drop(smps.loc[start_PSL300nm_3:end_PSL300nm_3].index, inplace=True)

start_PSL200nm_2 = datetime.datetime(2021,6,24,17,20,00)
end_PSL200nm_2 = datetime.datetime(2021,6,24,17,35,00)
smps.loc[start_PSL200nm_2:end_PSL200nm_2, 'qc_Flags'] = 2
smps.drop(smps.loc[start_PSL200nm_2:end_PSL200nm_2].index, inplace=True)

start_Peak_1 = datetime.datetime(2019,1,24,11,30,00)
end_Peak_1 = datetime.datetime(2019,1,24,16,10,00)
smps.loc[start_Peak_1:end_Peak_1, 'qc_Flags'] = 2
smps.drop(smps.loc[start_Peak_1:end_Peak_1].index, inplace=True)

start_Peak_1 = datetime.datetime(2020,1,24,11,30,00)
end_Peak_1 = datetime.datetime(2020,1,24,16,10,00)
smps.loc[start_Peak_1:end_Peak_1, 'qc_Flags'] = 2
smps.drop(smps.loc[start_Peak_1:end_Peak_1].index, inplace=True)

start_Peak_2 = datetime.datetime(2021,1,22,8,40,00)
end_Peak_2 = datetime.datetime(2021,1,22,9,30,00)
smps.loc[start_Peak_2:end_Peak_2, 'qc_Flags'] = 2
smps.drop(smps.loc[start_Peak_2:end_Peak_2].index, inplace=True)

start_Peak_3 = datetime.datetime(2021,1,26,10,40,00)
end_Peak_3 = datetime.datetime(2021,1,26,10,50,00)
smps.loc[start_Peak_3:end_Peak_3, 'qc_Flags'] = 2
smps.drop(smps.loc[start_Peak_3:end_Peak_3].index, inplace=True)

start_Peak_4 = datetime.datetime(2019,6,12,3,30,00)
end_Peak_4 = datetime.datetime(2019,6,19,11,30,00)
smps.loc[start_Peak_4:end_Peak_4, 'qc_Flags'] = 2
smps.drop(smps.loc[start_Peak_4:end_Peak_4].index, inplace=True)

start_Peak_5 = datetime.datetime(2019,7,13,7,10,00)
end_Peak_5 = datetime.datetime(2019,7,13,8,5,00)
smps.loc[start_Peak_5:end_Peak_5, 'qc_Flags'] = 2
smps.drop(smps.loc[start_Peak_5:end_Peak_5].index, inplace=True)

start_Peak_6 = datetime.datetime(2019,12,17,8,0,00)
end_Peak_6 = datetime.datetime(2019,12,17,9,0,00)
smps.loc[start_Peak_6:end_Peak_6, 'qc_Flags'] = 2
smps.drop(smps.loc[start_Peak_6:end_Peak_6].index, inplace=True)

start_Peak_7 = datetime.datetime(2020,5,12,12,0,00)
end_Peak_7 = datetime.datetime(2020,5,12,13,0,00)
smps.loc[start_Peak_7:end_Peak_7, 'qc_Flags'] = 2
smps.drop(smps.loc[start_Peak_7:end_Peak_7].index, inplace=True)

start_Peak_8 = datetime.datetime(2020,6,24,7,5,00)
end_Peak_8 = datetime.datetime(2020,6,24,7,20,00)
smps.loc[start_Peak_8:end_Peak_8, 'qc_Flags'] = 2
smps.drop(smps.loc[start_Peak_8:end_Peak_8].index, inplace=True)

start_Peak_9 = datetime.datetime(2021,11,19,7,30,00)
end_Peak_9 = datetime.datetime(2021,11,19,10,30,00)
smps.loc[start_Peak_9:end_Peak_9, 'qc_Flags'] = 2
smps.drop(smps.loc[start_Peak_9:end_Peak_9].index, inplace=True)

start_Peak_10 = datetime.datetime(2021,11,2,8,10,00)
end_Peak_10 = datetime.datetime(2021,11,2,10,0,00)
smps.loc[start_Peak_10:end_Peak_10, 'qc_Flags'] = 2
smps.drop(smps.loc[start_Peak_10:end_Peak_10].index, inplace=True)

start_Peak_10 = datetime.datetime(2021,12,12,13,0,00)
end_Peak_10 = datetime.datetime(2021,12,12,13,30,00)
smps.loc[start_Peak_10:end_Peak_10, 'qc_Flags'] = 2
smps.drop(smps.loc[start_Peak_10:end_Peak_10].index, inplace=True)

#print(column_titles)

column_titles = smps.iloc[0:5]
column_titles = column_titles.transpose()
column_titles['titles'] = column_titles.index
column_titles['titles'] = column_titles['titles'].astype(str)
column_titles.drop(column_titles.iloc[:, 0:5], inplace=True, axis=1)

column_titles.drop(column_titles[(column_titles['titles'] < '0' )].index,inplace =True)
column_titles.drop(column_titles[(column_titles['titles'] > '999999' )].index,inplace =True)
column_titles['titles'] = column_titles['titles'].astype(float)
column_titles.index = column_titles['titles']
column_titles = column_titles.sort_index()


column_titles['numbers'] = np.arange(len(column_titles))
column_titles['numbers'] = column_titles['numbers'].astype(int)
column_titles['numbers'] = column_titles['numbers'] + 1
column_titles.index = column_titles['numbers']
column_titles = column_titles.sort_index()
#print(column_titles)

#column_titles.to_csv(str(Data_Output_Folder) + 'maqs-SMPS-CPC_label_3_20' + str(date_file_label)  + str(status) + str(version_number) + '.csv')

#smps.to_csv(str(Data_Output_Folder) + 'maqs-SMPS-CPC_other_20' + str(date_file_label)  + str(status) + str(version_number) + '.csv')

column_titles['Label_pt_2'] = column_titles['titles'] 
column_titles['Label_pt_2'] = column_titles['Label_pt_2'].astype(str)

data_smps_labels = column_titles[['Label_pt_2', 'numbers']]
#print(data_smps_labels)

data_smps_labels['Full_Label'] = data_smps_labels['Label_pt_2']
data_smps_labels['Long_Label'] = 'Number Concentration of Ambient Particles in Channel with Midpoint Aerosol Diameter of ' + data_smps_labels['Label_pt_2'] +  ' nm'
data_smps_labels['Short_Label'] = 'number_concentration_of_ambient_particles_in_channel_with_midpoint_aerosol_diameter_of_' + data_smps_labels['Label_pt_2'] +  '_nm'
smps_label_dict = data_smps_labels[['Label_pt_2', 'Full_Label', 'Long_Label', 'Short_Label', 'numbers']]
smps_label_dict['numbers'] = smps_label_dict['numbers'] - 1
first_column = smps_label_dict['numbers'].min()
last_column = smps_label_dict['numbers'].max()
first_column = int(first_column)
last_column = int(last_column)
smps_label_dict['Aerosol Size Average'] = smps_label_dict['Label_pt_2']
smps_label_dict['Aerosol Size Average'] = smps_label_dict['Aerosol Size Average'].astype(float)
Smallest_Aerosol = smps_label_dict['Aerosol Size Average'].min()
Largest_Aerosol = smps_label_dict['Aerosol Size Average'].max()
smps_label_dict = smps_label_dict.drop(columns=['Aerosol Size Average'])
#print(first_column)
#print(last_column)
#data_smps_labels = data_smps_labels.drop(columns=['numbers'])

smps_label_dict.rename(columns={'numbers' : 'identity' }, inplace=True)
smps_label_dict['identity'] = smps_label_dict['identity'].astype(str)
smps_label_dict['identity'] = 'Aerosol_Label_' + smps_label_dict['identity']
smps_label_dict.index = smps_label_dict['identity']
identity_labels = smps_label_dict

long_smps_dict = smps_label_dict['Long_Label'].to_dict()
short_smps_dict = smps_label_dict['Short_Label'].to_dict()
smps_label_dict = smps_label_dict['Label_pt_2'].to_dict()
#smps_label_dict = data_smps_labels['Label_pt_2'].to_dict()
#print(smps_label_dict)

#smps = smps.drop(columns=['datetime'])
#smps_distribution = smps.iloc[:,int(first_column):(int(last_column) + 1)]
smps_distribution = smps.iloc[:,int(first_column):]
smps_distribution = smps_distribution.drop(smps_distribution.filter(regex=" ").columns, axis=1)
smps_distribution = smps_distribution.drop(smps_distribution.filter(regex="_").columns, axis=1)
smps_distribution = smps_distribution.dropna(how='all', axis='columns').copy()
smps_distribution[list(smps_distribution.columns.difference(smps_distribution.columns))] = np.nan
smps_factors = smps.iloc[:,int(first_column):]
smps_factors = smps_factors.drop(smps_factors.filter(regex="1").columns, axis=1)
smps_factors = smps_factors.drop(smps_factors.filter(regex="2").columns, axis=1)
smps_factors = smps_factors.drop(smps_factors.filter(regex="4").columns, axis=1)
smps_factors = smps_factors.drop(smps_factors.filter(regex="5").columns, axis=1)
smps_factors = smps_factors.drop(smps_factors.filter(regex="6").columns, axis=1)
smps_factors = smps_factors.drop(smps_factors.filter(regex="7").columns, axis=1)
smps_factors = smps_factors.drop(smps_factors.filter(regex="8").columns, axis=1)
smps_factors = smps_factors.drop(smps_factors.filter(regex="9").columns, axis=1)
smps_factors = smps_factors.drop(smps_factors.filter(regex="0").columns, axis=1)
smps_factors = smps_factors.dropna(how='all', axis='columns').copy()
smps_distribution[list(smps_distribution.columns.difference(smps_distribution.columns))] = np.nan

smps_distribution.iloc[0] = smps_distribution.columns
smps_distribution.iloc[0] = smps_distribution.iloc[0].astype(float)
smps_distribution.columns = smps_distribution.iloc[0]

smps = smps.dropna(how='all', axis='columns').copy()
smps[list(smps.columns.difference(smps.columns))] = np.nan
last_column = len(smps_distribution.columns)

smps_distribution.iloc[0] = smps.iloc[0,0:(int(last_column) )]
smps_distribution = smps_distribution.reindex(sorted(smps_distribution.columns), axis=1)
smps_distribution['datetime'] = smps_distribution.index
smps_factors['datetime'] = smps_factors.index

smps = pd.concat([smps_distribution, smps_factors])

#smps.columns = smps.iloc['Full_Label']
#smps.loc['Label_pt_2'] = smps.columns
#smps.loc['Full_Label'] = np.where( (smps.loc['Full_Label'].isnull() ) , smps.loc['Label_pt_2'], smps.loc['Full_Label'])
#smps_label_dict = smps.loc[['Full_Label', 'Label_pt_2']]
#smps.columns = smps.iloc[2]
#smps = smps.drop(index=['Label_pt_1', 'Label_pt_2', 'Full_Label']) # 'Full_Label'

smps.index = smps['datetime']
smps = smps.sort_index()
smps = smps.drop(columns=['datetime'])
smps[:].replace('', np.nan, inplace=True)
smps[:].replace('-1.#IO', np.nan, inplace=True)
smps.iloc[:] = smps.iloc[:].astype(float)
corrective_Freq = '1min'
smps = smps.groupby(pd.Grouper(freq=corrective_Freq)).mean()

#smps.replace(0, np.nan, inplace=True)

smps.drop(smps[(smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'].isnull() )].index,inplace =True)
smps.drop(smps[(smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'] == 0)].index,inplace =True)
smps.drop(smps[(smps['Geometric Mean (nm)'].isnull() )].index,inplace =True)
smps.drop(smps[(smps['Geometric Mean (nm)'] == 0)].index,inplace =True)

if start_year_month_str < '1908':
    smps.iloc[:,int(first_column):int(last_column)].replace(0, np.nan, inplace=True)
    smps.dropna(how='all', axis=1, inplace=True)
    smps.iloc[:,int(first_column):int(last_column)].replace(np.nan, 0, inplace=True)
else:
    smps.iloc[:,int(first_column):int(last_column)].replace(np.nan, 0, inplace=True)

smps.iloc[:,int(first_column):int(last_column)].replace(0, np.nan, inplace=True)
smps.dropna(how='all', axis=1, inplace=True)
smps.iloc[:,int(first_column):int(last_column)].replace(np.nan, 0, inplace=True)
smps['qc_Flags'].replace(np.nan, 0, inplace=True)
smps['qc_Flags'] = smps['qc_Flags'].astype(int)
smps['qc_Flags'].replace(0, np.nan, inplace=True)
smps['qc_Flags'] = smps['qc_Flags'].astype(float)
smps['qc_Flags'] = smps['qc_Flags'].astype(int)
smps['qc_Flags'] = smps['qc_Flags'].astype(str)
#smps.to_csv(str(Data_Output_Folder) + 'maqs-SMPS-CPC_20' + str(date_file_label)  + str(status) + str(version_number) + '.csv')

#smps = smps.drop(columns=[52,54,56,58])
#smps.drop(smps.iloc[:, 133:139], inplace=True, axis=1)

#print(smps_label_dict)
#print(smps)
first_rows = smps.iloc[0:2,:]
first_rows.iloc[0] = first_rows.columns
first_rows = first_rows.transpose()
first_rows.iloc[:,0] = first_rows.iloc[:,0].astype(str)
first_rows.drop(first_rows[((first_rows.iloc[:,0]) < '0' )].index,inplace =True)
first_rows.drop(first_rows[((first_rows.iloc[:,0]) > '999999'  )].index,inplace =True)
first_rows.iloc[:,0] = first_rows.iloc[:,0].astype(float)
first_rows.index = first_rows.iloc[:,0]
first_rows = first_rows.sort_index()
first_rows['numbers'] = np.arange(len(first_rows))
first_column = first_rows['numbers'].min()
last_column = first_rows['numbers'].max()
first_column = int(first_column)
last_column = int(last_column)
first_rows['Label_pt_2'] = first_rows.index
first_rows.index = first_rows['numbers']
first_rows['Label_pt_2'] = first_rows['Label_pt_2'].astype(str)
first_rows = first_rows[['Label_pt_2', 'numbers']]

first_rows['Full_Label'] = first_rows['Label_pt_2']
first_rows['Long_Label'] = 'Number Concentration of Ambient Particles in Channel with Midpoint Aerosol Diameter of ' + first_rows['Label_pt_2'] +  ' nm'
first_rows['Short_Label'] = 'number_concentration_of_ambient_particles_in_channel_with_midpoint_aerosol_diameter_of_' + first_rows['Label_pt_2'] +  '_nm'
first_rows = first_rows[['Label_pt_2', 'Full_Label', 'Long_Label', 'Short_Label', 'numbers']]

first_rows['Aerosol Size Average'] = first_rows['Label_pt_2']
first_rows['Aerosol Size Average'] = first_rows['Aerosol Size Average'].astype(float)
Smallest_Aerosol = first_rows['Aerosol Size Average'].min()
Largest_Aerosol = first_rows['Aerosol Size Average'].max()
first_rows = first_rows.drop(columns=['Aerosol Size Average'])

first_rows.rename(columns={'numbers' : 'identity' }, inplace=True)
first_rows['identity'] = first_rows['identity'].astype(str)
first_rows['identity'] = 'Aerosol_Label_' + first_rows['identity']
first_rows.index =first_rows['identity']

long_smps_dict = first_rows['Long_Label'].to_dict()
short_smps_dict = first_rows['Short_Label'].to_dict()
smps_label_dict = first_rows['Label_pt_2'].to_dict()

aerosol_ref_1 = 'Aerosol_Label_' + str(column_check_no)
aerosol_ref_2 = 'Aerosol_Label_' + str((column_check_no) + 10)
aerosol_ref_3 = 'Aerosol_Label_' + str((column_check_no) + 20)

smps.drop(smps[(smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'].isnull() )].index,inplace =True)
smps.drop(smps[(smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'] == 0)].index,inplace =True)
smps.drop(smps[(smps['Geometric Mean (nm)'].isnull() )].index,inplace =True)
smps.drop(smps[(smps['Geometric Mean (nm)'] == 0)].index,inplace =True)
smps.drop(smps[(smps['qc_Flags'] == 'qc_Flags')].index,inplace =True)
smps['qc_Flags'] = np.where( smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)']>1000000, "2", smps['qc_Flags'])

cut_off_low_channel = smps['Lower Size (nm)'].min()
cut_off_high_channel = smps['Upper Size (nm)'].max()

smps['datetime'] = smps.index
smps.index = smps['datetime']
smps = smps.sort_index()
smps = smps.drop(columns=['datetime'])

#print(str(smps_label_dict[(str(aerosol_ref_1))]))
plt.plot(smps[(float(smps_label_dict[(str(aerosol_ref_1))]))], label= str(long_smps_dict[(str(aerosol_ref_1))] ))
plt.plot(smps[(float(smps_label_dict[(str(aerosol_ref_2))]))], label= str(long_smps_dict[(str(aerosol_ref_2))]) )
plt.plot(smps[(float(smps_label_dict[(str(aerosol_ref_3))]))], label= str(long_smps_dict[(str(aerosol_ref_3))]) )
plt.plot(smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'], label='Total Aerosol Concentration ##/cm3')
plt.legend()
plt.ylabel('##/cm3')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}
#ax.set_xticks(ax.get_xticks()[::2])
plt.rc('font', **font)
#plt.ylim(10, 30)
plt.show()


smps_distribution = smps.iloc[:,int(first_column):int(last_column)]
aerosol_ref_first = 'Aerosol_Label_' + str(first_column)
aerosol_ref_last = 'Aerosol_Label_' + str(last_column)

columns= list(range(int(first_column), int(last_column)))


dates = smps_distribution.index # setting x-axis
diameters = smps_distribution.columns # setting y-axis
stride = 10                                                 #change stride to change averaging period
dates_subset = dates[::stride]
size_matrix = np.zeros((len(columns), dates_subset.size))
# align the particle size columns as rows into the size matrix
for ind, col in enumerate(columns):    
    size_matrix[ind,:] = smps_distribution.iloc[::stride, col]

x = dates_subset
y = diameters
z_min, z_max = size_matrix[:].min(), size_matrix[:].max()
z = size_matrix[:]

print(z_max)

fig, ax = plt.subplots()
myplot = ax.pcolormesh(x, y, z, cmap='RdYlBu_r', vmin=z_min, vmax=z_max)
ax.set_title('SMPS-CPC distribution')
plt.ylabel('particle size (nm)')
plt.xlabel('Date and Time')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
plt.colorbar(myplot)
plt.figure()
plt.show
()


smps_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/20' + str(date_file_label) + '/SMPS_CPC/'
check_Folder = os.path.isdir(smps_Folder)
if not check_Folder:
    os.makedirs(smps_Folder)
    print("created folder : ", smps_Folder)
else:
    print(smps_Folder, "folder already exists.")

smps.to_csv(str(smps_Folder) + 'SMPS-CPC_maqs_20' + str(date_file_label) + '_aerosol-size-distribution'  + str(status) + str(version_number) + '.csv')

smps['TimeDateSince'] = smps.index-datetime.datetime(1970,1,1,0,0,00)
smps['TimeSecondsSince'] = smps['TimeDateSince'].dt.total_seconds()
smps['day_year'] = pd.DatetimeIndex(smps['TimeDateSince'].index).dayofyear
smps['year'] = pd.DatetimeIndex(smps['TimeDateSince'].index).year
smps['month'] = pd.DatetimeIndex(smps['TimeDateSince'].index).month
smps['day'] = pd.DatetimeIndex(smps['TimeDateSince'].index).day
smps['hour'] = pd.DatetimeIndex(smps['TimeDateSince'].index).hour
smps['minute'] = pd.DatetimeIndex(smps['TimeDateSince'].index).minute
smps['second'] = pd.DatetimeIndex(smps['TimeDateSince'].index).second



