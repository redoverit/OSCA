# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 16:44:35 2022

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

sample_Freq = '60min'
av_Freq = '60min' #averaging frequency required of the data
data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v2.0' #version of the code
year_start = 2022 #input the year of study by number
month_start = 12 #input the month of study by number
default_start_day = 1 #default start date set
day_start = default_start_day #can put number
end_day = "default" # put either "default" or your end day
validity_status = 'Ratified' #Ratified or Unratified

status = np.where(validity_status == 'Unratified' , '_Unratified_', '_Ratified_')

today = date.today()
current_day = today.strftime("%Y%m%d")

start = datetime.datetime(year_start,month_start,day_start,0,0,0) #start time of the period 
month_After = start + dateutil.relativedelta.relativedelta(months=1)
month_After_str = str(month_After.strftime("%Y")) + str(month_After.strftime("%m"))
default_end_date = month_After - timedelta(minutes=1) #last day of month more complex so established here

default_end_day = str(default_end_date.strftime("%Y")) + str(default_end_date.strftime("%m")) + str(default_end_date.strftime("%d"))

year_end = int(default_end_date.strftime("%Y")) #this converts the default_end_day into the end of time selected
month_end = int(default_end_date.strftime("%m"))
day_end = int(default_end_date.strftime("%d"))

end = datetime.datetime(year_end,month_end,day_end,23,59,59) #if new end date needed to can be changed here 

start_year_month_str = str(start.strftime("%Y")) + str(start.strftime("%m")) # convert start and end months to strings
end_year_month_str = str(end.strftime("%Y")) + str(end.strftime("%m"))

end_Date_Check = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

date_file_label = np.where(start_year_month_str == end_year_month_str, start_year_month_str, str(start_year_month_str) + "-" + str(end_year_month_str))
#print(date_file_label) #print end date to check it is correct

folder = np.where((str(version_number) == 'v0.6'), 'Preliminary', str(validity_status))
#print("using a " + str(folder) + "_" + str(version_number) + " folder")

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/TCA/', 'D:/FirsData/TCA/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(folder) + '_' + str(version_number) + '/', 'D:/' + str(folder) + '_' + str(version_number) + '/')

month_Prior = start + dateutil.relativedelta.relativedelta(months=1)
month_Prior_str = str(month_Prior.strftime("%Y")) + str(month_Prior.strftime("%m"))

if float(date_file_label) < 202205:
    TCA_Feb_files = str(Data_Source_Folder) + '*' + '202202' + '*_tca.txt'
    TCA_March_files = str(Data_Source_Folder) + '*' + '202203' + '*_tca.txt'
    TCA_April_files = str(Data_Source_Folder) + '*' + '202204' + '*_tca.txt'
    TCA_May_files = str(Data_Source_Folder) + '202205010000_tca.txt'
    TCA_file = glob.glob(str(TCA_Feb_files)) + glob.glob(str(TCA_March_files)) + glob.glob(str(TCA_April_files)) + glob.glob(str(TCA_May_files))

    frames = []

    for csv in TCA_file:
        csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors ## or use 'r'
        df = pd.read_csv(csv, low_memory=False, header=None, index_col=False, skip_blank_lines=True, error_bad_lines=False, na_filter=True) ##, skiprows=1, usecols=[0,1,5,6,7,8,9,10,11,12]
        frames.append(df)
    
    TCA_Data = pd.concat(frames)

    TCA_Data.rename(columns={0: 'Date',  1: 'Time'}, inplace=True)

    TCA_Data['Date'] = TCA_Data['Date'].astype(str)
    TCA_Data['Time'] = TCA_Data['Time'].astype(str)
    TCA_Data['Date_length'] = TCA_Data['Date'].str.len()
    TCA_Data['Time_length'] = TCA_Data['Time'].str.len()
    TCA_Data=TCA_Data[TCA_Data.Date_length == 10] 
    TCA_Data=TCA_Data[TCA_Data.Time_length == 8] 
    TCA_Data['datetime'] = TCA_Data['Date'] + ' ' + TCA_Data['Time']# added Date and time into new columns
    TCA_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in TCA_Data['datetime']] #converts the dateTime format from string to python dateTime
    TCA_Data['datetime'] = TCA_Data['datetime'] - timedelta(minutes=80) 
    TCA_Data.index = TCA_Data['datetime']
    TCA_Data = TCA_Data.sort_index()
    TCA_Data = TCA_Data.drop(columns=['Time', 'Date', 'datetime'])
    TCA_Data = TCA_Data.iloc[:,0].str.split(' ', expand=True)
    #print(TCA_Data)
    TCA_Data.columns = TCA_Data.columns + 2
elif float(date_file_label) == 202205:
    TCA_All_files = str(Data_Source_Folder) + '*' + str(date_file_label) + '*_tca.txt'
    TCA_file = glob.glob(str(TCA_All_files))

    frames = []

    for csv in TCA_file:
        csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors ## or use 'r'
        df = pd.read_csv(csv, low_memory=False, header=None, index_col=False, skip_blank_lines=True, error_bad_lines=False, na_filter=True) ##, skiprows=1, usecols=[0,1,5,6,7,8,9,10,11,12]
        frames.append(df)
    
    Early_TCA_Data = pd.concat(frames)

    Early_TCA_Data.rename(columns={0: 'Date',  1: 'Time'}, inplace=True)

    Early_TCA_Data['Date'] = Early_TCA_Data['Date'].astype(str)
    Early_TCA_Data['Time'] = Early_TCA_Data['Time'].astype(str)
    Early_TCA_Data['Date_length'] = Early_TCA_Data['Date'].str.len()
    Early_TCA_Data['Time_length'] = Early_TCA_Data['Time'].str.len()
    Early_TCA_Data=Early_TCA_Data[Early_TCA_Data.Date_length == 10] 
    Early_TCA_Data=Early_TCA_Data[Early_TCA_Data.Time_length == 8] 
    Early_TCA_Data['datetime'] = Early_TCA_Data['Date'] + ' ' + Early_TCA_Data['Time']# added Date and time into new columns
    Early_TCA_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in Early_TCA_Data['datetime']] #converts the dateTime format from string to python dateTime
    Early_TCA_Data['datetime'] = Early_TCA_Data['datetime'] - timedelta(minutes=80) 
    Early_TCA_Data.index = Early_TCA_Data['datetime']
    Early_TCA_Data = Early_TCA_Data.sort_index()
    Early_TCA_Data = Early_TCA_Data.drop(columns=['Time', 'Date', 'datetime'])
    Early_TCA_Data = Early_TCA_Data.iloc[:,0].str.split(' ', expand=True)
    #print(Early_TCA_Data)
    Early_TCA_Data.columns = Early_TCA_Data.columns + 2
    
    
    TCA_Early_files = str(Data_Source_Folder) + '202205250903_tca.txt'
    TCA_file = glob.glob(str(TCA_Early_files))
    
    frames = []

    for csv in TCA_file:
        csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors ## or use 'r'
        df = pd.read_csv(csv, low_memory=False, header=None, index_col=False, skip_blank_lines=True, error_bad_lines=False, na_filter=True) ##, usecols=[0,1,5,6,7,8,9,10,11,12]
        frames.append(df)
    
    TCA_Data = pd.concat(frames)
    
    TCA_Typical_files = str(Data_Source_Folder) + '202205250926_tca.txt'
    TCA_After_files = str(Data_Source_Folder) + '*' + str(month_After_str) + '*_tca.txt'
    TCA_file = glob.glob(str(TCA_Typical_files)) + glob.glob(str(TCA_After_files))

    frames = []

    for csv in TCA_file:
        csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors ## or use 'r'
        df = pd.read_csv(csv, low_memory=False, header=None, index_col=False, skiprows=1, skip_blank_lines=True, error_bad_lines=False, na_filter=True) ##, usecols=[0,1,5,6,7,8,9,10,11,12]
        frames.append(df)
    
    late_TCA_Data = pd.concat(frames)
    TCA_Data = pd.concat([TCA_Data, late_TCA_Data])

    #TCA_Data = TCA_Data.iloc[:,0].str.split(',', expand=True)

    TCA_Data.rename(columns={0: 'Date',  1: 'Time'}, inplace=True)

    TCA_Data['Date'] = TCA_Data['Date'].astype(str)
    TCA_Data['Time'] = TCA_Data['Time'].astype(str)
    TCA_Data['datetime'] = TCA_Data['Date'] + ' ' + TCA_Data['Time']# added Date and time into new columns
    TCA_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in TCA_Data['datetime']] #converts the dateTime format from string to python dateTime
    TCA_Data['datetime'] = TCA_Data['datetime'] - timedelta(minutes=80) 
    TCA_Data.index = TCA_Data['datetime']
    TCA_Data = TCA_Data.sort_index()
    TCA_Data = TCA_Data.drop(columns=['Time', 'Date', 'datetime'])
    
    TCA_Data = pd.concat([Early_TCA_Data, TCA_Data])
    
else:
    TCA_All_files = str(Data_Source_Folder) + '*' + str(date_file_label) + '*_tca.txt'
    TCA_After_files = str(Data_Source_Folder) + '*' + str(month_After_str) + '*_tca.txt'
    TCA_file = glob.glob(str(TCA_All_files)) + glob.glob(str(TCA_After_files))

    frames = []

    for csv in TCA_file:
        csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors ## or use 'r'
        df = pd.read_csv(csv, low_memory=False, header=None, index_col=False, skiprows=1, skip_blank_lines=True, error_bad_lines=False, na_filter=True) ##, usecols=[0,1,5,6,7,8,9,10,11,12]
        frames.append(df)
    
    TCA_Data = pd.concat(frames)

    #TCA_Data = TCA_Data.iloc[:,0].str.split(',', expand=True)

    TCA_Data.rename(columns={0: 'Date',  1: 'Time'}, inplace=True)

    TCA_Data['Date'] = TCA_Data['Date'].astype(str)
    TCA_Data['Time'] = TCA_Data['Time'].astype(str)
    TCA_Data['datetime'] = TCA_Data['Date'] + ' ' + TCA_Data['Time']# added Date and time into new columns
    TCA_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in TCA_Data['datetime']] #converts the dateTime format from string to python dateTime
    TCA_Data['datetime'] = TCA_Data['datetime'] - timedelta(minutes=80) 
    TCA_Data.index = TCA_Data['datetime']
    TCA_Data = TCA_Data.sort_index()

TCA_Data = TCA_Data.iloc[:,16:]
TCA_Data = TCA_Data[start:end]


TCA_Data.rename(columns={16: 'TCcounts',  17: 'TCmass', 18: 'TCconc',  19: 'AE33_BC6', 20: 'AE33_ValidData'  }, inplace=True)
TCA_Data.rename(columns={21: 'AE33_b',  22: 'OC', 23: 'EC',  24: 'CO2', 25: 'Volume'  }, inplace=True)
TCA_Data.rename(columns={26: 'Chamber',  27: 'SetupID', 28: 'a1',  29: 'b1', 30: 'c1'  }, inplace=True)
TCA_Data.rename(columns={31: 'd1',  32: 'e1', 33: 'f1',  34: 'a2', 35: 'b2'  }, inplace=True)
TCA_Data.rename(columns={36: 'c2',  37: 'd2', 38: 'e2',  39: 'f2' }, inplace=True)


TCA_Data.rename(columns={'TCconc' : 'Total Carbon (ug/m3)', 'OC' : 'Organic Carbon (ug/m3)', 'EC' : 'Elemental Carbon (ug/m3)', 'CO2' : 'Average CO2 (ppm)' }, inplace=True)

TCA_Data.drop(TCA_Data[(TCA_Data['Total Carbon (ug/m3)'] == 'Total Carbon (ug/m3)')].index,inplace =True) 
TCA_Data.drop(TCA_Data[(TCA_Data['Organic Carbon (ug/m3)'] == 'Organic Carbon (ug/m3)')].index,inplace =True) 
TCA_Data.drop(TCA_Data[(TCA_Data['Organic Carbon (ug/m3)'] == 'Organic Carbon (ug/m3)')].index,inplace =True) 
TCA_Data.drop(TCA_Data[(TCA_Data['Organic Carbon (ug/m3)'] == 'Organic Carbon (ug/m3)')].index,inplace =True) 
TCA_Data.drop(TCA_Data[(TCA_Data['Total Carbon (ug/m3)'] == 'Total Carbon (ng/m3)')].index,inplace =True) 
TCA_Data.drop(TCA_Data[(TCA_Data['Organic Carbon (ug/m3)'] == 'Organic Carbon (ng/m3)')].index,inplace =True) 
TCA_Data.drop(TCA_Data[(TCA_Data['Organic Carbon (ug/m3)'] == 'Organic Carbon (ng/m3)')].index,inplace =True) 
TCA_Data.drop(TCA_Data[(TCA_Data['Organic Carbon (ug/m3)'] == 'Organic Carbon (ng/m3)')].index,inplace =True) 

TCA_Data['Total Carbon (ug/m3)'] = TCA_Data['Total Carbon (ug/m3)'].astype(float)
TCA_Data['Organic Carbon (ug/m3)'] = TCA_Data['Organic Carbon (ug/m3)'].astype(float)
TCA_Data['Elemental Carbon (ug/m3)'] = TCA_Data['Elemental Carbon (ug/m3)'].astype(float)
TCA_Data['Average CO2 (ppm)'] = TCA_Data['Average CO2 (ppm)'].astype(float)

TCA_Data['Total Carbon (ug/m3)'] = TCA_Data['Total Carbon (ug/m3)']/1000
TCA_Data['Organic Carbon (ug/m3)'] = TCA_Data['Organic Carbon (ug/m3)']/1000
TCA_Data['Elemental Carbon (ug/m3)'] = TCA_Data['Elemental Carbon (ug/m3)']/1000

TCA_Data['qc_Flags'] = 1

start_install_1 = datetime.datetime(2022,1,28,13,0,00)# 28 January 2022 13:26 Aethalometer on cabin air while inlets are rearranged to incorporate TCA.
end_install_1 = datetime.datetime(2022,1,28,15,0,00)
TCA_Data.loc[start_install_1:end_install_1, 'qc_Flags'] = 2
#TCA_Data.drop(TCA_Data.loc[start_install_1:end_install_1].index, inplace=True)

start_Denuder_1 = datetime.datetime(2022,3,17,10,0,00)# 17 March 2022  10:05 TCA filters changed 10:39 TCA denuder changed
end_Denuder_1 = datetime.datetime(2022,3,17,11,0,00)
TCA_Data.loc[start_Denuder_1:end_Denuder_1, 'qc_Flags'] = 2
#TCA_Data.drop(TCA_Data.loc[start_Denuder_1:end_Denuder_1].index, inplace=True)

start_Pink_1 = datetime.datetime(2022,4,7,8,0,00) # 7 April 2022 - 08:00 TCA Filters changed -visible pinkish deposits on the filters, also noted that the pump speed was gradually increasing to keep flow constant.
end_Pink_1 = datetime.datetime(2022,4,7,19,0,00)
TCA_Data.loc[start_Pink_1:end_Pink_1, 'qc_Flags'] = 2
#TCA_Data.drop(TCA_Data.loc[start_Pink_1:end_Pink_1].index, inplace=True)

start_Denuder_2 = datetime.datetime(2022,5,16,13,0,00)# 16 May 2022 14:50 TCA Denuder and filters changed. TCA filters were showing signs of filter failure. Channel 2 was very close to having two holes if it did not already. No sign from the data, and no message from the instrument that the filter had failed.
end_Denuder_2 = datetime.datetime(2022,5,16,16,0,00)
TCA_Data.loc[start_Denuder_1:end_Denuder_1, 'qc_Flags'] = 2
#TCA_Data.drop(TCA_Data.loc[start_Denuder_1:end_Denuder_1].index, inplace=True)

start_inspection_1 = datetime.datetime(2022,5,25,9,50,00) # 25 May 2022 - On site for lifting gear inspection - Looking at TCA data for evidence of change in TCA signal with the ageing of the denuder, does seem to be a step change in TC at the point of the denuder change, looks like it was left for too long. - Also noted that TCA housekeeping files are not being written properly (has been the case for some time).
end_inspection_1 = datetime.datetime(2022,5,25,9,55,00)
TCA_Data.loc[start_inspection_1:end_inspection_1, 'qc_Flags'] = 2
#TCA_Data.drop(TCA_Data.loc[start_inspection_1:end_inspection_1].index, inplace=True)

start_inlet_1 = datetime.datetime(2022,6,8,11,0,00) # 8 June 2022 - 11:10 Connected low cost sensor from Barry Speed on to one of the spare ports on the Aethalometer/TCA inlet.
end_inlet_1 = datetime.datetime(2022,6,8,12,0,00)
TCA_Data.loc[start_inlet_1:end_inlet_1, 'qc_Flags'] = 2
#TCA_Data.drop(TCA_Data.loc[start_inlet_1:end_inlet_1].index, inplace=True)

start_Denuder_2 = datetime.datetime(2022,6,15,13,0,00) # 15 June 2022 - 13:47 TCA Filter change and TCA denuder change.
end_Denuder_2 = datetime.datetime(2022,6,15,14,0,00)
TCA_Data.loc[start_Denuder_2:end_Denuder_2, 'qc_Flags'] = 2
#TCA_Data.drop(TCA_Data.loc[start_Denuder_2:end_Denuder_2].index, inplace=True)

start_Denuder_3 = datetime.datetime(2022,7,8,10,0,00) # 8 July 2022 - 10:45 TCA denuder change, also cleaning of TCA and Aeth cyclones.
end_Denuder_3 = datetime.datetime(2022,7,8,11,0,00)
TCA_Data.loc[start_Denuder_3:end_Denuder_3, 'qc_Flags'] = 2
#TCA_Data.drop(TCA_Data.loc[start_Denuder_3:end_Denuder_3].index, inplace=True)

start_Denuder_4 = datetime.datetime(2022,8,12,13,0,00) # 12 August 2022 - 13:09 TCA denuder and filters changed.
end_Denuder_4 = datetime.datetime(2022,8,12,14,0,00)
TCA_Data.loc[start_Denuder_4:end_Denuder_4, 'qc_Flags'] = 2
#TCA_Data.drop(TCA_Data.loc[start_Denuder_4:end_Denuder_4].index, inplace=True)

start_Denuder_5 = datetime.datetime(2022,9,14,14,45,00) # 14 Sept 2022 - TCA filters and denuder changed
end_Denuder_5 = datetime.datetime(2022,9,14,17,38,00)
TCA_Data.loc[start_Denuder_5:end_Denuder_5, 'qc_Flags'] = 2
#TCA_Data.drop(TCA_Data.loc[start_Denuder_5:end_Denuder_5].index, inplace=True)

start_clean_1 = datetime.datetime(2022,10,4,10,0,00) # 4 oct 2022 - 10:17 Aethalometer and TCA inlets open to cabin for cleaning. 10:39 Aethalometer and TCA inlets closed again after cleaning.
end_clean_1 = datetime.datetime(2022,10,4,11,0,00)
TCA_Data.loc[start_clean_1:end_clean_1, 'qc_Flags'] = 2
#TCA_Data.drop(TCA_Data.loc[start_clean_1:end_clean_1].index, inplace=True)

start_Denuder_6 = datetime.datetime(2022,10,13,7,0,00) # 13th October 2022 - 08:00 TCA filters changed, TCA denuder changed -shared inlet with Aeth open to cabin for 2min.
end_Denuder_6 = datetime.datetime(2022,10,13,9,0,00)
TCA_Data.loc[start_Denuder_6:end_Denuder_6, 'qc_Flags'] = 2
#TCA_Data.drop(TCA_Data.loc[start_Denuder_6:end_Denuder_6].index, inplace=True)

start_Clean2 = datetime.datetime(2022,10,4,8,0,00) #cleaning denuder
end_Clean2 = datetime.datetime(2022,10,4,8,30,00)
TCA_Data.loc[start_Clean2:end_Clean2, ('qc_Flags')] = 2

start_Clean3 = datetime.datetime(2022,12,5,13,0,00) #cleaning denuder
end_Clean3 = datetime.datetime(2022,12,5,13,30,00)
TCA_Data.loc[start_Clean3:end_Clean3, ('qc_Flags')] = 2

start_Clean4 = datetime.datetime(2022,12,9,12,30,00) #cleaning denuder
end_Clean4 = datetime.datetime(2022,12,9,17,30,00)
TCA_Data.loc[start_Clean4:end_Clean4, ('qc_Flags')] = 2
TCA_Data.drop(TCA_Data.loc[start_Clean4:end_Clean4].index, inplace=True)

TCA_Data = TCA_Data[['Total Carbon (ug/m3)', 'Organic Carbon (ug/m3)', 'Elemental Carbon (ug/m3)', 'Average CO2 (ppm)', 'qc_Flags']]


TCA_Data['qc_Flag_TC'] = np.where(TCA_Data['Total Carbon (ug/m3)'] < 0.3, 2, TCA_Data['qc_Flags']) #0.3 μg C m−3 
TCA_Data['qc_Flag_OC'] = np.where(TCA_Data['Organic Carbon (ug/m3)'] < 0.3, 2, TCA_Data['qc_Flags'])
TCA_Data['qc_Flag_EC'] = np.where(TCA_Data['Elemental Carbon (ug/m3)'] < 0.3, 2, TCA_Data['qc_Flags'])
TCA_Data['qc_Flag_CO2'] = np.where(TCA_Data['Average CO2 (ppm)'] < 400, 2, TCA_Data['qc_Flags'])

TCA_Data = TCA_Data.drop(columns=['qc_Flags'])

qc_Flag_TC = TCA_Data['qc_Flag_TC'].groupby(pd.Grouper(freq=av_Freq)).max() 
qc_Flag_OC = TCA_Data['qc_Flag_OC'].groupby(pd.Grouper(freq=av_Freq)).max() 
qc_Flag_EC = TCA_Data['qc_Flag_EC'].groupby(pd.Grouper(freq=av_Freq)).max() 
qc_Flag_CO2 = TCA_Data['qc_Flag_CO2'].groupby(pd.Grouper(freq=av_Freq)).max() 
TCA_Data = TCA_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
TCA_Data['qc_Flag_TC'] = pd.Series(qc_Flag_TC)
TCA_Data['qc_Flag_OC'] = pd.Series(qc_Flag_OC)
TCA_Data['qc_Flag_EC'] = pd.Series(qc_Flag_EC)
TCA_Data['qc_Flag_CO2'] = pd.Series(qc_Flag_CO2)

TCA_Data = TCA_Data.dropna(subset=['Total Carbon (ug/m3)'])

TCA_Data['qc_Flag_TC'] = TCA_Data['qc_Flag_TC'].astype(float)
TCA_Data['qc_Flag_OC'] = TCA_Data['qc_Flag_OC'].astype(float)
TCA_Data['qc_Flag_EC'] = TCA_Data['qc_Flag_EC'].astype(float)
TCA_Data['qc_Flag_CO2'] = TCA_Data['qc_Flag_CO2'].astype(float)

TCA_Data['qc_Flag_TC'] = TCA_Data['qc_Flag_TC'].astype(int)
TCA_Data['qc_Flag_OC'] = TCA_Data['qc_Flag_OC'].astype(int)
TCA_Data['qc_Flag_EC'] = TCA_Data['qc_Flag_EC'].astype(int)
TCA_Data['qc_Flag_CO2'] = TCA_Data['qc_Flag_CO2'].astype(int)

TCA_Data['qc_Flag_TC'] = TCA_Data['qc_Flag_TC'].astype(str)
TCA_Data['qc_Flag_OC'] = TCA_Data['qc_Flag_OC'].astype(str)
TCA_Data['qc_Flag_EC'] = TCA_Data['qc_Flag_EC'].astype(str)
TCA_Data['qc_Flag_CO2'] = TCA_Data['qc_Flag_CO2'].astype(str)

CO2_Data = TCA_Data[['Average CO2 (ppm)', 'qc_Flag_CO2']]

TCA_Data = TCA_Data.drop(columns=['Average CO2 (ppm)', 'qc_Flag_CO2'])

plt.plot(TCA_Data['Total Carbon (ug/m3)'], label='Total Carbon')
plt.plot(TCA_Data['Organic Carbon (ug/m3)'], label='Organic Carbon')
plt.plot(TCA_Data['Elemental Carbon (ug/m3)'], label='Elemental Carbon')
plt.legend()
plt.ylabel('ug/m3')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()


plt.plot(CO2_Data['Average CO2 (ppm)'], label='Average CO2')
plt.legend()
plt.ylabel('ppm')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

TCA_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/TCA/'
check_Folder = os.path.isdir(TCA_Folder)
if not check_Folder:
    os.makedirs(TCA_Folder)
    print("created folder : ", TCA_Folder)

else:
    print(TCA_Folder, "folder already exists.")

TCA_Data.to_csv(str(TCA_Folder) + 'TCA_maqs_' + str(date_file_label) + '_aerosol-carbon-content_' + str(validity_status) + '_' + str(version_number) + '.csv')
CO2_Data.to_csv(str(TCA_Folder) + 'TCA_maqs_' + str(date_file_label) + '_ambient-CO2-concentration_' + str(validity_status) + '_' + str(version_number) + '.csv')

TCA_Data['TimeDateSince'] = TCA_Data.index-datetime.datetime(1970,1,1,0,0,00)
TCA_Data['TimeSecondsSince'] = TCA_Data['TimeDateSince'].dt.total_seconds()
TCA_Data['day_year'] = pd.DatetimeIndex(TCA_Data['TimeDateSince'].index).dayofyear
TCA_Data['year'] = pd.DatetimeIndex(TCA_Data['TimeDateSince'].index).year
TCA_Data['month'] = pd.DatetimeIndex(TCA_Data['TimeDateSince'].index).month
TCA_Data['day'] = pd.DatetimeIndex(TCA_Data['TimeDateSince'].index).day
TCA_Data['hour'] = pd.DatetimeIndex(TCA_Data['TimeDateSince'].index).hour
TCA_Data['minute'] = pd.DatetimeIndex(TCA_Data['TimeDateSince'].index).minute
TCA_Data['second'] = pd.DatetimeIndex(TCA_Data['TimeDateSince'].index).second





