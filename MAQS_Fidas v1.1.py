# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 13:27:44 2020

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
version_number = 'v1.1'
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

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/Fidas/', 'D:/FirsData/Fidas/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/Ratified_' + str(version_number) + '/', 'D:/Ratified_' + str(version_number) + '/')

pattern = str(Data_Source_Folder) + str(date_file_label) + '*_fidas_1min.txt'# Needs to be address of data location - Collect CSV files
csv_files = glob.glob(pattern)

# Create an empty list
frames = []

#  Iterate over csv_files
for csv in csv_files:
    df = pd.read_csv(csv, index_col=False, header=None, skiprows=1, usecols=[0,1,7,14,15,16,17,18,19,20,21,22])
    frames.append(df)

# Concatenate frames into a single DataFrame
fidas_Data = pd.concat(frames, sort=True)

fidas_Data.columns = ['Date','Time','Cal_error','Cn (P/cm3)','PM1 (ug/m3)','PM2.5 (ug/m3)','PM4 (ug/m3)','PM10 (ug/m3)','PMtotal (ug/m3)','Temperature (deg C)','Pressure (mbar)','Humidity (%)']#,'Heater Temperature (deg C)','Raw Channel Deviation']
#'Flow Sensor Error','Coincidence Error','Pump Error','Weatherstation Error','IADS error','Calibration Error','LED Temperature Error','Modus Error','Flow Rate (lpm)','Pump Speed (%)','Particle Velocity (m/s)','LED Temp (deg C)',
fidas_Data['Date'] = fidas_Data['Date'].astype(str)
fidas_Data['Time'] = fidas_Data['Time'].astype(str)
fidas_Data['datetime'] = fidas_Data['Date'] + ' ' + fidas_Data['Time']# added Date and time into new columns
fidas_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in fidas_Data['datetime']] #converts the dateTime format from string to python dateTime
fidas_Data.index = fidas_Data['datetime']
fidas_Data = fidas_Data.drop(columns=['Time', 'Date'])
fidas_Data = fidas_Data.groupby(pd.Grouper(key='datetime',freq=av_Freq)).mean()

fidas_Data = fidas_Data[start:end]

#combine the full month timeline with the sonic data, aligned to the time indexed.   
#fidas_Data = pd.concat([fidas_Data, TimeLineSince], axis=1)

col_List_fidasPM = list(fidas_Data.columns.values) #make new data frame and list unwanted columns that are then dropped
col_List_fidasPM.remove('Cn (P/cm3)')
col_List_fidasPM.remove('PM1 (ug/m3)')
col_List_fidasPM.remove('PM2.5 (ug/m3)')
col_List_fidasPM.remove('PM10 (ug/m3)')
col_List_fidasPM.remove('PMtotal (ug/m3)')
fidas_PM = fidas_Data.drop(columns=col_List_fidasPM)

fidas_PM['PM1 (ug/m3)']= fidas_PM['PM1 (ug/m3)'] *1000
fidas_PM['PM2.5 (ug/m3)']= fidas_PM['PM2.5 (ug/m3)'] *1000
fidas_PM['PM10 (ug/m3)']= fidas_PM['PM10 (ug/m3)'] *1000
fidas_PM['PMtotal (ug/m3)']= fidas_PM['PMtotal (ug/m3)'] *1000

fidas_PM['PM_Flag'] = np.where((fidas_Data['Cal_error'] >0),'3','1')#populate the column with condition
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM10 (ug/m3)'] >200),'3',fidas_PM['PM_Flag'])
#fidas_PM['PM_prelim_Flag'] = fidas_PM['PM_Flag'] #seperating out a preliminary flagging column
fidas_PM['PM_Flag_-6_offset'] = fidas_PM['PM_Flag'].shift(periods=-6) #setting up columns to bloc off the area around flagged data
fidas_PM['PM_Flag_-5_offset'] = fidas_PM['PM_Flag'].shift(periods=-5)
fidas_PM['PM_Flag_-4_offset'] = fidas_PM['PM_Flag'].shift(periods=-4)
fidas_PM['PM_Flag_-3_offset'] = fidas_PM['PM_Flag'].shift(periods=-3)
fidas_PM['PM_Flag_-2_offset'] = fidas_PM['PM_Flag'].shift(periods=-2)
fidas_PM['PM_Flag_-1_offset'] = fidas_PM['PM_Flag'].shift(periods=-1) 
fidas_PM['PM_Flag_+1_offset'] = fidas_PM['PM_Flag'].shift(periods=1)
fidas_PM['PM_Flag_+2_offset'] = fidas_PM['PM_Flag'].shift(periods=2)
fidas_PM['PM_Flag_+3_offset'] = fidas_PM['PM_Flag'].shift(periods=3)
fidas_PM['PM_Flag_+4_offset'] = fidas_PM['PM_Flag'].shift(periods=4)
fidas_PM['PM_Flag_+5_offset'] = fidas_PM['PM_Flag'].shift(periods=5)
fidas_PM['PM_Flag_+6_offset'] = fidas_PM['PM_Flag'].shift(periods=6)
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM_Flag_-6_offset']>'1'),fidas_PM['PM_Flag_-6_offset'],fidas_PM['PM_Flag']) #expanded flagged area integrated into original column
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM_Flag_-5_offset']>'1'),fidas_PM['PM_Flag_-5_offset'],fidas_PM['PM_Flag'])
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM_Flag_-4_offset']>'1'),fidas_PM['PM_Flag_-4_offset'],fidas_PM['PM_Flag'])
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM_Flag_-3_offset']>'1'),fidas_PM['PM_Flag_-3_offset'],fidas_PM['PM_Flag'])
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM_Flag_-2_offset']>'1'),fidas_PM['PM_Flag_-2_offset'],fidas_PM['PM_Flag'])
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM_Flag_-1_offset']>'1'),fidas_PM['PM_Flag_-1_offset'],fidas_PM['PM_Flag'])
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM_Flag_+1_offset']>'1'),fidas_PM['PM_Flag_+1_offset'],fidas_PM['PM_Flag'])
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM_Flag_+2_offset']>'1'),fidas_PM['PM_Flag_+2_offset'],fidas_PM['PM_Flag'])
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM_Flag_+3_offset']>'1'),fidas_PM['PM_Flag_+3_offset'],fidas_PM['PM_Flag'])
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM_Flag_+4_offset']>'1'),fidas_PM['PM_Flag_+4_offset'],fidas_PM['PM_Flag'])
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM_Flag_+5_offset']>'1'),fidas_PM['PM_Flag_+5_offset'],fidas_PM['PM_Flag'])
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM_Flag_+6_offset']>'1'),fidas_PM['PM_Flag_+6_offset'],fidas_PM['PM_Flag'])
list_Flag_Offset = list(fidas_PM.columns.values)
list_Flag_Offset.remove('Cn (P/cm3)')
list_Flag_Offset.remove('PM1 (ug/m3)')
list_Flag_Offset.remove('PM2.5 (ug/m3)')
list_Flag_Offset.remove('PM10 (ug/m3)')
list_Flag_Offset.remove('PMtotal (ug/m3)')
list_Flag_Offset.remove('PM_Flag')
fidas_PM = fidas_PM.drop(columns=list_Flag_Offset) #dropping newly made columns flagged data

start_Tarmac = datetime.datetime(2020,5,4,7,30,00)
end_Tarmac = datetime.datetime(2020,5,15,16,0,00)
fidas_PM.loc[start_Tarmac:end_Tarmac, 'PM_Flag'] = "4"

start_Audit1 = datetime.datetime(2019,7,19,9,50,00) # 19-07-2019 09:50 - 10:15 audit and calibration of FIDAS
end_Audit1 = datetime.datetime(2019,7,19,10,15,00)
fidas_PM.drop(fidas_PM.loc[start_Audit1:end_Audit1].index, inplace=True)

start_Audit2 = datetime.datetime(2019,8,9,7,45,00) # 09-08-2019 07:45 - 08:30 audit and calibration of FIDAS
end_Audit2 = datetime.datetime(2019,8,9,8,30,00)
fidas_PM.drop(fidas_PM.loc[start_Audit2:end_Audit2].index, inplace=True)

start_Audit3 = datetime.datetime(2019,10,2,16,40,00) #02-10-2019 16:30 - 17:00 FIDAS sensitivity calibration
end_Audit3 = datetime.datetime(2019,10,2,17,0,00)
fidas_PM.drop(fidas_PM.loc[start_Audit3:end_Audit3].index, inplace=True)

start_Audit4 = datetime.datetime(2020,3,18,9,50,00)
end_Audit4 = datetime.datetime(2020,3,18,11,35,00)
fidas_PM.drop(fidas_PM.loc[start_Audit4:end_Audit4].index, inplace=True)

start_Audit5 = datetime.datetime(2020,10,2,9,15,00)
end_Audit5 = datetime.datetime(2020,10,2,10,15,00)
fidas_PM.drop(fidas_PM.loc[start_Audit5:end_Audit5].index, inplace=True)

start_Audit6 = datetime.datetime(2021,3,30,8,55,00)
end_Audit6 = datetime.datetime(2021,3,30,10,45,00)
fidas_PM.drop(fidas_PM.loc[start_Audit6:end_Audit6].index, inplace=True)

start_Audit7 = datetime.datetime(2021,10,27,7,50,00) #audit on the 27th October
end_Audit7 = datetime.datetime(2021,10,27,9,40,00)
fidas_PM.drop(fidas_PM.loc[start_Audit7:end_Audit7].index, inplace=True)

#start_Audit8 = datetime.datetime(yyyy,mm,dd,hr,min,sec) #next audit
#end_Audit8 = datetime.datetime(yyyy,mm,dd,hr,min,sec)
#fidas_PM.drop(fidas_PM.loc[start_Audit8:end_Audit8].index, inplace=True)

start_cleanup1 = datetime.datetime(2019,1,1,0,1,00) #Site only started generating data on 19-07-2019
end_cleanup1 = datetime.datetime(2019,7,19,10,30,00)
fidas_PM.drop(fidas_PM.loc[start_cleanup1:end_cleanup1].index, inplace=True)

start_cleanup2 = datetime.datetime(2019,9,26,14,00,00) # 14.03 Fidas inlet removed for checking
end_cleanup2 = datetime.datetime(2019,9,26,14,50,00) # 14:49 FIDAS auto sampling ambient and voltage offset adjusted
fidas_PM.drop(fidas_PM.loc[start_cleanup2:end_cleanup2].index, inplace=True)

start_outage1 = datetime.datetime(2019,8,19,15,5,00) #Site shut down started due to planned power outage till the 21-08-2019
end_outage1 = datetime.datetime(2019,8,21,9,35,00)
fidas_PM.drop(fidas_PM.loc[start_outage1:end_outage1].index, inplace=True)

start_outage2 = datetime.datetime(2019,8,22,17,40,00) #Computer restarted and program not restarted till 05-09-2019
end_outage2 = datetime.datetime(2019,9,5,13,42,00)
fidas_PM.drop(fidas_PM.loc[start_outage2:end_outage2].index, inplace=True)

#start_Cal_Error_1 = datetime.datetime(2019,9,26,22,32,00) #Unknown
#end_Cal_Error_1 = datetime.datetime(2019,9,27,3,55,00)
#fidas_PM.drop(fidas_PM.loc[start_Cal_Error_1:end_Cal_Error_1].index, inplace=True)

#start_Cal_Error_2 = datetime.datetime(2019,9,28,20,39,00) #Unknown
#end_Cal_Error_2 = datetime.datetime(2019,9,29,1,38,00)
#fidas_PM.drop(fidas_PM.loc[start_Cal_Error_2:end_Cal_Error_2].index, inplace=True)

#start_Cal_Error_3 = datetime.datetime(2019,9,29,6,46,00) #Unknown
#end_Cal_Error_3 = datetime.datetime(2019,9,29,8,1,00)
#fidas_PM.drop(fidas_PM.loc[start_Cal_Error_3:end_Cal_Error_3].index, inplace=True)

fidas_PM = fidas_PM.dropna(subset=['PM1 (ug/m3)']) #drop rows with no PM data on

col_List_fidasMet = list(fidas_Data.columns.values)
col_List_fidasMet.remove('Temperature (deg C)')
col_List_fidasMet.remove('Pressure (mbar)')
col_List_fidasMet.remove('Humidity (%)')
fidas_Met = fidas_Data.drop(columns=col_List_fidasMet)
fidas_Met['Met_Flag'] = "1"
fidas_Met['Temperature (K)'] = fidas_Met['Temperature (deg C)'] + 273.15
fidas_Met = fidas_Met[fidas_Met['Pressure (mbar)'] >= 950]

plt.plot(fidas_PM['PM1 (ug/m3)'], label='PM1')
plt.plot(fidas_PM['PM2.5 (ug/m3)'], label='PM2.5')
plt.plot(fidas_PM['PM10 (ug/m3)'], label='PM10')
#plt.plot(fidas_Met['Temperature (deg C)'], label= 'Temp')
#plt.plot(fidas_Met['Pressure (mbar)'], label= 'Pres')
#plt.plot(fidas_Met['Humidity (%)'], label= 'Hum')
#plt.plot(fidas_PM['PM_Flag'], label='flag')
#plt.plot(fidas_Data['Cal_error'], label='cal_error')
plt.legend()
plt.ylabel('ug/m3')
#plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
#plt.ylim(10, 30)
#plt.figure()
plt.show()

fidas_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/Fidas/'
check_Folder = os.path.isdir(fidas_Folder)
if not check_Folder:
    os.makedirs(fidas_Folder)
    print("created folder : ", fidas_Folder)

else:
    print(fidas_Folder, "folder already exists.")

fidas_PM.to_csv(str(fidas_Folder) + 'maqs-fidas-PM_' + str(date_file_label) + '_' + str(version_number) + '.csv')
fidas_Met.to_csv(str(fidas_Folder) + 'maqs-fidas-Met_' + str(date_file_label) + '_' + str(version_number) + '.csv')

#calculate the time in seconds since 1970 for the datetime index
fidas_PM['TimeDateSince'] = fidas_PM.index-datetime.datetime(1970,1,1,0,0,00)
fidas_PM['TimeSecondsSince'] = fidas_PM['TimeDateSince'].dt.total_seconds()
fidas_PM['day_year'] = pd.DatetimeIndex(fidas_PM.index).dayofyear
fidas_PM['year'] = pd.DatetimeIndex(fidas_PM.index).year
fidas_PM['month'] = pd.DatetimeIndex(fidas_PM.index).month
fidas_PM['day'] = pd.DatetimeIndex(fidas_PM.index).day
fidas_PM['hour'] = pd.DatetimeIndex(fidas_PM.index).hour
fidas_PM['minute'] = pd.DatetimeIndex(fidas_PM.index).minute
fidas_PM['second'] = pd.DatetimeIndex(fidas_PM.index).second
#fidas_PM['year'].head()

fidas_Met['TimeDateSince'] = fidas_Met.index-datetime.datetime(1970,1,1,0,0,00)
fidas_Met['TimeSecondsSince'] = fidas_Met['TimeDateSince'].dt.total_seconds()
fidas_Met['day_year'] = pd.DatetimeIndex(fidas_Met.index).dayofyear
fidas_Met['year'] = pd.DatetimeIndex(fidas_Met.index).year
fidas_Met['month'] = pd.DatetimeIndex(fidas_Met.index).month
fidas_Met['day'] = pd.DatetimeIndex(fidas_Met.index).day
fidas_Met['hour'] = pd.DatetimeIndex(fidas_Met.index).hour
fidas_Met['minute'] = pd.DatetimeIndex(fidas_Met.index).minute
fidas_Met['second'] = pd.DatetimeIndex(fidas_Met.index).second
#fidas_PM['hour'].head()
