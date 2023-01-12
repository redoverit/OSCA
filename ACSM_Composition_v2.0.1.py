# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 17:31:56 2022

@author: j65808nw
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

av_Freq = '30min' #averaging frequency required of the data
data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v2.0' #version of the code
year_start = 2022 #input the year of study
month_start = 12 #input the month of study
default_start_day = 1 #default start date set
day_start = default_start_day
validity_status = 'Ratified' #Ratified or Unratified
file_type = '.csv'

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
year_str = str(start.strftime("%Y"))
end_year_month_str = str(end.strftime("%Y")) + str(end.strftime("%m"))

end_Date_Check = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))
print(end_Date_Check) #print end date to check it is correct

date_file_label = np.where(start_year_month_str == end_year_month_str, start_year_month_str, str(start_year_month_str) + "-" + str(end_year_month_str))
print(date_file_label) #print end date to check it is correct

folder = np.where((str(version_number) == 'v0.6'), 'Preliminary', str(validity_status))

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FirsData/ACSM/ACSMProcessedData/', 'D:/FirsData/ACSM/ACSMProcessedData/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(folder) + '_' + str(version_number) + '/', 'D:/' + str(folder) + '_' + str(version_number) + '/')

Year_files = str(Data_Source_Folder) + 'time_series' + '*_final_v2.0.csv'

ACSM_csv_files = glob.glob(Year_files)

# Create an empty list
frames = []

#  Iterate over csv_files
for csv in ACSM_csv_files:
    csv = open(csv, 'r', errors='ignore')
    df = pd.read_csv(csv, index_col=False, encoding= 'unicode_escape', error_bad_lines=False) # , skiprows=25, header=None
    frames.append(df)

# Concatenate frames into a single DataFrame
ACSM_Data = pd.concat(frames, sort=True)

ACSM_Data.rename(columns={'Chl' : 'Chl (ug/m3)', 'NH4' : 'NH4 (ug/m3)', 'NO3' : 'NO3 (ug/m3)', 'SO4' : 'SO4 (ug/m3)', 'Org' : 'organic (ug/m3)' }, inplace=True)
ACSM_Data = ACSM_Data[['acsm_utc_time', 'Chl (ug/m3)', 'NH4 (ug/m3)', 'NO3 (ug/m3)', 'SO4 (ug/m3)', 'organic (ug/m3)']]
ACSM_Data.rename(columns={'acsm_utc_time' : 'datetime' }, inplace=True)

ACSM_Data['datetime'] = ACSM_Data['datetime'].astype(str)
ACSM_Data['datetime_length'] = ACSM_Data['datetime'].str.len() 
ACSM_Data=ACSM_Data[ACSM_Data.datetime_length == 19]

ACSM_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in ACSM_Data['datetime']]
ACSM_Data.index = ACSM_Data['datetime']
ACSM_Data = ACSM_Data.sort_index()
ACSM_Data = ACSM_Data.drop(columns=['datetime', 'datetime_length'])
#print(ACSM_Data)

ACSM_Data = ACSM_Data[start:end]

ACSM_Data['qc_Flags'] = 1

start_prealign_1 = datetime.datetime(2019,6,20,0,0,00)
end_prealign_1 = datetime.datetime(2019,9,13,12,0,00)
ACSM_Data.loc[start_prealign_1:end_prealign_1, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_prealign_1:end_prealign_1].index, inplace=True)

start_pressure_1 = datetime.datetime(2019,9,25,9,0,00)
end_pressure_1 = datetime.datetime(2019,9,25,9,30,00)
ACSM_Data.loc[start_pressure_1:end_pressure_1, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_pressure_1:end_pressure_1].index, inplace=True)

start_airbeam_1 = datetime.datetime(2019,12,3,19,0,00)
end_airbeam_1 = datetime.datetime(2019,12,18,10,0,00)
ACSM_Data.loc[start_airbeam_1:end_airbeam_1, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_airbeam_1:end_airbeam_1].index, inplace=True)

start_airbeam_2 = datetime.datetime(2020,1,29,12,0,00)
end_airbeam_2 = datetime.datetime(2020,2,4,12,0,00)
ACSM_Data.loc[start_airbeam_2:end_airbeam_2, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_airbeam_2:end_airbeam_2].index, inplace=True)

start_pressure_2 = datetime.datetime(2020,2,25,15,30,00) # lowpressure ACSM igor error.
end_pressure_2 = datetime.datetime(2020,2,28,15,40,00)
#ACSM_Data.loc[start_pressure_2:end_pressure_2, 'qc_Flags'] = 2
ACSM_Data.drop(ACSM_Data.loc[start_pressure_2:end_pressure_2].index, inplace=True)

start_pressure_3 = datetime.datetime(2020,3,10,10,0,00) 
end_pressure_3 = datetime.datetime(2020,3,13,12,30,00)
#ACSM_Data.loc[start_pressure_3:end_pressure_3, 'qc_Flags'] = 2
ACSM_Data.drop(ACSM_Data.loc[start_pressure_3:end_pressure_3].index, inplace=True)

start_airbeam_3 = datetime.datetime(2020,3,16,15,45,00)
end_airbeam_3 = datetime.datetime(2020,3,24,10,0,00)
#ACSM_Data.loc[start_airbeam_3:end_airbeam_3, 'qc_Flags'] = 2
ACSM_Data.drop(ACSM_Data.loc[start_airbeam_3:end_airbeam_3].index, inplace=True)

start_pressure_4 = datetime.datetime(2020,6,11,9,0,00) 
end_pressure_4 = datetime.datetime(2020,7,21,13,5,00)
ACSM_Data.loc[start_pressure_4:end_pressure_4, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_pressure_4:end_pressure_4].index, inplace=True)

start_airbeam_4 = datetime.datetime(2020,6,11,9,15,00)
end_airbeam_4 = datetime.datetime(2020,8,12,7,40,0,00)
ACSM_Data.loc[start_airbeam_4:end_airbeam_4, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_airbeam_4:end_airbeam_4].index, inplace=True)

start_airbeam_5 = datetime.datetime(2021,6,4,8,10,00)
end_airbeam_5 = datetime.datetime(2021,6,4,10,30,00)
ACSM_Data.loc[start_airbeam_5:end_airbeam_5, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_airbeam_5:end_airbeam_5].index, inplace=True)

start_airbeam_6 = datetime.datetime(2021,8,16,6,20,00)
end_airbeam_6 = datetime.datetime(2021,8,23,18,55,00)
ACSM_Data.loc[start_airbeam_6:end_airbeam_6, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_airbeam_6:end_airbeam_6].index, inplace=True)

start_pressure_5 = datetime.datetime(2021,11,9,0,0,00) 
end_pressure_5 = datetime.datetime(2022,2,7,17,22,00)
ACSM_Data.loc[start_pressure_5:end_pressure_5, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_pressure_5:end_pressure_5].index, inplace=True)

start_pressure_6 = datetime.datetime(2022,5,31,14,40,00) 
end_pressure_6 = datetime.datetime(2022,6,1,8,40,00)
ACSM_Data.loc[start_pressure_6:end_pressure_6, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_pressure_6:end_pressure_6].index, inplace=True)

start_pressure_7 = datetime.datetime(2022,7,30,0,0,00) 
end_pressure_7 = datetime.datetime(2022,8,1,14,7,00)
ACSM_Data.loc[start_pressure_7:end_pressure_7, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_pressure_7:end_pressure_7].index, inplace=True)

start_pressure_8 = datetime.datetime(2021,8,23,0,0,00) 
end_pressure_8 = datetime.datetime(2021,9,17,11,0,00)
ACSM_Data.loc[start_pressure_8:end_pressure_8, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_pressure_8:end_pressure_8].index, inplace=True)

start_pressure_9 = datetime.datetime(2022,8,10,15,0,00) 
end_pressure_9 = datetime.datetime(2022,8,12,13,0,00)
ACSM_Data.loc[start_pressure_9:end_pressure_9, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_pressure_9:end_pressure_9].index, inplace=True)

start_pressure_10 = datetime.datetime(2022,10,1,23,0,00) 
end_pressure_10 = datetime.datetime(2022,10,4,10,0,00)
ACSM_Data.loc[start_pressure_10:end_pressure_10, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_pressure_10:end_pressure_10].index, inplace=True)

start_inlet_1 = datetime.datetime(2022,8,25,11,54,00) 
end_inlet_1 = datetime.datetime(2022,10,26,12,53,00)
ACSM_Data.loc[start_inlet_1:end_inlet_1, 'qc_Flags'] = 2
#ACSM_Data.drop(ACSM_Data.loc[start_inlet_1:end_inlet_1].index, inplace=True)

start_airbeam_7 = datetime.datetime(2022,3,1,6,30,00)
end_airbeam_7 = datetime.datetime(2022,3,1,10,45,00)
#ACSM_Data.loc[start_airbeam_7:end_airbeam_7, 'qc_Flags'] = 2
ACSM_Data.drop(ACSM_Data.loc[start_airbeam_7:end_airbeam_7].index, inplace=True)

start_Cal_1 = datetime.datetime(2022,10,4,9,43,00)
end_Cal_1 = datetime.datetime(2022,10,4,15,20,00)
#ACSM_Data.loc[start_Cal_1:end_Cal_1, 'qc_Flags'] = 2
ACSM_Data.drop(ACSM_Data.loc[start_Cal_1:end_Cal_1].index, inplace=True)

start_Cal_2 = datetime.datetime(2022,10,6,8,53,00)
end_Cal_2 = datetime.datetime(2022,10,6,21,45,00)
#ACSM_Data.loc[start_Cal_2:end_Cal_2, 'qc_Flags'] = 2
ACSM_Data.drop(ACSM_Data.loc[start_Cal_2:end_Cal_2].index, inplace=True)

start_Cal_3 = datetime.datetime(2022,10,11,9,32,00)
end_Cal_3 = datetime.datetime(2022,10,11,17,56,00)
#ACSM_Data.loc[start_Cal_3:end_Cal_3, 'qc_Flags'] = 2
ACSM_Data.drop(ACSM_Data.loc[start_Cal_3:end_Cal_3].index, inplace=True)

start_Cal_4 = datetime.datetime(2021,8,16,7,30,00)
end_Cal_4 = datetime.datetime(2021,8,23,18,15,00)
#ACSM_Data.loc[start_Cal_4:end_Cal_4, 'qc_Flags'] = 2
ACSM_Data.drop(ACSM_Data.loc[start_Cal_4:end_Cal_4].index, inplace=True)

start_Cal_5 = datetime.datetime(2022,12,16,10,0,00)
end_Cal_5 = datetime.datetime(2022,12,16,17,0,00)
#ACSM_Data.loc[start_Cal_5:end_Cal_5, 'qc_Flags'] = 2
ACSM_Data.drop(ACSM_Data.loc[start_Cal_5:end_Cal_5].index, inplace=True)

ACSM_Data['qc_Flag_Chl'] = np.where( ACSM_Data['Chl (ug/m3)'] < 0.2, 2, ACSM_Data['qc_Flags'])
ACSM_Data['qc_Flag_NH4'] = np.where( ACSM_Data['NH4 (ug/m3)'] < 0.2, 2, ACSM_Data['qc_Flags'])
ACSM_Data['qc_Flag_NO3'] = np.where( ACSM_Data['NO3 (ug/m3)'] < 0.2, 2, ACSM_Data['qc_Flags'])
ACSM_Data['qc_Flag_SO4'] = np.where( ACSM_Data['SO4 (ug/m3)'] < 0.2, 2, ACSM_Data['qc_Flags'])
ACSM_Data['qc_Flag_organic'] = np.where( ACSM_Data['organic (ug/m3)'] < 0.2, 2, ACSM_Data['qc_Flags'])

ACSM_Data['qc_Flag_Chl'] = np.where( ACSM_Data['Chl (ug/m3)'] > 100, 2, ACSM_Data['qc_Flag_Chl'])
ACSM_Data['qc_Flag_NH4'] = np.where( ACSM_Data['NH4 (ug/m3)'] > 100, 2, ACSM_Data['qc_Flag_NH4'])
ACSM_Data['qc_Flag_NO3'] = np.where( ACSM_Data['NO3 (ug/m3)'] > 100, 2, ACSM_Data['qc_Flag_NO3'])
ACSM_Data['qc_Flag_SO4'] = np.where( ACSM_Data['SO4 (ug/m3)'] > 100, 2, ACSM_Data['qc_Flag_SO4'])
ACSM_Data['qc_Flag_organic'] = np.where( ACSM_Data['organic (ug/m3)'] > 100, 2, ACSM_Data['qc_Flag_organic'])
ACSM_Data = ACSM_Data.drop(columns=['qc_Flags'])

ACSM_Data['qc_Flag_Chl'] = ACSM_Data['qc_Flag_Chl'].astype(float)
ACSM_Data['qc_Flag_NH4'] = ACSM_Data['qc_Flag_NH4'].astype(float)
ACSM_Data['qc_Flag_NO3'] = ACSM_Data['qc_Flag_NO3'].astype(float)
ACSM_Data['qc_Flag_SO4'] = ACSM_Data['qc_Flag_SO4'].astype(float)
ACSM_Data['qc_Flag_organic'] = ACSM_Data['qc_Flag_organic'].astype(float)

ACSM_Data['qc_Flag_Chl'] = ACSM_Data['qc_Flag_Chl'].astype(int)
ACSM_Data['qc_Flag_NH4'] = ACSM_Data['qc_Flag_NH4'].astype(int)
ACSM_Data['qc_Flag_NO3'] = ACSM_Data['qc_Flag_NO3'].astype(int)
ACSM_Data['qc_Flag_SO4'] = ACSM_Data['qc_Flag_SO4'].astype(int)
ACSM_Data['qc_Flag_organic'] = ACSM_Data['qc_Flag_organic'].astype(int)

ACSM_Data['qc_Flag_Chl'] = ACSM_Data['qc_Flag_Chl'].astype(str)
ACSM_Data['qc_Flag_NH4'] = ACSM_Data['qc_Flag_NH4'].astype(str)
ACSM_Data['qc_Flag_NO3'] = ACSM_Data['qc_Flag_NO3'].astype(str)
ACSM_Data['qc_Flag_SO4'] = ACSM_Data['qc_Flag_SO4'].astype(str)
ACSM_Data['qc_Flag_organic'] = ACSM_Data['qc_Flag_organic'].astype(str)

#print(ACSM_Data)

plt.plot(ACSM_Data['NH4 (ug/m3)'], label='Ammonium component of ambient aerosol')
#plt.plot(ACSM_Data['Chl (ug/m3)'], label='Chlorine component of ambient aerosol')
plt.plot(ACSM_Data['NO3 (ug/m3)'], label='Nitrate component of ambient aerosol')
plt.plot(ACSM_Data['SO4 (ug/m3)'], label='Sulphate component of ambient aerosol')
plt.plot(ACSM_Data['organic (ug/m3)'], label='Organic component of ambient aerosol')
plt.legend()
plt.ylabel('abundance (ug/m3)')
plt.rc('figure', figsize=(30, 50))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
#plt.ylim(10, 30)
#plt.figure()
#plt.show()

print(str(Data_Output_Folder))
ACSM_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/ACSM/'
check_Folder = os.path.isdir(ACSM_Folder)
if not check_Folder:
    os.makedirs(ACSM_Folder)
    print("created folder : ", ACSM_Folder)
else:
    print(ACSM_Folder, "folder already exists.")

if str(date_file_label) == '201909':
    ACSM_prelim_Data = ACSM_Data[start:end_prealign_1]
    ACSM_Data = ACSM_Data[end_prealign_1:end]
    ACSM_prelim_Data.to_csv(str(ACSM_Folder) + 'ACSM_maqs_early_' + str(date_file_label) + '_non-refractory-composition' + str(status) + str(version_number) + '.1.csv')
else:
    pass

ACSM_Data.to_csv(str(ACSM_Folder) + 'ACSM_maqs_' + str(date_file_label) + '_non-refractory-aerosol-composition' + str(status) + str(version_number) + '.1.csv')

ACSM_Data['TimeDateSince'] = ACSM_Data.index-datetime.datetime(1970,1,1,0,0,00)
ACSM_Data['TimeSecondsSince'] = ACSM_Data['TimeDateSince'].dt.total_seconds()
ACSM_Data['day_year'] = pd.DatetimeIndex(ACSM_Data['TimeDateSince'].index).dayofyear
ACSM_Data['year'] = pd.DatetimeIndex(ACSM_Data['TimeDateSince'].index).year
ACSM_Data['month'] = pd.DatetimeIndex(ACSM_Data['TimeDateSince'].index).month
ACSM_Data['day'] = pd.DatetimeIndex(ACSM_Data['TimeDateSince'].index).day
ACSM_Data['hour'] = pd.DatetimeIndex(ACSM_Data['TimeDateSince'].index).hour
ACSM_Data['minute'] = pd.DatetimeIndex(ACSM_Data['TimeDateSince'].index).minute
ACSM_Data['second'] = pd.DatetimeIndex(ACSM_Data['TimeDateSince'].index).second


