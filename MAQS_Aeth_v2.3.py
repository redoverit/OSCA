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
from datetime import date
import datetime
import shutil
import os, sys

sample_Freq = '1min'
av_Freq = '1min' #averaging frequency required of the data
data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v2.3' #version of the code
year_start = 2022 #input the year of study by number
month_start = 12 #input the month of study by number
default_start_day = 1 #default start date set
day_start = default_start_day
validity_status = 'Ratified' #Ratified or Unratified
Source = 'Processed' #'Raw' or 'Processed'

status = np.where(validity_status == 'Unratified' , '_Unratified_', '_Ratified_')

today = date.today()
current_day = today.strftime("%Y%m%d")

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

date_file_label = np.where(start_year_month_str == end_year_month_str, start_year_month_str, str(start_year_month_str) + "-" + str(end_year_month_str))
#print(date_file_label) #print end date to check it is correct

full_file_label = str(start.strftime("%Y")) + str(start.strftime("%m"))

prior_date_1 = start - dateutil.relativedelta.relativedelta(days=1)
prior_data_yr = str(prior_date_1.strftime("%Y"))
prior_date_1_str = str(prior_date_1.strftime("%Y")) + str(prior_date_1.strftime("%m")) + str(prior_date_1.strftime("%d"))

later_date_1 = end + dateutil.relativedelta.relativedelta(days=1)
prior_data_yr = str(later_date_1.strftime("%Y")) 
later_date_1_str = str(later_date_1.strftime("%Y")) + str(later_date_1.strftime("%m")) + str(later_date_1.strftime("%d"))

print(start_year_month_str)

if float(start_year_month_str) < 201812:
    sys.exit("Error Message: This program cannot be used for data prior to December 2018.")

folder = np.where((str(version_number) == 'v0.6'), 'Preliminary', str(validity_status))

if str(Source) == 'Raw':
    AE33_Source = 'AE33-local'
    file_type = '.dat'
else:
    AE33_Source = 'Aethalometer'
    file_type = '.csv'
    
Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/' + str(AE33_Source) + '/', 'D:/FirsData/' + str(AE33_Source) + '/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(folder) + '_' + str(version_number) + '/', 'D:/' + str(folder) + '_' + str(version_number) + '/')

if str(Source) == 'Raw':
    Month_files = str(Data_Source_Folder) + str(year_start) + '/' + 'AE33_AE33-S07-00664_' + str(date_file_label) + '*' + str(file_type)
    Prior_File_1 = str(Data_Source_Folder) + str(prior_data_yr) + '/' + 'AE33_AE33-S07-00664_' + str(prior_date_1_str) + '*' + str(file_type)
    Later_File_1 = str(Data_Source_Folder) + str(later_date_1_str) + '/' + 'AE33_AE33-S07-00664_' + str(prior_date_1_str) + '*' + str(file_type)
else:
    if float(start_year_month_str) == 202106:
        Month_file_1 = str(Data_Source_Folder) + '2021060' + '*_Aeth' + str(file_type)
        Month_file_2 = str(Data_Source_Folder) + '2021061' + '*_Aeth' + str(file_type)
        Month_file_3 = str(Data_Source_Folder) + '2021062' + '*_Aeth' + str(file_type)
        Month_file_4 = str(Data_Source_Folder) + '2021063' + '*_Aeth' + str(file_type)
        Prior_File_1 = str(Data_Source_Folder) + str(prior_date_1_str) + '*_Aeth' + str(file_type)
        Later_File_1 = str(Data_Source_Folder) + str(later_date_1_str) + '*_Aeth' + str(file_type)
        csv_files = glob.glob(Prior_File_1) + glob.glob(Later_File_1) + glob.glob(Month_file_1) + glob.glob(Month_file_2) +  glob.glob(Month_file_3) + glob.glob(Month_file_4) #
    else:
        Month_files = str(Data_Source_Folder) + str(date_file_label) + '*_Aeth' + str(file_type)
        Prior_File_1 = str(Data_Source_Folder)  + str(prior_date_1_str) + '*_Aeth' + str(file_type)
        Later_File_1 = str(Data_Source_Folder)  + str(later_date_1_str) + '*_Aeth' + str(file_type)
        prior_file = str(Data_Source_Folder) + '202112180000_Aeth.csv'
        csv_files = glob.glob(prior_file) + glob.glob(Month_files) + glob.glob(Prior_File_1) + glob.glob(Later_File_1) 

#print(prior_date_1)

#July to November 2019
#November 2019 to March 2020
#March 2020 onwards
rows_to_skip = np.where(float(start_year_month_str) <202005, 1, 0)

frames = []
    
for csv in csv_files:
    csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv, skiprows=int(rows_to_skip), header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=False, na_filter=False) ##, usecols=[0,1,5,6,7,8,9,10,11,12]
    frames.append(df)
    
aeth_Data = pd.concat(frames)

aeth_Data.iloc[0] = aeth_Data.iloc[0].astype(str)
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '370.0', '370 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '470.0', '470 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '520.0', '520 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '590.0', '590 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '660.0', '660 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '880.0', '880 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '950.0', '950 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = aeth_Data.iloc[0].str.strip('l/min').astype(str)
aeth_Data.iloc[0] = aeth_Data.iloc[0].str.lstrip().astype(str)
aeth_Data.iloc[0] = aeth_Data.iloc[0].str.rstrip().astype(str)
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '370ng/m3', '370 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '470ng/m3', '470 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '520ng/m3', '520 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '590ng/m3', '590 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '660ng/m3', '660 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '880ng/m3', '880 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = np.where(aeth_Data.iloc[0] == '950ng/m3', '950 (ng/m3)', aeth_Data.iloc[0])
aeth_Data.iloc[0] = aeth_Data.iloc[0].astype(str)
aeth_Data.iloc[:,2] = aeth_Data.iloc[:,2].astype(str)
aeth_Data.iloc[:,2] = aeth_Data.iloc[:,2].str.lstrip().astype(str)
aeth_Data.iloc[:,2] = aeth_Data.iloc[:,2].str.rstrip().astype(str)

if float(start_year_month_str) == 202004:
    aeth_label_Data = aeth_Data
    aeth_label_Data['row number'] = aeth_label_Data.index
    aeth_label_Data = aeth_label_Data.transpose()
    aeth_label_Data.columns = aeth_label_Data.iloc[0]

    aeth_label_Data['Computer Date'] = aeth_label_Data['Computer Date'].astype(str)
    aeth_label_Data['Computer Date'] = aeth_label_Data['Computer Date'].str.lstrip().astype(str)
    aeth_label_Data['Computer Date'] = aeth_label_Data['Computer Date'].str.rstrip().astype(str)
    aeth_label_Data['Computer Date'] = aeth_label_Data['Computer Date'].str.strip(' l/min').astype(str)
    aeth_label_Data['Computer Date'] = np.where(aeth_label_Data['Computer Date'] == '370ng/m3', '370 (ng/m3)', aeth_label_Data['Computer Date'])
    aeth_label_Data['Computer Date'] = np.where(aeth_label_Data['Computer Date'] == '470ng/m3', '470 (ng/m3)', aeth_label_Data['Computer Date'])
    aeth_label_Data['Computer Date'] = np.where(aeth_label_Data['Computer Date'] == '520ng/m3', '520 (ng/m3)', aeth_label_Data['Computer Date'])
    aeth_label_Data['Computer Date'] = np.where(aeth_label_Data['Computer Date'] == '590ng/m3', '590 (ng/m3)', aeth_label_Data['Computer Date'])
    aeth_label_Data['Computer Date'] = np.where(aeth_label_Data['Computer Date'] == '660ng/m3', '660 (ng/m3)', aeth_label_Data['Computer Date'])
    aeth_label_Data['Computer Date'] = np.where(aeth_label_Data['Computer Date'] == '880ng/m3', '880 (ng/m3)', aeth_label_Data['Computer Date'])
    aeth_label_Data['Computer Date'] = np.where(aeth_label_Data['Computer Date'] == '950ng/m3', '950 (ng/m3)', aeth_label_Data['Computer Date'])
    aeth_label_Data.index = aeth_label_Data['Computer Date'] 
    aeth_label_Data = aeth_label_Data.transpose()

    aeth_label_Data.index = aeth_label_Data['0']
    aeth_label_Data = aeth_label_Data.drop(aeth_label_Data[aeth_label_Data['Computer Date'] == 'Computer Date'].index)
    aeth_label_Data = aeth_label_Data.drop(columns=['0'])
    aeth_Data = aeth_label_Data
else:
    aeth_Data.columns = aeth_Data.iloc[0]

#print(aeth_Data.columns)

#aeth_Data.to_csv(str(Data_Output_Folder) + 'maqs-AE33-1-' + str(date_file_label) + '-black_carbon-concentration' + str(status) + str(version_number) + '.csv')

aeth_Data['Title_Flag'] = np.where(aeth_Data['Serial No']== 'Serial No', 1, 0)
aeth_Data['Title_Flag'] = np.where(aeth_Data['Instrument Date']== 'Instrument Date', 1, aeth_Data['Title_Flag'])
aeth_Data['Title_Flag'] = np.where(aeth_Data['Instrument Time']== 'Instrument Time', 1, aeth_Data['Title_Flag'])
aeth_Data = aeth_Data.drop(aeth_Data[aeth_Data['Serial No'] == ''].index)
aeth_Data = aeth_Data.drop(aeth_Data[aeth_Data['Instrument Date'] == ''].index)
aeth_Data = aeth_Data.drop(aeth_Data[aeth_Data['Instrument Date'] == ''].index)
aeth_Data['Serial No'] = aeth_Data['Serial No'].replace('', np.nan, inplace=True)
aeth_Data['Instrument Date'] = aeth_Data['Instrument Date'].replace('', np.nan, inplace=True)
aeth_Data['Instrument Time'] = aeth_Data['Instrument Time'].replace('', np.nan, inplace=True)
aeth_Data = aeth_Data.drop(aeth_Data[aeth_Data.Title_Flag == 1].index)
aeth_Data = aeth_Data.drop(aeth_Data[aeth_Data['air flow'] == 'air flow'].index)
aeth_Data = aeth_Data.drop(aeth_Data[aeth_Data['air flow'] == ' air flow'].index)

aeth_Data = aeth_Data.drop(columns=['Title_Flag', 'Serial No', 'Instrument Time', 'Instrument Date'])

aeth_Data.columns.values[0] = 'Computer Date'
aeth_Data.columns.values[1] = 'Computer Time'

aeth_Data['Computer Date'] = aeth_Data['Computer Date'].astype(str)
aeth_Data['Computer Time'] = aeth_Data['Computer Time'].astype(str)
aeth_Data['Date_length'] = aeth_Data['Computer Date'].str.len()
aeth_Data['Time_length'] = aeth_Data['Computer Time'].str.len()
aeth_Data=aeth_Data[aeth_Data.Date_length > 6]
aeth_Data=aeth_Data[aeth_Data.Date_length < 12]
aeth_Data=aeth_Data[aeth_Data.Time_length == 8]

aeth_Data['datetime'] = aeth_Data['Computer Date'] + ' ' + aeth_Data['Computer Time']# added Date and time into new columns
aeth_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in aeth_Data['datetime']] #converts the dateTime format from string to python dateTime
aeth_Data.index = aeth_Data['datetime']
aeth_Data = aeth_Data.sort_index()
aeth_Data = aeth_Data[start:end]
aeth_Data = aeth_Data.drop(columns=['Computer Time', 'Computer Date', 'datetime', 'Date_length', 'Time_length'])

if start_year_month_str == 201906:
    aeth_Data=aeth_Data.drop(aeth_Data.iloc[:, 44:], inplace=True, axis=1)
else:
    pass

start_Error5 = datetime.datetime(2019,6,17,22,13,00) #next audit
end_Error5 = datetime.datetime(2019,6,17,22,22,00)
aeth_Data.drop(aeth_Data.loc[start_Error5:end_Error5].index, inplace=True)

#aeth_Data.iloc[:,44:49] = aeth_Data.iloc[:,44:49].astype(float)
#print(aeth_Data.iloc[1200:1250])

#aeth_Data[:3000] = aeth_Data[:3000].astype(float)


aeth_Data.rename(columns={0: '370 (ng/m3)',1: '470 (ng/m3)', 2 :'520 (ng/m3)', 3 : '590 (ng/m3)', 4 : '660 (ng/m3)' }, inplace = True)
aeth_Data.rename(columns={5 :'880 (ng/m3)',6 : '950 (ng/m3)', 'air flow' :'Air_Flow'}, inplace = True)

aeth_Data = aeth_Data[['370 (ng/m3)','470 (ng/m3)','520 (ng/m3)','590 (ng/m3)','660 (ng/m3)', '880 (ng/m3)', '950 (ng/m3)','Air_Flow']]

aeth_Data['Zero_Flag'] = np.where(aeth_Data['370 (ng/m3)'] == 0, 1, 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['470 (ng/m3)'] == 0, aeth_Data['Zero_Flag'], 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['520 (ng/m3)'] == 0, aeth_Data['Zero_Flag'], 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['590 (ng/m3)'] == 0, aeth_Data['Zero_Flag'], 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['660 (ng/m3)'] == 0, aeth_Data['Zero_Flag'], 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['880 (ng/m3)'] == 0, aeth_Data['Zero_Flag'], 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['950 (ng/m3)'] == 0, aeth_Data['Zero_Flag'], 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['370 (ng/m3)'].isnull() , aeth_Data['Zero_Flag'], 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['470 (ng/m3)'].isnull() , aeth_Data['Zero_Flag'], 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['520 (ng/m3)'].isnull() , aeth_Data['Zero_Flag'], 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['590 (ng/m3)'].isnull() , aeth_Data['Zero_Flag'], 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['660 (ng/m3)'].isnull() , aeth_Data['Zero_Flag'], 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['880 (ng/m3)'].isnull() , aeth_Data['Zero_Flag'], 2)
aeth_Data['Zero_Flag'] = np.where(aeth_Data['950 (ng/m3)'].isnull() , aeth_Data['Zero_Flag'], 2)

aeth_Data.drop(aeth_Data[(aeth_Data['Zero_Flag'] == 1)].index,inplace =True)

aeth_Data = aeth_Data.drop(aeth_Data[aeth_Data.Air_Flow == 0].index)

aeth_Data['Air_Flow'] = aeth_Data['Air_Flow'].astype(float)
aeth_Data['Air_Flow_Flag'] = np.where(aeth_Data['Air_Flow'] < 4.9, 3, 1)
aeth_Data['Air_Flow_Flag'] = np.where(aeth_Data['Air_Flow'] > 5.1, 3, aeth_Data['Air_Flow_Flag'])
#aeth_Data['Air_Flow_Flag'] = np.where(aeth_Data['Air_Flow'] != 5, 3, 1)

start_Simon_1 = datetime.datetime(2018,12,18,0,0,00) # logging in simon building
end_Simon_1 = datetime.datetime(2019,1,29,12,37,00) 
#aeth_Data.loc[start_Simon_1:end_Simon_1, ('MultiCarbon_Flag')] = "2"

start_move_1 = datetime.datetime(2019,1,29,12,38,00) # moving to firs
end_move_1 = datetime.datetime(2019,1,29,23,32,00)
aeth_Data.loc[start_move_1:end_move_1, ('Air_Flow_Flag')] = 2

start_move_2 = datetime.datetime(2019,6,12,7,10,00) # moved aethelometre
end_move_2 = datetime.datetime(2019,6,12,21,51,00)
aeth_Data.loc[start_move_2:end_move_2, ('Air_Flow_Flag')] = 2

start_Error1 = datetime.datetime(2019,10,30,16,26,00)
end_Error1 = datetime.datetime(2019,10,31,9,39,00)
#aeth_Data.drop(aeth_Data.loc[start_Error1:end_Error1].index, inplace=True)

start_Error2 = datetime.datetime(2019,5,6,9,0,00) #next audit
end_Error2 = datetime.datetime(2019,5,6,19,0,00)
aeth_Data.drop(aeth_Data.loc[start_Error2:end_Error2].index, inplace=True)

start_Error3 = datetime.datetime(2019,5,7,12,0,00) 
end_Error3 = datetime.datetime(2019,5,7,15,0,00)
aeth_Data.drop(aeth_Data.loc[start_Error3:end_Error3].index, inplace=True)

start_Error4 = datetime.datetime(2019,5,8,9,0,00) 
end_Error4 = datetime.datetime(2019,5,8,10,30,00)
aeth_Data.drop(aeth_Data.loc[start_Error4:end_Error4].index, inplace=True)

start_Error6 = datetime.datetime(2020,5,12,6,50,00)
end_Error6 = datetime.datetime(2020,5,12,7,5,00)
aeth_Data.drop(aeth_Data.loc[start_Error6:end_Error6].index, inplace=True)

start_Clean1 = datetime.datetime(2022,10,4,10,10,00) #cleaning denuder
end_Clean1 = datetime.datetime(2022,10,4,10,50,00)
aeth_Data.drop(aeth_Data.loc[start_Clean1:end_Clean1].index, inplace=True)
#aeth_Data.loc[start_Clean1:end_Clean1, ('Air_Flow_Flag')] = 2

start_Clean2 = datetime.datetime(2022,10,4,8,0,00) #cleaning denuder
end_Clean2 = datetime.datetime(2022,10,4,8,30,00)
aeth_Data.loc[start_Clean2:end_Clean2, ('Air_Flow_Flag')] = 2

start_Clean3 = datetime.datetime(2022,12,5,13,0,00) #cleaning denuder
end_Clean3 = datetime.datetime(2022,12,5,13,30,00)
aeth_Data.loc[start_Clean3:end_Clean3, ('Air_Flow_Flag')] = 2

#aeth_Data['Air_Flow_Flag'] = np.where(aeth_Data['Air_Flow'] == 5, aeth_Data['Air_Flow_Flag'], 2)

aeth_Data['370 (ng/m3)'] = aeth_Data['370 (ng/m3)'].astype(float)
aeth_Data['470 (ng/m3)'] = aeth_Data['470 (ng/m3)'].astype(float)
aeth_Data['520 (ng/m3)'] = aeth_Data['520 (ng/m3)'].astype(float)
aeth_Data['590 (ng/m3)'] = aeth_Data['590 (ng/m3)'].astype(float)
aeth_Data['660 (ng/m3)'] = aeth_Data['660 (ng/m3)'].astype(float)
aeth_Data['880 (ng/m3)'] = aeth_Data['880 (ng/m3)'].astype(float)
aeth_Data['950 (ng/m3)'] = aeth_Data['950 (ng/m3)'].astype(float)

aeth_Data['qc_flag_UVPM'] = np.where(aeth_Data['370 (ng/m3)'] == 0, 2, aeth_Data['Air_Flow_Flag'])
aeth_Data['qc_flag_BC_470'] = np.where(aeth_Data['470 (ng/m3)'] == 0, 2, aeth_Data['Air_Flow_Flag'])
aeth_Data['qc_flag_BC_520'] = np.where(aeth_Data['520 (ng/m3)'] == 0, 2, aeth_Data['Air_Flow_Flag'])
aeth_Data['qc_flag_BC_590'] = np.where(aeth_Data['590 (ng/m3)'] == 0, 2, aeth_Data['Air_Flow_Flag'])
aeth_Data['qc_flag_BC_660'] = np.where(aeth_Data['660 (ng/m3)'] == 0, 2, aeth_Data['Air_Flow_Flag'])
aeth_Data['qc_flag_BC'] = np.where(aeth_Data['880 (ng/m3)'] == 0, 2, aeth_Data['Air_Flow_Flag'])
aeth_Data['qc_flag_BC_950'] = np.where(aeth_Data['950 (ng/m3)'] == 0, 2, aeth_Data['Air_Flow_Flag'])

aeth_Data['Null_Flag'] = np.where(aeth_Data['370 (ng/m3)'].isnull() , 3, 1)
aeth_Data['Null_Flag'] = np.where(aeth_Data['470 (ng/m3)'].isnull() , aeth_Data['Null_Flag'], 1)
aeth_Data['Null_Flag'] = np.where(aeth_Data['520 (ng/m3)'].isnull() , aeth_Data['Null_Flag'], 1)
aeth_Data['Null_Flag'] = np.where(aeth_Data['590 (ng/m3)'].isnull() , aeth_Data['Null_Flag'], 1)
aeth_Data['Null_Flag'] = np.where(aeth_Data['660 (ng/m3)'].isnull() , aeth_Data['Null_Flag'], 1)
aeth_Data['Null_Flag'] = np.where(aeth_Data['880 (ng/m3)'].isnull() , aeth_Data['Null_Flag'], 1)
aeth_Data['Null_Flag'] = np.where(aeth_Data['950 (ng/m3)'].isnull() , aeth_Data['Null_Flag'], 1)

aeth_Data.drop(aeth_Data[(aeth_Data['Zero_Flag'] == 1)].index,inplace =True)
aeth_Data.drop(aeth_Data[(aeth_Data['370 (ng/m3)']== 0)].index,inplace =True)
aeth_Data.drop(aeth_Data[(aeth_Data['Null_Flag'] == 3)].index,inplace =True)

aeth_Data = aeth_Data.drop(columns=['Air_Flow', 'Zero_Flag', 'Null_Flag'])

UVPM_Flag = aeth_Data['qc_flag_UVPM'].groupby(pd.Grouper(freq=av_Freq)).max()
BC_470_Flag = aeth_Data['qc_flag_BC_470'].groupby(pd.Grouper(freq=av_Freq)).max()
BC_520_Flag = aeth_Data['qc_flag_BC_520'].groupby(pd.Grouper(freq=av_Freq)).max()
BC_590_Flag = aeth_Data['qc_flag_BC_590'].groupby(pd.Grouper(freq=av_Freq)).max()
BC_660_Flag = aeth_Data['qc_flag_BC_660'].groupby(pd.Grouper(freq=av_Freq)).max()
BC_Flag = aeth_Data['qc_flag_BC'].groupby(pd.Grouper(freq=av_Freq)).max()
BC_950_Flag = aeth_Data['qc_flag_BC_950'].groupby(pd.Grouper(freq=av_Freq)).max()

aeth_Data[:] = aeth_Data[:].astype(float)

aeth_Data = aeth_Data.groupby(pd.Grouper(freq=av_Freq)).mean()

aeth_Data['qc_flag_UVPM'] = pd.Series(UVPM_Flag) 
aeth_Data['qc_flag_BC_470'] = pd.Series(BC_470_Flag) 
aeth_Data['qc_flag_BC_520'] = pd.Series(BC_520_Flag) 
aeth_Data['qc_flag_BC_590'] = pd.Series(BC_590_Flag) 
aeth_Data['qc_flag_BC_660'] = pd.Series(BC_660_Flag) 
aeth_Data['qc_flag_BC'] = pd.Series(BC_Flag) 
aeth_Data['qc_flag_BC_950'] = pd.Series(BC_950_Flag) 

aeth_Data.drop(aeth_Data[(aeth_Data['370 (ng/m3)'].isnull() & aeth_Data['470 (ng/m3)'].isnull() & aeth_Data['520 (ng/m3)'].isnull() & aeth_Data['590 (ng/m3)'].isnull() & aeth_Data['660 (ng/m3)'].isnull() & aeth_Data['880 (ng/m3)'].isnull() & aeth_Data['950 (ng/m3)'].isnull() )].index,inplace =True)

aeth_Data.rename(columns={'880 (ng/m3)': 'BC Conc (ng/m3)','370 (ng/m3)': 'UVPM_370_nm (ng/m3)' }, inplace = True)
aeth_Data.rename(columns={'470 (ng/m3)': 'BC_470 (ng/m3)','520 (ng/m3)': 'BC_520 (ng/m3)' }, inplace = True)
aeth_Data.rename(columns={'590 (ng/m3)': 'BC_590 (ng/m3)','660 (ng/m3)': 'BC_660 (ng/m3)' }, inplace = True)
aeth_Data.rename(columns={'950 (ng/m3)': 'BC_950 (ng/m3)'}, inplace = True)

#aeth_Nov_2019 = aeth_Data[starta:enda]
#aeth_Nov_2020 = aeth_Data[startb:endb]

aeth_Data=aeth_Data[['BC Conc (ng/m3)', 'UVPM_370_nm (ng/m3)', 'BC_470 (ng/m3)', 'BC_520 (ng/m3)', 'BC_590 (ng/m3)', 'BC_660 (ng/m3)', 'BC_950 (ng/m3)', 'qc_flag_BC','qc_flag_UVPM','qc_flag_BC_470','qc_flag_BC_520','qc_flag_BC_590','qc_flag_BC_660','qc_flag_BC_950' ]]

aeth_Data['qc_flag_BC'] = np.where((aeth_Data['BC Conc (ng/m3)'] < 10) | (aeth_Data['BC Conc (ng/m3)'] > 100000), 2, aeth_Data['qc_flag_BC'])
aeth_Data['qc_flag_UVPM'] = np.where((aeth_Data['UVPM_370_nm (ng/m3)'] < 10) | (aeth_Data['UVPM_370_nm (ng/m3)'] > 100000), 2, aeth_Data['qc_flag_UVPM'])
aeth_Data['qc_flag_BC_470'] = np.where((aeth_Data['BC_470 (ng/m3)'] < 10) | (aeth_Data['BC_470 (ng/m3)'] > 100000), 2, aeth_Data['qc_flag_BC_470'])
aeth_Data['qc_flag_BC_520'] = np.where((aeth_Data['BC_520 (ng/m3)'] < 10) | (aeth_Data['BC_520 (ng/m3)'] > 100000), 2, aeth_Data['qc_flag_BC_520'])
aeth_Data['qc_flag_BC_590'] = np.where((aeth_Data['BC_590 (ng/m3)'] < 10) | (aeth_Data['BC_590 (ng/m3)'] > 100000), 2, aeth_Data['qc_flag_BC_590'])
aeth_Data['qc_flag_BC_660'] = np.where((aeth_Data['BC_660 (ng/m3)'] < 10) | (aeth_Data['BC_660 (ng/m3)'] > 100000), 2, aeth_Data['qc_flag_BC_660'])
aeth_Data['qc_flag_BC_950'] = np.where((aeth_Data['BC_950 (ng/m3)'] < 10) | (aeth_Data['BC_950 (ng/m3)'] > 100000), 2, aeth_Data['qc_flag_BC_950'])

upper_flag = 100000

aeth_Data['qc_flag_BC'] = np.where((aeth_Data['BC Conc (ng/m3)'] > float(upper_flag)), 2, aeth_Data['qc_flag_BC'])
aeth_Data['qc_flag_UVPM'] = np.where( (aeth_Data['UVPM_370_nm (ng/m3)'] > float(upper_flag)), 2, aeth_Data['qc_flag_UVPM'])
aeth_Data['qc_flag_BC_470'] = np.where( (aeth_Data['BC_470 (ng/m3)'] > float(upper_flag)), 2, aeth_Data['qc_flag_BC_470'])
aeth_Data['qc_flag_BC_520'] = np.where((aeth_Data['BC_520 (ng/m3)'] > float(upper_flag)), 2, aeth_Data['qc_flag_BC_520'])
aeth_Data['qc_flag_BC_590'] = np.where((aeth_Data['BC_590 (ng/m3)'] > float(upper_flag)), 2, aeth_Data['qc_flag_BC_590'])
aeth_Data['qc_flag_BC_660'] = np.where((aeth_Data['BC_660 (ng/m3)'] > float(upper_flag)), 2, aeth_Data['qc_flag_BC_660'])
aeth_Data['qc_flag_BC_950'] = np.where((aeth_Data['BC_950 (ng/m3)'] > float(upper_flag)), 2, aeth_Data['qc_flag_BC_950'])

flag_name_1 = 'qc_flag_BC'
flag_name_2 = 'qc_flag_UVPM'
flag_name_3 = 'qc_flag_BC_470'
flag_name_4 = 'qc_flag_BC_520'
flag_name_5 = 'qc_flag_BC_590'
flag_name_6 = 'qc_flag_BC_660'
flag_name_7 = 'qc_flag_BC_950'

current_flag_name = str(flag_name_1)
aeth_Data['Flag_-1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-1)
aeth_Data['Flag_-2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-2)
aeth_Data['Flag_-3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-3)
aeth_Data['Flag_-4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-4)
aeth_Data['Flag_-5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-5)
aeth_Data['Flag_-6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-6)
aeth_Data['Flag_+1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=1)
aeth_Data['Flag_+2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=2)
aeth_Data['Flag_+3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=3)
aeth_Data['Flag_+4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=4)
aeth_Data['Flag_+5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=5)
aeth_Data['Flag_+6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=6)
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-6_offset']!= 1) & (aeth_Data['Flag_-6_offset'].notnull() ) ,aeth_Data['Flag_-6_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-5_offset']!= 1) & (aeth_Data['Flag_-5_offset'].notnull() ) ,aeth_Data['Flag_-5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-4_offset']!= 1) & (aeth_Data['Flag_-4_offset'].notnull() ) ,aeth_Data['Flag_-4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-3_offset']!= 1) & (aeth_Data['Flag_-3_offset'].notnull() ) ,aeth_Data['Flag_-3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-2_offset']!= 1) & (aeth_Data['Flag_-2_offset'].notnull() ) ,aeth_Data['Flag_-2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-1_offset']!= 1) & (aeth_Data['Flag_-1_offset'].notnull() ) ,aeth_Data['Flag_-1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+1_offset']!= 1) & (aeth_Data['Flag_+1_offset'].notnull() ) ,aeth_Data['Flag_+1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+2_offset']!= 1) & (aeth_Data['Flag_+2_offset'].notnull() ) ,aeth_Data['Flag_+2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+3_offset']!= 1) & (aeth_Data['Flag_+3_offset'].notnull() ) ,aeth_Data['Flag_+3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+4_offset']!= 1) & (aeth_Data['Flag_+4_offset'].notnull() ) ,aeth_Data['Flag_+4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+5_offset']!= 1) & (aeth_Data['Flag_+5_offset'].notnull() ) ,aeth_Data['Flag_+5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+6_offset']!= 1) & (aeth_Data['Flag_+6_offset'].notnull() ) ,aeth_Data['Flag_+6_offset'],aeth_Data[str(current_flag_name)])

current_flag_name = str(flag_name_2)
aeth_Data['Flag_-1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-1)
aeth_Data['Flag_-2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-2)
aeth_Data['Flag_-3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-3)
aeth_Data['Flag_-4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-4)
aeth_Data['Flag_-5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-5)
aeth_Data['Flag_-6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-6)
aeth_Data['Flag_+1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=1)
aeth_Data['Flag_+2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=2)
aeth_Data['Flag_+3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=3)
aeth_Data['Flag_+4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=4)
aeth_Data['Flag_+5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=5)
aeth_Data['Flag_+6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=6)
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-6_offset']!= 1) & (aeth_Data['Flag_-6_offset'].notnull() ) ,aeth_Data['Flag_-6_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-5_offset']!= 1) & (aeth_Data['Flag_-5_offset'].notnull() ) ,aeth_Data['Flag_-5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-4_offset']!= 1) & (aeth_Data['Flag_-4_offset'].notnull() ) ,aeth_Data['Flag_-4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-3_offset']!= 1) & (aeth_Data['Flag_-3_offset'].notnull() ) ,aeth_Data['Flag_-3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-2_offset']!= 1) & (aeth_Data['Flag_-2_offset'].notnull() ) ,aeth_Data['Flag_-2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-1_offset']!= 1) & (aeth_Data['Flag_-1_offset'].notnull() ) ,aeth_Data['Flag_-1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+1_offset']!= 1) & (aeth_Data['Flag_+1_offset'].notnull() ) ,aeth_Data['Flag_+1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+2_offset']!= 1) & (aeth_Data['Flag_+2_offset'].notnull() ) ,aeth_Data['Flag_+2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+3_offset']!= 1) & (aeth_Data['Flag_+3_offset'].notnull() ) ,aeth_Data['Flag_+3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+4_offset']!= 1) & (aeth_Data['Flag_+4_offset'].notnull() ) ,aeth_Data['Flag_+4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+5_offset']!= 1) & (aeth_Data['Flag_+5_offset'].notnull() ) ,aeth_Data['Flag_+5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+6_offset']!= 1) & (aeth_Data['Flag_+6_offset'].notnull() ) ,aeth_Data['Flag_+6_offset'],aeth_Data[str(current_flag_name)])

current_flag_name = str(flag_name_3)
aeth_Data['Flag_-1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-1)
aeth_Data['Flag_-2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-2)
aeth_Data['Flag_-3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-3)
aeth_Data['Flag_-4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-4)
aeth_Data['Flag_-5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-5)
aeth_Data['Flag_-6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-6)
aeth_Data['Flag_+1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=1)
aeth_Data['Flag_+2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=2)
aeth_Data['Flag_+3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=3)
aeth_Data['Flag_+4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=4)
aeth_Data['Flag_+5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=5)
aeth_Data['Flag_+6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=6)
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-6_offset']!= 1) & (aeth_Data['Flag_-6_offset'].notnull() ) ,aeth_Data['Flag_-6_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-5_offset']!= 1) & (aeth_Data['Flag_-5_offset'].notnull() ) ,aeth_Data['Flag_-5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-4_offset']!= 1) & (aeth_Data['Flag_-4_offset'].notnull() ) ,aeth_Data['Flag_-4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-3_offset']!= 1) & (aeth_Data['Flag_-3_offset'].notnull() ) ,aeth_Data['Flag_-3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-2_offset']!= 1) & (aeth_Data['Flag_-2_offset'].notnull() ) ,aeth_Data['Flag_-2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-1_offset']!= 1) & (aeth_Data['Flag_-1_offset'].notnull() ) ,aeth_Data['Flag_-1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+1_offset']!= 1) & (aeth_Data['Flag_+1_offset'].notnull() ) ,aeth_Data['Flag_+1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+2_offset']!= 1) & (aeth_Data['Flag_+2_offset'].notnull() ) ,aeth_Data['Flag_+2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+3_offset']!= 1) & (aeth_Data['Flag_+3_offset'].notnull() ) ,aeth_Data['Flag_+3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+4_offset']!= 1) & (aeth_Data['Flag_+4_offset'].notnull() ) ,aeth_Data['Flag_+4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+5_offset']!= 1) & (aeth_Data['Flag_+5_offset'].notnull() ) ,aeth_Data['Flag_+5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+6_offset']!= 1) & (aeth_Data['Flag_+6_offset'].notnull() ) ,aeth_Data['Flag_+6_offset'],aeth_Data[str(current_flag_name)])

current_flag_name = str(flag_name_4)
aeth_Data['Flag_-1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-1)
aeth_Data['Flag_-2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-2)
aeth_Data['Flag_-3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-3)
aeth_Data['Flag_-4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-4)
aeth_Data['Flag_-5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-5)
aeth_Data['Flag_-6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-6)
aeth_Data['Flag_+1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=1)
aeth_Data['Flag_+2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=2)
aeth_Data['Flag_+3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=3)
aeth_Data['Flag_+4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=4)
aeth_Data['Flag_+5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=5)
aeth_Data['Flag_+6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=6)
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-6_offset']!= 1) & (aeth_Data['Flag_-6_offset'].notnull() ) ,aeth_Data['Flag_-6_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-5_offset']!= 1) & (aeth_Data['Flag_-5_offset'].notnull() ) ,aeth_Data['Flag_-5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-4_offset']!= 1) & (aeth_Data['Flag_-4_offset'].notnull() ) ,aeth_Data['Flag_-4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-3_offset']!= 1) & (aeth_Data['Flag_-3_offset'].notnull() ) ,aeth_Data['Flag_-3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-2_offset']!= 1) & (aeth_Data['Flag_-2_offset'].notnull() ) ,aeth_Data['Flag_-2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-1_offset']!= 1) & (aeth_Data['Flag_-1_offset'].notnull() ) ,aeth_Data['Flag_-1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+1_offset']!= 1) & (aeth_Data['Flag_+1_offset'].notnull() ) ,aeth_Data['Flag_+1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+2_offset']!= 1) & (aeth_Data['Flag_+2_offset'].notnull() ) ,aeth_Data['Flag_+2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+3_offset']!= 1) & (aeth_Data['Flag_+3_offset'].notnull() ) ,aeth_Data['Flag_+3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+4_offset']!= 1) & (aeth_Data['Flag_+4_offset'].notnull() ) ,aeth_Data['Flag_+4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+5_offset']!= 1) & (aeth_Data['Flag_+5_offset'].notnull() ) ,aeth_Data['Flag_+5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+6_offset']!= 1) & (aeth_Data['Flag_+6_offset'].notnull() ) ,aeth_Data['Flag_+6_offset'],aeth_Data[str(current_flag_name)])

current_flag_name = str(flag_name_5)
aeth_Data['Flag_-1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-1)
aeth_Data['Flag_-2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-2)
aeth_Data['Flag_-3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-3)
aeth_Data['Flag_-4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-4)
aeth_Data['Flag_-5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-5)
aeth_Data['Flag_-6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-6)
aeth_Data['Flag_+1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=1)
aeth_Data['Flag_+2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=2)
aeth_Data['Flag_+3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=3)
aeth_Data['Flag_+4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=4)
aeth_Data['Flag_+5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=5)
aeth_Data['Flag_+6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=6)
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-6_offset']!= 1) & (aeth_Data['Flag_-6_offset'].notnull() ) ,aeth_Data['Flag_-6_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-5_offset']!= 1) & (aeth_Data['Flag_-5_offset'].notnull() ) ,aeth_Data['Flag_-5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-4_offset']!= 1) & (aeth_Data['Flag_-4_offset'].notnull() ) ,aeth_Data['Flag_-4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-3_offset']!= 1) & (aeth_Data['Flag_-3_offset'].notnull() ) ,aeth_Data['Flag_-3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-2_offset']!= 1) & (aeth_Data['Flag_-2_offset'].notnull() ) ,aeth_Data['Flag_-2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-1_offset']!= 1) & (aeth_Data['Flag_-1_offset'].notnull() ) ,aeth_Data['Flag_-1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+1_offset']!= 1) & (aeth_Data['Flag_+1_offset'].notnull() ) ,aeth_Data['Flag_+1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+2_offset']!= 1) & (aeth_Data['Flag_+2_offset'].notnull() ) ,aeth_Data['Flag_+2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+3_offset']!= 1) & (aeth_Data['Flag_+3_offset'].notnull() ) ,aeth_Data['Flag_+3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+4_offset']!= 1) & (aeth_Data['Flag_+4_offset'].notnull() ) ,aeth_Data['Flag_+4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+5_offset']!= 1) & (aeth_Data['Flag_+5_offset'].notnull() ) ,aeth_Data['Flag_+5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+6_offset']!= 1) & (aeth_Data['Flag_+6_offset'].notnull() ) ,aeth_Data['Flag_+6_offset'],aeth_Data[str(current_flag_name)])

current_flag_name = str(flag_name_6)
aeth_Data['Flag_-1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-1)
aeth_Data['Flag_-2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-2)
aeth_Data['Flag_-3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-3)
aeth_Data['Flag_-4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-4)
aeth_Data['Flag_-5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-5)
aeth_Data['Flag_-6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-6)
aeth_Data['Flag_+1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=1)
aeth_Data['Flag_+2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=2)
aeth_Data['Flag_+3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=3)
aeth_Data['Flag_+4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=4)
aeth_Data['Flag_+5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=5)
aeth_Data['Flag_+6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=6)
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-6_offset']!= 1) & (aeth_Data['Flag_-6_offset'].notnull() ) ,aeth_Data['Flag_-6_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-5_offset']!= 1) & (aeth_Data['Flag_-5_offset'].notnull() ) ,aeth_Data['Flag_-5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-4_offset']!= 1) & (aeth_Data['Flag_-4_offset'].notnull() ) ,aeth_Data['Flag_-4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-3_offset']!= 1) & (aeth_Data['Flag_-3_offset'].notnull() ) ,aeth_Data['Flag_-3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-2_offset']!= 1) & (aeth_Data['Flag_-2_offset'].notnull() ) ,aeth_Data['Flag_-2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-1_offset']!= 1) & (aeth_Data['Flag_-1_offset'].notnull() ) ,aeth_Data['Flag_-1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+1_offset']!= 1) & (aeth_Data['Flag_+1_offset'].notnull() ) ,aeth_Data['Flag_+1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+2_offset']!= 1) & (aeth_Data['Flag_+2_offset'].notnull() ) ,aeth_Data['Flag_+2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+3_offset']!= 1) & (aeth_Data['Flag_+3_offset'].notnull() ) ,aeth_Data['Flag_+3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+4_offset']!= 1) & (aeth_Data['Flag_+4_offset'].notnull() ) ,aeth_Data['Flag_+4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+5_offset']!= 1) & (aeth_Data['Flag_+5_offset'].notnull() ) ,aeth_Data['Flag_+5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+6_offset']!= 1) & (aeth_Data['Flag_+6_offset'].notnull() ) ,aeth_Data['Flag_+6_offset'],aeth_Data[str(current_flag_name)])

current_flag_name = str(flag_name_7)
aeth_Data['Flag_-1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-1)
aeth_Data['Flag_-2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-2)
aeth_Data['Flag_-3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-3)
aeth_Data['Flag_-4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-4)
aeth_Data['Flag_-5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-5)
aeth_Data['Flag_-6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=-6)
aeth_Data['Flag_+1_offset'] = aeth_Data[str(current_flag_name)].shift(periods=1)
aeth_Data['Flag_+2_offset'] = aeth_Data[str(current_flag_name)].shift(periods=2)
aeth_Data['Flag_+3_offset'] = aeth_Data[str(current_flag_name)].shift(periods=3)
aeth_Data['Flag_+4_offset'] = aeth_Data[str(current_flag_name)].shift(periods=4)
aeth_Data['Flag_+5_offset'] = aeth_Data[str(current_flag_name)].shift(periods=5)
aeth_Data['Flag_+6_offset'] = aeth_Data[str(current_flag_name)].shift(periods=6)
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-6_offset']!= 1) & (aeth_Data['Flag_-6_offset'].notnull() ) ,aeth_Data['Flag_-6_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-5_offset']!= 1) & (aeth_Data['Flag_-5_offset'].notnull() ) ,aeth_Data['Flag_-5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-4_offset']!= 1) & (aeth_Data['Flag_-4_offset'].notnull() ) ,aeth_Data['Flag_-4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-3_offset']!= 1) & (aeth_Data['Flag_-3_offset'].notnull() ) ,aeth_Data['Flag_-3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-2_offset']!= 1) & (aeth_Data['Flag_-2_offset'].notnull() ) ,aeth_Data['Flag_-2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_-1_offset']!= 1) & (aeth_Data['Flag_-1_offset'].notnull() ) ,aeth_Data['Flag_-1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+1_offset']!= 1) & (aeth_Data['Flag_+1_offset'].notnull() ) ,aeth_Data['Flag_+1_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+2_offset']!= 1) & (aeth_Data['Flag_+2_offset'].notnull() ) ,aeth_Data['Flag_+2_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+3_offset']!= 1) & (aeth_Data['Flag_+3_offset'].notnull() ) ,aeth_Data['Flag_+3_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+4_offset']!= 1) & (aeth_Data['Flag_+4_offset'].notnull() ) ,aeth_Data['Flag_+4_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+5_offset']!= 1) & (aeth_Data['Flag_+5_offset'].notnull() ) ,aeth_Data['Flag_+5_offset'],aeth_Data[str(current_flag_name)])
aeth_Data[str(current_flag_name)] = np.where((aeth_Data['Flag_+6_offset']!= 1) & (aeth_Data['Flag_+6_offset'].notnull() ) ,aeth_Data['Flag_+6_offset'],aeth_Data[str(current_flag_name)])

aeth_Data=aeth_Data[['BC Conc (ng/m3)', 'UVPM_370_nm (ng/m3)', 'BC_470 (ng/m3)', 'BC_520 (ng/m3)', 'BC_590 (ng/m3)', 'BC_660 (ng/m3)', 'BC_950 (ng/m3)', 'qc_flag_BC','qc_flag_UVPM','qc_flag_BC_470','qc_flag_BC_520','qc_flag_BC_590','qc_flag_BC_660','qc_flag_BC_950' ]]

aeth_Data.rename(columns={'BC Conc (ng/m3)': 'BC Conc (ug/m3)', 'UVPM_370_nm (ng/m3)' : 'UVPM_370_nm (ug/m3)' }, inplace = True)
aeth_Data.rename(columns={'BC_470 (ng/m3)' : 'BC_470 (ug/m3)', 'BC_520 (ng/m3)' : 'BC_520 (ug/m3)' }, inplace = True)
aeth_Data.rename(columns={'BC_590 (ng/m3)' : 'BC_590 (ug/m3)','BC_660 (ng/m3)' : 'BC_660 (ug/m3)' }, inplace = True)
aeth_Data.rename(columns={'BC_950 (ng/m3)' : 'BC_950 (ug/m3)'}, inplace = True)

aeth_Data['BC Conc (ug/m3)'] = aeth_Data['BC Conc (ug/m3)']/1000
aeth_Data['UVPM_370_nm (ug/m3)'] = aeth_Data['UVPM_370_nm (ug/m3)']/1000
aeth_Data['BC_470 (ug/m3)'] = aeth_Data['BC_470 (ug/m3)']/1000
aeth_Data['BC_520 (ug/m3)'] = aeth_Data['BC_520 (ug/m3)']/1000
aeth_Data['BC_590 (ug/m3)'] = aeth_Data['BC_590 (ug/m3)']/1000
aeth_Data['BC_660 (ug/m3)' ] = aeth_Data['BC_660 (ug/m3)']/1000
aeth_Data['BC_950 (ug/m3)'] = aeth_Data['BC_950 (ug/m3)']/1000

aeth_Data['qc_flag_BC'] = aeth_Data['qc_flag_BC'].astype(float)
aeth_Data['qc_flag_UVPM'] = aeth_Data['qc_flag_UVPM'].astype(float)
aeth_Data['qc_flag_BC_470'] = aeth_Data['qc_flag_BC_470'].astype(float)
aeth_Data['qc_flag_BC_520'] = aeth_Data['qc_flag_BC_520'].astype(float)
aeth_Data['qc_flag_BC_590'] = aeth_Data['qc_flag_BC_590'].astype(float)
aeth_Data['qc_flag_BC_660'] = aeth_Data['qc_flag_BC_660'].astype(float)
aeth_Data['qc_flag_BC_950'] = aeth_Data['qc_flag_BC_950'].astype(float)

aeth_Data['qc_flag_BC'] = aeth_Data['qc_flag_BC'].astype(int)
aeth_Data['qc_flag_UVPM'] = aeth_Data['qc_flag_UVPM'].astype(int)
aeth_Data['qc_flag_BC_470'] = aeth_Data['qc_flag_BC_470'].astype(int)
aeth_Data['qc_flag_BC_520'] = aeth_Data['qc_flag_BC_520'].astype(int)
aeth_Data['qc_flag_BC_590'] = aeth_Data['qc_flag_BC_590'].astype(int)
aeth_Data['qc_flag_BC_660'] = aeth_Data['qc_flag_BC_660'].astype(int)
aeth_Data['qc_flag_BC_950'] = aeth_Data['qc_flag_BC_950'].astype(int)

aeth_Data['qc_flag_BC'] = aeth_Data['qc_flag_BC'].astype(str)
aeth_Data['qc_flag_UVPM'] = aeth_Data['qc_flag_UVPM'].astype(str)
aeth_Data['qc_flag_BC_470'] = aeth_Data['qc_flag_BC_470'].astype(str)
aeth_Data['qc_flag_BC_520'] = aeth_Data['qc_flag_BC_520'].astype(str)
aeth_Data['qc_flag_BC_590'] = aeth_Data['qc_flag_BC_590'].astype(str)
aeth_Data['qc_flag_BC_660'] = aeth_Data['qc_flag_BC_660'].astype(str)
aeth_Data['qc_flag_BC_950'] = aeth_Data['qc_flag_BC_950'].astype(str)

plt.plot(aeth_Data['BC Conc (ug/m3)'], label='BC')
plt.plot(aeth_Data['UVPM_370_nm (ug/m3)'], label='UVPM')
#plt.plot(aeth_Data['BC_470 (ug/m3)'], label='BC_470 (ug/m3)')
plt.legend()
plt.xlabel('Date and Time')
plt.ylabel('Abundance (ug/m^3)')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()


#plt.plot(aeth_Data['BC_520 (ug/m3)'], label='BC_520 (ug/m3)')
#plt.plot(aeth_Data['BC_590 (ug/m3)'], label='BC_590 (ug/m3)')
#plt.plot(aeth_Data['BC_660 (ug/m3)'], label='BC_660 (ug/m3)')
#plt.plot(aeth_Data['BC_950 (ug/m3)'], label='BC_950 (ug/m3)')
#plt.legend()
#plt.ylabel('ug m-3')
#plt.rc('figure', figsize=(60, 100))
#font = {'family' : 'normal',
#        'weight' : 'bold',
#        'size'   : 12}

#plt.rc('font', **font)
#plt.ylim(10, 30)
#plt.figure()
#plt.show()

AE33_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/AE33/'
check_Folder = os.path.isdir(AE33_Folder)
if not check_Folder:
    os.makedirs(AE33_Folder)
    print("created folder : ", AE33_Folder)

else:
    print(AE33_Folder, "folder already exists.")

aeth_Data.to_csv(str(AE33_Folder) + 'AE33_maqs_' + str(date_file_label) + '_black-carbon-concentration' + str(status) + str(version_number) + '.csv')

aeth_Data['TimeDateSince'] = aeth_Data.index-datetime.datetime(1970,1,1,0,0,00)
aeth_Data['TimeSecondsSince'] = aeth_Data['TimeDateSince'].dt.total_seconds()
aeth_Data['day_year'] = pd.DatetimeIndex(aeth_Data['TimeDateSince'].index).dayofyear
aeth_Data['year'] = pd.DatetimeIndex(aeth_Data['TimeDateSince'].index).year
aeth_Data['month'] = pd.DatetimeIndex(aeth_Data['TimeDateSince'].index).month
aeth_Data['day'] = pd.DatetimeIndex(aeth_Data['TimeDateSince'].index).day
aeth_Data['hour'] = pd.DatetimeIndex(aeth_Data['TimeDateSince'].index).hour
aeth_Data['minute'] = pd.DatetimeIndex(aeth_Data['TimeDateSince'].index).minute
aeth_Data['second'] = pd.DatetimeIndex(aeth_Data['TimeDateSince'].index).second


