# -*- coding: utf-8 -*-
"""
Created on Wed Apr 1 13:28:13 2020

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
import datetime
import os, sys

av_Freq = '1min' #averaging frequency required of the data
data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v2.2' #version of the code
year_start = 2022 #input the year of study
month_start = 12 #input the month of study
default_start_day = 1 #default start date set
day_start = default_start_day
validity_status = 'Unratified' #Ratified or Unratified

status = np.where(validity_status == 'Unratified' , '_Unratified_', '_Ratified_')

start = datetime.datetime(year_start,month_start,day_start,0,0,00) #start time of the period 
month_After = start + dateutil.relativedelta.relativedelta(months=1)
default_end_date = month_After - timedelta(minutes=1) #last day of month more complex so established here

default_end_day = str(default_end_date.strftime("%Y")) + str(default_end_date.strftime("%m")) + str(default_end_date.strftime("%d"))

year_end = int(default_end_date.strftime("%Y")) #this converts the default_end_day into the end of time selected
month_end = int(default_end_date.strftime("%m"))
day_end = int(default_end_date.strftime("%d"))

end = datetime.datetime(year_end,month_end,day_end,23,59,00) #if new end date needed to can be changed here 

start_year_month_str = str(start.strftime("%Y")) + str(start.strftime("%m")) # convert start and end months to strings
end_year_month_str = str(end.strftime("%Y")) + str(end.strftime("%m"))

end_Date_Check = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))
print(end_Date_Check) #print end date to check it is correct

date_file_label = np.where(start_year_month_str == end_year_month_str, start_year_month_str, str(start_year_month_str) + "-" + str(end_year_month_str))
print(date_file_label) #print end date to check it is correct

folder = np.where((str(version_number) == 'v0.6'), 'Preliminary', str(validity_status))

#Gas_Cal_Data_Source = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/NOyOzone/', 'D:/') #identify folders for calibrations and data inputs and output folders
Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/NOyOzone/', 'D:/FirsData/NOyOzone/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(folder) + '_' + str(version_number) + '/', 'D:/' + str(folder) + '_' + str(version_number) + '/')
Data_Source_Folder = np.where((start_year_month_str == '201901')|(start_year_month_str == '201906')|(start_year_month_str == '201909')|(start_year_month_str == '201911'), 'D:/FirsData/NOyOzone/', Data_Source_Folder)
#Data_Output_Folder = np.where((start_year_month_str == '201901')|(start_year_month_str == '201906')|(start_year_month_str == '201909'), 'D:/Ratified_v1.0/', Data_Output_Folder)

Gas_Cal_Data_Source = str(Data_Output_Folder) + "Gas_Cal_Files/"

pattern = str(Gas_Cal_Data_Source) + '1_Overall_Gas_Calibrations*' + str(version_number) + '.csv'# Needs to be address of data location - Collect CSV files
Gas_cal_file = glob.glob(pattern)
print(str(pattern))

# Create an empty list
frames = []

#  Iterate over csv_files
for csv in Gas_cal_file:
    df = pd.read_csv(csv)
    frames.append(df)

# Concatenate frames into a single DataFrame
Gas_Cal = pd.concat(frames)

Gas_Cal['datetime'] = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in Gas_Cal['datetime']]

NOy_Calib = Gas_Cal[['datetime', 'NO Zero (ppb)','NO Response', 'NOy Zero (ppb)', 'NOy Response']]
NOy_Calib.drop(NOy_Calib[(NOy_Calib['NO Response'].isnull())].index,inplace =True)

CO_AutoZero = Gas_Cal[['datetime', 'CO Zero (ppb)']]
CO_AutoZero.drop(CO_AutoZero[(CO_AutoZero['CO Zero (ppb)'].isnull())].index,inplace =True)

CO_Calib = Gas_Cal[['datetime', 'CO Response']]
CO_Calib.drop(CO_Calib[(CO_Calib['CO Response'].isnull())].index,inplace =True)

Other_Gas_Cals = Gas_Cal[['datetime', 'O3 Zero (ppb)', 'O3 Response', 'NO2 Zero (ppb)', 'NO2 Response']]
Other_Gas_Cals.drop(Other_Gas_Cals[(Other_Gas_Cals['O3 Response'].isnull())].index,inplace =True)


#Load data acquired with the first file format
default_Early_Month = '201910' #a month to load then exclude if post-2019

early_Date = np.where((start_year_month_str == end_year_month_str) & (year_start == 2019) & (2 <= month_start <= 11),  start_year_month_str, default_Early_Month) #str(year_start)
early_Date = np.where((start_year_month_str == end_year_month_str) & (year_start == 2018),  start_year_month_str, early_Date) #str(year_start)

pattern = str(Data_Source_Folder) + str(early_Date) + '*_gas.csv'# Collect CSV files

prior_date = start - timedelta(days=1)
date_Check = str(prior_date.strftime("%Y")) + str(prior_date.strftime("%m")) + str(prior_date.strftime("%d"))
#print(date_Check)

prior_month_pattern = str(Data_Source_Folder) + str(date_Check) + '*_gas.csv'#
#print(prior_month_pattern)

csv_files = glob.glob(pattern) + glob.glob(prior_month_pattern)

if start_year_month_str == '201812':
    Dec_files_1 = str(Data_Source_Folder) + '201901181636_gas.csv' 
    Dec_files_2 = str(Data_Source_Folder) + '201901182359_gas.csv' 
    Dec_files_3 = str(Data_Source_Folder) + '20181219*' + '_gas.csv' 
    Dec_files_4 = str(Data_Source_Folder) + '2018122*' + '_gas.csv' 
    
    csv_files = glob.glob(Dec_files_1) + glob.glob(Dec_files_2) + glob.glob(Dec_files_3) + glob.glob(Dec_files_4)

    gas_frames = []

    for csv in csv_files:
    
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, header=None, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,15,18])
        gas_frames.append(df)

    v_early_Data = pd.concat(gas_frames) #columns 1-6 are fine
    v_early_Data.rename(columns={0: 'Date'}, inplace=True) #columns 8,9,10,11,12 are 12,13,14,15,16 in later files
    v_early_Data.rename(columns={1: 'Time'}, inplace=True)
    v_early_Data.rename(columns={2: 'NO (ppb)'}, inplace=True)
    v_early_Data.rename(columns={3: 'Diff (ppb)'}, inplace=True)
    v_early_Data.rename(columns={4: 'NOy (ppb)'}, inplace=True)
    v_early_Data.rename(columns={5: 'NOy Flow (l/min)'}, inplace=True)
    v_early_Data.rename(columns={6: 'NOy Pressure (mmHG)'}, inplace=True)
    v_early_Data.rename(columns={7: 'NO2 (ppb)'}, inplace=True)
    v_early_Data.rename(columns={8: 'Ozone (ppb)'}, inplace=True)
    v_early_Data.rename(columns={9: 'NOy Flags'}, inplace=True)
    v_early_Data.rename(columns={10: 'NO2 Status'}, inplace=True)
    v_early_Data.rename(columns={11: 'O3 Flags'}, inplace=True)
    v_early_Data.rename(columns={15: 'SO2 (ppb)'}, inplace=True) #15,18 are columns 20 & 23 in later files
    v_early_Data.rename(columns={18: 'SO2 Flags'}, inplace=True) 

    early_Data = v_early_Data

elif start_year_month_str == '201901':
    jan_files_1 = str(Data_Source_Folder) + '201812302359_gas'
    jan_files_2 = str(Data_Source_Folder) + '2019010*' + '00_gas.csv'
    jan_files_3 = str(Data_Source_Folder) + '20190102*' + '59_gas.csv'
    jan_files_4 = str(Data_Source_Folder) + '20190104*' + '59_gas.csv'
    jan_files_5 = str(Data_Source_Folder) + '20190105*' + '59_gas.csv'
    jan_files_6 = str(Data_Source_Folder) + '20190106*' + '59_gas.csv'
    jan_files_7 = str(Data_Source_Folder) + '20190107*' + '59_gas.csv'
    
    csv_files = glob.glob(jan_files_1) + glob.glob(jan_files_2) + glob.glob(jan_files_3) + glob.glob(jan_files_4) + glob.glob(jan_files_5) + glob.glob(jan_files_6) + glob.glob(jan_files_7) 

    gas_frames = []

    for csv in csv_files:
    
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, header=None, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,15,18])
        gas_frames.append(df)

    Jan_Data_1 = pd.concat(gas_frames) #columns 1-6 are fine
    
    Jan_Data_1.rename(columns={0: 'Date'}, inplace=True) #columns 8,9,10,11,12 are 12,13,14,15,16 in later files
    Jan_Data_1.rename(columns={1: 'Time'}, inplace=True)
    Jan_Data_1.rename(columns={2: 'NO (ppb)'}, inplace=True)
    Jan_Data_1.rename(columns={3: 'Diff (ppb)'}, inplace=True)
    Jan_Data_1.rename(columns={4: 'NOy (ppb)'}, inplace=True)
    Jan_Data_1.rename(columns={5: 'NOy Flow (l/min)'}, inplace=True)
    Jan_Data_1.rename(columns={6: 'NOy Pressure (mmHG)'}, inplace=True)
    Jan_Data_1.rename(columns={7: 'NO2 (ppb)'}, inplace=True)
    Jan_Data_1.rename(columns={8: 'Ozone (ppb)'}, inplace=True)
    Jan_Data_1.rename(columns={9: 'NOy Flags'}, inplace=True)
    Jan_Data_1.rename(columns={10: 'NO2 Status'}, inplace=True)
    Jan_Data_1.rename(columns={11: 'O3 Flags'}, inplace=True)
    Jan_Data_1.rename(columns={15: 'SO2 (ppb)'}, inplace=True) #15,18 are columns 20 & 23 in later files
    Jan_Data_1.rename(columns={18: 'SO2 Flags'}, inplace=True) 
    
    jan_files_1 = str(Data_Source_Folder) + '20190108*' + '_gas.csv' 
    jan_files_2 = str(Data_Source_Folder) + '201901100000_gas'
    
    csv_files = glob.glob(jan_files_1) + glob.glob(jan_files_2)

    gas_frames = []

    for csv in csv_files:
    
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, header=None, usecols=[0,1,2,3,4,5,6,8,9,10,11,12,15,18])
        gas_frames.append(df)

    Jan_Data_2 = pd.concat(gas_frames) #columns 1-6 are fine
    
    Jan_Data_2.rename(columns={0: 'Date'}, inplace=True) #columns 8,9,10,11,12 are 12,13,14,15,16 in later files
    Jan_Data_2.rename(columns={1: 'Time'}, inplace=True)
    Jan_Data_2.rename(columns={2: 'NO (ppb)'}, inplace=True)
    Jan_Data_2.rename(columns={3: 'Diff (ppb)'}, inplace=True)
    Jan_Data_2.rename(columns={4: 'NOy (ppb)'}, inplace=True)
    Jan_Data_2.rename(columns={5: 'NOy Flow (l/min)'}, inplace=True)
    Jan_Data_2.rename(columns={6: 'NOy Pressure (mmHG)'}, inplace=True)
    Jan_Data_2.rename(columns={8: 'NO2 (ppb)'}, inplace=True)
    Jan_Data_2.rename(columns={9: 'Ozone (ppb)'}, inplace=True)
    Jan_Data_2.rename(columns={10: 'NOy Flags'}, inplace=True)
    Jan_Data_2.rename(columns={11: 'NO2 Status'}, inplace=True)
    Jan_Data_2.rename(columns={12: 'O3 Flags'}, inplace=True)
    Jan_Data_2.rename(columns={15: 'SO2 (ppb)'}, inplace=True) #15,18 are columns 20 & 23 in later files
    Jan_Data_2.rename(columns={18: 'SO2 Flags'}, inplace=True) 
    
    jan_files_3 = str(Data_Source_Folder) + '201901101306*' + '_gas.csv' 
    jan_files_4 = str(Data_Source_Folder) + '2019011*59' + '_gas.csv' 
    jan_files_5 = str(Data_Source_Folder) + '20190111*' + '_gas.csv' 
    jan_files_6 = str(Data_Source_Folder) + '20190112*' + '_gas.csv' 
    jan_files_7 = str(Data_Source_Folder) + '20190113*' + '_gas.csv' 
    jan_files_8 = str(Data_Source_Folder) + '20190119*' + '_gas.csv' 
    jan_files_9 = str(Data_Source_Folder) + '2019012*' + '_gas.csv' 
    
    csv_files = glob.glob(jan_files_3) + glob.glob(jan_files_4) + glob.glob(jan_files_5) + glob.glob(jan_files_6) + glob.glob(jan_files_7) + glob.glob(jan_files_8) + glob.glob(jan_files_9)

    gas_frames = []

    for csv in csv_files:
    
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, header=None, usecols=[0,1,2,3,4,5,6,12,13,14,15,16,20,23])
        gas_frames.append(df)

    early_Data = pd.concat(gas_frames) 
    
    early_Data.rename(columns={0: 'Date'}, inplace=True)
    early_Data.rename(columns={1: 'Time'}, inplace=True)
    early_Data.rename(columns={2: 'NO (ppb)'}, inplace=True)
    early_Data.rename(columns={3: 'Diff (ppb)'}, inplace=True)
    early_Data.rename(columns={4: 'NOy (ppb)'}, inplace=True)
    early_Data.rename(columns={5: 'NOy Flow (l/min)'}, inplace=True)
    early_Data.rename(columns={6: 'NOy Pressure (mmHG)'}, inplace=True)
    early_Data.rename(columns={12: 'NO2 (ppb)'}, inplace=True)
    early_Data.rename(columns={13: 'Ozone (ppb)'}, inplace=True)
    early_Data.rename(columns={14: 'NOy Flags'}, inplace=True)
    early_Data.rename(columns={15: 'NO2 Status'}, inplace=True)
    early_Data.rename(columns={16: 'O3 Flags'}, inplace=True)
    early_Data.rename(columns={20: 'SO2 (ppb)'}, inplace=True)
    early_Data.rename(columns={23: 'SO2 Flags'}, inplace=True)   
    
    early_Data = pd.concat([early_Data, Jan_Data_1, Jan_Data_2])

elif start_year_month_str == '201906':
    june_files_1 = str(Data_Source_Folder) + '201906*0000' + '_gas.csv'
    june_files_2 = str(Data_Source_Folder) + '201906*59' + '_gas.csv' #removing file labelled 201906171837_gas
    june_files_3 = str(Data_Source_Folder) + '201906*01' + '_gas.csv' #removing file labelled 201906201338_gas
    june_files_4 = str(Data_Source_Folder) + '201906*56' + '_gas.csv'
    june_files_5 = str(Data_Source_Folder) + '201906*37' + '_gas.csv'
    csv_files = glob.glob(june_files_1) + glob.glob(june_files_2) + glob.glob(june_files_3) + glob.glob(june_files_4) + glob.glob(june_files_5)

    gas_frames = []

    for csv in csv_files:
    
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, header=None, usecols=[0,1,2,3,4,5,6,12,13,14,15,16,20,23])
        gas_frames.append(df)

    early_Data = pd.concat(gas_frames) 

    early_Data.rename(columns={0: 'Date'}, inplace=True)
    early_Data.rename(columns={1: 'Time'}, inplace=True)
    early_Data.rename(columns={2: 'NO (ppb)'}, inplace=True)
    early_Data.rename(columns={3: 'Diff (ppb)'}, inplace=True)
    early_Data.rename(columns={4: 'NOy (ppb)'}, inplace=True)
    early_Data.rename(columns={5: 'NOy Flow (l/min)'}, inplace=True)
    early_Data.rename(columns={6: 'NOy Pressure (mmHG)'}, inplace=True)
    early_Data.rename(columns={12: 'NO2 (ppb)'}, inplace=True)
    early_Data.rename(columns={13: 'Ozone (ppb)'}, inplace=True)
    early_Data.rename(columns={14: 'NOy Flags'}, inplace=True)
    early_Data.rename(columns={15: 'NO2 Status'}, inplace=True)
    early_Data.rename(columns={16: 'O3 Flags'}, inplace=True)
    early_Data.rename(columns={20: 'SO2 (ppb)'}, inplace=True)
    early_Data.rename(columns={23: 'SO2 Flags'}, inplace=True)

else:
    gas_frames = []

    for csv in csv_files:
    
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, header=None, usecols=[0,1,2,3,4,5,6,12,13,14,15,16,20,23])
        gas_frames.append(df)

    early_Data = pd.concat(gas_frames) 

    early_Data.rename(columns={0: 'Date'}, inplace=True)
    early_Data.rename(columns={1: 'Time'}, inplace=True)
    early_Data.rename(columns={2: 'NO (ppb)'}, inplace=True)
    early_Data.rename(columns={3: 'Diff (ppb)'}, inplace=True)
    early_Data.rename(columns={4: 'NOy (ppb)'}, inplace=True)
    early_Data.rename(columns={5: 'NOy Flow (l/min)'}, inplace=True)
    early_Data.rename(columns={6: 'NOy Pressure (mmHG)'}, inplace=True)
    early_Data.rename(columns={12: 'NO2 (ppb)'}, inplace=True)
    early_Data.rename(columns={13: 'Ozone (ppb)'}, inplace=True)
    early_Data.rename(columns={14: 'NOy Flags'}, inplace=True)
    early_Data.rename(columns={15: 'NO2 Status'}, inplace=True)
    early_Data.rename(columns={16: 'O3 Flags'}, inplace=True)
    early_Data.rename(columns={20: 'SO2 (ppb)'}, inplace=True)
    early_Data.rename(columns={23: 'SO2 Flags'}, inplace=True)

early_Data.drop(early_Data[(early_Data['Diff (ppb)'] == 'NaN')].index,inplace =True)
early_Data['Date'] = early_Data['Date'].astype(str)
early_Data['Date_length'] = early_Data['Date'].str.len()
early_Data=early_Data.loc[early_Data.Date_length == 10] #check the data string length for corruption
early_Data = early_Data.drop(columns=['Date_length'])
early_Data['datetime'] = early_Data['Date']+' '+early_Data['Time']# added Date and time into new columns
early_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in early_Data['datetime']] #converts the dateTime format from string to python dateTime
early_Data.index = early_Data['datetime']
early_Data = early_Data.sort_index()

early_Data.drop(early_Data[(early_Data['NO2 (ppb)']  == '0C100000')].index,inplace =True)
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags'].isnull()), 'CC000000', early_Data['NOy Flags'])


early_Data['NO (ppb)'] = early_Data['NO (ppb)'].astype(float)
early_Data['NOy (ppb)'] = early_Data['NOy (ppb)'].astype(float)
early_Data['NO2 (ppb)'] = early_Data['NO2 (ppb)'].astype(float)
early_Data['Ozone (ppb)'] = early_Data['Ozone (ppb)'].astype(float)
early_Data['Ozone (ppb)'] = early_Data['Ozone (ppb)'].astype(float)
early_Data['CO (ppb)'] = np.nan
early_Data['CO Flags'] = np.nan

default_Later_Month = '201912'

later_Date = np.where((start_year_month_str == end_year_month_str) & ((year_start >= 2020) | ((year_start == 2019) & (month_start >= 11))),  start_year_month_str, default_Later_Month)
print(later_Date)

#all_Data = pd.concat(map(pd.read_csv, glob.glob(str(Data_Source_Folder) + str(later_Date) + '*_firsgas.csv')),sort=True)

pattern = str(Data_Source_Folder) + str(later_Date) + '*_firsgas.csv'

if start_year_month_str == '201911':
    pattern_1 = str(Data_Source_Folder) + '2019112' + '*_firsgas.csv'
    pattern_2 = str(Data_Source_Folder) + '2019111' + '*00_firsgas.csv'
    pattern_3 = str(Data_Source_Folder) + '2019111' + '*11_firsgas.csv'
    pattern_4 = str(Data_Source_Folder) + '2019111' + '*23_firsgas.csv'
    csv_files = glob.glob(pattern_1) + glob.glob(pattern_2) + glob.glob(pattern_3) + glob.glob(pattern_4)

else:
    csv_files = glob.glob(pattern)

gas_frames = []

for csv in csv_files:
    
    #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv, header=None, usecols=[0,1,2,3,4,5,6,7,8,12,13,16,17,18,20,21])
    gas_frames.append(df)

all_Data = pd.concat(gas_frames) 

#all_Data.rename(columns={'NOy Flags': 'NOyFlags'}, inplace=True)

all_Data.rename(columns={0: 'Date'}, inplace=True)
all_Data.rename(columns={1: 'Time'}, inplace=True)
all_Data.rename(columns={2: 'NO (ppb)'}, inplace=True)
all_Data.rename(columns={3: 'Diff (ppb)'}, inplace=True)
all_Data.rename(columns={4: 'NOy (ppb)'}, inplace=True)
all_Data.rename(columns={5: 'NOy Flow (l/min)'}, inplace=True)
all_Data.rename(columns={6: 'NOy Pressure (mmHG)'}, inplace=True)
all_Data.rename(columns={7: 'NO2 (ppb)'}, inplace=True)
all_Data.rename(columns={8: 'Ozone (ppb)'}, inplace=True)
all_Data.rename(columns={12: 'CO (ppb)'}, inplace=True)
all_Data.rename(columns={13: 'SO2 (ppb)'}, inplace=True)
all_Data.rename(columns={16: 'NOy Flags'}, inplace=True)
all_Data.rename(columns={17: 'O3 Flags'}, inplace=True)
all_Data.rename(columns={18: 'NO2 Status'}, inplace=True)
all_Data.rename(columns={20: 'CO Flags'}, inplace=True)
all_Data.rename(columns={21: 'SO2 Flags'}, inplace=True)

all_Data.drop(all_Data[(all_Data['Diff (ppb)'] == 'NaN')].index,inplace =True)
all_Data['Date'] = all_Data['Date'].astype(str)
all_Data['Date_length'] = all_Data['Date'].str.len()
all_Data=all_Data.loc[all_Data.Date_length == 10] 
all_Data['Time'] = all_Data['Time'].astype(str)
all_Data['Time_length'] = all_Data['Time'].str.len()
all_Data=all_Data.loc[all_Data.Time_length == 8] #check the data string length for corruption
all_Data = all_Data.drop(columns=['Date_length', 'Time_length'])


all_Data['datetime'] = all_Data['Date']+' '+all_Data['Time']# added Date and time into new columns
all_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in all_Data['datetime']]  #converts the dateTime format from string to python dateTime
all_Data.index = all_Data['datetime']
all_Data = all_Data.drop(columns=['Date', 'Time'])
all_Data = all_Data.sort_index()

all_Data['NO (ppb)'] = all_Data['NO (ppb)'].astype(float)
all_Data['NOy (ppb)'] = all_Data['NOy (ppb)'].astype(float)
all_Data['NO2 (ppb)'] = all_Data['NO2 (ppb)'].astype(float)
all_Data['Ozone (ppb)'] = all_Data['Ozone (ppb)'].astype(float)

all_Data.drop(all_Data[(all_Data['CO (ppb)'] == 'FFFFFFFF')].index,inplace =True)
all_Data.drop(all_Data[(all_Data['CO (ppb)'] == '0C100000')].index,inplace =True)
all_Data['CO (ppb)'] = all_Data['CO (ppb)'].astype(float)

all_Data = pd.concat([early_Data, all_Data])
all_Data = all_Data[start:end]
all_Data = all_Data.sort_index()

all_Data['All_Data_Flag'] = 1

start_simon = datetime.datetime(2018,12,18,0,0,00) #data from instruments located in room 2.10 Simon Building
end_simon = datetime.datetime(2019,1,29,23,59,00)
all_Data.loc[start_simon:end_simon, ('All_Data_Flag')] = 2

start_move_1 = datetime.datetime(2019,1,30,0,0,00) #instrument moved to FIRS trailer
end_move_1 = datetime.datetime(2019,1,30,23,59,00)
all_Data.loc[start_move_1:end_move_1, ('All_Data_Flag')] = 2

start_audit1 = datetime.datetime(2019,8,9,6,30,00)
end_audit1 = datetime.datetime(2019,8,9,12,00,00)
all_Data.loc[start_audit1:end_audit1, ('All_Data_Flag')] = 0

start_Anom_1 = datetime.datetime(2018,12,21,13,0,00)
end_Anom_1 = datetime.datetime(2018,12,21,17,0,00)
all_Data.loc[start_Anom_1:end_Anom_1, ('All_Data_Flag')] = 0

#Calibration Day 2
year_Audit_2 = 2020 #input the year of study
month_Audit_2 = 3 #input the month of study
day_Audit_2 = 18 #default start date set

#Calibration Day 3
year_Audit_3 = 2020 #input the year of study
month_Audit_3 = 10 #input the month of study
day_Audit_3 = 2 #default start date set

#Audit 4
year_Audit_4 = 2021 #input the year of study
month_Audit_4 = 3 #input the month of study
day_Audit_4 = 30 #default start date set

#Audit 5
year_Audit_5 = 2021 #input the year of study
month_Audit_5 = 10 #input the month of study
day_Audit_5 = 27 #default start date set

start_Audit_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,9,28,00)
end_Audit_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,14,35,00)
all_Data.loc[start_Audit_2:end_Audit_2,  ('All_Data_Flag')] = 0

start_Audit_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,24,00)
end_Audit_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,10,44,00)
all_Data.loc[start_Audit_3:end_Audit_3,  ('All_Data_Flag')] = 0

start_Audit_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,5,00)
end_Audit_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,14,40,00)
all_Data.loc[start_Audit_4:end_Audit_4,  ('All_Data_Flag')] = 0

start_Audit_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,7,26,00)
end_Audit_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,11,25,00)
all_Data.loc[start_Audit_5:end_Audit_5,  ('All_Data_Flag')] = 0

#Audit 5
year_Audit_6 = 2022 #input the year of study
month_Audit_6 = 5 #input the month of study
day_Audit_6 = 4 #default start date set

start_Audit_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,8,30,00)
end_Audit_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,12,13,00)
all_Data.loc[start_Audit_6:end_Audit_6,  ('All_Data_Flag')] = 0

start_uncertainty = datetime.datetime(2018,12,18,0,0,00)
end_uncertainty = datetime.datetime(2019,1,10,23,59,00)
all_Data.loc[start_uncertainty:end_uncertainty,  ('All_Data_Flag')] = 2

start_Anom_2 = datetime.datetime(2019,4,25,22,40,00)
end_Anom_2 = datetime.datetime(2019,4,25,22,45,00)
all_Data.loc[start_Anom_2:end_Anom_2, ('All_Data_Flag')] = 0

all_Data.drop(all_Data[(all_Data['All_Data_Flag'] == 0)].index,inplace =True)

gas_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/gas_Analysers/'
check_Folder = os.path.isdir(gas_Folder)
if not check_Folder:
    os.makedirs(gas_Folder)
    print("created folder : ", gas_Folder)

else:
    print(gas_Folder, "folder already exists.")

if start_year_month_str == '202106' or start_year_month_str == '202107':
    SO2_Data = all_Data[['SO2 (ppb)', 'SO2 Flags']]
    SO2_Data['SO2 Flags'] = np.where((SO2_Data['SO2 Flags']=='FFFFFFFF'), 0, 1) # two flags are 'FFFFFFFF' which indicates no data and '4' which indicates data running
    SO2_Data.drop(SO2_Data[(SO2_Data['SO2 Flags'] == 0)].index,inplace =True)
    SO2_Data.drop(SO2_Data[(SO2_Data['SO2 (ppb)'] == 'Sampling')].index,inplace =True)
    SO2_Data['SO2 (ppb)'] = SO2_Data['SO2 (ppb)'].astype(float)
    SO2_Data = SO2_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
    SO2_Data['SO2 Flags'] = SO2_Data['SO2 Flags'].astype(float)
    SO2_Data['SO2_Prelim_Flag'] = np.where((SO2_Data['SO2 Flags']>1), 2, 1)
    SO2_Data.drop(SO2_Data[(SO2_Data['SO2_Prelim_Flag'] == 2)].index,inplace =True)
    SO2_Data['SO2 Flags'] = SO2_Data['SO2_Prelim_Flag']
    SO2_Data['SO2 Flags'] = SO2_Data['SO2 Flags'].astype(str)
    SO2_Data = SO2_Data.drop(columns=['SO2_Prelim_Flag'])
    SO2_Data.drop(SO2_Data[(SO2_Data['SO2 (ppb)'].isnull())].index,inplace =True)
    SO2_Data.drop(SO2_Data[(SO2_Data['SO2 (ppb)'] == 0)].index,inplace =True)
    
    plt.plot(SO2_Data['SO2 (ppb)'], label='SO2')
    plt.legend()
    plt.ylabel('ppb')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 16}

    plt.rc('font', **font)
    #plt.ylim(10, 30)
    #plt.figure()
    plt.show()

    SO2_Data.to_csv(str(gas_Folder) + 'maqs-SO2-concentration' + str(status) + str(date_file_label) + '_' + str(version_number) + '.csv')
else:
    print('no SO2 Data here')

NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime', 'All_Data_Flag']]

NOy_Data.drop(NOy_Data[(NOy_Data['NO (ppb)'] == 'FFFFFFFF')].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NOy (ppb)'] == 'FFFFFFFF')].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NO (ppb)'] == 'nan')].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NO (ppb)'] == 'NaN')].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NOy (ppb)'] == 'nan')].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NOy (ppb)'] == 'NaN')].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NO (ppb)'].isnull())].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NOy (ppb)'].isnull())].index,inplace =True)
NOy_Data['NOy (ppb)'] = NOy_Data['NOy (ppb)'].astype(float)
NOy_Data['NOy (ppb)'] = NOy_Data['NOy (ppb)'].astype(float)
NOy_Data.drop(NOy_Data[(NOy_Data['NO (ppb)'].isnull())].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NO (ppb)'] == 0)].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NOy (ppb)'].isnull())].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NOy (ppb)'] == 0)].index,inplace =True)

NOy_Data['NOy Flags']= NOy_Data['NOy Flags'].str.lstrip().astype(str)
NOy_Data['NOy Flags']= NOy_Data['NOy Flags'].str.rstrip().astype(str)
NOy_Data['NOy Flags']= np.where(NOy_Data['NOy Flags'].isnull() , 'CC000000', NOy_Data['NOy Flags'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC000000'), 1, NOy_Data['NOy Flags'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['All_Data_Flag']== 2), 2, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['All_Data_Flag']== 0), 0, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='FFFFFFFF'), 0, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where(NOy_Data['NOy Flags'].str.contains('CC03', case=False, na=False), 0, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where(NOy_Data['NOy Flags'].str.contains('CC00002', case=False, na=False), 0, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC000500'), 0, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC000422'), 0, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC000428'), 0, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC000002'), 2, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='FFFFFFFF'), 2, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC000100'), 2, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC000120'), 0, NOy_Data['NOy_Prelim_Flag'])#
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC000128'), 0, NOy_Data['NOy_Prelim_Flag'])#
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC000400'), 2, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC000420'), 0, NOy_Data['NOy_Prelim_Flag'])#
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC000600'), 2, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC001600'), 2, NOy_Data['NOy_Prelim_Flag'])#
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC008000'), 2, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC008002'), 0, NOy_Data['NOy_Prelim_Flag'])#
NOy_Data['NOy_Prelim_Flag'] = np.where(NOy_Data['NOy Flags'].str.contains('CC00802', case=False, na=False), 0, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy Flags']=='CC009600'), 2, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = NOy_Data['NOy_Prelim_Flag'].astype(float)
NOy_Data['NOy_Prelim_Flag'] = NOy_Data['NOy_Prelim_Flag'].astype(int)
#NOy_Data['NOy_Prelim_Flag'] = np.where(NOy_Data['NOy_Prelim_Flag'].isnull(), 1, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['NOy_Prelim_Flag'] = np.where((NOy_Data['NOy_Prelim_Flag'] == 0) | (NOy_Data['NOy_Prelim_Flag'] == 1) | (NOy_Data['NOy_Prelim_Flag'] == 2), NOy_Data['NOy_Prelim_Flag'], 2)

start_NOy_gas_sampling_check = datetime.datetime(2020,6,24,9,10,00) # NOy gas span without cal on turned on
end_NOy_gas_sampling_check = datetime.datetime(2020,6,24,12,14,59)
NOy_Data.loc[start_NOy_gas_sampling_check:end_NOy_gas_sampling_check, ('NOy_Prelim_Flag')] = 2

start_NOy_gas_span1 = datetime.datetime(2019,8,22,12,45,00) 
end_NOy_gas_span1 = datetime.datetime(2019,8,22,13,5,00)
NOy_Data.loc[start_NOy_gas_span1:end_NOy_gas_span1, ('NOy_Prelim_Flag')] = 0

start_NOy_gas_span2 = datetime.datetime(2019,9,6,14,10,00) 
end_NOy_gas_span2 = datetime.datetime(2019,9,6,14,30,00)
NOy_Data.loc[start_NOy_gas_span2:end_NOy_gas_span2, ('NOy_Prelim_Flag')] = 0

start_NOy_gas_span3 = datetime.datetime(2019,9,10,14,10,00)
end_NOy_gas_span3 = datetime.datetime(2019,9,10,14,50,00)
NOy_Data.loc[start_NOy_gas_span3:end_NOy_gas_span3, ('NOy_Prelim_Flag')] = 0

start_NOy_gas_span4 = datetime.datetime(2019,9,17,10,25,00)
end_NOy_gas_span4 = datetime.datetime(2019,9,17,10,45,00)
NOy_Data.loc[start_NOy_gas_span4:end_NOy_gas_span4, ('NOy_Prelim_Flag')] = 0

start_NOy_gas_span5 = datetime.datetime(2019,9,26,8,55,00)
end_NOy_gas_span5 = datetime.datetime(2019,9,26,9,15,00)
NOy_Data.loc[start_NOy_gas_span5:end_NOy_gas_span5, ('NOy_Prelim_Flag')] = 0

start_NOy_gas_span6 = datetime.datetime(2019,10,2,14,35,00)
end_NOy_gas_span6 = datetime.datetime(2019,10,2,14,55,00)
NOy_Data.loc[start_NOy_gas_span6:end_NOy_gas_span6, ('NOy_Prelim_Flag')] = 0

start_NOy_gas_span7 = datetime.datetime(2019,10,9,13,55,00)
end_NOy_gas_span7 = datetime.datetime(2019,10,9,14,15,00)
NOy_Data.loc[start_NOy_gas_span7:end_NOy_gas_span7, ('NOy_Prelim_Flag')] = 0

start_NOy_gas_span8 = datetime.datetime(2019,10,15,12,55,00)
end_NOy_gas_span8 = datetime.datetime(2019,10,15,13,25,00)
NOy_Data.loc[start_NOy_gas_span8:end_NOy_gas_span8, ('NOy_Prelim_Flag')] = 0

start_NOy_gas_span9 = datetime.datetime(2019,10,24,8,10,00)
end_NOy_gas_span9 = datetime.datetime(2019,10,24,9,10,00)
NOy_Data.loc[start_NOy_gas_span9:end_NOy_gas_span9, ('NOy_Prelim_Flag')] = 0

start_NOy_gas_span10 = datetime.datetime(2019,10,31,11,10,00)
end_NOy_gas_span10 = datetime.datetime(2019,10,31,11,40,00)
NOy_Data.loc[start_NOy_gas_span10:end_NOy_gas_span10, ('NOy_Prelim_Flag')] = 0

start_NOy_gas_span11 = datetime.datetime(2020,9,25,9,10,00)
end_NOy_gas_span11 = datetime.datetime(2020,9,25,10,40,00)
NOy_Data.loc[start_NOy_gas_span11:end_NOy_gas_span11, ('NOy_Prelim_Flag')] = 0

start_NOy_gas_span12 = datetime.datetime(2021,3,30,6,30,00)
end_NOy_gas_span12 = datetime.datetime(2021,3,30,10,40,00)
NOy_Data.loc[start_NOy_gas_span12:end_NOy_gas_span12, ('NOy_Prelim_Flag')] = 0

start_NOy_gas_span13 = datetime.datetime(2021,10,21,10,20,00)
end_NOy_gas_span13 = datetime.datetime(2021,10,21,10,50,00)
NOy_Data.loc[start_NOy_gas_span13:end_NOy_gas_span13, ('NOy_Prelim_Flag')] = 0

start_inlet_reconfig_1 = datetime.datetime(2019,8,9,16,30,00) # 09-08-2019 16:30 - 18:00 audit and calibration of FIDAS
end_inlet_reconfig_1 = datetime.datetime(2019,8,9,18,0,00)
NOy_Data.loc[start_inlet_reconfig_1:end_inlet_reconfig_1, ('NOy_Prelim_Flag')] = 0

start_NOy_spike = datetime.datetime(2022,9,3,20,0,00) 
end_NOy_spike = datetime.datetime(2022,9,5,4,0,00)
NOy_Data.loc[start_NOy_spike:end_NOy_spike, ('NOy_Prelim_Flag')] = 2
NOy_Data.drop(NOy_Data.loc[start_NOy_spike:end_NOy_spike].index, inplace=True)

start_NOy_spike_2 = datetime.datetime(2022,9,5,0,0,00) 
end_NOy_spike_2 = datetime.datetime(2022,9,5,0,20,00)
NOy_Data.loc[start_NOy_spike_2:end_NOy_spike_2, ('NOy_Prelim_Flag')] = 0

NOy_Data.drop(NOy_Data[(NOy_Data['NO (ppb)'] == 0)].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NOy (ppb)'] == 0)].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NO (ppb)'].isnull())].index,inplace =True)

NOy_Data['NO a'] = np.interp(NOy_Data['datetime'], NOy_Calib['datetime'], NOy_Calib['NO Zero (ppb)'])
NOy_Data['NO b'] = np.interp(NOy_Data['datetime'], NOy_Calib['datetime'], NOy_Calib['NO Response'])
NOy_Data['NO (ppb) perlim'] = (NOy_Data['NO (ppb)'] - NOy_Data['NO a'])*NOy_Data['NO b'] #or NOy_Data['NO (ppb)']*NOy_Data['NO b'] - NOy_Data['NO a']

NOy_Data['NOy a'] = np.interp(NOy_Data['datetime'], NOy_Calib['datetime'], NOy_Calib['NOy Zero (ppb)'])
NOy_Data['NOy b'] = np.interp(NOy_Data['datetime'], NOy_Calib['datetime'], NOy_Calib['NOy Response'])
NOy_Data['NOy (ppb) perlim'] = (NOy_Data['NOy (ppb)'] - NOy_Data['NOy a'])*NOy_Data['NOy b'] # or NOy_Data['NOy (ppb)']*NOy_Data['NOy b'] - NOy_Data['NOy a']

start_Cal_1 = datetime.datetime(2018,12,21,12,0,00)
end_Cal_1 = datetime.datetime(2018,12,21,17,0,00)
NOy_Cal_data = NOy_Data[start_Cal_1:end_Cal_1]
NOy_Cal_data['NOy_Prelim_Flag'] = np.where((NOy_Cal_data['NO (ppb)'] >100) , 0, NOy_Cal_data['NOy_Prelim_Flag']) 
NOy_Cal_data['NOy_Prelim_Flag'] = np.where((NOy_Cal_data['NOy (ppb)'] >100) , 0, NOy_Cal_data['NOy_Prelim_Flag']) 
NOy_Cal_flag = NOy_Cal_data['NOy_Prelim_Flag'] 
NOy_Data.loc[start_Cal_1:end_Cal_1, ('NOy_Prelim_Flag')] = pd.Series(NOy_Cal_flag)

NOy_Data_Drop = list(NOy_Data.columns.values)
NOy_Data_Drop.remove('NO (ppb) perlim')
NOy_Data_Drop.remove('NOy (ppb) perlim')
NOy_Data_Drop.remove('NOy_Prelim_Flag')
NOy_Data = NOy_Data.drop(columns=NOy_Data_Drop)

NOy_Data['NOy_Prelim_Flag'] = np.where(NOy_Data['NOy_Prelim_Flag'] == 0, 6, NOy_Data['NOy_Prelim_Flag'])
max_NOy_flag = NOy_Data['NOy_Prelim_Flag'].groupby(pd.Grouper(freq=av_Freq)).max() #this transfers over error from original cal checks into averaged data
NOy_Data = NOy_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
NOy_Data['NOy_Prelim_Flag'] = pd.Series(max_NOy_flag)
NOy_Data['NOy_Prelim_Flag'] = np.where(NOy_Data['NOy_Prelim_Flag'] == 6, 0, NOy_Data['NOy_Prelim_Flag'])
NOy_Data['Diff (ppb) perlim'] = NOy_Data['NOy (ppb) perlim'] - NOy_Data['NO (ppb) perlim']
NOy_Data.rename(columns={'NO (ppb) perlim': 'NO (ppb)', 'Diff (ppb) perlim': 'Diff (ppb)', 'NOy (ppb) perlim': 'NOy (ppb)', "NOy_Prelim_Flag": "NOy_qc_flags"}, inplace = True)

NOy_Data['NOy_qc_flags']= NOy_Data['NOy_qc_flags'].astype(str)
NOy_Data['NOy_qc_flags']= np.where(NOy_Data['NOy_qc_flags'] == 'nan', 2, NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags']= np.where(NOy_Data['NOy_qc_flags'] == 'NaN', 2, NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = NOy_Data['NOy_qc_flags'].astype(float)
NOy_Data['NOy_qc_flags'] = np.where(NOy_Data['NOy_qc_flags'] == 2, int(2), NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags']= np.where(NOy_Data['NOy_qc_flags'] == 1, int(1), NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags']= np.where(NOy_Data['NOy_qc_flags'] == 0, int(0), NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = NOy_Data['NOy_qc_flags'].astype(int)

NOy_Data['NOy_qc_flags'] =np.where((NOy_Data['NOy (ppb)']>300) & (NOy_Data['NOy_qc_flags'] == 1),2, NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] =np.where((NOy_Data['NO (ppb)']<-5) & (NOy_Data['NOy_qc_flags'] == 1),2, NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] =np.where((NOy_Data['Diff (ppb)']<-5) & (NOy_Data['NOy_qc_flags'] == 1),2, NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] =np.where((NOy_Data['NOy (ppb)']<-5) & (NOy_Data['NOy_qc_flags'] == 1),2, NOy_Data['NOy_qc_flags'])

NOy_Data['NOy_qc_flags_-6_offset'] = NOy_Data['NOy_qc_flags'].shift(periods=-6) #setting up columns to bloc off the area around flagged data
NOy_Data['NOy_qc_flags_-5_offset'] = NOy_Data['NOy_qc_flags'].shift(periods=-5)
NOy_Data['NOy_qc_flags_-4_offset'] = NOy_Data['NOy_qc_flags'].shift(periods=-4)
NOy_Data['NOy_qc_flags_-3_offset'] = NOy_Data['NOy_qc_flags'].shift(periods=-3)
NOy_Data['NOy_qc_flags_-2_offset'] = NOy_Data['NOy_qc_flags'].shift(periods=-2)
NOy_Data['NOy_qc_flags_-1_offset'] = NOy_Data['NOy_qc_flags'].shift(periods=-1) 
NOy_Data['NOy_qc_flags_+1_offset'] = NOy_Data['NOy_qc_flags'].shift(periods=1)
NOy_Data['NOy_qc_flags_+2_offset'] = NOy_Data['NOy_qc_flags'].shift(periods=2)
NOy_Data['NOy_qc_flags_+3_offset'] = NOy_Data['NOy_qc_flags'].shift(periods=3)
NOy_Data['NOy_qc_flags_+4_offset'] = NOy_Data['NOy_qc_flags'].shift(periods=4)
NOy_Data['NOy_qc_flags_+5_offset'] = NOy_Data['NOy_qc_flags'].shift(periods=5)
NOy_Data['NOy_qc_flags_+6_offset'] = NOy_Data['NOy_qc_flags'].shift(periods=6)
NOy_Data['NOy_qc_flags_-6_offset'] = np.where(NOy_Data['NOy_qc_flags'] == 0, NOy_Data['NOy_qc_flags'], NOy_Data['NOy_qc_flags_-6_offset'])
NOy_Data['NOy_qc_flags_-5_offset'] = np.where(NOy_Data['NOy_qc_flags'] == 0, NOy_Data['NOy_qc_flags'], NOy_Data['NOy_qc_flags_-5_offset'])
NOy_Data['NOy_qc_flags_-4_offset'] = np.where(NOy_Data['NOy_qc_flags'] == 0, NOy_Data['NOy_qc_flags'], NOy_Data['NOy_qc_flags_-4_offset'])
NOy_Data['NOy_qc_flags_-3_offset'] = np.where(NOy_Data['NOy_qc_flags'] == 0, NOy_Data['NOy_qc_flags'], NOy_Data['NOy_qc_flags_-3_offset'])
NOy_Data['NOy_qc_flags_-2_offset'] = np.where(NOy_Data['NOy_qc_flags'] == 0, NOy_Data['NOy_qc_flags'], NOy_Data['NOy_qc_flags_-2_offset'])
NOy_Data['NOy_qc_flags_-1_offset'] = np.where(NOy_Data['NOy_qc_flags'] == 0, NOy_Data['NOy_qc_flags'], NOy_Data['NOy_qc_flags_-1_offset'])
NOy_Data['NOy_qc_flags_+1_offset'] = np.where(NOy_Data['NOy_qc_flags'] == 0, NOy_Data['NOy_qc_flags'], NOy_Data['NOy_qc_flags_+1_offset'])
NOy_Data['NOy_qc_flags_+2_offset'] = np.where(NOy_Data['NOy_qc_flags'] == 0, NOy_Data['NOy_qc_flags'], NOy_Data['NOy_qc_flags_+2_offset'])
NOy_Data['NOy_qc_flags_+3_offset'] = np.where(NOy_Data['NOy_qc_flags'] == 0, NOy_Data['NOy_qc_flags'], NOy_Data['NOy_qc_flags_+3_offset'])
NOy_Data['NOy_qc_flags_+4_offset'] = np.where(NOy_Data['NOy_qc_flags'] == 0, NOy_Data['NOy_qc_flags'], NOy_Data['NOy_qc_flags_+4_offset'])
NOy_Data['NOy_qc_flags_+5_offset'] = np.where(NOy_Data['NOy_qc_flags'] == 0, NOy_Data['NOy_qc_flags'], NOy_Data['NOy_qc_flags_+5_offset'])
NOy_Data['NOy_qc_flags_+6_offset'] = np.where(NOy_Data['NOy_qc_flags'] == 0, NOy_Data['NOy_qc_flags'], NOy_Data['NOy_qc_flags_+6_offset'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_-6_offset']!=1) & (NOy_Data['NOy_qc_flags_-6_offset'].notnull() ),NOy_Data['NOy_qc_flags_-6_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_-5_offset']!=1) & (NOy_Data['NOy_qc_flags_-5_offset'].notnull() ),NOy_Data['NOy_qc_flags_-5_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_-4_offset']!=1) & (NOy_Data['NOy_qc_flags_-4_offset'].notnull() ),NOy_Data['NOy_qc_flags_-4_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_-3_offset']!=1) & (NOy_Data['NOy_qc_flags_-3_offset'].notnull() ),NOy_Data['NOy_qc_flags_-3_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_-2_offset']!=1) & (NOy_Data['NOy_qc_flags_-2_offset'].notnull() ),NOy_Data['NOy_qc_flags_-2_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_-1_offset']!=1) & (NOy_Data['NOy_qc_flags_-1_offset'].notnull() ),NOy_Data['NOy_qc_flags_-1_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_+1_offset']!=1) & (NOy_Data['NOy_qc_flags_+1_offset'].notnull() ),NOy_Data['NOy_qc_flags_+1_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_+2_offset']!=1) & (NOy_Data['NOy_qc_flags_+2_offset'].notnull() ),NOy_Data['NOy_qc_flags_+2_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_+3_offset']!=1) & (NOy_Data['NOy_qc_flags_+3_offset'].notnull() ),NOy_Data['NOy_qc_flags_+3_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_+4_offset']!=1) & (NOy_Data['NOy_qc_flags_+4_offset'].notnull() ),NOy_Data['NOy_qc_flags_+4_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_+5_offset']!=1) & (NOy_Data['NOy_qc_flags_+5_offset'].notnull() ),NOy_Data['NOy_qc_flags_+5_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_+6_offset']!=1) & (NOy_Data['NOy_qc_flags_+6_offset'].notnull() ),NOy_Data['NOy_qc_flags_+6_offset'],NOy_Data['NOy_qc_flags'])
NOy_Flag_Offset = list(NOy_Data.columns.values)
NOy_Flag_Offset.remove('NO (ppb)')
NOy_Flag_Offset.remove('Diff (ppb)')
NOy_Flag_Offset.remove('NOy (ppb)')
NOy_Flag_Offset.remove('NOy_qc_flags')
#NOy_Data = NOy_Data.drop(columns=NOy_Flag_Offset) #dropping newly made columns flagged data

start_NOy_flow_1 = datetime.datetime(2021,3,30,8,45,00) #extension to audit carried out on NOy
end_NOy_flow_1 = datetime.datetime(2021,3,30,15,50,00)
NOy_Data.loc[start_NOy_flow_1:end_NOy_flow_1, ('NOy_qc_flags')] = 0

NOy_Data.drop(NOy_Data[(NOy_Data['NOy_qc_flags'] == 0)].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NO (ppb)'] == 0)].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['Diff (ppb)'] == 0)].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NOy (ppb)'] == 0)].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NO (ppb)'].isnull() )].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['Diff (ppb)'].isnull() )].index,inplace =True)
NOy_Data.drop(NOy_Data[(NOy_Data['NOy (ppb)'].isnull() )].index,inplace =True)

NOy_Data['NOy_qc_flags'] = NOy_Data['NOy_qc_flags'].astype(float)
NOy_Data['NOy_qc_flags'] = NOy_Data['NOy_qc_flags'].astype(int)
NOy_Data['NOy_qc_flags'] = NOy_Data['NOy_qc_flags'].astype(str)

NOy_Data = NOy_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy_qc_flags']]

plt.plot(NOy_Data['NO (ppb)'], label='NO')
plt.plot(NOy_Data['NOy (ppb)'], label='NOy')
#plt.plot(NOy_Data['NOy_qc_flags'], label='NOy Flags')
plt.legend()
plt.ylabel('ppb')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

NOy_Data.to_csv(str(gas_Folder) + 'Thermo-42iy_maqs_' +  str(date_file_label) + '_nox-noxy-concentration' + str(status) + str(version_number) + '.csv')

NOy_Data['TimeDateSince'] = NOy_Data.index-datetime.datetime(1970,1,1,0,0,00)
NOy_Data['TimeSecondsSince'] = NOy_Data['TimeDateSince'].dt.total_seconds()
NOy_Data['day_year'] = pd.DatetimeIndex(NOy_Data['TimeDateSince'].index).dayofyear
NOy_Data['year'] = pd.DatetimeIndex(NOy_Data['TimeDateSince'].index).year
NOy_Data['month'] = pd.DatetimeIndex(NOy_Data['TimeDateSince'].index).month
NOy_Data['day'] = pd.DatetimeIndex(NOy_Data['TimeDateSince'].index).day
NOy_Data['hour'] = pd.DatetimeIndex(NOy_Data['TimeDateSince'].index).hour
NOy_Data['minute'] = pd.DatetimeIndex(NOy_Data['TimeDateSince'].index).minute
NOy_Data['second'] = pd.DatetimeIndex(NOy_Data['TimeDateSince'].index).second

NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime', 'All_Data_Flag']]
NO2_Data.drop(NO2_Data[(NO2_Data['NO2 (ppb)'] == 'FFFFFFFF')].index,inplace =True)
NO2_Data.drop(NO2_Data[(NO2_Data['NO2 (ppb)'].isnull())].index,inplace =True)
NO2_Data['NO2 (ppb)'] = NO2_Data['NO2 (ppb)'].astype(float)
NO2_Data.drop(NO2_Data[(NO2_Data['NO2 (ppb)'] == 0)].index,inplace =True)
NO2_Data.drop(NO2_Data[(NO2_Data['NO2 (ppb)'].isnull())].index,inplace =True)
NO2_Data['NO2 Status'] = NO2_Data['NO2 Status'].str.lstrip().astype(str)
NO2_Data['NO2 Status'] = NO2_Data['NO2 Status'].str.rstrip().astype(str)
NO2_Data['NO2 Status']= np.where(NO2_Data['NO2 Status'].isnull() , 'Sampling', NO2_Data['NO2 Status'])
NO2_Data['NO2_Prelim_Flag'] = np.where((NO2_Data['NO2 Status']=='Sampling'), 1,NO2_Data['NO2 Status'])
NO2_Data['NO2_Prelim_Flag'] = np.where((NO2_Data['NO2 Status']=='Recovering'), 0, NO2_Data['NO2_Prelim_Flag'])
NO2_Data['NO2_Prelim_Flag'] = np.where((NO2_Data['NO2 Status']=='RecoveringZ'),0, NO2_Data['NO2_Prelim_Flag'])
NO2_Data['NO2_Prelim_Flag'] = np.where((NO2_Data['NO2 Status']=='RecoveringS'), 0, NO2_Data['NO2_Prelim_Flag'])
NO2_Data['NO2_Prelim_Flag'] = np.where((NO2_Data['NO2 Status']=='FFFFFFFF'), 2, NO2_Data['NO2_Prelim_Flag'])
NO2_Data['NO2_Prelim_Flag'] = np.where((NO2_Data['NO2 Status']=='Zero Cal Check in progress'), 0, NO2_Data['NO2_Prelim_Flag'])
NO2_Data['NO2_Prelim_Flag'] = np.where((NO2_Data['NO2 Status']=='Zero Cal In Progress'), 0, NO2_Data['NO2_Prelim_Flag'])
NO2_Data['NO2_Prelim_Flag'] = np.where((NO2_Data['NO2 Status']=='External Cal'), 0, NO2_Data['NO2_Prelim_Flag'])
NO2_Data['NO2_Prelim_Flag'] = np.where((NO2_Data['NO2 Status']=='Span Check In Progress'), 0, NO2_Data['NO2_Prelim_Flag'])
NO2_Data['NO2_Prelim_Flag'] = np.where((NO2_Data['All_Data_Flag']== 2), 2, NO2_Data['NO2_Prelim_Flag'])
NO2_Data['NO2_Prelim_Flag'] = np.where((NO2_Data['All_Data_Flag']== 0), 0, NO2_Data['NO2_Prelim_Flag'])
NO2_Data['NO2_Prelim_Flag'] = np.where((NO2_Data['NO2 Status']=='FFFFFFFF'), 0, NO2_Data['NO2_Prelim_Flag'])
NO2_Data['NO2_Prelim_Flag'] = NO2_Data['NO2_Prelim_Flag'].astype(float)
#NO2_Data.drop(NO2_Data[(NO2_Data['NO2_Prelim_Flag'].isnull() )].index,inplace =True)
NO2_Data['NO2_Prelim_Flag'] = NO2_Data['NO2_Prelim_Flag'].astype(int)

start_NO2_false_zero1 = datetime.datetime(2020,4,2,0,0,00)
end_NO2_false_zero1 = datetime.datetime(2020,4,2,10,0,00)
NO2_Data.loc[start_NO2_false_zero1:end_NO2_false_zero1, ('NO2_Prelim_Flag')] = 0

start_NO2_Early_Cals = datetime.datetime(2018,12,1,0,0,00)
end_NO2_Early_Cals = datetime.datetime(2019,1,31,23,59,00)
Early_NO2_data = NO2_Data[start_NO2_Early_Cals:end_NO2_Early_Cals]
Early_NO2_data['NO2_Prelim_Flag'] = np.where((Early_NO2_data['NO2 (ppb)'] <0.5) , 0, Early_NO2_data['NO2_Prelim_Flag']) 
NO2_Early_flags = Early_NO2_data['NO2_Prelim_Flag']
NO2_Data.loc[start_Cal_1:end_Cal_1, ('NO2_Prelim_Flag')] = pd.Series(NO2_Early_flags)

NO2_Data['NO2 a'] = np.interp(NO2_Data['datetime'], Other_Gas_Cals['datetime'], Other_Gas_Cals['NO2 Zero (ppb)'])
NO2_Data['NO2 b'] = np.interp(NO2_Data['datetime'], Other_Gas_Cals['datetime'], Other_Gas_Cals['NO2 Response'])
NO2_Data['NO2 (ppb) perlim'] = (NO2_Data['NO2 (ppb)'] - NO2_Data['NO2 a'])*NO2_Data['NO2 b'] # or NOy_Data['NOy (ppb)']*NOy_Data['NOy b'] - NOy_Data['NOy a']

NO2_Data_Drop = list(NO2_Data.columns.values)
NO2_Data_Drop.remove('NO2 (ppb) perlim')
NO2_Data_Drop.remove('NO2_Prelim_Flag')
NO2_Data = NO2_Data.drop(columns=NO2_Data_Drop)

NO2_Data['NO2_Prelim_Flag'] = np.where(NO2_Data['NO2_Prelim_Flag'] == 0, 6, NO2_Data['NO2_Prelim_Flag'])
max_NO2_flag = NO2_Data['NO2_Prelim_Flag'].groupby(pd.Grouper(freq=av_Freq)).max() #this transfers over error from original cal checks into averaged data
NO2_Data = NO2_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
NO2_Data['NO2_Prelim_Flag'] = pd.Series(max_NO2_flag)
NO2_Data['NO2_Prelim_Flag'] = np.where(NO2_Data['NO2_Prelim_Flag'] == 6, 0, NO2_Data['NO2_Prelim_Flag'])

NO2_Data.rename(columns={'NO2 (ppb) perlim': 'NO2 (ppb)', "NO2_Prelim_Flag": "NO2_qc_flags"}, inplace = True)

NO2_Data['NO2_qc_flags'] = NO2_Data['NO2_qc_flags'].astype(str)
NO2_Data['NO2_qc_flags'] = np.where(NO2_Data['NO2_qc_flags'] == 'nan', 2, NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = NO2_Data['NO2_qc_flags'].astype(float)
NO2_Data['NO2_qc_flags'] = np.where(NO2_Data['NO2_qc_flags'] == 2, int(2), NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where(NO2_Data['NO2_qc_flags'] == 1, int(1), NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where(NO2_Data['NO2_qc_flags'] == 0, int(0), NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = NO2_Data['NO2_qc_flags'].astype(int)

NO2_Data['NO2_qc_flags'] =np.where((NO2_Data['NO2 (ppb)']<0) & (NO2_Data['NO2_qc_flags'] == 1),2, NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] =np.where((NO2_Data['NO2 (ppb)']>1000) & (NO2_Data['NO2_qc_flags'] == 1),0, NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] =np.where((NO2_Data['NO2 (ppb)']>300) & (NO2_Data['NO2_qc_flags'] == 1),2, NO2_Data['NO2_qc_flags'])

NO2_Data['NO2_qc_flags_-6_offset'] = NO2_Data['NO2_qc_flags'].shift(periods=-6) 
NO2_Data['NO2_qc_flags_-5_offset'] = NO2_Data['NO2_qc_flags'].shift(periods=-5)
NO2_Data['NO2_qc_flags_-4_offset'] = NO2_Data['NO2_qc_flags'].shift(periods=-4)
NO2_Data['NO2_qc_flags_-3_offset'] = NO2_Data['NO2_qc_flags'].shift(periods=-3)
NO2_Data['NO2_qc_flags_-2_offset'] = NO2_Data['NO2_qc_flags'].shift(periods=-2)
NO2_Data['NO2_qc_flags_-1_offset'] = NO2_Data['NO2_qc_flags'].shift(periods=-1) 
NO2_Data['NO2_qc_flags_+1_offset'] = NO2_Data['NO2_qc_flags'].shift(periods=1)
NO2_Data['NO2_qc_flags_+2_offset'] = NO2_Data['NO2_qc_flags'].shift(periods=2)
NO2_Data['NO2_qc_flags_+3_offset'] = NO2_Data['NO2_qc_flags'].shift(periods=3)
NO2_Data['NO2_qc_flags_+4_offset'] = NO2_Data['NO2_qc_flags'].shift(periods=4)
NO2_Data['NO2_qc_flags_+5_offset'] = NO2_Data['NO2_qc_flags'].shift(periods=5)
NO2_Data['NO2_qc_flags_+6_offset'] = NO2_Data['NO2_qc_flags'].shift(periods=6)
NO2_Data['NO2_qc_flags_-6_offset'] = np.where(NO2_Data['NO2_qc_flags'] == 0, NO2_Data['NO2_qc_flags'], NO2_Data['NO2_qc_flags_-6_offset'])
NO2_Data['NO2_qc_flags_-5_offset'] = np.where(NO2_Data['NO2_qc_flags'] == 0, NO2_Data['NO2_qc_flags'], NO2_Data['NO2_qc_flags_-5_offset'])
NO2_Data['NO2_qc_flags_-4_offset'] = np.where(NO2_Data['NO2_qc_flags'] == 0, NO2_Data['NO2_qc_flags'], NO2_Data['NO2_qc_flags_-4_offset'])
NO2_Data['NO2_qc_flags_-3_offset'] = np.where(NO2_Data['NO2_qc_flags'] == 0, NO2_Data['NO2_qc_flags'], NO2_Data['NO2_qc_flags_-3_offset'])
NO2_Data['NO2_qc_flags_-2_offset'] = np.where(NO2_Data['NO2_qc_flags'] == 0, NO2_Data['NO2_qc_flags'], NO2_Data['NO2_qc_flags_-2_offset'])
NO2_Data['NO2_qc_flags_-1_offset'] = np.where(NO2_Data['NO2_qc_flags'] == 0, NO2_Data['NO2_qc_flags'], NO2_Data['NO2_qc_flags_-1_offset'])
NO2_Data['NO2_qc_flags_+1_offset'] = np.where(NO2_Data['NO2_qc_flags'] == 0, NO2_Data['NO2_qc_flags'], NO2_Data['NO2_qc_flags_+1_offset'])
NO2_Data['NO2_qc_flags_+2_offset'] = np.where(NO2_Data['NO2_qc_flags'] == 0, NO2_Data['NO2_qc_flags'], NO2_Data['NO2_qc_flags_+2_offset'])
NO2_Data['NO2_qc_flags_+3_offset'] = np.where(NO2_Data['NO2_qc_flags'] == 0, NO2_Data['NO2_qc_flags'], NO2_Data['NO2_qc_flags_+3_offset'])
NO2_Data['NO2_qc_flags_+4_offset'] = np.where(NO2_Data['NO2_qc_flags'] == 0, NO2_Data['NO2_qc_flags'], NO2_Data['NO2_qc_flags_+4_offset'])
NO2_Data['NO2_qc_flags_+5_offset'] = np.where(NO2_Data['NO2_qc_flags'] == 0, NO2_Data['NO2_qc_flags'], NO2_Data['NO2_qc_flags_+5_offset'])
NO2_Data['NO2_qc_flags_+6_offset'] = np.where(NO2_Data['NO2_qc_flags'] == 0, NO2_Data['NO2_qc_flags'], NO2_Data['NO2_qc_flags_+6_offset'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_-6_offset']!=1) & (NO2_Data['NO2_qc_flags_-6_offset'].notnull() ),NO2_Data['NO2_qc_flags_-6_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_-5_offset']!=1) & (NO2_Data['NO2_qc_flags_-5_offset'].notnull() ),NO2_Data['NO2_qc_flags_-5_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_-4_offset']!=1) & (NO2_Data['NO2_qc_flags_-4_offset'].notnull() ),NO2_Data['NO2_qc_flags_-4_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_-3_offset']!=1) & (NO2_Data['NO2_qc_flags_-3_offset'].notnull() ),NO2_Data['NO2_qc_flags_-3_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_-2_offset']!=1) & (NO2_Data['NO2_qc_flags_-2_offset'].notnull() ),NO2_Data['NO2_qc_flags_-2_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_-1_offset']!=1) & (NO2_Data['NO2_qc_flags_-1_offset'].notnull() ),NO2_Data['NO2_qc_flags_-1_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_+1_offset']!=1) & (NO2_Data['NO2_qc_flags_+1_offset'].notnull() ),NO2_Data['NO2_qc_flags_+1_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_+2_offset']!=1) & (NO2_Data['NO2_qc_flags_+2_offset'].notnull() ),NO2_Data['NO2_qc_flags_+2_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_+3_offset']!=1) & (NO2_Data['NO2_qc_flags_+3_offset'].notnull() ),NO2_Data['NO2_qc_flags_+3_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_+4_offset']!=1) & (NO2_Data['NO2_qc_flags_+4_offset'].notnull() ),NO2_Data['NO2_qc_flags_+4_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_+5_offset']!=1) & (NO2_Data['NO2_qc_flags_+5_offset'].notnull() ),NO2_Data['NO2_qc_flags_+5_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_+6_offset']!=1) & (NO2_Data['NO2_qc_flags_+6_offset'].notnull() ),NO2_Data['NO2_qc_flags_+6_offset'],NO2_Data['NO2_qc_flags'])

NO2_Flag_Offset = list(NO2_Data.columns.values)
NO2_Flag_Offset.remove('NO2 (ppb)')
NO2_Flag_Offset.remove('NO2_qc_flags')
NO2_Data = NO2_Data.drop(columns=NO2_Flag_Offset) #dropping newly made columns flagged data

start_NO2_false_cal1 = datetime.datetime(2021,3,24,0,0,00)
end_NO2_false_cal1 = datetime.datetime(2021,3,24,0,50,00)
NO2_Data.loc[start_NO2_false_cal1:end_NO2_false_cal1, ('NO2_qc_flags')] = 0

NO2_Data.drop(NO2_Data[(NO2_Data['NO2 (ppb)'] >1000)].index,inplace =True)
NO2_Data.drop(NO2_Data[(NO2_Data['NO2_qc_flags'] == 0)].index,inplace =True)
NO2_Data['NO2_qc_flags'] = NO2_Data['NO2_qc_flags'].astype(float)
NO2_Data['NO2_qc_flags'] = NO2_Data['NO2_qc_flags'].astype(int)
NO2_Data['NO2_qc_flags'] = NO2_Data['NO2_qc_flags'].astype(str)

NO2_Data=NO2_Data[['NO2 (ppb)', 'NO2_qc_flags']]

NO2_Data.drop(NO2_Data[(NO2_Data['NO2 (ppb)'].isnull())].index,inplace =True)
NO2_Data.drop(NO2_Data[(NO2_Data['NO2 (ppb)'] == 0)].index,inplace =True)

plt.plot(NOy_Data['Diff (ppb)'], label='NOy Diff')
plt.plot(NO2_Data['NO2 (ppb)'], label='NO2')
#plt.plot(NO2_Data['NO2_qc_flags'], label='NO2 Flags')
plt.legend()
plt.ylabel('ppb')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

NO2_Data.to_csv(str(gas_Folder) + 'Teledyne-T500U_maqs_' +  str(date_file_label) + '_NO2-concentration' + str(status) + str(version_number) + '.csv')

NO2_Data['TimeDateSince'] = NO2_Data.index-datetime.datetime(1970,1,1,0,0,00)
NO2_Data['TimeSecondsSince'] = NO2_Data['TimeDateSince'].dt.total_seconds()
NO2_Data['day_year'] = pd.DatetimeIndex(NO2_Data['TimeDateSince'].index).dayofyear
NO2_Data['year'] = pd.DatetimeIndex(NO2_Data['TimeDateSince'].index).year
NO2_Data['month'] = pd.DatetimeIndex(NO2_Data['TimeDateSince'].index).month
NO2_Data['day'] = pd.DatetimeIndex(NO2_Data['TimeDateSince'].index).day
NO2_Data['hour'] = pd.DatetimeIndex(NO2_Data['TimeDateSince'].index).hour
NO2_Data['minute'] = pd.DatetimeIndex(NO2_Data['TimeDateSince'].index).minute
NO2_Data['second'] = pd.DatetimeIndex(NO2_Data['TimeDateSince'].index).second

ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime', 'All_Data_Flag']]
ozone_Data.drop(ozone_Data[(ozone_Data['Ozone (ppb)'] == 'FFFFFFFF')].index,inplace =True)
ozone_Data.drop(ozone_Data[(ozone_Data['Ozone (ppb)'].isnull())].index,inplace =True)
ozone_Data['Ozone (ppb)'] = ozone_Data['Ozone (ppb)'].astype(float)
ozone_Data.drop(ozone_Data[(ozone_Data['Ozone (ppb)'] == 0)].index,inplace =True)
ozone_Data.drop(ozone_Data[(ozone_Data['Ozone (ppb)'].isnull())].index,inplace =True)
ozone_Data['O3 Flags'] = ozone_Data['O3 Flags'].str.lstrip().astype(str)
ozone_Data['O3 Flags'] = ozone_Data['O3 Flags'].str.rstrip().astype(str)
ozone_Data['O3 Flags'] = np.where(ozone_Data['O3 Flags'].isnull() , '0C100000', ozone_Data['O3 Flags'])
ozone_Data['O3_Prelim_Flag'] = np.where(ozone_Data['O3 Flags'].str.contains('0C10000', case=False, na=False), 0, ozone_Data['O3 Flags'])
ozone_Data['O3_Prelim_Flag'] = np.where(ozone_Data['O3 Flags'].str.contains('2C1', case=False, na=False), 0, ozone_Data['O3 Flags'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C100000'), 1, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['All_Data_Flag']== 0), 0, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['All_Data_Flag']== 2), 2, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0CD00000'), 0, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0CD00500'), 0, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C101000'), 2, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='FFFFFFFF'), 2, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C310000'), 0, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0CF10000'), 0, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0CF00000'), 0, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C500000'), 0, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C310500'), 0, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C700000'), 0, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0CF01000'), 2, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0CF10000'), 2, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='8C100000'), 1, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C100400'), 2, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C100500'), 2, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C105000'), 2, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C104000'), 2, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C100100'), 2, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C100002'), 2, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0C310002'), 0, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where((ozone_Data['O3 Flags']=='0CD00002'), 0, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = np.where(((ozone_Data['O3 Flags']=='nan') & (ozone_Data['Ozone (ppb)'].notnull() ) ), 1, ozone_Data['O3_Prelim_Flag'])
ozone_Data['O3_Prelim_Flag'] = ozone_Data['O3_Prelim_Flag'].astype(float)
ozone_Data['O3_Prelim_Flag'] = ozone_Data['O3_Prelim_Flag'].astype(int)

ozone_Data.rename(columns={'O3_Prelim_Flag': 'O3_qc_flags'}, inplace = True)

start_O3_gas_span1 = datetime.datetime(2019,8,22,12,45,00) # O3 gas span without cal on turned on
end_O3_gas_span1 = datetime.datetime(2019,8,22,13,5,00)
ozone_Data.loc[start_O3_gas_span1:end_O3_gas_span1, ('O3_qc_flags')] = 0

start_O3_gas_span2 = datetime.datetime(2019,9,17,12,15,00) 
end_O3_gas_span2 = datetime.datetime(2019,9,17,12,52,00)
ozone_Data.loc[start_O3_gas_span2:end_O3_gas_span2, ('O3_qc_flags')] = 0

start_O3_gas_span3 = datetime.datetime(2019,9,26,8,38,00) 
end_O3_gas_span3 = datetime.datetime(2019,9,26,8,48,00)
ozone_Data.loc[start_O3_gas_span3:end_O3_gas_span3, ('O3_qc_flags')] = 0

start_O3_gas_span4 = datetime.datetime(2019,9,6,13,45,00) 
end_O3_gas_span4 = datetime.datetime(2019,9,6,14,42,00)
ozone_Data.loc[start_O3_gas_span4:end_O3_gas_span4, ('O3_qc_flags')] = 0

start_O3_gas_span5 = datetime.datetime(2019,9,10,13,45,00) 
end_O3_gas_span5 = datetime.datetime(2019,9,10,14,30,00)
ozone_Data.loc[start_O3_gas_span5:end_O3_gas_span5, ('O3_qc_flags')] = 0

start_O3_gas_span6 = datetime.datetime(2019,9,17,11,0,00) 
end_O3_gas_span6 = datetime.datetime(2019,9,17,12,0,00)
ozone_Data.loc[start_O3_gas_span6:end_O3_gas_span6, ('O3_qc_flags')] = 0

start_O3_gas_span7 = datetime.datetime(2019,9,26,8,30,00) 
end_O3_gas_span7 = datetime.datetime(2019,9,26,8,50,00)
ozone_Data.loc[start_O3_gas_span6:end_O3_gas_span6, ('O3_qc_flags')] = 0

start_O3_flow_1 = datetime.datetime(2020,3,3,18,52,00) # O3 gas span without cal on turned on
end_O3_flow_1 = datetime.datetime(2020,3,3,18,58,00)
ozone_Data.loc[start_O3_flow_1:end_O3_flow_1, ('O3_qc_flags')] = 0

start_O3_flow_2 = datetime.datetime(2020,10,13,19,5,00)
end_O3_flow_2 = datetime.datetime(2020,10,13,19,10,00)
ozone_Data.loc[start_O3_flow_2:end_O3_flow_2, ('O3_qc_flags')] = 0

start_O3_flow_3 = datetime.datetime(2019,1,15,13,45,00)
end_O3_flow_3 = datetime.datetime(2019,1,15,15,30,00)
ozone_Data.loc[start_O3_flow_3:end_O3_flow_3, ('O3_qc_flags')] = 0

start_O3_flow_4 = datetime.datetime(2019,11,9,13,55,00)
end_O3_flow_4 = datetime.datetime(2019,11,9,14,2,00)
ozone_Data.loc[start_O3_flow_4:end_O3_flow_4, ('O3_qc_flags')] = 0

start_O3_flow_4 = datetime.datetime(2019,11,19,8,14,00)
end_O3_flow_4 = datetime.datetime(2019,11,19,8,20,00)
ozone_Data.loc[start_O3_flow_4:end_O3_flow_4, ('O3_qc_flags')] = 0

start_O3_flow_5 = datetime.datetime(2020,9,4,0,15,00)
end_O3_flow_5 = datetime.datetime(2020,9,4,0,25,00)
ozone_Data.loc[start_O3_flow_5:end_O3_flow_5, ('O3_qc_flags')] = 0

start_O3_flow_6 = datetime.datetime(2020,12,1,3,20,00)
end_O3_flow_6 = datetime.datetime(2020,12,1,3,30,00)
ozone_Data.loc[start_O3_flow_6:end_O3_flow_6, ('O3_qc_flags')] = 0
    
start_O3_Cabin_Air = datetime.datetime(2022,6,5,2,30,00) 
end_O3_Cabin_Air = datetime.datetime(2022,6,6,15,30,00)
ozone_Data.loc[start_O3_Cabin_Air:end_O3_Cabin_Air, ('O3_qc_flags')] = 0
    
start_O3_False = datetime.datetime(2022,8,30,7,4,00) 
end_O3_False = datetime.datetime(2022,8,30,7,8,00)
ozone_Data.loc[start_O3_False:end_O3_False, ('O3_qc_flags')] = 0

start_O3_pump = datetime.datetime(2022,9,24,22,0,00)
end_O3_pump = datetime.datetime(2022,9,26,18,30,00)
ozone_Data.loc[start_O3_pump:end_O3_pump, ('O3_qc_flags')] = 0
ozone_Data.drop(ozone_Data.loc[start_O3_pump:end_O3_pump].index, inplace=True)

start_O3_dip = datetime.datetime(2022,11,24,23,31,00)
end_O3_dip = datetime.datetime(2022,11,24,23,34,00)
ozone_Data.loc[start_O3_dip:end_O3_dip, ('O3_qc_flags')] = 0
ozone_Data.drop(ozone_Data.loc[start_O3_dip:end_O3_dip].index, inplace=True)

ozone_Data.rename(columns={'O3_qc_flags': 'O3_Prelim_Flag'}, inplace = True)

ozone_Data['O3 a'] = np.interp(ozone_Data['datetime'], Other_Gas_Cals['datetime'], Other_Gas_Cals['O3 Zero (ppb)'])
ozone_Data['O3 b'] = np.interp(ozone_Data['datetime'], Other_Gas_Cals['datetime'], Other_Gas_Cals['O3 Response'])
ozone_Data['Ozone (ppb) perlim'] = (ozone_Data['Ozone (ppb)']- ozone_Data['O3 a'])*ozone_Data['O3 b'] # or ozone_Data['Ozone (ppb)']*ozone_Data['O3 b'] - ozone_Data['O3 a']

O3_Data_Drop = list(ozone_Data.columns.values)
O3_Data_Drop.remove('Ozone (ppb) perlim')
O3_Data_Drop.remove('O3_Prelim_Flag')
ozone_Data = ozone_Data.drop(columns=O3_Data_Drop)

ozone_Data['O3_Prelim_Flag'] = np.where(ozone_Data['O3_Prelim_Flag'] == 0, 6, ozone_Data['O3_Prelim_Flag'])
max_O3_flag = ozone_Data['O3_Prelim_Flag'].groupby(pd.Grouper(freq=av_Freq)).max() #this transfers over error from original cal checks into averaged data
ozone_Data = ozone_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
ozone_Data['O3_Prelim_Flag'] = pd.Series(max_O3_flag)
ozone_Data['O3_Prelim_Flag'] = np.where(ozone_Data['O3_Prelim_Flag'] == 6, 0, ozone_Data['O3_Prelim_Flag'])
ozone_Data.rename(columns={'Ozone (ppb) perlim': 'Ozone (ppb)', 'O3_Prelim_Flag': 'O3_qc_flags'}, inplace = True)

ozone_Data['O3_qc_flags'] = ozone_Data['O3_qc_flags'].astype(str)
ozone_Data['O3_qc_flags'] = np.where(ozone_Data['O3_qc_flags'] == 'nan', 2, ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = ozone_Data['O3_qc_flags'].astype(float)
ozone_Data['O3_qc_flags'] = np.where(ozone_Data['O3_qc_flags'] == 2, int(2), ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where(ozone_Data['O3_qc_flags'] == 1, int(1), ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = ozone_Data['O3_qc_flags'].astype(int)

ozone_Data['O3_qc_flags']=np.where((ozone_Data['Ozone (ppb)']<0) & (ozone_Data['O3_qc_flags'] == 1),2, ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags']=np.where((ozone_Data['Ozone (ppb)']>150) & (ozone_Data['O3_qc_flags'] == 1),2, ozone_Data['O3_qc_flags'])

ozone_Data['O3_qc_flags_-6_offset'] = ozone_Data['O3_qc_flags'].shift(periods=-6) #setting up columns to bloc off the area around flagged data
ozone_Data['O3_qc_flags_-5_offset'] = ozone_Data['O3_qc_flags'].shift(periods=-5)
ozone_Data['O3_qc_flags_-4_offset'] = ozone_Data['O3_qc_flags'].shift(periods=-4)
ozone_Data['O3_qc_flags_-3_offset'] = ozone_Data['O3_qc_flags'].shift(periods=-3)
ozone_Data['O3_qc_flags_-2_offset'] = ozone_Data['O3_qc_flags'].shift(periods=-2)
ozone_Data['O3_qc_flags_-1_offset'] = ozone_Data['O3_qc_flags'].shift(periods=-1) 
ozone_Data['O3_qc_flags_+1_offset'] = ozone_Data['O3_qc_flags'].shift(periods=1)
ozone_Data['O3_qc_flags_+2_offset'] = ozone_Data['O3_qc_flags'].shift(periods=2)
ozone_Data['O3_qc_flags_+3_offset'] = ozone_Data['O3_qc_flags'].shift(periods=3)
ozone_Data['O3_qc_flags_+4_offset'] = ozone_Data['O3_qc_flags'].shift(periods=4)
ozone_Data['O3_qc_flags_+5_offset'] = ozone_Data['O3_qc_flags'].shift(periods=5)
ozone_Data['O3_qc_flags_+6_offset'] = ozone_Data['O3_qc_flags'].shift(periods=6)
ozone_Data['O3_qc_flags_-6_offset'] = np.where(ozone_Data['O3_qc_flags'] == 0, ozone_Data['O3_qc_flags'], ozone_Data['O3_qc_flags_-6_offset'])
ozone_Data['O3_qc_flags_-5_offset'] = np.where(ozone_Data['O3_qc_flags'] == 0, ozone_Data['O3_qc_flags'], ozone_Data['O3_qc_flags_-5_offset'])
ozone_Data['O3_qc_flags_-4_offset'] = np.where(ozone_Data['O3_qc_flags'] == 0, ozone_Data['O3_qc_flags'], ozone_Data['O3_qc_flags_-4_offset'])
ozone_Data['O3_qc_flags_-3_offset'] = np.where(ozone_Data['O3_qc_flags'] == 0, ozone_Data['O3_qc_flags'], ozone_Data['O3_qc_flags_-3_offset'])
ozone_Data['O3_qc_flags_-2_offset'] = np.where(ozone_Data['O3_qc_flags'] == 0, ozone_Data['O3_qc_flags'], ozone_Data['O3_qc_flags_-2_offset'])
ozone_Data['O3_qc_flags_-1_offset'] = np.where(ozone_Data['O3_qc_flags'] == 0, ozone_Data['O3_qc_flags'], ozone_Data['O3_qc_flags_-1_offset'])
ozone_Data['O3_qc_flags_+1_offset'] = np.where(ozone_Data['O3_qc_flags'] == 0, ozone_Data['O3_qc_flags'], ozone_Data['O3_qc_flags_+1_offset'])
ozone_Data['O3_qc_flags_+2_offset'] = np.where(ozone_Data['O3_qc_flags'] == 0, ozone_Data['O3_qc_flags'], ozone_Data['O3_qc_flags_+2_offset'])
ozone_Data['O3_qc_flags_+3_offset'] = np.where(ozone_Data['O3_qc_flags'] == 0, ozone_Data['O3_qc_flags'], ozone_Data['O3_qc_flags_+3_offset'])
ozone_Data['O3_qc_flags_+4_offset'] = np.where(ozone_Data['O3_qc_flags'] == 0, ozone_Data['O3_qc_flags'], ozone_Data['O3_qc_flags_+4_offset'])
ozone_Data['O3_qc_flags_+5_offset'] = np.where(ozone_Data['O3_qc_flags'] == 0, ozone_Data['O3_qc_flags'], ozone_Data['O3_qc_flags_+5_offset'])
ozone_Data['O3_qc_flags_+6_offset'] = np.where(ozone_Data['O3_qc_flags'] == 0, ozone_Data['O3_qc_flags'], ozone_Data['O3_qc_flags_+6_offset'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_-6_offset']!=1) & (ozone_Data['O3_qc_flags_-6_offset'].notnull() ),ozone_Data['O3_qc_flags_-6_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_-5_offset']!=1) & (ozone_Data['O3_qc_flags_-5_offset'].notnull() ),ozone_Data['O3_qc_flags_-5_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_-4_offset']!=1) & (ozone_Data['O3_qc_flags_-4_offset'].notnull() ),ozone_Data['O3_qc_flags_-4_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_-3_offset']!=1) & (ozone_Data['O3_qc_flags_-3_offset'].notnull() ),ozone_Data['O3_qc_flags_-3_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_-2_offset']!=1) & (ozone_Data['O3_qc_flags_-2_offset'].notnull() ),ozone_Data['O3_qc_flags_-2_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_-1_offset']!=1) & (ozone_Data['O3_qc_flags_-1_offset'].notnull() ),ozone_Data['O3_qc_flags_-1_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_+1_offset']!=1) & (ozone_Data['O3_qc_flags_+1_offset'].notnull() ),ozone_Data['O3_qc_flags_+1_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_+2_offset']!=1) & (ozone_Data['O3_qc_flags_+2_offset'].notnull() ),ozone_Data['O3_qc_flags_+2_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_+3_offset']!=1) & (ozone_Data['O3_qc_flags_+3_offset'].notnull() ),ozone_Data['O3_qc_flags_+3_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_+4_offset']!=1) & (ozone_Data['O3_qc_flags_+4_offset'].notnull() ),ozone_Data['O3_qc_flags_+4_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_+5_offset']!=1) & (ozone_Data['O3_qc_flags_+5_offset'].notnull() ),ozone_Data['O3_qc_flags_+5_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_+6_offset']!=1) & (ozone_Data['O3_qc_flags_+6_offset'].notnull() ),ozone_Data['O3_qc_flags_+6_offset'],ozone_Data['O3_qc_flags'])
O3_Flag_Offset = list(ozone_Data.columns.values)
O3_Flag_Offset.remove('Ozone (ppb)')
O3_Flag_Offset.remove('O3_qc_flags')
ozone_Data = ozone_Data.drop(columns=O3_Flag_Offset) #dropping newly made columns flagged data

ozone_Data.drop(ozone_Data[(ozone_Data['O3_qc_flags'] == 0)].index,inplace =True)
ozone_Data['O3_qc_flags'] = ozone_Data['O3_qc_flags'].astype(float)
ozone_Data['O3_qc_flags'] = ozone_Data['O3_qc_flags'].astype(int)
ozone_Data['O3_qc_flags'] = ozone_Data['O3_qc_flags'].astype(str)

ozone_Data=ozone_Data[['Ozone (ppb)', 'O3_qc_flags']]

ozone_Data.drop(ozone_Data[(ozone_Data['Ozone (ppb)'].isnull())].index,inplace =True)
ozone_Data.drop(ozone_Data[(ozone_Data['Ozone (ppb)'] == 0)].index,inplace =True)

plt.plot(ozone_Data["Ozone (ppb)"], label='O3')
#plt.plot(ozone_Data['O3_qc_flags'], label='O3 flags')
plt.legend()
plt.ylabel('ppb')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

ozone_Data.to_csv(str(gas_Folder) + 'Thermo-49i_maqs_' +  str(date_file_label) + '_O3-concentration' + str(status) + str(version_number) + '.csv')

ozone_Data['TimeDateSince'] = ozone_Data.index-datetime.datetime(1970,1,1,0,0,00)
ozone_Data['TimeSecondsSince'] = ozone_Data['TimeDateSince'].dt.total_seconds()
ozone_Data['day_year'] = pd.DatetimeIndex(ozone_Data['TimeDateSince'].index).dayofyear
ozone_Data['year'] = pd.DatetimeIndex(ozone_Data['TimeDateSince'].index).year
ozone_Data['month'] = pd.DatetimeIndex(ozone_Data['TimeDateSince'].index).month
ozone_Data['day'] = pd.DatetimeIndex(ozone_Data['TimeDateSince'].index).day
ozone_Data['hour'] = pd.DatetimeIndex(ozone_Data['TimeDateSince'].index).hour
ozone_Data['minute'] = pd.DatetimeIndex(ozone_Data['TimeDateSince'].index).minute
ozone_Data['second'] = pd.DatetimeIndex(ozone_Data['TimeDateSince'].index).second



if start_year_month_str < '202003':
    print('no CO Data here')
elif start_year_month_str == '202207':
    print('CO analyser not functioning')
else:
    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime', 'All_Data_Flag']]
    CO_Data.drop(CO_Data[(CO_Data['CO (ppb)'] == 'FFFFFFFF')].index,inplace =True)
    CO_Data.drop(CO_Data[(CO_Data['CO (ppb)'].isnull())].index,inplace =True)
    CO_Data['CO (ppb)'] = CO_Data['CO (ppb)'].astype(float)
    CO_Data.drop(CO_Data[(CO_Data['CO (ppb)'] == 0)].index,inplace =True)
    CO_Data.drop(CO_Data[(CO_Data['CO (ppb)'].isnull())].index,inplace =True)
    CO_Data['CO_Prelim_Flag'] = np.where(CO_Data['CO Flags'].str.contains('8C041', case=False, na=False), 2, CO_Data['CO Flags'])
    CO_Data['CO_Prelim_Flag'] = np.where(CO_Data['CO Flags'].str.contains('8C06', case=False, na=False), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where(CO_Data['CO Flags'].str.contains('8C045', case=False, na=False), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where(CO_Data['CO Flags'].str.contains('8C049', case=False, na=False), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where(CO_Data['CO Flags'].str.contains('AC0', case=False, na=False), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C040000'), 1, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['All_Data_Flag']== 2), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['All_Data_Flag']== 0), 0, CO_Data['CO_Prelim_Flag']) #0
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='FFFFFFFF'), 2, CO_Data['CO_Prelim_Flag']) #0
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags'].isnull() ), 0, CO_Data['CO_Prelim_Flag']) #0
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C040001'), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C040005'), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C040400'), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C041415'), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C040401'), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C044000'), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C050000'), 2, CO_Data['CO_Prelim_Flag']) #0
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C050400'), 2, CO_Data['CO_Prelim_Flag']) #0
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C070000'), 2, CO_Data['CO_Prelim_Flag']) #0
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C070001'), 2, CO_Data['CO_Prelim_Flag']) #0
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C074000'), 2, CO_Data['CO_Prelim_Flag']) #0
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='AC040000'), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = np.where((CO_Data['CO Flags']=='8C041000'), 2, CO_Data['CO_Prelim_Flag'])
    CO_Data['CO_Prelim_Flag'] = CO_Data['CO_Prelim_Flag'].astype(float)
    CO_Data['CO_Prelim_Flag'] = CO_Data['CO_Prelim_Flag'].astype(int)
       
    CO_Data.drop(CO_Data[(CO_Data['CO Flags'] =='0C100000')].index,inplace =True)

    CO_Data['CO a'] = np.interp(CO_Data['datetime'], CO_AutoZero['datetime'], CO_AutoZero['CO Zero (ppb)'])
    CO_Data['CO b'] = np.interp(CO_Data['datetime'], CO_Calib['datetime'], CO_Calib['CO Response'])
    CO_Data['CO (ppb) perlim'] = (CO_Data['CO (ppb)'] - CO_Data['CO a'])*CO_Data['CO b'] # 0.97 or CO_Data['CO (ppb)']*CO_Data['CO b'] - CO_Data['CO a']
    
    start_Flow_CO_1 = datetime.datetime(2022,1,1,0,0,00) #unknown uncertainty
    end_Flow_CO_1 = datetime.datetime(2022,1,5,0,0,00)
    flow_CO_data = CO_Data[start_Flow_CO_1:end_Flow_CO_1]
    flow_CO_data['CO_Prelim_Flag'] = np.where(flow_CO_data['CO (ppb) perlim'] <100 , 0, flow_CO_data['CO_Prelim_Flag']) 
    flow_CO_flag = flow_CO_data['CO_Prelim_Flag']
    CO_Data.loc[start_Flow_CO_1:end_Flow_CO_1, ('CO_Prelim_Flag')] = pd.Series(flow_CO_flag)
    
    start_Flow_CO_2 = datetime.datetime(2020,3,26,0,0,00) #unknown uncertainty
    end_Flow_CO_2 = datetime.datetime(2020,5,15,0,0,00)
    flow_CO_data = CO_Data[start_Flow_CO_2:end_Flow_CO_2]
    flow_CO_data['CO_Prelim_Flag'] = np.where(flow_CO_data['CO (ppb) perlim'] >500 , 0, flow_CO_data['CO_Prelim_Flag']) 
    flow_CO_flag = flow_CO_data['CO_Prelim_Flag']
    CO_Data.loc[start_Flow_CO_2:end_Flow_CO_2, ('CO_Prelim_Flag')] = pd.Series(flow_CO_flag)
    
    start_Flow_CO_3 = datetime.datetime(2020,3,17,0,0,00) #unknown uncertainty
    end_Flow_CO_3 = datetime.datetime(2020,3,18,8,0,00)
    flow_CO_data = CO_Data[start_Flow_CO_3:end_Flow_CO_3]
    flow_CO_data['CO_Prelim_Flag'] = np.where(flow_CO_data['CO_Prelim_Flag'] == 1, 2, flow_CO_data['CO_Prelim_Flag']) 
    flow_CO_flag = flow_CO_data['CO_Prelim_Flag']
    CO_Data.loc[start_Flow_CO_3:end_Flow_CO_3, ('CO_Prelim_Flag')] = pd.Series(flow_CO_flag)
    
    start_Flow_CO_4 = datetime.datetime(2021,4,8,1,36,00) #unknown uncertainty
    end_Flow_CO_4 = datetime.datetime(2021,4,8,1,41,00)
    CO_Data.loc[start_Flow_CO_4:end_Flow_CO_4, ('CO_Prelim_Flag')] = 0
    
    start_Flow_CO_5 = datetime.datetime(2021,9,24,0,0,00) #unknown uncertainty
    end_Flow_CO_5 = datetime.datetime(2021,9,30,23,59,00)
    flow_CO_data = CO_Data[start_Flow_CO_5:end_Flow_CO_5]
    flow_CO_data['CO_Prelim_Flag'] = np.where(flow_CO_data['CO (ppb) perlim'] >600 , 0, flow_CO_data['CO_Prelim_Flag']) 
    flow_CO_flag = flow_CO_data['CO_Prelim_Flag']
    CO_Data.loc[start_Flow_CO_5:end_Flow_CO_5, ('CO_Prelim_Flag')] = pd.Series(flow_CO_flag)
    
    start_Flow_CO_6 = datetime.datetime(2022,4,18,2,49,00) #unknown uncertainty
    end_Flow_CO_6 = datetime.datetime(2022,4,18,2,54,00)
    flow_CO_data = CO_Data[start_Flow_CO_6:end_Flow_CO_6]
    flow_CO_data['CO_Prelim_Flag'] = np.where(flow_CO_data['CO (ppb) perlim'] >600 , 0, flow_CO_data['CO_Prelim_Flag']) 
    flow_CO_flag = flow_CO_data['CO_Prelim_Flag']
    CO_Data.loc[start_Flow_CO_6:end_Flow_CO_6, ('CO_Prelim_Flag')] = pd.Series(flow_CO_flag)



    CO_Data_Drop = list(CO_Data.columns.values)
    CO_Data_Drop.remove('CO (ppb) perlim')
    CO_Data_Drop.remove('CO_Prelim_Flag')
    CO_Data = CO_Data.drop(columns=CO_Data_Drop)

    CO_Data['CO_Prelim_Flag'] = np.where(CO_Data['CO_Prelim_Flag'] == 0, 6, CO_Data['CO_Prelim_Flag'])
    max_CO_flag = CO_Data['CO_Prelim_Flag'].groupby(pd.Grouper(freq=av_Freq)).max() #this transfers over error from original cal checks into averaged data
    CO_Data = CO_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
    CO_Data['CO_Prelim_Flag'] = pd.Series(max_CO_flag)
    CO_Data['CO_Prelim_Flag'] = np.where(CO_Data['CO_Prelim_Flag'] == 6, 0, CO_Data['CO_Prelim_Flag'])
    CO_Data.rename(columns={'CO (ppb) perlim': 'CO (ppb)', 'CO_Prelim_Flag': 'CO_qc_flags'}, inplace = True)

    CO_Data['CO_qc_flags'] = CO_Data['CO_qc_flags'].astype(str)
    CO_Data['CO_qc_flags'] = np.where(CO_Data['CO_qc_flags'] == 'nan', 2, CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = CO_Data['CO_qc_flags'].astype(float)
    CO_Data['CO_qc_flags'] = np.where(CO_Data['CO_qc_flags'] == 2, int(2), CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where(CO_Data['CO_qc_flags'] == 1, int(1), CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = CO_Data['CO_qc_flags'].astype(int)

    CO_Data['CO_qc_flags']=np.where((CO_Data['CO (ppb)']<5) & (CO_Data['CO_qc_flags']== 1), 2, CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags']=np.where((CO_Data['CO (ppb)']>2000) & (CO_Data['CO_qc_flags']== 1),2, CO_Data['CO_qc_flags'])

    CO_Data['CO_qc_flags_-7_offset'] = CO_Data['CO_qc_flags'].shift(periods=-7)
    CO_Data['CO_qc_flags_-6_offset'] = CO_Data['CO_qc_flags'].shift(periods=-6) #setting up columns to bloc off the area around flagged data
    CO_Data['CO_qc_flags_-5_offset'] = CO_Data['CO_qc_flags'].shift(periods=-5)
    CO_Data['CO_qc_flags_-4_offset'] = CO_Data['CO_qc_flags'].shift(periods=-4)
    CO_Data['CO_qc_flags_-3_offset'] = CO_Data['CO_qc_flags'].shift(periods=-3)
    CO_Data['CO_qc_flags_-2_offset'] = CO_Data['CO_qc_flags'].shift(periods=-2)
    CO_Data['CO_qc_flags_-1_offset'] = CO_Data['CO_qc_flags'].shift(periods=-1) 
    CO_Data['CO_qc_flags_+1_offset'] = CO_Data['CO_qc_flags'].shift(periods=1)
    CO_Data['CO_qc_flags_+2_offset'] = CO_Data['CO_qc_flags'].shift(periods=2)
    CO_Data['CO_qc_flags_+3_offset'] = CO_Data['CO_qc_flags'].shift(periods=3)
    CO_Data['CO_qc_flags_+4_offset'] = CO_Data['CO_qc_flags'].shift(periods=4)
    CO_Data['CO_qc_flags_+5_offset'] = CO_Data['CO_qc_flags'].shift(periods=5)
    CO_Data['CO_qc_flags_+6_offset'] = CO_Data['CO_qc_flags'].shift(periods=6)
    CO_Data['CO_qc_flags_+7_offset'] = CO_Data['CO_qc_flags'].shift(periods=7)
    CO_Data['CO_qc_flags_-6_offset'] = np.where(CO_Data['CO_qc_flags'] == 0, CO_Data['CO_qc_flags'], CO_Data['CO_qc_flags_-6_offset'])
    CO_Data['CO_qc_flags_-5_offset'] = np.where(CO_Data['CO_qc_flags'] == 0, CO_Data['CO_qc_flags'], CO_Data['CO_qc_flags_-5_offset'])
    CO_Data['CO_qc_flags_-4_offset'] = np.where(CO_Data['CO_qc_flags'] == 0, CO_Data['CO_qc_flags'], CO_Data['CO_qc_flags_-4_offset'])
    CO_Data['CO_qc_flags_-3_offset'] = np.where(CO_Data['CO_qc_flags'] == 0, CO_Data['CO_qc_flags'], CO_Data['CO_qc_flags_-3_offset'])
    CO_Data['CO_qc_flags_-2_offset'] = np.where(CO_Data['CO_qc_flags'] == 0, CO_Data['CO_qc_flags'], CO_Data['CO_qc_flags_-2_offset'])
    CO_Data['CO_qc_flags_-1_offset'] = np.where(CO_Data['CO_qc_flags'] == 0, CO_Data['CO_qc_flags'], CO_Data['CO_qc_flags_-1_offset'])
    CO_Data['CO_qc_flags_+1_offset'] = np.where(CO_Data['CO_qc_flags'] == 0, CO_Data['CO_qc_flags'], CO_Data['CO_qc_flags_+1_offset'])
    CO_Data['CO_qc_flags_+2_offset'] = np.where(CO_Data['CO_qc_flags'] == 0, CO_Data['CO_qc_flags'], CO_Data['CO_qc_flags_+2_offset'])
    CO_Data['CO_qc_flags_+3_offset'] = np.where(CO_Data['CO_qc_flags'] == 0, CO_Data['CO_qc_flags'], CO_Data['CO_qc_flags_+3_offset'])
    CO_Data['CO_qc_flags_+4_offset'] = np.where(CO_Data['CO_qc_flags'] == 0, CO_Data['CO_qc_flags'], CO_Data['CO_qc_flags_+4_offset'])
    CO_Data['CO_qc_flags_+5_offset'] = np.where(CO_Data['CO_qc_flags'] == 0, CO_Data['CO_qc_flags'], CO_Data['CO_qc_flags_+5_offset'])
    CO_Data['CO_qc_flags_+6_offset'] = np.where(CO_Data['CO_qc_flags'] == 0, CO_Data['CO_qc_flags'], CO_Data['CO_qc_flags_+6_offset'])    
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_-7_offset']!=1) & (CO_Data['CO_qc_flags_-7_offset'].notnull() ),CO_Data['CO_qc_flags_-7_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_-6_offset']!=1) & (CO_Data['CO_qc_flags_-6_offset'].notnull() ),CO_Data['CO_qc_flags_-6_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_-5_offset']!=1) & (CO_Data['CO_qc_flags_-5_offset'].notnull() ),CO_Data['CO_qc_flags_-5_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_-4_offset']!=1) & (CO_Data['CO_qc_flags_-4_offset'].notnull() ),CO_Data['CO_qc_flags_-4_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_-3_offset']!=1) & (CO_Data['CO_qc_flags_-3_offset'].notnull() ),CO_Data['CO_qc_flags_-3_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_-2_offset']!=1) & (CO_Data['CO_qc_flags_-2_offset'].notnull() ),CO_Data['CO_qc_flags_-2_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_-1_offset']!=1) & (CO_Data['CO_qc_flags_-1_offset'].notnull() ),CO_Data['CO_qc_flags_-1_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_+1_offset']!=1) & (CO_Data['CO_qc_flags_+1_offset'].notnull() ),CO_Data['CO_qc_flags_+1_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_+2_offset']!=1) & (CO_Data['CO_qc_flags_+2_offset'].notnull() ),CO_Data['CO_qc_flags_+2_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_+3_offset']!=1) & (CO_Data['CO_qc_flags_+3_offset'].notnull() ),CO_Data['CO_qc_flags_+3_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_+4_offset']!=1) & (CO_Data['CO_qc_flags_+4_offset'].notnull() ),CO_Data['CO_qc_flags_+4_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_+5_offset']!=1) & (CO_Data['CO_qc_flags_+5_offset'].notnull() ),CO_Data['CO_qc_flags_+5_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_+6_offset']!=1) & (CO_Data['CO_qc_flags_+6_offset'].notnull() ),CO_Data['CO_qc_flags_+6_offset'],CO_Data['CO_qc_flags'])
    CO_Data['CO_qc_flags'] = np.where((CO_Data['CO_qc_flags_+7_offset']!=1) & (CO_Data['CO_qc_flags_+7_offset'].notnull() ),CO_Data['CO_qc_flags_+7_offset'],CO_Data['CO_qc_flags'])
    CO_Flag_Offset = list(CO_Data.columns.values)
    CO_Flag_Offset.remove('CO (ppb)')
    CO_Flag_Offset.remove('CO_qc_flags')
    CO_Data = CO_Data.drop(columns=CO_Flag_Offset) #dropping newly made columns flagged data
    
    CO_Data.drop(CO_Data[(CO_Data['CO_qc_flags'] == 0)].index,inplace =True)
    CO_Data.drop(CO_Data[(CO_Data['CO_qc_flags'] == 2)].index,inplace =True)
    CO_Data['CO_qc_flags'] = CO_Data['CO_qc_flags'].astype(float)
    CO_Data['CO_qc_flags'] = CO_Data['CO_qc_flags'].astype(int)
    CO_Data['CO_qc_flags'] = CO_Data['CO_qc_flags'].astype(str)

    CO_Data=CO_Data[['CO (ppb)', 'CO_qc_flags']]

    CO_Data.drop(CO_Data[(CO_Data['CO (ppb)'].isnull())].index,inplace =True)
    CO_Data.drop(CO_Data[(CO_Data['CO (ppb)'] == 0)].index,inplace =True)

    plt.plot(CO_Data['CO (ppb)'], label='CO')
    #plt.plot(CO_Data['CO_qc_flags'], label='CO flags')
    plt.ylabel('abundance (ppb)')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 16}

    plt.legend()
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    plt.figure()
    plt.show()
    
    CO_Data.to_csv(str(gas_Folder) + 'Thermo-48i_maqs_' + str(date_file_label) + '_CO-concentration' + str(status) + str(version_number) + '.csv')
    
    CO_Data['TimeDateSince'] = CO_Data.index-datetime.datetime(1970,1,1,0,0,00)
    CO_Data['TimeSecondsSince'] = CO_Data['TimeDateSince'].dt.total_seconds()
    CO_Data['day_year'] = pd.DatetimeIndex(CO_Data['TimeDateSince'].index).dayofyear
    CO_Data['year'] = pd.DatetimeIndex(CO_Data['TimeDateSince'].index).year
    CO_Data['month'] = pd.DatetimeIndex(CO_Data['TimeDateSince'].index).month
    CO_Data['day'] = pd.DatetimeIndex(CO_Data['TimeDateSince'].index).day
    CO_Data['hour'] = pd.DatetimeIndex(CO_Data['TimeDateSince'].index).hour
    CO_Data['minute'] = pd.DatetimeIndex(CO_Data['TimeDateSince'].index).minute
    CO_Data['second'] = pd.DatetimeIndex(CO_Data['TimeDateSince'].index).second
