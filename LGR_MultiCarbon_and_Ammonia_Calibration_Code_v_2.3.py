# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 19:24:56 2021

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
data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v2.2' #version of the code

today = date.today()
current_day = today.strftime("%Y%m%d")

folder = np.where((str(version_number) == 'v0.6'), 'Preliminary', 'Ratified')

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/LGR/', 'D:/FirsData/LGR/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(folder) + '_' + str(version_number) + '/', 'D:/' + str(folder) + '_' + str(version_number) + '/')


#Calibration Day 1
year_Audit_1 = 2019 #input the year of Audit
month_Audit_1 = 8 #input the month of Audit
day_Audit_1 = 9 #input the day of Audit

start_Audit_Day_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,0,0,00)
end_Audit_Day_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,23,59,00)

#Calibration Day 2
year_Audit_2 = 2020 #input the year of study
month_Audit_2 = 3 #input the month of study
day_Audit_2 = 18 #default start date set

start_Audit_Day_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,0,0,00)
end_Audit_Day_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,23,59,00)

#Calibration Day 3
year_Audit_3 = 2020 #input the year of study
month_Audit_3 = 10 #input the month of study
day_Audit_3 = 2 #default start date set

start_Audit_Day_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,0,0,00)
end_Audit_Day_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,23,59,00)

#Audit 4
year_Audit_4 = 2021 #input the year of study
month_Audit_4 = 3 #input the month of study
day_Audit_4 = 30 #default start date set

start_Audit_Day_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,0,0,00)
end_Audit_Day_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,23,59,00)

#Ammonia_Audit_1
year_AmmoniaZero_1_1 = 2021 #input the year of study
month_AmmoniaZero_1_1 = 7 #input the month of study
day1_AmmoniaZero_1_1 = 26 #default start date set
day2_AmmoniaZero_1_1 = 27 #default start date set

start_NH3_Zero_1_1 = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day1_AmmoniaZero_1_1,0,0,00)
end_NH3_Zero_1_1 = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,23,59,00)

#Ammonia_Audit_2
year_AmmoniaZero_1_2 = 2021 #input the year of study
month_AmmoniaZero_1_2 = 7 #input the month of study
day1_AmmoniaZero_1_2 = 30 #default start date set
day2_AmmoniaZero_1_2 = 30 #default start date set

start_NH3_Zero_1_2 = datetime.datetime(year_AmmoniaZero_1_2,month_AmmoniaZero_1_2,day1_AmmoniaZero_1_2,0,0,00)
end_NH3_Zero_1_2 = datetime.datetime(year_AmmoniaZero_1_2,month_AmmoniaZero_1_2,day1_AmmoniaZero_1_2,23,59,00)

#Audit 5
year_Audit_5 = 2021 #input the year of study
month_Audit_5 = 10 #input the month of study
day_Audit_5 = 27 #default start date set

start_Audit_Day_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,0,0,00)
end_Audit_Day_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,23,59,00)

#Audit 6 and ammonia zero
year_Audit_6 = 2022 #input the year of study
month_Audit_6 = 5 #input the month of study
day1_Audit_6 = 4 
day2_Audit_6 = 5 

start_Audit_Day_6 = datetime.datetime(year_Audit_6,month_Audit_6,day1_Audit_6,0,0,00)
end_Audit_Day_6 = datetime.datetime(year_Audit_6,month_Audit_6,day2_Audit_6,23,59,00)

start = start_Audit_Day_1
end = end_Audit_Day_1

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

prior_Audit_Day = start - timedelta(days=1)
prior_Audit_str = str(prior_Audit_Day.strftime("%Y")) + str(prior_Audit_Day.strftime("%m")) + str(prior_Audit_Day.strftime("%d"))

if start_Audit_str == end_Audit_str:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_Audit_Import_1)
else:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_Audit_Import_1)
    
ghg_frames = []

for csv in csv_files:
    
    csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv2, usecols=[0,1,2,4,6,8,32,33,35],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False ) #
    ghg_frames.append(df)

Prior_LGR_Data = pd.concat(ghg_frames)

Prior_LGR_Data['row_numbers']=(Prior_LGR_Data.index).astype(float) 
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['row_numbers'] <= 9)].index,inplace =True)
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['row_numbers'])

Prior_LGR_Data.rename(columns={0: 'Date'}, inplace=True)
Prior_LGR_Data.rename(columns={1: 'Time'}, inplace=True)
Prior_LGR_Data.rename(columns={2: 'CH4 (ppm)'}, inplace=True)
Prior_LGR_Data.rename(columns={4: 'H2O (ppm) - MultiCarbon analyser'}, inplace=True)
Prior_LGR_Data.rename(columns={6: 'CO2 (ppm)'}, inplace=True)
Prior_LGR_Data.rename(columns={8: 'CO (ppb)'}, inplace=True)
Prior_LGR_Data.rename(columns={32: 'Test'}, inplace=True)
Prior_LGR_Data.rename(columns={33: 'NH3 (ppb)'}, inplace=True) #NH3 is labelled as NH4 in early raw files
Prior_LGR_Data.rename(columns={35: 'H2O (ppm) - NH3 analyser'}, inplace=True)

Prior_LGR_Data['Date'] = Prior_LGR_Data['Date'].astype(str)
Prior_LGR_Data['Time'] = Prior_LGR_Data['Time'].astype(str)
Prior_LGR_Data['Date_length'] = Prior_LGR_Data['Date'].str.len()
Prior_LGR_Data['Time_length'] = Prior_LGR_Data['Time'].str.len()
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.Date_length == 10] #checking that the cells of GHG_Data['Date'] have only 10 characters such as with 01/01/2019
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.Time_length == 8] #checking that the cells of GHG_Data['Time'] have only 8 characters such as with 12:00:00
Prior_LGR_Data['datetime'] = Prior_LGR_Data['Date']+' '+ Prior_LGR_Data['Time']# added Date and time into new columns
Prior_LGR_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in Prior_LGR_Data['datetime']] #converts the dateTime format from string to python dateTime
Prior_LGR_Data.index = Prior_LGR_Data['datetime']
Prior_LGR_Data = Prior_LGR_Data.sort_index()
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['Time', 'Date', 'Date_length','datetime','Time_length'])
#Prior_LGR_Data = Prior_GHG_Data.drop(columns=['datetime']) # could drop datetime column?

#Prior_LGR_Data['NH3 (ppb)'] = np.where(Prior_LGR_Data["NH3 (ppb)"] >= -5)

#Prior_LGR_Data['Multi C Cal'] = Prior_LGR_Data['Multi C Cal'].astype(str)
Prior_LGR_Data = Prior_LGR_Data[start:end]
Prior_LGR_Data['error_1'] = np.where(Prior_LGR_Data['Test'] == '       Disabled', 'TRUE', 'FALSE')

Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['error_1'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['error_1'])

Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - NH3 analyser'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'TRUE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - NH3 analyser'] == 'TRUE')].index,inplace =True)

Prior_LGR_Data['CH4 (ppm)'] = Prior_LGR_Data['CH4 (ppm)'].astype(str)
Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] = Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'].astype(str)
Prior_LGR_Data['CO2 (ppm)'] = Prior_LGR_Data['CO2 (ppm)'].astype(str)
Prior_LGR_Data['CO (ppb)'] = Prior_LGR_Data['CO (ppb)'].astype(str)
Prior_LGR_Data['H2O (ppm) - NH3 analyser'] = Prior_LGR_Data['H2O (ppm) - NH3 analyser'].astype(str)
Prior_LGR_Data['NH3 (ppb)'] = Prior_LGR_Data['NH3 (ppb)'].astype(str)

Prior_LGR_Data['CH4_str_length'] = Prior_LGR_Data['CH4 (ppm)'].str.len()
Prior_LGR_Data['H2O_1_str_length'] = Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'].str.len()
Prior_LGR_Data['CO2_str_length'] = Prior_LGR_Data['CO2 (ppm)'].str.len()
Prior_LGR_Data['CO_str_length'] = Prior_LGR_Data['CO (ppb)'].str.len()
Prior_LGR_Data['H2O_2_str_length'] = Prior_LGR_Data['H2O (ppm) - NH3 analyser'].str.len()
Prior_LGR_Data['NH3_str_length'] = Prior_LGR_Data['NH3 (ppb)'].str.len()

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CH4_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CH4_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_1_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_1_str_length <= 22]

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO2_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO2_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO_str_length <= 22]

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_2_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_2_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.NH3_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.NH3_str_length <= 22]

Prior_LGR_Data = Prior_LGR_Data.drop(columns=['CH4_str_length', 'H2O_1_str_length', 'CO2_str_length','CO_str_length','H2O_2_str_length','NH3_str_length'])


GHG_Data = Prior_LGR_Data[['CH4 (ppm)', 'H2O (ppm) - MultiCarbon analyser','CO2 (ppm)','CO (ppb)']]
GHG_Data['CH4 (ppm)'] = GHG_Data['CH4 (ppm)'].astype(float)
GHG_Data['H2O (ppm) - MultiCarbon analyser'] = GHG_Data['H2O (ppm) - MultiCarbon analyser'].astype(float)
GHG_Data['CO2 (ppm)'] = GHG_Data['CO2 (ppm)'].astype(float)
GHG_Data['CO (ppb)'] = GHG_Data['CO (ppb)'].astype(float)

start_CO_Anom_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,34,6)
end_CO_Anom_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,34,8)
#GHG_Data.drop(GHG_Data.loc[start_CO_Anom_1:end_CO_Anom_1].index, inplace=True)
GHG_Data.loc[start_CO_Anom_1:end_CO_Anom_1, ('CO (ppb)')] = np.nan

start_CO_Anom_2 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,39,39)
end_CO_Anom_2 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,39,41)
#GHG_Data.drop(GHG_Data.loc[start_CO_Anom_2:end_CO_Anom_2].index, inplace=True)
GHG_Data.loc[start_CO_Anom_2:end_CO_Anom_2, ('CO (ppb)')] = np.nan

start_CO_Anom_3 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,42,19)
end_CO_Anom_3 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,42,21)
#GHG_Data.drop(GHG_Data.loc[start_CO_Anom_3:end_CO_Anom_3].index, inplace=True)
GHG_Data.loc[start_CO_Anom_3:end_CO_Anom_3, ('CO (ppb)')] = np.nan

start_CO_Anom_4 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,46,57)
end_CO_Anom_4 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,46,59)
#GHG_Data.drop(GHG_Data.loc[start_CO_Anom_4:end_CO_Anom_4].index, inplace=True)
GHG_Data.loc[start_CO_Anom_4:end_CO_Anom_4, ('CO (ppb)')] = np.nan

GHG_Data['NH3 (ppm)'] = np.nan
GHG_Data['H2O (ppm) - NH3 analyser'] = np.nan

GHG_Data.rename(columns={'CO (ppb)': 'CO (ppm)'}, inplace = True)

Audit1 = GHG_Data[['CH4 (ppm)', 'CO2 (ppm)','CO (ppm)', 'NH3 (ppm)']]

start = start_Audit_Day_2
end = end_Audit_Day_2

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

prior_Audit_Day = start - timedelta(days=1)
prior_Audit_str = str(prior_Audit_Day.strftime("%Y")) + str(prior_Audit_Day.strftime("%m")) + str(prior_Audit_Day.strftime("%d"))

if start_Audit_str == end_Audit_str:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_Audit_Import_1)
else:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_Audit_Import_1)
    
ghg_frames = []

for csv in csv_files:
    
    csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv2, usecols=[0,1,2,4,6,8,32,33,35,54,55],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False ) #
    ghg_frames.append(df)

Prior_LGR_Data = pd.concat(ghg_frames)

Prior_LGR_Data['row_numbers']=(Prior_LGR_Data.index).astype(float) 
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['row_numbers'] <= 9)].index,inplace =True)
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['row_numbers'])

Prior_LGR_Data.rename(columns={0: 'Date'}, inplace=True)
Prior_LGR_Data.rename(columns={1: 'Time'}, inplace=True)
Prior_LGR_Data.rename(columns={2: 'CH4 (ppm)'}, inplace=True)
Prior_LGR_Data.rename(columns={4: 'H2O (ppm) - MultiCarbon analyser'}, inplace=True)
Prior_LGR_Data.rename(columns={6: 'CO2 (ppm)'}, inplace=True)
Prior_LGR_Data.rename(columns={8: 'CO (ppb)'}, inplace=True)
Prior_LGR_Data.rename(columns={32: 'Test'}, inplace=True)
Prior_LGR_Data.rename(columns={33: 'NH3 (ppb)'}, inplace=True) #NH3 is labelled as NH4 in early raw files
Prior_LGR_Data.rename(columns={35: 'H2O (ppm) - NH3 analyser'}, inplace=True)
Prior_LGR_Data.rename(columns={54: 'Multi C Cal'}, inplace=True)
Prior_LGR_Data.rename(columns={55: 'NH3 Cal'}, inplace=True)

Prior_LGR_Data['Date'] = Prior_LGR_Data['Date'].astype(str)
Prior_LGR_Data['Time'] = Prior_LGR_Data['Time'].astype(str)
Prior_LGR_Data['Date_length'] = Prior_LGR_Data['Date'].str.len()
Prior_LGR_Data['Time_length'] = Prior_LGR_Data['Time'].str.len()
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.Date_length == 10] #checking that the cells of GHG_Data['Date'] have only 10 characters such as with 01/01/2019
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.Time_length == 8] #checking that the cells of GHG_Data['Time'] have only 8 characters such as with 12:00:00
Prior_LGR_Data['datetime'] = Prior_LGR_Data['Date']+' '+ Prior_LGR_Data['Time']# added Date and time into new columns
Prior_LGR_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in Prior_LGR_Data['datetime']] #converts the dateTime format from string to python dateTime
Prior_LGR_Data.index = Prior_LGR_Data['datetime']
Prior_LGR_Data = Prior_LGR_Data.sort_index()
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['Time', 'Date', 'Date_length','datetime','Time_length'])


Prior_LGR_Data = Prior_LGR_Data[start:end]

Prior_LGR_Data['error_1'] = np.where(Prior_LGR_Data['Test'] == '       Disabled', 'TRUE', 'FALSE')

Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['error_1'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['error_1'])

Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - NH3 analyser'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'TRUE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - NH3 analyser'] == 'TRUE')].index,inplace =True)

Prior_LGR_Data['CH4 (ppm)'] = Prior_LGR_Data['CH4 (ppm)'].astype(str)
Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] = Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'].astype(str)
Prior_LGR_Data['CO2 (ppm)'] = Prior_LGR_Data['CO2 (ppm)'].astype(str)
Prior_LGR_Data['CO (ppb)'] = Prior_LGR_Data['CO (ppb)'].astype(str)
Prior_LGR_Data['H2O (ppm) - NH3 analyser'] = Prior_LGR_Data['H2O (ppm) - NH3 analyser'].astype(str)
Prior_LGR_Data['NH3 (ppb)'] = Prior_LGR_Data['NH3 (ppb)'].astype(str)

Prior_LGR_Data['CH4_str_length'] = Prior_LGR_Data['CH4 (ppm)'].str.len()
Prior_LGR_Data['H2O_1_str_length'] = Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'].str.len()
Prior_LGR_Data['CO2_str_length'] = Prior_LGR_Data['CO2 (ppm)'].str.len()
Prior_LGR_Data['CO_str_length'] = Prior_LGR_Data['CO (ppb)'].str.len()
Prior_LGR_Data['H2O_2_str_length'] = Prior_LGR_Data['H2O (ppm) - NH3 analyser'].str.len()
Prior_LGR_Data['NH3_str_length'] = Prior_LGR_Data['NH3 (ppb)'].str.len()

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CH4_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CH4_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_1_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_1_str_length <= 22]

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO2_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO2_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO_str_length <= 22]

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_2_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_2_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.NH3_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.NH3_str_length <= 22]

Prior_LGR_Data = Prior_LGR_Data.drop(columns=['CH4_str_length', 'H2O_1_str_length', 'CO2_str_length','CO_str_length','H2O_2_str_length','NH3_str_length'])

GHG_Data = Prior_LGR_Data[['CH4 (ppm)', 'H2O (ppm) - MultiCarbon analyser','CO2 (ppm)','CO (ppb)', 'Multi C Cal', 'NH3 Cal']]
GHG_Data['CH4 (ppm)'] = GHG_Data['CH4 (ppm)'].astype(float)
GHG_Data['H2O (ppm) - MultiCarbon analyser'] = GHG_Data['H2O (ppm) - MultiCarbon analyser'].astype(float)
GHG_Data['CO2 (ppm)'] = GHG_Data['CO2 (ppm)'].astype(float)
GHG_Data['CO (ppb)'] = GHG_Data['CO (ppb)'].astype(float)

GHG_Data['NH3 (ppm)'] = np.nan
GHG_Data['H2O (ppm) - NH3 analyser'] = np.nan

GHG_Data.rename(columns={'CO (ppb)': 'CO (ppm)'}, inplace = True)

Audit2 = GHG_Data[['CH4 (ppm)', 'CO2 (ppm)','CO (ppm)', 'NH3 (ppm)']]

start = start_Audit_Day_3
end = end_Audit_Day_3

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

prior_Audit_Day = start - timedelta(days=1)
prior_Audit_str = str(prior_Audit_Day.strftime("%Y")) + str(prior_Audit_Day.strftime("%m")) + str(prior_Audit_Day.strftime("%d"))

if start_Audit_str == end_Audit_str:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_Audit_Import_1)
else:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_Audit_Import_1)
    
ghg_frames = []

for csv in csv_files:
    
    csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv2, usecols=[0,1,2,4,6,8,32,33,35,54,55],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False ) #
    ghg_frames.append(df)

Prior_LGR_Data = pd.concat(ghg_frames)

Prior_LGR_Data['row_numbers']=(Prior_LGR_Data.index).astype(float) 
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['row_numbers'] <= 9)].index,inplace =True)
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['row_numbers'])

Prior_LGR_Data.rename(columns={0: 'Date'}, inplace=True)
Prior_LGR_Data.rename(columns={1: 'Time'}, inplace=True)
Prior_LGR_Data.rename(columns={2: 'CH4 (ppm)'}, inplace=True)
Prior_LGR_Data.rename(columns={4: 'H2O (ppm) - MultiCarbon analyser'}, inplace=True)
Prior_LGR_Data.rename(columns={6: 'CO2 (ppm)'}, inplace=True)
Prior_LGR_Data.rename(columns={8: 'CO (ppb)'}, inplace=True)
Prior_LGR_Data.rename(columns={32: 'Test'}, inplace=True)
Prior_LGR_Data.rename(columns={33: 'NH3 (ppb)'}, inplace=True) #NH3 is labelled as NH4 in early raw files
Prior_LGR_Data.rename(columns={35: 'H2O (ppm) - NH3 analyser'}, inplace=True)
Prior_LGR_Data.rename(columns={54: 'Multi C Cal'}, inplace=True)
Prior_LGR_Data.rename(columns={55: 'NH3 Cal'}, inplace=True)

Prior_LGR_Data['Date'] = Prior_LGR_Data['Date'].astype(str)
Prior_LGR_Data['Time'] = Prior_LGR_Data['Time'].astype(str)
Prior_LGR_Data['Date_length'] = Prior_LGR_Data['Date'].str.len()
Prior_LGR_Data['Time_length'] = Prior_LGR_Data['Time'].str.len()
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.Date_length == 10] #checking that the cells of GHG_Data['Date'] have only 10 characters such as with 01/01/2019
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.Time_length == 8] #checking that the cells of GHG_Data['Time'] have only 8 characters such as with 12:00:00
Prior_LGR_Data['datetime'] = Prior_LGR_Data['Date']+' '+ Prior_LGR_Data['Time']# added Date and time into new columns
Prior_LGR_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in Prior_LGR_Data['datetime']] #converts the dateTime format from string to python dateTime
Prior_LGR_Data.index = Prior_LGR_Data['datetime']
Prior_LGR_Data = Prior_LGR_Data.sort_index()
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['Time', 'Date', 'Date_length','datetime','Time_length'])

Prior_LGR_Data = Prior_LGR_Data[start:end]

Prior_LGR_Data['error_1'] = np.where(Prior_LGR_Data['Test'] == '       Disabled', 'TRUE', 'FALSE')

Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['error_1'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['error_1'])

Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - NH3 analyser'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'TRUE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - NH3 analyser'] == 'TRUE')].index,inplace =True)

Prior_LGR_Data['CH4 (ppm)'] = Prior_LGR_Data['CH4 (ppm)'].astype(str)
Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] = Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'].astype(str)
Prior_LGR_Data['CO2 (ppm)'] = Prior_LGR_Data['CO2 (ppm)'].astype(str)
Prior_LGR_Data['CO (ppb)'] = Prior_LGR_Data['CO (ppb)'].astype(str)
Prior_LGR_Data['H2O (ppm) - NH3 analyser'] = Prior_LGR_Data['H2O (ppm) - NH3 analyser'].astype(str)
Prior_LGR_Data['NH3 (ppb)'] = Prior_LGR_Data['NH3 (ppb)'].astype(str)

Prior_LGR_Data['CH4_str_length'] = Prior_LGR_Data['CH4 (ppm)'].str.len()
Prior_LGR_Data['H2O_1_str_length'] = Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'].str.len()
Prior_LGR_Data['CO2_str_length'] = Prior_LGR_Data['CO2 (ppm)'].str.len()
Prior_LGR_Data['CO_str_length'] = Prior_LGR_Data['CO (ppb)'].str.len()
Prior_LGR_Data['H2O_2_str_length'] = Prior_LGR_Data['H2O (ppm) - NH3 analyser'].str.len()
Prior_LGR_Data['NH3_str_length'] = Prior_LGR_Data['NH3 (ppb)'].str.len()

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CH4_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CH4_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_1_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_1_str_length <= 22]

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO2_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO2_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO_str_length <= 22]

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_2_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_2_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.NH3_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.NH3_str_length <= 22]

Prior_LGR_Data = Prior_LGR_Data.drop(columns=['CH4_str_length', 'H2O_1_str_length', 'CO2_str_length','CO_str_length','H2O_2_str_length','NH3_str_length'])

GHG_Data = Prior_LGR_Data[['CH4 (ppm)', 'H2O (ppm) - MultiCarbon analyser','CO2 (ppm)','CO (ppb)', 'Multi C Cal', 'NH3 Cal']]
GHG_Data['CH4 (ppm)'] = GHG_Data['CH4 (ppm)'].astype(float)
GHG_Data['H2O (ppm) - MultiCarbon analyser'] = GHG_Data['H2O (ppm) - MultiCarbon analyser'].astype(float)
GHG_Data['CO2 (ppm)'] = GHG_Data['CO2 (ppm)'].astype(float)
GHG_Data['CO (ppb)'] = GHG_Data['CO (ppb)'].astype(float)

GHG_Data['NH3 (ppm)'] = np.nan
GHG_Data['H2O (ppm) - NH3 analyser'] = np.nan

GHG_Data.rename(columns={'CO (ppb)': 'CO (ppm)'}, inplace = True)

Audit3 = GHG_Data[['CH4 (ppm)', 'CO2 (ppm)','CO (ppm)', 'NH3 (ppm)']]

start = start_Audit_Day_4
end = end_Audit_Day_4

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

prior_Audit_Day = start - timedelta(days=1)
prior_Audit_str = str(prior_Audit_Day.strftime("%Y")) + str(prior_Audit_Day.strftime("%m")) + str(prior_Audit_Day.strftime("%d"))

if start_Audit_str == end_Audit_str:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_Audit_Import_1)
else:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_Audit_Import_1)
    
ghg_frames = []

for csv in csv_files:
    
    csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv2, usecols=[0,1,2,4,6,8,32,33,35,54,55],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False ) #
    ghg_frames.append(df)

Prior_LGR_Data = pd.concat(ghg_frames)

Prior_LGR_Data['row_numbers']=(Prior_LGR_Data.index).astype(float) 
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['row_numbers'] <= 9)].index,inplace =True)
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['row_numbers'])

Prior_LGR_Data.rename(columns={0: 'Date'}, inplace=True)
Prior_LGR_Data.rename(columns={1: 'Time'}, inplace=True)
Prior_LGR_Data.rename(columns={2: 'CH4 (ppm)'}, inplace=True)
Prior_LGR_Data.rename(columns={4: 'H2O (ppm) - MultiCarbon analyser'}, inplace=True)
Prior_LGR_Data.rename(columns={6: 'CO2 (ppm)'}, inplace=True)
Prior_LGR_Data.rename(columns={8: 'CO (ppb)'}, inplace=True)
Prior_LGR_Data.rename(columns={32: 'Test'}, inplace=True)
Prior_LGR_Data.rename(columns={33: 'NH3 (ppb)'}, inplace=True) #NH3 is labelled as NH4 in early raw files
Prior_LGR_Data.rename(columns={35: 'H2O (ppm) - NH3 analyser'}, inplace=True)
Prior_LGR_Data.rename(columns={54: 'Multi C Cal'}, inplace=True)
Prior_LGR_Data.rename(columns={55: 'NH3 Cal'}, inplace=True)

Prior_LGR_Data['Date'] = Prior_LGR_Data['Date'].astype(str)
Prior_LGR_Data['Time'] = Prior_LGR_Data['Time'].astype(str)
Prior_LGR_Data['Date_length'] = Prior_LGR_Data['Date'].str.len()
Prior_LGR_Data['Time_length'] = Prior_LGR_Data['Time'].str.len()
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.Date_length == 10] #checking that the cells of GHG_Data['Date'] have only 10 characters such as with 01/01/2019
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.Time_length == 8] #checking that the cells of GHG_Data['Time'] have only 8 characters such as with 12:00:00
Prior_LGR_Data['datetime'] = Prior_LGR_Data['Date']+' '+ Prior_LGR_Data['Time']# added Date and time into new columns
Prior_LGR_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in Prior_LGR_Data['datetime']] #converts the dateTime format from string to python dateTime
Prior_LGR_Data.index = Prior_LGR_Data['datetime']
Prior_LGR_Data = Prior_LGR_Data.sort_index()
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['Time', 'Date', 'Date_length','datetime','Time_length'])

Prior_LGR_Data = Prior_LGR_Data[start:end]

Prior_LGR_Data['error_1'] = np.where(Prior_LGR_Data['Test'] == '       Disabled', 'TRUE', 'FALSE')

Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['error_1'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['error_1'])

Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - NH3 analyser'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'TRUE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - NH3 analyser'] == 'TRUE')].index,inplace =True)

Prior_LGR_Data['CH4 (ppm)'] = Prior_LGR_Data['CH4 (ppm)'].astype(str)
Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] = Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'].astype(str)
Prior_LGR_Data['CO2 (ppm)'] = Prior_LGR_Data['CO2 (ppm)'].astype(str)
Prior_LGR_Data['CO (ppb)'] = Prior_LGR_Data['CO (ppb)'].astype(str)
Prior_LGR_Data['H2O (ppm) - NH3 analyser'] = Prior_LGR_Data['H2O (ppm) - NH3 analyser'].astype(str)
Prior_LGR_Data['NH3 (ppb)'] = Prior_LGR_Data['NH3 (ppb)'].astype(str)

Prior_LGR_Data['CH4_str_length'] = Prior_LGR_Data['CH4 (ppm)'].str.len()
Prior_LGR_Data['H2O_1_str_length'] = Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'].str.len()
Prior_LGR_Data['CO2_str_length'] = Prior_LGR_Data['CO2 (ppm)'].str.len()
Prior_LGR_Data['CO_str_length'] = Prior_LGR_Data['CO (ppb)'].str.len()
Prior_LGR_Data['H2O_2_str_length'] = Prior_LGR_Data['H2O (ppm) - NH3 analyser'].str.len()
Prior_LGR_Data['NH3_str_length'] = Prior_LGR_Data['NH3 (ppb)'].str.len()

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CH4_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CH4_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_1_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_1_str_length <= 22]

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO2_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO2_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO_str_length <= 22]

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_2_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_2_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.NH3_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.NH3_str_length <= 22]

Prior_LGR_Data = Prior_LGR_Data.drop(columns=['CH4_str_length', 'H2O_1_str_length', 'CO2_str_length','CO_str_length','H2O_2_str_length','NH3_str_length'])

GHG_Data = Prior_LGR_Data[['CH4 (ppm)', 'H2O (ppm) - MultiCarbon analyser','CO2 (ppm)','CO (ppb)', 'Multi C Cal', 'NH3 Cal']]
GHG_Data['CH4 (ppm)'] = GHG_Data['CH4 (ppm)'].astype(float)
GHG_Data['H2O (ppm) - MultiCarbon analyser'] = GHG_Data['H2O (ppm) - MultiCarbon analyser'].astype(float)
GHG_Data['CO2 (ppm)'] = GHG_Data['CO2 (ppm)'].astype(float)
GHG_Data['CO (ppb)'] = GHG_Data['CO (ppb)'].astype(float)

GHG_Data['NH3 (ppm)'] = np.nan
GHG_Data['H2O (ppm) - NH3 analyser'] = np.nan

GHG_Data.rename(columns={'CO (ppb)': 'CO (ppm)'}, inplace = True)

Audit4 = GHG_Data[['CH4 (ppm)', 'CO2 (ppm)','CO (ppm)', 'NH3 (ppm)']]

start = start_Audit_Day_5
end = end_Audit_Day_5

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

prior_Audit_Day = start - timedelta(days=1)
prior_Audit_str = str(prior_Audit_Day.strftime("%Y")) + str(prior_Audit_Day.strftime("%m")) + str(prior_Audit_Day.strftime("%d"))

if start_Audit_str == end_Audit_str:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_Audit_Import_1)
else:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_Audit_Import_1)
    
ghg_frames = []

for csv in csv_files:
    
    csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv2, usecols=[0,1,2,4,6,8,32,33,35,54,55],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False ) #
    ghg_frames.append(df)

Prior_LGR_Data = pd.concat(ghg_frames)

Prior_LGR_Data['row_numbers']=(Prior_LGR_Data.index).astype(float) 
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['row_numbers'] <= 9)].index,inplace =True)
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['row_numbers'])

Prior_LGR_Data.rename(columns={0: 'Date'}, inplace=True)
Prior_LGR_Data.rename(columns={1: 'Time'}, inplace=True)
Prior_LGR_Data.rename(columns={2: 'CH4 (ppm)'}, inplace=True)
Prior_LGR_Data.rename(columns={4: 'H2O (ppm) - MultiCarbon analyser'}, inplace=True)
Prior_LGR_Data.rename(columns={6: 'CO2 (ppm)'}, inplace=True)
Prior_LGR_Data.rename(columns={8: 'CO (ppb)'}, inplace=True)
Prior_LGR_Data.rename(columns={32: 'Test'}, inplace=True)
Prior_LGR_Data.rename(columns={33: 'NH3 (ppb)'}, inplace=True) #NH3 is labelled as NH4 in early raw files
Prior_LGR_Data.rename(columns={35: 'H2O (ppm) - NH3 analyser'}, inplace=True)
Prior_LGR_Data.rename(columns={54: 'Multi C Cal'}, inplace=True)
Prior_LGR_Data.rename(columns={55: 'NH3 Cal'}, inplace=True)

Prior_LGR_Data['Date'] = Prior_LGR_Data['Date'].astype(str)
Prior_LGR_Data['Time'] = Prior_LGR_Data['Time'].astype(str)
Prior_LGR_Data['Date_length'] = Prior_LGR_Data['Date'].str.len()
Prior_LGR_Data['Time_length'] = Prior_LGR_Data['Time'].str.len()
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.Date_length == 10] #checking that the cells of GHG_Data['Date'] have only 10 characters such as with 01/01/2019
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.Time_length == 8] #checking that the cells of GHG_Data['Time'] have only 8 characters such as with 12:00:00
Prior_LGR_Data['datetime'] = Prior_LGR_Data['Date']+' '+ Prior_LGR_Data['Time']# added Date and time into new columns
Prior_LGR_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in Prior_LGR_Data['datetime']] #converts the dateTime format from string to python dateTime
Prior_LGR_Data.index = Prior_LGR_Data['datetime']
Prior_LGR_Data = Prior_LGR_Data.sort_index()
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['Time', 'Date', 'Date_length','datetime','Time_length'])

Prior_LGR_Data = Prior_LGR_Data[start:end]

Prior_LGR_Data['error_1'] = np.where(Prior_LGR_Data['Test'] == '       Disabled', 'TRUE', 'FALSE')

Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['error_1'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['error_1'])

Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - NH3 analyser'] == 'FALSE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'TRUE')].index,inplace =True)
Prior_LGR_Data.drop(Prior_LGR_Data[(Prior_LGR_Data['H2O (ppm) - NH3 analyser'] == 'TRUE')].index,inplace =True)

Prior_LGR_Data['CH4 (ppm)'] = Prior_LGR_Data['CH4 (ppm)'].astype(str)
Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'] = Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'].astype(str)
Prior_LGR_Data['CO2 (ppm)'] = Prior_LGR_Data['CO2 (ppm)'].astype(str)
Prior_LGR_Data['CO (ppb)'] = Prior_LGR_Data['CO (ppb)'].astype(str)
Prior_LGR_Data['H2O (ppm) - NH3 analyser'] = Prior_LGR_Data['H2O (ppm) - NH3 analyser'].astype(str)
Prior_LGR_Data['NH3 (ppb)'] = Prior_LGR_Data['NH3 (ppb)'].astype(str)

Prior_LGR_Data['CH4_str_length'] = Prior_LGR_Data['CH4 (ppm)'].str.len()
Prior_LGR_Data['H2O_1_str_length'] = Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'].str.len()
Prior_LGR_Data['CO2_str_length'] = Prior_LGR_Data['CO2 (ppm)'].str.len()
Prior_LGR_Data['CO_str_length'] = Prior_LGR_Data['CO (ppb)'].str.len()
Prior_LGR_Data['H2O_2_str_length'] = Prior_LGR_Data['H2O (ppm) - NH3 analyser'].str.len()
Prior_LGR_Data['NH3_str_length'] = Prior_LGR_Data['NH3 (ppb)'].str.len()

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CH4_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CH4_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_1_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_1_str_length <= 22]

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO2_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO2_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO_str_length <= 22]

Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_2_str_length >= 12] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_2_str_length <= 22] 
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.NH3_str_length >= 12]
Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.NH3_str_length <= 22]

Prior_LGR_Data = Prior_LGR_Data.drop(columns=['CH4_str_length', 'H2O_1_str_length', 'CO2_str_length','CO_str_length','H2O_2_str_length','NH3_str_length'])


GHG_Data = Prior_LGR_Data[['CH4 (ppm)', 'H2O (ppm) - MultiCarbon analyser','CO2 (ppm)','CO (ppb)', 'Multi C Cal', 'NH3 Cal']]
GHG_Data['CH4 (ppm)'] = GHG_Data['CH4 (ppm)'].astype(float)
GHG_Data['H2O (ppm) - MultiCarbon analyser'] = GHG_Data['H2O (ppm) - MultiCarbon analyser'].astype(float)
GHG_Data['CO2 (ppm)'] = GHG_Data['CO2 (ppm)'].astype(float)
GHG_Data['CO (ppb)'] = GHG_Data['CO (ppb)'].astype(float)

GHG_Data['NH3 (ppm)'] = np.nan
GHG_Data['H2O (ppm) - NH3 analyser'] = np.nan

GHG_Data.rename(columns={'CO (ppb)': 'CO (ppm)'}, inplace = True)

Audit5 = GHG_Data[['CH4 (ppm)', 'CO2 (ppm)','CO (ppm)', 'NH3 (ppm)']]

start = start_NH3_Zero_1_1
end = end_NH3_Zero_1_1

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

prior_Audit_Day = start - timedelta(days=1)
prior_Audit_str = str(prior_Audit_Day.strftime("%Y")) + str(prior_Audit_Day.strftime("%m")) + str(prior_Audit_Day.strftime("%d"))

if start_Audit_str == end_Audit_str:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_Audit_Import_1)
else:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_Audit_Import_1)
    
ghg_frames = []

for csv in csv_files:
    
    csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv2, usecols=[0,1,2,4,6,8,32,33,35,54,55],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False ) #
    ghg_frames.append(df)

LGR_Data = pd.concat(ghg_frames)

LGR_Data['row_numbers']=(LGR_Data.index).astype(float) 
LGR_Data.drop(LGR_Data[(LGR_Data['row_numbers'] <= 9)].index,inplace =True)
LGR_Data = LGR_Data.drop(columns=['row_numbers'])


LGR_Data.rename(columns={0: 'Date'}, inplace=True)
LGR_Data.rename(columns={1: 'Time'}, inplace=True)
LGR_Data.rename(columns={2: 'CH4 (ppm)'}, inplace=True)
LGR_Data.rename(columns={4: 'H2O (ppm) - MultiCarbon analyser'}, inplace=True)
LGR_Data.rename(columns={6: 'CO2 (ppm)'}, inplace=True)
LGR_Data.rename(columns={8: 'CO (ppb)'}, inplace=True)
LGR_Data.rename(columns={32: 'Test'}, inplace=True)
LGR_Data.rename(columns={33: 'NH3 (ppb)'}, inplace=True)
LGR_Data.rename(columns={35: 'H2O (ppm) - NH3 analyser'}, inplace=True)
LGR_Data.rename(columns={54: 'Multi C Cal'}, inplace=True)
LGR_Data.rename(columns={55: 'NH3 Cal'}, inplace=True)

LGR_drop_list = list(LGR_Data.columns.values)
LGR_drop_list.remove('Date')
LGR_drop_list.remove('Time')
LGR_drop_list.remove('CH4 (ppm)')
LGR_drop_list.remove('H2O (ppm) - MultiCarbon analyser')
LGR_drop_list.remove('CO2 (ppm)')
LGR_drop_list.remove('CO (ppb)')
LGR_drop_list.remove('NH3 (ppb)')
LGR_drop_list.remove('Test')
LGR_drop_list.remove('H2O (ppm) - NH3 analyser')
LGR_drop_list.remove('Multi C Cal')
LGR_drop_list.remove('NH3 Cal')
LGR_Data = LGR_Data.drop(columns=LGR_drop_list)

LGR_Data['Date'] = LGR_Data['Date'].astype(str)
LGR_Data['Time'] = LGR_Data['Time'].astype(str)
LGR_Data['Date_length'] = LGR_Data['Date'].str.len()
LGR_Data['Time_length'] = LGR_Data['Time'].str.len()
LGR_Data=LGR_Data[LGR_Data.Date_length == 10] #checking that the cells of GHG_Data['Date'] have only 10 characters such as with 01/01/2019
LGR_Data=LGR_Data[LGR_Data.Time_length == 8] #checking that the cells of GHG_Data['Time'] have only 8 characters such as with 12:00:00
LGR_Data['datetime'] = LGR_Data['Date']+' '+ LGR_Data['Time']# added Date and time into new columns
LGR_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in LGR_Data['datetime']] #converts the dateTime format from string to python dateTime
LGR_Data.index =LGR_Data['datetime']
LGR_Data = LGR_Data.sort_index()
LGR_Data = LGR_Data.drop(columns=['Time', 'Date', 'Date_length','Time_length', 'datetime'])

LGR_Data['error_2'] = np.where(LGR_Data['Test'] == '       Disabled', 'TRUE', 'FALSE')
LGR_Data.drop(LGR_Data[(LGR_Data['error_2'] == 'FALSE')].index,inplace =True)
LGR_Data = LGR_Data.drop(columns=['Test', 'error_2'])

LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'FALSE')].index,inplace =True)
LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - NH3 analyser'] == 'FALSE')].index,inplace =True)
LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'TRUE')].index,inplace =True)
LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - NH3 analyser'] == 'TRUE')].index,inplace =True) 

LGR_Data['CH4 (ppm)'] = LGR_Data['CH4 (ppm)'].astype(str)
LGR_Data['H2O (ppm) - MultiCarbon analyser'] = LGR_Data['H2O (ppm) - MultiCarbon analyser'].astype(str)
LGR_Data['CO2 (ppm)'] = LGR_Data['CO2 (ppm)'].astype(str)
LGR_Data['CO (ppb)'] = LGR_Data['CO (ppb)'].astype(str)
LGR_Data['H2O (ppm) - NH3 analyser'] = LGR_Data['H2O (ppm) - NH3 analyser'].astype(str)
LGR_Data['NH3 (ppb)'] = LGR_Data['NH3 (ppb)'].astype(str)

LGR_Data['CH4_str_length'] = LGR_Data['CH4 (ppm)'].str.len()
LGR_Data['H2O_1_str_length'] = LGR_Data['H2O (ppm) - MultiCarbon analyser'].str.len()
LGR_Data['CO2_str_length'] = LGR_Data['CO2 (ppm)'].str.len()
LGR_Data['CO_str_length'] = LGR_Data['CO (ppb)'].str.len()
LGR_Data['H2O_2_str_length'] = LGR_Data['H2O (ppm) - NH3 analyser'].str.len()
LGR_Data['NH3_str_length'] = LGR_Data['NH3 (ppb)'].str.len()

LGR_Data=LGR_Data[LGR_Data.CH4_str_length >= 1] 
LGR_Data=LGR_Data[LGR_Data.CH4_str_length <= 22] 
LGR_Data=LGR_Data[LGR_Data.H2O_1_str_length >= 1]
LGR_Data=LGR_Data[LGR_Data.H2O_1_str_length <= 22]

LGR_Data=LGR_Data[LGR_Data.CO2_str_length >= 1] 
LGR_Data=LGR_Data[LGR_Data.CO2_str_length <= 22] 
LGR_Data=LGR_Data[LGR_Data.CO_str_length >= 1]
LGR_Data=LGR_Data[LGR_Data.CO_str_length <= 22]

LGR_Data=LGR_Data[LGR_Data.H2O_2_str_length >= 1] 
LGR_Data=LGR_Data[LGR_Data.H2O_2_str_length <= 22] 
LGR_Data=LGR_Data[LGR_Data.NH3_str_length >= 1]
LGR_Data=LGR_Data[LGR_Data.NH3_str_length <= 22]

LGR_Data = LGR_Data.drop(columns=['CH4_str_length', 'H2O_1_str_length', 'CO2_str_length','CO_str_length','H2O_2_str_length','NH3_str_length'])

Ammonia_Data = LGR_Data[['H2O (ppm) - NH3 analyser','NH3 (ppb)', 'Multi C Cal', 'NH3 Cal']]
Ammonia_Data.rename(columns={'NH3 (ppb)': 'NH3 (ppm)' }, inplace = True)
Ammonia_Data['H2O (ppm) - NH3 analyser'] = Ammonia_Data['H2O (ppm) - NH3 analyser'].astype(float)
Ammonia_Data['NH3 (ppm)'] = Ammonia_Data['NH3 (ppm)'].astype(float)

Ammonia_Data['CH4 (ppm)'] = np.nan
Ammonia_Data['H2O (ppm) - MultiCarbon analyser'] = np.nan
Ammonia_Data['CO (ppb)'] = np.nan
Ammonia_Data['CO2 (ppm)'] = np.nan

Ammonia_Data.rename(columns={'CO (ppb)': 'CO (ppm)'}, inplace = True)

Ammonia_Zero_1_1 = Ammonia_Data[['CH4 (ppm)', 'CO2 (ppm)','CO (ppm)', 'NH3 (ppm)']]

start = start_NH3_Zero_1_2
end = end_NH3_Zero_1_2

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

prior_Audit_Day = start - timedelta(days=1)
prior_Audit_str = str(prior_Audit_Day.strftime("%Y")) + str(prior_Audit_Day.strftime("%m")) + str(prior_Audit_Day.strftime("%d"))

if start_Audit_str == end_Audit_str:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_Audit_Import_1)
else:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_Audit_Import_1)
    
ghg_frames = []

for csv in csv_files:
    
    csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv2, usecols=[0,1,2,4,6,8,32,33,35,54,55],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False ) #
    ghg_frames.append(df)

LGR_Data = pd.concat(ghg_frames)

LGR_Data['row_numbers']=(LGR_Data.index).astype(float) 
LGR_Data.drop(LGR_Data[(LGR_Data['row_numbers'] <= 9)].index,inplace =True)
LGR_Data = LGR_Data.drop(columns=['row_numbers'])

LGR_Data.rename(columns={0: 'Date'}, inplace=True)
LGR_Data.rename(columns={1: 'Time'}, inplace=True)
LGR_Data.rename(columns={2: 'CH4 (ppm)'}, inplace=True)
LGR_Data.rename(columns={4: 'H2O (ppm) - MultiCarbon analyser'}, inplace=True)
LGR_Data.rename(columns={6: 'CO2 (ppm)'}, inplace=True)
LGR_Data.rename(columns={8: 'CO (ppb)'}, inplace=True)
LGR_Data.rename(columns={32: 'Test'}, inplace=True)
LGR_Data.rename(columns={33: 'NH3 (ppb)'}, inplace=True)
LGR_Data.rename(columns={35: 'H2O (ppm) - NH3 analyser'}, inplace=True)
LGR_Data.rename(columns={54: 'Multi C Cal'}, inplace=True)
LGR_Data.rename(columns={55: 'NH3 Cal'}, inplace=True)

LGR_drop_list = list(LGR_Data.columns.values)
LGR_drop_list.remove('Date')
LGR_drop_list.remove('Time')
LGR_drop_list.remove('CH4 (ppm)')
LGR_drop_list.remove('H2O (ppm) - MultiCarbon analyser')
LGR_drop_list.remove('CO2 (ppm)')
LGR_drop_list.remove('CO (ppb)')
LGR_drop_list.remove('NH3 (ppb)')
LGR_drop_list.remove('Test')
LGR_drop_list.remove('H2O (ppm) - NH3 analyser')
LGR_drop_list.remove('Multi C Cal')
LGR_drop_list.remove('NH3 Cal')
LGR_Data = LGR_Data.drop(columns=LGR_drop_list)

LGR_Data['Date'] = LGR_Data['Date'].astype(str)
LGR_Data['Time'] = LGR_Data['Time'].astype(str)
LGR_Data['Date_length'] = LGR_Data['Date'].str.len()
LGR_Data['Time_length'] = LGR_Data['Time'].str.len()
LGR_Data=LGR_Data[LGR_Data.Date_length == 10] #checking that the cells of GHG_Data['Date'] have only 10 characters such as with 01/01/2019
LGR_Data=LGR_Data[LGR_Data.Time_length == 8] #checking that the cells of GHG_Data['Time'] have only 8 characters such as with 12:00:00
LGR_Data['datetime'] = LGR_Data['Date']+' '+ LGR_Data['Time']# added Date and time into new columns
LGR_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in LGR_Data['datetime']] #converts the dateTime format from string to python dateTime
LGR_Data.index =LGR_Data['datetime']
LGR_Data = LGR_Data.sort_index()
LGR_Data = LGR_Data.drop(columns=['Time', 'Date', 'Date_length','Time_length', 'datetime'])

LGR_Data['error_2'] = np.where(LGR_Data['Test'] == '       Disabled', 'TRUE', 'FALSE')
LGR_Data.drop(LGR_Data[(LGR_Data['error_2'] == 'FALSE')].index,inplace =True)
LGR_Data = LGR_Data.drop(columns=['Test', 'error_2'])

LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'FALSE')].index,inplace =True)
LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - NH3 analyser'] == 'FALSE')].index,inplace =True)
LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'TRUE')].index,inplace =True)
LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - NH3 analyser'] == 'TRUE')].index,inplace =True) 

LGR_Data['CH4 (ppm)'] = LGR_Data['CH4 (ppm)'].astype(str)
LGR_Data['H2O (ppm) - MultiCarbon analyser'] = LGR_Data['H2O (ppm) - MultiCarbon analyser'].astype(str)
LGR_Data['CO2 (ppm)'] = LGR_Data['CO2 (ppm)'].astype(str)
LGR_Data['CO (ppb)'] = LGR_Data['CO (ppb)'].astype(str)
LGR_Data['H2O (ppm) - NH3 analyser'] = LGR_Data['H2O (ppm) - NH3 analyser'].astype(str)
LGR_Data['NH3 (ppb)'] = LGR_Data['NH3 (ppb)'].astype(str)

LGR_Data['CH4_str_length'] = LGR_Data['CH4 (ppm)'].str.len()
LGR_Data['H2O_1_str_length'] = LGR_Data['H2O (ppm) - MultiCarbon analyser'].str.len()
LGR_Data['CO2_str_length'] = LGR_Data['CO2 (ppm)'].str.len()
LGR_Data['CO_str_length'] = LGR_Data['CO (ppb)'].str.len()
LGR_Data['H2O_2_str_length'] = LGR_Data['H2O (ppm) - NH3 analyser'].str.len()
LGR_Data['NH3_str_length'] = LGR_Data['NH3 (ppb)'].str.len()

LGR_Data=LGR_Data[LGR_Data.CH4_str_length >= 1] 
LGR_Data=LGR_Data[LGR_Data.CH4_str_length <= 22] 
LGR_Data=LGR_Data[LGR_Data.H2O_1_str_length >= 1]
LGR_Data=LGR_Data[LGR_Data.H2O_1_str_length <= 22]

LGR_Data=LGR_Data[LGR_Data.CO2_str_length >= 1] 
LGR_Data=LGR_Data[LGR_Data.CO2_str_length <= 22] 
LGR_Data=LGR_Data[LGR_Data.CO_str_length >= 1]
LGR_Data=LGR_Data[LGR_Data.CO_str_length <= 22]

LGR_Data=LGR_Data[LGR_Data.H2O_2_str_length >= 1] 
LGR_Data=LGR_Data[LGR_Data.H2O_2_str_length <= 22] 
LGR_Data=LGR_Data[LGR_Data.NH3_str_length >= 1]
LGR_Data=LGR_Data[LGR_Data.NH3_str_length <= 22]

LGR_Data = LGR_Data.drop(columns=['CH4_str_length', 'H2O_1_str_length', 'CO2_str_length','CO_str_length','H2O_2_str_length','NH3_str_length'])

Ammonia_Data = LGR_Data[['H2O (ppm) - NH3 analyser','NH3 (ppb)', 'Multi C Cal', 'NH3 Cal']]
Ammonia_Data.rename(columns={'NH3 (ppb)': 'NH3 (ppm)' }, inplace = True)
Ammonia_Data['H2O (ppm) - NH3 analyser'] = Ammonia_Data['H2O (ppm) - NH3 analyser'].astype(float)
Ammonia_Data['NH3 (ppm)'] = Ammonia_Data['NH3 (ppm)'].astype(float)

Ammonia_Data['CH4 (ppm)'] = np.nan
Ammonia_Data['H2O (ppm) - MultiCarbon analyser'] = np.nan
Ammonia_Data['CO (ppb)'] = np.nan
Ammonia_Data['CO2 (ppm)'] = np.nan

Ammonia_Data.rename(columns={'CO (ppb)': 'CO (ppm)'}, inplace = True)

Ammonia_Zero_1_2 = Ammonia_Data[['CH4 (ppm)', 'CO2 (ppm)','CO (ppm)', 'NH3 (ppm)']]

start = start_Audit_Day_6 
end = end_Audit_Day_6 

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

prior_Audit_Day = start - timedelta(days=1)
prior_Audit_str = str(prior_Audit_Day.strftime("%Y")) + str(prior_Audit_Day.strftime("%m")) + str(prior_Audit_Day.strftime("%d"))

if start_Audit_str == end_Audit_str:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_Audit_Import_1)
else:
    Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_lgr.csv' # Collect CSV files
    Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_lgr.csv' # Collect CSV files
    prior_Audit_Import_1 = str(Data_Source_Folder) + str(prior_Audit_str) + '*_lgr.csv' # Collect CSV files
    csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_Audit_Import_1)
    
ghg_frames = []

for csv in csv_files:
    
    csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv2, usecols=[0,1,2,4,6,8,32,33,35,54,55],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False ) #
    ghg_frames.append(df)

LGR_Data = pd.concat(ghg_frames)

LGR_Data['row_numbers']=(LGR_Data.index).astype(float) 
LGR_Data.drop(LGR_Data[(LGR_Data['row_numbers'] <= 9)].index,inplace =True)
LGR_Data = LGR_Data.drop(columns=['row_numbers'])

LGR_Data.rename(columns={0: 'Date'}, inplace=True)
LGR_Data.rename(columns={1: 'Time'}, inplace=True)
LGR_Data.rename(columns={2: 'CH4 (ppm)'}, inplace=True)
LGR_Data.rename(columns={4: 'H2O (ppm) - MultiCarbon analyser'}, inplace=True)
LGR_Data.rename(columns={6: 'CO2 (ppm)'}, inplace=True)
LGR_Data.rename(columns={8: 'CO (ppb)'}, inplace=True)
LGR_Data.rename(columns={32: 'Test'}, inplace=True)
LGR_Data.rename(columns={33: 'NH3 (ppb)'}, inplace=True)
LGR_Data.rename(columns={35: 'H2O (ppm) - NH3 analyser'}, inplace=True)
LGR_Data.rename(columns={54: 'Multi C Cal'}, inplace=True)
LGR_Data.rename(columns={55: 'NH3 Cal'}, inplace=True)

LGR_drop_list = list(LGR_Data.columns.values)
LGR_drop_list.remove('Date')
LGR_drop_list.remove('Time')
LGR_drop_list.remove('CH4 (ppm)')
LGR_drop_list.remove('H2O (ppm) - MultiCarbon analyser')
LGR_drop_list.remove('CO2 (ppm)')
LGR_drop_list.remove('CO (ppb)')
LGR_drop_list.remove('NH3 (ppb)')
LGR_drop_list.remove('Test')
LGR_drop_list.remove('H2O (ppm) - NH3 analyser')
LGR_drop_list.remove('Multi C Cal')
LGR_drop_list.remove('NH3 Cal')
LGR_Data = LGR_Data.drop(columns=LGR_drop_list)

LGR_Data['Date'] = LGR_Data['Date'].astype(str)
LGR_Data['Time'] = LGR_Data['Time'].astype(str)
LGR_Data['Date_length'] = LGR_Data['Date'].str.len()
LGR_Data['Time_length'] = LGR_Data['Time'].str.len()
LGR_Data=LGR_Data[LGR_Data.Date_length == 10] #checking that the cells of GHG_Data['Date'] have only 10 characters such as with 01/01/2019
LGR_Data=LGR_Data[LGR_Data.Time_length == 8] #checking that the cells of GHG_Data['Time'] have only 8 characters such as with 12:00:00
LGR_Data['datetime'] = LGR_Data['Date']+' '+ LGR_Data['Time']# added Date and time into new columns
LGR_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in LGR_Data['datetime']] #converts the dateTime format from string to python dateTime
LGR_Data.index =LGR_Data['datetime']
LGR_Data = LGR_Data.sort_index()
LGR_Data = LGR_Data.drop(columns=['Time', 'Date', 'Date_length','Time_length', 'datetime'])

LGR_Data['error_2'] = np.where(LGR_Data['Test'] == '       Disabled', 'TRUE', 'FALSE')
LGR_Data.drop(LGR_Data[(LGR_Data['error_2'] == 'FALSE')].index,inplace =True)
LGR_Data = LGR_Data.drop(columns=['Test', 'error_2'])

LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'FALSE')].index,inplace =True)
LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - NH3 analyser'] == 'FALSE')].index,inplace =True)
LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'TRUE')].index,inplace =True)
LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - NH3 analyser'] == 'TRUE')].index,inplace =True) 

LGR_Data['CH4 (ppm)'] = LGR_Data['CH4 (ppm)'].astype(str)
LGR_Data['H2O (ppm) - MultiCarbon analyser'] = LGR_Data['H2O (ppm) - MultiCarbon analyser'].astype(str)
LGR_Data['CO2 (ppm)'] = LGR_Data['CO2 (ppm)'].astype(str)
LGR_Data['CO (ppb)'] = LGR_Data['CO (ppb)'].astype(str)
LGR_Data['H2O (ppm) - NH3 analyser'] = LGR_Data['H2O (ppm) - NH3 analyser'].astype(str)
LGR_Data['NH3 (ppb)'] = LGR_Data['NH3 (ppb)'].astype(str)

LGR_Data['CH4_str_length'] = LGR_Data['CH4 (ppm)'].str.len()
LGR_Data['H2O_1_str_length'] = LGR_Data['H2O (ppm) - MultiCarbon analyser'].str.len()
LGR_Data['CO2_str_length'] = LGR_Data['CO2 (ppm)'].str.len()
LGR_Data['CO_str_length'] = LGR_Data['CO (ppb)'].str.len()
LGR_Data['H2O_2_str_length'] = LGR_Data['H2O (ppm) - NH3 analyser'].str.len()
LGR_Data['NH3_str_length'] = LGR_Data['NH3 (ppb)'].str.len()

LGR_Data=LGR_Data[LGR_Data.CH4_str_length >= 1] 
LGR_Data=LGR_Data[LGR_Data.CH4_str_length <= 22] 
LGR_Data=LGR_Data[LGR_Data.H2O_1_str_length >= 1]
LGR_Data=LGR_Data[LGR_Data.H2O_1_str_length <= 22]

LGR_Data=LGR_Data[LGR_Data.CO2_str_length >= 1] 
LGR_Data=LGR_Data[LGR_Data.CO2_str_length <= 22] 
LGR_Data=LGR_Data[LGR_Data.CO_str_length >= 1]
LGR_Data=LGR_Data[LGR_Data.CO_str_length <= 22]

LGR_Data=LGR_Data[LGR_Data.H2O_2_str_length >= 1] 
LGR_Data=LGR_Data[LGR_Data.H2O_2_str_length <= 22] 
LGR_Data=LGR_Data[LGR_Data.NH3_str_length >= 1]
LGR_Data=LGR_Data[LGR_Data.NH3_str_length <= 22]

LGR_Data = LGR_Data.drop(columns=['CH4_str_length', 'H2O_1_str_length', 'CO2_str_length','CO_str_length','H2O_2_str_length','NH3_str_length'])

GHG_Data = LGR_Data[['CH4 (ppm)', 'H2O (ppm) - MultiCarbon analyser','CO2 (ppm)','CO (ppb)', 'H2O (ppm) - NH3 analyser','NH3 (ppb)', 'Multi C Cal', 'NH3 Cal']]
GHG_Data['CH4 (ppm)'] = GHG_Data['CH4 (ppm)'].astype(float)
GHG_Data['H2O (ppm) - MultiCarbon analyser'] = GHG_Data['H2O (ppm) - MultiCarbon analyser'].astype(float)
GHG_Data['CO2 (ppm)'] = GHG_Data['CO2 (ppm)'].astype(float)
GHG_Data['CO (ppb)'] = GHG_Data['CO (ppb)'].astype(float)

GHG_Data.rename(columns={'NH3 (ppb)': 'NH3 (ppm)', 'CO (ppb)': 'CO (ppm)' }, inplace = True)
GHG_Data['H2O (ppm) - NH3 analyser'] = GHG_Data['H2O (ppm) - NH3 analyser'].astype(float)
GHG_Data['NH3 (ppm)'] = GHG_Data['NH3 (ppm)'].astype(float)

Audit6 = GHG_Data[['CH4 (ppm)', 'CO2 (ppm)','CO (ppm)', 'NH3 (ppm)']]

#Audit6 = Audit6.groupby(pd.Grouper(freq=av_Freq)).mean() 
#Audit6.to_csv(str(Data_Output_Folder) + 'LGR_Calibrations_Audit_6_' + str(current_day) + '_' + str(version_number) + '.csv')

Calibrations = pd.concat([Audit1, Audit2, Audit3, Audit4, Ammonia_Zero_1_1, Ammonia_Zero_1_2, Audit5, Audit6])

#CO2 & CH4 Multicarbon Calibrations: 0 = normal operations, 1 means testing the zero, 2 means CO & CO2 & CH4 calibration, 3 means CO2 & CH4 calibrations only
#MultiCarbon_calibration_Flag: 0 = normal operations, 1 means CO & CO2 & CH4 calibration, 2 means CO2 & CH4 calibration only, 3 means CO calibration only, 4 means CO realignment
#Ammonia Calibration: 0 means normal operations, 1 means testing the zero, 2 means NH3 calibration

Calibrations['CH4_calibration_cylinder_ppm'] = np.nan
Calibrations['CO2_calibration_cylinder_ppm'] = np.nan
Calibrations['CO_calibration_cylinder_ppm'] = np.nan

Calibrations['MultiCarbon_Zero_Flag'] = 0
Calibrations['MultiCarbon_calibration_Flag'] = 0
Calibrations['NH3_Zero_Flag'] = 0

Calibrations['Calibration_Flag'] = 0

Calibrations['CH4_Zero'] = np.nan
Calibrations['CH4_LGR_Mean'] = np.nan
Calibrations['CO2_Zero'] = np.nan
Calibrations['CO2_LGR_Mean'] = np.nan
Calibrations['CO_Zero'] = np.nan
Calibrations['CO_LGR_Mean'] = np.nan
Calibrations['NH3_Zero'] = np.nan
Calibrations['NH3_LGR_Mean'] = 0

start_MultiCarbonZero_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,39,00)
end_MultiCarbonZero_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,48,00)
Calibrations.loc[start_MultiCarbonZero_1:end_MultiCarbonZero_1, ('MultiCarbon_Zero_Flag')] = 1
Calibrations.loc[start_MultiCarbonZero_1:end_MultiCarbonZero_1, ('Calibration_Flag')] = 1
MultiCarbonZero_1 = Calibrations[start_MultiCarbonZero_1:end_MultiCarbonZero_1]
MultiCarbonZero_1['MultiCarbon_Zero_Flag'] = 1 
MultiCarbonZero_1['Calibration_Flag'] = 1 
CH4_zero_1_mean = MultiCarbonZero_1['CH4 (ppm)'].mean() 
CO2_zero_1_mean = MultiCarbonZero_1['CO2 (ppm)'].mean() 

print('The Mean CH4 measurement from zero cylinder is: ' + str(CH4_zero_1_mean))
print('The Mean CO2 measurement from zero cylinder is: ' + str(CO2_zero_1_mean))

#zero_av_Freq = '1min'
#MultiCarbonZero_1 = MultiCarbonZero_1.groupby(pd.Grouper(freq=zero_av_Freq)).mean()
#CO_zero_1_mean = MultiCarbonZero_1['CO (ppm)'].min() 

start_CO_zero_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,42,00)
end_CO_zero_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,46,00)
CO_Zero_1 = Calibrations[start_CO_zero_1:end_CO_zero_1]
zero_av_Freq = '1min'
CO_Zero_1 = CO_Zero_1.groupby(pd.Grouper(freq=zero_av_Freq)).mean()
CO_zero_1_mean = CO_Zero_1['CO (ppm)'].min() 
#CO_Zero_1.to_csv(str(Data_Output_Folder) + '/CO_zero_1.csv')

print('The Mean CO measurement from zero cylinder is: ' + str(CO_zero_1_mean))

start_CO_Cal_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,55,00)
end_CO_Cal_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,3,00)
CO_Cal_1 = Calibrations[start_CO_Cal_1:end_CO_Cal_1]
CO_Cal_1_mean = CO_Cal_1['CO (ppm)'].mean() 
minimum = min(start_CO_Cal_1,end_CO_Cal_1)
maximum = max(start_CO_Cal_1,end_CO_Cal_1)
Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] = CO_Cal_1_mean
Calibrations.loc[minimum:maximum, ('MultiCarbon_Zero_Flag')] = 3
Calibrations.loc[minimum:maximum, ('Calibration_Flag')] = 1
print('The Mean CO abundance in calibration cylinder is: ' + str(CO_Cal_1_mean))

start_MultiCarbonCal_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,29,00)
end_MultiCarbonCal_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,40,00)
Calibrations.loc[start_MultiCarbonCal_1:end_MultiCarbonCal_1, ('CH4_calibration_cylinder_ppm')] = 2.058
Calibrations.loc[start_MultiCarbonCal_1:end_MultiCarbonCal_1, ('CO2_calibration_cylinder_ppm')] = 411.9
Calibrations.loc[start_MultiCarbonCal_1:end_MultiCarbonCal_1, ('MultiCarbon_calibration_Flag')] = 2
Calibrations.loc[start_MultiCarbonCal_1:end_MultiCarbonCal_1, ('Calibration_Flag')] = 1
MultiCarbonCal_1 = Calibrations[start_MultiCarbonCal_1:end_MultiCarbonCal_1]
MultiCarbonCal_1['MultiCarbon_Zero_Flag'] = 1 
MultiCarbonCal_1['Calibration_Flag'] = 1 
CH4_cal_1_mean = MultiCarbonCal_1['CH4 (ppm)'].mean() 
CO2_cal_1_mean = MultiCarbonCal_1['CO2 (ppm)'].mean() 

start_CO_recal_1a = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,55,00)
end_CO_recal_1a = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,5,00)
CO_recal_1a = Calibrations[start_CO_recal_1a:end_CO_recal_1a]
CO_recal_1_mean = CO_recal_1a['CO (ppm)'].mean() 
minimum = min(start_CO_recal_1a,end_CO_recal_1a)
maximum = max(start_CO_recal_1a,end_CO_recal_1a)
Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] = CO_recal_1_mean
Calibrations.loc[minimum:maximum, ('MultiCarbon_Zero_Flag')] = 4
Calibrations.loc[minimum:maximum, ('Calibration_Flag')] = 0

start_CO_recal_1b = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,9,00)
end_CO_recal_1b = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,13,00)
CO_recal_1b = Calibrations[start_CO_recal_1b:end_CO_recal_1b]
CO_recal_1_mean = CO_recal_1b['CO (ppm)'].mean() 
minimum = min(start_CO_recal_1b,end_CO_recal_1b)
maximum = max(start_CO_recal_1b,end_CO_recal_1b)
Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] = CO_recal_1_mean
Calibrations.loc[minimum:maximum, ('MultiCarbon_Zero_Flag')] = 4
Calibrations.loc[minimum:maximum, ('Calibration_Flag')] = 0

start_CO_recal_1c = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,16,00)
end_CO_recal_1c = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,20,00)
CO_recal_1c = Calibrations[start_CO_recal_1c:end_CO_recal_1c]
CO_recal_1_mean = CO_recal_1c['CO (ppm)'].mean() 
minimum = min(start_CO_recal_1c,end_CO_recal_1c)
maximum = max(start_CO_recal_1c,end_CO_recal_1c)
Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] = CO_recal_1_mean
Calibrations.loc[minimum:maximum, ('MultiCarbon_Zero_Flag')] = 4
Calibrations.loc[minimum:maximum, ('Calibration_Flag')] = 0

start_CO_recal_1d = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,22,00)
end_CO_recal_1d = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,27,00)
CO_recal_1d = Calibrations[start_CO_recal_1d:end_CO_recal_1d]
CO_recal_1_mean = CO_recal_1d['CO (ppm)'].mean() 
minimum = min(start_CO_recal_1d,end_CO_recal_1d)
maximum = max(start_CO_recal_1d,end_CO_recal_1d)
Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] = CO_recal_1_mean
Calibrations.loc[minimum:maximum, ('MultiCarbon_Zero_Flag')] = 4
Calibrations.loc[minimum:maximum, ('Calibration_Flag')] = 0

start_CO_recal_1e = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,33,00)
end_CO_recal_1e = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,10,0,00)
CO_recal_1e = Calibrations[start_CO_recal_1d:end_CO_recal_1d]
CO_recal_1_mean = CO_recal_1e['CO (ppm)'].mean() 
minimum = min(start_CO_recal_1e,end_CO_recal_1e)
maximum = max(start_CO_recal_1e,end_CO_recal_1e)
Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] = CO_recal_1_mean
Calibrations.loc[minimum:maximum, ('MultiCarbon_Zero_Flag')] = 4
Calibrations.loc[minimum:maximum, ('Calibration_Flag')] = 0

minimum = min(start_CO_Cal_1,end_CO_Cal_1,start_MultiCarbonZero_1,end_MultiCarbonZero_1,start_MultiCarbonCal_1,end_MultiCarbonCal_1)
maximum = max(start_CO_Cal_1,end_CO_Cal_1,start_MultiCarbonZero_1,end_MultiCarbonZero_1,start_MultiCarbonCal_1,end_MultiCarbonCal_1)
Calibrations.loc[minimum:maximum, ('CH4_Zero')] = CH4_zero_1_mean
Calibrations.loc[minimum:maximum, ('CH4_LGR_Mean')] = CH4_cal_1_mean
Calibrations.loc[minimum:maximum, ('CO2_Zero')] = CO2_zero_1_mean
Calibrations.loc[minimum:maximum, ('CO2_LGR_Mean')] = CO2_cal_1_mean
Calibrations.loc[minimum:maximum, ('CO_Zero')] = CO_zero_1_mean
#Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] =  0.793
Calibrations.loc[minimum:maximum, ('CH4_calibration_cylinder_ppm')] = 2.058 
Calibrations.loc[minimum:maximum, ('CO2_calibration_cylinder_ppm')] = 411.9 
Calibrations.loc[minimum:maximum, ('CO_calibration_cylinder_ppm')] = 10.67 
Calibrations.loc[minimum:maximum, ('CH4_lit_Zero')] =  0.01
Calibrations.loc[minimum:maximum, ('CH4_lit_Response')] = 0.962
Calibrations.loc[minimum:maximum, ('CO2_lit_Zero')] =  0.76
Calibrations.loc[minimum:maximum, ('CO2_lit_Response')] = 0.984
Calibrations.loc[minimum:maximum, ('CO_lit_Zero')] =  -0.185
Calibrations.loc[minimum:maximum, ('CO_lit_Response')] =  0.793

start_MultiCarbonZero_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,3,00)
end_MultiCarbonZero_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,9,00)
Calibrations.loc[start_MultiCarbonZero_2:end_MultiCarbonZero_2, ('MultiCarbon_Zero_Flag')] = 1
Calibrations.loc[start_MultiCarbonZero_2:end_MultiCarbonZero_2, ('Calibration_Flag')] = 1
MultiCarbonZero_2 = Calibrations[start_MultiCarbonZero_2:end_MultiCarbonZero_2]
CH4_zero_2_mean = MultiCarbonZero_2['CH4 (ppm)'].mean() 
CO2_zero_2_mean = MultiCarbonZero_2['CO2 (ppm)'].mean() 
CO_zero_2_mean = MultiCarbonZero_2['CO (ppm)'].mean() 

start_MultiCarbonCal_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,15,00)
end_MultiCarbonCal_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,30,00)
Calibrations.loc[start_MultiCarbonCal_2:end_MultiCarbonCal_2, ('CH4_calibration_cylinder_ppm')] = 2.058
Calibrations.loc[start_MultiCarbonCal_2:end_MultiCarbonCal_2, ('CO2_calibration_cylinder_ppm')] = 411.9
Calibrations.loc[start_MultiCarbonCal_2:end_MultiCarbonCal_2, ('CO_calibration_cylinder_ppm')] = 10.67
Calibrations.loc[start_MultiCarbonCal_2:end_MultiCarbonCal_2, ('MultiCarbon_calibration_Flag')] = 1
Calibrations.loc[start_MultiCarbonCal_2:end_MultiCarbonCal_2, ('Calibration_Flag')] = 1
MultiCarbonCal_2 = Calibrations[start_MultiCarbonCal_2:end_MultiCarbonCal_2]
MultiCarbonCal_2['MultiCarbon_Zero_Flag'] = 1 
MultiCarbonCal_2['Calibration_Flag'] = 1 
CH4_cal_2_mean = MultiCarbonCal_2['CH4 (ppm)'].mean() 
CO2_cal_2_mean = MultiCarbonCal_2['CO2 (ppm)'].mean() 
CO_cal_2_mean = MultiCarbonCal_2['CO (ppm)'].mean() 

start_CO_recal_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,12,10,00)
end_CO_recal_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,13,0,00)
Calibrations.loc[start_CO_recal_2:end_CO_recal_2, ('CH4_calibration_cylinder_ppm')] = 2.058
Calibrations.loc[start_CO_recal_2:end_CO_recal_2, ('CO2_calibration_cylinder_ppm')] = 411.9
Calibrations.loc[start_CO_recal_2:end_CO_recal_2, ('CO_calibration_cylinder_ppm')] = 10.67
Calibrations.loc[start_CO_recal_2:end_CO_recal_2, ('MultiCarbon_calibration_Flag')] = 4
Calibrations.loc[start_CO_recal_2:end_CO_recal_2, ('Calibration_Flag')] = 0
CO_recal_2 = Calibrations[start_CO_recal_2:start_CO_recal_2]
CO_recal_2_mean = CO_recal_2['CO (ppm)'].mean()

#MultiCarbonZero_2 = pd.concat([MultiCarbonZero_2a, MultiCarbonZero_2b])

#CH4_zero_2_mean = MultiCarbonZero_3['CH4 (ppm)'].mean() 
#CO2_zero_2_mean = MultiCarbonZero_3['CO2 (ppm)'].mean() 
#CO_zero_2_mean = MultiCarbonZero_3['CO (ppm)'].mean() 

minimum = min(start_CO_recal_2,end_CO_recal_2,start_MultiCarbonZero_2,end_MultiCarbonZero_2,start_MultiCarbonCal_2,end_MultiCarbonCal_2)
maximum = max(start_CO_recal_2,end_CO_recal_2,start_MultiCarbonZero_2,end_MultiCarbonZero_2,start_MultiCarbonCal_2,end_MultiCarbonCal_2)
Calibrations.loc[minimum:maximum, ('CH4_Zero')] = CH4_zero_2_mean
Calibrations.loc[minimum:maximum, ('CH4_LGR_Mean')] = CH4_cal_2_mean
Calibrations.loc[minimum:maximum, ('CO2_Zero')] = CO2_zero_2_mean
Calibrations.loc[minimum:maximum, ('CO2_LGR_Mean')] = CO2_cal_2_mean
Calibrations.loc[minimum:maximum, ('CO_Zero')] = CO_zero_2_mean
Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] = CO_cal_2_mean
Calibrations.loc[minimum:maximum, ('CH4_calibration_cylinder_ppm')] = 2.058 
Calibrations.loc[minimum:maximum, ('CO2_calibration_cylinder_ppm')] = 411.9 
Calibrations.loc[minimum:maximum, ('CO_calibration_cylinder_ppm')] = 10.67 
Calibrations.loc[minimum:maximum, ('CH4_lit_Zero')] =  0.01
Calibrations.loc[minimum:maximum, ('CH4_lit_Response')] = 0.962
Calibrations.loc[minimum:maximum, ('CO2_lit_Zero')] =  1.25
Calibrations.loc[minimum:maximum, ('CO2_lit_Response')] = 0.984
Calibrations.loc[minimum:maximum, ('CO_lit_Zero')] =  -0.15
Calibrations.loc[minimum:maximum, ('CO_lit_Response')] =  0.802

start_MultiCarbonCal_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,42,00) #08:28-08:41
end_MultiCarbonCal_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,50,00)
Calibrations.loc[start_MultiCarbonCal_3:end_MultiCarbonCal_3, ('CH4_calibration_cylinder_ppm')] = 1.8123 
Calibrations.loc[start_MultiCarbonCal_3:end_MultiCarbonCal_3, ('CO2_calibration_cylinder_ppm')] = 400.01 
Calibrations.loc[start_MultiCarbonCal_3:end_MultiCarbonCal_3, ('MultiCarbon_calibration_Flag')] = 2
Calibrations.loc[start_MultiCarbonCal_3:end_MultiCarbonCal_3, ('Calibration_Flag')] = 1
MultiCarbonCal_3 = Calibrations[start_MultiCarbonCal_3:end_MultiCarbonCal_3]
MultiCarbonCal_3['MultiCarbon_Zero_Flag'] = 1 
MultiCarbonCal_3['Calibration_Flag'] = 1 
CH4_cal_3_mean = MultiCarbonCal_3['CH4 (ppm)'].mean() 
CO2_cal_3_mean = MultiCarbonCal_3['CO2 (ppm)'].mean() 
#CO_cal_3_mean = MultiCarbonCal_3['CO (ppm)'].mean() 

start_MultiCarbonZero_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,56,00)
end_MultiCarbonZero_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,1,00)
Calibrations.loc[start_MultiCarbonZero_3a:end_MultiCarbonZero_3a, ('MultiCarbon_Zero_Flag')] = 1
Calibrations.loc[start_MultiCarbonZero_3a:end_MultiCarbonZero_3a, ('Calibration_Flag')] = 1
MultiCarbonZero_3a = Calibrations[start_MultiCarbonZero_3a:end_MultiCarbonZero_3a]

start_MultiCarbonZero_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,12,00)
end_MultiCarbonZero_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,14,00)
Calibrations.loc[start_MultiCarbonZero_3b:end_MultiCarbonZero_3b, ('MultiCarbon_Zero_Flag')] = 1
Calibrations.loc[start_MultiCarbonZero_3b:end_MultiCarbonZero_3b, ('Calibration_Flag')] = 1
MultiCarbonZero_3b = Calibrations[start_MultiCarbonZero_3b:end_MultiCarbonZero_3b]

start_MultiCarbonZero_3c = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,40,00)
end_MultiCarbonZero_3c = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,48,00)
Calibrations.loc[start_MultiCarbonZero_3b:end_MultiCarbonZero_3b, ('MultiCarbon_Zero_Flag')] = 1
Calibrations.loc[start_MultiCarbonZero_3b:end_MultiCarbonZero_3b, ('Calibration_Flag')] = 1
MultiCarbonZero_3c = Calibrations[start_MultiCarbonZero_3c:end_MultiCarbonZero_3c]

MultiCarbonZero_3 = pd.concat([MultiCarbonZero_3a, MultiCarbonZero_3b])

CH4_zero_3_mean = MultiCarbonZero_3['CH4 (ppm)'].mean() 
CO2_zero_3_mean = MultiCarbonZero_3['CO2 (ppm)'].mean() 
#CO_zero_3_mean = MultiCarbonZero_3['CO (ppm)'].mean() 

MultiCarbonZero_3a = MultiCarbonZero_3a.groupby(pd.Grouper(freq=zero_av_Freq)).mean() 
CO_zero_3_mean = MultiCarbonZero_3a['CO (ppm)'].min() 

minimum = min(start_MultiCarbonZero_3a,end_MultiCarbonZero_3a,start_MultiCarbonZero_3b,end_MultiCarbonZero_3b,start_MultiCarbonCal_3,end_MultiCarbonCal_3)
maximum = max(start_MultiCarbonZero_3a,end_MultiCarbonZero_3a,start_MultiCarbonZero_3b,end_MultiCarbonZero_3b,start_MultiCarbonCal_3,end_MultiCarbonCal_3)
Calibrations.loc[minimum:maximum, ('CH4_Zero')] = CH4_zero_3_mean
Calibrations.loc[minimum:maximum, ('CH4_LGR_Mean')] = CH4_cal_3_mean
Calibrations.loc[minimum:maximum, ('CO2_Zero')] = CO2_zero_3_mean
Calibrations.loc[minimum:maximum, ('CO2_LGR_Mean')] = CO2_cal_3_mean
Calibrations.loc[minimum:maximum, ('CO_Zero')] = CO_zero_3_mean
#Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] = CO_cal_3_mean
Calibrations.loc[minimum:maximum, ('CH4_calibration_cylinder_ppm')] = 1.8123 
Calibrations.loc[minimum:maximum, ('CO2_calibration_cylinder_ppm')] = 400.08 
Calibrations.loc[minimum:maximum, ('CH4_lit_Zero')] =  0
Calibrations.loc[minimum:maximum, ('CH4_lit_Response')] = 0.962
Calibrations.loc[minimum:maximum, ('CO2_lit_Zero')] =  0.86
Calibrations.loc[minimum:maximum, ('CO2_lit_Response')] = 0.984
Calibrations.loc[minimum:maximum, ('CO_lit_Zero')] =  -0.15
#Calibrations.loc[minimum:maximum, ('CO_lit_Response')] =  0.802

start_MultiCarbonCal_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,23,00)
end_MultiCarbonCal_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,26,00)
Calibrations.loc[start_MultiCarbonCal_4:end_MultiCarbonCal_4, ('MultiCarbon_calibration_Flag')] = 2
Calibrations.loc[start_MultiCarbonCal_4:end_MultiCarbonCal_4, ('Calibration_Flag')] = 1
MultiCarbonCal_4 = Calibrations[start_MultiCarbonCal_4:end_MultiCarbonCal_4]
MultiCarbonCal_4['MultiCarbon_Zero_Flag'] = 1 
MultiCarbonCal_4['Calibration_Flag'] = 1 
CH4_cal_4_mean = MultiCarbonCal_4['CH4 (ppm)'].mean() 
CO2_cal_4_mean = MultiCarbonCal_4['CO2 (ppm)'].mean() 
#CO_cal_4_mean = MultiCarbonCal_4['CO (ppm)'].mean() 

start_MultiCarbonZero_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,10,00)
end_MultiCarbonZero_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,15,00)
Calibrations.loc[start_MultiCarbonZero_4:end_MultiCarbonZero_4, ('MultiCarbon_Zero_Flag')] = 1
Calibrations.loc[start_MultiCarbonZero_4:end_MultiCarbonZero_4, ('Calibration_Flag')] = 1
MultiCarbonZero_4 = Calibrations[start_MultiCarbonZero_4:end_MultiCarbonZero_4]
CH4_zero_4_mean = MultiCarbonZero_4['CH4 (ppm)'].mean() 
CO2_zero_4_mean = MultiCarbonZero_4['CO2 (ppm)'].mean() 
CO_zero_4_mean = MultiCarbonZero_4['CO (ppm)'].mean() 

#MultiCarbonZero_4 = MultiCarbonZero_4.groupby(pd.Grouper(freq=av_Freq)).mean() 
#CO_zero_4_mean = MultiCarbonZero_4['CO (ppm)'].min() 

start_CO_Zero_4a = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,21,00)
end_CO_Zero_4a = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,26,59)
Calibrations.loc[start_CO_Zero_4a:end_CO_Zero_4a, ('Calibration_Flag')] = 1
CO_Zero_4a = Calibrations[start_CO_Zero_4a:end_CO_Zero_4a]
#CO_zero_4_mean = CO_Zero_4a['CO (ppm)'].mean() 

start_CO_Zero_4b = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,0,00)
end_CO_Zero_4b = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,15,00)
Calibrations.loc[start_CO_Zero_4b:end_CO_Zero_4b, ('Calibration_Flag')] = 1
CO_Zero_4b = Calibrations[start_CO_Zero_4b:end_CO_Zero_4b]
#CO_zero_4_mean = CO_Zero_4b['CO (ppm)'].mean() 

start_CO_Cal_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,10,2,00)
end_CO_Cal_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,10,2,59)
#CO_Cal_4 = Calibrations[start_CO_Cal_4:end_CO_Cal_4]
#CO_cal_4_mean = CO_Cal_4['CO (ppm)'].mean() 
#minimum = min(start_CO_Cal_4,end_CO_Cal_4)
#maximum = max(start_CO_Cal_4,end_CO_Cal_4)
#Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] = CO_cal_4_mean
#Calibrations.loc[minimum:maximum, ('MultiCarbon_Zero_Flag')] = 4
#Calibrations.loc[minimum:maximum, ('Calibration_Flag')] = 1

minimum = min(start_CO_Cal_4,end_CO_Cal_4,start_MultiCarbonZero_4,end_MultiCarbonZero_4,start_MultiCarbonCal_4,end_MultiCarbonCal_4)
maximum = max(start_CO_Cal_4,end_CO_Cal_4,start_MultiCarbonZero_4,end_MultiCarbonZero_4,start_MultiCarbonCal_4,end_MultiCarbonCal_4)
Calibrations.loc[minimum:maximum, ('CH4_Zero')] = CH4_zero_4_mean
Calibrations.loc[minimum:maximum, ('CH4_LGR_Mean')] = CH4_cal_4_mean
Calibrations.loc[minimum:maximum, ('CO2_Zero')] = CO2_zero_4_mean
Calibrations.loc[minimum:maximum, ('CO2_LGR_Mean')] = CO2_cal_4_mean
Calibrations.loc[minimum:maximum, ('CO_Zero')] = CO_zero_4_mean
#Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] = CO_cal_4_mean
Calibrations.loc[minimum:maximum, ('CH4_calibration_cylinder_ppm')] = 1.8123 
Calibrations.loc[minimum:maximum, ('CO2_calibration_cylinder_ppm')] = 400.08 
#Calibrations.loc[minimum:maximum, ('CO_calibration_cylinder_ppm')] = 10.9 
Calibrations.loc[minimum:maximum, ('CH4_lit_Zero')] =  0
Calibrations.loc[minimum:maximum, ('CH4_lit_Response')] = 0.974
Calibrations.loc[minimum:maximum, ('CO2_lit_Zero')] =  0.86
Calibrations.loc[minimum:maximum, ('CO2_lit_Response')] = 0.975
Calibrations.loc[minimum:maximum, ('CO_lit_Zero')] =  -0.15
#Calibrations.loc[minimum:maximum, ('CO_lit_Response')] =  0.802

start_AmmoniaZero_1a = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day1_AmmoniaZero_1_1,16,0,00) 
end_AmmoniaZero_1a = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,7,38,00)
Calibrations.loc[start_AmmoniaZero_1a:end_AmmoniaZero_1a, ('NH3_Zero_Flag')] = 1
Calibrations.loc[start_AmmoniaZero_1a:end_AmmoniaZero_1a, ('Calibration_Flag')] = 1
AmmoniaZero_1a = Calibrations[start_AmmoniaZero_1a:end_AmmoniaZero_1a]
NH3_zero_1a_mean = AmmoniaZero_1a['NH3 (ppm)'].mean() 
minimum = min(start_AmmoniaZero_1a,end_AmmoniaZero_1a)
maximum = max(start_AmmoniaZero_1a,end_AmmoniaZero_1a)
Calibrations.loc[minimum:maximum, ('NH3_Zero')] = NH3_zero_1a_mean

ZeroAmmonia_1a = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day1_AmmoniaZero_1_1,16,0,00) 
ZeroAmmonia_1b = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day1_AmmoniaZero_1_1,16,45,00)
ZeroAmmonia_1c = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,0,0,00)
ZeroAmmonia_1d = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,7,38,00) 
Calibrations.loc[ZeroAmmonia_1a:ZeroAmmonia_1b, ('NH3_lit_Zero')] = 0.09/1000
Calibrations.loc[ZeroAmmonia_1b:ZeroAmmonia_1c, ('NH3_lit_Zero')] = 0.1/1000
Calibrations.loc[ZeroAmmonia_1c:ZeroAmmonia_1d, ('NH3_lit_Zero')] = 0.25/1000

#ZeroAmmonia_1d = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,16,25,00)
#AmmoniaZero_1a.loc[ZeroAmmonia_1d, ('CH4_lit_Zero')] = 0.57

start_AmmoniaZero_1b = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,8,15,00) 
end_AmmoniaZero_1b = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,9,3,00)
Calibrations.loc[start_AmmoniaZero_1b:end_AmmoniaZero_1b, ('NH3_Zero_Flag')] = 1
Calibrations.loc[start_AmmoniaZero_1b:end_AmmoniaZero_1b, ('Calibration_Flag')] = 1
AmmoniaZero_1b = Calibrations[start_AmmoniaZero_1b:end_AmmoniaZero_1b]
NH3_zero_1b_mean = AmmoniaZero_1b['NH3 (ppm)'].mean() 
minimum = min(start_AmmoniaZero_1b,end_AmmoniaZero_1b)
maximum = max(start_AmmoniaZero_1b,end_AmmoniaZero_1b)
Calibrations.loc[minimum:maximum, ('NH3_Zero')] = NH3_zero_1b_mean
Calibrations.loc[minimum:maximum, ('NH3_lit_Zero')] = 0.57/1000 

start_AmmoniaZero_1c = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,9,14,00) 
end_AmmoniaZero_1c = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,9,26,00)
Calibrations.loc[start_AmmoniaZero_1c:end_AmmoniaZero_1c, ('NH3_Zero_Flag')] = 1
Calibrations.loc[start_AmmoniaZero_1c:end_AmmoniaZero_1c, ('Calibration_Flag')] = 1
AmmoniaZero_1c = Calibrations[start_AmmoniaZero_1c:end_AmmoniaZero_1c]
NH3_zero_1c_mean = AmmoniaZero_1c['NH3 (ppm)'].mean() 
minimum = min(start_AmmoniaZero_1c,end_AmmoniaZero_1c)
maximum = max(start_AmmoniaZero_1c,end_AmmoniaZero_1c)
Calibrations.loc[minimum:maximum, ('NH3_Zero')] = NH3_zero_1c_mean
Calibrations.loc[minimum:maximum, ('NH3_lit_Zero')] = 0.2/1000 

start_AmmoniaZero_1d = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,9,30,00) 
end_AmmoniaZero_1d = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,9,44,00)
Calibrations.loc[start_AmmoniaZero_1d:end_AmmoniaZero_1d, ('NH3_Zero_Flag')] = 1
Calibrations.loc[start_AmmoniaZero_1d:end_AmmoniaZero_1d, ('Calibration_Flag')] = 1
AmmoniaZero_1d = Calibrations[start_AmmoniaZero_1d:end_AmmoniaZero_1d]
NH3_zero_1d_mean = AmmoniaZero_1d['NH3 (ppm)'].mean() 
minimum = min(start_AmmoniaZero_1d,end_AmmoniaZero_1d)
maximum = max(start_AmmoniaZero_1d,end_AmmoniaZero_1d)
Calibrations.loc[minimum:maximum, ('NH3_Zero')] = NH3_zero_1d_mean
Calibrations.loc[minimum:maximum, ('NH3_lit_Zero')] = 0.2/1000 

start_AmmoniaZero_1e = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,11,54,00) 
end_AmmoniaZero_1e = datetime.datetime(year_AmmoniaZero_1_1,month_AmmoniaZero_1_1,day2_AmmoniaZero_1_1,12,37,00)
Calibrations.loc[start_AmmoniaZero_1e:end_AmmoniaZero_1e, ('NH3_Zero_Flag')] = 1
Calibrations.loc[start_AmmoniaZero_1e:end_AmmoniaZero_1e, ('Calibration_Flag')] = 1
AmmoniaZero_1e = Calibrations[start_AmmoniaZero_1e:end_AmmoniaZero_1e]
NH3_zero_1e_mean = AmmoniaZero_1e['NH3 (ppm)'].mean() 
minimum = min(start_AmmoniaZero_1e,end_AmmoniaZero_1e)
maximum = max(start_AmmoniaZero_1e,end_AmmoniaZero_1e)
Calibrations.loc[minimum:maximum, ('NH3_Zero')] = NH3_zero_1e_mean
Calibrations.loc[minimum:maximum, ('NH3_lit_Zero')] = 0.36/1000 

start_AmmoniaZero_1_2 = datetime.datetime(year_AmmoniaZero_1_2,month_AmmoniaZero_1_2,day1_AmmoniaZero_1_2,12,29,00) 
end_AmmoniaZero_1_2 = datetime.datetime(year_AmmoniaZero_1_2,month_AmmoniaZero_1_2,day2_AmmoniaZero_1_2,12,58,00)
Calibrations.loc[start_AmmoniaZero_1_2:end_AmmoniaZero_1_2, ('NH3_Zero_Flag')] = 1
Calibrations.loc[start_AmmoniaZero_1_2:end_AmmoniaZero_1_2, ('Calibration_Flag')] = 1
AmmoniaZero_2 = Calibrations[start_AmmoniaZero_1_2:end_AmmoniaZero_1_2]
NH3_zero_2_mean = AmmoniaZero_2['NH3 (ppm)'].mean() 
minimum = min(start_AmmoniaZero_1_2,end_AmmoniaZero_1_2)
maximum = max(start_AmmoniaZero_1_2,end_AmmoniaZero_1_2)
Calibrations.loc[minimum:maximum, ('NH3_Zero')] = NH3_zero_2_mean

start_MultiCarbonZero_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,10,21,00)
end_MultiCarbonZero_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,10,25,00)
Calibrations.loc[start_MultiCarbonZero_5:end_MultiCarbonZero_5, ('MultiCarbon_Zero_Flag')] = 1
Calibrations.loc[start_MultiCarbonZero_5:end_MultiCarbonZero_5, ('Calibration_Flag')] = 1
MultiCarbonZero_5 = Calibrations[start_MultiCarbonZero_5:end_MultiCarbonZero_5]
MultiCarbonZero_5['MultiCarbon_Zero_Flag'] = 1 
MultiCarbonZero_5['Calibration_Flag'] = 1 
CH4_zero_5_mean = MultiCarbonZero_5['CH4 (ppm)'].mean() 
CO2_zero_5_mean = MultiCarbonZero_5['CO2 (ppm)'].mean() 
#CO_zero_5_mean = MultiCarbonZero_5['CO (ppm)'].mean() 

start_CO_Zero_5a = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,9,44,00)
end_CO_Zero_5a = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,9,48,00)
Calibrations.loc[start_CO_Zero_5a:end_CO_Zero_5a, ('Calibration_Flag')] = 1
CO_Zero_5a = Calibrations[start_CO_Zero_5a:end_CO_Zero_5a]
#CO_zero_5_mean = CO_Zero_5a['CO (ppm)'].mean() 

start_CO_Zero_5b = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,10,20,00)
end_CO_Zero_5b = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,10,26,00)
Calibrations.loc[start_CO_Zero_5b:end_CO_Zero_5b, ('Calibration_Flag')] = 1
CO_Zero_5b = Calibrations[start_CO_Zero_5b:end_CO_Zero_5b]
#CO_zero_5_mean = CO_Zero_5b['CO (ppm)'].mean() 

CO_Zero_5b = CO_Zero_5b.groupby(pd.Grouper(freq=zero_av_Freq)).mean() 
CO_zero_5_mean = CO_Zero_5b['CO (ppm)'].min() 

start_MultiCarbonCal_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,9,45,00)
end_MultiCarbonCal_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,9,47,00)
Calibrations.loc[start_MultiCarbonCal_5:end_MultiCarbonCal_5, ('CH4_calibration_cylinder_ppm')] = 1.8123 
Calibrations.loc[start_MultiCarbonCal_5:end_MultiCarbonCal_5, ('CO2_calibration_cylinder_ppm')] = 400.08 
Calibrations.loc[start_MultiCarbonCal_5:end_MultiCarbonCal_5, ('MultiCarbon_calibration_Flag')] = 2
Calibrations.loc[start_MultiCarbonCal_5:end_MultiCarbonCal_5, ('Calibration_Flag')] = 1
MultiCarbonCal_5 = Calibrations[start_MultiCarbonCal_5:end_MultiCarbonCal_5]
MultiCarbonCal_5['MultiCarbon_calibration_Flag'] = 1 
MultiCarbonCal_5['Calibration_Flag'] = 1 
CH4_cal_5_mean = MultiCarbonCal_5['CH4 (ppm)'].mean() 
CO2_cal_5_mean = MultiCarbonCal_5['CO2 (ppm)'].mean() 
#CO_cal_5_mean = MultiCarbonCal_5['CO (ppm)'].mean() 

minimum = min(start_MultiCarbonZero_5,end_MultiCarbonZero_5,start_MultiCarbonCal_5,end_MultiCarbonCal_5)
maximum = max(start_MultiCarbonZero_5,end_MultiCarbonZero_5,start_MultiCarbonCal_5,end_MultiCarbonCal_5)
Calibrations.loc[minimum:maximum, ('CH4_Zero')] = CH4_zero_5_mean
Calibrations.loc[minimum:maximum, ('CH4_LGR_Mean')] = CH4_cal_5_mean
Calibrations.loc[minimum:maximum, ('CO2_Zero')] = CO2_zero_5_mean
Calibrations.loc[minimum:maximum, ('CO2_LGR_Mean')] = CO2_cal_5_mean
Calibrations.loc[minimum:maximum, ('CO_Zero')] = CO_zero_5_mean
#Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] = CO_cal_5_mean
Calibrations.loc[minimum:maximum, ('CH4_calibration_cylinder_ppm')] = 1.8123 
Calibrations.loc[minimum:maximum, ('CO2_calibration_cylinder_ppm')] = 400.08
Calibrations.loc[minimum:maximum, ('CH4_lit_Zero')] =  0
Calibrations.loc[minimum:maximum, ('CH4_lit_Response')] = 0.971
Calibrations.loc[minimum:maximum, ('CO2_lit_Zero')] =  0.86
Calibrations.loc[minimum:maximum, ('CO2_lit_Response')] = 0.969
Calibrations.loc[minimum:maximum, ('CO_lit_Zero')] =  -0.15
#Calibrations.loc[minimum:maximum, ('CO_lit_Response')] =  0.802

start_Audit_Day_6 = datetime.datetime(year_Audit_6,month_Audit_6,day1_Audit_6,0,0,00)
end_Audit_Day_6 = datetime.datetime(year_Audit_6,month_Audit_6,day2_Audit_6,23,59,00)

start_MultiCarbonZero_6 = datetime.datetime(year_Audit_6,month_Audit_6,day1_Audit_6,9,31,00)
end_MultiCarbonZero_6 = datetime.datetime(year_Audit_6,month_Audit_6,day1_Audit_6,9,38,00)
Calibrations.loc[start_MultiCarbonZero_6:end_MultiCarbonZero_6, ('MultiCarbon_Zero_Flag')] = 1
Calibrations.loc[start_MultiCarbonZero_6:end_MultiCarbonZero_6, ('Calibration_Flag')] = 1
MultiCarbonZero_6 = Calibrations[start_MultiCarbonZero_6:end_MultiCarbonZero_6]
MultiCarbonZero_6['MultiCarbon_Zero_Flag'] = 1 
MultiCarbonZero_6['Calibration_Flag'] = 1 
CH4_zero_6_mean = MultiCarbonZero_6['CH4 (ppm)'].mean() 
MultiCarbonZero_6 = MultiCarbonZero_6.groupby(pd.Grouper(freq=av_Freq)).mean() 
CO2_zero_6_mean = MultiCarbonZero_6['CO2 (ppm)'].min() 
CO_zero_6_mean = MultiCarbonZero_6['CO (ppm)'].min()

start_MultiCarbonCal_6 = datetime.datetime(year_Audit_6,month_Audit_6,day1_Audit_6,9,45,00)
end_MultiCarbonCal_6 = datetime.datetime(year_Audit_6,month_Audit_6,day1_Audit_6,9,52,00)
Calibrations.loc[start_MultiCarbonCal_6:end_MultiCarbonCal_6, ('CH4_calibration_cylinder_ppm')] = 1.81 
Calibrations.loc[start_MultiCarbonCal_6:end_MultiCarbonCal_6, ('CO2_calibration_cylinder_ppm')] = 400.08 
Calibrations.loc[start_MultiCarbonCal_6:end_MultiCarbonCal_6, ('MultiCarbon_calibration_Flag')] = 2
Calibrations.loc[start_MultiCarbonCal_6:end_MultiCarbonCal_6, ('Calibration_Flag')] = 1
MultiCarbonCal_6 = Calibrations[start_MultiCarbonCal_6:end_MultiCarbonCal_6]
MultiCarbonCal_6['MultiCarbon_calibration_Flag'] = 1 
MultiCarbonCal_6['Calibration_Flag'] = 1 
CH4_cal_6_mean = MultiCarbonCal_6['CH4 (ppm)'].mean() 
MultiCarbonCal_6 = MultiCarbonCal_6.groupby(pd.Grouper(freq=av_Freq)).mean() 
CO2_cal_6_mean = MultiCarbonCal_6['CO2 (ppm)'].min() 
#CO_cal_6_mean = MultiCarbonCal_6['CO (ppm)'].mean() 

minimum = min(start_MultiCarbonZero_6,end_MultiCarbonZero_6,start_MultiCarbonCal_6,end_MultiCarbonCal_6)
maximum = max(start_MultiCarbonZero_6,end_MultiCarbonZero_6,start_MultiCarbonCal_6,end_MultiCarbonCal_6)
Calibrations.loc[minimum:maximum, ('CH4_Zero')] = CH4_zero_6_mean
Calibrations.loc[minimum:maximum, ('CH4_LGR_Mean')] = CH4_cal_6_mean
Calibrations.loc[minimum:maximum, ('CO2_Zero')] = CO2_zero_6_mean
Calibrations.loc[minimum:maximum, ('CO2_LGR_Mean')] = CO2_cal_6_mean
Calibrations.loc[minimum:maximum, ('CO_Zero')] = CO_zero_6_mean
#Calibrations.loc[minimum:maximum, ('CO_LGR_Mean')] = CO_cal_6_mean
Calibrations.loc[minimum:maximum, ('CH4_calibration_cylinder_ppm')] = 1.81
Calibrations.loc[minimum:maximum, ('CO2_calibration_cylinder_ppm')] = 400.08
Calibrations.loc[minimum:maximum, ('CH4_lit_Zero')] =  0.014
Calibrations.loc[minimum:maximum, ('CH4_lit_Response')] = 0.975
Calibrations.loc[minimum:maximum, ('CO2_lit_Zero')] =  0.76
Calibrations.loc[minimum:maximum, ('CO2_lit_Response')] = 0.969
Calibrations.loc[minimum:maximum, ('CO_lit_Zero')] =  -0.2
#Calibrations.loc[minimum:maximum, ('CO_lit_Response')] =  0.802

start_AmmoniaZero_3 = datetime.datetime(year_Audit_6,month_Audit_6,day1_Audit_6,13,35,00) 
end_AmmoniaZero_3 = datetime.datetime(year_Audit_6,month_Audit_6,day2_Audit_6,9,30,00)
Calibrations.loc[start_AmmoniaZero_3:end_AmmoniaZero_3, ('NH3_Zero_Flag')] = 1
Calibrations.loc[start_AmmoniaZero_3:end_AmmoniaZero_3, ('Calibration_Flag')] = 1
AmmoniaZero_3 = Calibrations[start_AmmoniaZero_3:end_AmmoniaZero_3]
NH3_zero_3_mean = AmmoniaZero_3['NH3 (ppm)'].mean() 
minimum = min(start_AmmoniaZero_3,end_AmmoniaZero_3) 
maximum = max(start_AmmoniaZero_3,end_AmmoniaZero_3)
Calibrations.loc[minimum:maximum, ('NH3_Zero')] = NH3_zero_3_mean
Calibrations.loc[minimum:maximum, ('NH3_lit_Zero')] = 0.4/1000

First_Calibration_start = min(start_CO_Cal_1,end_CO_Cal_1,start_MultiCarbonZero_1,end_MultiCarbonZero_1,start_MultiCarbonCal_1,end_MultiCarbonCal_1)
Final_Calibration_end = maximum

Calibrations.drop(Calibrations[(Calibrations['Calibration_Flag'] == 0)].index,inplace =True)

Calibrations = Calibrations.drop(columns=['Calibration_Flag'])

#Cal_check = Calibrations

#Cal_check.to_csv(str(Data_Output_Folder) + 'LGR_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

#Calibrations = Calibrations.drop(columns=['min_CH4 (ppm)', 'max_CH4 (ppm)', 'min_CO2 (ppm)','max_CO2 (ppm)','min_CO (ppm)','max_CO (ppm)', 'min_NH3 (ppm)','max_NH3 (ppm)'])

#CO2 & CH4 Multicarbon Calibrations: 0 = normal operations, 1 means testing the zero, 2 means CO & CO2 & CH4 calibration, 3 means CO2 & CH4 calibrations only
#MultiCarbon_calibration_Flag: 0 = normal operations, 1 means CO & CO2 & CH4 calibration, 2 means CO2 & CH4 calibration only, 3 means CO calibration only, 4 means CO realignment
#Ammonia Calibration: 0 means normal operations, 1 means testing the zero, 2 means NH3 calibration

Original_Calibrations = Calibrations

Cal_av_Freq = '1min'

Calibrations = Calibrations.groupby(pd.Grouper(freq=Cal_av_Freq)).mean()

Calibrations['NH3_Response'] = np.nan
Calibrations['NH3_Response'] = np.where((Calibrations['CH4_Zero'].notna()), 1, 0)
Calibrations['NH3_Response'] = np.where((Calibrations['NH3_Zero'].notna()), 1, Calibrations['NH3_Response'])

Calibrations.drop(Calibrations[(Calibrations['NH3_Response'] == 0)].index,inplace =True)

Calibrations['CH4_Response'] = (Calibrations['CH4_calibration_cylinder_ppm'] + Calibrations['CH4_Zero'])/Calibrations['CH4_LGR_Mean']
Calibrations['CO2_Response'] = (Calibrations['CO2_calibration_cylinder_ppm'] + Calibrations['CO2_Zero'])/Calibrations['CO2_LGR_Mean'] 
Calibrations['CO_Response'] = (Calibrations['CO_calibration_cylinder_ppm'] + Calibrations['CO_Zero'])/(Calibrations['CO_LGR_Mean'])

Calibrations['CH4_Slope'] = Calibrations['CH4_calibration_cylinder_ppm']/(Calibrations['CH4_LGR_Mean'] - Calibrations['CH4_Zero'])
Calibrations['CO2_Slope'] = Calibrations['CO2_calibration_cylinder_ppm']/(Calibrations['CO2_LGR_Mean'] - Calibrations['CO2_Zero'])
Calibrations['CO_Slope'] = Calibrations['CO_calibration_cylinder_ppm']/(Calibrations['CO_LGR_Mean'] - Calibrations['CO_Zero'])
Calibrations['NH3_Slope'] = 1

minimum = min(start_CO_recal_2,end_CO_recal_2,start_MultiCarbonZero_2,end_MultiCarbonZero_2,start_MultiCarbonCal_2,end_MultiCarbonCal_2)
maximum = max(start_CO_recal_2,end_CO_recal_2,start_MultiCarbonZero_2,end_MultiCarbonZero_2,start_MultiCarbonCal_2,end_MultiCarbonCal_2)
MultiCarbon_Audit_2 = Calibrations[minimum:maximum]
CH4_early_Response = MultiCarbon_Audit_2['CH4_Response'].mean()
CO2_early_Response = MultiCarbon_Audit_2['CO2_Response'].mean()
CO_early_Response = MultiCarbon_Audit_2['CO_Response'].mean()
CH4_early_Slope = MultiCarbon_Audit_2['CH4_Slope'].mean()
CO2_early_Slope = MultiCarbon_Audit_2['CO2_Slope'].mean()
CO_early_Slope = MultiCarbon_Audit_2['CO_Slope'].mean()

First_Calibration_end = max(start_CO_Cal_1,end_CO_Cal_1,start_MultiCarbonZero_1,end_MultiCarbonZero_1,start_MultiCarbonCal_1,end_MultiCarbonCal_1)
MultiCarbon_Audit_1 = Calibrations[First_Calibration_start:First_Calibration_end]
CO_early_cylinder = 0.793 * MultiCarbon_Audit_1['CO_LGR_Mean'].mean() - MultiCarbon_Audit_1['CO_Zero'].mean()
Calibrations.loc[First_Calibration_start:First_Calibration_end, ('CO_calibration_cylinder_ppm')] = CO_early_cylinder
Calibrations.loc[First_Calibration_start:First_Calibration_end, ('CH4_Response')] = CH4_early_Response
Calibrations.loc[First_Calibration_start:First_Calibration_end, ('CO2_Response')] = CO2_early_Response
Calibrations.loc[First_Calibration_start:First_Calibration_end, ('CO_Response')] = 0.793
Calibrations.loc[First_Calibration_start:First_Calibration_end, ('CH4_Slope')] = CH4_early_Slope
Calibrations.loc[First_Calibration_start:First_Calibration_end, ('CO2_Slope')] = CO2_early_Slope
Calibrations.loc[First_Calibration_start:First_Calibration_end, ('CO_Slope')] = 0.793

Calibrations.loc[start_MultiCarbonCal_3:Final_Calibration_end, ('CO_Response')] = CO_early_Response
Calibrations.loc[start_MultiCarbonCal_3:Final_Calibration_end, ('CO_Slope')] = CO_early_Slope

Calibrations['CH4_Intercept'] = 0 - Calibrations['CH4_Slope']*Calibrations['CH4_Zero']
Calibrations['CO2_Intercept'] = 0 - Calibrations['CO2_Slope']*Calibrations['CO2_Zero']
Calibrations['CO_Intercept'] = 0 - Calibrations['CO_Slope']*Calibrations['CO_Zero']
Calibrations['NH3_Intercept'] = 0 - Calibrations['NH3_Slope']*Calibrations['NH3_Zero']

#y(TrueValue) = m(ResponseValue) * x(RawValue) + c (zero value)
#c (zero value) equals the value of y when x =0 
#c (zero value) = 0 - m(ResponseValue) * x(RawValue)

#m (response value) equals the value of y when x =0 
# m(response value) = y(TrueValue) - c (zero value)/x(RawValue)

#LGR_Cals = Calibrations[['CH4_Zero', 'CH4_Response', 'CO2_Zero', 'CO2_Response', 'CO_Zero', 'CO_Response', 'NH3_Zero','NH3_Response', 'CH4_Intercept', 'CH4_Slope', 'CO2_Intercept', 'CO2_Slope', 'CO_Intercept', 'CO_Slope', 'NH3_Intercept','NH3_Slope']]

#LGR_Cals.to_csv(str(Data_Output_Folder) + '3_Averaged_LGR_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

Calibrations['CH4_Diff_Zero'] = Calibrations['CH4_Zero'] - Calibrations['CH4_lit_Zero']
Calibrations['CH4_Diff_Response'] = Calibrations['CH4_Response'] - Calibrations['CH4_lit_Response']
Calibrations['CO2_Diff_Zero'] = Calibrations['CO2_Zero'] - Calibrations['CO2_lit_Zero']
Calibrations['CO2_Diff_Response'] = Calibrations['CO2_Response'] - Calibrations['CO2_lit_Response']
Calibrations['CO_Diff_Zero'] = Calibrations['CO_Zero'] - Calibrations['CO_lit_Zero']
Calibrations['CO_Diff_Response'] = Calibrations['CO_Response'] - Calibrations['CO_lit_Response']
Calibrations['NH3_Diff_Zero'] = Calibrations['NH3_Zero'] - Calibrations['NH3_lit_Zero']

LGR_prov_Cals = Calibrations[['CH4_Intercept', 'CH4_Slope', 'CO2_Intercept', 'CO2_Slope', 'CO_Intercept', 'CO_Slope', 'NH3_Intercept','NH3_Slope','CH4_Zero', 'CH4_lit_Zero', 'CH4_Diff_Zero', 'CH4_Response', 'CH4_lit_Response', 'CH4_Diff_Response', 'CO2_Zero','CO2_lit_Zero', 'CO2_Diff_Zero', 'CO2_Response', 'CO2_lit_Response','CO2_Diff_Response', 'CO_Zero', 'CO_lit_Zero','CO_Diff_Zero','CO_Response','CO_lit_Response', 'CO_Diff_Response','NH3_Zero', 'NH3_lit_Zero', 'NH3_Diff_Zero','NH3_Response']]

#LGR_prov_Cals.to_csv(str(Data_Output_Folder) + '2_For_Check_LGR_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

LGR_prov_Cals['CO_Zero'] = LGR_prov_Cals['CO_Zero']*1000
LGR_prov_Cals['NH3_Zero'] = LGR_prov_Cals['NH3_Zero']*1000
LGR_prov_Cals['CO_Intercept'] = LGR_prov_Cals['CO_Intercept']*1000
LGR_prov_Cals['NH3_Intercept'] = LGR_prov_Cals['NH3_Intercept']*1000
LGR_prov_Cals['CO_lit_Zero'] = LGR_prov_Cals['CO_lit_Zero']*1000
LGR_prov_Cals['NH3_lit_Zero'] = LGR_prov_Cals['NH3_lit_Zero']*1000
LGR_prov_Cals['CO_Diff_Zero'] = LGR_prov_Cals['CO_Zero'] - LGR_prov_Cals['CO_lit_Zero']
LGR_prov_Cals['NH3_Diff_Zero'] = LGR_prov_Cals['NH3_Zero'] - LGR_prov_Cals['NH3_lit_Zero']

#LGR_prov_Cals.to_csv(str(Data_Output_Folder) + '6_For_Check_LGR_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

LGR_Cals = LGR_prov_Cals[['CH4_Zero', 'CH4_Response', 'CO2_Zero', 'CO2_Response', 'CO_Zero', 'CO_Response', 'NH3_Zero','NH3_Response', 'CH4_Intercept', 'CH4_Slope', 'CO2_Intercept', 'CO2_Slope', 'CO_Intercept', 'CO_Slope', 'NH3_Intercept','NH3_Slope']]

LGR_Cals['CO_Zero'] = LGR_Cals['CO_Zero']/1000
LGR_Cals['NH3_Zero'] = LGR_Cals['NH3_Zero']/1000
LGR_Cals['CO_Intercept'] = LGR_Cals['CO_Intercept']/1000
LGR_Cals['NH3_Intercept'] = LGR_Cals['NH3_Intercept']/1000

LGR_Cals['CO_-1_offset'] = LGR_Cals['CO_Zero'].shift(periods=-1)
LGR_Cals['CO_+1_offset'] = LGR_Cals['CO_Zero'].shift(periods=1)

LGR_Cals['offset_flags'] = np.where(((LGR_Cals['CO_Zero'] != LGR_Cals['CO_-1_offset']) & (LGR_Cals['NH3_Zero'].isnull() )), 1, 0)
LGR_Cals['offset_flags'] = np.where(((LGR_Cals['CO_Zero'] != LGR_Cals['CO_+1_offset']) & (LGR_Cals['NH3_Zero'].isnull() )), 1, LGR_Cals['offset_flags'])
#LGR_Cals.drop(LGR_Cals[(LGR_Cals['Multi-Carbon_offset_flags'] == 1)].index,inplace =True)

LGR_Cals['NH3_-1_offset'] = LGR_Cals['NH3_Zero'].shift(periods=-1)
LGR_Cals['NH3_+1_offset'] = LGR_Cals['NH3_Zero'].shift(periods=1)

LGR_Cals['offset_flags'] = np.where(((LGR_Cals['NH3_Zero'] != LGR_Cals['NH3_-1_offset']) & (LGR_Cals['CO_Zero'].isnull() )), 1, LGR_Cals['offset_flags'])
LGR_Cals['offset_flags'] = np.where(((LGR_Cals['NH3_Zero'] != LGR_Cals['NH3_+1_offset']) & (LGR_Cals['CO_Zero'].isnull() )), 1, LGR_Cals['offset_flags'])
LGR_Cals.drop(LGR_Cals[(LGR_Cals['offset_flags'] == 0)].index,inplace =True)

LGR_Cals = LGR_Cals.drop(columns=[ 'CO_-1_offset', 'CO_+1_offset', 'NH3_-1_offset', 'NH3_+1_offset'])
LGR_Cals = LGR_Cals.drop(columns=['offset_flags'])

#Start Audit
cal_Freq = '60min'
start_file_date = datetime.datetime(2022,5,16,0,0,00)

start_date_str = str(start_file_date.strftime("%Y")) + str(start_file_date.strftime("%m")) 
next_month = start_file_date + dateutil.relativedelta.relativedelta(months=1)
next_month_str = str(next_month.strftime("%Y")) + str(next_month.strftime("%m")) 
months_audit = [str(start_date_str), str(next_month_str)]

print(months_audit)
end_date_str = str(today.strftime("%Y")) + str(today.strftime("%m"))

while str(next_month_str) <str(end_date_str):
    print(str(next_month_str), str(end_date_str))
    next_month = next_month + dateutil.relativedelta.relativedelta(months=1)
    next_month_str = str(next_month.strftime("%Y")) + str(next_month.strftime("%m")) 
    months_audit.append(str(next_month_str))
    if str(next_month_str) == str(end_date_str):
       break



for x in months_audit:
    Monthly_files = str(Data_Source_Folder) + x + '*_lgr.csv'
    #Monthly_files = str(Data_Source_Folder) + str(start_date_str) + '*_lgr.csv'
    csv_files = glob.glob(Monthly_files) 

    ghg_frames = []

    for csv in csv_files:
    
        csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv2, usecols=[0,1,2,4,6,8,32,33,35,54,55],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False ) #
        ghg_frames.append(df)

    LGR_Data = pd.concat(ghg_frames)

    LGR_Data['row_numbers']=(LGR_Data.index).astype(float) 
    LGR_Data.drop(LGR_Data[(LGR_Data['row_numbers'] <= 9)].index,inplace =True)
    LGR_Data = LGR_Data.drop(columns=['row_numbers'])
    
    LGR_Data.rename(columns={0: 'Date',1: 'Time',2: 'CH4 (ppm)',4: 'H2O (ppm) - MultiCarbon analyser',6: 'CO2 (ppm)',8: 'CO (ppb)'}, inplace=True)
    LGR_Data.rename(columns={32: 'Test',33: 'NH3 (ppb)',35: 'H2O (ppm) - NH3 analyser',54: 'Multi C Cal',55: 'NH3 Cal'}, inplace=True)

    LGR_Data = LGR_Data[['Date','Time','CH4 (ppm)','H2O (ppm) - MultiCarbon analyser','CO2 (ppm)','CO (ppb)','NH3 (ppb)','Test','H2O (ppm) - NH3 analyser','Multi C Cal','NH3 Cal']]

    LGR_Data['Date'] = LGR_Data['Date'].astype(str)
    LGR_Data['Time'] = LGR_Data['Time'].astype(str)
    LGR_Data['Date_length'] = LGR_Data['Date'].str.len()
    LGR_Data['Time_length'] = LGR_Data['Time'].str.len()
    LGR_Data=LGR_Data[LGR_Data.Date_length == 10] #checking that the cells of GHG_Data['Date'] have only 10 characters such as with 01/01/2019
    LGR_Data=LGR_Data[LGR_Data.Time_length == 8] #checking that the cells of GHG_Data['Time'] have only 8 characters such as with 12:00:00
    LGR_Data['datetime'] = LGR_Data['Date']+' '+ LGR_Data['Time']# added Date and time into new columns
    LGR_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in LGR_Data['datetime']] #converts the dateTime format from string to python dateTime
    LGR_Data.index =LGR_Data['datetime']
    LGR_Data = LGR_Data.sort_index()
    LGR_Data = LGR_Data.drop(columns=['Time', 'Date', 'Date_length','Time_length', 'datetime'])

    LGR_Data['error_2'] = np.where(LGR_Data['Test'] == '       Disabled', 'TRUE', 'FALSE')
    LGR_Data.drop(LGR_Data[(LGR_Data['error_2'] == 'FALSE')].index,inplace =True)
    LGR_Data = LGR_Data.drop(columns=['Test', 'error_2'])
    
    if x == str(start_date_str):
        LGR_Audit_Data = LGR_Data
    else:
        LGR_Audit_Data = pd.concat([LGR_Audit_Data, LGR_Data])
        LGR_Audit_Data = LGR_Audit_Data.sort_index()


print(LGR_Audit_Data)

LGR_Data = LGR_Audit_Data

LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'FALSE')].index,inplace =True)
LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - NH3 analyser'] == 'FALSE')].index,inplace =True)
LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - MultiCarbon analyser'] == 'TRUE')].index,inplace =True)
LGR_Data.drop(LGR_Data[(LGR_Data['H2O (ppm) - NH3 analyser'] == 'TRUE')].index,inplace =True) 

LGR_Data['CH4 (ppm)'] = LGR_Data['CH4 (ppm)'].astype(str)
LGR_Data['H2O (ppm) - MultiCarbon analyser'] = LGR_Data['H2O (ppm) - MultiCarbon analyser'].astype(str)
LGR_Data['CO2 (ppm)'] = LGR_Data['CO2 (ppm)'].astype(str)
LGR_Data['CO (ppb)'] = LGR_Data['CO (ppb)'].astype(str)
LGR_Data['H2O (ppm) - NH3 analyser'] = LGR_Data['H2O (ppm) - NH3 analyser'].astype(str)
LGR_Data['NH3 (ppb)'] = LGR_Data['NH3 (ppb)'].astype(str)

LGR_Data['CH4_str_length'] = LGR_Data['CH4 (ppm)'].str.len()
LGR_Data['H2O_1_str_length'] = LGR_Data['H2O (ppm) - MultiCarbon analyser'].str.len()
LGR_Data['CO2_str_length'] = LGR_Data['CO2 (ppm)'].str.len()
LGR_Data['CO_str_length'] = LGR_Data['CO (ppb)'].str.len()
LGR_Data['H2O_2_str_length'] = LGR_Data['H2O (ppm) - NH3 analyser'].str.len()
LGR_Data['NH3_str_length'] = LGR_Data['NH3 (ppb)'].str.len()

LGR_Data=LGR_Data[LGR_Data.CH4_str_length >= 1] 
LGR_Data=LGR_Data[LGR_Data.CH4_str_length <= 22] 
LGR_Data=LGR_Data[LGR_Data.H2O_1_str_length >= 1]
LGR_Data=LGR_Data[LGR_Data.H2O_1_str_length <= 22]

LGR_Data=LGR_Data[LGR_Data.CO2_str_length >= 1] 
LGR_Data=LGR_Data[LGR_Data.CO2_str_length <= 22] 
LGR_Data=LGR_Data[LGR_Data.CO_str_length >= 1]
LGR_Data=LGR_Data[LGR_Data.CO_str_length <= 22]

LGR_Data=LGR_Data[LGR_Data.H2O_2_str_length >= 1] 
LGR_Data=LGR_Data[LGR_Data.H2O_2_str_length <= 22] 
LGR_Data=LGR_Data[LGR_Data.NH3_str_length >= 1]
LGR_Data=LGR_Data[LGR_Data.NH3_str_length <= 22]

LGR_Data = LGR_Data.drop(columns=['CH4_str_length', 'H2O_1_str_length', 'CO2_str_length','CO_str_length','H2O_2_str_length','NH3_str_length'])

GHG_Data = LGR_Data[['CH4 (ppm)','H2O (ppm) - MultiCarbon analyser','CO2 (ppm)','CO (ppb)','Multi C Cal']]

GHG_Data['CH4 (ppm)'] = GHG_Data['CH4 (ppm)'].astype(float)
GHG_Data['H2O (ppm) - MultiCarbon analyser'] = GHG_Data['H2O (ppm) - MultiCarbon analyser'].astype(float)
GHG_Data['CO2 (ppm)'] = GHG_Data['CO2 (ppm)'].astype(float)
GHG_Data['CO (ppb)'] = GHG_Data['CO (ppb)'].astype(float)
GHG_Data['Multi C Cal'] = GHG_Data['Multi C Cal'].astype(float)

GHG_Cal_Data = GHG_Data[GHG_Data['Multi C Cal'] != 0] 

start = datetime.datetime(int(start_file_date.strftime("%Y")),int(start_file_date.strftime("%m")),int(start_file_date.strftime("%d")),0,0,00) 
end = datetime.datetime(int(today.strftime("%Y")),int(today.strftime("%m")),int(today.strftime("%d")),23,59,59) 

GHG_Cal_Data = GHG_Cal_Data[start:end]
GHG_Cal_Data = GHG_Cal_Data.groupby(pd.Grouper(freq=av_Freq)).mean()

CO_Zero_Data=GHG_Cal_Data[GHG_Cal_Data['CO (ppb)'] < -0.2]
CO_Zero_Data=CO_Zero_Data[CO_Zero_Data['CO (ppb)'] > -0.45]
CO_Zero_Data = CO_Zero_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
CO_Zero_Data['Cal-1'] = CO_Zero_Data['Multi C Cal'].shift(periods=-1)
CO_Zero_Data['Cal+1'] = CO_Zero_Data['Multi C Cal'].shift(periods=1)
CO_Zero_Data.drop(CO_Zero_Data[(CO_Zero_Data['Cal-1'].isnull() )].index,inplace =True) 
CO_Zero_Data.drop(CO_Zero_Data[(CO_Zero_Data['Cal+1'].isnull() )].index,inplace =True) 
CO_Zero_Data.drop(CO_Zero_Data[(CO_Zero_Data['CO (ppb)'].isnull() )].index,inplace =True) 
CO_Zero_Data = CO_Zero_Data[['CH4 (ppm)','H2O (ppm) - MultiCarbon analyser','CO2 (ppm)','CO (ppb)']]
#CO_min = CO_Zero_Data['CO (ppb)'].groupby(pd.Grouper(freq=cal_Freq)).min() 
CO_Zero_Data = CO_Zero_Data.groupby(pd.Grouper(freq=cal_Freq)).mean()
#CO_Zero_Data['CO (ppb)'] = pd.Series(CO_min)
CO_Zero_Data.drop(CO_Zero_Data[(CO_Zero_Data['CO (ppb)'].isnull() )].index,inplace =True) 
CO_Zero_Data.rename(columns={'CO (ppb)': 'CO Zero'}, inplace=True)
print(CO_Zero_Data)

CO_Cal_Data=GHG_Cal_Data[GHG_Cal_Data['CO (ppb)'] < 6.8]
CO_Cal_Data=CO_Cal_Data[CO_Cal_Data['CO (ppb)'] > 6.2]
CO_Cal_Data = CO_Cal_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
CO_Cal_Data['Cal-1'] = CO_Cal_Data['Multi C Cal'].shift(periods=-1)
CO_Cal_Data['Cal+1'] = CO_Cal_Data['Multi C Cal'].shift(periods=1)
CO_Cal_Data.drop(CO_Cal_Data[(CO_Cal_Data['Cal-1'].isnull() )].index,inplace =True) 
CO_Cal_Data.drop(CO_Cal_Data[(CO_Cal_Data['Cal+1'].isnull() )].index,inplace =True) 
CO_Cal_Data.drop(CO_Cal_Data[(CO_Cal_Data['CO (ppb)'].isnull() )].index,inplace =True) 
CO_Cal_Data = CO_Cal_Data[['CH4 (ppm)','H2O (ppm) - MultiCarbon analyser','CO2 (ppm)','CO (ppb)']]
#CO_min = CO_Cal_Data['CO (ppb)'].groupby(pd.Grouper(freq=cal_Freq)).max() 
CO_Cal_Data = CO_Cal_Data.groupby(pd.Grouper(freq=cal_Freq)).mean()
#CO_Cal_Data['CO (ppb)'] = pd.Series(CO_min)
CO_Cal_Data.drop(CO_Cal_Data[(CO_Cal_Data['CO (ppb)'].isnull() )].index,inplace =True) 
CO_Cal_Data.rename(columns={'CO (ppb)': 'CO Cal'}, inplace=True)

CO_Zero_Data = CO_Zero_Data[['CO2 (ppm)','CO Zero']]
CO_Internal_Cals = CO_Cal_Data[['CH4 (ppm)','CO Cal']]
CO_Internal_Cals = pd.concat([CO_Zero_Data, CO_Internal_Cals])
CO_Internal_Cals = CO_Internal_Cals[['CO Zero','CO Cal']]
CO_Internal_Cals = CO_Internal_Cals.sort_index()
CO_Internal_Cals = CO_Internal_Cals.groupby(pd.Grouper(freq=cal_Freq)).mean()
CO_Internal_Cals.drop(CO_Internal_Cals[(CO_Internal_Cals['CO Zero'].isnull() & CO_Internal_Cals['CO Cal'].isnull() )].index,inplace =True) 
CO_Internal_Cals['datetime'] = CO_Internal_Cals.index
day_Freq = '1440min'
datetime_min = CO_Internal_Cals['datetime'].groupby(pd.Grouper(freq=day_Freq)).min() 
CO_Internal_Cals = CO_Internal_Cals.groupby(pd.Grouper(freq=day_Freq)).mean()
CO_Internal_Cals['datetime'] = pd.Series(datetime_min)
CO_Internal_Cals.drop(CO_Internal_Cals[(CO_Internal_Cals['CO Zero'].isnull() & CO_Internal_Cals['CO Cal'].isnull() )].index,inplace =True) 

CO_Internal_Cals.index = CO_Internal_Cals['datetime']
CO_Internal_Cals=CO_Internal_Cals[['CO Zero','CO Cal']]
CO_Internal_Cals.drop(CO_Internal_Cals[(CO_Internal_Cals['CO Cal'].isnull() )].index,inplace =True) 
CO_Internal_Cals['CO Cal'] = 5/(CO_Internal_Cals['CO Cal'] - CO_Internal_Cals['CO Zero'])
CO_Internal_Cals['CO_Intercept'] = - CO_Internal_Cals['CO Cal']*CO_Internal_Cals['CO Zero']
CO_Internal_Cals = CO_Internal_Cals[['CO_Intercept','CO Cal']]
CO_Internal_Cals.rename(columns={'CO Cal': 'CO_Slope'}, inplace=True)
#print(CO_Internal_Cals)

LGR_Cals = pd.concat([LGR_Cals, CO_Internal_Cals])

LGR_Cals = LGR_Cals.sort_index()

Full_Cal_Folder = str(Data_Output_Folder) + "LGR_Cal_Files/"

if not os.path.exists(Full_Cal_Folder):
    os.makedirs(Full_Cal_Folder)

Old_Cal_Folder = str(Full_Cal_Folder) + "/Previous_LGR_Cal_Files/"

if not os.path.exists(Old_Cal_Folder):
    os.makedirs(Old_Cal_Folder)

full_cal_file = str(Full_Cal_Folder) + '1_Overall_LGR_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv'

if os.path.exists(str(full_cal_file)):
    os.rename(str(full_cal_file), str(Data_Output_Folder) + '1_Overall_LGR_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '_old.csv')
else:
    pass

pattern = '1_Overall_LGR_Calibrations*.csv'
files = glob.glob(str(Full_Cal_Folder) + pattern)

# move the files with txt extension
for file in files:
    # extract file name form file path
    file_name = os.path.basename(file)
    if os.path.isfile(Old_Cal_Folder + file_name):
        expand = 1
        while True:
            expand += 1
            new_file_name = file_name.split(".csv")[0] + str(expand) + ".csv"
            if os.path.isfile(new_file_name):
                continue
            else:
                file_name = new_file_name
                break          

LGR_Cals.to_csv(str(Full_Cal_Folder) + '1_Overall_LGR_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

