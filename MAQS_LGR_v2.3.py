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
version_number = 'v2.3' #version of the code
year_start = 2022 #input the year of study
month_start = 12 #input the month of study
default_start_day = 1 #default start date set
day_start = default_start_day
validity_status = 'Unratified' #Ratified or Unratified

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

end = datetime.datetime(year_end,month_end,day_end,23,59,00) #if new end date needed to can be changed here 

start_year_month_str = str(start.strftime("%Y")) + str(start.strftime("%m")) # convert start and end months to strings
end_year_month_str = str(end.strftime("%Y")) + str(end.strftime("%m"))

end_Date_Check = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

date_file_label = np.where(start_year_month_str == end_year_month_str, start_year_month_str, str(start_year_month_str) + "-" + str(end_year_month_str))
#print(date_file_label) #print end date to check it is correct

prior_date_1 = start - timedelta(days=1)
date_Check_1 = str(prior_date_1.strftime("%Y")) + str(prior_date_1.strftime("%m")) + str(prior_date_1.strftime("%d"))

prior_date_2 = start - timedelta(days=2)
date_Check_2 = str(prior_date_2.strftime("%Y")) + str(prior_date_2.strftime("%m")) + str(prior_date_2.strftime("%d"))

folder = np.where((str(version_number) == 'v0.6'), 'Preliminary', str(validity_status))
print("using a " + str(folder) + "_" + str(version_number) + " folder")

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/LGR/', 'D:/FirsData/LGR/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(folder) + '_' + str(version_number) + '/', 'D:/' + str(folder) + '_' + str(version_number) + '/')
#Data_Source_Folder = np.where((start_year_month_str == '201901')|(start_year_month_str == '201906')|(start_year_month_str == '201909')|(start_year_month_str == '201911'), 'D:/FirsData/NOyOzone/', Data_Source_Folder)
#Data_Output_Folder = np.where((start_year_month_str == '201901')|(start_year_month_str == '201906')|(start_year_month_str == '201909'), 'D:/Ratified_v1.0/', Data_Output_Folder)

LGR_Cal_Data_Source = str(Data_Output_Folder) + "LGR_Cal_Files/"

pattern = str(LGR_Cal_Data_Source) + '1_Overall_LGR_Calibrations*' + '.csv'# Needs to be address of data location - Collect CSV files
LGR_cal_file = glob.glob(pattern)
print(pattern)
# Create an empty list
frames = []

#  Iterate over csv_files
for csv in LGR_cal_file:
    df = pd.read_csv(csv)
    frames.append(df)

# Concatenate frames into a single DataFrame
LGR_Cal = pd.concat(frames)
LGR_Cal['datetime'] = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in LGR_Cal['datetime']]

#print(LGR_Cal['CH4_Zero'])

#LGR_Cal.iloc[-1] = np.where( LGR_Cal.iloc[-1].isnull() , , LGR_Cal.iloc[-1])

LGR_Cal['Ammonia_Cal'] = np.where((LGR_Cal['NH3_Intercept'].isnull()), True, False) 
LGR_Cal['MultiCarbon_Cal'] = np.where((LGR_Cal['CH4_Intercept'].isnull() & LGR_Cal['CO2_Intercept'].isnull()  & LGR_Cal['CO_Intercept'].isnull() ), True, False)
GHG_Cal = LGR_Cal[['datetime', 'CH4_Intercept', 'CH4_Slope', 'CO2_Intercept', 'CO2_Slope', 'CO_Intercept', 'CO_Slope', 'MultiCarbon_Cal']]
GHG_Cal.drop(GHG_Cal[(GHG_Cal['MultiCarbon_Cal'] == True)].index,inplace =True) 

CO_Cal = GHG_Cal[['datetime', 'CO_Intercept', 'CO_Slope', 'MultiCarbon_Cal']]
CO_Cal.drop(CO_Cal[(CO_Cal['CO_Slope'].isnull() )].index,inplace =True)

CO2_Cal = GHG_Cal[['datetime', 'CO2_Intercept', 'CO2_Slope', 'MultiCarbon_Cal']]
CO2_Cal.drop(CO2_Cal[(CO2_Cal['CO2_Slope'].isnull() )].index,inplace =True)

CH4_Cal = GHG_Cal[['datetime', 'CH4_Intercept', 'CH4_Slope', 'MultiCarbon_Cal']]
CH4_Cal.drop(CH4_Cal[(CH4_Cal['CH4_Slope'].isnull() )].index,inplace =True)

Ammonia_Cal = LGR_Cal[['datetime', 'NH3_Intercept','NH3_Slope', 'Ammonia_Cal']]
Ammonia_Cal.drop(Ammonia_Cal[(Ammonia_Cal['Ammonia_Cal'] == True)].index,inplace =True)
Ammonia_Cal.drop(Ammonia_Cal[(Ammonia_Cal['NH3_Intercept'].isnull() )].index,inplace =True)


#print(Ammonia_Cal)

#LGR_Cal.to_csv(str(Data_Output_Folder) + '6_For_Check_LGR_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')
#GHG_Cal.to_csv(str(Data_Output_Folder) + '7_For_Check_LGR_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')
#Ammonia_Cal.to_csv(str(Data_Output_Folder) + '8_For_Check_LGR_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

default_Early_Month = '20190929'

early_month = np.where((start_year_month_str == end_year_month_str) & (year_start == 2019) & (1 <= month_start <= 10), start_year_month_str, default_Early_Month) #str(year_start)

Early_month_pattern = str(Data_Source_Folder) + str(early_month) + '*_lgr.csv' # Collect CSV files

default_prior_day_1 = '20190930'
default_prior_day_2 = '20190928'

prior_day_1 = np.where((start_year_month_str == end_year_month_str) & (year_start == 2019) & (1 <= month_start <= 10),  date_Check_1, default_prior_day_1) #str(year_start)
prior_day_1 = np.where((start_year_month_str == end_year_month_str) & (year_start == 2018),  default_prior_day_1, prior_day_1) #str(year_start)

prior_day_2 = np.where((start_year_month_str == end_year_month_str) & (year_start == 2019) & (1 <= month_start <= 10),  date_Check_2, default_prior_day_2) #str(year_start)
prior_day_2 = np.where((start_year_month_str == end_year_month_str) & (year_start == 2018),  default_prior_day_2, prior_day_2) #str(year_start)

prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1) + '*_lgr.csv'# Collect CSV files

prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2) + '*_lgr.csv'# Collect CSV files

check_File_1 = os.path.isdir(prior_day_1_pattern)
if not check_File_1:
    prior_day_pattern = prior_day_2_pattern
    if start_year_month_str == '201812':
        pass
    else:
        print("using files for the date: ", str(prior_day_2))
   
else:
    prior_day_pattern = prior_day_1_pattern
    if start_year_month_str == '201812':
        pass
    else:
        print("using files for the date: ", str(prior_day_1))

if start_year_month_str == '201812':
    early_month = start_year_month_str
    Early_month_pattern = str(Data_Source_Folder) + str(early_month) + '*_lgr.csv' 
    prior_day = '20181219'
    prior_day_pattern = str(Data_Source_Folder) + str(prior_day) + '*_lgr.csv' 
    print("using files for the dated: 201812")
else:
    pass

print("using files labelled: ", str(Early_month_pattern))
print("Also using files labelled: ", str(prior_day_pattern))


if start_year_month_str == '201906':
    print("using method for date: ", str(start_year_month_str))
    Prior_Day = str(Data_Source_Folder) + str(20190531) + '*_lgr.csv'
    Full_Files_1 = str(Data_Source_Folder) + str(201906) + '*00_lgr.csv'
    Full_Files_2 = str(Data_Source_Folder) + str(201906) + '*59_lgr.csv'
    Full_Files_3 = str(Data_Source_Folder) + str(201906) + '*56_lgr.csv'
    Full_Files_4 = str(Data_Source_Folder) + str(201906) + '*50_lgr.csv'
    Full_Files_5 = str(Data_Source_Folder) + str(201906) + '*55_lgr.csv'
    Full_Files_6 = str(Data_Source_Folder) + str(201906) + '*39_lgr.csv'
    Full_Files_7 = str(Data_Source_Folder) + str(201906) + '*51_lgr.csv'
    Full_Files_8 = str(Data_Source_Folder) + str(201906) + '*36_lgr.csv'
    Full_Files_9 = str(Data_Source_Folder) + str(201906) + '*01_lgr.csv'
    
    csv_files = glob.glob(Prior_Day) + glob.glob(Full_Files_1) + glob.glob(Full_Files_2) + glob.glob(Full_Files_3) + glob.glob(Full_Files_4) + glob.glob(Full_Files_5) + glob.glob(Full_Files_6) + glob.glob(Full_Files_7) + glob.glob(Full_Files_8) + glob.glob(Full_Files_9)
    
    ghg_frames = []
    
    for csv in csv_files:
        
        csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv2, usecols=[0,1,2,4,6,8,32,33,35],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False) #
        ghg_frames.append(df)

    Prior_LGR_Data = pd.concat(ghg_frames)

elif start_year_month_str == '201812':
    print("using method for date: ", str(start_year_month_str))
    Full_Files = str(Data_Source_Folder) + str(201812) + '*_lgr.csv'
    Full_Files_1 = str(Data_Source_Folder) + str(201812) + '*00_lgr.csv'
    Full_Files_2 = str(Data_Source_Folder) + str(201812) + '*59_lgr.csv'
    Full_Files_3 = str(Data_Source_Folder) + str(201812) + '*20_lgr.csv'
    Full_Files_4 = str(Data_Source_Folder) + str(201812) + '*36_lgr.csv'
    Full_Files_5 = str(Data_Source_Folder) + str(201812) + '*11_lgr.csv'
    Full_Files_6 = str(Data_Source_Folder) + str(201812) + '*21_lgr.csv'
    Full_Files_7 = str(Data_Source_Folder) + str(201812) + '*06_lgr.csv'
    Full_Files_8 = str(Data_Source_Folder) + str(201812) + '*15_lgr.csv'
    
#    Full_Files_1 = str(Data_Source_Folder) + str(201812) + '*00_lgr.csv'
#    Full_Files_2 = str(Data_Source_Folder) + str(201812) + '*59_lgr.csv'
#    Full_Files_3 = str(Data_Source_Folder) + str(201812) + '*36_lgr.csv'
#    Full_Files_4 = str(Data_Source_Folder) + str(201812) + '*11_lgr.csv'
#    Full_Files_5 = str(Data_Source_Folder) + str(201812) + '*26_lgr.csv'
#    Full_Files_6 = str(Data_Source_Folder) + str(201812) + '*20_lgr.csv'
#    Full_Files_7 = str(Data_Source_Folder) + str(201812) + '*06_lgr.csv'
#    Full_Files_8 = str(Data_Source_Folder) + str(201812) + '*20_lgr.csv'
#    Full_Files_9 = str(Data_Source_Folder) + str(201812) + '*15_lgr.csv'
#    
    csv_files = glob.glob(Full_Files_1) + glob.glob(Full_Files_2)  + glob.glob(Full_Files_3) + glob.glob(Full_Files_4) + glob.glob(Full_Files_5) + glob.glob(Full_Files_6) + glob.glob(Full_Files_7) + glob.glob(Full_Files_8) # 
#    csv_files = glob.glob(Full_Files)
    
    ghg_frames = []
    
    for csv in csv_files:
        
        csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv2,header=None, index_col=False, skiprows=4) #, usecols=[0,1,2,4,6,8,32,33,35],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False
        ghg_frames.append(df)

    Prior_LGR_Data = pd.concat(ghg_frames)
    
    Prior_LGR_Data.rename(columns={0: 'Date'}, inplace=True)
    Prior_LGR_Data.rename(columns={1: 'Time'}, inplace=True)
    Prior_LGR_Data.rename(columns={2: 'CH4 (ppm)'}, inplace=True)
    Prior_LGR_Data.rename(columns={4: 'H2O (ppm) - MultiCarbon analyser'}, inplace=True)
    Prior_LGR_Data.rename(columns={6: 'CO2 (ppm)'}, inplace=True)
    Prior_LGR_Data.rename(columns={8: 'CO (ppm)'}, inplace=True)
    Prior_LGR_Data.rename(columns={32: 'Test'}, inplace=True)
    Prior_LGR_Data.rename(columns={33: 'NH3 (ppm)'}, inplace=True) #NH3 is labelled as NH4 in early raw files
    Prior_LGR_Data.rename(columns={35: 'H2O (ppm) - NH3 analyser'}, inplace=True)
    
    LGR_drop_list = list(Prior_LGR_Data.columns.values)
    LGR_drop_list.remove('Date')
    LGR_drop_list.remove('Time')
    LGR_drop_list.remove('CH4 (ppm)')
    LGR_drop_list.remove('H2O (ppm) - MultiCarbon analyser')
    LGR_drop_list.remove('CO2 (ppm)')
    LGR_drop_list.remove('CO (ppm)')
    LGR_drop_list.remove('NH3 (ppm)')
    LGR_drop_list.remove('Test')
    LGR_drop_list.remove('H2O (ppm) - NH3 analyser')
    Prior_LGR_Data = Prior_LGR_Data.drop(columns=LGR_drop_list)
#    Prior_LGR_Data.to_csv(str(Data_Output_Folder) + '9_MultiCarbon_File_' + str(date_file_label) + '_' + str(version_number) + '.csv')

else:
    print("using standard method")
    csv_files = glob.glob(Early_month_pattern) + glob.glob(prior_day_pattern)
    
    ghg_frames = []
    
    for csv in csv_files:
        
        csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv2, usecols=[0,1,2,4,6,8,32,33,35],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False) #
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
Prior_LGR_Data.rename(columns={8: 'CO (ppm)'}, inplace=True)
Prior_LGR_Data.rename(columns={32: 'Test'}, inplace=True)
Prior_LGR_Data.rename(columns={33: 'NH3 (ppm)'}, inplace=True) #NH3 is labelled as NH4 in early raw files
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
Prior_LGR_Data = Prior_LGR_Data.drop(columns=['Time', 'Date', 'Date_length','Time_length'])
#Prior_LGR_Data = Prior_GHG_Data.drop(columns=['datetime']) # could drop datetime column?

#Prior_LGR_Data['NH3 (ppm)'] = np.where(Prior_LGR_Data["NH3 (ppm)"] >= -5)

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
Prior_LGR_Data['CO (ppm)'] = Prior_LGR_Data['CO (ppm)'].astype(str)
Prior_LGR_Data['H2O (ppm) - NH3 analyser'] = Prior_LGR_Data['H2O (ppm) - NH3 analyser'].astype(str)
Prior_LGR_Data['NH3 (ppm)'] = Prior_LGR_Data['NH3 (ppm)'].astype(str)

Prior_LGR_Data['CH4_str_length'] = Prior_LGR_Data['CH4 (ppm)'].str.len()
Prior_LGR_Data['H2O_1_str_length'] = Prior_LGR_Data['H2O (ppm) - MultiCarbon analyser'].str.len()
Prior_LGR_Data['CO2_str_length'] = Prior_LGR_Data['CO2 (ppm)'].str.len()
Prior_LGR_Data['CO_str_length'] = Prior_LGR_Data['CO (ppm)'].str.len()
Prior_LGR_Data['H2O_2_str_length'] = Prior_LGR_Data['H2O (ppm) - NH3 analyser'].str.len()
Prior_LGR_Data['NH3_str_length'] = Prior_LGR_Data['NH3 (ppm)'].str.len()

if start_year_month_str == '201812':
    Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CH4_str_length >= 2] 
    Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CH4_str_length <= 16] 
    Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_1_str_length >= 2]
    Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_1_str_length <= 16]

    Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO2_str_length >= 2] 
    Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO2_str_length <= 16] 
    Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO_str_length >= 2]
    Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.CO_str_length <= 16]

    Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_2_str_length >= 2] 
    Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.H2O_2_str_length <= 16] 
    Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.NH3_str_length >= 2]
    Prior_LGR_Data=Prior_LGR_Data[Prior_LGR_Data.NH3_str_length <= 16]

else:
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

#Prior_LGR_Data.to_csv(str(Data_Output_Folder) + '4_MultiCarbon_File_' + str(date_file_label) + '_' + str(version_number) + '.csv')

Prior_GHG_Data = Prior_LGR_Data[['CH4 (ppm)', 'H2O (ppm) - MultiCarbon analyser','CO2 (ppm)','CO (ppm)','datetime']]

Prior_GHG_Data['CH4 (ppm)'] = Prior_GHG_Data['CH4 (ppm)'].astype(float)
Prior_GHG_Data['H2O (ppm) - MultiCarbon analyser'] = Prior_GHG_Data['H2O (ppm) - MultiCarbon analyser'].astype(float)
Prior_GHG_Data['CO2 (ppm)'] = Prior_GHG_Data['CO2 (ppm)'].astype(float)
Prior_GHG_Data['CO (ppm)'] = Prior_GHG_Data['CO (ppm)'].astype(float)

year_Audit_1 = 2019 #input the year of Audit
month_Audit_1 = 8 #input the month of Audit
day_Audit_1 = 9 #input the day of Audit

start_CO_Anom_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,34,6)
end_CO_Anom_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,34,8)
#GHG_Data.drop(GHG_Data.loc[start_CO_Anom_1:end_CO_Anom_1].index, inplace=True)
Prior_GHG_Data.loc[start_CO_Anom_1:end_CO_Anom_1, ('CO (ppm)')] = np.nan

start_CO_Anom_2 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,39,39)
end_CO_Anom_2 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,39,41)
#GHG_Data.drop(GHG_Data.loc[start_CO_Anom_2:end_CO_Anom_2].index, inplace=True)
Prior_GHG_Data.loc[start_CO_Anom_2:end_CO_Anom_2, ('CO (ppm)')] = np.nan

start_CO_Anom_3 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,42,19)
end_CO_Anom_3 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,42,21)
#GHG_Data.drop(GHG_Data.loc[start_CO_Anom_3:end_CO_Anom_3].index, inplace=True)
Prior_GHG_Data.loc[start_CO_Anom_3:end_CO_Anom_3, ('CO (ppm)')] = np.nan

start_CO_Anom_4 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,46,57)
end_CO_Anom_4 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,46,59)
#GHG_Data.drop(GHG_Data.loc[start_CO_Anom_4:end_CO_Anom_4].index, inplace=True)
Prior_GHG_Data.loc[start_CO_Anom_4:end_CO_Anom_4, ('CO (ppm)')] = np.nan

Prior_GHG_Data['Multi C Cal']=np.nan

Calibration_CH4_Boundary = 6 # setting that if the methane level goes above 6ppm then it is being calibrated

Prior_GHG_Data['Multi C Cal'] = np.where(Prior_GHG_Data['CH4 (ppm)']> float(Calibration_CH4_Boundary), 'TRUE', 'FALSE')

Prior_Ammonia_Data = Prior_LGR_Data[['H2O (ppm) - NH3 analyser', 'NH3 (ppm)','datetime']]

if start_year_month_str == '201906' or start_year_month_str == '201907' or start_year_month_str == '201908' or start_year_month_str == '201909':
    Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'] = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'].str.replace('es', 'e+').astype(str)
    Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'] = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'].str.strip('S').astype(str)
    Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'] = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'].str.strip('@abcSNÅÉÊå').astype(str)
    Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'] = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'].str.lstrip().astype(str)  
    Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'] = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'].str.lstrip('@').astype(str) 
    Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'] = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'].str.lstrip().astype(str)  
    Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'] = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'].str.strip('S,b,d,Ã,...,N,a,c,i,f,\,`,N,K,Ã,e,').astype(str)
    Prior_Ammonia_Data['H2O_2_str_length'] = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'].str.len()
    Prior_Ammonia_Data=Prior_Ammonia_Data[Prior_Ammonia_Data.H2O_2_str_length == 11]
    Prior_Ammonia_Data['NH3 (ppm)'] = Prior_Ammonia_Data['NH3 (ppm)'].str.replace('es', 'e+').astype(str)
    Prior_Ammonia_Data['NH3 (ppm)'] = Prior_Ammonia_Data['NH3 (ppm)'].str.strip('S').astype(str)
    Prior_Ammonia_Data['NH3 (ppm)'] = Prior_Ammonia_Data['NH3 (ppm)'].str.strip('@abcSNÅÉÊå').astype(str)
    Prior_Ammonia_Data['NH3 (ppm)'] = Prior_Ammonia_Data['NH3 (ppm)'].str.lstrip().astype(str)  
    Prior_Ammonia_Data['NH3 (ppm)'] = Prior_Ammonia_Data['NH3 (ppm)'].str.lstrip('@').astype(str) 
    Prior_Ammonia_Data['NH3 (ppm)'] = Prior_Ammonia_Data['NH3 (ppm)'].str.lstrip().astype(str)  
    Prior_Ammonia_Data['NH3 (ppm)'] = Prior_Ammonia_Data['NH3 (ppm)'].str.strip('S,b,d,Ã,...,N,a,c,i,f,\,`,N,K,Ã,e,').astype(str)
    Prior_Ammonia_Data['NH3_str_length'] = Prior_Ammonia_Data['NH3 (ppm)'].str.len()
    Prior_Ammonia_Data=Prior_Ammonia_Data[Prior_Ammonia_Data.NH3_str_length == 11]
    Prior_Ammonia_Data['H2O_2_prelim'] = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser']
    Prior_Ammonia_Data['H2O_2_prelim'] = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    Prior_Ammonia_Data['NH3_prelim'] = Prior_Ammonia_Data['NH3 (ppm)']
    Prior_Ammonia_Data['NH3_prelim'] = Prior_Ammonia_Data['NH3_prelim'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'] = Prior_Ammonia_Data['H2O_2_prelim'].astype(float)
    Prior_Ammonia_Data['NH3 (ppm)'] = Prior_Ammonia_Data['NH3_prelim'].astype(float)
    Prior_Ammonia_Data = Prior_Ammonia_Data.drop(columns=['H2O_2_str_length', 'NH3_str_length', 'H2O_2_prelim', 'NH3_prelim'])
#    Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'] = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'].astype(float)
#    Prior_Ammonia_Data.index = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser']
#    Prior_Ammonia_Data = Prior_Ammonia_Data.sort_index()
#    for Element in 
#    Prior_Ammonia_Data['H2O_2_prelim'].str.replace(r'[0-9].[0-9]+e[0-9]+', regex=True)
#    Prior_Ammonia_Data['H2O_2_float_data'] = np.where((type(Prior_Ammonia_Data['H2O_2_prelim']) == float), Prior_Ammonia_Data['H2O_2_prelim'], np.nan)
#    Prior_Ammonia_Data = Prior_Ammonia_Data[pd.to_numeric(Prior_Ammonia_Data['H2O_2_prelim'], errors='coerce')] #.notnull()

else:
     Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'] = Prior_Ammonia_Data['H2O (ppm) - NH3 analyser'].astype(float)
     Prior_Ammonia_Data['NH3 (ppm)'] = Prior_Ammonia_Data['NH3 (ppm)'].astype(float)

Calibration_NH3_Boundary = 1

Prior_Ammonia_Data['NH3 Cal']=np.nan

Prior_Ammonia_Data['NH3 Cal'] = np.where(Prior_Ammonia_Data['NH3 (ppm)']> float(Calibration_NH3_Boundary), 'TRUE', 'FALSE')

default_Late_1 = '20191129'

late_month = np.where((start_year_month_str == end_year_month_str) & (year_start == 2019) & (1 <= month_start <= 10), default_Late_1, start_year_month_str) #str(year_start)
late_month = np.where((start_year_month_str == end_year_month_str) & (year_start == 2018),  default_Late_1, late_month) #str(year_start)

Later_month_pattern = str(Data_Source_Folder) + str(late_month) + '*_lgr.csv'# Collect CSV files

default_prior_day_3 = '20191130'
default_prior_day_4 = '20191131'

prior_day_3 = np.where((start_year_month_str == end_year_month_str) & (year_start == 2019) & (1 <= month_start <= 10), default_prior_day_3, date_Check_1) #str(year_start)
prior_day_3 = np.where((start_year_month_str == end_year_month_str) & (year_start == 2018),  default_prior_day_3, prior_day_3) #str(year_start)

prior_day_4 = np.where((start_year_month_str == end_year_month_str) & (year_start == 2019) & (1 <= month_start <= 10), default_prior_day_4, date_Check_2) #str(year_start)
prior_day_4 = np.where((start_year_month_str == end_year_month_str) & (year_start == 2018),  default_prior_day_4, prior_day_4) #str(year_start)

print(str(late_month))

prior_day_3_pattern = str(Data_Source_Folder) + str(prior_day_3) + '*_lgr.csv'# Collect CSV files

prior_day_4_pattern = str(Data_Source_Folder) + str(prior_day_4) + '*_lgr.csv'# Collect CSV files

check_File_2 = os.path.isdir(prior_day_3_pattern)
if not check_File_2:
    prior_day_2_pattern = prior_day_4_pattern
    print("using file dated : ", str(prior_day_4))

else:
    prior_day_2_pattern = prior_day_3_pattern
    print("using file dated : ", str(prior_day_3))

csv_files_2 = glob.glob(Later_month_pattern) + glob.glob(prior_day_2_pattern)

csv_files_2 = list(filter(lambda file: os.stat(file).st_size > 1000, csv_files_2))

ghg_frames_2 = []

for csv in csv_files_2:
    
    csv2 = open(csv, 'r', errors='backslashreplace')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv2, usecols=[0,1,2,4,6,8,32,33,35,54,55],header=None, low_memory=False,skip_blank_lines=True, error_bad_lines=True, na_filter=False ) #
    ghg_frames_2.append(df)

LGR_Data = pd.concat(ghg_frames_2)

LGR_Data['row_numbers']=(LGR_Data.index).astype(float) 
LGR_Data.drop(LGR_Data[(LGR_Data['row_numbers'] <= 9)].index,inplace =True)
LGR_Data = LGR_Data.drop(columns=['row_numbers'])

#GHG_Data = pd.concat(map(pd.read_csv, csv_files_2),sort=True)

LGR_Data.rename(columns={0: 'Date'}, inplace=True)
LGR_Data.rename(columns={1: 'Time'}, inplace=True)
LGR_Data.rename(columns={2: 'CH4 (ppm)'}, inplace=True)
LGR_Data.rename(columns={4: 'H2O (ppm) - MultiCarbon analyser'}, inplace=True)
LGR_Data.rename(columns={6: 'CO2 (ppm)'}, inplace=True)
LGR_Data.rename(columns={8: 'CO (ppm)'}, inplace=True)
LGR_Data.rename(columns={32: 'Test'}, inplace=True)
LGR_Data.rename(columns={33: 'NH3 (ppm)'}, inplace=True)
LGR_Data.rename(columns={35: 'H2O (ppm) - NH3 analyser'}, inplace=True)
LGR_Data.rename(columns={54: 'Multi C Cal'}, inplace=True)
LGR_Data.rename(columns={55: 'NH3 Cal'}, inplace=True)

LGR_drop_list = list(LGR_Data.columns.values)
LGR_drop_list.remove('Date')
LGR_drop_list.remove('Time')
LGR_drop_list.remove('CH4 (ppm)')
LGR_drop_list.remove('H2O (ppm) - MultiCarbon analyser')
LGR_drop_list.remove('CO2 (ppm)')
LGR_drop_list.remove('CO (ppm)')
LGR_drop_list.remove('NH3 (ppm)')
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
LGR_Data = LGR_Data.drop(columns=['Time', 'Date', 'Date_length','Time_length'])
#LGR_Data = LGR_Data.drop(columns=['datetime'])

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
LGR_Data['CO (ppm)'] = LGR_Data['CO (ppm)'].astype(str)
LGR_Data['H2O (ppm) - NH3 analyser'] = LGR_Data['H2O (ppm) - NH3 analyser'].astype(str)
LGR_Data['NH3 (ppm)'] = LGR_Data['NH3 (ppm)'].astype(str)

LGR_Data['CH4_str_length'] = LGR_Data['CH4 (ppm)'].str.len()
LGR_Data['H2O_1_str_length'] = LGR_Data['H2O (ppm) - MultiCarbon analyser'].str.len()
LGR_Data['CO2_str_length'] = LGR_Data['CO2 (ppm)'].str.len()
LGR_Data['CO_str_length'] = LGR_Data['CO (ppm)'].str.len()
LGR_Data['H2O_2_str_length'] = LGR_Data['H2O (ppm) - NH3 analyser'].str.len()
LGR_Data['NH3_str_length'] = LGR_Data['NH3 (ppm)'].str.len()

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

GHG_Data = LGR_Data[['CH4 (ppm)', 'H2O (ppm) - MultiCarbon analyser','CO2 (ppm)','CO (ppm)', 'Multi C Cal','datetime']]
GHG_Data['CH4 (ppm)'] = GHG_Data['CH4 (ppm)'].astype(float)
GHG_Data['H2O (ppm) - MultiCarbon analyser'] = GHG_Data['H2O (ppm) - MultiCarbon analyser'].astype(float)
GHG_Data['CO2 (ppm)'] = GHG_Data['CO2 (ppm)'].astype(float)
GHG_Data['CO (ppm)'] = GHG_Data['CO (ppm)'].astype(float)

Ammonia_Data = LGR_Data[['H2O (ppm) - NH3 analyser','NH3 (ppm)', 'NH3 Cal','datetime']]
Ammonia_Data['H2O (ppm) - NH3 analyser'] = Ammonia_Data['H2O (ppm) - NH3 analyser'].astype(float)
Ammonia_Data['NH3 (ppm)'] = Ammonia_Data['NH3 (ppm)'].astype(float)

#GHG_Data.to_csv(str(Data_Output_Folder) + '9_MultiCarbon_File_' + str(date_file_label) + '_' + str(version_number) + '.csv')

GHG_Data = pd.concat([Prior_GHG_Data, GHG_Data])
Ammonia_Data = pd.concat([Prior_Ammonia_Data, Ammonia_Data])
GHG_Data = GHG_Data[start:end]
Ammonia_Data = Ammonia_Data[start:end]

GHG_Data['CH4 a'] = np.interp(GHG_Data['datetime'], CH4_Cal['datetime'], CH4_Cal['CH4_Intercept']) # interpolate the zero values
GHG_Data['CH4 b'] = np.interp(GHG_Data['datetime'], CH4_Cal['datetime'], CH4_Cal['CH4_Slope']) #
GHG_Data['CH4 (ppm) perlim']=np.nan
GHG_Data['CH4 (ppm) perlim'] = (GHG_Data['CH4 (ppm)']*GHG_Data['CH4 b']) + GHG_Data['CH4 a']

GHG_Data['CO2 a'] = np.interp(GHG_Data['datetime'], CO2_Cal['datetime'], CO2_Cal['CO2_Intercept']) # interpolate the zero values
GHG_Data['CO2 b'] = np.interp(GHG_Data['datetime'], CO2_Cal['datetime'], CO2_Cal['CO2_Slope']) #
GHG_Data['CO2 (ppm) perlim']=np.nan
GHG_Data['CO2 (ppm) perlim'] = (GHG_Data['CO2 (ppm)']*GHG_Data['CO2 b']) + GHG_Data['CO2 a']

GHG_Data['CO a'] = np.interp(GHG_Data['datetime'], CO_Cal['datetime'], CO_Cal['CO_Intercept']) # interpolate the zero values
GHG_Data['CO b'] = np.interp(GHG_Data['datetime'], CO_Cal['datetime'], CO_Cal['CO_Slope']) #
GHG_Data['CO (ppm) perlim']=np.nan
GHG_Data['CO (ppm) perlim'] = (GHG_Data['CO (ppm)']*GHG_Data['CO b']) + GHG_Data['CO a']

GHG_Data = GHG_Data.drop(columns=['CH4 a', 'CH4 b', 'CO2 a', 'CO2 b', 'CO a', 'CO b'])

Ammonia_Data['NH3 a'] = np.interp(Ammonia_Data['datetime'], Ammonia_Cal['datetime'], Ammonia_Cal['NH3_Intercept']) # interpolate the zero values
Ammonia_Data['NH3 b'] = np.interp(Ammonia_Data['datetime'], Ammonia_Cal['datetime'], Ammonia_Cal['NH3_Slope']) #
Ammonia_Data['NH3 (ppm) perlim']=np.nan
Ammonia_Data['NH3 (ppm) perlim'] = Ammonia_Data['NH3 (ppm)']*Ammonia_Data['NH3 b'] + Ammonia_Data['NH3 a']

Ammonia_Data = Ammonia_Data.drop(columns=['NH3 a', 'NH3 b'])

#GHG_Data['Multi C Cal'] = GHG_Data['Multi C Cal'].astype(str)
#GHG_Data['NH3 Cal'] = GHG_Data['NH3 Cal'].astype(str)

GHG_Data['MultiCarbon_Flag'] = np.nan
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['Multi C Cal'] == 'TRUE'), 0, 1) # 4/5/2020 switch from true/false to 0 & 1
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['Multi C Cal'] == 1), 0, GHG_Data['MultiCarbon_Flag']) # 4/5/2020 switch from true/false to 0 & 1
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['Multi C Cal'] == '1'), 0, GHG_Data['MultiCarbon_Flag']) # 4/5/2020 switch from true/false to 0 & 1
Ammonia_Data['Ammonia_Flag'] = np.nan
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['NH3 Cal'] == 'TRUE'), 0, 1)
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['NH3 Cal'] == 1), 0, Ammonia_Data['Ammonia_Flag'])
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['NH3 Cal'] == '1'), 0, Ammonia_Data['Ammonia_Flag'])

#GHG_Data.drop(GHG_Data[(GHG_Data['Multi C Cal'] == 'TRUE')].index,inplace =True)
#Ammonia_Data.drop(Ammonia_Data[(Ammonia_Data['NH3 Cal'] == 'TRUE')].index,inplace =True)

MultiCarbon_Cal_Flags = GHG_Data['MultiCarbon_Flag'].groupby(pd.Grouper(freq=av_Freq)).min()
Ammonia_Cal_Flags = Ammonia_Data['Ammonia_Flag'].groupby(pd.Grouper(freq=av_Freq)).min()

GHG_Data = GHG_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
Ammonia_Data = Ammonia_Data.groupby(pd.Grouper(freq=av_Freq)).mean()

GHG_Data['MultiCarbon_Flag'] = MultiCarbon_Cal_Flags
Ammonia_Data['Ammonia_Flag'] = Ammonia_Cal_Flags 

GHG_Data['MultiCarbon_Flag_-6_offset'] = GHG_Data['MultiCarbon_Flag'].shift(periods=-6)
GHG_Data['MultiCarbon_Flag_-5_offset'] = GHG_Data['MultiCarbon_Flag'].shift(periods=-5)
GHG_Data['MultiCarbon_Flag_-4_offset'] = GHG_Data['MultiCarbon_Flag'].shift(periods=-4)
GHG_Data['MultiCarbon_Flag_-3_offset'] = GHG_Data['MultiCarbon_Flag'].shift(periods=-3)
GHG_Data['MultiCarbon_Flag_-2_offset'] = GHG_Data['MultiCarbon_Flag'].shift(periods=-2)
GHG_Data['MultiCarbon_Flag_-1_offset'] = GHG_Data['MultiCarbon_Flag'].shift(periods=-1)
GHG_Data['MultiCarbon_Flag_+1_offset'] = GHG_Data['MultiCarbon_Flag'].shift(periods=1)
GHG_Data['MultiCarbon_Flag_+2_offset'] = GHG_Data['MultiCarbon_Flag'].shift(periods=2) 
GHG_Data['MultiCarbon_Flag_+3_offset'] = GHG_Data['MultiCarbon_Flag'].shift(periods=3)
GHG_Data['MultiCarbon_Flag_+4_offset'] = GHG_Data['MultiCarbon_Flag'].shift(periods=4)
GHG_Data['MultiCarbon_Flag_+5_offset'] = GHG_Data['MultiCarbon_Flag'].shift(periods=5)
GHG_Data['MultiCarbon_Flag_+6_offset'] = GHG_Data['MultiCarbon_Flag'].shift(periods=6)
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['MultiCarbon_Flag_-6_offset']!= 1),GHG_Data['MultiCarbon_Flag_-6_offset'],GHG_Data['MultiCarbon_Flag'])
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['MultiCarbon_Flag_-5_offset']!= 1),GHG_Data['MultiCarbon_Flag_-5_offset'],GHG_Data['MultiCarbon_Flag'])
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['MultiCarbon_Flag_-4_offset']!= 1),GHG_Data['MultiCarbon_Flag_-4_offset'],GHG_Data['MultiCarbon_Flag'])
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['MultiCarbon_Flag_-3_offset']!= 1),GHG_Data['MultiCarbon_Flag_-3_offset'],GHG_Data['MultiCarbon_Flag'])
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['MultiCarbon_Flag_-2_offset']!= 1),GHG_Data['MultiCarbon_Flag_-2_offset'],GHG_Data['MultiCarbon_Flag'])
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['MultiCarbon_Flag_-1_offset']!= 1),GHG_Data['MultiCarbon_Flag_-1_offset'],GHG_Data['MultiCarbon_Flag'])
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['MultiCarbon_Flag_+1_offset']!= 1),GHG_Data['MultiCarbon_Flag_+1_offset'],GHG_Data['MultiCarbon_Flag'])
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['MultiCarbon_Flag_+2_offset']!= 1),GHG_Data['MultiCarbon_Flag_+2_offset'],GHG_Data['MultiCarbon_Flag'])
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['MultiCarbon_Flag_+3_offset']!= 1),GHG_Data['MultiCarbon_Flag_+3_offset'],GHG_Data['MultiCarbon_Flag'])
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['MultiCarbon_Flag_+4_offset']!= 1),GHG_Data['MultiCarbon_Flag_+4_offset'],GHG_Data['MultiCarbon_Flag'])
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['MultiCarbon_Flag_+5_offset']!= 1),GHG_Data['MultiCarbon_Flag_+5_offset'],GHG_Data['MultiCarbon_Flag'])
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['MultiCarbon_Flag_+6_offset']!= 1),GHG_Data['MultiCarbon_Flag_+6_offset'],GHG_Data['MultiCarbon_Flag'])

GHG_Data['MultiCarbon_Flag'] = np.where(GHG_Data['CH4 (ppm)'].isnull() & GHG_Data['H2O (ppm) - MultiCarbon analyser'].isnull() & GHG_Data['CO (ppm)'].isnull() & GHG_Data['CO2 (ppm)'].isnull(), 0, GHG_Data['MultiCarbon_Flag'])
GHG_Data.drop(GHG_Data[(GHG_Data['MultiCarbon_Flag'] == 0)].index,inplace =True)


Ammonia_Data['Ammonia_Flag_-6_offset'] = Ammonia_Data['Ammonia_Flag'].shift(periods=-6)
Ammonia_Data['Ammonia_Flag_-5_offset'] = Ammonia_Data['Ammonia_Flag'].shift(periods=-5)
Ammonia_Data['Ammonia_Flag_-4_offset'] = Ammonia_Data['Ammonia_Flag'].shift(periods=-4)
Ammonia_Data['Ammonia_Flag_-3_offset'] = Ammonia_Data['Ammonia_Flag'].shift(periods=-3)
Ammonia_Data['Ammonia_Flag_-2_offset'] = Ammonia_Data['Ammonia_Flag'].shift(periods=-2)
Ammonia_Data['Ammonia_Flag_-1_offset'] = Ammonia_Data['Ammonia_Flag'].shift(periods=-1)
Ammonia_Data['Ammonia_Flag_+1_offset'] = Ammonia_Data['Ammonia_Flag'].shift(periods=1)
Ammonia_Data['Ammonia_Flag_+2_offset'] = Ammonia_Data['Ammonia_Flag'].shift(periods=2) 
Ammonia_Data['Ammonia_Flag_+3_offset'] = Ammonia_Data['Ammonia_Flag'].shift(periods=3)
Ammonia_Data['Ammonia_Flag_+4_offset'] = Ammonia_Data['Ammonia_Flag'].shift(periods=4)
Ammonia_Data['Ammonia_Flag_+5_offset'] = Ammonia_Data['Ammonia_Flag'].shift(periods=5)
Ammonia_Data['Ammonia_Flag_+6_offset'] = Ammonia_Data['Ammonia_Flag'].shift(periods=6)
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['Ammonia_Flag_-6_offset']!= 1),Ammonia_Data['Ammonia_Flag_-6_offset'],Ammonia_Data['Ammonia_Flag'])
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['Ammonia_Flag_-5_offset']!= 1),Ammonia_Data['Ammonia_Flag_-5_offset'],Ammonia_Data['Ammonia_Flag'])
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['Ammonia_Flag_-4_offset']!= 1),Ammonia_Data['Ammonia_Flag_-4_offset'],Ammonia_Data['Ammonia_Flag'])
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['Ammonia_Flag_-3_offset']!= 1),Ammonia_Data['Ammonia_Flag_-3_offset'],Ammonia_Data['Ammonia_Flag'])
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['Ammonia_Flag_-2_offset']!= 1),Ammonia_Data['Ammonia_Flag_-2_offset'],Ammonia_Data['Ammonia_Flag'])
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['Ammonia_Flag_-1_offset']!= 1),Ammonia_Data['Ammonia_Flag_-1_offset'],Ammonia_Data['Ammonia_Flag'])
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['Ammonia_Flag_+1_offset']!= 1),Ammonia_Data['Ammonia_Flag_+1_offset'],Ammonia_Data['Ammonia_Flag'])
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['Ammonia_Flag_+2_offset']!= 1),Ammonia_Data['Ammonia_Flag_+2_offset'],Ammonia_Data['Ammonia_Flag'])
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['Ammonia_Flag_+3_offset']!= 1),Ammonia_Data['Ammonia_Flag_+3_offset'],Ammonia_Data['Ammonia_Flag'])
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['Ammonia_Flag_+4_offset']!= 1),Ammonia_Data['Ammonia_Flag_+4_offset'],Ammonia_Data['Ammonia_Flag'])
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['Ammonia_Flag_+5_offset']!= 1),Ammonia_Data['Ammonia_Flag_+5_offset'],Ammonia_Data['Ammonia_Flag'])
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['Ammonia_Flag_+6_offset']!= 1),Ammonia_Data['Ammonia_Flag_+6_offset'],Ammonia_Data['Ammonia_Flag'])

Ammonia_Data['Ammonia_Flag'] = np.where(Ammonia_Data['NH3 (ppm)'].isnull() & Ammonia_Data['H2O (ppm) - NH3 analyser'].isnull(), 0, Ammonia_Data['Ammonia_Flag'])
Ammonia_Data.drop(Ammonia_Data[(Ammonia_Data['Ammonia_Flag'] == 0)].index,inplace =True)



GHG_Data['MultiCarbon_Flag'] = GHG_Data['MultiCarbon_Flag'].astype(str)
Ammonia_Data['Ammonia_Flag'] = Ammonia_Data['Ammonia_Flag'].astype(str)

GHG_Data['CH4 (ppm)'] = GHG_Data['CH4 (ppm) perlim']
GHG_Data['CO2 (ppm)'] = GHG_Data['CO2 (ppm) perlim']
GHG_Data['CO (ppm)'] = GHG_Data['CO (ppm) perlim']
Ammonia_Data['NH3 (ppm)'] = Ammonia_Data['NH3 (ppm) perlim']

start_Simon_1 = datetime.datetime(2018,12,18,0,0,00) # logging in simon building
end_Simon_1 = datetime.datetime(2019,1,29,12,37,00) 
#GHG_Data.loc[start_Simon_1:end_Simon_1, ('MultiCarbon_Flag')] = "3"
#Ammonia_Data.loc[start_Simon_1:end_Simon_1, ('Ammonia_Flag')] = "3"

start_move_1 = datetime.datetime(2019,1,29,12,38,00) # moving to firs
end_move_1 = datetime.datetime(2019,1,29,23,32,00)
GHG_Data.loc[start_move_1:end_move_1, ('MultiCarbon_Flag')] = "3"
Ammonia_Data.loc[start_move_1:end_move_1, ('Ammonia_Flag')] = "3"

start_move_2 = datetime.datetime(2019,6,12,7,10,00) # logging in simon building
end_move_2 = datetime.datetime(2019,6,12,21,51,00)
GHG_Data.loc[start_move_2:end_move_2, ('MultiCarbon_Flag')] = "3"
Ammonia_Data.loc[start_move_2:end_move_2, ('Ammonia_Flag')] = "3"

start_flowCheck_1 = datetime.datetime(2019,8,8,13,45,00) # measuring flow on ammonia analyser
end_flowCheck_1 = datetime.datetime(2019,8,8,14,55,00) 
Ammonia_Data.loc[start_flowCheck_1:end_flowCheck_1, 'Ammonia_Flag'] = "3"

start_flowCheck_2 = datetime.datetime(2019,8,8,14,55,00) # measuring flow on multicarbon analyser, change over and retried in 15.20
end_flowCheck_2 = datetime.datetime(2019,8,8,15,44,00) 
GHG_Data.loc[start_flowCheck_2:end_flowCheck_2, ('Multicarbon_Flag')] = "3"

start_calibration_1 = datetime.datetime(2019,8,9,7,30,00) # NPL audit of site - time needs checking
end_calibration_1 = datetime.datetime(2019,8,9,10,00,00)
GHG_Data.loc[start_calibration_1:end_calibration_1, ('MultiCarbon_Flag')] = "0"

start_flowCheck_3 = datetime.datetime(2019,8,9,15,0,00) #NH4 bypass check
end_flowCheck_3 = datetime.datetime(2019,8,9,16,0,00)
GHG_Data.loc[start_flowCheck_3:end_flowCheck_3, ('MultiCarbon_Flag')] = "3"
Ammonia_Data.loc[start_flowCheck_3:end_flowCheck_3, ('Ammonia_Flag')] = "3"

start_outage1 = datetime.datetime(2019,8,19,15,5,00) #Site shut down started due to planned power outage till the 21-08-2019
end_outage1 = datetime.datetime(2019,8,21,9,35,00)
GHG_Data.loc[start_outage1:end_outage1, ('MultiCarbon_Flag')] = "3"
Ammonia_Data.loc[start_outage1:end_outage1, ('Ammonia_Flag')] = "3"

start_calibration_2 = datetime.datetime(2019,8,9,13,00,00) #Multicarbon analyser on to compressed air cylinder
end_calibration_2 = datetime.datetime(2019,8,9,13,30,00)
GHG_Data.loc[start_calibration_2:end_calibration_2, ('MultiCarbon_Flag')] = "0"

start_outage2 = datetime.datetime(2019,8,22,17,40,00) #Computer restarted and program not restarted till 05-09-2019
end_outage2 = datetime.datetime(2019,9,5,13,42,00)
GHG_Data.loc[start_outage2:end_outage2, ('MultiCarbon_Flag')] = "3"
Ammonia_Data.loc[start_outage2:end_outage2, ('Ammonia_Flag')] = "3"

start_calibration_3 = datetime.datetime(2019,9,5,14,17,00) # Multicarbon onto cylinder reading
end_calibration_3 = datetime.datetime(2019,9,5,14,51,00)
GHG_Data.loc[start_calibration_3:end_calibration_3, ('MultiCarbon_Flag')] = "0"

start_calibration_4 = datetime.datetime(2019,9,6,14,18,00) # Multicarbon onto cylinder reading
end_calibration_4 = datetime.datetime(2019,9,6,14,40,00)
GHG_Data.loc[start_calibration_4:end_calibration_4, ('Multicarbon_Flag')] = "0"

start_calibration_5 = datetime.datetime(2019,9,10,14,19,00) # Multicarbon onto cylinder reading
end_calibration_5 = datetime.datetime(2019,9,10,14,36,00)
GHG_Data.loc[start_calibration_5:end_calibration_5, ('MultiCarbon_Flag')] = "0"

start_calibration_6 = datetime.datetime(2019,9,17,11,5,00) # Multicarbon onto cylinder reading
end_calibration_6 = datetime.datetime(2019,9,17,11,16,00)
GHG_Data.loc[start_calibration_6:end_calibration_6, ('Multicarbon_Flag')] = "0"

start_software_1 = datetime.datetime(2019,9,24,11,26,00) #significant glitching on NH3 data
end_software_1 = datetime.datetime(2019,9,24,15,6,00)
Ammonia_Data.loc[start_software_1:end_software_1, ('Ammonia_Flag')] = "0"

start_software_2 = datetime.datetime(2019,9,25,11,29,00) #glitching was back again
end_software_2 = datetime.datetime(2019,9,25,16,2,00)
Ammonia_Data.loc[start_software_2:end_software_2, ('Ammonia_Flag')] = "0"

start_calibration_7 = datetime.datetime(2019,9,26,8,24,00) # Multicarbon gas cal check
end_calibration_7 = datetime.datetime(2019,9,26,8,54,00)
GHG_Data.loc[start_calibration_7:end_calibration_7, ('Multicarbon_Flag')] = "0"

start_calibration_8 = datetime.datetime(2019,10,2,14,10,00) # Multicarbon gas cal check
end_calibration_8 = datetime.datetime(2019,10,2,14,30,00)
GHG_Data.loc[start_calibration_8:end_calibration_8, ('Multicarbon_Flag')] = "0"

start_calibration_9 = datetime.datetime(2019,10,9,13,45,00) # Multicarbon gas cal check
end_calibration_9 = datetime.datetime(2019,10,9,14,0,00)
GHG_Data.loc[start_calibration_9:end_calibration_9, ('Multicarbon_Flag')] = "0"

start_calibration_10 = datetime.datetime(2019,10,15,12,50,00) # Multicarbon gas cal check
end_calibration_10 = datetime.datetime(2019,10,15,13,10,00)
GHG_Data.loc[start_calibration_10:end_calibration_10, ('Multicarbon_Flag')] = "0"

start_calibration_11 = datetime.datetime(2019,10,24,8,5,00) # Multicarbon gas cal check
end_calibration_11 = datetime.datetime(2019,10,24,8,30,00)
GHG_Data.loc[start_calibration_11:end_calibration_11, ('Multicarbon_Flag')] = "0"

start_calibration_12 = datetime.datetime(2019,10,31,11,5,00) # Multicarbon gas cal check
end_calibration_12 = datetime.datetime(2019,10,31,11,25,00)
GHG_Data.loc[start_calibration_12:end_calibration_12, ('Multicarbon_Flag')] = "0"

start_AmmoniaZero_1_1 = datetime.datetime(2021,7,26,15,45,00)
end_AmmoniaZero_1_1 = datetime.datetime(2021,7,27,12,50,00)
Ammonia_Data.loc[start_AmmoniaZero_1_1:end_AmmoniaZero_1_1, ('Ammonia_Flag')] = "0"

start_AmmoniaZero_1_2 = datetime.datetime(2021,7,30,12,00,00) 
end_AmmoniaZero_1_2 = datetime.datetime(2021,7,30,13,30,00)
Ammonia_Data.loc[start_AmmoniaZero_1_2:end_AmmoniaZero_1_2, ('Ammonia_Flag')] = "0"

start_AmmoniaZero_2 = datetime.datetime(2022,5,4,12,35,00)
end_AmmoniaZero_2 = datetime.datetime(2022,5,5,9,45,00)
Ammonia_Data.loc[start_AmmoniaZero_2:end_AmmoniaZero_2, ('Ammonia_Flag')] = "0"

start_Audit_1 = datetime.datetime(2019,8,9,7,30,00) # Multicarbon gas cal check
end_Audit_1 = datetime.datetime(2019,8,9,10,30,00)
GHG_Data.loc[start_Audit_1:end_Audit_1, ('Multicarbon_Flag')] = "0"

start_Audit_2 = datetime.datetime(2020,3,18,10,0,00) 
end_Audit_2 = datetime.datetime(2020,3,18,13,30,00)
GHG_Data.loc[start_Audit_2:end_Audit_2, ('Multicarbon_Flag')] = "0"

start_Audit_3 = datetime.datetime(2020,10,2,7,30,00) 
end_Audit_3 = datetime.datetime(2020,10,2,8,30,00)
GHG_Data.loc[start_Audit_3:end_Audit_3, ('Multicarbon_Flag')] = "0"

start_Audit_4 = datetime.datetime(2021,3,30,8,15,00) 
end_Audit_4 = datetime.datetime(2021,3,30,10,15,00)
GHG_Data.loc[start_Audit_2:end_Audit_2, ('Multicarbon_Flag')] = "0"

start_Audit_5 = datetime.datetime(2021,10,27,9,30,00) 
end_Audit_5 = datetime.datetime(2021,10,27,10,45,00)
GHG_Data.loc[start_Audit_3:end_Audit_3, ('Multicarbon_Flag')] = "0"

start_Audit_6 = datetime.datetime(2022,5,4,9,15,00) 
end_Audit_6 = datetime.datetime(2022,5,4,10,15,00)
GHG_Data.loc[start_Audit_2:end_Audit_2, ('Multicarbon_Flag')] = "0"

start_Flow_1 = datetime.datetime(2019,1,10,16,5,00) # Multicarbon gas cal check
end_Flow_1 = datetime.datetime(2019,1,10,16,20,00)
GHG_Data.loc[start_Flow_1:end_Flow_1, ('Multicarbon_Flag')] = "0"
Ammonia_Data.loc[start_Flow_1:end_Flow_1, ('Ammonia_Flag')] = "0"

start_Flow_2 = datetime.datetime(2019,1,29,13,0,00) # Multicarbon gas cal check
end_Flow_2 = datetime.datetime(2019,1,29,18,0,00)
Ammonia_Data.loc[start_Flow_2:end_Flow_2, ('Ammonia_Flag')] = "0"

start_Flow_3 = datetime.datetime(2019,4,14,7,15,00) # Multicarbon gas cal check
end_Flow_3 = datetime.datetime(2019,4,14,9,30,00)
GHG_Data.loc[start_Flow_3:end_Flow_3, ('Multicarbon_Flag')] = "0"

start_Flow_4 = datetime.datetime(2019,5,16,10,45,00) 
end_Flow_4 = datetime.datetime(2019,5,16,11,25,00)
Ammonia_Data.loc[start_Flow_4:end_Flow_4, ('Ammonia_Flag')] = "0"

start_Flow_5 = datetime.datetime(2019,8,8,13,31,00) 
end_Flow_5 = datetime.datetime(2019,8,8,13,37,00)
Ammonia_Data.loc[start_Flow_5:end_Flow_5, ('Ammonia_Flag')] = "0"

start_Flow_6 = datetime.datetime(2019,8,8,14,45,00) 
end_Flow_6 = datetime.datetime(2019,8,8,16,0,00)
GHG_Data.loc[start_Flow_6:end_Flow_6, ('Multicarbon_Flag')] = "0"
Ammonia_Data.loc[start_Flow_6:end_Flow_6, ('Ammonia_Flag')] = "0"

start_Flow_6 = datetime.datetime(2019,8,9,6,0,00) 
end_Flow_6 = datetime.datetime(2019,8,9,17,0,00)
GHG_Data.loc[start_Flow_6:end_Flow_6, ('Multicarbon_Flag')] = "0"
Ammonia_Data.loc[start_Flow_6:end_Flow_6, ('Ammonia_Flag')] = "0"

start_Flow_7 = datetime.datetime(2019,8,22,13,0,00) 
end_Flow_7 = datetime.datetime(2019,8,22,13,30,00)
GHG_Data.loc[start_Flow_7:end_Flow_7, ('Multicarbon_Flag')] = "0"

start_Flow_8 = datetime.datetime(2019,8,19,18,30,00) 
end_Flow_8 = datetime.datetime(2019,8,19,18,50,00)
GHG_Data.loc[start_Flow_8:end_Flow_8, ('Multicarbon_Flag')] = "0"

start_Flow_9 = datetime.datetime(2019,6,17,12,0,00) 
end_Flow_9 = datetime.datetime(2019,6,18,12,0,00)
Ammonia_Data.loc[start_Flow_9:end_Flow_9, ('Ammonia_Flag')] = "3"

start_Flow_10 = datetime.datetime(2019,8,21,8,0,00) 
end_Flow_10 = datetime.datetime(2019,6,22,8,0,00)
Ammonia_Data.loc[start_Flow_10:end_Flow_10, ('Ammonia_Flag')] = "3"

start_Cal_Check_1 = datetime.datetime(2019,10,28,14,30,00) 
end_Cal_Check_1 = datetime.datetime(2019,10,28,14,50,00)
GHG_Data.loc[start_Cal_Check_1:end_Cal_Check_1, ('Multicarbon_Flag')] = "0"

start_Startup_1 = datetime.datetime(2020,3,12,9,30,00) 
end_Startup_1 = datetime.datetime(2020,3,12,9,40,00)
Ammonia_Data.loc[start_Startup_1:end_Startup_1, ('Ammonia_Flag')] = "0"

start_Startup_2 = datetime.datetime(2020,5,11,11,30,00) 
end_Startup_2 = datetime.datetime(2020,5,11,11,50,00)
Ammonia_Data.loc[start_Startup_2:end_Startup_1, ('Ammonia_Flag')] = "0"

start_Cal_Check_2 = datetime.datetime(2020,5,11,11,20,00) 
end_Cal_Check_2 = datetime.datetime(2020,5,11,11,50,00)
GHG_Data.loc[start_Cal_Check_2:end_Cal_Check_2, ('Multicarbon_Flag')] = "0"

start_Cal_Check_3 = datetime.datetime(2020,5,22,8,30,00) 
end_Cal_Check_3 = datetime.datetime(2020,5,22,11,30,00)
GHG_Data.loc[start_Cal_Check_3:end_Cal_Check_3, ('Multicarbon_Flag')] = "0"

start_Cal_Check_4 = datetime.datetime(2020,6,2,10,15,00) 
end_Cal_Check_4 = datetime.datetime(2020,6,2,11,20,00)
GHG_Data.loc[start_Cal_Check_4:end_Cal_Check_4, ('Multicarbon_Flag')] = "0"

start_Cal_Check_5 = datetime.datetime(2020,6,9,10,0,00) 
end_Cal_Check_5 = datetime.datetime(2020,6,9,10,40,00)
GHG_Data.loc[start_Cal_Check_5:end_Cal_Check_5, ('Multicarbon_Flag')] = "0"

start_Cal_Check_6 = datetime.datetime(2020,6,16,9,0,00) 
end_Cal_Check_6 = datetime.datetime(2020,6,16,11,15,00)
GHG_Data.loc[start_Cal_Check_6:end_Cal_Check_6, ('Multicarbon_Flag')] = "0"

start_Cal_Check_7 = datetime.datetime(2020,6,24,10,50,00) 
end_Cal_Check_7 = datetime.datetime(2020,6,24,12,20,00)
GHG_Data.loc[start_Cal_Check_7:end_Cal_Check_7, ('Multicarbon_Flag')] = "0"

start_Cal_Check_8 = datetime.datetime(2020,7,2,9,30,00) 
end_Cal_Check_8 = datetime.datetime(2020,7,2,10,30,00)
GHG_Data.loc[start_Cal_Check_8:end_Cal_Check_8, ('Multicarbon_Flag')] = "0"

start_Cal_Check_9 = datetime.datetime(2020,7,8,14,30,00) 
end_Cal_Check_9 = datetime.datetime(2020,7,8,15,10,00)
GHG_Data.loc[start_Cal_Check_9:end_Cal_Check_9, ('Multicarbon_Flag')] = "0"

start_Cal_Check_10 = datetime.datetime(2020,7,17,12,10,00) 
end_Cal_Check_10 = datetime.datetime(2020,7,17,13,10,00)
GHG_Data.loc[start_Cal_Check_10:end_Cal_Check_10, ('Multicarbon_Flag')] = "0"

start_Cal_Check_11 = datetime.datetime(2020,7,23,8,30,00) 
end_Cal_Check_11 = datetime.datetime(2020,7,23,9,20,00)
GHG_Data.loc[start_Cal_Check_11:end_Cal_Check_11, ('Multicarbon_Flag')] = "0"

start_Cal_Check_12 = datetime.datetime(2020,8,11,12,30,00) 
end_Cal_Check_12 = datetime.datetime(2020,8,11,13,15,00)
GHG_Data.loc[start_Cal_Check_12:end_Cal_Check_12, ('Multicarbon_Flag')] = "0"

start_Cal_Check_13 = datetime.datetime(2020,8,12,13,0,00) 
end_Cal_Check_13 = datetime.datetime(2020,8,12,16,40,00)
GHG_Data.loc[start_Cal_Check_13:end_Cal_Check_13, ('Multicarbon_Flag')] = "0"

start_Cal_Check_14 = datetime.datetime(2020,8,20,7,35,00) 
end_Cal_Check_14 = datetime.datetime(2020,8,20,8,0,00)
GHG_Data.loc[start_Cal_Check_14:end_Cal_Check_14, ('Multicarbon_Flag')] = "0"

start_Cal_Check_15 = datetime.datetime(2020,8,26,9,30,00) 
end_Cal_Check_15 = datetime.datetime(2020,8,26,11,0,00)
GHG_Data.loc[start_Cal_Check_15:end_Cal_Check_15, ('Multicarbon_Flag')] = "0"

start_Startup_3 = datetime.datetime(2020,8,12,12,0,00) 
end_Startup_3 = datetime.datetime(2020,8,13,4,0,00)
Ammonia_Data.loc[start_Startup_3:end_Startup_3, ('Ammonia_Flag')] = "0"

start_Cal_Check_16 = datetime.datetime(2020,9,4,10,20,00) 
end_Cal_Check_16 = datetime.datetime(2020,9,4,11,30,00)
GHG_Data.loc[start_Cal_Check_16:end_Cal_Check_16, ('Multicarbon_Flag')] = "0"

start_Cal_Check_16 = datetime.datetime(2020,9,11,8,50,00) 
end_Cal_Check_16 = datetime.datetime(2020,9,11,9,30,00)
GHG_Data.loc[start_Cal_Check_16:end_Cal_Check_16, ('Multicarbon_Flag')] = "0"

start_Cal_Check_16 = datetime.datetime(2020,9,25,9,10,00) 
end_Cal_Check_16 = datetime.datetime(2020,9,25,10,35,00)
GHG_Data.loc[start_Cal_Check_16:end_Cal_Check_16, ('Multicarbon_Flag')] = "0"

start_Flow_11 = datetime.datetime(2021,1,29,9,0,00) 
end_Flow_11 = datetime.datetime(2021,1,29,12,0,00)
Ammonia_Data.loc[start_Flow_11:end_Flow_11, ('Ammonia_Flag')] = "0"

start_Flow_12 = datetime.datetime(2021,6,3,8,0,00) 
end_Flow_12 = datetime.datetime(2021,6,4,4,0,00)
Ammonia_Data.loc[start_Flow_12:end_Flow_12, ('Ammonia_Flag')] = "0"

start_Flow_13 = datetime.datetime(2021,6,30,8,0,00) 
end_Flow_13 = datetime.datetime(2021,7,1,12,0,00)
Ammonia_Data.loc[start_Flow_13:end_Flow_13, ('Ammonia_Flag')] = "0"

start_Flow_14 = datetime.datetime(2022,6,27,8,0,00) 
end_Flow_14 = datetime.datetime(2022,6,27,12,0,00)
#Ammonia_Data.loc[start_Flow_14:end_Flow_14, ('Ammonia_Flag')] = "0"

start_Flow_14 = datetime.datetime(2021,6,1,0,0,00)#the flow on this multicarbon data is off so i have removed the most extreme data and flagged the rest
end_Flow_14 = datetime.datetime(2021,6,21,18,0,00)
flow_14_data = GHG_Data[start_Flow_14:end_Flow_14]
flow_14_data['Multicarbon_Flag'] = np.where(flow_14_data['CH4 (ppm)'] <1.9 , "0", "3") 
flow_14_data['Multicarbon_Flag'] = np.where(flow_14_data['CO2 (ppm)'] >500 , "0", flow_14_data['Multicarbon_Flag']) 
flow_14_data['Multicarbon_Flag'] = np.where(flow_14_data['CO2 (ppm)'] <400 , "0", flow_14_data['Multicarbon_Flag']) 
flow_14_flag = flow_14_data['Multicarbon_Flag']
GHG_Data.loc[start_Flow_14:end_Flow_14, ('Multicarbon_Flag')] = flow_14_flag

start_Flow_15 = datetime.datetime(2021,8,13,16,30,00) 
end_Flow_15 = datetime.datetime(2021,8,13,16,50,00)
Ammonia_Data.loc[start_Flow_15:end_Flow_15, ('Ammonia_Flag')] = "0"

start_Flow_16 = datetime.datetime(2021,10,27,9,0,00) 
end_Flow_16 = datetime.datetime(2021,10,28,4,0,00)
Ammonia_Data.loc[start_Flow_16:end_Flow_16, ('Ammonia_Flag')] = "0"

start_Flow_17 = datetime.datetime(2022,1,20,0,0,00)#the flow on this multicarbon data is off so i have removed the most extreme data and flagged the rest
end_Flow_17 = datetime.datetime(2022,2,20,0,0,00)
flow_17_data = GHG_Data[start_Flow_17:end_Flow_17]
flow_17_data['Multicarbon_Flag'] = np.where(flow_17_data['CH4 (ppm)'] <1.95 , "0", "1") 
#flow_17_data['Multicarbon_Flag'] = np.where(flow_17_data['CO2 (ppm)'] >500 , "0", flow_17_data['Multicarbon_Flag']) 
flow_17_data['Multicarbon_Flag'] = np.where(flow_17_data['CO2 (ppm)'] <405 , "0", flow_17_data['Multicarbon_Flag']) 
flow_17_flag = flow_17_data['Multicarbon_Flag']
GHG_Data.loc[start_Flow_17:end_Flow_17, ('Multicarbon_Flag')] = flow_17_flag

start_CH4_Cal_1 = datetime.datetime(2022,2,4,12,30,00) 
end_CH4_Cal_1 = datetime.datetime(2022,2,4,13,10,00)
GHG_Data.loc[start_CH4_Cal_1:end_CH4_Cal_1, ('Multicarbon_Flag')] = "0"

start_CO_Cal_1 = datetime.datetime(2022,3,1,8,30,00) 
end_CO_Cal_1 = datetime.datetime(2022,3,1,12,10,00)
GHG_Data.loc[start_CO_Cal_1:end_CO_Cal_1, ('Multicarbon_Flag')] = "0"

GHG_Data.drop(GHG_Data[(GHG_Data['Multicarbon_Flag'] == "0")].index,inplace =True)
Ammonia_Data.drop(Ammonia_Data[(Ammonia_Data['Ammonia_Flag'] == "0")].index,inplace =True)

GHG_Data['CO (ppm)'] = GHG_Data['CO (ppm)']*1000
GHG_Data.rename(columns={'CO (ppm)': 'CO (ppb)','H2O (ppm) - MultiCarbon analyser': 'H2O (ppm)' }, inplace = True)

GHG_Data['CH4_qc_flags']=np.nan
GHG_Data['CH4_qc_flags']=np.where(GHG_Data['CH4 (ppm)']>1.5, '1','3') 
GHG_Data['CH4_qc_flags']=np.where(GHG_Data['CH4 (ppm)']>30, '3', GHG_Data['CH4_qc_flags']) 
GHG_Data['CH4_qc_flags']=np.where((GHG_Data['MultiCarbon_Flag'] == '3'), '3', GHG_Data['CH4_qc_flags']) 
#GHG_Data['CH4_qc_flags']=np.where(GHG_Data['CH4 (ppm)']>0.0003, GHG_Data['CH4_qc_flags'], '2') 
#GHG_Data['CH4_qc_flags']=np.where(GHG_Data['CH4 (ppm)']>100, '2', GHG_Data['CH4_qc_flags']) 

GHG_Data['H2O_qc_flags']=np.nan
GHG_Data['H2O_qc_flags']=np.where(GHG_Data['H2O (ppm)']>20, '1','3') 
GHG_Data['H2O_qc_flags']=np.where(GHG_Data['H2O (ppm)']>70000, '3', GHG_Data['H2O_qc_flags']) 
GHG_Data['H2O_qc_flags']=np.where((GHG_Data['MultiCarbon_Flag'] == '3'), '3', GHG_Data['H2O_qc_flags'])
#GHG_Data['H2O_qc_flags']=np.where(GHG_Data['H2O (ppm)']>20, GHG_Data['H2O_qc_flags'],'2') 
#GHG_Data['H2O_qc_flags']=np.where(GHG_Data['H2O (ppm)']>70000, '2', GHG_Data['H2O_qc_flags']) 

GHG_Data['CO2_qc_flags']=np.nan
GHG_Data['CO2_qc_flags'] = np.where(GHG_Data['CO2 (ppm)']>350, '1','3') 
GHG_Data['CO2_qc_flags'] = np.where(GHG_Data['CO2 (ppm)']>1000, '3', GHG_Data['CO2_qc_flags']) 
GHG_Data['CO2_qc_flags']=np.where((GHG_Data['MultiCarbon_Flag'] == '3'), '3', GHG_Data['CO2_qc_flags'])
#GHG_Data['CO2_qc_flags'] = np.where(GHG_Data['CO2 (ppm)']>0.1, GHG_Data['CO2_qc_flags'],'2') 
#GHG_Data['CO2_qc_flags'] = np.where(GHG_Data['CO2 (ppm)']>3000, '2', GHG_Data['CO2_qc_flags']) 

GHG_Data['CO_qc_flags']=np.nan
GHG_Data['CO_qc_flags']=np.where((GHG_Data['CO (ppb)']>5), '1', '3') 
GHG_Data['CO_qc_flags']=np.where(GHG_Data['CO (ppb)']>2000,'3',GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags']=np.where((GHG_Data['MultiCarbon_Flag'] == '3'), '3', GHG_Data['CO_qc_flags'])
#GHG_Data['CO_qc_flags']=np.where((GHG_Data['CO (ppb)']>-5), GHG_Data['CO_qc_flags'], '2') 
#GHG_Data['CO_qc_flags']=np.where(GHG_Data['CO (ppb)']>100000,'2', GHG_Data['CO_qc_flags'])

GHG_Data['CH4_qc_flags_-6_offset'] = GHG_Data['CH4_qc_flags'].shift(periods=-6)
GHG_Data['CH4_qc_flags_-5_offset'] = GHG_Data['CH4_qc_flags'].shift(periods=-5)
GHG_Data['CH4_qc_flags_-4_offset'] = GHG_Data['CH4_qc_flags'].shift(periods=-4)
GHG_Data['CH4_qc_flags_-3_offset'] = GHG_Data['CH4_qc_flags'].shift(periods=-3)
GHG_Data['CH4_qc_flags_-2_offset'] = GHG_Data['CH4_qc_flags'].shift(periods=-2)
GHG_Data['CH4_qc_flags_-1_offset'] = GHG_Data['CH4_qc_flags'].shift(periods=-1)
GHG_Data['CH4_qc_flags_+1_offset'] = GHG_Data['CH4_qc_flags'].shift(periods=1)
GHG_Data['CH4_qc_flags_+2_offset'] = GHG_Data['CH4_qc_flags'].shift(periods=2)
GHG_Data['CH4_qc_flags_+3_offset'] = GHG_Data['CH4_qc_flags'].shift(periods=3)
GHG_Data['CH4_qc_flags_+4_offset'] = GHG_Data['CH4_qc_flags'].shift(periods=4)
GHG_Data['CH4_qc_flags_+5_offset'] = GHG_Data['CH4_qc_flags'].shift(periods=5)
GHG_Data['CH4_qc_flags_+6_offset'] = GHG_Data['CH4_qc_flags'].shift(periods=6)
GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags_-6_offset']>'1'),GHG_Data['CH4_qc_flags_-6_offset'],GHG_Data['CH4_qc_flags'])
GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags_-5_offset']>'1'),GHG_Data['CH4_qc_flags_-5_offset'],GHG_Data['CH4_qc_flags'])
GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags_-4_offset']>'1'),GHG_Data['CH4_qc_flags_-4_offset'],GHG_Data['CH4_qc_flags'])
GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags_-3_offset']>'1'),GHG_Data['CH4_qc_flags_-3_offset'],GHG_Data['CH4_qc_flags'])
GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags_-2_offset']>'1'),GHG_Data['CH4_qc_flags_-2_offset'],GHG_Data['CH4_qc_flags'])
GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags_-1_offset']>'1'),GHG_Data['CH4_qc_flags_-1_offset'],GHG_Data['CH4_qc_flags'])
GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags_+1_offset']>'1'),GHG_Data['CH4_qc_flags_+1_offset'],GHG_Data['CH4_qc_flags'])
GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags_+2_offset']>'1'),GHG_Data['CH4_qc_flags_+2_offset'],GHG_Data['CH4_qc_flags'])
GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags_+3_offset']>'1'),GHG_Data['CH4_qc_flags_+3_offset'],GHG_Data['CH4_qc_flags'])
GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags_+4_offset']>'1'),GHG_Data['CH4_qc_flags_+4_offset'],GHG_Data['CH4_qc_flags'])
GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags_+5_offset']>'1'),GHG_Data['CH4_qc_flags_+5_offset'],GHG_Data['CH4_qc_flags'])
GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags_+6_offset']>'1'),GHG_Data['CH4_qc_flags_+6_offset'],GHG_Data['CH4_qc_flags'])

GHG_Data['H2O_qc_flags_-6_offset'] = GHG_Data['H2O_qc_flags'].shift(periods=-6)
GHG_Data['H2O_qc_flags_-5_offset'] = GHG_Data['H2O_qc_flags'].shift(periods=-5)
GHG_Data['H2O_qc_flags_-4_offset'] = GHG_Data['H2O_qc_flags'].shift(periods=-4)
GHG_Data['H2O_qc_flags_-3_offset'] = GHG_Data['H2O_qc_flags'].shift(periods=-3)
GHG_Data['H2O_qc_flags_-2_offset'] = GHG_Data['H2O_qc_flags'].shift(periods=-2)
GHG_Data['H2O_qc_flags_-1_offset'] = GHG_Data['H2O_qc_flags'].shift(periods=-1)
GHG_Data['H2O_qc_flags_+1_offset'] = GHG_Data['H2O_qc_flags'].shift(periods=1)
GHG_Data['H2O_qc_flags_+2_offset'] = GHG_Data['H2O_qc_flags'].shift(periods=2)
GHG_Data['H2O_qc_flags_+3_offset'] = GHG_Data['H2O_qc_flags'].shift(periods=3)
GHG_Data['H2O_qc_flags_+4_offset'] = GHG_Data['H2O_qc_flags'].shift(periods=4)
GHG_Data['H2O_qc_flags_+5_offset'] = GHG_Data['H2O_qc_flags'].shift(periods=5)
GHG_Data['H2O_qc_flags_+6_offset'] = GHG_Data['H2O_qc_flags'].shift(periods=6)
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags_-6_offset']>'1'),GHG_Data['H2O_qc_flags_-6_offset'],GHG_Data['H2O_qc_flags'])
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags_-5_offset']>'1'),GHG_Data['H2O_qc_flags_-5_offset'],GHG_Data['H2O_qc_flags'])
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags_-4_offset']>'1'),GHG_Data['H2O_qc_flags_-4_offset'],GHG_Data['H2O_qc_flags'])
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags_-3_offset']>'1'),GHG_Data['H2O_qc_flags_-3_offset'],GHG_Data['H2O_qc_flags'])
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags_-2_offset']>'1'),GHG_Data['H2O_qc_flags_-2_offset'],GHG_Data['H2O_qc_flags'])
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags_-1_offset']>'1'),GHG_Data['H2O_qc_flags_-1_offset'],GHG_Data['H2O_qc_flags'])
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags_+1_offset']>'1'),GHG_Data['H2O_qc_flags_+1_offset'],GHG_Data['H2O_qc_flags'])
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags_+2_offset']>'1'),GHG_Data['H2O_qc_flags_+2_offset'],GHG_Data['H2O_qc_flags'])
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags_+3_offset']>'1'),GHG_Data['H2O_qc_flags_+3_offset'],GHG_Data['H2O_qc_flags'])
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags_+4_offset']>'1'),GHG_Data['H2O_qc_flags_+4_offset'],GHG_Data['H2O_qc_flags'])
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags_+5_offset']>'1'),GHG_Data['H2O_qc_flags_+5_offset'],GHG_Data['H2O_qc_flags'])
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags_+6_offset']>'1'),GHG_Data['H2O_qc_flags_+6_offset'],GHG_Data['H2O_qc_flags'])

GHG_Data['CO2_qc_flags_-6_offset'] = GHG_Data['CO2_qc_flags'].shift(periods=-6)
GHG_Data['CO2_qc_flags_-5_offset'] = GHG_Data['CO2_qc_flags'].shift(periods=-5)
GHG_Data['CO2_qc_flags_-4_offset'] = GHG_Data['CO2_qc_flags'].shift(periods=-4)
GHG_Data['CO2_qc_flags_-3_offset'] = GHG_Data['CO2_qc_flags'].shift(periods=-3)
GHG_Data['CO2_qc_flags_-2_offset'] = GHG_Data['CO2_qc_flags'].shift(periods=-2)
GHG_Data['CO2_qc_flags_-1_offset'] = GHG_Data['CO2_qc_flags'].shift(periods=-1)
GHG_Data['CO2_qc_flags_+1_offset'] = GHG_Data['CO2_qc_flags'].shift(periods=1)
GHG_Data['CO2_qc_flags_+2_offset'] = GHG_Data['CO2_qc_flags'].shift(periods=2)
GHG_Data['CO2_qc_flags_+3_offset'] = GHG_Data['CO2_qc_flags'].shift(periods=3)
GHG_Data['CO2_qc_flags_+4_offset'] = GHG_Data['CO2_qc_flags'].shift(periods=4)
GHG_Data['CO2_qc_flags_+5_offset'] = GHG_Data['CO2_qc_flags'].shift(periods=5)
GHG_Data['CO2_qc_flags_+6_offset'] = GHG_Data['CO2_qc_flags'].shift(periods=6)
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags_-6_offset']>'1'),GHG_Data['CO2_qc_flags_-6_offset'],GHG_Data['CO2_qc_flags'])
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags_-5_offset']>'1'),GHG_Data['CO2_qc_flags_-5_offset'],GHG_Data['CO2_qc_flags'])
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags_-4_offset']>'1'),GHG_Data['CO2_qc_flags_-4_offset'],GHG_Data['CO2_qc_flags'])
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags_-3_offset']>'1'),GHG_Data['CO2_qc_flags_-3_offset'],GHG_Data['CO2_qc_flags'])
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags_-2_offset']>'1'),GHG_Data['CO2_qc_flags_-2_offset'],GHG_Data['CO2_qc_flags'])
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags_-1_offset']>'1'),GHG_Data['CO2_qc_flags_-1_offset'],GHG_Data['CO2_qc_flags'])
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags_+1_offset']>'1'),GHG_Data['CO2_qc_flags_+1_offset'],GHG_Data['CO2_qc_flags'])
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags_+2_offset']>'1'),GHG_Data['CO2_qc_flags_+2_offset'],GHG_Data['CO2_qc_flags'])
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags_+3_offset']>'1'),GHG_Data['CO2_qc_flags_+3_offset'],GHG_Data['CO2_qc_flags'])
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags_+4_offset']>'1'),GHG_Data['CO2_qc_flags_+4_offset'],GHG_Data['CO2_qc_flags'])
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags_+5_offset']>'1'),GHG_Data['CO2_qc_flags_+5_offset'],GHG_Data['CO2_qc_flags'])
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags_+6_offset']>'1'),GHG_Data['CO2_qc_flags_+6_offset'],GHG_Data['CO2_qc_flags'])

GHG_Data['CO_qc_flags_-6_offset'] = GHG_Data['CO_qc_flags'].shift(periods=-6)
GHG_Data['CO_qc_flags_-5_offset'] = GHG_Data['CO_qc_flags'].shift(periods=-5)
GHG_Data['CO_qc_flags_-4_offset'] = GHG_Data['CO_qc_flags'].shift(periods=-4)
GHG_Data['CO_qc_flags_-3_offset'] = GHG_Data['CO_qc_flags'].shift(periods=-3)
GHG_Data['CO_qc_flags_-2_offset'] = GHG_Data['CO_qc_flags'].shift(periods=-2)
GHG_Data['CO_qc_flags_-1_offset'] = GHG_Data['CO_qc_flags'].shift(periods=-1)
GHG_Data['CO_qc_flags_+1_offset'] = GHG_Data['CO_qc_flags'].shift(periods=1)
GHG_Data['CO_qc_flags_+2_offset'] = GHG_Data['CO_qc_flags'].shift(periods=2)
GHG_Data['CO_qc_flags_+3_offset'] = GHG_Data['CO_qc_flags'].shift(periods=3)
GHG_Data['CO_qc_flags_+4_offset'] = GHG_Data['CO_qc_flags'].shift(periods=4)
GHG_Data['CO_qc_flags_+5_offset'] = GHG_Data['CO_qc_flags'].shift(periods=5)
GHG_Data['CO_qc_flags_+6_offset'] = GHG_Data['CO_qc_flags'].shift(periods=6)
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_-6_offset']>'1'),GHG_Data['CO_qc_flags_-6_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_-5_offset']>'1'),GHG_Data['CO_qc_flags_-5_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_-4_offset']>'1'),GHG_Data['CO_qc_flags_-4_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_-3_offset']>'1'),GHG_Data['CO_qc_flags_-3_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_-4_offset']>'1'),GHG_Data['CO_qc_flags_-4_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_-3_offset']>'1'),GHG_Data['CO_qc_flags_-3_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_-2_offset']>'1'),GHG_Data['CO_qc_flags_-2_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_-1_offset']>'1'),GHG_Data['CO_qc_flags_-1_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_+1_offset']>'1'),GHG_Data['CO_qc_flags_+1_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_+2_offset']>'1'),GHG_Data['CO_qc_flags_+2_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_+3_offset']>'1'),GHG_Data['CO_qc_flags_+3_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_+4_offset']>'1'),GHG_Data['CO_qc_flags_+4_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_+5_offset']>'1'),GHG_Data['CO_qc_flags_+5_offset'],GHG_Data['CO_qc_flags'])
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags_+6_offset']>'1'),GHG_Data['CO_qc_flags_+6_offset'],GHG_Data['CO_qc_flags'])

GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4 (ppm)'].isnull()), '0', GHG_Data['CH4_qc_flags']) 
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O (ppm)'].isnull()), '0', GHG_Data['H2O_qc_flags']) 
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2 (ppm)'].isnull()), '0', GHG_Data['CO2_qc_flags']) 
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO (ppb)'].isnull()), '0', GHG_Data['CO_qc_flags']) 
GHG_Data['MultiCarbon_Flag'] = np.where((GHG_Data['CH4_qc_flags'] == '0') & (GHG_Data['H2O_qc_flags'] == '0') & (GHG_Data['CO2_qc_flags'] == '0') & (GHG_Data['CO_qc_flags'] == '0'), '5', GHG_Data['MultiCarbon_Flag'])
GHG_Data.drop(GHG_Data[(GHG_Data['MultiCarbon_Flag'] == '5')].index,inplace =True)

GHG_Data['CH4_qc_flags'] = np.where((GHG_Data['CH4_qc_flags']=='0'), '3', GHG_Data['CH4_qc_flags']) 
GHG_Data['H2O_qc_flags'] = np.where((GHG_Data['H2O_qc_flags']=='0'), '3', GHG_Data['H2O_qc_flags']) 
GHG_Data['CO2_qc_flags'] = np.where((GHG_Data['CO2_qc_flags']=='0'), '3', GHG_Data['CO2_qc_flags']) 
GHG_Data['CO_qc_flags'] = np.where((GHG_Data['CO_qc_flags']=='0'), '3', GHG_Data['CO_qc_flags']) 

col_List_GHG = list(GHG_Data.columns.values) # create a list of column names
col_List_GHG.remove('CH4 (ppm)')
col_List_GHG.remove('CO2 (ppm)')
col_List_GHG.remove('H2O (ppm)')
col_List_GHG.remove('CO (ppb)')
col_List_GHG.remove('CH4_qc_flags')
col_List_GHG.remove('H2O_qc_flags')
col_List_GHG.remove('CO2_qc_flags')
col_List_GHG.remove('CO_qc_flags')
GHG_Data = GHG_Data.drop(columns=col_List_GHG) #removing unwanted columns

plt.plot(GHG_Data['CH4 (ppm)'], label='CH4')
#plt.plot(GHG_Data['H2O (ppm)'], label='H2O - MultiCarbon Analyser')
#plt.plot(GHG_Data['CO2 (ppm)'], label='CO2')
#plt.plot(GHG_Data['CO (ppb)'], label='CO')
plt.legend()
plt.ylabel('abundance (ppm)')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

#plt.plot(GHG_Data['CH4 (ppm)'], label='CH4')
#plt.plot(GHG_Data['H2O (ppm)'], label='H2O - MultiCarbon Analyser')
plt.plot(GHG_Data['CO2 (ppm)'], label='CO2')
#plt.plot(GHG_Data['CO (ppb)'], label='CO')
plt.legend()
plt.ylabel('abundance (ppm)')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

#plt.plot(GHG_Data['CH4 (ppm)'], label='CH4')
#plt.plot(GHG_Data['H2O (ppm)'], label='H2O - MultiCarbon Analyser')
#plt.plot(GHG_Data['CO2 (ppm)'], label='CO2')
plt.plot(GHG_Data['CO (ppb)'], label='CO')
plt.legend()
plt.ylabel('abundance (ppb)')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

LGR_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/LGR/'
check_Folder = os.path.isdir(LGR_Folder)
if not check_Folder:
    os.makedirs(LGR_Folder)
    print("created folder : ", LGR_Folder)

else:
    print(LGR_Folder, "folder already exists.")

GHG_Data.to_csv(str(LGR_Folder) + 'lgr-multicarbon_maqs_'  + str(date_file_label) + '_CH4-CO2-CO-H2O_concentration' + str(status) +  str(version_number) + '.csv')

GHG_Data['TimeDateSince'] = GHG_Data.index-datetime.datetime(1970,1,1,0,0,00)
GHG_Data['TimeSecondsSince'] = GHG_Data['TimeDateSince'].dt.total_seconds()
GHG_Data['day_year'] = pd.DatetimeIndex(GHG_Data['TimeDateSince'].index).dayofyear
GHG_Data['year'] = pd.DatetimeIndex(GHG_Data['TimeDateSince'].index).year
GHG_Data['month'] = pd.DatetimeIndex(GHG_Data['TimeDateSince'].index).month
GHG_Data['day'] = pd.DatetimeIndex(GHG_Data['TimeDateSince'].index).day
GHG_Data['hour'] = pd.DatetimeIndex(GHG_Data['TimeDateSince'].index).hour
GHG_Data['minute'] = pd.DatetimeIndex(GHG_Data['TimeDateSince'].index).minute
GHG_Data['second'] = pd.DatetimeIndex(GHG_Data['TimeDateSince'].index).second

#processing H2O & NH3 data from Ammonia analyser

Ammonia_Data['NH3 (ppm)'] = Ammonia_Data['NH3 (ppm) perlim']*1000
Ammonia_Data.rename(columns={'NH3 (ppm)': 'NH3 (ppb)','H2O (ppm) - NH3 analyser': 'H2O (ppm)' }, inplace = True)

Ammonia_Data['NH3_qc_flags']=np.nan
Ammonia_Data['NH3_qc_flags']=np.where(Ammonia_Data['NH3 (ppb)']>0.5, '1','3') 
Ammonia_Data['NH3_qc_flags']=np.where((Ammonia_Data['NH3 (ppb)']>300), '3', Ammonia_Data['NH3_qc_flags']) 
Ammonia_Data['NH3_qc_flags']=np.where((Ammonia_Data['Ammonia_Flag'] == '3'), '3', Ammonia_Data['NH3_qc_flags'])
#Ammonia_Data['NH3_qc_flags']=np.where(Ammonia_Data['NH3 (ppb)']>-5, Ammonia_Data['NH3_qc_flags'],'2') 
#Ammonia_Data['NH3_qc_flags']=np.where((Ammonia_Data['NH3 (ppb)']>10000), '2', Ammonia_Data['NH3_qc_flags']) 

Ammonia_Data['H2O_qc_flags']=np.nan
Ammonia_Data['H2O_qc_flags']=np.where(Ammonia_Data['H2O (ppm)']>20, '1','3') 
Ammonia_Data['H2O_qc_flags']=np.where(Ammonia_Data['H2O (ppm)']>70000, '3', Ammonia_Data['H2O_qc_flags']) 
Ammonia_Data['H2O_qc_flags']=np.where((Ammonia_Data['Ammonia_Flag'] == '3'), '3', Ammonia_Data['H2O_qc_flags'])
#Ammonia_Data['H2O_qc_flags']=np.where(Ammonia_Data['H2O (ppm)']>100, Ammonia_Data['H2O_qc_flags'],'2') #measurement boundary range
#Ammonia_Data['H2O_qc_flags']=np.where(Ammonia_Data['H2O (ppm)']>30000, '2', Ammonia_Data['H2O_qc_flags']) #measurement boundary range

Ammonia_Data['H2O_qc_flags_-4_offset'] = Ammonia_Data['H2O_qc_flags'].shift(periods=-4)
Ammonia_Data['H2O_qc_flags_-3_offset'] = Ammonia_Data['H2O_qc_flags'].shift(periods=-3)
Ammonia_Data['H2O_qc_flags_-2_offset'] = Ammonia_Data['H2O_qc_flags'].shift(periods=-2)
Ammonia_Data['H2O_qc_flags_-1_offset'] = Ammonia_Data['H2O_qc_flags'].shift(periods=-1)
Ammonia_Data['H2O_qc_flags_+1_offset'] = Ammonia_Data['H2O_qc_flags'].shift(periods=1)
Ammonia_Data['H2O_qc_flags_+2_offset'] = Ammonia_Data['H2O_qc_flags'].shift(periods=2)
Ammonia_Data['H2O_qc_flags_+3_offset'] = Ammonia_Data['H2O_qc_flags'].shift(periods=3)
Ammonia_Data['H2O_qc_flags_+4_offset'] = Ammonia_Data['H2O_qc_flags'].shift(periods=4)
Ammonia_Data['H2O_qc_flags'] = np.where((Ammonia_Data['H2O_qc_flags_-4_offset']>'1'),Ammonia_Data['H2O_qc_flags_-4_offset'],Ammonia_Data['H2O_qc_flags'])
Ammonia_Data['H2O_qc_flags'] = np.where((Ammonia_Data['H2O_qc_flags_-3_offset']>'1'),Ammonia_Data['H2O_qc_flags_-3_offset'],Ammonia_Data['H2O_qc_flags'])
Ammonia_Data['H2O_qc_flags'] = np.where((Ammonia_Data['H2O_qc_flags_-2_offset']>'1'),Ammonia_Data['H2O_qc_flags_-2_offset'],Ammonia_Data['H2O_qc_flags'])
Ammonia_Data['H2O_qc_flags'] = np.where((Ammonia_Data['H2O_qc_flags_-1_offset']>'1'),Ammonia_Data['H2O_qc_flags_-1_offset'],Ammonia_Data['H2O_qc_flags'])
Ammonia_Data['H2O_qc_flags'] = np.where((Ammonia_Data['H2O_qc_flags_+1_offset']>'1'),Ammonia_Data['H2O_qc_flags_+1_offset'],Ammonia_Data['H2O_qc_flags'])
Ammonia_Data['H2O_qc_flags'] = np.where((Ammonia_Data['H2O_qc_flags_+2_offset']>'1'),Ammonia_Data['H2O_qc_flags_+2_offset'],Ammonia_Data['H2O_qc_flags'])
Ammonia_Data['H2O_qc_flags'] = np.where((Ammonia_Data['H2O_qc_flags_+3_offset']>'1'),Ammonia_Data['H2O_qc_flags_+3_offset'],Ammonia_Data['H2O_qc_flags'])
Ammonia_Data['H2O_qc_flags'] = np.where((Ammonia_Data['H2O_qc_flags_+4_offset']>'1'),Ammonia_Data['H2O_qc_flags_+4_offset'],Ammonia_Data['H2O_qc_flags'])

Ammonia_Data['NH3_qc_flags_-4_offset'] = Ammonia_Data['NH3_qc_flags'].shift(periods=-4)
Ammonia_Data['NH3_qc_flags_-3_offset'] = Ammonia_Data['NH3_qc_flags'].shift(periods=-3)
Ammonia_Data['NH3_qc_flags_-2_offset'] = Ammonia_Data['NH3_qc_flags'].shift(periods=-2)
Ammonia_Data['NH3_qc_flags_-1_offset'] = Ammonia_Data['NH3_qc_flags'].shift(periods=-1)
Ammonia_Data['NH3_qc_flags_+1_offset'] = Ammonia_Data['NH3_qc_flags'].shift(periods=1)
Ammonia_Data['NH3_qc_flags_+2_offset'] = Ammonia_Data['NH3_qc_flags'].shift(periods=2)
Ammonia_Data['NH3_qc_flags_+3_offset'] = Ammonia_Data['NH3_qc_flags'].shift(periods=3)
Ammonia_Data['NH3_qc_flags_+4_offset'] = Ammonia_Data['NH3_qc_flags'].shift(periods=4)
Ammonia_Data['NH3_qc_flags'] = np.where((Ammonia_Data['NH3_qc_flags_-4_offset']>'1'),Ammonia_Data['NH3_qc_flags_-4_offset'],Ammonia_Data['NH3_qc_flags'])
Ammonia_Data['NH3_qc_flags'] = np.where((Ammonia_Data['NH3_qc_flags_-3_offset']>'1'),Ammonia_Data['NH3_qc_flags_-3_offset'],Ammonia_Data['NH3_qc_flags'])
Ammonia_Data['NH3_qc_flags'] = np.where((Ammonia_Data['NH3_qc_flags_-2_offset']>'1'),Ammonia_Data['NH3_qc_flags_-2_offset'],Ammonia_Data['NH3_qc_flags'])
Ammonia_Data['NH3_qc_flags'] = np.where((Ammonia_Data['NH3_qc_flags_-1_offset']>'1'),Ammonia_Data['NH3_qc_flags_-1_offset'],Ammonia_Data['NH3_qc_flags'])
Ammonia_Data['NH3_qc_flags'] = np.where((Ammonia_Data['NH3_qc_flags_+1_offset']>'1'),Ammonia_Data['NH3_qc_flags_+1_offset'],Ammonia_Data['NH3_qc_flags'])
Ammonia_Data['NH3_qc_flags'] = np.where((Ammonia_Data['NH3_qc_flags_+2_offset']>'1'),Ammonia_Data['NH3_qc_flags_+2_offset'],Ammonia_Data['NH3_qc_flags'])
Ammonia_Data['NH3_qc_flags'] = np.where((Ammonia_Data['NH3_qc_flags_+3_offset']>'1'),Ammonia_Data['NH3_qc_flags_+3_offset'],Ammonia_Data['NH3_qc_flags'])
Ammonia_Data['NH3_qc_flags'] = np.where((Ammonia_Data['NH3_qc_flags_+4_offset']>'1'),Ammonia_Data['NH3_qc_flags_+4_offset'],Ammonia_Data['NH3_qc_flags'])

Ammonia_Data['NH3_qc_flags'] = np.where((Ammonia_Data['NH3 (ppb)'].isnull()), '0', Ammonia_Data['NH3_qc_flags']) 
Ammonia_Data['H2O_qc_flags'] = np.where((Ammonia_Data['H2O (ppm)'].isnull()), '0', Ammonia_Data['H2O_qc_flags']) 
Ammonia_Data['Ammonia_Flag'] = np.where((Ammonia_Data['NH3_qc_flags'] == '0') & (Ammonia_Data['H2O_qc_flags'] == '0'), '5', Ammonia_Data['Ammonia_Flag'])
Ammonia_Data.drop(Ammonia_Data[(Ammonia_Data['Ammonia_Flag'] == '5')].index,inplace =True)

Ammonia_Data['NH3_qc_flags'] = np.where((Ammonia_Data['NH3_qc_flags']=='0'), '3', Ammonia_Data['NH3_qc_flags']) 
Ammonia_Data['H2O_qc_flags'] = np.where((Ammonia_Data['H2O_qc_flags']=='0'), '3', Ammonia_Data['H2O_qc_flags']) 

NH3_List = list(Ammonia_Data.columns.values)
NH3_List.remove('NH3 (ppb)')
NH3_List.remove('NH3_qc_flags')
NH3_List.remove('H2O (ppm)')
NH3_List.remove('H2O_qc_flags')
Ammonia_Data = Ammonia_Data.drop(columns=NH3_List)

#plt.plot(Ammonia_Data['NH3 (ppb)'], label='NH3')
plt.plot(GHG_Data['H2O (ppm)'], label='H2O - MultiCarbon Analyser')
plt.plot(Ammonia_Data['H2O (ppm)'], label='H2O - Ammonia Analyser')
plt.legend()
plt.ylabel('abundance (ppm)')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

plt.plot(Ammonia_Data['NH3 (ppb)'], label='NH3')
#plt.plot(GHG_Data['CO (ppb)'], label='CO')
plt.legend()
plt.ylabel('abundance (ppb)')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

Ammonia_Data.to_csv(str(LGR_Folder) + 'lgr-ammonia-analyser_maqs_' + str(date_file_label) + '_NH3-H2O-concentration' + str(status) + str(version_number) + '.csv')

Ammonia_Data['TimeDateSince'] = Ammonia_Data.index-datetime.datetime(1970,1,1,0,0,00)
Ammonia_Data['TimeSecondsSince'] = Ammonia_Data['TimeDateSince'].dt.total_seconds()
Ammonia_Data['day_year'] = pd.DatetimeIndex(Ammonia_Data['TimeDateSince'].index).dayofyear
Ammonia_Data['year'] = pd.DatetimeIndex(Ammonia_Data['TimeDateSince'].index).year
Ammonia_Data['month'] = pd.DatetimeIndex(Ammonia_Data['TimeDateSince'].index).month
Ammonia_Data['day'] = pd.DatetimeIndex(Ammonia_Data['TimeDateSince'].index).day
Ammonia_Data['hour'] = pd.DatetimeIndex(Ammonia_Data['TimeDateSince'].index).hour
Ammonia_Data['minute'] = pd.DatetimeIndex(Ammonia_Data['TimeDateSince'].index).minute
Ammonia_Data['second'] = pd.DatetimeIndex(Ammonia_Data['TimeDateSince'].index).second


