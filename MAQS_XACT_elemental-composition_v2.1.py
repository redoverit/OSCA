# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 09:27:33 2022

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

data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v2.1' #version of the code
year_start = 2022 #input the year of study
month_start = 12 #input the month of study
default_start_day = 1 #default start date set
day_start = default_start_day
validity_status = 'Ratified' #Ratified or Unratified
av_Freq = '60min' #averaging frequency required of the data
Correcting_Freq = '1min'
#PM2p5_and_PM10_Freq ='120min'
display_XACT_graphs = 'Yes' #'Yes' or 'No'
display_cal_graph = 'No' #'Yes' or 'No'
Flag_Error_Alarm = 'Yes' #'Yes' or 'No'
Flag_Elements_Alarm_Only = 'No' #'Yes' or 'No'

if Flag_Elements_Alarm_Only == 'Yes':
    Flag_Error_Alarm = 'No'
else:
    pass

status = np.where(validity_status == 'Unratified' , '-Unratified_', '-Ratified_')

PM2p5_Start = datetime.datetime(2020,12,2,0,0,00)

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

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/XACT/Process_Data_CSV/', 'D:/FirsData/XACT/Process_Data_CSV/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(validity_status) + '_' + str(version_number) + '/', 'D:/' + str(validity_status) + '_' + str(version_number) + '/')

prior_date_1 = start - timedelta(days=1)
prior_date_1_str = str(prior_date_1.strftime("%m")) + '_' + str(prior_date_1.strftime("%d")) + '_' + str(prior_date_1.strftime("%Y")) 

prior_date_2 = start - timedelta(days=2)
prior_date_2_str = str(prior_date_2.strftime("%m")) + '_' + str(prior_date_2.strftime("%d")) + '_' + str(prior_date_2.strftime("%Y")) 

later_date_1 = end + timedelta(days=1)
later_date_1_str = str(later_date_1.strftime("%m")) + '_' + str(later_date_1.strftime("%d")) + '_' + str(later_date_1.strftime("%Y")) 

later_date_2 = end + timedelta(days=2)
later_date_2_str = str(later_date_2.strftime("%m")) + '_' + str(later_date_2.strftime("%d")) + '_' + str(later_date_2.strftime("%Y")) 

folder = str(validity_status)
print("using a " + str(folder) + "_" + str(version_number) + " folder")

Prior_File_1 = str(Data_Source_Folder) + 'Sample_' + str(prior_date_1_str) + '*.csv'
Prior_File_2 = str(Data_Source_Folder) + 'Sample_' + str(prior_date_2_str) + '*.csv'
Later_File_1 = str(Data_Source_Folder) + 'Sample_' + str(later_date_1_str) + '*.csv'
Later_File_2 = str(Data_Source_Folder) + 'Sample_' + str(later_date_2_str) + '*.csv'

Month_files = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '*' +  str(start.strftime("%Y")) + '*.csv' # Needs to be address of data location - Collect CSV files
print(str(Month_files))

if int(start_year_month_str) < 201907:
    sys.exit("Error Message: no data exists prior to July 2019")
elif int(start_year_month_str) == 202010:
    sys.exit("Error Message: no data exists for October 2020")
else:
    pass

XACT_csv_files = glob.glob(Month_files) + glob.glob(Prior_File_1) + glob.glob(Prior_File_2) + glob.glob(Later_File_1) + glob.glob(Later_File_2)

xactcsv_frames = []

if int(start_year_month_str) < 202010:
    for csv in XACT_csv_files:
        df = pd.read_csv(csv, usecols=[*range(0, 159)], header=None)
        xactcsv_frames.append(df)
    xact_Data_csv = pd.concat(xactcsv_frames)
    xact_Data_csv.rename(columns={20: 'ALARM'}, inplace=True)
    xact_Data_csv = xact_Data_csv.drop(columns=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])

elif int(start_year_month_str) == 202212:
    
    Month_files_1 = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '_01'+ '*' +  str(start.strftime("%Y")) + '*.csv' 
    Month_files_2 = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '_02'+ '*' +  str(start.strftime("%Y")) + '*.csv' 
    Month_files_3 = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '_03'+ '*' +  str(start.strftime("%Y")) + '*.csv' 
    Month_files_4 = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '_04'+ '*' +  str(start.strftime("%Y")) + '*.csv' 
    Month_files_5 = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '_05'+ '*' +  str(start.strftime("%Y")) + '*.csv' 
    Month_files_6 = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '_06'+ '*' +  str(start.strftime("%Y")) + '*.csv' 
    Month_files_7 = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '_07'+ '*' +  str(start.strftime("%Y")) + '*.csv' 
    Month_files_8 = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '_08'+ '*' +  str(start.strftime("%Y")) + '*.csv' 
    XACT_older_files = glob.glob(Month_files_1) + glob.glob(Month_files_2) + glob.glob(Month_files_3) + glob.glob(Month_files_4) + glob.glob(Month_files_5) + glob.glob(Month_files_6) + glob.glob(Month_files_7) + glob.glob(Month_files_8)
    
    for csv in XACT_older_files:
        df = pd.read_csv(csv, usecols=[*range(0, 160)], header=None) #, parse_dates = True , usecols=[0:160]
        xactcsv_frames.append(df)
    xact_Data_older = pd.concat(xactcsv_frames)
    print(xact_Data_older)
    xact_Data_older.rename(columns={20: 'ALARM'}, inplace=True)
    xact_Data_older = xact_Data_older.drop(columns=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
    
    xact_Data_older.columns = range(xact_Data_older.columns.size)
    
    xactcsv_frames = []
    
    Month_files_0 = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '_09'+ '*' +  str(start.strftime("%Y")) + '*.csv' 
    Month_files_1 = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '_1'+ '*' +  str(start.strftime("%Y")) + '*.csv' 
    Month_files_2 = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '_2'+ '*' +  str(start.strftime("%Y")) + '*.csv' 
    Month_files_3 = str(Data_Source_Folder) + 'Sample_' + str(start.strftime("%m")) + '_3'+ '*' +  str(start.strftime("%Y")) + '*.csv' 
    XACT_csv_files = glob.glob(Month_files_0) + glob.glob(Month_files_1) + glob.glob(Month_files_2) + glob.glob(Month_files_3) + glob.glob(Later_File_1) + glob.glob(Later_File_2)
    for csv in XACT_csv_files:
        csv = open(csv, 'r', errors='ignore')
        df = pd.read_csv(csv, encoding= 'unicode_escape', header=None, usecols=[*range(0, 167)], error_bad_lines=False, index_col=False) #, parse_dates = True , usecols=[0:160], , usecols=[*range(0, 166)]
        xactcsv_frames.append(df)
    xact_Data_csv = pd.concat(xactcsv_frames)
    xact_Data_csv.rename(columns={20: 'ALARM'}, inplace=True)
    
    xact_Data_csv.rename(columns={21: 'XC VER', 22: 'Sample Type', 23: 'Mg 12 (ng/m3)', 24: 'Mg uncert (ng/m3)', 35: 'Ar 18 (ng/m3)', 36: 'Ar uncert (ng/m3)' }, inplace=True)

    xact_Data_csv['Sample Type'] = xact_Data_csv['Sample Type'].astype(str)
    xact_Data_csv['Sample Flag'] = np.where(xact_Data_csv['Sample Type'] == '2' , np.nan , 1)
    xact_Data_csv['ALARM'] = np.where( xact_Data_csv['Sample Flag'].isnull() , 'Upscale  0', xact_Data_csv['ALARM'])    
    xact_Data_csv = xact_Data_csv.drop(columns=['XC VER', 'Sample Flag', 'Sample Type', 'Mg 12 (ng/m3)', 'Mg uncert (ng/m3)', 'Ar 18 (ng/m3)', 'Ar uncert (ng/m3)']) 
    xact_Data_csv = xact_Data_csv.drop(columns=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]) # , 21, 22, 23, 24, 35, 36
    
    xact_Data_csv.columns = range(xact_Data_csv.columns.size)
    xact_Data_older[142] = (list(xact_Data_csv.iloc[0:int(xact_Data_older.index.size),142]))
    xact_Data_csv = pd.concat([xact_Data_older, xact_Data_csv])

elif int(start_year_month_str) > 202212:
    for csv in XACT_csv_files:
        csv = open(csv, 'r', errors='ignore')
        df = pd.read_csv(csv, encoding= 'unicode_escape', header=None, usecols=[*range(0, 167)], error_bad_lines=False, index_col=False) #, parse_dates = True , usecols=[0:160], , usecols=[*range(0, 166)]
        xactcsv_frames.append(df)
    xact_Data_csv = pd.concat(xactcsv_frames)
    xact_Data_csv.rename(columns={20: 'ALARM'}, inplace=True)
    
    xact_Data_csv.rename(columns={21: 'XC VER', 22: 'Sample Type', 23: 'Mg 12 (ng/m3)', 24: 'Mg uncert (ng/m3)', 35: 'Ar 18 (ng/m3)', 36: 'Ar uncert (ng/m3)' }, inplace=True)

    xact_Data_csv['Sample Type'] = xact_Data_csv['Sample Type'].astype(str)
    xact_Data_csv['Sample Flag'] = np.where(xact_Data_csv['Sample Type'] == '2' , np.nan , 1)
    xact_Data_csv['ALARM'] = np.where( xact_Data_csv['Sample Flag'].isnull() , 'Upscale  0', xact_Data_csv['ALARM'])    
    xact_Data_csv = xact_Data_csv.drop(columns=['XC VER', 'Sample Flag', 'Sample Type', 'Mg 12 (ng/m3)', 'Mg uncert (ng/m3)', 'Ar 18 (ng/m3)', 'Ar uncert (ng/m3)']) 
    xact_Data_csv = xact_Data_csv.drop(columns=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]) # , 21, 22, 23, 24, 35, 36
    
else:
    for csv in XACT_csv_files:
        df = pd.read_csv(csv, usecols=[*range(0, 160)], header=None) #, parse_dates = True , usecols=[0:160]
        xactcsv_frames.append(df)
    xact_Data_csv = pd.concat(xactcsv_frames)
    xact_Data_csv.rename(columns={20: 'ALARM'}, inplace=True)
    xact_Data_csv = xact_Data_csv.drop(columns=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
#print(xact_Data_csv)
xact_Data_csv.drop(xact_Data_csv[(xact_Data_csv[0].isnull())].index,inplace =True)
xact_Data_csv.iloc[0] = xact_Data_csv.iloc[0].str.lstrip().astype(str) 
xact_Data_csv.columns = xact_Data_csv.iloc[0]
xact_Data_csv.drop(xact_Data_csv[(xact_Data_csv['TIME'] == 'TIME')].index,inplace =True)

xact_Data_csv = xact_Data_csv.rename(columns={'TIME': 'datetime',  'Output Pin 7 (True=ON)': 'PM Valve' })

xact_Data_csv['datetime'] = xact_Data_csv['datetime'].astype(str)
xact_Data_csv['datetime_length'] = xact_Data_csv['datetime'].str.len()
xact_Data_csv=xact_Data_csv.loc[xact_Data_csv.datetime_length <= 22] 
xact_Data_csv=xact_Data_csv.loc[xact_Data_csv.datetime_length >= 18] 
xact_Data_csv = xact_Data_csv.drop(columns=['datetime_length'])

#xact_Data_csv['datetime'] = xact_Data_csv['datetime'].astype(str)
xact_Data_csv['datetime'] = [datetime.datetime.strptime(x, '%m/%d/%Y %H:%M:%S') for x in xact_Data_csv['datetime']] #converts the dateTime format from string to python dateTime
xact_Data_csv.index = xact_Data_csv['datetime']
xact_Data_csv.sort_index(inplace=True)
#xact_Data_csv.drop(columns=['datetime'], inplace=True)

xact_Data_csv = xact_Data_csv[start:end]

#xact_Data_csv.drop(xact_Data_csv[(xact_Data_csv['Sample Flag'].notnull() )].index,inplace =True)

#xact_Data_csv = xact_Data_csv.rename(columns={' ALARM': 'ALARM'})
xact_Data_csv['ALARM'] = xact_Data_csv['ALARM'].astype(str)

xact_Data_csv['qc_flag'] = '1'
#xact_Data_csv['qc_flag'] = np.where(xact_Data_csv['ALARM'] != 0, '2', xact_Data_csv['qc_flag'])

#xact_Data_csv=xact_Data_csv.drop(xact_Data_csv[(xact_Data_csv['Sample Flag'] == 1 )].index,inplace =True)

xact_Data_csv['Upscale_flag'] = np.where(xact_Data_csv['ALARM'] == 'Upscale  0', 2, 1)
xact_Data_csv['Upscale_flag'] = np.where(xact_Data_csv['ALARM'] == 'Upscale  200', 2, xact_Data_csv['Upscale_flag'])
xact_Data_csv['Upscale_flag'] = np.where(xact_Data_csv['ALARM'] == 'Upscale  201', 2, xact_Data_csv['Upscale_flag'])
xact_Data_csv['Upscale_flag'] = np.where(xact_Data_csv['ALARM'] == 'Upscale  202', 2, xact_Data_csv['Upscale_flag'])
xact_Data_csv['Upscale_flag'] = np.where(xact_Data_csv['ALARM'] == 'Upscale  203', 2, xact_Data_csv['Upscale_flag'])
xact_Data_csv['Upscale_flag'] = np.where(xact_Data_csv['ALARM'] == 'Upscale  204', 2, xact_Data_csv['Upscale_flag'])
xact_Data_csv['Upscale_flag'] = np.where(xact_Data_csv['ALARM'] == 'Upscale  205', 2, xact_Data_csv['Upscale_flag'])

print(xact_Data_csv.iloc[:,3])

xact_Raw_Data_csv = xact_Data_csv.loc[xact_Data_csv.Upscale_flag == 1] 
xact_Cal_csv = xact_Data_csv.loc[xact_Data_csv.Upscale_flag == 2] 

Alarm_Flag = xact_Cal_csv['ALARM']
Upscale_flag = xact_Cal_csv['Upscale_flag']

xact_Cal_csv.drop(columns=['Upscale_flag', 'ALARM'], inplace=True)

xact_Cal_csv = xact_Cal_csv.astype(str) 

xact_Cal_csv.replace(['0', '0.0'], '', inplace=True)
xact_Cal_csv.index = xact_Cal_csv['datetime']
xact_Cal_csv.sort_index(inplace=True)
PM_Valve = xact_Cal_csv['PM Valve'] 
xact_Cal_csv.drop(columns=['datetime', 'PM Valve', 'qc_flag'], inplace=True)

xact_Cal_csv = xact_Cal_csv.astype(float)

#xact_Cal_csv['Upscale_flag'] = pd.Series(Upscale_flag)
#xact_Cal_csv['ALARM'] = pd.Series(Alarm_Flag)
#xact_Cal_csv['ALARM'] = xact_Cal_csv['ALARM'].astype(str)
#xact_Cal_csv['Upscale_flag'] = xact_Cal_csv['Upscale_flag'].astype(str)
xact_Cal_csv.rename(columns={'Nb 41(ng/m3)': 'Nb 41 (ng/m3)'}, inplace = True) 
xact_Cal_csv = xact_Cal_csv.dropna(how='all', axis=1)
xact_Cal_csv = xact_Cal_csv.loc[:, (xact_Cal_csv != 0).any(axis=0)]
xact_Cal_csv = xact_Cal_csv.drop(xact_Cal_csv.filter(regex="Si").columns, axis=1)
xact_Cal_csv = xact_Cal_csv.drop(xact_Cal_csv.filter(regex="Ca").columns, axis=1)
xact_Cal_csv = xact_Cal_csv.drop(xact_Cal_csv.filter(regex="Fe").columns, axis=1)
xact_Cal_csv = xact_Cal_csv.drop(xact_Cal_csv.filter(regex="Co").columns, axis=1)
xact_Cal_csv = xact_Cal_csv.drop(xact_Cal_csv.filter(regex="Zn").columns, axis=1)
xact_Cal_csv = xact_Cal_csv.drop(xact_Cal_csv.filter(regex="Ba").columns, axis=1)
xact_Cal_csv = xact_Cal_csv.drop(xact_Cal_csv.filter(regex="La").columns, axis=1)
xact_Cal_csv.replace(0, np.nan, inplace=True)

xact_Cal_csv.drop(xact_Cal_csv.iloc[:, 42:61], inplace=True, axis=1)

xact_Data_csv = xact_Raw_Data_csv

if int(start_year_month_str) < 202012:
    xact_Data_csv['PM_flag'] = 2
else:
    xact_Data_csv['PM Valve'] = xact_Data_csv['PM Valve'].astype(str)
    xact_Data_csv['PM_Valve_Length'] = xact_Data_csv['PM Valve'].str.len()
    xact_Data_csv['PM_flag'] = 0
    xact_Data_csv['PM_flag'] = np.where(xact_Data_csv['PM_Valve_Length'] == 4, 2, xact_Data_csv['PM_flag'])
    xact_Data_csv['PM_flag'] = np.where(xact_Data_csv['PM_Valve_Length'] == 5, 1, xact_Data_csv['PM_flag'])
    xact_Data_csv.drop(columns=['PM_Valve_Length'], inplace=True)
    

xact_Data_csv['TimeDateSince'] = xact_Data_csv.index-datetime.datetime(1970,1,1,0,0,00)
xact_Data_csv['minute'] = pd.DatetimeIndex(xact_Data_csv['TimeDateSince'].index).minute
xact_Data_csv['minute'] = xact_Data_csv['minute'].astype(float)
xact_Data_csv.drop(xact_Data_csv[(xact_Data_csv['minute'] == 15)].index,inplace =True)
xact_Data_csv = xact_Data_csv.drop(columns=['TimeDateSince', 'minute', 'datetime'])

xact_Data_csv.drop(columns=['PM Valve'], inplace=True)

xact_Data_csv = xact_Data_csv.astype(str) 

xact_Data_csv['ALARM'] = xact_Data_csv['ALARM'].astype(float)

xact_Data_csv['Cr_Alarm'] = np.where(xact_Data_csv['ALARM'] == 200, '2', '1')
xact_Data_csv['Pb_Alarm'] = np.where(xact_Data_csv['ALARM'] == 201, '2', '1')
xact_Data_csv['Cd_Alarm'] = np.where(xact_Data_csv['ALARM'] == 202, '2', '1')
xact_Data_csv['Nb_Alarm'] = np.where(xact_Data_csv['ALARM'] == 203, '2', '1')
xact_Alarm_series = xact_Data_csv[['Cr_Alarm', 'Pb_Alarm', 'Cd_Alarm', 'Nb_Alarm']]

if Flag_Error_Alarm == 'Yes':
    xact_Data_csv['qc_flag'] = np.where((xact_Data_csv['ALARM'] != 0) , '2', xact_Data_csv['qc_flag'])
else:
    pass

xact_Data_csv.replace(['0', '0.0'], '', inplace=True)

XACT_Alarm_series = xact_Data_csv['ALARM']

xact_Data_csv.drop(columns=['ALARM', 'Cr_Alarm', 'Pb_Alarm', 'Cd_Alarm', 'Nb_Alarm'], inplace=True)

xact_Data_csv = xact_Data_csv.astype(float) 

xact_Data_csv.iloc[:,0:142] = xact_Data_csv.iloc[:,0:142].astype(float)

upward_limit = 60000

xact_Data_csv.rename(columns={'Nb 41(ng/m3)': 'Nb 41 (ng/m3)'}, inplace = True) 

xact_Data_csv['Al_flag'] = np.where(((xact_Data_csv['Al 13 (ng/m3)']< 170)| (xact_Data_csv['Al 13 (ng/m3)']==0 )| (xact_Data_csv['Al 13 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Si_flag'] = np.where(((xact_Data_csv['Si 14 (ng/m3)']< 31)| (xact_Data_csv['Si 14 (ng/m3)']==0 )|(xact_Data_csv['Si 14 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['P_flag'] = np.where(((xact_Data_csv['P 15 (ng/m3)']< 9)| (xact_Data_csv['P 15 (ng/m3)']==0 )|(xact_Data_csv['P 15 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['S_flag'] = np.where(((xact_Data_csv['S 16 (ng/m3)']< 5.5)| (xact_Data_csv['S 16 (ng/m3)']==0 )|(xact_Data_csv['S 16 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Cl_flag'] = np.where(((xact_Data_csv['Cl 17 (ng/m3)']< 3)| (xact_Data_csv['Cl 17 (ng/m3)']==0 )|(xact_Data_csv['Cl 17 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['K_flag'] = np.where(((xact_Data_csv['K 19 (ng/m3)']< 2)| (xact_Data_csv['K 19 (ng/m3)']==0 )|(xact_Data_csv['K 19 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Ca_flag'] = np.where(((xact_Data_csv['Ca 20 (ng/m3)']< 0.52)| (xact_Data_csv['Ca 20 (ng/m3)']==0 )|(xact_Data_csv['Ca 20 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Sc_flag'] = np.where(((xact_Data_csv['Sc 21 (ng/m3)'].isnull() )| (xact_Data_csv['Sc 21 (ng/m3)']==0 )|(xact_Data_csv['Sc 21 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Ti_flag'] = np.where(((xact_Data_csv['Ti 22 (ng/m3)']< 0.28)| (xact_Data_csv['Ti 22 (ng/m3)']==0 )|(xact_Data_csv['Ti 22 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['V_flag'] = np.where(((xact_Data_csv['V 23 (ng/m3)']< 0.21)| (xact_Data_csv['V 23 (ng/m3)']==0 )|(xact_Data_csv['V 23 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Cr_flag'] = np.where(((xact_Data_csv['Cr 24 (ng/m3)']< 0.2)| (xact_Data_csv['Cr 24 (ng/m3)']==0 )|(xact_Data_csv['Cr 24 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Mn_flag'] = np.where(((xact_Data_csv['Mn 25 (ng/m3)']< 0.25)| (xact_Data_csv['Mn 25 (ng/m3)']==0 )|(xact_Data_csv['Mn 25 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Fe_flag'] = np.where(((xact_Data_csv['Fe 26 (ng/m3)']< 0.3)| (xact_Data_csv['Fe 26 (ng/m3)']==0 )|(xact_Data_csv['Fe 26 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Co_flag'] = np.where(((xact_Data_csv['Co 27 (ng/m3)']< 0.24)| (xact_Data_csv['Co 27 (ng/m3)']==0 )|(xact_Data_csv['Co 27 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Ni_flag'] = np.where(((xact_Data_csv['Ni 28 (ng/m3)']< 0.17)| (xact_Data_csv['Ni 28 (ng/m3)']==0 )|(xact_Data_csv['Ni 28 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Cu_flag'] = np.where(((xact_Data_csv['Cu 29 (ng/m3)']< 0.14)| (xact_Data_csv['Cu 29 (ng/m3)']==0 )|(xact_Data_csv['Cu 29 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Zn_flag'] = np.where(((xact_Data_csv['Zn 30 (ng/m3)']< 0.12)| (xact_Data_csv['Zn 30 (ng/m3)']==0 )|(xact_Data_csv['Zn 30 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Ga_flag'] = np.where(((xact_Data_csv['Ga 31 (ng/m3)']< 0.1)| (xact_Data_csv['Ga 31 (ng/m3)']==0 )|(xact_Data_csv['Ga 31 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Ge_flag'] = np.where(((xact_Data_csv['Ge 32 (ng/m3)']< 0.097)| (xact_Data_csv['Ge 32 (ng/m3)']==0 )|(xact_Data_csv['Ge 32 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['As_flag'] = np.where(((xact_Data_csv['As 33 (ng/m3)']< 0.11)| (xact_Data_csv['As 33 (ng/m3)']==0 )|(xact_Data_csv['As 33 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Se_flag'] = np.where(((xact_Data_csv['Se 34 (ng/m3)']< 0.14)| (xact_Data_csv['Se 34 (ng/m3)']==0 )|(xact_Data_csv['Se 34 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Br_flag'] = np.where(((xact_Data_csv['Br 35 (ng/m3)']< 0.18)| (xact_Data_csv['Br 35 (ng/m3)']==0 )|(xact_Data_csv['Br 35 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Rb_flag'] = np.where(((xact_Data_csv['Rb 37 (ng/m3)']< 0.33)| (xact_Data_csv['Rb 37 (ng/m3)']==0 )|(xact_Data_csv['Rb 37 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Sr_flag'] = np.where(((xact_Data_csv['Sr 38 (ng/m3)']< 0.38)| (xact_Data_csv['Sr 38 (ng/m3)']==0 )|(xact_Data_csv['Sr 38 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Y_flag'] = np.where(((xact_Data_csv['Y 39 (ng/m3)']< 0.48)| (xact_Data_csv['Y 39 (ng/m3)']==0 )|(xact_Data_csv['Y 39 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Zr_flag'] = np.where(((xact_Data_csv['Zr 40 (ng/m3)']< 0.57)| (xact_Data_csv['Zr 40 (ng/m3)']==0 )|(xact_Data_csv['Zr 40 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Nb_flag'] = np.where(((xact_Data_csv['Nb 41 (ng/m3)']< 0.7)| (xact_Data_csv['Nb 41 (ng/m3)']==0 )|(xact_Data_csv['Nb 41 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Mo_flag'] = np.where(((xact_Data_csv['Mo 42 (ng/m3)'].isnull() )| (xact_Data_csv['Mo 42 (ng/m3)']==0 )| (xact_Data_csv['Mo 42 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Ru_flag'] = np.where(((xact_Data_csv['Ru 44 (ng/m3)'].isnull() )| (xact_Data_csv['Ru 44 (ng/m3)']==0 )| (xact_Data_csv['Ru 44 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Rh_flag'] = np.where(((xact_Data_csv['Rh 45 (ng/m3)'].isnull() )| (xact_Data_csv['Rh 45 (ng/m3)']==0 )| (xact_Data_csv['Rh 45 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Pd_flag'] = np.where(((xact_Data_csv['Pd 46 (ng/m3)']<3.8 )| (xact_Data_csv['Pd 46 (ng/m3)']==0 )|(xact_Data_csv['Pd 46 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Ag_flag'] = np.where(((xact_Data_csv['Ag 47 (ng/m3)']<3.3 )| (xact_Data_csv['Ag 47 (ng/m3)']==0 )|(xact_Data_csv['Ag 47 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Cd_flag'] = np.where(((xact_Data_csv['Cd 48 (ng/m3)']< 4.4)| (xact_Data_csv['Cd 48 (ng/m3)']==0 )|(xact_Data_csv['Cd 48 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['In_flag'] = np.where(((xact_Data_csv['In 49 (ng/m3)']< 5.4)| (xact_Data_csv['In 49 (ng/m3)']==0 )|(xact_Data_csv['In 49 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Sn_flag'] = np.where(((xact_Data_csv['Sn 50 (ng/m3)']< 7.1)| (xact_Data_csv['Sn 50 (ng/m3)']==0 )|(xact_Data_csv['Sn 50 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Sb_flag'] = np.where(((xact_Data_csv['Sb 51 (ng/m3)']< 9)| (xact_Data_csv['Sb 51 (ng/m3)']==0 )|(xact_Data_csv['Sb 51 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Te_flag'] = np.where(((xact_Data_csv['Te 52 (ng/m3)']< 1)| (xact_Data_csv['Te 52 (ng/m3)']==0 )|(xact_Data_csv['Te 52 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['I_flag'] = np.where(((xact_Data_csv['I 53 (ng/m3)']< 0.85)| (xact_Data_csv['I 53 (ng/m3)']==0 )|(xact_Data_csv['I 53 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Cs_flag'] = np.where(((xact_Data_csv['Cs 55 (ng/m3)']< 0.65)| (xact_Data_csv['Cs 55 (ng/m3)']==0 )|(xact_Data_csv['Cs 55 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Ba_flag'] = np.where(((xact_Data_csv['Ba 56 (ng/m3)']< 0.67)| (xact_Data_csv['Ba 56 (ng/m3)']==0 )|(xact_Data_csv['Ba 56 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['La_flag'] = np.where(((xact_Data_csv['La 57 (ng/m3)']< 0.63)| (xact_Data_csv['La 57 (ng/m3)']==0 )|(xact_Data_csv['La 57 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Ce_flag'] = np.where(((xact_Data_csv['Ce 58 (ng/m3)']< 0.52)| (xact_Data_csv['Ce 58 (ng/m3)']==0 )|(xact_Data_csv['Ce 58 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Pr_flag'] = np.where(((xact_Data_csv['Pr 59 (ng/m3)'].isnull() )| (xact_Data_csv['Pr 59 (ng/m3)']==0 )| (xact_Data_csv['Pr 59 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Nd_flag'] = np.where(((xact_Data_csv['Nd 60 (ng/m3)'].isnull() )| (xact_Data_csv['Nd 60 (ng/m3)']==0 )| (xact_Data_csv['Nd 60 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Pm_flag'] = np.where(((xact_Data_csv['Pm 61 (ng/m3)'].isnull() )| (xact_Data_csv['Pm 61 (ng/m3)']==0 )| (xact_Data_csv['Pm 61 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Sm_flag'] = np.where(((xact_Data_csv['Sm 62 (ng/m3)'].isnull() )| (xact_Data_csv['Sm 62 (ng/m3)']==0 )| (xact_Data_csv['Sm 62 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Eu_flag'] = np.where(((xact_Data_csv['Eu 63 (ng/m3)'].isnull() )| (xact_Data_csv['Eu 63 (ng/m3)']==0 )| (xact_Data_csv['Eu 63 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Gd_flag'] = np.where(((xact_Data_csv['Gd 64 (ng/m3)'].isnull())| (xact_Data_csv['Gd 64 (ng/m3)']==0 )| (xact_Data_csv['Gd 64 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Tb_flag'] = np.where(((xact_Data_csv['Tb 65 (ng/m3)'].isnull() )| (xact_Data_csv['Tb 65 (ng/m3)']==0 )| (xact_Data_csv['Tb 65 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Dy_flag'] = np.where(((xact_Data_csv['Dy 66 (ng/m3)'].isnull() )| (xact_Data_csv['Dy 66 (ng/m3)']==0 )| (xact_Data_csv['Dy 66 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Ho_flag'] = np.where(((xact_Data_csv['Ho 67 (ng/m3)'].isnull() )| (xact_Data_csv['Ho 67 (ng/m3)']==0 )| (xact_Data_csv['Ho 67 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Er_flag'] = np.where(((xact_Data_csv['Er 68 (ng/m3)'].isnull() )| (xact_Data_csv['Er 68 (ng/m3)']==0 )| (xact_Data_csv['Er 68 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Tm_flag'] = np.where(((xact_Data_csv['Tm 69 (ng/m3)'].isnull() )| (xact_Data_csv['Tm 69 (ng/m3)']==0 )| (xact_Data_csv['Tm 69 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Yb_flag'] = np.where(((xact_Data_csv['Yb 70 (ng/m3)'].isnull() )| (xact_Data_csv['Yb 70 (ng/m3)']==0 )| (xact_Data_csv['Yb 70 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Lu_flag'] = np.where(((xact_Data_csv['Lu 71 (ng/m3)'].isnull() )| (xact_Data_csv['Lu 71 (ng/m3)']==0 )| (xact_Data_csv['Lu 71 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Hf_flag'] = np.where(((xact_Data_csv['Hf 72 (ng/m3)'].isnull() )| (xact_Data_csv['Hf 72 (ng/m3)']==0 )| (xact_Data_csv['Hf 72 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Ta_flag'] = np.where(((xact_Data_csv['Ta 73 (ng/m3)'].isnull() )| (xact_Data_csv['Ta 73 (ng/m3)']==0 )| (xact_Data_csv['Ta 73 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['W_flag'] = np.where(((xact_Data_csv['W 74 (ng/m3)'].isnull() )| (xact_Data_csv['W 74 (ng/m3)']==0 )| (xact_Data_csv['W 74 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Re_flag'] = np.where(((xact_Data_csv['Re 75 (ng/m3)'].isnull() )| (xact_Data_csv['Re 75 (ng/m3)']==0 )| (xact_Data_csv['Re 75 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Os_flag'] = np.where(((xact_Data_csv['Os 76 (ng/m3)'].isnull() )| (xact_Data_csv['Os 76 (ng/m3)']==0 )| (xact_Data_csv['Os 76 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Ir_flag'] = np.where(((xact_Data_csv['Ir 77 (ng/m3)'].isnull() )| (xact_Data_csv['Ir 77 (ng/m3)']==0 )| (xact_Data_csv['Ir 77 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Pt_flag'] = np.where(((xact_Data_csv['Pt 78 (ng/m3)']< 0.2)| (xact_Data_csv['Pt 78 (ng/m3)']==0 )|(xact_Data_csv['Pt 78 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Au_flag'] = np.where(((xact_Data_csv['Au 79 (ng/m3)']< 0.18)| (xact_Data_csv['Au 79 (ng/m3)']==0 )|(xact_Data_csv['Au 79 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Hg_flag'] = np.where(((xact_Data_csv['Hg 80 (ng/m3)']< 0.21)| (xact_Data_csv['Hg 80 (ng/m3)']==0 )|(xact_Data_csv['Hg 80 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Tl_flag'] = np.where(((xact_Data_csv['Tl 81 (ng/m3)']< 0.2)| (xact_Data_csv['Tl 81 (ng/m3)']==0 )|(xact_Data_csv['Tl 81 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Pb_flag'] = np.where(((xact_Data_csv['Pb 82 (ng/m3)']< 0.22)| (xact_Data_csv['Pb 82 (ng/m3)']==0 )|(xact_Data_csv['Pb 82 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Bi_flag'] = np.where(((xact_Data_csv['Bi 83 (ng/m3)']< 0.23)| (xact_Data_csv['Bi 83 (ng/m3)']==0 )|(xact_Data_csv['Bi 83 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Th_flag'] = np.where(((xact_Data_csv['Th 90 (ng/m3)'].isnull())| (xact_Data_csv['Th 90 (ng/m3)']==0 )| (xact_Data_csv['Th 90 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['Pa_flag'] = np.where(((xact_Data_csv['Pa 91 (ng/m3)'].isnull() )| (xact_Data_csv['Pa 91 (ng/m3)']==0 )| (xact_Data_csv['Pa 91 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])
xact_Data_csv['U_flag'] = np.where(((xact_Data_csv['U 92 (ng/m3)'].isnull() )| (xact_Data_csv['U 92 (ng/m3)']==0 )| (xact_Data_csv['U 92 (ng/m3)']>float(upward_limit))) , '2',xact_Data_csv['qc_flag'])



xact_Data_csv['Al Rel Uncert']= xact_Data_csv['Al Uncert (ng/m3)']/xact_Data_csv['Al 13 (ng/m3)']
xact_Data_csv['Si Rel Uncert']= xact_Data_csv['Si Uncert (ng/m3)']/xact_Data_csv['Si 14 (ng/m3)']
xact_Data_csv['P Rel Uncert']= xact_Data_csv['P Uncert (ng/m3)']/xact_Data_csv['P 15 (ng/m3)']
xact_Data_csv['S Rel Uncert']= xact_Data_csv['S Uncert (ng/m3)']/xact_Data_csv['S 16 (ng/m3)']
xact_Data_csv['Cl Rel Uncert']= xact_Data_csv['Cl Uncert (ng/m3)']/xact_Data_csv['Cl 17 (ng/m3)']
xact_Data_csv['K Rel Uncert']= xact_Data_csv['K Uncert (ng/m3)']/xact_Data_csv['K 19 (ng/m3)']
xact_Data_csv['Ca Rel Uncert']= xact_Data_csv['Ca Uncert (ng/m3)']/xact_Data_csv['Ca 20 (ng/m3)']
xact_Data_csv['Sc Rel Uncert']= xact_Data_csv['Sc Uncert (ng/m3)']/xact_Data_csv['Sc 21 (ng/m3)']
xact_Data_csv['Ti Rel Uncert']= xact_Data_csv['Ti Uncert (ng/m3)']/xact_Data_csv['Ti 22 (ng/m3)']
xact_Data_csv['V Rel Uncert']= xact_Data_csv['V Uncert (ng/m3)']/xact_Data_csv['V 23 (ng/m3)']
xact_Data_csv['Cr Rel Uncert']= xact_Data_csv['Cr Uncert (ng/m3)']/xact_Data_csv['Cr 24 (ng/m3)']
xact_Data_csv['Mn Rel Uncert']= xact_Data_csv['Mn Uncert (ng/m3)']/xact_Data_csv['Mn 25 (ng/m3)']
xact_Data_csv['Fe Rel Uncert']= xact_Data_csv['Fe Uncert (ng/m3)']/xact_Data_csv['Fe 26 (ng/m3)']
xact_Data_csv['Co Rel Uncert']= xact_Data_csv['Co Uncert (ng/m3)']/xact_Data_csv['Co 27 (ng/m3)']
xact_Data_csv['Ni Rel Uncert']= xact_Data_csv['Ni Uncert (ng/m3)']/xact_Data_csv['Ni 28 (ng/m3)']
xact_Data_csv['Cu Rel Uncert']= xact_Data_csv['Cu Uncert (ng/m3)']/xact_Data_csv['Cu 29 (ng/m3)']
xact_Data_csv['Zn Rel Uncert']= xact_Data_csv['Zn Uncert (ng/m3)']/xact_Data_csv['Zn 30 (ng/m3)']
xact_Data_csv['Ga Rel Uncert']= xact_Data_csv['Ga Uncert (ng/m3)']/xact_Data_csv['Ga 31 (ng/m3)']
xact_Data_csv['Ge Rel Uncert']= xact_Data_csv['Ge Uncert (ng/m3)']/xact_Data_csv['Ge 32 (ng/m3)']
xact_Data_csv['As Rel Uncert']= xact_Data_csv['As Uncert (ng/m3)']/xact_Data_csv['As 33 (ng/m3)']
xact_Data_csv['Se Rel Uncert']= xact_Data_csv['Se Uncert (ng/m3)']/xact_Data_csv['Se 34 (ng/m3)']
xact_Data_csv['Br Rel Uncert']= xact_Data_csv['Br Uncert (ng/m3)']/xact_Data_csv['Br 35 (ng/m3)']
xact_Data_csv['Rb Rel Uncert']= xact_Data_csv['Rb Uncert (ng/m3)']/xact_Data_csv['Rb 37 (ng/m3)']
xact_Data_csv['Sr Rel Uncert']= xact_Data_csv['Sr Uncert (ng/m3)']/xact_Data_csv['Sr 38 (ng/m3)']
xact_Data_csv['Y Rel Uncert']= xact_Data_csv['Y Uncert (ng/m3)']/xact_Data_csv['Y 39 (ng/m3)']
xact_Data_csv['Zr Rel Uncert']= xact_Data_csv['Zr Uncert (ng/m3)']/xact_Data_csv['Zr 40 (ng/m3)']
xact_Data_csv['Nb Rel Uncert']= xact_Data_csv['Nb Uncert (ng/m3)']/xact_Data_csv['Nb 41 (ng/m3)']
xact_Data_csv['Mo Rel Uncert']= xact_Data_csv['Mo Uncert (ng/m3)']/xact_Data_csv['Mo 42 (ng/m3)']
xact_Data_csv['Ru Rel Uncert']= xact_Data_csv['Ru Uncert (ng/m3)']/xact_Data_csv['Ru 44 (ng/m3)']
xact_Data_csv['Rh Rel Uncert']= xact_Data_csv['Rh Uncert (ng/m3)']/xact_Data_csv['Rh 45 (ng/m3)']
xact_Data_csv['Pd Rel Uncert']= xact_Data_csv['Pd Uncert (ng/m3)']/xact_Data_csv['Pd 46 (ng/m3)']
xact_Data_csv['Ag Rel Uncert']= xact_Data_csv['Ag Uncert (ng/m3)']/xact_Data_csv['Ag 47 (ng/m3)']
xact_Data_csv['Cd Rel Uncert']= xact_Data_csv['Cd Uncert (ng/m3)']/xact_Data_csv['Cd 48 (ng/m3)']
xact_Data_csv['In Rel Uncert']= xact_Data_csv['In Uncert (ng/m3)']/xact_Data_csv['In 49 (ng/m3)']
xact_Data_csv['Sn Rel Uncert']= xact_Data_csv['Sn Uncert (ng/m3)']/xact_Data_csv['Sn 50 (ng/m3)']
xact_Data_csv['Sb Rel Uncert']= xact_Data_csv['Sb Uncert (ng/m3)']/xact_Data_csv['Sb 51 (ng/m3)']
xact_Data_csv['Te Rel Uncert']= xact_Data_csv['Te Uncert (ng/m3)']/xact_Data_csv['Te 52 (ng/m3)']
xact_Data_csv['I Rel Uncert']= xact_Data_csv['I Uncert (ng/m3)']/xact_Data_csv['I 53 (ng/m3)']
xact_Data_csv['Cs Rel Uncert']= xact_Data_csv['Cs Uncert (ng/m3)']/xact_Data_csv['Cs 55 (ng/m3)']
xact_Data_csv['Ba Rel Uncert']= xact_Data_csv['Ba Uncert (ng/m3)']/xact_Data_csv['Ba 56 (ng/m3)']
xact_Data_csv['La Rel Uncert']= xact_Data_csv['La Uncert (ng/m3)']/xact_Data_csv['La 57 (ng/m3)']
xact_Data_csv['Ce Rel Uncert']= xact_Data_csv['Ce Uncert (ng/m3)']/xact_Data_csv['Ce 58 (ng/m3)']
xact_Data_csv['Pr Rel Uncert']= xact_Data_csv['Pr Uncert (ng/m3)']/xact_Data_csv['Pr 59 (ng/m3)']
xact_Data_csv['Nd Rel Uncert']= xact_Data_csv['Nd Uncert (ng/m3)']/xact_Data_csv['Nd 60 (ng/m3)']
xact_Data_csv['Pm Rel Uncert']= xact_Data_csv['Pm Uncert (ng/m3)']/xact_Data_csv['Pm 61 (ng/m3)']
xact_Data_csv['Sm Rel Uncert']= xact_Data_csv['Sm Uncert (ng/m3)']/xact_Data_csv['Sm 62 (ng/m3)']
xact_Data_csv['Eu Rel Uncert']= xact_Data_csv['Eu Uncert (ng/m3)']/xact_Data_csv['Eu 63 (ng/m3)']
xact_Data_csv['Gd Rel Uncert']= xact_Data_csv['Gd Uncert (ng/m3)']/xact_Data_csv['Gd 64 (ng/m3)']
xact_Data_csv['Tb Rel Uncert']= xact_Data_csv['Tb Uncert (ng/m3)']/xact_Data_csv['Tb 65 (ng/m3)']
xact_Data_csv['Dy Rel Uncert']= xact_Data_csv['Dy Uncert (ng/m3)']/xact_Data_csv['Dy 66 (ng/m3)']
xact_Data_csv['Ho Rel Uncert']= xact_Data_csv['Ho Uncert (ng/m3)']/xact_Data_csv['Ho 67 (ng/m3)']
xact_Data_csv['Er Rel Uncert']= xact_Data_csv['Er Uncert (ng/m3)']/xact_Data_csv['Er 68 (ng/m3)']
xact_Data_csv['Tm Rel Uncert']= xact_Data_csv['Tm Uncert (ng/m3)']/xact_Data_csv['Tm 69 (ng/m3)']
xact_Data_csv['Yb Rel Uncert']= xact_Data_csv['Yb Uncert (ng/m3)']/xact_Data_csv['Yb 70 (ng/m3)']
xact_Data_csv['Lu Rel Uncert']= xact_Data_csv['Lu Uncert (ng/m3)']/xact_Data_csv['Lu 71 (ng/m3)']
xact_Data_csv['Hf Rel Uncert']= xact_Data_csv['Hf Uncert (ng/m3)']/xact_Data_csv['Hf 72 (ng/m3)']
xact_Data_csv['Ta Rel Uncert']= xact_Data_csv['Ta Uncert (ng/m3)']/xact_Data_csv['Ta 73 (ng/m3)']
xact_Data_csv['W Rel Uncert']= xact_Data_csv['W Uncert (ng/m3)']/xact_Data_csv['W 74 (ng/m3)']
xact_Data_csv['Re Rel Uncert']= xact_Data_csv['Re Uncert (ng/m3)']/xact_Data_csv['Re 75 (ng/m3)']
xact_Data_csv['Os Rel Uncert']= xact_Data_csv['Os Uncert (ng/m3)']/xact_Data_csv['Os 76 (ng/m3)']
xact_Data_csv['Ir Rel Uncert']= xact_Data_csv['Ir Uncert (ng/m3)']/xact_Data_csv['Ir 77 (ng/m3)']
xact_Data_csv['Pt Rel Uncert']= xact_Data_csv['Pt Uncert (ng/m3)']/xact_Data_csv['Pt 78 (ng/m3)']
xact_Data_csv['Au Rel Uncert']= xact_Data_csv['Au Uncert (ng/m3)']/xact_Data_csv['Au 79 (ng/m3)']
xact_Data_csv['Hg Rel Uncert']= xact_Data_csv['Hg Uncert (ng/m3)']/xact_Data_csv['Hg 80 (ng/m3)']
xact_Data_csv['Tl Rel Uncert']= xact_Data_csv['Tl Uncert (ng/m3)']/xact_Data_csv['Tl 81 (ng/m3)']
xact_Data_csv['Pb Rel Uncert']= xact_Data_csv['Pb Uncert (ng/m3)']/xact_Data_csv['Pb 82 (ng/m3)']
xact_Data_csv['Bi Rel Uncert']= xact_Data_csv['Bi Uncert (ng/m3)']/xact_Data_csv['Bi 83 (ng/m3)']
xact_Data_csv['Th Rel Uncert']= xact_Data_csv['Th Uncert (ng/m3)']/xact_Data_csv['Th 90 (ng/m3)']
xact_Data_csv['Pa Rel Uncert']= xact_Data_csv['Pa Uncert (ng/m3)']/xact_Data_csv['Pa 91 (ng/m3)']
#xact_Data_csv['U Rel Uncert'] = xact_Data_csv['U Uncert (ng/m3)']/xact_Data_csv['U 92 (ng/m3)']

uncert_upper_limit = 0.5

xact_Data_csv['Al_flag'] = np.where(xact_Data_csv['Al Rel Uncert']>float(uncert_upper_limit), '2',xact_Data_csv['Al_flag'])
xact_Data_csv['Si_flag'] = np.where(xact_Data_csv['Si Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Si_flag'])
xact_Data_csv['P_flag'] = np.where(xact_Data_csv['P Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['P_flag'])
xact_Data_csv['S_flag'] = np.where(xact_Data_csv['S Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['S_flag'])
xact_Data_csv['Cl_flag'] = np.where(xact_Data_csv['Cl Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Cl_flag'])
xact_Data_csv['K_flag'] = np.where(xact_Data_csv['K Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['K_flag'])
xact_Data_csv['Ca_flag'] = np.where(xact_Data_csv['Ca Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Ca_flag'])
xact_Data_csv['Sc_flag'] = np.where(xact_Data_csv['Sc Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Sc_flag'])
xact_Data_csv['Ti_flag'] = np.where(xact_Data_csv['Ti Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Ti_flag'])
xact_Data_csv['V_flag'] = np.where(xact_Data_csv['V Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['V_flag'])
xact_Data_csv['Cr_flag'] = np.where(xact_Data_csv['Cr Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Cr_flag'])
xact_Data_csv['Mn_flag'] = np.where(xact_Data_csv['Mn Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Mn_flag'])
xact_Data_csv['Fe_flag'] = np.where(xact_Data_csv['Fe Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Fe_flag'])
xact_Data_csv['Co_flag'] = np.where(xact_Data_csv['Co Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Co_flag'])
xact_Data_csv['Ni_flag'] = np.where(xact_Data_csv['Ni Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Ni_flag'])
xact_Data_csv['Cu_flag'] = np.where(xact_Data_csv['Cu Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Cu_flag'])
xact_Data_csv['Zn_flag'] = np.where(xact_Data_csv['Zn Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Zn_flag'])
xact_Data_csv['Ga_flag'] = np.where(xact_Data_csv['Ga Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Ga_flag'])
xact_Data_csv['Ge_flag'] = np.where(xact_Data_csv['Ge Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Ge_flag'])
xact_Data_csv['As_flag'] = np.where(xact_Data_csv['As Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['As_flag'])
xact_Data_csv['Se_flag'] = np.where(xact_Data_csv['Se Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Se_flag'])
xact_Data_csv['Br_flag'] = np.where(xact_Data_csv['Br Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Br_flag'])
xact_Data_csv['Rb_flag'] = np.where(xact_Data_csv['Rb Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Rb_flag'])
xact_Data_csv['Sr_flag'] = np.where(xact_Data_csv['Sr Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Sr_flag'])
xact_Data_csv['Y_flag'] = np.where(xact_Data_csv['Y Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Y_flag'])
xact_Data_csv['Zr_flag'] = np.where(xact_Data_csv['Zr Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Zr_flag'])
xact_Data_csv['Nb_flag'] = np.where(xact_Data_csv['Nb Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Nb_flag'])
xact_Data_csv['Mo_flag'] = np.where(xact_Data_csv['Mo Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Mo_flag'])
xact_Data_csv['Ru_flag'] = np.where(xact_Data_csv['Ru Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Ru_flag'])
xact_Data_csv['Rh_flag'] = np.where(xact_Data_csv['Rh Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Rh_flag'])
xact_Data_csv['Pd_flag'] = np.where(xact_Data_csv['Pd Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Pd_flag'])
xact_Data_csv['Ag_flag'] = np.where(xact_Data_csv['Ag Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Ag_flag'])
xact_Data_csv['Cd_flag'] = np.where(xact_Data_csv['Cd Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Cd_flag'])
xact_Data_csv['In_flag'] = np.where(xact_Data_csv['In Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['In_flag'])
xact_Data_csv['Sn_flag'] = np.where(xact_Data_csv['Sn Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Sn_flag'])
xact_Data_csv['Sb_flag'] = np.where(xact_Data_csv['Sb Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Sb_flag'])
xact_Data_csv['Te_flag'] = np.where(xact_Data_csv['Te Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Te_flag'])
xact_Data_csv['I_flag'] = np.where(xact_Data_csv['I Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['I_flag'])
xact_Data_csv['Cs_flag'] = np.where(xact_Data_csv['Cs Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Cs_flag'])
xact_Data_csv['Ba_flag'] = np.where(xact_Data_csv['Ba Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Ba_flag'])
xact_Data_csv['La_flag'] = np.where(xact_Data_csv['La Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['La_flag'])
xact_Data_csv['Ce_flag'] = np.where(xact_Data_csv['Ce Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Ce_flag'])
xact_Data_csv['Pr_flag'] = np.where(xact_Data_csv['Pr Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Pr_flag'])
xact_Data_csv['Nd_flag'] = np.where(xact_Data_csv['Nd Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Nd_flag'])
xact_Data_csv['Pm_flag'] = np.where(xact_Data_csv['Pm Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Pm_flag'])
xact_Data_csv['Sm_flag'] = np.where(xact_Data_csv['Sm Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Sm_flag'])
xact_Data_csv['Eu_flag'] = np.where(xact_Data_csv['Eu Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Eu_flag'])
xact_Data_csv['Gd_flag'] = np.where(xact_Data_csv['Gd Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Gd_flag'])
xact_Data_csv['Tb_flag'] = np.where(xact_Data_csv['Tb Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Tb_flag'])
xact_Data_csv['Dy_flag'] = np.where(xact_Data_csv['Dy Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Dy_flag'])
xact_Data_csv['Ho_flag'] = np.where(xact_Data_csv['Ho Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Ho_flag'])
xact_Data_csv['Er_flag'] = np.where(xact_Data_csv['Er Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Er_flag'])
xact_Data_csv['Tm_flag'] = np.where(xact_Data_csv['Tm Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Tm_flag'])
xact_Data_csv['Yb_flag'] = np.where(xact_Data_csv['Yb Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Yb_flag'])
xact_Data_csv['Lu_flag'] = np.where(xact_Data_csv['Lu Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Lu_flag'])
xact_Data_csv['Hf_flag'] = np.where(xact_Data_csv['Hf Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Hf_flag'])
xact_Data_csv['Ta_flag'] = np.where(xact_Data_csv['Ta Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Ta_flag'])
xact_Data_csv['W_flag'] = np.where(xact_Data_csv['W Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['W_flag'])
xact_Data_csv['Re_flag'] = np.where(xact_Data_csv['Re Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Re_flag'])
xact_Data_csv['Os_flag'] = np.where(xact_Data_csv['Os Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Os_flag'])
xact_Data_csv['Ir_flag'] = np.where(xact_Data_csv['Ir Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Ir_flag'])
xact_Data_csv['Pt_flag'] = np.where(xact_Data_csv['Pt Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Pt_flag'])
xact_Data_csv['Au_flag'] = np.where(xact_Data_csv['Au Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Au_flag'])
xact_Data_csv['Hg_flag'] = np.where(xact_Data_csv['Hg Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Hg_flag'])
xact_Data_csv['Tl_flag'] = np.where(xact_Data_csv['Tl Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Tl_flag'])
xact_Data_csv['Pb_flag'] = np.where(xact_Data_csv['Pb Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Pb_flag'])
xact_Data_csv['Bi_flag'] = np.where(xact_Data_csv['Bi Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Bi_flag'])
xact_Data_csv['Th_flag'] = np.where(xact_Data_csv['Th Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Th_flag'])
xact_Data_csv['Pa_flag'] = np.where(xact_Data_csv['Pa Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['Pa_flag'])
#xact_Data_csv['U_flag'] = np.where(xact_Data_csv['U Rel Uncert']>float(uncert_upper_limit) , '2',xact_Data_csv['U_flag'])

#xact_Data_csv['ALARM'] = pd.Series(XACT_Alarm_series)
#xact_Data_csv['ALARM'] = xact_Data_csv['ALARM'].astype(float)

PM_Flag_series = xact_Data_csv['PM_flag'] 

xact_Data_csv.drop(columns=['qc_flag'], inplace=True)
#xact_Data_csv.drop(columns=['ALARM'], inplace=True)
#xact_Data_csv.drop(columns=['PM_flag'], inplace=True)

xact_Data_csv = xact_Data_csv.drop(xact_Data_csv.filter(regex='Rel Uncert').columns, axis=1)

xact_flags = xact_Data_csv.drop(xact_Data_csv.filter(regex="ng/m3").columns, axis=1)
xact_flags.drop(xact_flags.iloc[:, 44:63], inplace=True, axis=1)
xact_flags.drop(columns=['Sc_flag' , 'Rb_flag', 'Ru_flag', 'Rh_flag', 'Cs_flag'], inplace=True)
xact_flags.drop(columns=['Pa_flag', 'U_flag', 'Au_flag', 'Th_flag'], inplace=True)
xact_flags.drop(columns=['I_flag'], inplace=True) #'Tl_flag', 


if Flag_Elements_Alarm_Only == 'Yes':
    xact_flags = pd.concat([xact_flags, xact_Alarm_series])
    xact_flags.sort_index(inplace=True)
    xact_flags = xact_flags.astype(float)
    xact_flags = xact_flags.groupby(pd.Grouper(freq=Correcting_Freq)).mean()
    xact_flags = xact_flags.astype(str)
    xact_flags['Cr_flag'] = np.where(xact_flags['Cr_Alarm'] == '2', '2', xact_flags['Cr_flag'])
    xact_flags['Pb_flag'] = np.where( xact_flags['Pb_Alarm'] == '2', '2', xact_flags['Pb_flag'])
    xact_flags['Cd_flag'] = np.where( xact_flags['Cd_Alarm'] == '2', '2', xact_flags['Cd_flag'])
    xact_flags['Nb_flag'] = np.where( xact_flags['Nb_Alarm'] == '2', '2', xact_flags['Nb_flag'])
    xact_flags.drop(columns=['Cr_Alarm', 'Pb_Alarm', 'Cd_Alarm', 'Nb_Alarm'], inplace=True)
else:
    print('No Element by element alarm used')
    pass

xact_Data_without_flag = xact_Data_csv.drop(xact_Data_csv.filter(regex="_flag").columns, axis=1)
xact_Data_without_flag.rename(columns=lambda s: s.replace("Uncert (ng/m3)", "Uncert (ug/m3)"), inplace=True)
xact_Data_uncert = xact_Data_without_flag.drop(xact_Data_without_flag.filter(regex="ng/m3").columns, axis=1)
xact_Data_uncert.drop(xact_Data_uncert.iloc[:, 42:61], inplace=True, axis=1)
xact_Data_uncert.drop(columns=['Sc Uncert (ug/m3)' , 'Rb Uncert (ug/m3)', 'Ru Uncert (ug/m3)', 'Rh Uncert (ug/m3)', 'Cs Uncert (ug/m3)'], inplace=True)
xact_Data_uncert.drop(columns=['Pa Uncert (ug/m3)', 'Au Uncert (ug/m3)', 'Th Uncert (ug/m3)'], inplace=True) #, 'U Uncert (ug/m3)'
xact_Data_uncert.drop(columns=[ 'I Uncert (ug/m3)'], inplace=True) #'Tl Uncert (ug/m3)',
xact_Data_uncert = xact_Data_uncert.iloc[:,0:].div(1000, axis=0)

xact_Data_only = xact_Data_without_flag
xact_Data_only.rename(columns=lambda s: s.replace("ng/m3", "ug/m3"), inplace=True)
xact_Data_only = xact_Data_only.drop(xact_Data_only.filter(regex="Uncert").columns, axis=1)
xact_Data_only.drop(xact_Data_only.iloc[:, 42:61], inplace=True, axis=1)
xact_Data_only.drop(columns=['Sc 21 (ug/m3)' , 'Rb 37 (ug/m3)', 'Ru 44 (ug/m3)', 'Rh 45 (ug/m3)', 'Cs 55 (ug/m3)'], inplace=True)
xact_Data_only.drop(columns=['Pa 91 (ug/m3)', 'U 92 (ug/m3)', 'Au 79 (ug/m3)', 'Th 90 (ug/m3)'], inplace=True)
xact_Data_only.drop(columns=[ 'I 53 (ug/m3)'], inplace=True) #'Tl 81 (ug/m3)',
xact_Data_only = xact_Data_only.iloc[:,0:].div(1000, axis=0)

xact_Data_csv = pd.concat([xact_Data_only, xact_Data_uncert, xact_flags])

xact_Data_csv.sort_index(inplace=True)
xact_Data_csv = xact_Data_csv.astype(float)
xact_Data_csv = xact_Data_csv.groupby(pd.Grouper(freq=Correcting_Freq)).mean()
xact_Data_csv.drop(xact_Data_csv[(xact_Data_csv['Al 13 (ug/m3)'].isnull() )].index,inplace =True)
#xact_Data_csv.drop(xact_Data_csv.iloc[:, 84:125], inplace=True, axis=1)

start_Data_Anomaly_1 = datetime.datetime(2020,5,11,11,30,00)
end_Data_Anomaly_2 = datetime.datetime(2020,5,11,13,30,00)
xact_Data_csv.drop(xact_Data_csv.loc[start_Data_Anomaly_1:end_Data_Anomaly_2].index, inplace=True)

start_Clean_1 = datetime.datetime(2022,10,4,10,0,00) # XACT inlet cleaned
end_Clean_1 = datetime.datetime(2022,10,4,11,59,00)
#xact_Data_csv.loc[start_Clean_1:end_Clean_1, ('qc_flags')] = 2
xact_Data_csv.drop(xact_Data_csv.loc[start_Clean_1:end_Clean_1].index, inplace=True)

xact_Data_csv.iloc[:,84:125] = xact_Data_csv.iloc[:,84:125].astype(str)
xact_Data_csv['PM_flag'] = pd.Series(PM_Flag_series)

xact_Data_csv['datetime'] = xact_Data_csv.index

if int(start_year_month_str) < 202012:
    xact_PM10_csv = xact_Data_csv.loc[xact_Data_csv.PM_flag == 2] 
else:
    xact_PM10_csv = xact_Data_csv.loc[xact_Data_csv.PM_flag == 2] 
    xact_PM2p5_csv = xact_Data_csv.loc[xact_Data_csv.PM_flag == 1] 

xact_PM10_csv.index = xact_PM10_csv['datetime']
xact_PM10_csv.sort_index(inplace=True)
xact_PM10_csv.drop(columns=['datetime'], inplace=True)
xact_PM10_csv = xact_PM10_csv.astype(float)
xact_PM10_csv = xact_PM10_csv[start:end]
xact_PM10_csv.drop(columns=['PM_flag'], inplace=True)

if int(start_year_month_str) < 202012:
    pass 
else:
    xact_PM2p5_csv.index = xact_PM2p5_csv['datetime']
    xact_PM2p5_csv.sort_index(inplace=True)
    xact_PM2p5_csv.drop(columns=['datetime'], inplace=True)
    xact_PM2p5_csv = xact_PM2p5_csv.astype(float) 
    xact_PM2p5_csv = xact_PM2p5_csv[start:end]
    xact_PM2p5_csv.drop(columns=['PM_flag'], inplace=True)

if int(start_year_month_str) < 202012:
    xact_PM10_csv_new = xact_PM10_csv
    xact_PM10_csv_new = xact_PM10_csv_new.add_prefix('PM10_')
    xact_PM10_csv = xact_PM10_csv_new
    xact_Data_csv = xact_PM10_csv_new
else:
    xact_PM10_csv_label = xact_PM10_csv
    xact_PM2p5_csv_label = xact_PM2p5_csv
    xact_PM2p5_csv_label = xact_PM2p5_csv_label.add_prefix('PM2.5_')
    xact_PM2p5_csv = xact_PM2p5_csv_label
    xact_PM2p5_csv.drop(xact_PM2p5_csv[(xact_PM2p5_csv['PM2.5_Al_flag'].isnull() )].index,inplace =True)
    xact_PM2p5_csv = xact_PM2p5_csv.reindex(sorted(xact_PM2p5_csv.columns), axis=1)
    xact_PM2p5_csv_new = xact_PM2p5_csv_label.astype(float)
    xact_PM2p5_csv_new = xact_PM2p5_csv_new.groupby(pd.Grouper(freq=av_Freq)).mean()
    xact_PM2p5_csv_new.iloc[:,84:125] = xact_PM2p5_csv_new.iloc[:,84:125].astype(str)
    xact_PM10_csv_label = xact_PM10_csv_label.add_prefix('PM10_')
    xact_PM10_csv = xact_PM10_csv_label
    xact_PM10_csv.drop(xact_PM10_csv[(xact_PM10_csv['PM10_Al_flag'].isnull() )].index,inplace =True)
    xact_PM10_csv = xact_PM10_csv.reindex(sorted(xact_PM10_csv.columns), axis=1)
    xact_PM10_csv_new = xact_PM10_csv_label.astype(float)
    xact_PM10_csv_new = xact_PM10_csv_new.groupby(pd.Grouper(freq=av_Freq)).mean()
    xact_PM10_csv_new.iloc[:,84:125] = xact_PM10_csv_new.iloc[:,84:125].astype(str)
    xact_Data_csv = pd.concat([xact_PM2p5_csv_new, xact_PM10_csv_new])
    xact_Data_csv.sort_index(inplace=True)
    
#xact_Data_csv = np.where(xact_Data_csv == 0, np.nan, xact_Data_csv)

#xact_Data_csv = xact_Data_csv.replace({'0': np.nan, 0: np.nan})
#xact_Data_csv = xact_Data_csv.replace({'0':-1.00E+20, 0:-1.00E+20, np.nan:-1.00E+20})
#xact_Data_csv = xact_Data_csv.astype(float) 


if int(start_year_month_str) < 202012:
    xact_Data_csv.drop(xact_Data_csv[(xact_Data_csv['PM10_Al_flag'].isnull() )].index,inplace =True)
    xact_Data_csv.drop(columns=['PM10_Upscale_flag'], inplace=True)
    xact_PM10_csv['PM10_Upscale_flag'] = 1
    xact_PM10_csv.drop(columns=['PM10_Upscale_flag'], inplace=True)
    xact_Data_csv = xact_Data_csv.reindex(sorted(xact_Data_csv.columns), axis=1)
    xact_PM10_csv = xact_PM10_csv.reindex(sorted(xact_PM10_csv.columns), axis=1)
else:
    collation_Freq = '120min'
    xact_Data_csv = xact_Data_csv.astype(float)
    xact_Data_csv = xact_Data_csv.groupby(pd.Grouper(freq=collation_Freq)).mean()
    xact_Data_csv.drop(xact_Data_csv[(xact_Data_csv['PM10_Al_flag'].isnull() )].index,inplace =True)
    xact_Data_csv.drop(xact_Data_csv[(xact_Data_csv['PM2.5_Al_flag'].isnull() )].index,inplace =True)
    xact_Data_csv.iloc[:,201:242] = xact_Data_csv.iloc[:,207:248].astype(str)
    xact_Data_csv.iloc[:,80:121] = xact_Data_csv.iloc[:,83:124].astype(str)
    #xact_Data_csv.drop(xact_Data_csv.iloc[:, 207:248], inplace=True, axis=1)
    #xact_Data_csv.drop(xact_Data_csv.iloc[:, 83:124], inplace=True, axis=1)
    xact_Data_csv.drop(columns=['PM10_Upscale_flag' , 'PM2.5_Upscale_flag'], inplace=True)
    xact_PM10_csv.drop(columns=['PM10_Upscale_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=['PM2.5_Upscale_flag'], inplace=True)
    xact_Data_csv = xact_Data_csv.reindex(sorted(xact_Data_csv.columns), axis=1)
    xact_PM10_csv = xact_PM10_csv.reindex(sorted(xact_PM10_csv.columns), axis=1)
    xact_PM2p5_csv = xact_PM2p5_csv.reindex(sorted(xact_PM2p5_csv.columns), axis=1)

Other_XACT_Folder = str(Data_Output_Folder) + 'XACT_Other/'
XACT_Full_Folder = str(Other_XACT_Folder) + 'XACT_All_Elements/'
check_Folder = os.path.isdir(XACT_Full_Folder)
if not check_Folder:
    os.makedirs(XACT_Full_Folder)
    print("created folder : ", XACT_Full_Folder)
else:
    print(XACT_Full_Folder, "folder already exists.")

XACT_Collective_Folder = str(Other_XACT_Folder) + 'XACT_Collective/'
check_Folder = os.path.isdir(XACT_Collective_Folder)
if not check_Folder:
    os.makedirs(XACT_Collective_Folder)
    print("created folder : ", XACT_Collective_Folder)
else:
    print(XACT_Collective_Folder, "folder already exists.")

if int(start_year_month_str) < 202012: 
    xact_PM10_csv.to_csv(str(XACT_Full_Folder) + 'XACT_maqs_' + str(date_file_label) + '_full-elemental-composition-in-PM10' + str(status) + str(version_number) + '.csv') 
else:
    xact_PM2p5_csv.to_csv(str(XACT_Full_Folder) + 'XACT_maqs_' + str(date_file_label) + '_full-elemental-composition-in-PM2p5'  + str(status) + str(version_number) + '.csv')
    xact_PM10_csv.to_csv(str(XACT_Full_Folder) + 'XACT_maqs_' + str(date_file_label) + '_full-elemental-composition-in-PM10' + str(status) + str(version_number) + '.csv')
    xact_Data_csv.to_csv(str(XACT_Full_Folder) + 'XACT_maqs_' + str(date_file_label) + '_full-elemental-composition-in-PM2p5-and-PM10' + str(status) + str(version_number) + '.csv')

xact_Data_csv.drop(columns=['PM10_Cd 48 (ug/m3)', 'PM10_Cd Uncert (ug/m3)', 'PM10_Cd_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_La 57 (ug/m3)', 'PM10_La Uncert (ug/m3)', 'PM10_La_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_Ce 58 (ug/m3)', 'PM10_Ce Uncert (ug/m3)', 'PM10_Ce_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_Pt 78 (ug/m3)', 'PM10_Pt Uncert (ug/m3)', 'PM10_Pt_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_Tl 81 (ug/m3)', 'PM10_Tl Uncert (ug/m3)', 'PM10_Tl_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_Bi 83 (ug/m3)', 'PM10_Bi Uncert (ug/m3)', 'PM10_Bi_flag'], inplace=True)

xact_Data_csv.drop(columns=['PM10_Co 27 (ug/m3)', 'PM10_Co Uncert (ug/m3)', 'PM10_Co_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_Ga 31 (ug/m3)', 'PM10_Ga Uncert (ug/m3)', 'PM10_Ga_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_Ge 32 (ug/m3)', 'PM10_Ge Uncert (ug/m3)', 'PM10_Ge_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_P 15 (ug/m3)', 'PM10_P Uncert (ug/m3)', 'PM10_P_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_Y 39 (ug/m3)', 'PM10_Y Uncert (ug/m3)', 'PM10_Y_flag'], inplace=True)

xact_Data_csv.drop(columns=['PM10_Zr 40 (ug/m3)', 'PM10_Zr Uncert (ug/m3)', 'PM10_Zr_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_Mo 42 (ug/m3)', 'PM10_Mo Uncert (ug/m3)', 'PM10_Mo_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_In 49 (ug/m3)', 'PM10_In Uncert (ug/m3)', 'PM10_In_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_Sn 50 (ug/m3)', 'PM10_Sn Uncert (ug/m3)', 'PM10_Sn_flag'], inplace=True)
xact_Data_csv.drop(columns=['PM10_Hg 80 (ug/m3)', 'PM10_Hg Uncert (ug/m3)', 'PM10_Hg_flag'], inplace=True)

xact_PM10_csv.drop(columns=['PM10_Cd 48 (ug/m3)', 'PM10_Cd Uncert (ug/m3)', 'PM10_Cd_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_La 57 (ug/m3)', 'PM10_La Uncert (ug/m3)', 'PM10_La_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_Ce 58 (ug/m3)', 'PM10_Ce Uncert (ug/m3)', 'PM10_Ce_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_Pt 78 (ug/m3)', 'PM10_Pt Uncert (ug/m3)', 'PM10_Pt_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_Tl 81 (ug/m3)', 'PM10_Tl Uncert (ug/m3)', 'PM10_Tl_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_Bi 83 (ug/m3)', 'PM10_Bi Uncert (ug/m3)', 'PM10_Bi_flag'], inplace=True)

xact_PM10_csv.drop(columns=['PM10_Co 27 (ug/m3)', 'PM10_Co Uncert (ug/m3)', 'PM10_Co_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_Ga 31 (ug/m3)', 'PM10_Ga Uncert (ug/m3)', 'PM10_Ga_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_Ge 32 (ug/m3)', 'PM10_Ge Uncert (ug/m3)', 'PM10_Ge_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_P 15 (ug/m3)', 'PM10_P Uncert (ug/m3)', 'PM10_P_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_Y 39 (ug/m3)', 'PM10_Y Uncert (ug/m3)', 'PM10_Y_flag'], inplace=True)

xact_PM10_csv.drop(columns=['PM10_Zr 40 (ug/m3)', 'PM10_Zr Uncert (ug/m3)', 'PM10_Zr_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_Mo 42 (ug/m3)', 'PM10_Mo Uncert (ug/m3)', 'PM10_Mo_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_In 49 (ug/m3)', 'PM10_In Uncert (ug/m3)', 'PM10_In_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_Sn 50 (ug/m3)', 'PM10_Sn Uncert (ug/m3)', 'PM10_Sn_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_Hg 80 (ug/m3)', 'PM10_Hg Uncert (ug/m3)', 'PM10_Hg_flag'], inplace=True)
xact_PM10_csv.drop(columns=['PM10_Nb 41 (ug/m3)', 'PM10_Nb Uncert (ug/m3)', 'PM10_Nb_flag'], inplace=True)

XACT_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/XACT/'
check_Folder = os.path.isdir(XACT_Folder)
if not check_Folder:
    os.makedirs(XACT_Folder)
    print("created folder : ", XACT_Folder)
else:
    print(XACT_Folder, "folder already exists.")


if int(start_year_month_str) < 202012: #Elemental Composition
    xact_PM10_csv.to_csv(str(XACT_Folder) + 'XACT_maqs_' + str(date_file_label) + '_elemental-composition-in-PM10' + str(status) + str(version_number) + '.csv') 
else:
    xact_Data_csv.drop(columns=['PM2.5_Cd 48 (ug/m3)', 'PM2.5_Cd Uncert (ug/m3)', 'PM2.5_Cd_flag'], inplace=True)
    xact_Data_csv.drop(columns=[ 'PM2.5_La 57 (ug/m3)', 'PM2.5_La Uncert (ug/m3)', 'PM2.5_La_flag'], inplace=True)
    xact_Data_csv.drop(columns=[ 'PM2.5_Ce 58 (ug/m3)', 'PM2.5_Ce Uncert (ug/m3)', 'PM2.5_Ce_flag'], inplace=True)
    xact_Data_csv.drop(columns=[ 'PM2.5_Pt 78 (ug/m3)', 'PM2.5_Pt Uncert (ug/m3)', 'PM2.5_Pt_flag'], inplace=True)
    xact_Data_csv.drop(columns=['PM2.5_Tl 81 (ug/m3)', 'PM2.5_Tl Uncert (ug/m3)', 'PM2.5_Tl_flag'], inplace=True)
    xact_Data_csv.drop(columns=['PM2.5_Bi 83 (ug/m3)', 'PM2.5_Bi Uncert (ug/m3)', 'PM2.5_Bi_flag'], inplace=True)

    xact_Data_csv.drop(columns=['PM2.5_Co 27 (ug/m3)', 'PM2.5_Co Uncert (ug/m3)', 'PM2.5_Co_flag'], inplace=True)
    xact_Data_csv.drop(columns=['PM2.5_Ga 31 (ug/m3)', 'PM2.5_Ga Uncert (ug/m3)', 'PM2.5_Ga_flag'], inplace=True)
    xact_Data_csv.drop(columns=['PM2.5_Ge 32 (ug/m3)', 'PM2.5_Ge Uncert (ug/m3)', 'PM2.5_Ge_flag'], inplace=True)
    xact_Data_csv.drop(columns=[ 'PM2.5_P 15 (ug/m3)', 'PM2.5_P Uncert (ug/m3)', 'PM2.5_P_flag'], inplace=True)
    xact_Data_csv.drop(columns=['PM2.5_Y 39 (ug/m3)', 'PM2.5_Y Uncert (ug/m3)', 'PM2.5_Y_flag'], inplace=True)

    xact_Data_csv.drop(columns=[ 'PM2.5_Zr 40 (ug/m3)', 'PM2.5_Zr Uncert (ug/m3)', 'PM2.5_Zr_flag'], inplace=True)
    xact_Data_csv.drop(columns=[ 'PM2.5_Mo 42 (ug/m3)', 'PM2.5_Mo Uncert (ug/m3)', 'PM2.5_Mo_flag'], inplace=True)
    xact_Data_csv.drop(columns=[ 'PM2.5_In 49 (ug/m3)', 'PM2.5_In Uncert (ug/m3)', 'PM2.5_In_flag'], inplace=True)
    xact_Data_csv.drop(columns=['PM2.5_Sn 50 (ug/m3)', 'PM2.5_Sn Uncert (ug/m3)', 'PM2.5_Sn_flag'], inplace=True)
    xact_Data_csv.drop(columns=[ 'PM2.5_Hg 80 (ug/m3)', 'PM2.5_Hg Uncert (ug/m3)', 'PM2.5_Hg_flag'], inplace=True)
    
    xact_PM2p5_csv.drop(columns=['PM2.5_Cd 48 (ug/m3)', 'PM2.5_Cd Uncert (ug/m3)', 'PM2.5_Cd_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=[ 'PM2.5_La 57 (ug/m3)', 'PM2.5_La Uncert (ug/m3)', 'PM2.5_La_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=[ 'PM2.5_Ce 58 (ug/m3)', 'PM2.5_Ce Uncert (ug/m3)', 'PM2.5_Ce_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=[ 'PM2.5_Pt 78 (ug/m3)', 'PM2.5_Pt Uncert (ug/m3)', 'PM2.5_Pt_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=['PM2.5_Tl 81 (ug/m3)', 'PM2.5_Tl Uncert (ug/m3)', 'PM2.5_Tl_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=['PM2.5_Bi 83 (ug/m3)', 'PM2.5_Bi Uncert (ug/m3)', 'PM2.5_Bi_flag'], inplace=True)

    xact_PM2p5_csv.drop(columns=['PM2.5_Co 27 (ug/m3)', 'PM2.5_Co Uncert (ug/m3)', 'PM2.5_Co_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=['PM2.5_Ga 31 (ug/m3)', 'PM2.5_Ga Uncert (ug/m3)', 'PM2.5_Ga_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=['PM2.5_Ge 32 (ug/m3)', 'PM2.5_Ge Uncert (ug/m3)', 'PM2.5_Ge_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=[ 'PM2.5_P 15 (ug/m3)', 'PM2.5_P Uncert (ug/m3)', 'PM2.5_P_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=['PM2.5_Y 39 (ug/m3)', 'PM2.5_Y Uncert (ug/m3)', 'PM2.5_Y_flag'], inplace=True)

    xact_PM2p5_csv.drop(columns=[ 'PM2.5_Zr 40 (ug/m3)', 'PM2.5_Zr Uncert (ug/m3)', 'PM2.5_Zr_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=[ 'PM2.5_Mo 42 (ug/m3)', 'PM2.5_Mo Uncert (ug/m3)', 'PM2.5_Mo_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=[ 'PM2.5_In 49 (ug/m3)', 'PM2.5_In Uncert (ug/m3)', 'PM2.5_In_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=['PM2.5_Sn 50 (ug/m3)', 'PM2.5_Sn Uncert (ug/m3)', 'PM2.5_Sn_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=[ 'PM2.5_Hg 80 (ug/m3)', 'PM2.5_Hg Uncert (ug/m3)', 'PM2.5_Hg_flag'], inplace=True)
    xact_PM2p5_csv.drop(columns=[ 'PM2.5_Nb 41 (ug/m3)', 'PM2.5_Nb Uncert (ug/m3)', 'PM2.5_Nb_flag'], inplace=True)

    xact_PM2p5_csv.to_csv(str(XACT_Folder) +  'XACT_maqs_' + str(date_file_label) + '_elemental-composition-in-PM2p5'  + str(status) + str(version_number) + '.csv')
    xact_PM10_csv.to_csv(str(XACT_Folder) + 'XACT_maqs_' + str(date_file_label) + '_elemental-composition-in-PM10' + str(status) + str(version_number) + '.csv')
    xact_Data_csv.to_csv(str(XACT_Collective_Folder) + 'XACT_maqs_' + str(date_file_label) + '_elemental-composition-in-PM2p5-and-PM10' + str(status) + str(version_number) + '.csv')

#xact_Data_csv['PM Valve Flag'] = pd.Series(PM_Valve)
#xact_Data_csv.drop(columns=['datetime'], inplace=True)

if display_XACT_graphs == 'Yes':
    if int(start_year_month_str) < 202012:
        plt.plot(xact_PM10_csv['PM10_S 16 (ug/m3)'], label='Sulphur_PM10') #PM10_
        plt.plot(xact_PM10_csv['PM10_K 19 (ug/m3)'], label='Potassium_PM10')
        plt.plot(xact_PM10_csv['PM10_Ca 20 (ug/m3)'], label='Calcium_PM10')
        plt.plot(xact_PM10_csv['PM10_Zn 30 (ug/m3)'], label='Zinc_PM10')
        #plt.plot(xact_PM10_csv['PM10_Cr 24 (ug/m3)'], label='Chronium_PM10')
        #plt.plot(xact_PM10_csv['PM10_Pb 82 (ug/m3)'], label='Lead_PM10')
        plt.plot(xact_Data_csv['PM10_Nb 41 (ug/m3)'], label='Niobium_PM10')
        plt.legend()
        plt.ylabel('abundance ug/m3')
        plt.rc('figure', figsize=(60, 100))
        font = {'family' : 'normal',
                'weight' : 'bold',
                'size'   : 16}
    
        plt.rc('font', **font)
        #plt.ylim(10, 30)
        plt.figure()
        plt.show()

    else:
        #plt.plot(xact_PM10_csv['PM10_S 16 (ug/m3)'], label='Sulphur_PM10')
        #plt.plot(xact_PM2p5_csv['PM2.5_S 16 (ug/m3)'], label='Sulphur_PM2.5')
        #plt.plot(xact_PM10_csv['PM10_K 19 (ug/m3)'], label='Potassium_PM10')
       # plt.plot(xact_PM2p5_csv['PM2.5_K 19 (ug/m3)'], label='Potassium_PM2.5')
        plt.plot(xact_PM10_csv['PM10_Ca 20 (ug/m3)'], label='Calcium_PM10')
        plt.plot(xact_PM2p5_csv['PM2.5_Ca 20 (ug/m3)'], label='Calcium_PM2.5')
        plt.plot(xact_PM10_csv['PM10_Si 14 (ug/m3)'], label='Silicon_PM10')
        plt.plot(xact_PM2p5_csv['PM2.5_Si 14 (ug/m3)'], label='Silicon_PM2.5')
        #plt.plot(xact_PM10_csv['PM10_Zn 30 (ug/m3)'], label='Zinc_PM10')
        #plt.plot(xact_PM2p5_csv['PM2.5_Zn 30 (ug/m3)'], label='Zinc_PM2.5')
        #plt.plot(xact_PM10_csv['PM10_Cr 24 (ug/m3)'], label='Chronium_PM10')
        #plt.plot(xact_PM2p5_csv['PM2.5_Cr 24 (ug/m3)'], label='Chronium_PM2.5')
        #plt.plot(xact_PM10_csv['PM10_Pb 82 (ug/m3)'], label='Lead_PM10')
        #plt.plot(xact_PM2p5_csv['PM2.5_Pb 82 (ug/m3)'], label='Lead_PM2.5')
        plt.plot(xact_Data_csv['PM10_Nb 41 (ug/m3)'], label='Niobium_PM10')
        plt.plot(xact_Data_csv['PM2.5_Nb 41 (ug/m3)'], label='Niobium_PM2.5')

        plt.legend()
        plt.ylabel('abundance ug/m3')
        plt.rc('figure', figsize=(60, 100))
        font = {'family' : 'normal',
                'weight' : 'bold',
                'size'   : 16}
        
        plt.rc('font', **font)
        #plt.ylim(10, 30)
        plt.figure()
        plt.show()
        
else:
    pass

xact_PM10_csv['TimeDateSince'] = xact_PM10_csv.index-datetime.datetime(1970,1,1,0,0,00)
xact_PM10_csv['TimeSecondsSince'] = xact_PM10_csv['TimeDateSince'].dt.total_seconds()
xact_PM10_csv['day_year'] = pd.DatetimeIndex(xact_PM10_csv['TimeDateSince'].index).dayofyear
xact_PM10_csv['year'] = pd.DatetimeIndex(xact_PM10_csv['TimeDateSince'].index).year
xact_PM10_csv['month'] = pd.DatetimeIndex(xact_PM10_csv['TimeDateSince'].index).month
xact_PM10_csv['day'] = pd.DatetimeIndex(xact_PM10_csv['TimeDateSince'].index).day
xact_PM10_csv['hour'] = pd.DatetimeIndex(xact_PM10_csv['TimeDateSince'].index).hour
xact_PM10_csv['minute'] = pd.DatetimeIndex(xact_PM10_csv['TimeDateSince'].index).minute
xact_PM10_csv['second'] = pd.DatetimeIndex(xact_PM10_csv['TimeDateSince'].index).second

if int(start_year_month_str) < 202012:
    pass 
else:
    xact_PM2p5_csv['TimeDateSince'] = xact_PM2p5_csv.index-datetime.datetime(1970,1,1,0,0,00)
    xact_PM2p5_csv['TimeSecondsSince'] = xact_PM2p5_csv['TimeDateSince'].dt.total_seconds()
    xact_PM2p5_csv['day_year'] = pd.DatetimeIndex(xact_PM2p5_csv['TimeDateSince'].index).dayofyear
    xact_PM2p5_csv['year'] = pd.DatetimeIndex(xact_PM2p5_csv['TimeDateSince'].index).year
    xact_PM2p5_csv['month'] = pd.DatetimeIndex(xact_PM2p5_csv['TimeDateSince'].index).month
    xact_PM2p5_csv['day'] = pd.DatetimeIndex(xact_PM2p5_csv['TimeDateSince'].index).day
    xact_PM2p5_csv['hour'] = pd.DatetimeIndex(xact_PM2p5_csv['TimeDateSince'].index).hour
    xact_PM2p5_csv['minute'] = pd.DatetimeIndex(xact_PM2p5_csv['TimeDateSince'].index).minute
    xact_PM2p5_csv['second'] = pd.DatetimeIndex(xact_PM2p5_csv['TimeDateSince'].index).second

xact_Data_csv['TimeDateSince'] = xact_Data_csv.index-datetime.datetime(1970,1,1,0,0,00)
xact_Data_csv['TimeSecondsSince'] = xact_Data_csv['TimeDateSince'].dt.total_seconds()
xact_Data_csv['day_year'] = pd.DatetimeIndex(xact_Data_csv['TimeDateSince'].index).dayofyear
xact_Data_csv['year'] = pd.DatetimeIndex(xact_Data_csv['TimeDateSince'].index).year
xact_Data_csv['month'] = pd.DatetimeIndex(xact_Data_csv['TimeDateSince'].index).month
xact_Data_csv['day'] = pd.DatetimeIndex(xact_Data_csv['TimeDateSince'].index).day
xact_Data_csv['hour'] = pd.DatetimeIndex(xact_Data_csv['TimeDateSince'].index).hour
xact_Data_csv['minute'] = pd.DatetimeIndex(xact_Data_csv['TimeDateSince'].index).minute
xact_Data_csv['second'] = pd.DatetimeIndex(xact_Data_csv['TimeDateSince'].index).second

if display_cal_graph == 'No':
    pass
else:
    plt.plot(xact_Cal_csv['Cr 24 (ng/m3)'], label='Chronium_Cal (Alarm 200)')
    plt.plot(xact_Cal_csv['Pb 82 (ng/m3)'], label='Lead_Cal (Alarm 201)')
    plt.plot(xact_Cal_csv['Cd 48 (ng/m3)'], label='Cadmium_Cal (Alarm 202)')
    plt.plot(xact_Cal_csv['Nb 41 (ng/m3)'], label='Niobium_Cal (Alarm 203)')
    #plt.plot(xact_Cal_csv['Al 13 (ng/m3)'], label='Aluminium_Cal')
    #plt.plot(xact_Cal_csv['Si 14 (ng/m3)'], label='Silicon_Cal')
    #plt.plot(xact_Cal_csv['S 16 (ng/m3)'], label='Sulphur_Cal')
    #plt.plot(xact_Cal_csv['K 19 (ng/m3)'], label='Potassium_Cal')
    #plt.plot(xact_Cal_csv['Ti 22 (ng/m3)'], label='Titanium_Cal')
    #plt.plot(xact_Cal_csv['Mn 25 (ng/m3)'], label='Manganese_Cal')
    #plt.plot(xact_Cal_csv['Cu 29 (ng/m3)'], label='Copper_Cal')
    #plt.plot(xact_Cal_csv['Y 39 (ng/m3)'], label='Yttrium_Cal')
    #plt.plot(xact_Cal_csv['Zr 40 (ng/m3)'], label='Zirconium_Cal')
    #plt.plot(xact_Cal_csv['Sb 51 (ng/m3)'], label='Antimony_Cal')
    #plt.plot(xact_Cal_csv['Tl 81 (ng/m3)'], label='Thallium_Cal')
    #plt.plot(xact_Cal_csv['Bi 83 (ng/m3)'], label='Bismuth_Cal')

    plt.legend()
    plt.ylabel('abundance ng/m3')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 16}
        
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    plt.figure()
    plt.show()


XACT_Cal_Folder = str(Other_XACT_Folder) + 'XACT_Cal/' #+ str(start.strftime("%Y")) + str(start.strftime("%m")) + '/' 
check_Folder = os.path.isdir(XACT_Cal_Folder)
if not check_Folder:
    os.makedirs(XACT_Cal_Folder)
    print("created folder : ", XACT_Cal_Folder)

else:
    print(XACT_Cal_Folder, "folder already exists.")

xact_Cal_csv.to_csv(str(XACT_Cal_Folder) + 'XACT-625i_maqs_'+ str(start.strftime("%Y")) + str(start.strftime("%m")) + '_Collective-Cal-file_' + str(status) + str(version_number) + '.csv')

