# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:14:40 2022

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
from datetime import date
import datetime
import shutil
import os, sys

sample_Freq = '1sec'
av_Freq = '1min' #averaging frequency required of the data
daily_Freq = '1440min'
data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v2.2' #version of the code
year_start = 2022 #input the year of study by number
month_start = 12 #input the month of study by number
default_start_day = 1 #default start date set
day_start = default_start_day
validity_status = 'Ratified' #Ratified or Unratified

status = np.where(validity_status == 'Unratified' , '_Unratified_', '_Ratified_')
today = date.today()
current_day = today.strftime("%Y%m%d")
start = datetime.datetime(year_start,month_start,day_start,0,0,0) #start time of the period 
month_After = start + dateutil.relativedelta.relativedelta(months=1)
default_end_date = month_After - timedelta(minutes=1) #last day of month more complex so established here
default_end_day = str(default_end_date.strftime("%Y")) + str(default_end_date.strftime("%m")) + str(default_end_date.strftime("%d"))
year_end = int(default_end_date.strftime("%Y")) #this converts the default_end_day into the end of time selected
month_end = int(default_end_date.strftime("%m"))
day_end = int(default_end_date.strftime("%d"))
end =datetime.datetime(year_end,month_end,day_end,23,59,59) #if new end date needed to can be changed here 
start_year_month_str = str(start.strftime("%Y")) + str(start.strftime("%m")) # convert start and end months to strings
end_year_month_str = str(end.strftime("%Y")) + str(end.strftime("%m"))
end_Date_Check = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))
date_file_label = np.where(start_year_month_str == end_year_month_str, start_year_month_str, str(start_year_month_str) + "-" + str(end_year_month_str))
#print(date_file_label) #print end date to check it is correct

prior_date_1 = start - timedelta(days=1)
prior_date_1_str = str(prior_date_1.strftime("%Y")) + str(prior_date_1.strftime("%m")) + str(prior_date_1.strftime("%d"))
prior_date_2 = start - timedelta(days=2)
prior_date_2_str = str(prior_date_2.strftime("%Y")) + str(prior_date_2.strftime("%m")) + str(prior_date_2.strftime("%d"))
later_date_1 = end + timedelta(days=1)
later_date_1_str = str(later_date_1.strftime("%Y")) + str(later_date_1.strftime("%m")) + str(later_date_1.strftime("%d"))
later_date_2 = end + timedelta(days=2)
later_date_2_str = str(later_date_2.strftime("%Y")) + str(later_date_2.strftime("%m")) + str(later_date_2.strftime("%d"))

folder = np.where((str(version_number) == 'v0.6'), 'Preliminary', str(validity_status))
print("using a " + str(folder) + "_" + str(version_number) + " folder")

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/Disdrometer/', 'D:/FirsData/Disdrometer/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(folder) + '_' + str(version_number) + '/', 'D:/' + str(folder) + '_' + str(version_number) + '/')

Month_files = str(Data_Source_Folder) + str(date_file_label) + '*_distrometer_1min' + '.txt'

Prior_File_1 = str(Data_Source_Folder) + str(prior_date_1_str) + '*_distrometer_1min' + '.txt'
Prior_File_2 = str(Data_Source_Folder) + str(prior_date_2_str) + '*_distrometer_1min' + '.txt'
Later_File_1 = str(Data_Source_Folder) + str(later_date_1_str) + '*_distrometer_1min' + '.txt'
Later_File_2 = str(Data_Source_Folder) + str(later_date_2_str) + '*_distrometer_1min' + '.txt'

distrometer_csv_files = glob.glob(Month_files) + glob.glob(Prior_File_1) + glob.glob(Prior_File_2) + glob.glob(Later_File_1) + glob.glob(Later_File_2)

if start_year_month_str == '201907':
    month_1 = str(Data_Source_Folder) + '2019070' + '*_distrometer_1min' + '.txt' 
    month_2 = str(Data_Source_Folder) + '2019071' + '*_distrometer_1min' + '.txt' 
    month_3 = str(Data_Source_Folder) + '2019072' + '*_distrometer_1min' + '.txt' 
    month_4 = str(Data_Source_Folder) + '2019073' + '*_distrometer_1min' + '.txt' 
    Later_File_1 = str(Data_Source_Folder) + str(later_date_1_str) + '*_distrometer_1min' + '.txt'
    Later_File_2 = str(Data_Source_Folder) + str(later_date_2_str) + '*_distrometer_1min' + '.txt'
    distrometer_csv_files = glob.glob(Later_File_1) + glob.glob(Later_File_2) + glob.glob(month_1) + glob.glob(month_2) + glob.glob(month_3) + glob.glob(month_4) # 
else:
    pass

distrometer_frames = []

for csv in distrometer_csv_files:
    csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv, index_col=False, header=None, skiprows=1) #, usecols=[*range(0, 74)],error_bad_lines=False, keep_default_na=False, delimiter=';'
    distrometer_frames.append(df)

# Concatenate frames into a single DataFrame
distrometer_Data = pd.concat(distrometer_frames, sort=True)

distrometer_Data=distrometer_Data[0].str.split(';', expand=True)


distrometer_Data.rename(columns={0: 'Date', 6: 'Time', 9: 'Other Precipitation Classification' , 13: 'Precipitation Classification' }, inplace=True)
distrometer_Data.rename(columns={14: 'Total Precipitation Rate (mm/hr)', 15: 'Liquid Precipitation Rate (mm/hr)', 16: 'Solid Precipitation Rate (mm/hr)', 17: 'Accumulated Precipitation (mm)'  }, inplace=True) #
distrometer_Data.rename(columns={18: 'Visibility in precipitation (m)', 19: 'Radar Reflectivity (dBZ)', 20: 'Measuring Quality (%)' }, inplace=True)
distrometer_Data.rename(columns={21: 'Maximum Diameter Hail (mm)', 22: 'Status Laser', 23: 'Static Signal' }, inplace=True)
distrometer_Data.rename(columns={24: 'Status Laser temperature (analogue)', 25: 'Status Laser temperature (digital)', 26: 'Status Laser current (analogue)' }, inplace=True)
distrometer_Data.rename(columns={27: 'Status Laser current (digital)', 28: 'Status Sensor supply', 29: 'Status Current pane heating laser head' }, inplace=True)
distrometer_Data.rename(columns={30: 'Status Current pane heating receiver head', 31: 'Status Temperature sensor', 32: 'Status Heating supply' }, inplace=True)
distrometer_Data.rename(columns={33: 'Status Current heating housing', 34: 'Status Current heating heads', 35: 'Status Current heating carriers', 36: 'Status Control output laser power' }, inplace=True)
#distrometer_Data.rename(columns={51: 'number_of_drops', 53: 'number_of_hydrometeors_below_speed_of_0.15m/s', 55: 'number_of_hydrometeors_above_speed_of_20m/s' }, inplace=True)
#distrometer_Data.rename(columns={57: 'number_of_hydrometeors_above_speed_of_20m/s', }, inplace=True)

#distrometer_Data.rename(columns={19: 'Minute Precipitation Measurement (mm)'}, inplace=True)

#distrometer_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'Conc (#/cc)', 3: 'Saturator Temperture Alert', 4: 'Condensor Temperture Alert' }, inplace=True)

#distrometer_Data = distrometer_Data.drop(columns=[2, 3, 4])
##distrometer_Data = distrometer_Data.drop(distrometer_Data.iloc[:, 46:512], inplace=True, axis=1) #distrometer_Data = distrometer_Data.drop(distrometer_Data.iloc[:, 46:50], inplace=True, axis=1)
#distrometer_Data = distrometer_Data.drop(distrometer_Data.iloc[:, 22:37], inplace=True, axis=1)

#distrometer_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'Conc (#/cc)', 3: 'Saturator Temperture Alert', 4: 'Condensor Temperture Alert' }, inplace=True)
#distrometer_Data.rename(columns={5: 'Optics Temperature Alert', 6: 'Inlet Flow Alert', 7: 'Aerosol Flow Alert', 8: 'Laser Power Alert' }, inplace=True)
#distrometer_Data.rename(columns={9: 'Liquid Reservoir Alert', 10: 'Aerosol Concentration Flag', 11: 'Calibration Alert', 18: 'CPC Cal Mode' }, inplace=True)


distrometer_Data['Date'] = distrometer_Data['Date'].astype(str)
distrometer_Data['Time'] = distrometer_Data['Time'].astype(str)
distrometer_Data['Date_length'] = distrometer_Data['Date'].str.len()
distrometer_Data['Time_length'] = distrometer_Data['Time'].str.len()
distrometer_Data=distrometer_Data[distrometer_Data.Date_length == 10]
distrometer_Data=distrometer_Data[distrometer_Data.Time_length == 8]
distrometer_Data['datetime'] = distrometer_Data['Date'] + ' ' + distrometer_Data['Time']# added Date and time into new columns
distrometer_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in distrometer_Data['datetime']] #converts the dateTime format from string to python dateTime
distrometer_Data.index = distrometer_Data['datetime']
distrometer_Data = distrometer_Data.sort_index()

start_fault_1 = datetime.datetime(2019,7,10,0,0,00) 
end_fault_1 = datetime.datetime(2019,7,10,11,0,00)
distrometer_Data.drop(distrometer_Data.loc[start_fault_1:end_fault_1].index, inplace=True)

start_fault_2 = datetime.datetime(2019,7,11,8,15,00) 
end_fault_2 = datetime.datetime(2019,7,12,0,30,00)
distrometer_Data.drop(distrometer_Data.loc[start_fault_2:end_fault_2].index, inplace=True)

start_fault_3 = datetime.datetime(2019,7,1,0,0,00) 
end_fault_3 = datetime.datetime(2019,7,4,23,59,59)
distrometer_Data.drop(distrometer_Data.loc[start_fault_3:end_fault_3].index, inplace=True)

start_fault_4 = datetime.datetime(2019,11,8,19,11,00) 
end_fault_4 = datetime.datetime(2019,11,8,19,34,59)
distrometer_Data.drop(distrometer_Data.loc[start_fault_4:end_fault_4].index, inplace=True)

distrometer_Data['Accumulated Precipitation (mm)'] = distrometer_Data['Accumulated Precipitation (mm)'].astype(float)
distrometer_Data['Accumulated Precipitation_+1_offset'] = distrometer_Data['Accumulated Precipitation (mm)'].shift(periods=1)
distrometer_Data['Accumulated Precipitation (mm) per min'] = distrometer_Data['Accumulated Precipitation (mm)'] - distrometer_Data['Accumulated Precipitation_+1_offset']

distrometer_Data = distrometer_Data.drop(columns=['Date_length','Time_length', 'Accumulated Precipitation_+1_offset']) #'Time', 'Date', 

distrometer_Data = distrometer_Data[start:end]

Midnight_Precipitation_One = distrometer_Data[['Date', 'Time', 'Accumulated Precipitation (mm)', 'datetime']]
Midnight_Precipitation_One.rename(columns={'Accumulated Precipitation (mm)': 'Midnight Precipitation (mm)' }, inplace=True)

Midnight_Precipitation_One['Date_Offset_-1'] = Midnight_Precipitation_One['Date'].shift(periods=-1)
Midnight_Precipitation_One['Date_Offset_+1'] = Midnight_Precipitation_One['Date'].shift(periods=1)
Midnight_Precipitation_One['Date_Offset_-1'] = Midnight_Precipitation_One['Date_Offset_-1'].astype(str)
Midnight_Precipitation_One['Date_Offset_+1'] = Midnight_Precipitation_One['Date_Offset_+1'].astype(str)
Midnight_Precipitation_One['Date'] = Midnight_Precipitation_One['Date'].astype(str)
Midnight_Precipitation_One['Date_Flag'] = np.where((Midnight_Precipitation_One['Date'] == Midnight_Precipitation_One['Date_Offset_-1']) & (Midnight_Precipitation_One['Date'] == Midnight_Precipitation_One['Date_Offset_+1']),2,1)
Midnight_Precipitation_One=Midnight_Precipitation_One.loc[Midnight_Precipitation_One.Date_Flag == 1] 
Midnight_Precipitation_One['Midnight Precipitation_Offset_+1'] = Midnight_Precipitation_One['Midnight Precipitation (mm)'].shift(periods=1)
Midnight_Precipitation_One['Midnight Precipitation (mm)'] = Midnight_Precipitation_One['Midnight Precipitation (mm)'].astype(float)
Midnight_Precipitation_One['Midnight Precipitation_Offset_+1'] = Midnight_Precipitation_One['Midnight Precipitation_Offset_+1'].astype(float)
Midnight_Precipitation_One['Date_Flag'] = np.where((Midnight_Precipitation_One['Date'] == Midnight_Precipitation_One['Date_Offset_+1']),1,2)
Midnight_Precipitation_One['Midnight Precipitation (mm)'] = np.where((Midnight_Precipitation_One['Midnight Precipitation_Offset_+1'] < Midnight_Precipitation_One['Midnight Precipitation (mm)']) & (Midnight_Precipitation_One['Date_Flag'] == 1), Midnight_Precipitation_One['Midnight Precipitation_Offset_+1'], Midnight_Precipitation_One['Midnight Precipitation (mm)'])
Midnight_Precipitation_One = Midnight_Precipitation_One.drop(columns=['Date','Date_Offset_+1','Date', 'Time','Date_Offset_-1', 'Midnight Precipitation_Offset_+1', 'Date_Flag'])
#Midnight_Precipitation_One.to_csv(str(Data_Output_Folder) + 'maqs-distrometer_1_' + str(date_file_label)  + str(status) + str(version_number) + '.csv')


distrometer_Data['Midnight Precipitation Value (mm)'] = np.interp(distrometer_Data['datetime'], Midnight_Precipitation_One['datetime'], Midnight_Precipitation_One['Midnight Precipitation (mm)'])
distrometer_Data['Midnight Precipitation Value (mm)'] = distrometer_Data['Midnight Precipitation Value (mm)'].astype(float)
distrometer_Data.rename(columns={'Accumulated Precipitation (mm)': 'Raw Accumulated Precipitation (mm)' }, inplace=True)
distrometer_Data['Accumulated Precipitation (mm) since midnight'] = distrometer_Data['Raw Accumulated Precipitation (mm)'] - distrometer_Data['Midnight Precipitation Value (mm)']
distrometer_Data['Precipitation Classification'] = distrometer_Data['Precipitation Classification'].str.rstrip().astype(str)  
distrometer_Data['Other Precipitation Classification'] = distrometer_Data['Other Precipitation Classification'].str.rstrip().astype(str) 
distrometer_Data.drop(distrometer_Data[(distrometer_Data['Precipitation Classification'] == '-9999')].index,inplace =True)
#distrometer_Data = distrometer_Data.drop(columns=['Precipitation Classification'])
distrometer_Data['Precipitation Classification Symbols'] = distrometer_Data['Precipitation Classification']
distrometer_Data.rename(columns={'Precipitation Classification': 'Precipitation Classification Full'}, inplace=True)

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'NP', 'No Precipitation', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RA', 'Light Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RA', 'Moderate Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RA', 'Heavy Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-UP', 'Light Unknown Precipitation', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'UP', 'Moderate Unknown Precipitation', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+UP', 'Heavy Unknown Precipitation', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-DZ', 'Light Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'DZ', 'Moderate Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+DZ', 'Heavy Drizzle', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-FZDZ', 'Light Freezing Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'FZDZ', 'Moderate Freezing Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+FZDZ', 'Heavy Freezing Drizzle', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RADZ', 'Light Drizzle with Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RADZ', 'Moderate Drizzle with Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RADZ', 'Heavy Drizzle with Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RA', 'Light Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RA', 'Moderate Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RA', 'Heavy Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-FZRA', 'Light Freezing Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'FZRA', 'Moderate Freezing Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+FZRA', 'Heavy Freezing Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RASN', 'Light Rain and/or Drizzle with Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RASN', 'Moderate Rain and/or Drizzle with Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RASN', 'Heavy Rain and/or Drizzle with Snow', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-SN', 'Light Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'SN', 'Moderate Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+SN', 'Heavy Snow', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-SG', 'Light Snow Grains', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'SG', 'Moderate Snow Grains', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+SG', 'Heavy Snow Grains', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-GS', 'Light Soft Hail', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'GS', 'Moderate Soft Hail', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+GS', 'Heavy Soft Hail', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'PE', 'Ice Pellets', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'PL', 'Ice Pellets', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'IC', 'Ice Crystals/Needles', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'GR', 'Hail', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-GR', 'Slight Hail', distrometer_Data['Precipitation Classification Full'])

distrometer_Data.rename(columns={'Precipitation Classification Full':'Precipitation Classification'}, inplace=True)

distrometer_Data['Precipitation Classification Symbols'] = distrometer_Data['Other Precipitation Classification']

distrometer_Data.rename(columns={'Other Precipitation Classification': 'Precipitation Classification Full'}, inplace=True)

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'NP', 'No Precipitation', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RA', 'Light Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RA', 'Moderate Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RA', 'Heavy Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-UP', 'Light Unknown Precipitation', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'UP', 'Moderate Unknown Precipitation', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+UP', 'Heavy Unknown Precipitation', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-DZ', 'Light Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'DZ', 'Moderate Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+DZ', 'Heavy Drizzle', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-FZDZ', 'Light Freezing Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'FZDZ', 'Moderate Freezing Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+FZDZ', 'Heavy Freezing Drizzle', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RADZ', 'Light Drizzle with Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RADZ', 'Moderate Drizzle with Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RADZ', 'Heavy Drizzle with Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RA', 'Light Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RA', 'Moderate Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RA', 'Heavy Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-FZRA', 'Light Freezing Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'FZRA', 'Moderate Freezing Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+FZRA', 'Heavy Freezing Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RASN', 'Light Rain and/or Drizzle with Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RASN', 'Moderate Rain and/or Drizzle with Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RASN', 'Heavy Rain and/or Drizzle with Snow', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-SN', 'Light Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'SN', 'Moderate Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+SN', 'Heavy Snow', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-SG', 'Light Snow Grains', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'SG', 'Moderate Snow Grains', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+SG', 'Heavy Snow Grains', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-GS', 'Light Soft Hail', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'GS', 'Moderate Soft Hail', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+GS', 'Heavy Soft Hail', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'PE', 'Ice Pellets', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'PL', 'Ice Pellets', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'IC', 'Ice Crystals/Needles', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'GR', 'Hail', distrometer_Data['Precipitation Classification Full'])

distrometer_Data.rename(columns={'Precipitation Classification Full':'Other Precipitation Classification'}, inplace=True)

#distrometer_Data['Minute Precipitation Measurement (mm)'] = distrometer_Data['Minute Precipitation Measurement (mm)'].astype(float)
#distrometer_Data['Minute Precipitation Measurement (mm)'] = np.where(distrometer_Data['Minute Precipitation Measurement (mm)']== -9.9, 0, distrometer_Data['Minute Precipitation Measurement (mm)'])

Midnight_Precipitation = distrometer_Data['Accumulated Precipitation (mm) since midnight']

distrometer_Data = distrometer_Data.drop(columns=['Midnight Precipitation Value (mm)','Precipitation Classification Symbols', 'datetime', 'Accumulated Precipitation (mm) since midnight'])

distrometer_Data['Total Precipitation Rate (mm/hr)'] = distrometer_Data['Total Precipitation Rate (mm/hr)'].astype(float)
distrometer_Data['Liquid Precipitation Rate (mm/hr)'] = distrometer_Data['Liquid Precipitation Rate (mm/hr)'].astype(float)
distrometer_Data['Solid Precipitation Rate (mm/hr)'] = distrometer_Data['Solid Precipitation Rate (mm/hr)'].astype(float)

distrometer_Data.drop(distrometer_Data[(distrometer_Data['Total Precipitation Rate (mm/hr)'] == 999.999)].index,inplace =True)
distrometer_Data.drop(distrometer_Data[(distrometer_Data['Liquid Precipitation Rate (mm/hr)'] == 999.999)].index,inplace =True)
distrometer_Data.drop(distrometer_Data[(distrometer_Data['Solid Precipitation Rate (mm/hr)'] == 999.999)].index,inplace =True)
distrometer_Data.drop(distrometer_Data[(distrometer_Data['Solid Precipitation Rate (mm/hr)'] == 999.999)].index,inplace =True)

distrometer_Data['qc_flag'] = np.where(distrometer_Data['Liquid Precipitation Rate (mm/hr)'] < 0, 3, 1)
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Solid Precipitation Rate (mm/hr)'] < 0, 3, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Liquid Precipitation Rate (mm/hr)'] > 300, 4, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Solid Precipitation Rate (mm/hr)'] > 300, 5, distrometer_Data['qc_flag'])

distrometer_Data['Status Laser'] = distrometer_Data['Status Laser'].astype(float)
distrometer_Data['Static Signal'] = distrometer_Data['Static Signal'].astype(float)
distrometer_Data['Status Laser temperature (analogue)'] = distrometer_Data['Status Laser temperature (analogue)'].astype(float)
distrometer_Data['Status Laser temperature (digital)'] = distrometer_Data['Status Laser temperature (digital)'].astype(float)
distrometer_Data['Status Laser current (analogue)'] = distrometer_Data['Status Laser current (analogue)'].astype(float)
distrometer_Data['Status Laser current (digital)'] = distrometer_Data['Status Laser current (digital)'].astype(float)
distrometer_Data['Status Sensor supply'] = distrometer_Data['Status Sensor supply'].astype(float)
distrometer_Data['Status Current pane heating laser head'] = distrometer_Data['Status Current pane heating laser head'].astype(float)
distrometer_Data['Status Current pane heating receiver head'] = distrometer_Data['Status Current pane heating receiver head'].astype(float)
distrometer_Data['Status Temperature sensor'] = distrometer_Data['Status Temperature sensor'].astype(float)
distrometer_Data['Status Heating supply'] = distrometer_Data['Status Heating supply'].astype(float)
distrometer_Data['Status Current heating housing'] = distrometer_Data['Status Current heating housing'].astype(float)
distrometer_Data['Status Current heating heads'] = distrometer_Data['Status Current heating heads'].astype(float)
distrometer_Data['Status Current heating carriers'] = distrometer_Data['Status Current heating carriers'].astype(float)
distrometer_Data['Status Control output laser power'] = distrometer_Data['Status Control output laser power'].astype(float)

distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Laser'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Static Signal'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Laser temperature (analogue)'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Laser temperature (digital)'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Laser current (analogue)'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Laser current (digital)'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Sensor supply'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Current pane heating laser head'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Current pane heating receiver head'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Temperature sensor'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Heating supply'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Current heating housing'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Current heating heads'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Current heating carriers'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Control output laser power'] == 1, 2, distrometer_Data['qc_flag'])

particles_type = 'particles' 
particles_name = 'hydrometeors'
distrometer_Data.rename(columns={51: 'Total No. of ' + str(particles_name), 53: 'No. of very slow moving ' + str(particles_name) + ' (<0.15m/s)', 55: 'No. of very fast moving ' + str(particles_name) + ' (>20m/s)', 57: 'No. of low diameter ' + str(particles_name) + ' (< 0.15mm)' }, inplace=True)
distrometer_Data['No. of low diameter ' + str(particles_name) + ' (< 0.15mm)']=distrometer_Data['No. of low diameter ' + str(particles_name) + ' (< 0.15mm)'].astype(float)

classification = 'with no hydrometeor'
first_column = 59
count_column = int(first_column)
volume_column = 60
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

classification = 'of unknown classification'
count_column = int(count_column) + 2
volume_column = int(volume_column) + 2
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

class_no = 1

while class_no < 10:
    classification = 'from Class ' + str(class_no)
    count_column = int(count_column) + 2
    volume_column = int(volume_column) + 2
    distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)
    #if class_no == 1:
        #first_column = int(count_column)
        
    if class_no == 9:
        last_column = int(volume_column) + 1
    class_no = class_no + 1

distrometer_Data.iloc[:,int(first_column):int(last_column)] =  distrometer_Data.iloc[:,int(first_column):int(last_column)].astype(float)

#print(last_column)
class_particle_data = distrometer_Data.iloc[:,int(first_column):int(last_column)]
class_particle_data.iloc[:] = class_particle_data.iloc[:].astype(float)

distrometer_Data['No. of very slow moving ' + str(particles_name) + ' (<0.15m/s)']=distrometer_Data['No. of very slow moving ' + str(particles_name) + ' (<0.15m/s)'].astype(float)
class_particle_data['No. of very slow moving ' + str(particles_name) + ' (<0.15m/s)'] = distrometer_Data['No. of very slow moving ' + str(particles_name) + ' (<0.15m/s)']

distrometer_Data['No. of very fast moving ' + str(particles_name) + ' (>20m/s)']=distrometer_Data['No. of very fast moving ' + str(particles_name) + ' (>20m/s)'].astype(float)
class_particle_data['No. of very fast moving ' + str(particles_name) + ' (>20m/s)'] = distrometer_Data['No. of very fast moving ' + str(particles_name) + ' (>20m/s)']

#distrometer_Data['No. of low diameter ' + str(particles_name) + ' (< 0.15mm)']=distrometer_Data['No. of low diameter ' + str(particles_name) + ' (< 0.15mm)'].astype(float)
#class_particle_data['No. of low diameter ' + str(particles_name) + ' (< 0.15mm)'] = distrometer_Data['No. of low diameter ' + str(particles_name) + ' (< 0.15mm)']

standard_label = 'No. of particles'
class_particle_data['Total Class Particle'] = class_particle_data[list(class_particle_data.filter(regex=str(standard_label)))].sum(axis=1)
distrometer_Data['Total No. of hydrometeors']=distrometer_Data['Total No. of hydrometeors'].astype(float)
class_particle_data['Total No. of hydrometeors'] = distrometer_Data['Total No. of hydrometeors']
distrometer_Data['Accumulated Precipitation (mm) per min']=distrometer_Data['Accumulated Precipitation (mm) per min'].astype(float)
distrometer_Data.drop(distrometer_Data[(distrometer_Data['Accumulated Precipitation (mm) per min'] <0 )].index,inplace =True)

distrometer_qc_flag = distrometer_Data.pop('qc_flag') 
thickness_of_rainfall = distrometer_Data.pop('Accumulated Precipitation (mm) per min')

rainfall_distribution = distrometer_Data.iloc[:,81:521]

rainfall_distribution['datetime'] = distrometer_Data.index
rainfall_distribution['datetime'] = rainfall_distribution['datetime'].astype(str)
rainfall_distribution['datetime'] = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in rainfall_distribution['datetime']] #converts the dateTime format from string to python dateTime
rainfall_distribution.index = rainfall_distribution['datetime']
rainfall_distribution = rainfall_distribution.sort_index()
rainfall_distribution = rainfall_distribution.drop(columns=['datetime']) 

rainfall_distribution.fillna(0, inplace=True)

if str(date_file_label) == '201911':
    rainfall_distribution.iloc[:] = rainfall_distribution.iloc[:].apply(lambda x: pd.to_numeric(x, errors='coerce'))
else:
    pass
rainfall_distribution.iloc[:] = rainfall_distribution.iloc[:].astype(float)
rainfall_distribution = rainfall_distribution.T.reset_index(drop=True).T
rainfall_distribution.columns = rainfall_distribution.columns +1

#rainfall_distribution['Total Rain Distribution'] = rainfall_distribution[:].sum(axis=1)
#rainfall_distribution['Total No. of hydrometeors'] = distrometer_Data['Total No. of hydrometeors']

class_no = 1
start_diameter_class = 0.125
class_width = 0.125

class_no = class_no + 1
next_diameter_class = float(start_diameter_class) + float(class_width)
all_diameter_classes = [float(start_diameter_class), float(next_diameter_class)]

while class_no < 22:
    class_no = class_no + 1
    next_diameter_class = float(next_diameter_class) + float(class_width) 
    all_diameter_classes.append(float(next_diameter_class))
    if class_no == 4:
       class_width = 0.25
    if class_no == 10:
       class_width = 0.5
    if class_no == 22:
       break

speed_no = 1
start_speed_class = 0
class_width = 0.2

speed_no = speed_no + 1
next_speed_class = float(start_speed_class) + float(class_width)
all_speed_classes = [float(start_speed_class), float(next_speed_class)]

while speed_no < 20:
    speed_no = speed_no + 1
    next_speed_class = next_speed_class + class_width
    next_speed_class = round((next_speed_class),1)
    all_speed_classes.append(next_speed_class)
    if speed_no == 6:
       class_width = 0.4
    if speed_no == 12:
       class_width = 0.8
    if speed_no == 19:
       class_width = 1
    if speed_no == 20:
       class_width = 10
       break

speed_labels = pd.DataFrame(np.array(rainfall_distribution.iloc[:2,:20]))
speed_labels[:] = np.nan
distribution_labels = pd.DataFrame(np.array(rainfall_distribution.iloc[:2,:22]))
distribution_labels[:] = np.nan

rainfall_labels = pd.DataFrame(np.array(rainfall_distribution.iloc[:2,:22]))
rainfall_labels[:] = np.nan
rainfall_labels = rainfall_labels.transpose()

speed_labels = speed_labels.transpose()
speed_labels = speed_labels.T.reset_index(drop=True).T
speed_labels.insert(1, 'all_speed_classes', all_speed_classes)
speed_labels = speed_labels.drop(columns=[0,1])
speed_labels['all_speed_names'] = speed_labels['all_speed_classes'].astype(str)
speed_labels['long_speed_ranges'] = speed_labels['all_speed_names'].shift(periods=-1)
speed_labels['long_speed_ranges'] = np.where(speed_labels['long_speed_ranges'].isnull() , '20.0', speed_labels['long_speed_ranges'])
speed_labels['upper speed channel limit'] = speed_labels['long_speed_ranges'].astype(float) 
speed_labels['long_speed_ranges'] = speed_labels['all_speed_names'] + ' - ' + speed_labels['long_speed_ranges'] + ' m/s'
speed_labels['all_speed_names'] = speed_labels['all_speed_classes'].astype(str)
speed_labels['all_speed_names'] = speed_labels['all_speed_names'].str.replace('.', 'p').astype(str)
speed_labels['all_speed_classes'] = speed_labels['all_speed_classes'].astype(float)


distribution_labels = distribution_labels.transpose()
distribution_labels = distribution_labels.T.reset_index(drop=True).T
distribution_labels.insert(0, 'all_diameter_classes', all_diameter_classes)
distribution_labels = distribution_labels.drop(columns=[0,1])
distribution_labels['all_diameter_names'] = distribution_labels['all_diameter_classes'].astype(str)
distribution_labels['long_diameter_ranges'] = distribution_labels['all_diameter_names'].shift(periods=-1)
distribution_labels['upper diameter channel limit'] = distribution_labels['long_diameter_ranges'].astype(float) 
distribution_labels['upper diameter channel limit'] = np.where(distribution_labels['upper diameter channel limit'].isnull() , 20, distribution_labels['upper diameter channel limit'])
distribution_labels['long_diameter_ranges'] = distribution_labels['all_diameter_names'] + ' - ' + distribution_labels['long_diameter_ranges'] + ' mm'
distribution_labels['long_diameter_ranges'] = np.where(distribution_labels['long_diameter_ranges'].isnull() , '> 8.0 mm', distribution_labels['long_diameter_ranges'])
distribution_labels['all_diameter_names'] = distribution_labels['all_diameter_names'].str.replace('.', 'p').astype(str)
distribution_labels['all_diameter_classes'] = distribution_labels['all_diameter_classes'].astype(float)

rainfall_labels['all_diameter_classes'] = distribution_labels['all_diameter_classes']
rainfall_labels['upper diameter channel limit'] = distribution_labels['upper diameter channel limit']
rainfall_labels['all_diameter_names'] = distribution_labels['all_diameter_names']
rainfall_labels['long_diameter_ranges'] = distribution_labels['long_diameter_ranges']

rainfall_labels['all_speed_classes'] = speed_labels['all_speed_classes']
rainfall_labels['upper speed channel limit'] = speed_labels['upper speed channel limit']
rainfall_labels['all_speed_names'] = speed_labels['all_speed_names']
rainfall_labels['long_speed_ranges'] = speed_labels['long_speed_ranges']
rainfall_labels = rainfall_labels.drop(columns=[0,1])

rainfall_labels['all_diameter_classes'] = rainfall_labels['all_diameter_classes'].astype(float)
rainfall_labels['all_speed_classes'] = rainfall_labels['all_speed_classes'].astype(float)


distribution_labels['all_diameter_classes'] = distribution_labels['all_diameter_classes'].astype(float)

all_diameter_classes = list(distribution_labels['all_diameter_classes'].values)
all_diameter_names = list(distribution_labels['all_diameter_names'].values)
long_diameter_range = list(distribution_labels['long_diameter_ranges'].values)
upper_diameter_channel_limit = list(distribution_labels['upper diameter channel limit'].values)

all_speed_classes = list(speed_labels['all_speed_classes'].values)
all_speed_names = list(speed_labels['all_speed_names'].values)
long_speed_range = list(speed_labels['long_speed_ranges'].values)
upper_speed_channel_limit = list(speed_labels['upper speed channel limit'].values)

diameter_classes = rainfall_labels[['all_diameter_classes', 'long_diameter_ranges']]

diameter_classes = pd.concat([diameter_classes,diameter_classes])
diameter_classes = pd.concat([diameter_classes,diameter_classes,diameter_classes,diameter_classes,diameter_classes])
diameter_classes = pd.concat([diameter_classes,diameter_classes])
diameter_classes = diameter_classes.sort_index()

diameter_classes['all_diameter_classes'] = diameter_classes['all_diameter_classes'].astype(str)
diameter_classes['long_diameter_classes'] = diameter_classes['all_diameter_classes'] + ' mm'
diameter_classes['all_diameter_classes'] = diameter_classes['all_diameter_classes'].astype(float)
long_diameter_classes = list(diameter_classes['long_diameter_classes'].values)

speed_labels = speed_labels[['all_speed_classes', 'all_speed_names', 'long_speed_ranges', 'upper speed channel limit']]
speed_labels['all_speed_classes'] = speed_labels['all_speed_classes'].astype(str)
speed_labels['long_speed_classes'] = speed_labels['all_speed_classes'] + ' m/s'
speed_labels['all_speed_classes'] = speed_labels['all_speed_classes'].astype(float)
long_speed_classes  = list(speed_labels['long_speed_classes'].values)

diameter_list_long = list(diameter_classes['long_diameter_classes'].values)
diameter_list_classes = list(diameter_classes['all_diameter_classes'].values)
diameter_range_long = list(diameter_classes['long_diameter_ranges'].values)

rainfall_distribution = pd.DataFrame(np.array(distrometer_Data.iloc[:,81:521]))

rainfall_distribution['datetime'] = distrometer_Data.index
rainfall_distribution['datetime'] = rainfall_distribution['datetime'].astype(str)
rainfall_distribution['datetime'] = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in rainfall_distribution['datetime']] #converts the dateTime format from string to python dateTime
rainfall_distribution.index = rainfall_distribution['datetime']
rainfall_distribution = rainfall_distribution.sort_index()
rainfall_distribution = rainfall_distribution.drop(columns=['datetime']) 

rainfall_distribution.fillna(0, inplace=True)
if str(date_file_label) == '201911':
    rainfall_distribution.iloc[:] = rainfall_distribution.iloc[:].apply(lambda x: pd.to_numeric(x, errors='coerce'))
else:
    pass
rainfall_distribution.iloc[:] = rainfall_distribution.iloc[:].astype(float)
rainfall_distribution = rainfall_distribution.T.reset_index(drop=True).T
rainfall_distribution.columns = rainfall_distribution.columns +1

rainfall_diameter_distribution = pd.DataFrame(np.array(rainfall_distribution))
rainfall_diameter_distribution['datetime'] = rainfall_distribution.index
rainfall_diameter_distribution['datetime'] = rainfall_diameter_distribution['datetime'].astype(str)
rainfall_diameter_distribution['datetime'] = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in rainfall_diameter_distribution['datetime']] #converts the dateTime format from string to python dateTime
rainfall_diameter_distribution.index = rainfall_diameter_distribution['datetime']
rainfall_diameter_distribution = rainfall_diameter_distribution.sort_index()
rainfall_diameter_distribution = rainfall_diameter_distribution.drop(columns=['datetime']) 
rainfall_diameter_distribution = rainfall_diameter_distribution.iloc[:,0:22] 
rainfall_diameter_distribution.iloc[:,0:22] = np.nan
rainfall_diameter_distribution.columns = all_diameter_classes

rainfall_speed_distribution = pd.DataFrame(np.array(rainfall_distribution))
rainfall_speed_distribution['datetime'] = rainfall_distribution.index
rainfall_speed_distribution['datetime'] = rainfall_speed_distribution['datetime'].astype(str)
rainfall_speed_distribution['datetime'] = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in rainfall_speed_distribution['datetime']] #converts the dateTime format from string to python dateTime
rainfall_speed_distribution.index = rainfall_speed_distribution['datetime']
rainfall_speed_distribution = rainfall_speed_distribution.sort_index()
rainfall_speed_distribution = rainfall_speed_distribution.drop(columns=['datetime'])
rainfall_speed_distribution = rainfall_speed_distribution.iloc[:,0:20].astype(float) 
rainfall_speed_distribution.iloc[:,0:20] = 0
rainfall_speed_distribution.columns = all_speed_classes
#print(rainfall_speed_distribution[:].max())

start_column = -20
final_column = 0
current_diametre_class = -1

for x in all_diameter_names:
    start_column = int(start_column) + 20
    final_column = int(final_column) + 20
    current_diameter_dist = pd.DataFrame(np.array(rainfall_distribution.iloc[:,int(start_column):int(final_column)] ))
    current_diameter_dist['datetime'] = rainfall_distribution.index
    current_diameter_dist['datetime'] = current_diameter_dist['datetime'].astype(str)
    current_diameter_dist['datetime'] = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in current_diameter_dist['datetime']] #converts the dateTime format from string to python dateTime
    current_diameter_dist.index = current_diameter_dist['datetime']
    current_diameter_dist = current_diameter_dist.sort_index()
    current_diameter_dist = current_diameter_dist.drop(columns=['datetime'])
    current_diameter_dist = current_diameter_dist.T.reset_index(drop=True).T
    current_diameter_dist.columns = all_speed_classes
    current_diametre_class += 1
    rainfall_diameter_distribution.iloc[:,int(current_diametre_class)] = current_diameter_dist[:].sum(axis=1)
    current_diameter_dist.iloc[:,0:20] = current_diameter_dist.iloc[:,0:20].astype(float) 
    rainfall_speed_distribution.iloc[:,0:20] = rainfall_speed_distribution.iloc[:,0:20] + current_diameter_dist.iloc[:,0:20]
    object_label = x
    locals()[object_label] = current_diameter_dist

#rainfall_diameter_distribution.columns = long_diameter_classes
#rainfall_speed_distribution.columns = long_speed_classes

#overall_distributions = pd.concat([rainfall_diameter_distribution,rainfall_speed_distribution])
#overall_distributions = overall_distributions.sort_index()
#overall_distributions = overall_distributions.groupby(pd.Grouper(freq=av_Freq)).mean()
#print(overall_distributions)

A = np.array(list(diameter_range_long)) # or diameter_list_classes
B = np.array(list(long_speed_range)*22) # or all_speed_classes 
C = np.array(rainfall_distribution.transpose())
D = rainfall_distribution.index 

df = pd.DataFrame(zip(A, B, C), columns=['Hydrometeor Diameter', 'Hydrometeor Speed', 'C'])

df = pd.DataFrame(data=C.T, columns=pd.MultiIndex.from_tuples(zip(A,B)), index = D)
distrometer_Distribution = df

distrometer_Data['Accumulated Precipitation (mm)'] = pd.Series(thickness_of_rainfall)
distrometer_Data['Accumulated Precipitation (mm)'] = distrometer_Data['Accumulated Precipitation (mm)'].astype(float)

distrometer_Data = distrometer_Data[['Accumulated Precipitation (mm)', 'Liquid Precipitation Rate (mm/hr)', 'Total Precipitation Rate (mm/hr)', 'Solid Precipitation Rate (mm/hr)', 'Maximum Diameter Hail (mm)', 'Total No. of hydrometeors', 'Visibility in precipitation (m)', 'Radar Reflectivity (dBZ)', 'Measuring Quality (%)']] # , 'qc_flag'

distrometer_Data.rename(columns={'Accumulated Precipitation (mm)' : 'Rain Accumulated in one minute (mm)' }, inplace=True)
distrometer_Data[:] = distrometer_Data[:].astype(float)
distrometer_Data.fillna(0, inplace=True)
distrometer_Data[:] = distrometer_Data[:].astype(float)
distrometer_Data['Total No. of hydrometeors'] = np.where(distrometer_Data['Total No. of hydrometeors'].isnull() , 0, distrometer_Data['Total No. of hydrometeors'])
distrometer_Data = distrometer_Data.drop(columns=['Maximum Diameter Hail (mm)'])

#distrometer_Data = pd.concat([distrometer_Data,distrometer_Distribution])
#distrometer_Data = distrometer_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
distrometer_Data['qc_flag'] = pd.Series(distrometer_qc_flag)
distrometer_Data['qc_flag'].fillna(1, inplace=True)
distrometer_Data['qc_flag'] = distrometer_Data['qc_flag'].astype(str)
distrometer_Distribution['qc_flag'] = distrometer_Data['qc_flag']

plt.plot(distrometer_Data['Total Precipitation Rate (mm/hr)'], label='Total Rain Rate (mm/hr)')
plt.plot(distrometer_Data['Solid Precipitation Rate (mm/hr)'], label='Solid Rain Rate (mm/hr)')
plt.plot(distrometer_Data['Liquid Precipitation Rate (mm/hr)'], label='Liquid Rain Rate (mm/hr)')
plt.legend()
plt.ylabel('mm/hr')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

Distrometer_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/Disdrometer/'
check_Folder = os.path.isdir(Distrometer_Folder)
if not check_Folder:
    os.makedirs(Distrometer_Folder)
    print("created folder : ", Distrometer_Folder)
else:
    print(Distrometer_Folder, "folder already exists.")

distrometer_Distribution.to_csv(str(Distrometer_Folder) + 'laser-precipitation-monitor_maqs_' + str(date_file_label) + '_hydrometeor-distribution'  + str(status) + str(version_number) + '.csv')

distrometer_Data.to_csv(str(Distrometer_Folder) + 'laser-precipitation-monitor_maqs_' + str(date_file_label) + '_precipitation-rates'  + str(status) + str(version_number) + '.csv')

distrometer_Data['TimeDateSince'] = distrometer_Data.index-datetime.datetime(1970,1,1,0,0,00)
distrometer_Data['TimeSecondsSince'] = distrometer_Data['TimeDateSince'].dt.total_seconds()
distrometer_Data['day_year'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).dayofyear
distrometer_Data['year'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).year
distrometer_Data['month'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).month
distrometer_Data['day'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).day
distrometer_Data['hour'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).hour
distrometer_Data['minute'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).minute
distrometer_Data['second'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).second


