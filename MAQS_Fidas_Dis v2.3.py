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
data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v2.3'
year_start = 2022 #input the year of study
month_start = 12 #input the month of study
default_start_day = 1 #default start date set
day_start = default_start_day
datatype = 'Ratified' # either Preliminary, Unratified or Ratified

start = datetime.datetime(year_start,month_start,day_start,0,0,00) #start time of the period 
month_After = start + dateutil.relativedelta.relativedelta(months=1)
default_end_date = month_After - timedelta(minutes=1) #last day of month more complex so established here

default_end_day = str(default_end_date.strftime("%Y")) + str(default_end_date.strftime("%m")) + str(default_end_date.strftime("%d"))

year_end = int(default_end_date.strftime("%Y")) #this converts the default_end_day into the end of time selected
month_end = int(default_end_date.strftime("%m"))
day_end = int(default_end_date.strftime("%d"))

end = datetime.datetime(year_end,month_end,day_end,23,59,59) #if new end date needed to can be changed here 

start_year_month_str = str(start.strftime("%Y")) + str(start.strftime("%m")) # convert start and end months to strings
end_year_month_str = str(end.strftime("%Y")) + str(end.strftime("%m"))

end_Date_Check = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))
print(end_Date_Check) #print end date to check it is correct

date_file_label = np.where(start_year_month_str == end_year_month_str, start_year_month_str, str(start_year_month_str) + "-" + str(end_year_month_str))
print(date_file_label) #print end date to check it is correct

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/Fidas/', 'D:/FirsData/Fidas/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(datatype) + '_' + str(version_number) + '/', 'D:/' + str(datatype) + '_' + str(version_number) + '/')

Month_files = str(Data_Source_Folder) + str(date_file_label) + '*_fidas_1min.txt'# Needs to be address of data location - Collect CSV files


prior_date_1 = start - dateutil.relativedelta.relativedelta(days=1)
prior_date_1_str = str(prior_date_1.strftime("%Y")) + str(prior_date_1.strftime("%m"))

prior_date_2 = start - dateutil.relativedelta.relativedelta(days=2)
prior_date_2_str = str(prior_date_2.strftime("%Y")) + str(prior_date_2.strftime("%m"))

later_date_1 = end + dateutil.relativedelta.relativedelta(days=1)
later_date_1_str = str(later_date_1.strftime("%Y")) + str(later_date_1.strftime("%m"))

later_date_2 = end + dateutil.relativedelta.relativedelta(days=2)
later_date_2_str = str(later_date_2.strftime("%Y")) + str(later_date_2.strftime("%m"))

print(later_date_2_str)

Prior_File_1 = str(Data_Source_Folder) + str(prior_date_1_str) + '*_fidas_1min.txt'
Prior_File_2 = str(Data_Source_Folder) + str(prior_date_2_str) + '*_fidas_1min.txt'
Later_File_1 = str(Data_Source_Folder) + str(later_date_1_str) + '*_fidas_1min.txt'
Later_File_2 = str(Data_Source_Folder) + str(later_date_2_str) + '*_fidas_1min.txt'
Format_file = str(Data_Source_Folder) + '202110010000_fidas_1min.txt'

csv_files = glob.glob(Format_file) + glob.glob(Month_files) + glob.glob(Prior_File_1) + glob.glob(Prior_File_2) + glob.glob(Later_File_1) + glob.glob(Later_File_2)

# Create an empty list
frames = []

#  Iterate over csv_files
for csv in csv_files:
    csv = open(csv, 'r', errors='ignore')
    df = pd.read_csv(csv, encoding= 'unicode_escape', index_col=False, header=None, error_bad_lines=False) #,  usecols=[0,1,7,14,15,16,17,18,19,20,21,22], skiprows=1
    frames.append(df)

fidas_Dist = pd.concat(frames, sort=True)

fidas_Dist.iloc[0] = fidas_Dist.iloc[0].astype(str)
fidas_Dist.iloc[0] = fidas_Dist.iloc[0].str.lstrip().astype(str) 
fidas_Dist.iloc[0] = fidas_Dist.iloc[0].str.rstrip().astype(str) 
fidas_Dist.iloc[0,25:] = fidas_Dist.iloc[0,25:] + ' um (##/cm^3)'
column_titles = fidas_Dist.iloc[0,25:]
fidas_Dist.rename(columns={0: 'Date', 1: 'Time', 2: 'Flow Sensor Error', 3: 'Coincidence Error', 4: 'Pump Error'}, inplace = True)
fidas_Dist.rename(columns={5: 'Weatherstation Error', 6: 'IADS error', 7: 'Calibration Error', 8: 'LED Temperature Error', 9: 'Modus Error'  }, inplace = True)
fidas_Dist.rename(columns={10: 'Flow Rate (lpm)', 11: 'Pump Speed (%)', 12: 'Particle Velocity (m/s)', 13: 'LED Temp (deg C)', 14: 'Cn (P/cm3)' }, inplace = True)
fidas_Dist.rename(columns={15: 'PM1 (ug/m3)', 16: 'PM2.5 (ug/m3)', 17: 'PM4 (ug/m3)', 18: 'PM10 (ug/m3)', 19: 'PMtotal (ug/m3)'  }, inplace = True) 
fidas_Dist.rename(columns={20: 'Temperature (deg C)', 21: 'Pressure (mbar)', 22: 'Humidity (%)', 23: 'Heater Temperature (deg C)', 24: 'Raw Channel Deviation'}, inplace = True)
fidas_Dist.iloc[0] = fidas_Dist.columns
fidas_Dist.iloc[0,25:] = pd.Series(column_titles)
fidas_Dist.columns = fidas_Dist.iloc[0]
fidas_Dist = fidas_Dist.drop(fidas_Dist.filter(regex="0.0 um").columns, axis=1)
#print(fidas_Dist.columns)

fidas_Dist.rename(columns={'Calibration Error': 'Cal_error' }, inplace = True)
fidas_Dist.drop(fidas_Dist[(fidas_Dist['Cal_error'] == 'Calibration Error')].index,inplace =True)
fidas_Dist.drop(fidas_Dist[(fidas_Dist['Flow Sensor Error'] == ' Flow Rate (lpm)')].index,inplace =True)

fidas_Dist.drop(fidas_Dist[(fidas_Dist['8.6596 um (##/cm^3)'].isnull()) ].index,inplace =True)

fidas_Dist = fidas_Dist.drop(fidas_Dist.filter(regex="nan um").columns, axis=1)

fidas_Dist['Date'] = fidas_Dist['Date'].astype(str)
fidas_Dist['Time'] = fidas_Dist['Time'].astype(str)
fidas_Dist['datetime'] = fidas_Dist['Date'] + ' ' + fidas_Dist['Time']# added Date and time into new columns
fidas_Dist['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in fidas_Dist['datetime']] #converts the dateTime format from string to python dateTime
fidas_Dist.index = fidas_Dist['datetime']
fidas_Dist = fidas_Dist.sort_index()
fidas_Dist = fidas_Dist.drop(columns=['Time', 'Date', 'datetime'])
fidas_Dist = fidas_Dist[start:end]

fidas_Dist[:] = fidas_Dist[:].astype(float)

fidas_Dist['PM_Flag'] = np.where((fidas_Dist['Pump Error'] != 0), 2, 1)
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['Flow Sensor Error'] != 0),2,fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['Coincidence Error'] != 0),2,fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['IADS error'] != 0),2,fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['Cal_error'] != 0),2,fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['LED Temperature Error'] != 0),2,fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['Modus Error'] != 0),2,fidas_Dist['PM_Flag'])

fidas_Dist['Met_Flag'] = np.where((fidas_Dist['Weatherstation Error'] != 0),2, 1)

fidas_Dist = fidas_Dist.drop(columns=['Pump Error', 'Flow Sensor Error', 'Coincidence Error', 'Weatherstation Error'])

fidas_Dist = fidas_Dist.drop(columns=[ 'Cal_error','LED Temperature Error', 'Modus Error','IADS error'])
fidas_Dist = fidas_Dist.drop(columns=['Flow Rate (lpm)', 'Pump Speed (%)', 'Particle Velocity (m/s)', 'LED Temp (deg C)'])
fidas_Dist = fidas_Dist.drop(columns=['Heater Temperature (deg C)', 'Raw Channel Deviation'])

fidas_Dist['PM1 (ug/m3)']= fidas_Dist['PM1 (ug/m3)'] *1000
fidas_Dist['PM2.5 (ug/m3)']= fidas_Dist['PM2.5 (ug/m3)'] *1000
fidas_Dist['PM10 (ug/m3)']= fidas_Dist['PM10 (ug/m3)'] *1000
fidas_Dist['PMtotal (ug/m3)']= fidas_Dist['PMtotal (ug/m3)'] *1000

fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM10 (ug/m3)'] >250), 3, fidas_Dist['PM_Flag'])

fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM10 (ug/m3)'] > fidas_Dist['PMtotal (ug/m3)']), 2, fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM2.5 (ug/m3)'] > fidas_Dist['PM10 (ug/m3)']), 2, fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM1 (ug/m3)'] > fidas_Dist['PM2.5 (ug/m3)']), 2, fidas_Dist['PM_Flag'])

fidas_Dist['PM_Flag'] = np.where((fidas_Dist['Cn (P/cm3)'] <= 0),2,fidas_Dist['PM_Flag']) # general PM flag is used because this may affect calculations of the overall PM levels
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM1 (ug/m3)'] <= 0),2,fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM2.5 (ug/m3)'] <= 0),2,fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM10 (ug/m3)'] <= 0),2,fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PMtotal (ug/m3)'] <= 0),2,fidas_Dist['PM_Flag'])

start_Tarmac = datetime.datetime(2020,5,4,7,30,00)
end_Tarmac = datetime.datetime(2020,5,15,16,0,00)
fidas_Dist.loc[start_Tarmac:end_Tarmac, 'PM_Flag'] = 2

start_Audit1 = datetime.datetime(2019,7,19,9,50,00) # 19-07-2019 09:50 - 10:15 audit and calibration of FIDAS
end_Audit1 = datetime.datetime(2019,7,19,10,15,00)
fidas_Dist.loc[start_Audit1:end_Audit1, 'PM_Flag'] = 2

start_Audit2 = datetime.datetime(2019,8,9,7,45,00) # 09-08-2019 07:45 - 08:30 audit and calibration of FIDAS
end_Audit2 = datetime.datetime(2019,8,9,8,30,00)
fidas_Dist.loc[start_Audit2:end_Audit2, 'PM_Flag'] = 2

start_Audit3 = datetime.datetime(2019,10,2,16,40,00) #02-10-2019 16:30 - 17:00 FIDAS sensitivity calibration
end_Audit3 = datetime.datetime(2019,10,2,17,0,00)
fidas_Dist.loc[start_Audit3:end_Audit3, 'PM_Flag'] = 2

start_Audit4 = datetime.datetime(2020,3,18,11,00,00)
end_Audit4 = datetime.datetime(2020,3,18,11,35,00)
fidas_Dist.loc[start_Audit4:end_Audit4, 'PM_Flag'] = 2

start_Audit5 = datetime.datetime(2020,10,2,9,15,00)
end_Audit5 = datetime.datetime(2020,10,2,10,15,00)
fidas_Dist.loc[start_Audit5:end_Audit5, 'PM_Flag'] = 2

start_Audit6 = datetime.datetime(2021,3,30,8,55,00)
end_Audit6 = datetime.datetime(2021,3,30,10,45,00)
fidas_Dist.loc[start_Audit6:end_Audit6, 'PM_Flag'] = 2

start_Audit7 = datetime.datetime(2021,10,27,9,15,00) #audit on the 27th October
end_Audit7 = datetime.datetime(2021,10,27,10,15,00)
fidas_Dist.loc[start_Audit7:end_Audit7, 'PM_Flag'] = 2
fidas_Dist.drop(fidas_Dist.loc[start_Audit7:end_Audit7].index, inplace=True)

start_Audit8 = datetime.datetime(2022,5,27,9,0,00) #next audit
end_Audit8 = datetime.datetime(2022,5,27,9,1,00)
fidas_Dist.drop(fidas_Dist.loc[start_Audit8:end_Audit8].index, inplace=True)

start_error_1 = datetime.datetime(2020,4,23,14,30,00) #audit on the 27th October
end_error_1 = datetime.datetime(2020,4,23,18,30,00)
fidas_Dist.loc[start_error_1:end_error_1, 'PM_Flag'] = 2

start_error_2 = datetime.datetime(2020,5,11,10,40,00) #audit on the 27th October
end_error_2 = datetime.datetime(2020,5,11,11,40,00)
fidas_Dist.loc[start_error_2:end_error_2, 'PM_Flag'] = 2

start_error_3 = datetime.datetime(2021,2,2,19,10,00) #audit on the 27th October
end_error_3 = datetime.datetime(2021,2,2,20,20,00)
fidas_Dist.loc[start_error_3:end_error_3, 'PM_Flag'] = 2


start_cleanup1 = datetime.datetime(2019,1,1,0,1,00) #Site only started generating data on 19-07-2019
end_cleanup1 = datetime.datetime(2019,7,19,10,30,00)
fidas_Dist.drop(fidas_Dist.loc[start_cleanup1:end_cleanup1].index, inplace=True)

start_cleanup2 = datetime.datetime(2019,9,26,14,00,00) # 14.03 Fidas inlet removed for checking
end_cleanup2 = datetime.datetime(2019,9,26,14,50,00) # 14:49 FIDAS auto sampling ambient and voltage offset adjusted
fidas_Dist.drop(fidas_Dist.loc[start_cleanup2:end_cleanup2].index, inplace=True)

start_outage1 = datetime.datetime(2019,8,19,15,5,00) #Site shut down started due to planned power outage till the 21-08-2019
end_outage1 = datetime.datetime(2019,8,21,9,35,00)
fidas_Dist.drop(fidas_Dist.loc[start_outage1:end_outage1].index, inplace=True)

start_outage2 = datetime.datetime(2019,8,22,17,40,00) #Computer restarted and program not restarted till 05-09-2019
end_outage2 = datetime.datetime(2019,9,5,13,42,00)
fidas_Dist.drop(fidas_Dist.loc[start_outage2:end_outage2].index, inplace=True)

start_outage1 = datetime.datetime(2019,8,19,15,5,00) #Site shut down started due to planned power outage till the 21-08-2019
end_outage1 = datetime.datetime(2019,8,21,9,35,00)
fidas_Dist.drop(fidas_Dist.loc[start_outage1:end_outage1].index, inplace=True)

start_outage2 = datetime.datetime(2019,8,22,17,40,00) #Computer restarted and program not restarted till 05-09-2019
end_outage2 = datetime.datetime(2019,9,5,13,42,00)
fidas_Dist.drop(fidas_Dist.loc[start_outage2:end_outage2].index, inplace=True)

start_filter_change = datetime.datetime(2022,5,4,8,40,00) #08:48 Hepa Filter on Fidas (switched to cal mode)
end_filter_change = datetime.datetime(2022,5,4,9,15,00)
fidas_Dist.drop(fidas_Dist.loc[start_filter_change:end_filter_change].index, inplace=True)

start_dust_1 = datetime.datetime(2022,5,4,10,54,00) #08:48 Hepa Filter on Fidas (switched to cal mode)
end_dust_1 = datetime.datetime(2022,5,4,11,5,00)
fidas_Dist.drop(fidas_Dist.loc[start_dust_1:end_dust_1].index, inplace=True)

start_filter_2 = datetime.datetime(2022,4,7,9,55,00) 
end_filter_2 = datetime.datetime(2022,4,7,10,10,00)
fidas_Dist.drop(fidas_Dist.loc[start_filter_2:end_filter_2].index, inplace=True)

start_filter_3 = datetime.datetime(2022,7,8,11,50,00) #08:48 Hepa Filter on Fidas (switched to cal mode)
end_filter_3 = datetime.datetime(2022,7,8,12,55,00)
fidas_Dist.drop(fidas_Dist.loc[start_filter_3:end_filter_3].index, inplace=True)

start_dust_3 = datetime.datetime(2022,8,9,11,33,00) #08:48 Hepa Filter on Fidas (switched to cal mode)
end_dust_3 = datetime.datetime(2022,8,9,12,5,00)
fidas_Dist.drop(fidas_Dist.loc[start_dust_3:end_dust_3].index, inplace=True)

start_data_drop_1 = datetime.datetime(2022,3,1,9,0,00) #FIDAS has failed to recognise its flow meter,
end_data_drop_1 = datetime.datetime(2022,3,29,16,15,00)#FIDAS replacement attached
fidas_Dist.drop(fidas_Dist.loc[start_data_drop_1:end_data_drop_1].index, inplace=True)

start_data_drop_2 = datetime.datetime(2022,7,8,11,50,00) #FIDAS has returned and temporary one removed
end_data_drop_2 = datetime.datetime(2022,7,8,13,40,00)#FIDAS instrument reattached
fidas_Dist.drop(fidas_Dist.loc[start_data_drop_2:end_data_drop_2].index, inplace=True)


#fidas_PM['PM_prelim_Flag'] = fidas_PM['PM_Flag'] #seperating out a preliminary flagging column
fidas_Dist['PM_Flag_-6_offset'] = fidas_Dist['PM_Flag'].shift(periods=-6) #setting up columns to bloc off the area around flagged data
fidas_Dist['PM_Flag_-5_offset'] = fidas_Dist['PM_Flag'].shift(periods=-5)
fidas_Dist['PM_Flag_-4_offset'] = fidas_Dist['PM_Flag'].shift(periods=-4)
fidas_Dist['PM_Flag_-3_offset'] = fidas_Dist['PM_Flag'].shift(periods=-3)
fidas_Dist['PM_Flag_-2_offset'] = fidas_Dist['PM_Flag'].shift(periods=-2)
fidas_Dist['PM_Flag_-1_offset'] = fidas_Dist['PM_Flag'].shift(periods=-1) 
fidas_Dist['PM_Flag_+1_offset'] = fidas_Dist['PM_Flag'].shift(periods=1)
fidas_Dist['PM_Flag_+2_offset'] = fidas_Dist['PM_Flag'].shift(periods=2)
fidas_Dist['PM_Flag_+3_offset'] = fidas_Dist['PM_Flag'].shift(periods=3)
fidas_Dist['PM_Flag_+4_offset'] = fidas_Dist['PM_Flag'].shift(periods=4)
fidas_Dist['PM_Flag_+5_offset'] = fidas_Dist['PM_Flag'].shift(periods=5)
fidas_Dist['PM_Flag_+6_offset'] = fidas_Dist['PM_Flag'].shift(periods=6)
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM_Flag_-6_offset']>1),fidas_Dist['PM_Flag_-6_offset'],fidas_Dist['PM_Flag']) #expanded flagged area integrated into original column
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM_Flag_-5_offset']>1),fidas_Dist['PM_Flag_-5_offset'],fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM_Flag_-4_offset']>1),fidas_Dist['PM_Flag_-4_offset'],fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM_Flag_-3_offset']>1),fidas_Dist['PM_Flag_-3_offset'],fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM_Flag_-2_offset']>1),fidas_Dist['PM_Flag_-2_offset'],fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM_Flag_-1_offset']>1),fidas_Dist['PM_Flag_-1_offset'],fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM_Flag_+1_offset']>1),fidas_Dist['PM_Flag_+1_offset'],fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM_Flag_+2_offset']>1),fidas_Dist['PM_Flag_+2_offset'],fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM_Flag_+3_offset']>1),fidas_Dist['PM_Flag_+3_offset'],fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM_Flag_+4_offset']>1),fidas_Dist['PM_Flag_+4_offset'],fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM_Flag_+5_offset']>1),fidas_Dist['PM_Flag_+5_offset'],fidas_Dist['PM_Flag'])
fidas_Dist['PM_Flag'] = np.where((fidas_Dist['PM_Flag_+6_offset']>1),fidas_Dist['PM_Flag_+6_offset'],fidas_Dist['PM_Flag'])

fidas_Dist = fidas_Dist.drop(columns=['PM_Flag_-6_offset','PM_Flag_-5_offset', 'PM_Flag_-4_offset', 'PM_Flag_-3_offset','PM_Flag_-2_offset', 'PM_Flag_-1_offset'])
fidas_Dist = fidas_Dist.drop(columns=['PM_Flag_+6_offset','PM_Flag_+5_offset', 'PM_Flag_+4_offset', 'PM_Flag_+3_offset','PM_Flag_+2_offset', 'PM_Flag_+1_offset'])


fidas_Dist['Distr_Flag'] = fidas_Dist['PM_Flag'] #fidas_Dist.rename(columns={'PM_Flag': 'Distr_Flag'}, inplace=True)

fidas_PM1 = fidas_Dist.pop('PM1 (ug/m3)') 
fidas_PM2p5 = fidas_Dist.pop('PM2.5 (ug/m3)') 
fidas_PM4 = fidas_Dist.pop('PM4 (ug/m3)') 
fidas_PM10 = fidas_Dist.pop('PM10 (ug/m3)') 
fidas_PM_flag = fidas_Dist.pop('PM_Flag') 
fidas_Dist['PM1 (ug/m3)'] = fidas_PM1 
fidas_Dist['PM2.5 (ug/m3)'] = fidas_PM2p5
fidas_Dist['PM4 (ug/m3)'] = fidas_PM4
fidas_Dist['PM10 (ug/m3)'] = fidas_PM10
fidas_Dist['PM_Flag'] = fidas_PM_flag

fidas_Temp = fidas_Dist.pop('Temperature (deg C)') 
fidas_Pressure = fidas_Dist.pop('Pressure (mbar)') 
fidas_Humidity = fidas_Dist.pop('Humidity (%)') 
fidas_met_flag = fidas_Dist.pop('Met_Flag') 
fidas_Dist['Temperature (deg C)'] = fidas_Temp 
fidas_Dist['Pressure (mbar)'] = fidas_Pressure 
fidas_Dist['Humidity (%)'] = fidas_Humidity
fidas_Dist['Met_Flag'] = fidas_met_flag

fidas_Data = fidas_Dist[:]

fidas_Dist = fidas_Dist.drop(columns=['PM1 (ug/m3)','PM2.5 (ug/m3)', 'PM4 (ug/m3)', 'PM10 (ug/m3)','PMtotal (ug/m3)','PM_Flag'])
fidas_Dist = fidas_Dist.drop(columns=['Temperature (deg C)','Pressure (mbar)', 'Humidity (%)','Met_Flag'])

#print(fidas_Dist.columns)

fidas_Dist[:]=fidas_Dist[:].astype(float)

fidas_Dist_Flag = fidas_Dist['Distr_Flag'].groupby(pd.Grouper(freq=av_Freq)).max()
fidas_Particle_Number = fidas_Dist['Cn (P/cm3)'].groupby(pd.Grouper(freq=av_Freq)).mean()
fidas_Dist = fidas_Dist.groupby(pd.Grouper(freq=av_Freq)).mean()

fidas_Dist = fidas_Dist.drop(columns=['Cn (P/cm3)', 'Distr_Flag'])

fidas_Dist.iloc[:] = fidas_Dist.iloc[:].astype(float)
#fidas_Dist.iloc[:] = fidas_Dist.iloc[:].replace(0, np.nan)

# Find the columns where each value is null
empty_cols = [col for col in fidas_Dist.columns if fidas_Dist[col].isnull().all()]
# Drop these columns from the dataframe
fidas_Dist.drop(empty_cols,
        axis=1,
        inplace=True)

fidas_Dist.iloc[:] = fidas_Dist.iloc[:].replace(np.nan, 0)

first_column = int(6)
last_column = len(fidas_Dist.columns)

#print(fidas_Dist.iloc[:,first_column:last_column])

fidas_Dist['Cn (P/cm3)'] = pd.Series(fidas_Particle_Number)
fidas_Dist['Distr_Flag'] = pd.Series(fidas_Dist_Flag)

fidas_Dist['Sum (P/cm3)'] = fidas_Dist[0:].sum(axis=1)

fidas_Dist['Distr_Flag'] = pd.Series(fidas_Dist_Flag)

fidas_Cn_Total = fidas_Dist.pop('Cn (P/cm3)')
#fidas_PM_Total = fidas_Dist.pop('PMtotal (ug/m3)')
fidas_Dist_Flag = fidas_Dist.pop('Distr_Flag')

fidas_Dist['Cn (P/cm3)'] = fidas_Cn_Total
#fidas_Dist['PMtotal (ug/m3)'] = fidas_PM_Total
fidas_Dist['Distr_Flag'] = fidas_Dist_Flag 

#df['Sum']=df[col_list]. sum(axis=1)

fidas_Dist['Distr_Flag'] = np.where( ((fidas_Dist['Sum (P/cm3)'] ==0) | (fidas_Dist['Sum (P/cm3)'] ==3)) , 3, fidas_Dist['Distr_Flag'])

fidas_Dist.drop(fidas_Dist[(fidas_Dist['Sum (P/cm3)'] ==0 )].index,inplace =True)
fidas_Dist.drop(fidas_Dist[(fidas_Dist['Sum (P/cm3)'] ==3 )].index,inplace =True)
fidas_Dist.drop(fidas_Dist[(fidas_Dist['Cn (P/cm3)'] ==0 )].index,inplace =True)
fidas_Dist.drop(fidas_Dist[(fidas_Dist['Cn (P/cm3)'].isnull() )].index,inplace =True)

fidas_Dist['Distr_Flag'] = fidas_Dist['Distr_Flag'].astype(float)
fidas_Dist['Distr_Flag'] = fidas_Dist['Distr_Flag'].astype(int)
fidas_Dist['Distr_Flag'] = fidas_Dist['Distr_Flag'].astype(str)

fidas_Dis_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/Fidas_Distribution/'
check_Folder = os.path.isdir(fidas_Dis_Folder)
if not check_Folder:
    os.makedirs(fidas_Dis_Folder)
    print("created folder : ", fidas_Dis_Folder)

else:
    print(fidas_Dis_Folder, "folder already exists.")

#plt.plot(fidas_Dist['Cn (P/cm3)'], label='Particle No')
#plt.legend()
#plt.ylabel('P/cm3')
#plt.rc('figure', figsize=(60, 100))
#font = {'family' : 'normal',
#        'weight' : 'bold',
#        'size'   : 12}

#plt.rc('font', **font)
#plt.ylim(10, 30)
#plt.figure()
#plt.show()


FIDAS_serial_number_1 = '9380'
FIDAS_cal_cert_1 = 'https://github.com/redoverit/OSCA/blob/main/FIDAS%20calibration%20cert.pdf'

FIDAS_serial_number_2 = '6825'
FIDAS_cal_cert_2 = 'unknown'

original_date_file_label = date_file_label

fidas_Dist = fidas_Dist.drop(columns=['0.1 um (##/cm^3)','0.1075 um (##/cm^3)', '0.1155 um (##/cm^3)','0.1241 um (##/cm^3)', '0.1334 um (##/cm^3)', '0.1433 um (##/cm^3)', 'Sum (P/cm3)']) # 

if start_year_month_str == '202203':
    changeover_date_1 = datetime.datetime(2022,3,29,15,50,00)
    fidas_Dist_Perm = fidas_Dist[start:changeover_date_1]
    fidas_Dist_Temp = fidas_Dist[changeover_date_1:end]
    date_file_label = '20220301'
    extra_file_label = '20220329-20220331'
    print(date_file_label)
    
    fidas_Dist_Perm.to_csv(str(fidas_Dis_Folder) + 'fidas_maqs_' + str(date_file_label) + '_PM-Distribution_'+ str(datatype) + '_' + str(version_number) + '.csv')
    fidas_Dist_Temp.to_csv(str(fidas_Dis_Folder) + 'fidas_maqs_' + str(extra_file_label) + '_PM-Distribution_' + str(datatype) + '_' + str(version_number) + '.csv')
    
    FIDAS_PM_serial_number = FIDAS_serial_number_1
    FIDAS_PM_cal_cert = FIDAS_cal_cert_1
    
    fidas_Dist = fidas_Dist_Perm
    fidas_Dist['TimeDateSince'] = fidas_Dist.index-datetime.datetime(1970,1,1,0,0,00)#calculate the time in seconds since 1970 for the datetime index
    fidas_Dist['TimeSecondsSince'] = fidas_Dist['TimeDateSince'].dt.total_seconds()
    fidas_Dist['day_year'] = pd.DatetimeIndex(fidas_Dist.index).dayofyear
    fidas_Dist['year'] = pd.DatetimeIndex(fidas_Dist.index).year
    fidas_Dist['month'] = pd.DatetimeIndex(fidas_Dist.index).month
    fidas_Dist['day'] = pd.DatetimeIndex(fidas_Dist.index).day
    fidas_Dist['hour'] = pd.DatetimeIndex(fidas_Dist.index).hour
    fidas_Dist['minute'] = pd.DatetimeIndex(fidas_Dist.index).minute
    fidas_Dist['second'] = pd.DatetimeIndex(fidas_Dist.index).second


    fidas_Dist_labels = fidas_Dist.iloc[0:1,0:(int(last_column)-int(first_column))]
    fidas_Dist_labels = fidas_Dist_labels.transpose()
    fidas_Dist_labels.iloc[:,0] = fidas_Dist_labels.index
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels.index
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='2018').columns, axis=1)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='2019').columns, axis=1)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='202').columns, axis=1)


    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip('(##/cm^3)').astype(str)
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip('um ').astype(str)
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.lstrip().astype(str)  
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip().astype(str)  
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].astype(float)
    Smallest_Aerosol = fidas_Dist_labels['Particle Size'].min()
    Largest_Aerosol = fidas_Dist_labels['Particle Size'].max()
    fidas_Dist_labels = fidas_Dist_labels.transpose()

    fidas_Dist_labels.drop(fidas_Dist_labels[(fidas_Dist_labels.iloc[:,0] == 'Particle Size')].index,inplace =True)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='Particle Size').columns, axis=1)

    fidas_Dist = pd.concat([fidas_Dist_labels, fidas_Dist])
    fidas_Dist.columns = np.where( fidas_Dist.iloc[0,:].isnull() , fidas_Dist.columns, fidas_Dist.iloc[0,:])
    fidas_Dist.drop(fidas_Dist[(fidas_Dist['hour'].isnull() )].index,inplace =True)
    fidas_Dist = fidas_Dist.drop(fidas_Dist.filter(regex='Particle Size').columns, axis=1)
    fidas_Dist = fidas_Dist.sort_index()

    fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))] = fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))].astype(float)

    fidas_Distribution_graph = fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))]

    #graph_Freq = '5min'
    #fidas_Distribution_graph = fidas_Distribution_graph.groupby(pd.Grouper(freq=graph_Freq)).mean()

    columns= list(range(0,(int(last_column)-int(first_column))))


    dates = fidas_Distribution_graph.index # setting x-axis
    diameters = fidas_Distribution_graph.columns # setting y-axis
    stride = 10                                                 #change stride to change averaging period
    dates_subset = dates[::stride]
    size_matrix = np.zeros((len(columns), dates_subset.size))
    # align the particle size columns as rows into the size matrix
    for ind, col in enumerate(columns):    
        size_matrix[ind,:] = fidas_Distribution_graph.iloc[::stride, col]

    x = dates_subset
    y = diameters
    z_min, z_max = size_matrix[:].min(), size_matrix[:].max()
    z = size_matrix[:]

    fig, ax = plt.subplots()
    myplot = ax.pcolormesh(x, y, z, cmap='RdYlBu_r', vmin=z_min, vmax=z_max)
    ax.set_title('FIDAS-particle distribution')
    plt.ylabel('nm')
    plt.xlabel('Date')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}

    plt.rc('font', **font)
    plt.colorbar(myplot)
    plt.show
    ()
    
    EXTRA_PM_serial_number = FIDAS_serial_number_2
    EXTRA_PM_cal_cert = FIDAS_cal_cert_2
    
    extra_fidas_Dist = fidas_Dist_Temp
    extra_fidas_Dist['TimeDateSince'] = extra_fidas_Dist.index-datetime.datetime(1970,1,1,0,0,00)#calculate the time in seconds since 1970 for the datetime index
    extra_fidas_Dist['TimeSecondsSince'] = extra_fidas_Dist['TimeDateSince'].dt.total_seconds()
    extra_fidas_Dist['day_year'] = pd.DatetimeIndex(extra_fidas_Dist.index).dayofyear
    extra_fidas_Dist['year'] = pd.DatetimeIndex(extra_fidas_Dist.index).year
    extra_fidas_Dist['month'] = pd.DatetimeIndex(extra_fidas_Dist.index).month
    extra_fidas_Dist['day'] = pd.DatetimeIndex(extra_fidas_Dist.index).day
    extra_fidas_Dist['hour'] = pd.DatetimeIndex(extra_fidas_Dist.index).hour
    extra_fidas_Dist['minute'] = pd.DatetimeIndex(extra_fidas_Dist.index).minute
    extra_fidas_Dist['second'] = pd.DatetimeIndex(extra_fidas_Dist.index).second


    fidas_Dist_labels = extra_fidas_Dist.iloc[0:1,0:(int(last_column)-int(first_column))]
    fidas_Dist_labels = fidas_Dist_labels.transpose()
    fidas_Dist_labels.iloc[:,0] = fidas_Dist_labels.index
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels.index
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='2018').columns, axis=1)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='2019').columns, axis=1)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='202').columns, axis=1)


    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip('(##/cm^3)').astype(str)
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip('um ').astype(str)
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.lstrip().astype(str)  
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip().astype(str)  
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].astype(float)
    Smallest_Aerosol = fidas_Dist_labels['Particle Size'].min()
    Largest_Aerosol = fidas_Dist_labels['Particle Size'].max()
    fidas_Dist_labels = fidas_Dist_labels.transpose()

    fidas_Dist_labels.drop(fidas_Dist_labels[(fidas_Dist_labels.iloc[:,0] == 'Particle Size')].index,inplace =True)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='Particle Size').columns, axis=1)

    extra_fidas_Dist = pd.concat([fidas_Dist_labels, extra_fidas_Dist])
    extra_fidas_Dist.columns = np.where( extra_fidas_Dist.iloc[0,:].isnull() , extra_fidas_Dist.columns, extra_fidas_Dist.iloc[0,:])
    extra_fidas_Dist.drop(extra_fidas_Dist[(extra_fidas_Dist['hour'].isnull() )].index,inplace =True)
    extra_fidas_Dist = extra_fidas_Dist.drop(extra_fidas_Dist.filter(regex='Particle Size').columns, axis=1)
    extra_fidas_Dist = extra_fidas_Dist.sort_index()

    extra_fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))] = extra_fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))].astype(float)

    fidas_Distribution_graph = extra_fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))] 

    #graph_Freq = '5min'
    #fidas_Distribution_graph = fidas_Distribution_graph.groupby(pd.Grouper(freq=graph_Freq)).mean()

    columns= list(range(0,(int(last_column)-int(first_column))))


    dates = fidas_Distribution_graph.index # setting x-axis
    diameters = fidas_Distribution_graph.columns # setting y-axis
    stride = 10                                                 #change stride to change averaging period
    dates_subset = dates[::stride]
    size_matrix = np.zeros((len(columns), dates_subset.size))
    # align the particle size columns as rows into the size matrix
    for ind, col in enumerate(columns):    
        size_matrix[ind,:] = fidas_Distribution_graph.iloc[::stride, col]

    x = dates_subset
    y = diameters
    z_min, z_max = size_matrix[:].min(), size_matrix[:].max()
    z = size_matrix[:]

    fig, ax = plt.subplots()
    myplot = ax.pcolormesh(x, y, z, cmap='RdYlBu_r', vmin=z_min, vmax=z_max)
    ax.set_title('FIDAS-particle distribution')
    plt.ylabel('nm')
    plt.xlabel('Date')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}

    plt.rc('font', **font)
    plt.colorbar(myplot)
    plt.show
    ()
    
elif start_year_month_str == '202207':
    changeover_date_2 = datetime.datetime(2022,7,8,12,30,00)
    fidas_Dist_Temp = fidas_Dist[start:changeover_date_2]
    fidas_Dist_Perm = fidas_Dist[changeover_date_2:end]
    date_file_label = '20220701-20220708'
    extra_file_label = '20220708-20220731'
    
    fidas_Dist_Temp.to_csv(str(fidas_Dis_Folder) + 'fidas_maqs_' + str(date_file_label) + '_PM-Distribution_'+ str(datatype) + '_' + str(version_number) + '.csv')
    fidas_Dist_Perm.to_csv(str(fidas_Dis_Folder) + 'fidas_maqs_' + str(extra_file_label) + '_PM-Distribution_' + str(datatype) + '_' + str(version_number) + '.csv')
    
    FIDAS_PM_serial_number = FIDAS_serial_number_2
    FIDAS_PM_cal_cert = FIDAS_cal_cert_2
    
    fidas_Dist = fidas_Dist_Temp
    fidas_Dist['TimeDateSince'] = fidas_Dist.index-datetime.datetime(1970,1,1,0,0,00)#calculate the time in seconds since 1970 for the datetime index
    fidas_Dist['TimeSecondsSince'] = fidas_Dist['TimeDateSince'].dt.total_seconds()
    fidas_Dist['day_year'] = pd.DatetimeIndex(fidas_Dist.index).dayofyear
    fidas_Dist['year'] = pd.DatetimeIndex(fidas_Dist.index).year
    fidas_Dist['month'] = pd.DatetimeIndex(fidas_Dist.index).month
    fidas_Dist['day'] = pd.DatetimeIndex(fidas_Dist.index).day
    fidas_Dist['hour'] = pd.DatetimeIndex(fidas_Dist.index).hour
    fidas_Dist['minute'] = pd.DatetimeIndex(fidas_Dist.index).minute
    fidas_Dist['second'] = pd.DatetimeIndex(fidas_Dist.index).second


    fidas_Dist_labels = fidas_Dist.iloc[0:1,0:(int(last_column)-int(first_column))]
    fidas_Dist_labels = fidas_Dist_labels.transpose()
    fidas_Dist_labels.iloc[:,0] = fidas_Dist_labels.index
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels.index
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='2018').columns, axis=1)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='2019').columns, axis=1)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='202').columns, axis=1)


    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip('(##/cm^3)').astype(str)
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip('um ').astype(str)
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.lstrip().astype(str)  
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip().astype(str)  
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].astype(float)
    Smallest_Aerosol = fidas_Dist_labels['Particle Size'].min()
    Largest_Aerosol = fidas_Dist_labels['Particle Size'].max()
    fidas_Dist_labels = fidas_Dist_labels.transpose()

    fidas_Dist_labels.drop(fidas_Dist_labels[(fidas_Dist_labels.iloc[:,0] == 'Particle Size')].index,inplace =True)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='Particle Size').columns, axis=1)

    fidas_Dist = pd.concat([fidas_Dist_labels, fidas_Dist])
    fidas_Dist.columns = np.where( fidas_Dist.iloc[0,:].isnull() , fidas_Dist.columns, fidas_Dist.iloc[0,:])
    fidas_Dist.drop(fidas_Dist[(fidas_Dist['hour'].isnull() )].index,inplace =True)
    fidas_Dist = fidas_Dist.drop(fidas_Dist.filter(regex='Particle Size').columns, axis=1)
    fidas_Dist = fidas_Dist.sort_index()

    fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))] = fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))].astype(float)

    fidas_Distribution_graph = fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))]

    #graph_Freq = '5min'
    #fidas_Distribution_graph = fidas_Distribution_graph.groupby(pd.Grouper(freq=graph_Freq)).mean()

    columns= list(range(0,(int(last_column)-int(first_column))))


    dates = fidas_Distribution_graph.index # setting x-axis
    diameters = fidas_Distribution_graph.columns # setting y-axis
    stride = 10                                                 #change stride to change averaging period
    dates_subset = dates[::stride]
    size_matrix = np.zeros((len(columns), dates_subset.size))
    # align the particle size columns as rows into the size matrix
    for ind, col in enumerate(columns):    
        size_matrix[ind,:] = fidas_Distribution_graph.iloc[::stride, col]

    x = dates_subset
    y = diameters
    z_min, z_max = size_matrix[:].min(), size_matrix[:].max()
    z = size_matrix[:]

    fig, ax = plt.subplots()
    myplot = ax.pcolormesh(x, y, z, cmap='RdYlBu_r', vmin=z_min, vmax=z_max)
    ax.set_title('FIDAS-particle distribution')
    plt.ylabel('nm')
    plt.xlabel('Date')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}

    plt.rc('font', **font)
    plt.colorbar(myplot)
    plt.show
    ()
    
    EXTRA_PM_serial_number = FIDAS_serial_number_1
    EXTRA_PM_cal_cert = FIDAS_cal_cert_1
    
    extra_fidas_Dist = fidas_Dist_Perm
    extra_fidas_Dist['TimeDateSince'] = extra_fidas_Dist.index-datetime.datetime(1970,1,1,0,0,00)#calculate the time in seconds since 1970 for the datetime index
    extra_fidas_Dist['TimeSecondsSince'] = extra_fidas_Dist['TimeDateSince'].dt.total_seconds()
    extra_fidas_Dist['day_year'] = pd.DatetimeIndex(extra_fidas_Dist.index).dayofyear
    extra_fidas_Dist['year'] = pd.DatetimeIndex(extra_fidas_Dist.index).year
    extra_fidas_Dist['month'] = pd.DatetimeIndex(extra_fidas_Dist.index).month
    extra_fidas_Dist['day'] = pd.DatetimeIndex(extra_fidas_Dist.index).day
    extra_fidas_Dist['hour'] = pd.DatetimeIndex(extra_fidas_Dist.index).hour
    extra_fidas_Dist['minute'] = pd.DatetimeIndex(extra_fidas_Dist.index).minute
    extra_fidas_Dist['second'] = pd.DatetimeIndex(extra_fidas_Dist.index).second


    fidas_Dist_labels = extra_fidas_Dist.iloc[0:1,0:(int(last_column)-int(first_column))]
    fidas_Dist_labels = fidas_Dist_labels.transpose()
    fidas_Dist_labels.iloc[:,0] = fidas_Dist_labels.index
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels.index
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='2018').columns, axis=1)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='2019').columns, axis=1)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='202').columns, axis=1)


    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip('(##/cm^3)').astype(str)
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip('um ').astype(str)
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.lstrip().astype(str)  
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip().astype(str)  
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].astype(float)
    Smallest_Aerosol = fidas_Dist_labels['Particle Size'].min()
    Largest_Aerosol = fidas_Dist_labels['Particle Size'].max()
    fidas_Dist_labels = fidas_Dist_labels.transpose()

    fidas_Dist_labels.drop(fidas_Dist_labels[(fidas_Dist_labels.iloc[:,0] == 'Particle Size')].index,inplace =True)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='Particle Size').columns, axis=1)

    extra_fidas_Dist = pd.concat([fidas_Dist_labels, extra_fidas_Dist])
    extra_fidas_Dist.columns = np.where( extra_fidas_Dist.iloc[0,:].isnull() , extra_fidas_Dist.columns, extra_fidas_Dist.iloc[0,:])
    extra_fidas_Dist.drop(extra_fidas_Dist[(extra_fidas_Dist['hour'].isnull() )].index,inplace =True)
    extra_fidas_Dist = extra_fidas_Dist.drop(extra_fidas_Dist.filter(regex='Particle Size').columns, axis=1)
    extra_fidas_Dist = extra_fidas_Dist.sort_index()

    extra_fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))] = extra_fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))].astype(float)

    fidas_Distribution_graph = extra_fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))]

    #graph_Freq = '5min'
    #fidas_Distribution_graph = fidas_Distribution_graph.groupby(pd.Grouper(freq=graph_Freq)).mean()

    columns= list(range(0,(int(last_column)-int(first_column))))


    dates = fidas_Distribution_graph.index # setting x-axis
    diameters = fidas_Distribution_graph.columns # setting y-axis
    stride = 10                                                 #change stride to change averaging period
    dates_subset = dates[::stride]
    size_matrix = np.zeros((len(columns), dates_subset.size))
    # align the particle size columns as rows into the size matrix
    for ind, col in enumerate(columns):    
        size_matrix[ind,:] = fidas_Distribution_graph.iloc[::stride, col]

    x = dates_subset
    y = diameters
    z_min, z_max = size_matrix[:].min(), size_matrix[:].max()
    z = size_matrix[:]

    fig, ax = plt.subplots()
    myplot = ax.pcolormesh(x, y, z, cmap='RdYlBu_r', vmin=z_min, vmax=z_max)
    ax.set_title('FIDAS-particle distribution')
    plt.ylabel('nm')
    plt.xlabel('Date')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}

    plt.rc('font', **font)
    plt.colorbar(myplot)
    plt.show
    ()

    
elif start_year_month_str == '202204' or start_year_month_str == '202205' or start_year_month_str == '202206':
    fidas_Dist.to_csv(str(fidas_Dis_Folder) + 'fidas_maqs_' + str(date_file_label) + '_PM-Distribution_' + str(datatype) + '_' + str(version_number) + '.csv')
    
    FIDAS_PM_serial_number = FIDAS_serial_number_2
    FIDAS_PM_cal_cert = FIDAS_cal_cert_2

    
    #calculate the time in seconds since 1970 for the datetime index
    fidas_Dist['TimeDateSince'] = fidas_Dist.index-datetime.datetime(1970,1,1,0,0,00)
    fidas_Dist['TimeSecondsSince'] = fidas_Dist['TimeDateSince'].dt.total_seconds()
    fidas_Dist['day_year'] = pd.DatetimeIndex(fidas_Dist.index).dayofyear
    fidas_Dist['year'] = pd.DatetimeIndex(fidas_Dist.index).year
    fidas_Dist['month'] = pd.DatetimeIndex(fidas_Dist.index).month
    fidas_Dist['day'] = pd.DatetimeIndex(fidas_Dist.index).day
    fidas_Dist['hour'] = pd.DatetimeIndex(fidas_Dist.index).hour
    fidas_Dist['minute'] = pd.DatetimeIndex(fidas_Dist.index).minute
    fidas_Dist['second'] = pd.DatetimeIndex(fidas_Dist.index).second
    #fidas_Dist['year'].head()



    fidas_Dist_labels = fidas_Dist.iloc[0:1,0:(int(last_column)-int(first_column))]
    fidas_Dist_labels = fidas_Dist_labels.transpose()
    fidas_Dist_labels.iloc[:,0] = fidas_Dist_labels.index
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels.index
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='2018').columns, axis=1)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='2019').columns, axis=1)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='202').columns, axis=1)


    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip('(##/cm^3)').astype(str)
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip('um ').astype(str)
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.lstrip().astype(str)  
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip().astype(str)  
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].astype(float)
    Smallest_Aerosol = fidas_Dist_labels['Particle Size'].min()
    Largest_Aerosol = fidas_Dist_labels['Particle Size'].max()
    fidas_Dist_labels = fidas_Dist_labels.transpose()

    fidas_Dist_labels.drop(fidas_Dist_labels[(fidas_Dist_labels.iloc[:,0] == 'Particle Size')].index,inplace =True)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='Particle Size').columns, axis=1)

    fidas_Dist = pd.concat([fidas_Dist_labels, fidas_Dist])
    fidas_Dist.columns = np.where( fidas_Dist.iloc[0,:].isnull() , fidas_Dist.columns, fidas_Dist.iloc[0,:])
    fidas_Dist.drop(fidas_Dist[(fidas_Dist['hour'].isnull() )].index,inplace =True)
    fidas_Dist = fidas_Dist.drop(fidas_Dist.filter(regex='Particle Size').columns, axis=1)
    fidas_Dist = fidas_Dist.sort_index()

    fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))] = fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))].astype(float)

    fidas_Distribution_graph = fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))]

    #graph_Freq = '5min'
    #fidas_Distribution_graph = fidas_Distribution_graph.groupby(pd.Grouper(freq=graph_Freq)).mean()
    print(first_column)
    print(last_column)

    columns= list(range(0,(int(last_column)-int(first_column))))


    dates = fidas_Distribution_graph.index # setting x-axis
    diameters = fidas_Distribution_graph.columns # setting y-axis
    stride = 10                                                 #change stride to change averaging period
    dates_subset = dates[::stride]
    size_matrix = np.zeros((len(columns), dates_subset.size))
    # align the particle size columns as rows into the size matrix
    for ind, col in enumerate(columns):    
        size_matrix[ind,:] = fidas_Distribution_graph.iloc[::stride, col]

    x = dates_subset
    y = diameters
    z_min, z_max = size_matrix[:].min(), size_matrix[:].max()
    z = size_matrix[:]

    fig, ax = plt.subplots()
    myplot = ax.pcolormesh(x, y, z, cmap='RdYlBu_r', vmin=z_min, vmax=z_max)
    ax.set_title('FIDAS-particle distribution')
    plt.ylabel('nm')
    plt.xlabel('Date')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}

    plt.rc('font', **font)
    plt.colorbar(myplot)
    plt.show
    ()

    
else:
    fidas_Dist.to_csv(str(fidas_Dis_Folder) + 'fidas_maqs_' + str(date_file_label) + '_PM-Distribution_' + str(datatype) + '_' + str(version_number) + '.csv')
    #print(str(fidas_Dis_Folder) + 'maqs-fidas-Distribution_' + str(date_file_label) + '_' + str(datatype) + '_' + str(version_number) + '.csv')
    #print(fidas_Dist['Distr_Flag'])
    
    FIDAS_PM_serial_number = FIDAS_serial_number_1
    FIDAS_PM_cal_cert = FIDAS_cal_cert_1

    #calculate the time in seconds since 1970 for the datetime index
    fidas_Dist['TimeDateSince'] = fidas_Dist.index-datetime.datetime(1970,1,1,0,0,00)
    fidas_Dist['TimeSecondsSince'] = fidas_Dist['TimeDateSince'].dt.total_seconds()
    fidas_Dist['day_year'] = pd.DatetimeIndex(fidas_Dist.index).dayofyear
    fidas_Dist['year'] = pd.DatetimeIndex(fidas_Dist.index).year
    fidas_Dist['month'] = pd.DatetimeIndex(fidas_Dist.index).month
    fidas_Dist['day'] = pd.DatetimeIndex(fidas_Dist.index).day
    fidas_Dist['hour'] = pd.DatetimeIndex(fidas_Dist.index).hour
    fidas_Dist['minute'] = pd.DatetimeIndex(fidas_Dist.index).minute
    fidas_Dist['second'] = pd.DatetimeIndex(fidas_Dist.index).second
    #fidas_Dist['year'].head()

#print(fidas_Dist.iloc[:,0:(int(last_column) - int(first_column))])
    fidas_Dist_labels = fidas_Dist.iloc[0:1,0:(int(last_column) - int(first_column))]
    fidas_Dist_labels = fidas_Dist_labels.transpose()
    fidas_Dist_labels.iloc[:,0] = fidas_Dist_labels.index
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels.index
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='2018').columns, axis=1)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='2019').columns, axis=1)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='202').columns, axis=1)


    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip('(##/cm^3)').astype(str)
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip('um ').astype(str)
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.lstrip().astype(str)  
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].str.rstrip().astype(str)  
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    fidas_Dist_labels['Particle Size'] = fidas_Dist_labels['Particle Size'].astype(float)
    Smallest_Aerosol = fidas_Dist_labels['Particle Size'].min()
    Largest_Aerosol = fidas_Dist_labels['Particle Size'].max()
    fidas_Dist_labels = fidas_Dist_labels.transpose()

    fidas_Dist_labels.drop(fidas_Dist_labels[(fidas_Dist_labels.iloc[:,0] == 'Particle Size')].index,inplace =True)
    fidas_Dist_labels = fidas_Dist_labels.drop(fidas_Dist_labels.filter(regex='Particle Size').columns, axis=1)

    fidas_Dist = pd.concat([fidas_Dist_labels, fidas_Dist])
    fidas_Dist.columns = np.where( fidas_Dist.iloc[0,:].isnull() , fidas_Dist.columns, fidas_Dist.iloc[0,:])
    fidas_Dist.drop(fidas_Dist[(fidas_Dist['hour'].isnull() )].index,inplace =True)
    fidas_Dist = fidas_Dist.drop(fidas_Dist.filter(regex='Particle Size').columns, axis=1)
    fidas_Dist = fidas_Dist.sort_index()

    fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))] = fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))].astype(float)

    fidas_Distribution_graph = fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))]
    print(int(last_column))
    print(int(first_column))

    #graph_Freq = '5min'
    #fidas_Distribution_graph = fidas_Distribution_graph.groupby(pd.Grouper(freq=graph_Freq)).mean()

    columns= list(range(0,(int(last_column)-int(first_column))))
    print(columns)


    dates = fidas_Distribution_graph.index # setting x-axis
    diameters = fidas_Distribution_graph.columns # setting y-axis
    stride = 10                                                 #change stride to change averaging period
    dates_subset = dates[::stride]
    size_matrix = np.zeros((len(columns), dates_subset.size))
    # align the particle size columns as rows into the size matrix
    for ind, col in enumerate(columns):    
        size_matrix[ind,:] = fidas_Distribution_graph.iloc[::stride, col]

    x = dates_subset
    y = diameters
    z_min, z_max = size_matrix[:].min(), size_matrix[:].max()
    z = size_matrix[:]
    print(z)
    fig, ax = plt.subplots()
    myplot = ax.pcolormesh(x, y, z, cmap='RdYlBu_r', vmin=z_min, vmax=z_max)
    ax.set_title('FIDAS-particle distribution')
    plt.ylabel('nm')
    plt.xlabel('Date')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}

    plt.rc('font', **font)
    plt.colorbar(myplot)
    plt.show
    ()
    #print(fidas_Distribution_graph)
    print( y)

