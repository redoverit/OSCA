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
data_Source = 'server' #input either 'externalHarddrive' or 'server'
version_number = 'v1.1' #version of the code
year_start = 2021 #input the year of study
month_start = 10 #input the month of study
default_start_day = 1 #default start date set
day_start = default_start_day

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

gas_Cal_Data_Source = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/NOyOzone/', 'D:/') #identify folders for calibrations and data inputs and output folders
Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/NOyOzone/', 'D:/FirsData/NOyOzone/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/Ratified_' + str(version_number) + '/', 'D:/Ratified_' + str(version_number) + '/')
Data_Source_Folder = np.where((start_year_month_str == '201901')|(start_year_month_str == '201906')|(start_year_month_str == '201909')|(start_year_month_str == '201911'), 'D:/FirsData/NOyOzone/', Data_Source_Folder)
#Data_Output_Folder = np.where((start_year_month_str == '201901')|(start_year_month_str == '201906')|(start_year_month_str == '201909'), 'D:/Ratified_v1.0/', Data_Output_Folder)

gas_Cal = pd.read_csv(str(gas_Cal_Data_Source) + 'Cal_Record.csv') # load the NOy cal record
gas_Cal['datetime'] = gas_Cal['Date'] + ' ' + gas_Cal['Time'] 
gas_Cal['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in gas_Cal['datetime']]

#Load data acquired with the first file format
default_Early_Month = '201910' #a month to load then exclude if post-2019

early_Date = np.where((start_year_month_str == end_year_month_str) & (year_start == 2019) & (2 <= month_start <= 11),  start_year_month_str, default_Early_Month) #str(year_start)
early_Date = np.where((start_year_month_str == end_year_month_str) & (year_start == 2018),  start_year_month_str, early_Date) #str(year_start)

pattern = str(Data_Source_Folder) + str(early_Date) + '*_gas.csv'# Collect CSV files

prior_date = start - timedelta(days=1)
date_Check = str(prior_date.strftime("%Y")) + str(prior_date.strftime("%m")) + str(prior_date.strftime("%d"))
#print(date_Check)

default_prior_day = '20190930'

prior_day = np.where((start_year_month_str == end_year_month_str) & (year_start == 2019) & (2 <= month_start <= 11),  date_Check, default_prior_day) #str(year_start)
prior_day = np.where((start_year_month_str == end_year_month_str) & (year_start == 2018),  default_prior_day, prior_day) #str(year_start)

prior_month_pattern = str(Data_Source_Folder) + str(prior_day) + '*_gas.csv'#
#print(prior_month_pattern)

#june_files_1 = str(Data_Source_Folder) + '201906*0000' + '_gas.csv'
#june_files_2 = str(Data_Source_Folder) + '201906*59' + '_gas.csv' #removing file labelled 201906171837_gas
#june_files_3 = str(Data_Source_Folder) + '201906*01' + '_gas.csv' #removing file labelled 201906201338_gas
#june_files_4 = str(Data_Source_Folder) + '201906*56' + '_gas.csv'

csv_files = glob.glob(pattern) + glob.glob(prior_month_pattern)
#csv_files = np.where(early_Date == '201906', glob.glob(june_files_1) + glob.glob(june_files_2) + glob.glob(june_files_3) + glob.glob(june_files_4), csv_files)

#prior_csv = glob.glob(prior_month_pattern)
#csv_files = pd.concat(csv_files,prior_csv)

gas_frames = []

for csv in csv_files:
    
    #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv, skiprows=3, header=None, usecols=[0,1,2,3,4,5,6,12,13,14,15,16])
    gas_frames.append(df)

early_Data = pd.concat(gas_frames) #sort=true?

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

#early_Data['Date'] = early_Data['Date'].astype(str)
#early_Data['Date_length'] = early_Data['Date'].str.len()
#early_Data=early_Data[early_Data.Date_length == 10]

early_Data['Date'] = early_Data['Date'].astype(str)
early_Data['Date_length'] = early_Data['Date'].str.len()
early_Data=early_Data.loc[early_Data.Date_length == 10] #check the data string length for corruption
early_Data = early_Data.drop(columns=['Date_length'])
early_Data['datetime'] = early_Data['Date']+' '+early_Data['Time']# added Date and time into new columns
early_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in early_Data['datetime']] #converts the dateTime format from string to python dateTime
early_Data.index = early_Data['datetime']
early_Data = early_Data.sort_index()

#NOy Flags: 0 - not used; 1 - good data; 2 - bad data not to be used
#O3 flags: 0 - not used; 1 - good data; 2- suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information; 3 - suspect_data_time_stamp_error
#NO Flags: 0 - not used; 1 - good data; 2 - bad data not to be used
#NOy Flags: 0 - not used; 1 - good data; 2 - bad data not to be used
#NO2 Flags: 0 - not used; 1 - good data; 2 - bad data as gas concentration outside instrument operational range; 3 - suspect data time stamp error

early_Data['O3 Flags+3'] = early_Data['O3 Flags'].shift(periods=3)
early_Data['NOy Flags3'] = early_Data['NOy Flags'].shift(periods=-3)
early_Data['Ozone (ppb)'] = early_Data['Ozone (ppb)'].astype(float)
early_Data['NO2 (ppb)'] = early_Data['NO2 (ppb)'].astype(float)   
early_Data['NO (ppb)'] = early_Data['NO (ppb)'].astype(float)
early_Data['NOy (ppb)'] = early_Data['NOy (ppb)'].astype(float)
  
early_Data['Ozone (ppb) perlim']=np.nan
early_Data['Ozone (ppb) perlim'] = np.where((early_Data['O3 Flags'] == '0C100000') & (early_Data['O3 Flags+3'] == '0C100000') & (early_Data['Ozone (ppb)'] > -5), early_Data['Ozone (ppb)']/1.05, early_Data['Ozone (ppb) perlim'])
early_Data['NO2 (ppb) perlim']=np.nan#create the perliminary NO2 data column
early_Data['NO2 (ppb) perlim'] = np.where((early_Data['NO2 Status'] == 'Sampling')& (early_Data['NO2 (ppb)'] > -5), early_Data['NO2 (ppb)']*0.954, early_Data['NO2 (ppb) perlim'])#populate the column with condition

calibration_code = 'CC000028'

early_Data['NOy Flags_+1_offset'] = early_Data['NOy Flags'].shift(periods=1)
early_Data['NOy Flags_+2_offset'] = early_Data['NOy Flags'].shift(periods=2)
early_Data['NOy Flags_+3_offset'] = early_Data['NOy Flags'].shift(periods=3)
early_Data['NOy Flags_+4_offset'] = early_Data['NOy Flags'].shift(periods=4)
early_Data['NOy Flags_+5_offset'] = early_Data['NOy Flags'].shift(periods=5)
early_Data['NOy Flags_+6_offset'] = early_Data['NOy Flags'].shift(periods=6)
early_Data['NOy Flags_+7_offset'] = early_Data['NOy Flags'].shift(periods=7)
early_Data['NOy Flags_+8_offset'] = early_Data['NOy Flags'].shift(periods=8)
early_Data['NOy Flags_+9_offset'] = early_Data['NOy Flags'].shift(periods=9)
early_Data['NOy Flags_+10_offset'] = early_Data['NOy Flags'].shift(periods=10)
early_Data['NOy Flags_+11_offset'] = early_Data['NOy Flags'].shift(periods=11)
early_Data['NOy Flags_+12_offset'] = early_Data['NOy Flags'].shift(periods=12)
early_Data['NOy Flags_+13_offset'] = early_Data['NOy Flags'].shift(periods=13)
early_Data['NOy Flags_+14_offset'] = early_Data['NOy Flags'].shift(periods=14)
early_Data['NOy Flags_+15_offset'] = early_Data['NOy Flags'].shift(periods=15)
early_Data['NOy Flags_+16_offset'] = early_Data['NOy Flags'].shift(periods=16)
early_Data['NOy Flags_+17_offset'] = early_Data['NOy Flags'].shift(periods=17)
early_Data['NOy Flags_+18_offset'] = early_Data['NOy Flags'].shift(periods=18)
early_Data['NOy Flags_+19_offset'] = early_Data['NOy Flags'].shift(periods=19)
early_Data['NOy Flags_+20_offset'] = early_Data['NOy Flags'].shift(periods=20)
early_Data['NOy Flags_+21_offset'] = early_Data['NOy Flags'].shift(periods=21)
early_Data['NOy Flags_+22_offset'] = early_Data['NOy Flags'].shift(periods=22)
early_Data['NOy Flags_+23_offset'] = early_Data['NOy Flags'].shift(periods=23)
early_Data['NOy Flags_+24_offset'] = early_Data['NOy Flags'].shift(periods=24)
early_Data['NOy Flags_+25_offset'] = early_Data['NOy Flags'].shift(periods=25)
early_Data['NOy Flags_+26_offset'] = early_Data['NOy Flags'].shift(periods=26)
early_Data['NOy Flags_+27_offset'] = early_Data['NOy Flags'].shift(periods=27)
early_Data['NOy Flags_+28_offset'] = early_Data['NOy Flags'].shift(periods=28)
early_Data['NOy Flags_+29_offset'] = early_Data['NOy Flags'].shift(periods=29)
early_Data['NOy Flags_+30_offset'] = early_Data['NOy Flags'].shift(periods=30)
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+1_offset'] == str(calibration_code)),early_Data['NOy Flags_+1_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+2_offset'] == str(calibration_code)),early_Data['NOy Flags_+2_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+3_offset'] == str(calibration_code)),early_Data['NOy Flags_+3_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+4_offset'] == str(calibration_code)),early_Data['NOy Flags_+4_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+5_offset'] == str(calibration_code)),early_Data['NOy Flags_+5_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+6_offset'] == str(calibration_code)),early_Data['NOy Flags_+6_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+7_offset'] == str(calibration_code)),early_Data['NOy Flags_+7_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+8_offset'] == str(calibration_code)),early_Data['NOy Flags_+8_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+9_offset'] == str(calibration_code)),early_Data['NOy Flags_+9_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+10_offset'] == str(calibration_code)),early_Data['NOy Flags_+10_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+11_offset'] == str(calibration_code)),early_Data['NOy Flags_+11_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+12_offset'] == str(calibration_code)),early_Data['NOy Flags_+12_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+13_offset'] == str(calibration_code)),early_Data['NOy Flags_+13_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+14_offset'] == str(calibration_code)),early_Data['NOy Flags_+14_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+15_offset'] == str(calibration_code)),early_Data['NOy Flags_+15_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+16_offset'] == str(calibration_code)),early_Data['NOy Flags_+16_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+17_offset'] == str(calibration_code)),early_Data['NOy Flags_+17_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+18_offset'] == str(calibration_code)),early_Data['NOy Flags_+18_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+19_offset'] == str(calibration_code)),early_Data['NOy Flags_+19_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+20_offset'] == str(calibration_code)),early_Data['NOy Flags_+20_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+10_offset'] == str(calibration_code)),early_Data['NOy Flags_+20_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+21_offset'] == str(calibration_code)),early_Data['NOy Flags_+21_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+22_offset'] == str(calibration_code)),early_Data['NOy Flags_+22_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+23_offset'] == str(calibration_code)),early_Data['NOy Flags_+23_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+24_offset'] == str(calibration_code)),early_Data['NOy Flags_+24_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+25_offset'] == str(calibration_code)),early_Data['NOy Flags_+25_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+26_offset'] == str(calibration_code)),early_Data['NOy Flags_+26_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+27_offset'] == str(calibration_code)),early_Data['NOy Flags_+27_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+28_offset'] == str(calibration_code)),early_Data['NOy Flags_+28_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+29_offset'] == str(calibration_code)),early_Data['NOy Flags_+29_offset'],early_Data['NOy Flags'])
early_Data['NOy Flags'] = np.where((early_Data['NOy Flags_+30_offset'] == str(calibration_code)),early_Data['NOy Flags_+30_offset'],early_Data['NOy Flags'])

#dropping newly made columns flagged data
early_Data = early_Data.drop(columns=['NOy Flags_+1_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+2_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+3_offset']) 
early_Data = early_Data.drop(columns=['NOy Flags_+4_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+5_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+6_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+7_offset']) 
early_Data = early_Data.drop(columns=['NOy Flags_+8_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+9_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+10_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+11_offset']) 
early_Data = early_Data.drop(columns=['NOy Flags_+12_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+13_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+14_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+15_offset']) 
early_Data = early_Data.drop(columns=['NOy Flags_+16_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+17_offset']) 
early_Data = early_Data.drop(columns=['NOy Flags_+18_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+19_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+20_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+21_offset']) 
early_Data = early_Data.drop(columns=['NOy Flags_+22_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+23_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+24_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+25_offset']) 
early_Data = early_Data.drop(columns=['NOy Flags_+26_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+27_offset']) 
early_Data = early_Data.drop(columns=['NOy Flags_+28_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+29_offset'])
early_Data = early_Data.drop(columns=['NOy Flags_+30_offset'])

#early_Data.to_csv(str(Data_Output_Folder) + 'nox-noxy_prelim_1_' + str(date_file_label) + '.csv')

early_Data['NOy a'] = np.interp(early_Data['datetime'], gas_Cal['datetime'], gas_Cal['NOy_Zero']) # interpolate the zero values
early_Data['NOy b'] = np.interp(early_Data['datetime'], gas_Cal['datetime'], gas_Cal['NOy_Slope']) #
early_Data['NO (ppb) perlim']=np.nan
early_Data['NO (ppb) perlim'] = np.where((early_Data['NOy Flags'] == "CC000000"), early_Data['NO (ppb)']*early_Data['NOy b'] + early_Data['NOy a'], early_Data['NO (ppb) perlim'])
early_Data['NOy (ppb) perlim']=np.nan
early_Data['NOy (ppb) perlim'] = np.where((early_Data['NOy Flags'] == "CC000000"), early_Data['NOy (ppb)']*early_Data['NOy b'] + early_Data['NOy a'], early_Data['NOy (ppb) perlim'])
early_Data['Diff (ppb) perlim']=np.nan
early_Data['Diff (ppb) perlim'] = np.where((early_Data['NOy Flags'] == "CC000000"), early_Data['NOy (ppb) perlim'] - early_Data['NO (ppb) perlim'], early_Data['Diff (ppb) perlim'])
   
#early_Data = early_Data.groupby(pd.Grouper(freq=av_Freq)).mean()

#Data acquired with the final file format
default_Later_Month = '201912'

later_Date = np.where((start_year_month_str == end_year_month_str) & ((year_start >= 2020) | ((year_start == 2019) & (month_start >= 11))),  start_year_month_str, default_Later_Month)
print(later_Date)

pattern_2 = str(Data_Source_Folder) + str(later_Date) + '*_firsgas.csv'

default_Later_Day = '20191130'

later_Day = np.where((start_year_month_str == end_year_month_str) & ((year_start >= 2020) | ((year_start == 2019) & (month_start >= 11))), date_Check, default_Later_Day)

prior_month_pattern_2 = str(Data_Source_Folder) + str(later_Day) + '*_firsgas.csv'

all_Data = pd.concat(map(pd.read_csv, (glob.glob(pattern_2) + glob.glob(prior_month_pattern_2))),sort=True)
all_Data['O3 Flags+3'] = all_Data['O3 Flags'].shift(periods=3)
all_Data['NOyFlagsF'] = all_Data['NOy Flags'].shift(periods=6)
#all_Data.rename(columns={'NOy Flags': 'NOyFlags'}, inplace=True)

all_Data['datetime'] = all_Data['Date']+' '+all_Data['Time']# added Date and time into new columns
all_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in all_Data['datetime']] #converts the dateTime format from string to python dateTime
all_Data = all_Data.drop(columns=['S2 NO (ppb)', 'S2 NO2 (ppb)', 'S2 NOx (ppb)', 'S2 SO2 (ppb)', 'S2 CO (ppb)','S3 Ozone (ppb)', 'S3 Status', 'S2 SO2 Flags ', 'S2 CO Flags', 'S2 NOx Flags'])
all_Data.index = all_Data['datetime']
all_Data = all_Data.sort_index()

all_Data['Ozone (ppb) perlim']=np.nan
all_Data['Ozone (ppb) perlim'] = np.where((all_Data['O3 Flags'] == '0C100000') & (all_Data['O3 Flags+3'] == '0C100000') & (all_Data['Ozone (ppb)'] > -5), all_Data['Ozone (ppb)']/1.05, np.nan)
all_Data['NO2 (ppb) perlim']=np.nan#create the perliminary NO2 data column
all_Data['NO2 (ppb) perlim'] = np.where((all_Data['NO2 Status'] == 'Sampling') & (all_Data['NO2 (ppb)'] > -5), all_Data['NO2 (ppb)']*0.954, all_Data['NO2 (ppb) perlim'])#populate the column with condition

all_Data['NOy Flags_+1_offset'] = all_Data['NOy Flags'].shift(periods=1)
all_Data['NOy Flags_+2_offset'] = all_Data['NOy Flags'].shift(periods=2)
all_Data['NOy Flags_+3_offset'] = all_Data['NOy Flags'].shift(periods=3)
all_Data['NOy Flags_+4_offset'] = all_Data['NOy Flags'].shift(periods=4)
all_Data['NOy Flags_+5_offset'] = all_Data['NOy Flags'].shift(periods=5)
all_Data['NOy Flags_+6_offset'] = all_Data['NOy Flags'].shift(periods=6)
all_Data['NOy Flags_+7_offset'] = all_Data['NOy Flags'].shift(periods=7)
all_Data['NOy Flags_+8_offset'] = all_Data['NOy Flags'].shift(periods=8)
all_Data['NOy Flags_+9_offset'] = all_Data['NOy Flags'].shift(periods=9)
all_Data['NOy Flags_+10_offset'] = all_Data['NOy Flags'].shift(periods=10)
all_Data['NOy Flags_+11_offset'] = all_Data['NOy Flags'].shift(periods=11)
all_Data['NOy Flags_+12_offset'] = all_Data['NOy Flags'].shift(periods=12)
all_Data['NOy Flags_+13_offset'] = all_Data['NOy Flags'].shift(periods=13)
all_Data['NOy Flags_+14_offset'] = all_Data['NOy Flags'].shift(periods=14)
all_Data['NOy Flags_+15_offset'] = all_Data['NOy Flags'].shift(periods=15)
all_Data['NOy Flags_+16_offset'] = all_Data['NOy Flags'].shift(periods=16)
all_Data['NOy Flags_+17_offset'] = all_Data['NOy Flags'].shift(periods=17)
all_Data['NOy Flags_+18_offset'] = all_Data['NOy Flags'].shift(periods=18)
all_Data['NOy Flags_+19_offset'] = all_Data['NOy Flags'].shift(periods=19)
all_Data['NOy Flags_+20_offset'] = all_Data['NOy Flags'].shift(periods=20)
all_Data['NOy Flags_+21_offset'] = all_Data['NOy Flags'].shift(periods=21)
all_Data['NOy Flags_+22_offset'] = all_Data['NOy Flags'].shift(periods=22)
all_Data['NOy Flags_+23_offset'] = all_Data['NOy Flags'].shift(periods=23)
all_Data['NOy Flags_+24_offset'] = all_Data['NOy Flags'].shift(periods=24)
all_Data['NOy Flags_+25_offset'] = all_Data['NOy Flags'].shift(periods=25)
all_Data['NOy Flags_+26_offset'] = all_Data['NOy Flags'].shift(periods=26)
all_Data['NOy Flags_+27_offset'] = all_Data['NOy Flags'].shift(periods=27)
all_Data['NOy Flags_+28_offset'] = all_Data['NOy Flags'].shift(periods=28)
all_Data['NOy Flags_+29_offset'] = all_Data['NOy Flags'].shift(periods=29)
all_Data['NOy Flags_+30_offset'] = all_Data['NOy Flags'].shift(periods=30)
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+1_offset'] == str(calibration_code)),all_Data['NOy Flags_+1_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+2_offset'] == str(calibration_code)),all_Data['NOy Flags_+2_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+3_offset'] == str(calibration_code)),all_Data['NOy Flags_+3_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+4_offset'] == str(calibration_code)),all_Data['NOy Flags_+4_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+5_offset'] == str(calibration_code)),all_Data['NOy Flags_+5_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+6_offset'] == str(calibration_code)),all_Data['NOy Flags_+6_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+7_offset'] == str(calibration_code)),all_Data['NOy Flags_+7_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+8_offset'] == str(calibration_code)),all_Data['NOy Flags_+8_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+9_offset'] == str(calibration_code)),all_Data['NOy Flags_+9_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+10_offset'] == str(calibration_code)),all_Data['NOy Flags_+10_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+11_offset'] == str(calibration_code)),all_Data['NOy Flags_+11_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+12_offset'] == str(calibration_code)),all_Data['NOy Flags_+12_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+13_offset'] == str(calibration_code)),all_Data['NOy Flags_+13_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+14_offset'] == str(calibration_code)),all_Data['NOy Flags_+14_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+15_offset'] == str(calibration_code)),all_Data['NOy Flags_+15_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+16_offset'] == str(calibration_code)),all_Data['NOy Flags_+16_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+17_offset'] == str(calibration_code)),all_Data['NOy Flags_+17_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+18_offset'] == str(calibration_code)),all_Data['NOy Flags_+18_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+19_offset'] == str(calibration_code)),all_Data['NOy Flags_+19_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+20_offset'] == str(calibration_code)),all_Data['NOy Flags_+20_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+21_offset'] == str(calibration_code)),all_Data['NOy Flags_+21_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+22_offset'] == str(calibration_code)),all_Data['NOy Flags_+22_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+23_offset'] == str(calibration_code)),all_Data['NOy Flags_+23_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+24_offset'] == str(calibration_code)),all_Data['NOy Flags_+24_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+25_offset'] == str(calibration_code)),all_Data['NOy Flags_+25_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+26_offset'] == str(calibration_code)),all_Data['NOy Flags_+26_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+27_offset'] == str(calibration_code)),all_Data['NOy Flags_+27_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+28_offset'] == str(calibration_code)),all_Data['NOy Flags_+28_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+29_offset'] == str(calibration_code)),all_Data['NOy Flags_+29_offset'],all_Data['NOy Flags'])
all_Data['NOy Flags'] = np.where((all_Data['NOy Flags_+30_offset'] == str(calibration_code)),all_Data['NOy Flags_+30_offset'],all_Data['NOy Flags'])

#all_Data = all_Data.drop(columns=['NOy Flags_*_offset'])
#dropping newly made columns flagged data
all_Data = all_Data.drop(columns=['NOy Flags_+1_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+2_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+3_offset']) 
all_Data = all_Data.drop(columns=['NOy Flags_+4_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+5_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+6_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+7_offset']) 
all_Data = all_Data.drop(columns=['NOy Flags_+8_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+9_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+10_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+11_offset']) 
all_Data = all_Data.drop(columns=['NOy Flags_+12_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+13_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+14_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+15_offset']) 
all_Data = all_Data.drop(columns=['NOy Flags_+16_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+17_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+18_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+19_offset']) 
all_Data = all_Data.drop(columns=['NOy Flags_+20_offset']) 
all_Data = all_Data.drop(columns=['NOy Flags_+21_offset']) 
all_Data = all_Data.drop(columns=['NOy Flags_+22_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+23_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+24_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+25_offset']) 
all_Data = all_Data.drop(columns=['NOy Flags_+26_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+27_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+28_offset'])
all_Data = all_Data.drop(columns=['NOy Flags_+29_offset']) 
all_Data = all_Data.drop(columns=['NOy Flags_+30_offset']) #dropping newly made columns flagged data

all_Data['NOy a'] = np.interp(all_Data['datetime'], gas_Cal['datetime'], gas_Cal['NOy_Zero']) # interpolate the zero values
all_Data['NOy b'] = np.interp(all_Data['datetime'], gas_Cal['datetime'], gas_Cal['NOy_Slope']) #
all_Data['NO (ppb) perlim']=np.nan
all_Data['NO (ppb) perlim'] = np.where((all_Data['NOy Flags'] == "CC000000"), all_Data['NO (ppb)']*all_Data['NOy b'] + all_Data['NOy a'], all_Data['NO (ppb) perlim'])
all_Data['NOy (ppb) perlim']=np.nan
all_Data['NOy (ppb) perlim'] = np.where((all_Data['NOy Flags'] == "CC000000"), all_Data['NOy (ppb)']*all_Data['NOy b'] + all_Data['NOy a'], all_Data['NOy (ppb) perlim'])
all_Data['Diff (ppb) perlim']=np.nan
all_Data['Diff (ppb) perlim'] = np.where((all_Data['NOy Flags'] == "CC000000"), all_Data['NOy (ppb) perlim'] - all_Data['NO (ppb) perlim'], all_Data['Diff (ppb) perlim'])

all_Data = pd.concat([early_Data, all_Data])
all_Data = all_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
all_Data = all_Data[start:end]

#go through the log to find any problems with the different gas analysers

start_uncertainty = datetime.datetime(2018,12,18,0,0,00)
end_uncertainty = datetime.datetime(2019,1,10,23,59,00)

start_simon = datetime.datetime(2018,12,18,0,0,00) #data from instruments located in room 2.10 Simon Building
end_simon = datetime.datetime(2019,1,29,23,59,00)
all_Data.drop(all_Data.loc[start_simon:end_simon].index, inplace=True)

start_move_1 = datetime.datetime(2019,1,30,0,0,00) #instrument moved to FIRS trailer
end_move_1 = datetime.datetime(2019,1,30,23,59,00)
all_Data.drop(all_Data.loc[start_move_1:end_move_1].index, inplace=True)

#start_move_2 = datetime.datetime(2019,6,6,0,0,00) #instrument moved to FIRS cabin needs to be defined
#end_move_2 = datetime.datetime(2019,6,7,23,59,00)
#all_Data.drop(all_Data.loc[start_move_2:end_move_2].index, inplace=True)

start_audit1 = datetime.datetime(2019,8,9,6,30,00)
end_audit1 = datetime.datetime(2019,8,9,12,00,00)
all_Data.drop(all_Data.loc[start_audit1:end_audit1].index, inplace=True)

#start_x = datetime.datetime(2019,8,9,16,30,00) 
#end_x = datetime.datetime(2019,8,9,18,00,00)
#all_Data.drop(all_Data.loc[start_x:end_x].index, inplace=True)


all_Data['O3_qc_flags']=np.where(all_Data['Ozone (ppb) perlim']>-5, '1','2')
all_Data.loc[start_uncertainty:end_uncertainty, 'O3_qc_flags'] = "3"
ozone_Data = all_Data[['Ozone (ppb) perlim', 'O3_qc_flags']]
ozone_Data['O3_qc_flags']=np.where(ozone_Data['Ozone (ppb) perlim']>200,'2', ozone_Data['O3_qc_flags']) 
#ozone_Data.drop(ozone_Data[(ozone_Data['O3_qc_flags'] == '2')].index,inplace =True)
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['Ozone (ppb) perlim'].isnull()), '0', ozone_Data['O3_qc_flags']) 
ozone_Data.drop(ozone_Data[(ozone_Data['O3_qc_flags'] == '0')].index,inplace =True)

start_O3_gas_span1 = datetime.datetime(2019,8,22,12,45,00) # O3 gas span without cal on turned on
end_O3_gas_span1 = datetime.datetime(2019,8,22,13,5,00)
ozone_Data.drop(ozone_Data.loc[start_O3_gas_span1:end_O3_gas_span1].index, inplace=True)

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
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_-6_offset']>'1'),ozone_Data['O3_qc_flags_-6_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_-5_offset']>'1'),ozone_Data['O3_qc_flags_-5_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_-4_offset']>'1'),ozone_Data['O3_qc_flags_-4_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_-3_offset']>'1'),ozone_Data['O3_qc_flags_-3_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_-2_offset']>'1'),ozone_Data['O3_qc_flags_-2_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_-1_offset']>'1'),ozone_Data['O3_qc_flags_-1_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_+1_offset']>'1'),ozone_Data['O3_qc_flags_+1_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_+2_offset']>'1'),ozone_Data['O3_qc_flags_+2_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_+3_offset']>'1'),ozone_Data['O3_qc_flags_+3_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_+4_offset']>'1'),ozone_Data['O3_qc_flags_+4_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_+5_offset']>'1'),ozone_Data['O3_qc_flags_+5_offset'],ozone_Data['O3_qc_flags'])
ozone_Data['O3_qc_flags'] = np.where((ozone_Data['O3_qc_flags_+6_offset']>'1'),ozone_Data['O3_qc_flags_+6_offset'],ozone_Data['O3_qc_flags'])
O3_Flag_Offset = list(ozone_Data.columns.values)
O3_Flag_Offset.remove('Ozone (ppb) perlim')
O3_Flag_Offset.remove('O3_qc_flags')
ozone_Data = ozone_Data.drop(columns=O3_Flag_Offset) #dropping newly made columns flagged data

ozone_Data.rename(columns={"Ozone (ppb) perlim": "Ozone (ppb)"}, inplace = True)

plt.plot(ozone_Data["Ozone (ppb)"], label='O3')
plt.plot(ozone_Data['O3_qc_flags'], label='O3 flags')
plt.legend()
plt.ylabel('ppm')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('font', **font)
#plt.ylim(10, 30)
#plt.figure()
plt.show()

gas_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/gas_Analyser/'
check_Folder = os.path.isdir(gas_Folder)
if not check_Folder:
    os.makedirs(gas_Folder)
    print("created folder : ", gas_Folder)

else:
    print(gas_Folder, "folder already exists.")

ozone_Data.to_csv(str(gas_Folder) + 'maqs-O3-concentration_' + str(date_file_label) + '_' + str(version_number) + '.csv')

ozone_Data['TimeDateSince'] = ozone_Data.index-datetime.datetime(1970,1,1,0,0,00)
ozone_Data['TimeSecondsSince'] = ozone_Data['TimeDateSince'].dt.total_seconds()
ozone_Data['day_year'] = pd.DatetimeIndex(ozone_Data.index).dayofyear
ozone_Data['year'] = pd.DatetimeIndex(ozone_Data.index).year
ozone_Data['month'] = pd.DatetimeIndex(ozone_Data.index).month
ozone_Data['day'] = pd.DatetimeIndex(ozone_Data.index).day
ozone_Data['hour'] = pd.DatetimeIndex(ozone_Data.index).hour
ozone_Data['minute'] = pd.DatetimeIndex(ozone_Data.index).minute
ozone_Data['second'] = pd.DatetimeIndex(ozone_Data.index).second

all_Data['NO2_qc_flags']=np.where(all_Data['NO2 (ppb) perlim']>-5, '1','2')
all_Data.loc[start_uncertainty:end_uncertainty, 'NO2_qc_flags'] = "3"
NO2_Data = all_Data[['NO2 (ppb) perlim', 'NO2_qc_flags']]
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2 (ppb) perlim'].isnull()), '0', NO2_Data['NO2_qc_flags']) 
NO2_Data.drop(NO2_Data[(NO2_Data['NO2_qc_flags'] == '0')].index,inplace =True)
NO2_Data['NO2_qc_flags']=np.where(NO2_Data['NO2 (ppb) perlim']>200,'2', NO2_Data['NO2_qc_flags'])
#NO2_Data.drop(NO2_Data[(NO2_Data['NO2_qc_flags'] == '2')].index,inplace =True)

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
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_-6_offset']>'1'),NO2_Data['NO2_qc_flags_-6_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_-5_offset']>'1'),NO2_Data['NO2_qc_flags_-5_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_-4_offset']>'1'),NO2_Data['NO2_qc_flags_-4_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_-3_offset']>'1'),NO2_Data['NO2_qc_flags_-3_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_-2_offset']>'1'),NO2_Data['NO2_qc_flags_-2_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_-1_offset']>'1'),NO2_Data['NO2_qc_flags_-1_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_+1_offset']>'1'),NO2_Data['NO2_qc_flags_+1_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_+2_offset']>'1'),NO2_Data['NO2_qc_flags_+2_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_+3_offset']>'1'),NO2_Data['NO2_qc_flags_+3_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_+4_offset']>'1'),NO2_Data['NO2_qc_flags_+4_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_+5_offset']>'1'),NO2_Data['NO2_qc_flags_+5_offset'],NO2_Data['NO2_qc_flags'])
NO2_Data['NO2_qc_flags'] = np.where((NO2_Data['NO2_qc_flags_+6_offset']>'1'),NO2_Data['NO2_qc_flags_+6_offset'],NO2_Data['NO2_qc_flags'])
NO2_Flag_Offset = list(NO2_Data.columns.values)
NO2_Flag_Offset.remove('NO2 (ppb) perlim')
NO2_Flag_Offset.remove('NO2_qc_flags')
NO2_Data = NO2_Data.drop(columns=NO2_Flag_Offset) #dropping newly made columns flagged data

NO2_Data.rename(columns={"NO2 (ppb) perlim": "NO2 (ppb)"}, inplace = True)

plt.plot(NO2_Data['NO2 (ppb)'], label='NO2')
plt.plot(NO2_Data['NO2_qc_flags'], label='NO2 Flags')
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

NO2_Data.to_csv(str(gas_Folder) + 'maqs-NO2-concentration_' + str(date_file_label) + '_' + str(version_number) + '.csv')

NO2_Data['TimeDateSince'] = NO2_Data.index-datetime.datetime(1970,1,1,0,0,00)
NO2_Data['TimeSecondsSince'] = NO2_Data['TimeDateSince'].dt.total_seconds()
NO2_Data['day_year'] = pd.DatetimeIndex(NO2_Data.index).dayofyear
NO2_Data['year'] = pd.DatetimeIndex(NO2_Data.index).year
NO2_Data['month'] = pd.DatetimeIndex(NO2_Data.index).month
NO2_Data['day'] = pd.DatetimeIndex(NO2_Data.index).day
NO2_Data['hour'] = pd.DatetimeIndex(NO2_Data.index).hour
NO2_Data['minute'] = pd.DatetimeIndex(NO2_Data.index).minute
NO2_Data['second'] = pd.DatetimeIndex(NO2_Data.index).second

all_Data['NOy_qc_flags']=np.where(all_Data['NOy (ppb) perlim']>-5, '1','2')
all_Data.loc[start_uncertainty:end_uncertainty, 'NOy_qc_flags'] = "3" # remove data from dates where files are convoluted
all_Data['NOy_qc_flags'] = np.where(all_Data['Diff (ppb) perlim']>0, all_Data['NOy_qc_flags'], '3') #flag data where the NOy - NO goes negative
NOy_Data = all_Data[['NOy (ppb) perlim', 'NO (ppb) perlim','NOy_qc_flags']]

start_inlet_reconfig_1 = datetime.datetime(2019,8,9,16,30,00) # 09-08-2019 16:30 - 18:00 audit and calibration of FIDAS
end_inlet_reconfig_1 = datetime.datetime(2019,8,9,18,00,00)
NOy_Data.drop(NOy_Data.loc[start_inlet_reconfig_1:end_inlet_reconfig_1].index, inplace=True)

#NOy_Data.drop(NOy_Data[(NOy_Data['NOy_qc_flags'] == '2')].index,inplace =True)
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy (ppb) perlim'].isnull()), '0', NOy_Data['NOy_qc_flags']) 
NOy_Data.drop(NOy_Data[(NOy_Data['NOy_qc_flags'] == '0')].index,inplace =True)
NOy_Data['NOy_qc_flags']=np.where(NOy_Data['NOy (ppb) perlim']>200,'3', NOy_Data['NOy_qc_flags'])

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
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_-6_offset']>'1'),NOy_Data['NOy_qc_flags_-6_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_-5_offset']>'1'),NOy_Data['NOy_qc_flags_-5_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_-4_offset']>'1'),NOy_Data['NOy_qc_flags_-4_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_-3_offset']>'1'),NOy_Data['NOy_qc_flags_-3_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_-2_offset']>'1'),NOy_Data['NOy_qc_flags_-2_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_-1_offset']>'1'),NOy_Data['NOy_qc_flags_-1_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_+1_offset']>'1'),NOy_Data['NOy_qc_flags_+1_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_+2_offset']>'1'),NOy_Data['NOy_qc_flags_+2_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_+3_offset']>'1'),NOy_Data['NOy_qc_flags_+3_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_+4_offset']>'1'),NOy_Data['NOy_qc_flags_+4_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_+5_offset']>'1'),NOy_Data['NOy_qc_flags_+5_offset'],NOy_Data['NOy_qc_flags'])
NOy_Data['NOy_qc_flags'] = np.where((NOy_Data['NOy_qc_flags_+6_offset']>'1'),NOy_Data['NOy_qc_flags_+6_offset'],NOy_Data['NOy_qc_flags'])
NOy_Flag_Offset = list(NOy_Data.columns.values)
NOy_Flag_Offset.remove('NOy (ppb) perlim')
NOy_Flag_Offset.remove('NO (ppb) perlim')
NOy_Flag_Offset.remove('NOy_qc_flags')
NOy_Data = NOy_Data.drop(columns=NOy_Flag_Offset) #dropping newly made columns flagged data

#NOy_Data.drop(NOy_Data[(NOy_Data['NOy_qc_flags'] == '3')].index,inplace =True)
start_NOy_gas_sampling_check = datetime.datetime(2020,6,24,9,10,00)
end_NOy_gas_sampling_check = datetime.datetime(2020,6,24,12,15,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_sampling_check:end_NOy_gas_sampling_check].index, inplace=True)

start_NOy_gas_span1 = datetime.datetime(2019,8,22,12,45,00) # NOy gas span without cal on turned on
end_NOy_gas_span1 = datetime.datetime(2019,8,22,13,5,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span1:end_NOy_gas_span1].index, inplace=True)

start_NOy_gas_span2 = datetime.datetime(2019,9,6,14,10,00) 
end_NOy_gas_span2 = datetime.datetime(2019,9,6,14,30,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span2:end_NOy_gas_span2].index, inplace=True)

start_NOy_gas_span3 = datetime.datetime(2019,9,10,14,10,00)
end_NOy_gas_span3 = datetime.datetime(2019,9,10,14,50,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span3:end_NOy_gas_span3].index, inplace=True)

start_NOy_gas_span4 = datetime.datetime(2019,9,17,10,25,00)
end_NOy_gas_span4 = datetime.datetime(2019,9,17,10,45,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span4:end_NOy_gas_span4].index, inplace=True)

start_NOy_gas_span5 = datetime.datetime(2019,9,26,8,55,00)
end_NOy_gas_span5 = datetime.datetime(2019,9,26,9,15,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span5:end_NOy_gas_span5].index, inplace=True)

start_NOy_gas_span6 = datetime.datetime(2019,10,2,14,35,00)
end_NOy_gas_span6 = datetime.datetime(2019,10,2,14,55,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span6:end_NOy_gas_span6].index, inplace=True)

start_NOy_gas_span7 = datetime.datetime(2019,10,9,13,55,00)
end_NOy_gas_span7 = datetime.datetime(2019,10,9,14,15,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span7:end_NOy_gas_span7].index, inplace=True)

start_NOy_gas_span8 = datetime.datetime(2019,10,15,12,55,00)
end_NOy_gas_span8 = datetime.datetime(2019,10,15,13,25,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span8:end_NOy_gas_span8].index, inplace=True)

start_NOy_gas_span9 = datetime.datetime(2019,10,24,8,10,00)
end_NOy_gas_span9 = datetime.datetime(2019,10,24,9,10,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span9:end_NOy_gas_span9].index, inplace=True)

start_NOy_gas_span10 = datetime.datetime(2019,10,31,11,10,00)
end_NOy_gas_span10 = datetime.datetime(2019,10,31,11,40,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span10:end_NOy_gas_span10].index, inplace=True)

start_NOy_gas_span11 = datetime.datetime(2020,9,25,9,10,00)
end_NOy_gas_span11 = datetime.datetime(2020,9,25,10,40,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span11:end_NOy_gas_span11].index, inplace=True)

start_NOy_gas_span12 = datetime.datetime(2021,3,30,6,30,00)
end_NOy_gas_span12 = datetime.datetime(2021,3,30,10,40,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span12:end_NOy_gas_span12].index, inplace=True)

start_NOy_gas_span13 = datetime.datetime(2021,10,21,10,20,00)
end_NOy_gas_span13 = datetime.datetime(2021,10,21,10,50,00)
NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span13:end_NOy_gas_span13].index, inplace=True)

#start_NOy_gas_span12 = datetime.datetime(2019,10,31,11,10,00)
#end_NOy_gas_span12 = datetime.datetime(2019,10,31,11,40,00)
#NOy_Data.drop(NOy_Data.loc[start_NOy_gas_span12:end_NOy_gas_span12].index, inplace=True)

NOy_Data.rename(columns={"NOy (ppb) perlim": "NOy (ppb)", "NO (ppb) perlim": "NO (ppb)" }, inplace = True)

plt.plot(NOy_Data['NOy (ppb)'], label='NOy')
plt.plot(NOy_Data['NO (ppb)'], label='NO')
plt.plot(NOy_Data['NOy_qc_flags'], label='NOy Flags')
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

NOy_Data.to_csv(str(gas_Folder) + 'maqs-nox-noxy-concentration_' + str(date_file_label) + '_' + str(version_number) + '.csv')

NOy_Data['TimeDateSince'] = NOy_Data.index-datetime.datetime(1970,1,1,0,0,00)
NOy_Data['TimeSecondsSince'] = NOy_Data['TimeDateSince'].dt.total_seconds()
NOy_Data['day_year'] = pd.DatetimeIndex(NOy_Data.index).dayofyear
NOy_Data['year'] = pd.DatetimeIndex(NOy_Data.index).year
NOy_Data['month'] = pd.DatetimeIndex(NOy_Data.index).month
NOy_Data['day'] = pd.DatetimeIndex(NOy_Data.index).day
NOy_Data['hour'] = pd.DatetimeIndex(NOy_Data.index).hour
NOy_Data['minute'] = pd.DatetimeIndex(NOy_Data.index).minute
NOy_Data['second'] = pd.DatetimeIndex(NOy_Data.index).second