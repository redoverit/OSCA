# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 13:33:28 2020

@author: mbexknm5
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import glob
import math

av_Freq = '1min'#everaging frequency required of the data
year = '2019'
month = '09'

start = datetime.datetime(2019,9,1,0,0,00)#start time of the period 
end = datetime.datetime(2019,10,1,0,0,00)#end time of the period

#create a timeline with a row for every 1min time period 
dt = start
end = end
step = datetime.timedelta(minutes=1)

timeline = []

while dt < end:
    timeline.append(dt.strftime('%Y-%m-%d %H:%M:%S'))
    dt += step
    
timeline = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in timeline] #converts the dateTime format from string to python dateTime
#timeSince = pd.Series(timeline)#-datetime.datetime(1970,1,1,0,0,00)

qc_Flags = [2]*len(timeline)

TimeLineSince= pd.DataFrame(qc_Flags, index=timeline, columns=['qc_flags'], dtype = np.float64)
#%%

sonic_Data = pd.concat(map(pd.read_csv, glob.glob('D:/FirsData/Sonic/'+year+month+'*_Sonic_1s.txt')))# read and concatenate the raw data

sonic_Data['datetime'] = sonic_Data['Date']+' '+ sonic_Data[' Time']# added Date and time into new columns
sonic_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in sonic_Data['datetime']] #converts the dateTime format from string to python dateTime
sonic_Data.index = sonic_Data['datetime']# sets the index to datetime

m_gust= sonic_Data[' s(m/s)'].groupby(pd.Grouper(freq=av_Freq)).max() # find the max gust value in each minute before averaging the data
sonic_Data = sonic_Data.groupby(pd.Grouper(freq=av_Freq)).mean() # averages the data 
sonic_Data['m_Gust'] = pd.Series(m_gust) # add gust to dataframe

#combine the full month timeline with the sonic data, aligned to the time indexed.   
sonic_Data = pd.concat([sonic_Data, TimeLineSince], axis=1)
#calculate the time in seconds since 1970 for the datetime index
sonic_Data['TimeDateSince'] = sonic_Data.index-datetime.datetime(1970,1,1,0,0,00)
sonic_Data['TimeSecondsSince'] = sonic_Data['TimeDateSince'].dt.total_seconds()

sonic_Data['wind_Sp (m/s)'] = sonic_Data[' s(m/s)'].replace(np.nan,-1.00E+20)
sonic_Data['wind_Dr'] = sonic_Data[' d(deg)'].replace(np.nan,-1.00E+20)
sonic_Data['max_Gust'] = sonic_Data['m_Gust'].replace(np.nan,-1.00E+20)

sonic_Data['qc_Flags'] = np.where(sonic_Data['wind_Sp (m/s)']==-1.00E+20, 2,1)
#%%
#housekeeping
sonic_Data = sonic_Data[:-1] # Trim the end of the dataframe

col_List_sonic = list(sonic_Data.columns.values) # create a list of column names
col_List_sonic.remove('wind_Sp (m/s)')
col_List_sonic.remove('wind_Dr')
col_List_sonic.remove('max_Gust')
col_List_sonic.remove('qc_Flags')
col_List_sonic.remove('TimeSecondsSince')
sonic_Data = sonic_Data.drop(columns=col_List_sonic) #removing unwanted columns
#%%
#plotting
plt.plot(sonic_Data['wind_Sp (m/s)'], label='Speed')
plt.plot(sonic_Data['wind_Dr'], label='Direction')
#plt.plot(sonic_Data['max_Gust'], label='Gust')

plt.legend()
plt.ylabel('mg/m3')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 24}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.show()


#sonic_Data = sonic_Data[start:end] #sets the data to the time length defined in MAQS_Master

#sonic_Data['windsp_qc_Flags'] = master['site_flags'] # creates the product specific flags. In this case it is the same as the site flags
#sonic_Data['winddir_qc_Flags'] = master['site_flags']
#
#master=pd.concat([master,sonic_Data], axis=1) #adds the somic data to the master dataframe 
#master.drop(master.tail(1).index,inplace=True)##drop the last line to avoid timeline missmatch

