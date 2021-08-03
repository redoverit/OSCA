# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 13:27:44 2020

@author: mbexknm5
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import glob
import math

av_Freq = '1min'#everaging frequency required of the data
year = 'all'
month = '09'

start = datetime.datetime(2019,7,26,0,0,00)#start time of the period 
end = datetime.datetime(2021,7,19,8,0,00)#end time of the period

#create a timeline with a row for every 1min time period 
#dt = start
#end = end
#step = datetime.timedelta(minutes=1)
#
#timeline = []
#
#while dt < end:
#    timeline.append(dt.strftime('%Y-%m-%d %H:%M:%S'))
#    dt += step
#    
#timeline = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in timeline] #converts the dateTime format from string to python dateTime
##timeSince = pd.Series(timeline)#-datetime.datetime(1970,1,1,0,0,00)
#
#Flags = [1]*len(timeline)
#qc_Flags = np.array(Flags, dtype='uint32')
##qc_Flags = nc.stringtochar(qc_Flags)
#
#TimeLineSince= pd.DataFrame(qc_Flags, index=timeline, columns=['qc_flags'])


pattern = 'D:/FirsData/Fidas/*_fidas_1min.txt'# Collect CSV files
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

col_List_fidasPM = list(fidas_Data.columns.values)
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

fidas_PM['PM_Flag'] = np.where((fidas_Data['Cal_error'] >0),3,1)#populate the column with condition
fidas_PM['PM_Flag'] = np.where((fidas_PM['PM10 (ug/m3)'] >200),4,fidas_PM['PM_Flag'])

start_Tarmac = datetime.datetime(2020,5,4,7,30,00)
end_Tarmac = datetime.datetime(2020,5,15,16,0,00)
fidas_PM.loc[start_Tarmac:end_Tarmac, 'PM_Flag'] = 4

start_Audit1 = datetime.datetime(2019,7,19,9,50,00)
end_Audit1 = datetime.datetime(2019,7,19,10,15,00)
fidas_PM.drop(fidas_PM.loc[start_Audit1:end_Audit1].index, inplace=True)

start_Audit2 = datetime.datetime(2019,10,2,16,40,00)
end_Audit2 = datetime.datetime(2019,10,2,17,0,00)
fidas_PM.drop(fidas_PM.loc[start_Audit2:end_Audit2].index, inplace=True)

start_Audit3 = datetime.datetime(2020,3,18,9,0,00)
end_Audit3 = datetime.datetime(2020,3,18,14,0,00)
fidas_PM.drop(fidas_PM.loc[start_Audit3:end_Audit3].index, inplace=True)

start_Audit4 = datetime.datetime(2020,10,2,9,0,00)
end_Audit4 = datetime.datetime(2020,10,2,12,0,00)
fidas_PM.drop(fidas_PM.loc[start_Audit4:end_Audit4].index, inplace=True)

start_Audit5 = datetime.datetime(2021,3,30,9,0,00)
end_Audit5 = datetime.datetime(2021,3,30,12,0,00)
fidas_PM.drop(fidas_PM.loc[start_Audit5:end_Audit5].index, inplace=True)


col_List_fidasMet = list(fidas_Data.columns.values)
col_List_fidasMet.remove('Temperature (deg C)')
col_List_fidasMet.remove('Pressure (mbar)')
col_List_fidasMet.remove('Humidity (%)')
fidas_Met = fidas_Data.drop(columns=col_List_fidasMet)
fidas_Met['Met_Flag'] = 1
fidas_Met['Temperature (K)'] = fidas_Met['Temperature (deg C)'] + 273.15
fidas_Met = fidas_Met[fidas_Met['Pressure (mbar)'] >= 950]

#plt.plot(fidas_PM['PM1 (ug/m3)'], label='PM1')
#plt.plot(fidas_PM['PM2.5 (ug/m3)'], label='PM2.5')
#plt.plot(fidas_PM['PM10 (ug/m3)'], label='PM10')
plt.plot(fidas_Met['Temperature (deg C)'], label= 'Temp')
plt.plot(fidas_Met['Pressure (mbar)'], label= 'Pres')
plt.plot(fidas_Met['Humidity (%)'], label= 'Hum')
#plt.plot(fidas_PM['PM_Flag'], label='flag')
#plt.plot(fidas_Data['Cal_error'], label='cal_error')
plt.legend()
plt.ylabel('ug/m3')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 24}

plt.rc('font', **font)
#plt.ylim(10, 30)
#plt.figure()
plt.show()

fidas_PM.to_csv('D:/maqs-fidas-PM_20210719_v0.5.csv')
fidas_Met.to_csv('D:/maqs-fidas-Met_20210719_v0.5.csv')

#calculate the time in seconds since 1970 for the datetime index
fidas_PM['TimeDateSince'] = fidas_PM.index-datetime.datetime(1970,1,1,0,0,00)
fidas_PM['TimeSecondsSince'] = fidas_PM['TimeDateSince'].dt.total_seconds()
fidas_PM['day_year'] = pd.DatetimeIndex(fidas_PM['TimeDateSince']).dayofyear
fidas_PM['year'] = pd.DatetimeIndex(fidas_PM['TimeDateSince']).year
fidas_PM['month'] = pd.DatetimeIndex(fidas_PM['TimeDateSince']).month
fidas_PM['day'] = pd.DatetimeIndex(fidas_PM['TimeDateSince']).day
fidas_PM['hour'] = pd.DatetimeIndex(fidas_PM['TimeDateSince']).hour
fidas_PM['minute'] = pd.DatetimeIndex(fidas_PM['TimeDateSince']).minute
fidas_PM['second'] = pd.DatetimeIndex(fidas_PM['TimeDateSince']).second

fidas_Met['TimeDateSince'] = fidas_Met.index-datetime.datetime(1970,1,1,0,0,00)
fidas_Met['TimeSecondsSince'] = fidas_Met['TimeDateSince'].dt.total_seconds()
fidas_Met['day_year'] = pd.DatetimeIndex(fidas_Met['TimeDateSince']).dayofyear
fidas_Met['year'] = pd.DatetimeIndex(fidas_Met['TimeDateSince']).year
fidas_Met['month'] = pd.DatetimeIndex(fidas_Met['TimeDateSince']).month
fidas_Met['day'] = pd.DatetimeIndex(fidas_Met['TimeDateSince']).day
fidas_Met['hour'] = pd.DatetimeIndex(fidas_Met['TimeDateSince']).hour
fidas_Met['minute'] = pd.DatetimeIndex(fidas_Met['TimeDateSince']).minute
fidas_Met['second'] = pd.DatetimeIndex(fidas_Met['TimeDateSince']).second
