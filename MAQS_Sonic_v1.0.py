# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 13:33:28 2020

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
year_start = 2020 #input the year of study
month_start = 2 #input the month of study
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

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/Sonic/', 'D:/FirsData/Sonic/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/Ratified_v1.0/', 'D:/Ratified_v1.0/')

#Load data acquired with the first file format
prior_date = start - timedelta(days=1)
date_Check = str(prior_date.strftime("%Y")) + str(prior_date.strftime("%m")) + str(prior_date.strftime("%d"))
#print(date_Check)

sonic_Data = pd.concat(map(pd.read_csv, glob.glob(str(Data_Source_Folder) + str(date_file_label) + '*_Sonic_1s.txt')))# read and concatenate the raw data

sonic_Data['Date'] = sonic_Data['Date'].astype(str)
sonic_Data['Time'] = sonic_Data[' Time'].astype(str)
sonic_Data['datetime'] = sonic_Data['Date'] + ' ' + sonic_Data['Time']# added Date and time into new columns
sonic_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in sonic_Data['datetime']] #converts the dateTime format from string to python dateTime
sonic_Data.index = sonic_Data['datetime']# sets the index to datetime
sonic_Data = sonic_Data.drop(columns=['Time', 'Date'])

m_gust= sonic_Data[' s(m/s)'].groupby(pd.Grouper(freq=av_Freq)).max() # find the max gust value in each minute before averaging the data
sonic_Data = sonic_Data.groupby(pd.Grouper(freq=av_Freq)).mean() # averages the data 
sonic_Data['m_Gust'] = pd.Series(m_gust) # add gust to dataframe

#combine the full month timeline with the sonic data, aligned to the time indexed.   
#sonic_Data = pd.concat([sonic_Data, TimeLineSince], axis=1)
#calculate the time in seconds since 1970 for the datetime index

sonic_Data['wind_Sp (m/s)'] = sonic_Data[' s(m/s)']
sonic_Data['wind_Dr (deg)'] = sonic_Data[' d(deg)']
sonic_Data['max_Gust (m/s)'] = sonic_Data['m_Gust']

sonic_Data['qc_flag_wind_Sp'] = np.where((sonic_Data['wind_Sp (m/s)'] <0), '2','1') #bad data outside operational range (0 to 50m s-1)
sonic_Data['qc_flag_wind_Sp'] = np.where((sonic_Data['wind_Sp (m/s)'] >50), '2','1') #1 - good data; 2b - bad data outside operational range (0 to 50m s-1)
#sonic_Data['qc_flag_wind_Sp'] = np.where((sonic_Data['wind_Sp (m/s)'].isnull()), '3','1') #1 - good data; 3b - suspect data measured wind speed == 0
sonic_Data['qc_flag_wind_Dr'] = np.where((sonic_Data['wind_Dr (deg)'] <0),'2','1') # 1b - good data; 2b - bad data outside operational range (0 to 360 degrees)
sonic_Data['qc_flag_wind_Dr'] = np.where((sonic_Data['wind_Dr (deg)'] >360),'2','1') # 1b - good data; 2b - bad data outside operational range (0 to 360 degrees)
#sonic_Data['qc_flag_wind_Dr'] = np.where((sonic_Data['wind_Dr (deg)'].isnull()),'3','1') # 1b - good data; 3b - suspect direction == 0; 

#sonic_Data['qc_flag_wind_Dr'] = np.where((sonic_Data.index ==0),'4','1')  # 1b - good data; 4b - suspect data time stamp error
sonic_Data = sonic_Data.dropna(subset=['wind_Sp (m/s)']) #drop rows with no wind speed data on
#%%
#housekeeping
sonic_Data = sonic_Data[:-1] # Trim the end of the dataframe

#start_cleanup1 = datetime.datetime(2019,1,1,0,1,00) #Site only started generating data on 19-07-2019
#end_cleanup1 = datetime.datetime(2019,7,3,16,16,00)
#sonic_Data.drop(sonic_Data.loc[start_cleanup1:end_cleanup1].index, inplace=True)

#start_cleanup2 = datetime.datetime(2019,9,26,14,00,00) # 14.03 Fidas inlet removed for checking
#end_cleanup2 = datetime.datetime(2019,9,26,14,50,00) # 14:49 FIDAS auto sampling ambient and voltage offset adjusted
#sonic_Data.drop(sonic_Data.loc[start_cleanup2:end_cleanup2].index, inplace=True)

#start_Audit1 = datetime.datetime(2019,7,19,9,50,00)
#end_Audit1 = datetime.datetime(2019,7,19,10,15,00)
#sonic_Data.drop(sonic_Data.loc[start_Audit1:end_Audit1].index, inplace=True)

#start_Audit2 = datetime.datetime(2019,10,2,16,40,00) #02-10-2019 16:30 - 17:00 FIDAS sensitivity calibration
#end_Audit2 = datetime.datetime(2019,10,2,17,0,00)
#sonic_Data.drop(sonic_Data.loc[start_Audit2:end_Audit2].index, inplace=True)

#start_Audit3 = datetime.datetime(2020,3,18,9,0,00)
#end_Audit3 = datetime.datetime(2020,3,18,14,0,00)
#sonic_Data.drop(sonic_Data.loc[start_Audit3:end_Audit3].index, inplace=True)

#start_Audit4 = datetime.datetime(2020,10,2,9,0,00)
#end_Audit4 = datetime.datetime(2020,10,2,12,0,00)
#sonic_Data.drop(sonic_Data.loc[start_Audit4:end_Audit4].index, inplace=True)

#start_Audit5 = datetime.datetime(2021,3,30,9,0,00)
#end_Audit5 = datetime.datetime(2021,3,30,12,0,00)
#sonic_Data.drop(sonic_Data.loc[start_Audit5:end_Audit5].index, inplace=True)

#start_Audit6 = datetime.datetime(2019,8,9,7,10,00) #audit and calibration of FIDAS
#end_Audit6 = datetime.datetime(2019,8,9,11,18,00)
#sonic_Data.drop(sonic_Data.loc[start_Audit6:end_Audit6].index, inplace=True)

#start_Tarmac = datetime.datetime(2020,5,4,7,30,00)
#end_Tarmac = datetime.datetime(2020,5,15,16,0,00)
#sonic_Data.loc[start_Tarmac:end_Tarmac, 'PM_Flag'] = "4"

start_outage1 = datetime.datetime(2019,8,19,15,5,00) #Site shut down started due to planned power outage till the 21-08-2019
end_outage1 = datetime.datetime(2019,8,21,9,35,00)
sonic_Data.drop(sonic_Data.loc[start_outage1:end_outage1].index, inplace=True)

start_outage2 = datetime.datetime(2019,8,22,17,40,00) #Computer restarted and program not restarted till 05-09-2019
end_outage2 = datetime.datetime(2019,9,5,13,42,00)
sonic_Data.drop(sonic_Data.loc[start_outage2:end_outage2].index, inplace=True)

#start_Cal_Error_1 = datetime.datetime(2019,9,26,22,32,00) #Unknown
#end_Cal_Error_1 = datetime.datetime(2019,9,27,3,55,00)
#sonic_Data.drop(sonic_Data.loc[start_Cal_Error_1:end_Cal_Error_1].index, inplace=True)

#start_Cal_Error_2 = datetime.datetime(2019,9,28,20,39,00) #Unknown
#end_Cal_Error_2 = datetime.datetime(2019,9,29,1,38,00)
#sonic_Data.drop(sonic_Data.loc[start_Cal_Error_2:end_Cal_Error_2].index, inplace=True)

#start_Cal_Error_3 = datetime.datetime(2019,9,29,6,46,00) #Unknown
#end_Cal_Error_3 = datetime.datetime(2019,9,29,8,1,00)
#sonic_Data.drop(sonic_Data.loc[start_Cal_Error_3:end_Cal_Error_3].index, inplace=True)

col_List_sonic = list(sonic_Data.columns.values) # create a list of column names
col_List_sonic.remove('wind_Sp (m/s)')
col_List_sonic.remove('qc_flag_wind_Sp')
col_List_sonic.remove('wind_Dr (deg)')
col_List_sonic.remove('max_Gust (m/s)')
col_List_sonic.remove('qc_flag_wind_Dr')
#col_List_sonic.remove('qc_Flags')
#col_List_sonic.remove('TimeSecondsSince')
#col_List_sonic.remove('day_year')
#col_List_sonic.remove('year')
#col_List_sonic.remove('month')
#col_List_sonic.remove('day')
#col_List_sonic.remove('hour')
#col_List_sonic.remove('minute')
#col_List_sonic.remove('second')
sonic_Data = sonic_Data.drop(columns=col_List_sonic) #removing unwanted columns
#%%
#plotting
plt.plot(sonic_Data['wind_Sp (m/s)'], label='Speed')
#plt.plot(sonic_Data['wind_Dr (deg)'], label='Direction')
#plt.plot(sonic_Data['max_Gust (m/s)'], label='Gust')
#plt.plot(sonic_Data['qc_flag_wind_Sp'], label='Wind Speed Flags')
#plt.plot(sonic_Data['qc_flag_wind_Dr'], label='Wind Direction Flags')

plt.legend()
plt.ylabel('mg/m3')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
#plt.ylim(10, 30)
#plt.figure()
plt.show()

sonic_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/Sonic/'
check_Folder = os.path.isdir(sonic_Folder)
if not check_Folder:
    os.makedirs(sonic_Folder)
    print("created folder : ", sonic_Folder)

else:
    print(sonic_Folder, "folder already exists.")

sonic_Data.to_csv(str(sonic_Folder) + 'maqs-sonic-Data_' + str(date_file_label) + '_v1.0.csv')


#sonic_Data = sonic_Data[start:end] #sets the data to the time length defined in MAQS_Master

#sonic_Data['qc_flag_wind_Sp'] = master['site_flags'] # creates the product specific flags. In this case it is the same as the site flags
#sonic_Data['qc_flag_wind_Dr'] = master['site_flags']
#
#master=pd.concat([master,sonic_Data], axis=1) #adds the somic data to the master dataframe 
#master.drop(master.tail(1).index,inplace=True)##drop the last line to avoid timeline 


#calculate the time in seconds since 1970 for the datetime index
sonic_Data['TimeDateSince'] = sonic_Data.index-datetime.datetime(1970,1,1,0,0,00)
sonic_Data['TimeSecondsSince'] = sonic_Data['TimeDateSince'].dt.total_seconds()
sonic_Data['day_year'] = pd.DatetimeIndex(sonic_Data.index).dayofyear
sonic_Data['year'] = pd.DatetimeIndex(sonic_Data.index).year
sonic_Data['month'] = pd.DatetimeIndex(sonic_Data.index).month
sonic_Data['day'] = pd.DatetimeIndex(sonic_Data.index).day
sonic_Data['hour'] = pd.DatetimeIndex(sonic_Data.index).hour
sonic_Data['minute'] = pd.DatetimeIndex(sonic_Data.index).minute
sonic_Data['second'] = pd.DatetimeIndex(sonic_Data.index).second
#fidas_PM['year'].head()


