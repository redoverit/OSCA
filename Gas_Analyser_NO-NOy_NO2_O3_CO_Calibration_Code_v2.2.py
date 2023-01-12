# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 17:34:47 2022

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
import scipy.stats

sample_Freq = '10sec'
av_Freq = '1min' #averaging frequency required of the data
data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v2.2' #version of the code
validity_status = 'Ratified' #Ratified or Unratified

NOy_Data_Source = 'logbook' #respond 'logbook' or 'raw_files'

CO_Data_Source = 'database' # respond either 'database' or 'logfile'

NOy_Adjustments = False #respond true for audit based adjustments or false for no adjustments

CO_Adjustments = False #respond true for audit based adjustments or false for no adjustments

today = date.today()
current_day = today.strftime("%Y%m%d") #this can then be written into the file name to establish when calibration file was generated

date_of_file_change = datetime.datetime(2019,11,14,0,0,00)
year = int(date_of_file_change.strftime("%Y"))
month = int(date_of_file_change.strftime("%m"))
day = int(date_of_file_change.strftime("%d"))
Start_of_file_change = datetime.datetime(year,month,day,14,16,00)
End_of_file_change = datetime.datetime(year,month,day,15,23,00)

folder = np.where((str(version_number) == 'v0.6'), 'Preliminary', str(validity_status))

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/NOyOzone/', 'D:/FirsData/NOyOzone/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(folder) + '_' + str(version_number) + '/', 'D:/' + str(folder) + '_' + str(version_number) + '/')

check_Folder = os.path.isdir(str(Data_Output_Folder))
if not check_Folder:
    os.makedirs(str(Data_Output_Folder))
    print("created folder : ", str(Data_Output_Folder))

else:
    print(str(Data_Output_Folder), "folder already exists.")

Conc_NOy_Cal_PPB = 463

Logbook_NOy_Cal = str(Data_Source_Folder) + 'Cal_LogBook_Record.csv' # Needs to be address of data location - Collect CSV files
print(str(Logbook_NOy_Cal))
Logbook_NOy_Cal_Files = glob.glob(Logbook_NOy_Cal)

# Create an empty list
frames = []

#  Iterate over csv_files
for csv in Logbook_NOy_Cal_Files:
    df = pd.read_csv(csv) #
    frames.append(df)

Logbook_Cal = pd.concat(frames)

Logbook_Cal.rename(columns={'Raw NO' : 'Raw_NO_Zero'}, inplace=True)
Logbook_Cal.rename(columns={'Raw NOY': 'Raw_NOy_Cal'}, inplace=True)
Logbook_Cal.rename(columns={'Corrected NO': 'Corrected_NO_Zero'}, inplace=True)
Logbook_Cal.rename(columns={'Corrected NOY': 'Corrected_NOy_Cal'}, inplace=True)

Logbook_Cal['Date'] = Logbook_Cal['Date'].astype(str)
Logbook_Cal['datetime'] = Logbook_Cal['Date']+ ' ' + Logbook_Cal['Time'] # added Date and time into new columns
Logbook_Cal['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M') for x in Logbook_Cal['datetime']] #converts the dateTime format from string to python dateTime
Logbook_Cal.index = Logbook_Cal['datetime']
Logbook_Cal = Logbook_Cal.sort_index()

Logbook_Cal['Raw_NO_Zero'] = np.where(Logbook_Cal['Raw_NO_Zero'].isnull(), 0, Logbook_Cal['Raw_NO_Zero'])
Logbook_Cal['Corrected_NO_Zero'] = np.where(Logbook_Cal['Corrected_NO_Zero'].isnull(), 0, Logbook_Cal['Corrected_NO_Zero'])

Logbook_Cal['Raw_NO_Zero'] = Logbook_Cal['Raw_NO_Zero'].astype(float)
Logbook_Cal['Corrected_NO_Zero'] = Logbook_Cal['Corrected_NO_Zero'].astype(float)

Logbook_Cal['NO_LogBook_Zero'] = np.where(Logbook_Cal['Raw_NO_Zero'] == 0, Logbook_Cal['Corrected_NO_Zero'], Logbook_Cal['Raw_NO_Zero'])

Logbook_Cal['NO_LogBook_Zero'] = Logbook_Cal['NO_LogBook_Zero'].astype(float)
Logbook_Cal['Raw_NOy_Cal'] = Logbook_Cal['Raw_NOy_Cal'].astype(float)
Logbook_Cal['Corrected_NOy_Cal'] = Logbook_Cal['Corrected_NOy_Cal'].astype(float)
Logbook_Cal = Logbook_Cal.drop(columns=['Raw_NO_Zero', 'Corrected_NO_Zero']) #'Date', 'Time', 


#Logbook_Cal.to_csv(str(Data_Output_Folder) + '12_Cal_log_Auto-Zeros_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

Original_NOy_Cal = str(Data_Source_Folder) + 'Cal_Record.csv' # Needs to be address of data location - Collect CSV files
Original_NOy_Cal_Files = glob.glob(Original_NOy_Cal)

# Create an empty list
frames = []

#  Iterate over csv_files
for csv in Original_NOy_Cal_Files:
    df = pd.read_csv(csv) #
    frames.append(df)

Automated_Cal = pd.concat(frames)
Automated_Cal.rename(columns={0: 'Date'}, inplace=True)
Automated_Cal.rename(columns={1: 'Time'}, inplace=True)

Automated_Cal['Date'] = Automated_Cal['Date'].astype(str)
Automated_Cal['Date_length'] = Automated_Cal['Date'].str.len()
Automated_Cal=Automated_Cal.loc[Automated_Cal.Date_length == 10] #check the data string length for corruption
Automated_Cal['datetime'] = Automated_Cal['Date']+ ' ' + Automated_Cal['Time'] # added Date and time into new columns
Automated_Cal['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in Automated_Cal['datetime']] #converts the dateTime format from string to python dateTime
Automated_Cal.index =Automated_Cal['datetime']
Automated_Cal = Automated_Cal.sort_index()

Automated_Cal.rename(columns={'NO_Zero': 'NO_File_Zero'}, inplace=True)
Automated_Cal.rename(columns={'NO_Slope': 'NO_File_Slope'}, inplace=True)

Automated_Cal['NO_File_Zero'] = Automated_Cal['NO_File_Zero'].astype(float)
Automated_Cal['NO_File_Slope'] = Automated_Cal['NO_File_Slope'].astype(float)

Automated_Cal.drop(Automated_Cal[(Automated_Cal['NO_File_Slope'] == 1)].index,inplace =True)

Automated_Cal['NO_Zero +1 offset'] = Automated_Cal['NO_File_Zero'].shift(periods=1)
Automated_Cal['NO_Slope +1 offset'] = Automated_Cal['NO_File_Slope'].shift(periods=1)

Automated_Cal['NOy_offset_flags'] = np.where(((Automated_Cal['NO_File_Zero'] == Automated_Cal['NO_Zero +1 offset']) & (Automated_Cal['NO_File_Slope'] == Automated_Cal['NO_Slope +1 offset'])), 1, 0)

Automated_Cal.drop(Automated_Cal[(Automated_Cal['NOy_offset_flags'] == 1)].index,inplace =True)

Automated_Cal.drop(Automated_Cal[(Automated_Cal['NO_File_Slope'] >= 80)].index,inplace =True)

Automated_Cal.drop(Automated_Cal[(Automated_Cal['NO_File_Zero'] == -0.023)].index,inplace =True)
Automated_Cal.drop(Automated_Cal[(Automated_Cal['NO_File_Zero'] == -0.007)].index,inplace =True)

Automated_Cal = pd.concat([Logbook_Cal, Automated_Cal])

Automated_Cal = Automated_Cal.sort_index()

Automated_Cal['NOy Span Cylinder (ppb)'] = float(Conc_NOy_Cal_PPB)

Automated_Cal['NOy_LogBook_Response'] = (Automated_Cal['NOy Span Cylinder (ppb)'] + Automated_Cal['NO_LogBook_Zero'])/Automated_Cal['Raw_NOy_Cal'] 

Automated_Cal['Date_-1'] = Automated_Cal['Date'].shift(periods=-1)
Automated_Cal['Date_-2'] = Automated_Cal['Date'].shift(periods=-2)
Automated_Cal['Date_+1'] = Automated_Cal['Date'].shift(periods=1)
Automated_Cal['Date_+2'] = Automated_Cal['Date'].shift(periods=2)

Automated_Cal['NO_Zero_offset_-1'] = Automated_Cal['NO_File_Zero'].shift(periods=-1)
Automated_Cal['NO_Zero_offset_-2'] = Automated_Cal['NO_File_Zero'].shift(periods=-2)
Automated_Cal['NO_Zero_offset_+1'] = Automated_Cal['NO_File_Zero'].shift(periods=1)
Automated_Cal['NO_Zero_offset_+2'] = Automated_Cal['NO_File_Zero'].shift(periods=2)

Automated_Cal['NO_Slope_offset_-1'] = Automated_Cal['NO_File_Slope'].shift(periods=-1)
Automated_Cal['NO_Slope_offset_-2'] = Automated_Cal['NO_File_Slope'].shift(periods=-2)
Automated_Cal['NO_Slope_offset_+1'] = Automated_Cal['NO_File_Slope'].shift(periods=1)
Automated_Cal['NO_Slope_offset_+2'] = Automated_Cal['NO_File_Slope'].shift(periods=2)

Automated_Cal['NO_File_Zero'] = np.where(((Automated_Cal['NO_File_Zero'].isnull()) & (Automated_Cal['Date_-1'] == Automated_Cal['Date'])), Automated_Cal['NO_Zero_offset_-1'], Automated_Cal['NO_File_Zero'])
Automated_Cal['NO_File_Zero'] = np.where(((Automated_Cal['NO_File_Zero'].isnull()) & (Automated_Cal['Date_-2'] == Automated_Cal['Date'])), Automated_Cal['NO_Zero_offset_-2'], Automated_Cal['NO_File_Zero'])
Automated_Cal['NO_File_Zero'] = np.where(((Automated_Cal['NO_File_Zero'].isnull()) & (Automated_Cal['Date_+1'] == Automated_Cal['Date'])), Automated_Cal['NO_Zero_offset_+1'], Automated_Cal['NO_File_Zero'])
Automated_Cal['NO_File_Zero'] = np.where(((Automated_Cal['NO_File_Zero'].isnull()) & (Automated_Cal['Date_+2'] == Automated_Cal['Date'])), Automated_Cal['NO_Zero_offset_+2'], Automated_Cal['NO_File_Zero'])

Automated_Cal['NO_File_Slope'] = np.where(((Automated_Cal['NO_File_Slope'].isnull()) & (Automated_Cal['Date_-1'] == Automated_Cal['Date'])), Automated_Cal['NO_Slope_offset_-1'], Automated_Cal['NO_File_Slope'])
Automated_Cal['NO_File_Slope'] = np.where(((Automated_Cal['NO_File_Slope'].isnull()) & (Automated_Cal['Date_-2'] == Automated_Cal['Date'])), Automated_Cal['NO_Slope_offset_-2'], Automated_Cal['NO_File_Slope'])
Automated_Cal['NO_File_Slope'] = np.where(((Automated_Cal['NO_File_Slope'].isnull()) & (Automated_Cal['Date_+1'] == Automated_Cal['Date'])), Automated_Cal['NO_Slope_offset_+1'], Automated_Cal['NO_File_Slope'])
Automated_Cal['NO_File_Slope'] = np.where(((Automated_Cal['NO_File_Slope'].isnull()) & (Automated_Cal['Date_+2'] == Automated_Cal['Date'])), Automated_Cal['NO_Slope_offset_+2'], Automated_Cal['NO_File_Slope'])

Automated_Cal['NO_Offset_Flag'] = np.where(((Automated_Cal['NO_LogBook_Zero'].isnull()) & ((Automated_Cal['Date_-1'] == Automated_Cal['Date']) | (Automated_Cal['Date_+1'] == Automated_Cal['Date']))), 1, 0)

start = datetime.datetime(2020,4,1,0,0,00)
end = datetime.datetime(2020,4,1,23,59,59)
Automated_Cal.loc[start:end, 'NO_Offset_Flag'] = 0

Automated_Cal.drop(Automated_Cal[(Automated_Cal['NO_Offset_Flag'] == 1)].index,inplace =True)

Automated_Cal['NO_File_Zero'] = np.where(Automated_Cal['NO_File_Zero'].isnull(), Automated_Cal['NO_LogBook_Zero'], Automated_Cal['NO_File_Zero'])
Automated_Cal['NO_File_Slope'] = np.where(Automated_Cal['NO_File_Slope'].isnull(), Automated_Cal['NOy_LogBook_Response'], Automated_Cal['NO_File_Slope'])

Cal_drop_list = list(Automated_Cal.columns.values)
Cal_drop_list.remove('NO_File_Zero')
Cal_drop_list.remove('NO_File_Slope')
Cal_drop_list.remove('Date')
Cal_drop_list.remove('Time')
#Cal_drop_list.remove('NOy Span Cylinder (ppb)')
#Cal_drop_list.remove('NO_LogBook_Zero')
#Cal_drop_list.remove('NO_LogBook_Response')
#Cal_drop_list.remove('datetime')
Automated_Cal = Automated_Cal.drop(columns=Cal_drop_list)

#Automated_Cal.to_csv(str(Data_Output_Folder) + '9_NO-NOy_Auto-Zeros_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

pattern_1 = str(Data_Source_Folder) + '201908*_gas.csv'# Collect CSV files

pattern_2 = str(Data_Source_Folder) + '201909*_gas.csv'

pattern_3 = str(Data_Source_Folder) + '201910*_gas.csv'

csv_files = glob.glob(pattern_1) + glob.glob(pattern_2) + glob.glob(pattern_3) # + glob.glob(pattern_4)

gas_frames = []

for csv in csv_files:
    
    #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv, header=None, usecols=[0,1,2,3,4,14])
    gas_frames.append(df)

early_Data = pd.concat(gas_frames)

early_Data.rename(columns={0: 'Date'}, inplace=True)
early_Data.rename(columns={1: 'Time'}, inplace=True)
early_Data.rename(columns={2: 'NO (ppb)'}, inplace=True)
early_Data.rename(columns={3: 'Diff (ppb)'}, inplace=True)
early_Data.rename(columns={4: 'NOy (ppb)'}, inplace=True)
early_Data.rename(columns={14: 'NOy Flags'}, inplace=True)

early_Data['Date'] = early_Data['Date'].astype(str)
early_Data['Date_length'] = early_Data['Date'].str.len()
early_Data=early_Data.loc[early_Data.Date_length == 10] #check the data string length for corruption
early_Data['datetime'] = early_Data['Date']+' '+early_Data['Time']# added Date and time into new columns
early_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in early_Data['datetime']] #converts the dateTime format from string to python dateTime
early_Data.index = early_Data['datetime']
early_Data = early_Data.sort_index()
early_Data = early_Data.drop(columns=['Date_length', 'Date', 'Time'])

early_Data.drop(early_Data[(early_Data['NOy Flags'] == 'NOy Flags')].index,inplace =True)

NOy_Data = early_Data

NOy_Data['Gas_Flag'] = "1"

start_NOy_gas_span1 = datetime.datetime(2019,8,22,12,45,00) # NOy gas span without cal on turned on
end_NOy_gas_span1 = datetime.datetime(2019,8,22,13,5,00)
NOy_Data.loc[start_NOy_gas_span1:end_NOy_gas_span1, 'Gas_Flag'] = "3"

start_NOy_gas_span2 = datetime.datetime(2019,9,6,14,10,00) 
end_NOy_gas_span2 = datetime.datetime(2019,9,6,14,30,00)
NOy_Data.loc[start_NOy_gas_span2:end_NOy_gas_span2, 'Gas_Flag'] = "3"

start_NOy_gas_span3 = datetime.datetime(2019,9,10,14,10,00)
end_NOy_gas_span3 = datetime.datetime(2019,9,10,14,50,00)
NOy_Data.loc[start_NOy_gas_span3:end_NOy_gas_span3, 'Gas_Flag'] = "3"

start_NOy_gas_span4 = datetime.datetime(2019,9,17,10,25,00)
end_NOy_gas_span4 = datetime.datetime(2019,9,17,10,45,00)
NOy_Data.loc[start_NOy_gas_span4:end_NOy_gas_span4, 'Gas_Flag'] = "3"

start_NOy_gas_span5 = datetime.datetime(2019,9,26,8,55,00)
end_NOy_gas_span5 = datetime.datetime(2019,9,26,9,15,00)
NOy_Data.loc[start_NOy_gas_span5:end_NOy_gas_span5, 'Gas_Flag'] = "3"

start_NOy_gas_span6 = datetime.datetime(2019,10,2,14,35,00)
end_NOy_gas_span6 = datetime.datetime(2019,10,2,14,55,00)
NOy_Data.loc[start_NOy_gas_span6:end_NOy_gas_span6, 'Gas_Flag'] = "3"

start_NOy_gas_span7 = datetime.datetime(2019,10,9,13,55,00)
end_NOy_gas_span7 = datetime.datetime(2019,10,9,14,15,00)
NOy_Data.loc[start_NOy_gas_span7:end_NOy_gas_span7, 'Gas_Flag'] = "3"

start_NOy_gas_span8 = datetime.datetime(2019,10,15,12,55,00)
end_NOy_gas_span8 = datetime.datetime(2019,10,15,13,25,00)
NOy_Data.loc[start_NOy_gas_span8:end_NOy_gas_span8, 'Gas_Flag'] = "3"

start_NOy_gas_span9 = datetime.datetime(2019,10,24,8,10,00)
end_NOy_gas_span9 = datetime.datetime(2019,10,24,8,45,00)
NOy_Data.loc[start_NOy_gas_span9:end_NOy_gas_span9, 'Gas_Flag'] = "3"

start_NOy_gas_span10 = datetime.datetime(2019,10,31,11,10,00)
end_NOy_gas_span10 = datetime.datetime(2019,10,31,11,40,00)
NOy_Data.loc[start_NOy_gas_span10:end_NOy_gas_span10, 'Gas_Flag'] = "3"

start_NOy_gas_span11 = datetime.datetime(2019,8,9,16,30,00)
end_NOy_gas_span11 = datetime.datetime(2019,8,9,17,45,00)
NOy_Data.loc[start_NOy_gas_span11:end_NOy_gas_span11, 'Gas_Flag'] = "3"

NOy_Data.drop(NOy_Data[(NOy_Data['Gas_Flag'] == "1")].index,inplace =True)

NOy_Data.drop(NOy_Data[(NOy_Data['NOy Flags'] == "CC030000")].index,inplace =True)

NOy_Data['NO (ppb)'] = NOy_Data['NO (ppb)'].astype(float)
NOy_Data['Diff (ppb)'] = NOy_Data['Diff (ppb)'].astype(float)
NOy_Data['NOy (ppb)'] = NOy_Data['NOy (ppb)'].astype(float)

NOy_Data.drop(NOy_Data[(NOy_Data['NOy (ppb)'] < 300)].index,inplace =True)

#NOy_Data.to_csv(str(Data_Output_Folder) + '11_NO-NOy_Early-Zeros_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')


pattern_1 = str(Data_Source_Folder) + '202*_firsgas.csv'# Collect CSV files

pattern_2 = str(Data_Source_Folder) + '2019*00_firsgas.csv'

pattern_3 = str(Data_Source_Folder) + '2019*59_firsgas.csv'

pattern_4 = str(Data_Source_Folder) + '2019*23_firsgas.csv'

csv_files = glob.glob(pattern_1) + glob.glob(pattern_2) + glob.glob(pattern_3) + glob.glob(pattern_4)

gas_frames = []

for csv in csv_files:
    
    #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv, header=None, usecols=[0,1,2,3,4,16])
    gas_frames.append(df)

NOy_Cal_Data = pd.concat(gas_frames)

NOy_Cal_Data.rename(columns={0: 'Date'}, inplace=True)
NOy_Cal_Data.rename(columns={1: 'Time'}, inplace=True)
NOy_Cal_Data.rename(columns={2: 'NO (ppb)'}, inplace=True)
NOy_Cal_Data.rename(columns={3: 'Diff (ppb)'}, inplace=True)
NOy_Cal_Data.rename(columns={4: 'NOy (ppb)'}, inplace=True)
NOy_Cal_Data.rename(columns={16: 'NOy_Flags'}, inplace=True)

NOy_Cal_Data.drop(NOy_Cal_Data[(NOy_Cal_Data['NOy_Flags'] == 'NOy Flags')].index,inplace =True)

NOy_Cal_Data['Date'] = NOy_Cal_Data['Date'].astype(str)
NOy_Cal_Data['Date_length'] = NOy_Cal_Data['Date'].str.len()
NOy_Cal_Data=NOy_Cal_Data.loc[NOy_Cal_Data.Date_length == 10] #check the data string length for corruption
NOy_Cal_Data['datetime'] = NOy_Cal_Data['Date']+' '+ NOy_Cal_Data['Time']# added Date and time into new columns
NOy_Cal_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in NOy_Cal_Data['datetime']] #converts the dateTime format from string to python dateTime
NOy_Cal_Data.index = NOy_Cal_Data['datetime']
NOy_Cal_Data = NOy_Cal_Data.sort_index()
NOy_Cal_Data = NOy_Cal_Data.drop(columns=['Date_length', 'Date', 'Time'])

#NOy_Cal_Data['NO_Flags'] = np.where(((NOy_Cal_Data['NOy_Flags'] == 'CC030000') | (NOy_Cal_Data['NOy_Flags'] == 'CC030028')), 0, 1)

NOy_Cal_Data=NOy_Cal_Data.loc[NOy_Cal_Data.NOy_Flags == 'CC030028']

NOy_Cal_Data = pd.concat([NOy_Cal_Data, NOy_Data, Automated_Cal])

NOy_Cal_Data = NOy_Cal_Data.sort_index()

NOy_Cal_Data['NO (ppb)'] = NOy_Cal_Data['NO (ppb)'].astype(float)
#NOy_Cal_Data['Diff (ppb)'] = NOy_Cal_Data['Diff (ppb)'].astype(float)
NOy_Cal_Data['NOy (ppb)'] = NOy_Cal_Data['NOy (ppb)'].astype(float)

NOy_Cal_Data.drop(NOy_Cal_Data[(NOy_Cal_Data['NO (ppb)'] == 0)].index,inplace =True)

NOy_Cal_Data.drop(NOy_Cal_Data[(NOy_Cal_Data['NOy (ppb)'] == 0)].index,inplace =True)

NOy_Cal_Data = NOy_Cal_Data.groupby(pd.Grouper(freq=av_Freq)).mean()

NOy_Old_Data = NOy_Cal_Data

NO_Cal_Freq = '1440min'

Mean_NO_AutoZero = NOy_Cal_Data['NO (ppb)'].groupby(pd.Grouper(freq=NO_Cal_Freq)).mean()

Max_NO_AutoCal = NOy_Cal_Data['NOy (ppb)'].groupby(pd.Grouper(freq=NO_Cal_Freq)).max()

Max_NO_Lit_Zero = NOy_Cal_Data['NO_File_Zero'].groupby(pd.Grouper(freq=NO_Cal_Freq)).mean()

Max_NO_Lit_Slope = NOy_Cal_Data['NO_File_Slope'].groupby(pd.Grouper(freq=NO_Cal_Freq)).max()

NOy_Cal_Data = NOy_Cal_Data.groupby(pd.Grouper(freq=NO_Cal_Freq)).mean()

NOy_Cal_Data['NO_Calculated_AutoZero'] = pd.Series(Mean_NO_AutoZero)

NOy_Cal_Data['NO_Calculated_AutoCal'] = pd.Series(Max_NO_AutoCal)

NOy_Cal_Data['NO_Lit_Zero'] = pd.Series(Max_NO_Lit_Zero)

NOy_Cal_Data['NO_Lit_Slope'] = pd.Series(Max_NO_Lit_Slope)

NOy_Cal_Data['NOy Span Cylinder (ppb)'] = float(Conc_NOy_Cal_PPB)

NOy_Cal_Data['NO_Calculated_Response'] = (NOy_Cal_Data['NOy Span Cylinder (ppb)'] + NOy_Cal_Data['NO_Calculated_AutoZero'])/NOy_Cal_Data['NO_Calculated_AutoCal'] 

NOy_Cal_Data['NO_Calculated_Slope'] = NOy_Cal_Data['NOy Span Cylinder (ppb)']/(NOy_Cal_Data['NO_Calculated_AutoCal'] - NOy_Cal_Data['NO_Calculated_AutoZero'])

NOy_Cal_Data['NO_Flag'] = np.where((NOy_Cal_Data['NO_Lit_Slope'].notnull()), 0, 1)

NOy_Cal_Data['NO_Flag'] = np.where((NOy_Cal_Data['NO_Calculated_Slope'].notnull()), 0, NOy_Cal_Data['NO_Flag'])

NOy_Cal_Data.drop(NOy_Cal_Data[(NOy_Cal_Data['NO_Flag'] == 1)].index,inplace =True)

NOy_Cal_Data = NOy_Cal_Data.drop(columns=['NO (ppb)', 'NOy (ppb)', 'NO_File_Zero', 'NO_File_Slope'])

NOy_Old_Data['NOy -1 offset'] = NOy_Old_Data['NOy (ppb)'].shift(periods=-1)
NOy_Old_Data['NOy +1 offset'] = NOy_Old_Data['NOy (ppb)'].shift(periods=1)

NOy_Old_Data['NOy_offset_flags'] = np.where((NOy_Old_Data['NOy (ppb)'].notnull() & NOy_Old_Data['NOy -1 offset'].isnull()), 1, 0)
NOy_Old_Data['NOy_offset_flags'] = np.where((NOy_Old_Data['NOy (ppb)'].notnull() & NOy_Old_Data['NOy +1 offset'].isnull()), 1, NOy_Old_Data['NOy_offset_flags'])

NOy_Old_Data.drop(NOy_Old_Data[(NOy_Old_Data['NOy_offset_flags'] == 0)].index,inplace =True)

NOy_Old_Data = NOy_Old_Data.drop(columns=['NOy -1 offset', 'NOy +1 offset', 'NOy_offset_flags'])

#NOy_Old_Data.to_csv(str(Data_Output_Folder) + '10_NO-NOy_offsets_' + str(current_day) + '_' + str(version_number) + '.csv')
#NOy_Cal_Data.to_csv(str(Data_Output_Folder) + '10_NO-NOy_Prov-Zeros_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

NOy_Cal_Data = pd.concat([NOy_Cal_Data, NOy_Old_Data])

NOy_Cal_Data = NOy_Cal_Data.sort_index()

NOy_Cal_Data['NO_+1_offset'] = NOy_Cal_Data['NO_Lit_Zero'].shift(periods=1)
NOy_Cal_Data['NO_+2_offset'] = NOy_Cal_Data['NO_Lit_Zero'].shift(periods=2)

NOy_Cal_Data['NO_Lit_Zero'] = np.where((NOy_Cal_Data['NO_Lit_Zero'].isnull() & NOy_Cal_Data['NO_+1_offset'].notnull()), NOy_Cal_Data['NO_+1_offset'], NOy_Cal_Data['NO_Lit_Zero'])
NOy_Cal_Data['NO_Lit_Zero'] = np.where((NOy_Cal_Data['NO_Lit_Zero'].isnull() & NOy_Cal_Data['NO_+2_offset'].notnull()), NOy_Cal_Data['NO_+2_offset'], NOy_Cal_Data['NO_Lit_Zero'])

NOy_Cal_Data['NO_+1_offset'] = NOy_Cal_Data['NO_Lit_Slope'].shift(periods=1)
NOy_Cal_Data['NO_+2_offset'] = NOy_Cal_Data['NO_Lit_Slope'].shift(periods=2)

NOy_Cal_Data['NO_Lit_Slope'] = np.where((NOy_Cal_Data['NO_Lit_Slope'].isnull() & NOy_Cal_Data['NO_+1_offset'].notnull()), NOy_Cal_Data['NO_+1_offset'], NOy_Cal_Data['NO_Lit_Slope'])
NOy_Cal_Data['NO_Lit_Slope'] = np.where((NOy_Cal_Data['NO_Lit_Slope'].isnull() & NOy_Cal_Data['NO_+2_offset'].notnull()), NOy_Cal_Data['NO_+2_offset'], NOy_Cal_Data['NO_Lit_Slope'])

NOy_Cal_Data['NO_+1_offset'] = NOy_Cal_Data['NO_Calculated_AutoZero'].shift(periods=1)
NOy_Cal_Data['NO_+2_offset'] = NOy_Cal_Data['NO_Calculated_AutoZero'].shift(periods=2)

NOy_Cal_Data['NO_Calculated_AutoZero'] = np.where((NOy_Cal_Data['NO_Calculated_AutoZero'].isnull() & NOy_Cal_Data['NO_+1_offset'].notnull()), NOy_Cal_Data['NO_+1_offset'], NOy_Cal_Data['NO_Calculated_AutoZero'])
NOy_Cal_Data['NO_Calculated_AutoZero'] = np.where((NOy_Cal_Data['NO_Calculated_AutoZero'].isnull() & NOy_Cal_Data['NO_+2_offset'].notnull()), NOy_Cal_Data['NO_+2_offset'], NOy_Cal_Data['NO_Calculated_AutoZero'])

NOy_Cal_Data['NO_+1_offset'] = NOy_Cal_Data['NO_Calculated_Response'].shift(periods=1)
NOy_Cal_Data['NO_+2_offset'] = NOy_Cal_Data['NO_Calculated_Response'].shift(periods=2)

NOy_Cal_Data['NO_Calculated_Response'] = np.where((NOy_Cal_Data['NO_Calculated_Response'].isnull() & NOy_Cal_Data['NO_+1_offset'].notnull()), NOy_Cal_Data['NO_+1_offset'], NOy_Cal_Data['NO_Calculated_Response'])
NOy_Cal_Data['NO_Calculated_Response'] = np.where((NOy_Cal_Data['NO_Calculated_Response'].isnull() & NOy_Cal_Data['NO_+2_offset'].notnull()), NOy_Cal_Data['NO_+2_offset'], NOy_Cal_Data['NO_Calculated_Response'])

NOy_Cal_Data['NO_+1_offset'] = NOy_Cal_Data['NO_Calculated_Slope'].shift(periods=1)
NOy_Cal_Data['NO_+2_offset'] = NOy_Cal_Data['NO_Calculated_Slope'].shift(periods=2)

NOy_Cal_Data['NO_Calculated_Slope'] = np.where((NOy_Cal_Data['NO_Calculated_Slope'].isnull() & NOy_Cal_Data['NO_+1_offset'].notnull()), NOy_Cal_Data['NO_+1_offset'], NOy_Cal_Data['NO_Calculated_Slope'])
NOy_Cal_Data['NO_Calculated_Slope'] = np.where((NOy_Cal_Data['NO_Calculated_Slope'].isnull() & NOy_Cal_Data['NO_+2_offset'].notnull()), NOy_Cal_Data['NO_+2_offset'], NOy_Cal_Data['NO_Calculated_Slope'])

NOy_Cal_Data['NOy_offset_flags'] = np.where((NOy_Cal_Data['NO_+1_offset'].isnull() & NOy_Cal_Data['NO_+2_offset'].isnull()), 1, 0)

NOy_Cal_Data.drop(NOy_Cal_Data[(NOy_Cal_Data['NOy_offset_flags'] == 1)].index,inplace =True)

NOy_Cal_drop_list = list(NOy_Cal_Data.columns.values)
NOy_Cal_drop_list.remove('NO_Lit_Zero')
NOy_Cal_drop_list.remove('NO_Lit_Slope')
NOy_Cal_drop_list.remove('NO_Calculated_AutoZero')
#NOy_Cal_drop_list.remove('NO_Calculated_Response')
NOy_Cal_drop_list.remove('NO_Calculated_Slope')
NOy_Cal_Data = NOy_Cal_Data.drop(columns=NOy_Cal_drop_list)


year_Audit_1 = 2019 #input the year of Audit
month_Audit_1 = 8 #input the month of Audit
day_Audit_1 = 9 #input the day of Audit

#Calibration Day 2
year_Audit_2 = 2020 #input the year of study
month_Audit_2 = 3 #input the month of study
day_Audit_2 = 18 #default start date set

#Calibration Day 3
year_Audit_3 = 2020 #input the year of study
month_Audit_3 = 10 #input the month of study
day_Audit_3 = 2 #default start date set

#Audit 4
year_Audit_4 = 2021 #input the year of study
month_Audit_4 = 3 #input the month of study
day_Audit_4 = 30 #default start date set

#Audit 5
year_Audit_5 = 2021 #input the year of study
month_Audit_5 = 10 #input the month of study
day_Audit_5 = 27 #default start date set

start_Audit_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,10,00)
end_Audit_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,11,18,00)
NOy_Cal_Data.drop(NOy_Cal_Data.loc[start_Audit_1:end_Audit_1].index, inplace=True)

start_Audit_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,9,28,00)
end_Audit_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,14,35,00)
NOy_Cal_Data.drop(NOy_Cal_Data.loc[start_Audit_2:end_Audit_2].index, inplace=True)

start_Audit_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,24,00)
end_Audit_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,10,44,00)
NOy_Cal_Data.drop(NOy_Cal_Data.loc[start_Audit_3:end_Audit_3].index, inplace=True)

start_Audit_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,5,00)
end_Audit_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,14,40,00)
NOy_Cal_Data.drop(NOy_Cal_Data.loc[start_Audit_4:end_Audit_4].index, inplace=True)

start_Audit_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,7,26,00)
end_Audit_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,11,13,00)
NOy_Cal_Data.drop(NOy_Cal_Data.loc[start_Audit_5:end_Audit_5].index, inplace=True)

#Audit 5
year_Audit_6 = 2022 #input the year of study
month_Audit_6 = 5 #input the month of study
day_Audit_6 = 4 #default start date set

start_Audit_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,8,30,00)
end_Audit_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,12,13,00)
NOy_Cal_Data.drop(NOy_Cal_Data.loc[start_Audit_6:end_Audit_6].index, inplace=True)

#NOy_Cal_Data = NOy_Cal_Data.drop(columns=['NO_Calculated_Slope'])

NOy_Cal_Data = NOy_Cal_Data[['NO_Lit_Zero', 'NO_Lit_Slope', 'NO_Calculated_AutoZero', 'NO_Calculated_Slope']]

NOy_Cal_Data['datetime'] = NOy_Cal_Data.index

#NOy_Cal_Data.to_csv(str(Data_Output_Folder) + '9_NO-NOy_Auto-Zeros_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

pattern = str(Data_Source_Folder) + '202*_firsgas.csv'# Collect CSV files

print(str(pattern))

csv_files = glob.glob(pattern)

gas_frames = []

for csv in csv_files:
    
    #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv, header=None, usecols=[0,1,12,20])
    gas_frames.append(df)

CO_Cal_Data = pd.concat(gas_frames)

CO_Cal_Data.rename(columns={0: 'Date'}, inplace=True)
CO_Cal_Data.rename(columns={1: 'Time'}, inplace=True)
CO_Cal_Data.rename(columns={12: 'CO (ppb)'}, inplace=True)
CO_Cal_Data.rename(columns={20: 'CO_Status'}, inplace=True)

CO_Cal_Data.drop(CO_Cal_Data[(CO_Cal_Data['CO (ppb)'] == 'S2 CO (ppb)')].index,inplace =True)

CO_Cal_Data['Date'] = CO_Cal_Data['Date'].astype(str)
CO_Cal_Data['Date_length'] = CO_Cal_Data['Date'].str.len()
CO_Cal_Data=CO_Cal_Data.loc[CO_Cal_Data.Date_length == 10] #check the data string length for corruption
CO_Cal_Data['datetime'] = CO_Cal_Data['Date']+' '+ CO_Cal_Data['Time']# added Date and time into new columns
CO_Cal_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in CO_Cal_Data['datetime']] #converts the dateTime format from string to python dateTime
CO_Cal_Data.index = CO_Cal_Data['datetime']
CO_Cal_Data = CO_Cal_Data.sort_index()
CO_Cal_Data = CO_Cal_Data.drop(columns=['Date_length', 'Date', 'Time'])

CO_Other_Cal=CO_Cal_Data.loc[CO_Cal_Data.CO_Status == '8C050400']

CO_Cal_Data=CO_Cal_Data.loc[CO_Cal_Data.CO_Status == '8C050000']

CO_Cal_Data = pd.concat([CO_Cal_Data, CO_Other_Cal])
CO_Cal_Data = CO_Cal_Data.sort_index()

Original_CO_Cal = str(Data_Source_Folder) + 'Cal_Record.csv' # Needs to be address of data location - Collect CSV files
Original_CO_Cal_Files = glob.glob(Original_CO_Cal)

# Create an empty list
frames = []

#  Iterate over csv_files
for csv in Original_CO_Cal_Files:
    df = pd.read_csv(csv) #
    frames.append(df)

Automated_Cal = pd.concat(frames)
Automated_Cal.rename(columns={0: 'Date'}, inplace=True)
Automated_Cal.rename(columns={1: 'Time'}, inplace=True)

Automated_Cal['Date'] = Automated_Cal['Date'].astype(str)
Automated_Cal['Date_length'] = Automated_Cal['Date'].str.len()
Automated_Cal=Automated_Cal.loc[Automated_Cal.Date_length == 10] #check the data string length for corruption
Automated_Cal['datetime'] = Automated_Cal['Date']+ ' ' + Automated_Cal['Time'] # added Date and time into new columns
Automated_Cal['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in Automated_Cal['datetime']] #converts the dateTime format from string to python dateTime
Automated_Cal.index = Automated_Cal['datetime']
Automated_Cal = Automated_Cal.sort_index()

Automated_Cal.rename(columns={'S2_CO_Zero': 'CO_Zero'}, inplace=True)
Automated_Cal['CO_Zero'] = Automated_Cal['CO_Zero'].astype(float)

Cal_drop_list = list(Automated_Cal.columns.values)
Cal_drop_list.remove('CO_Zero')
#Cal_drop_list.remove('datetime')
Automated_Cal = Automated_Cal.drop(columns=Cal_drop_list)
Automated_Cal.drop(Automated_Cal[(Automated_Cal['CO_Zero'] == 0)].index,inplace =True)

Automated_Cal['CO_+1_offset'] = Automated_Cal['CO_Zero'].shift(periods=1)
Automated_Cal['CO_Log_Flag'] = np.where((Automated_Cal['CO_+1_offset'] == Automated_Cal['CO_Zero']), 2, 1)

Automated_Cal.drop(Automated_Cal[(Automated_Cal['CO_Log_Flag'] == 2)].index,inplace =True)
Automated_Cal = Automated_Cal.drop(columns=['CO_+1_offset', 'CO_Log_Flag'])

CO_Cal_Data['CO (ppb)'] = CO_Cal_Data['CO (ppb)'].astype(float)
CO_Cal_Data.drop(CO_Cal_Data[(CO_Cal_Data['CO (ppb)'] == 0)].index,inplace =True)

CO_Cal_Data['CO_Flag_No'] = np.where(CO_Cal_Data['CO_Status'] == '8C050400', 2, 1) #either '8C050400' or '8C050000'
Max_CO_Flag = CO_Cal_Data['CO_Flag_No'].groupby(pd.Grouper(freq=av_Freq)).max()

CO_Cal_Data = CO_Cal_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
CO_Cal_Data['CO_Flag_No'] = pd.Series(Max_CO_Flag)
CO_Cal_Data['CO_Status'] = np.where(CO_Cal_Data['CO_Flag_No'] == 2, '8C050400', '8C050000')

CO_Cal_Data['datetime'] = CO_Cal_Data.index
CO_Cal_Data['CO_Alignment_Flags'] = np.where(CO_Cal_Data['CO (ppb)'].notnull(), 1, 0)

CO_Cal_Data['CO_+1_offset'] = CO_Cal_Data['CO (ppb)'].shift(periods=1)
CO_Cal_Data['CO_+2_offset'] = CO_Cal_Data['CO (ppb)'].shift(periods=2)
CO_Cal_Data['CO_Alignment_Flags'] = np.where((CO_Cal_Data['CO_+1_offset'].isnull() & CO_Cal_Data['CO (ppb)'].notnull()), 2, CO_Cal_Data['CO_Alignment_Flags'])
CO_Cal_Data['CO_Alignment_Flags'] = np.where((CO_Cal_Data['CO_+2_offset'].isnull() & CO_Cal_Data['CO (ppb)'].notnull()), 2, CO_Cal_Data['CO_Alignment_Flags'])

CO_Cal_Data['CO (ppb)'] = np.where(CO_Cal_Data['CO_Alignment_Flags'] ==2, np.nan, CO_Cal_Data['CO (ppb)'])

CO_Cal_Data['CO_-1_offset'] = CO_Cal_Data['CO (ppb)'].shift(periods=-1)
CO_Cal_Data['CO_Alignment_Flags'] = np.where((CO_Cal_Data['CO_-1_offset'].isnull() & CO_Cal_Data['CO (ppb)'].notnull()), 2, CO_Cal_Data['CO_Alignment_Flags'])

CO_Cal_Data = CO_Cal_Data.drop(columns=['CO_+1_offset', 'CO_+2_offset', 'CO_-1_offset'])

Auto_Zero_Length = '180min'

Min_CO_AutoZero = CO_Cal_Data['CO (ppb)'].groupby(pd.Grouper(freq=Auto_Zero_Length)).min()

CO_Cal_Data['Min_CO_AutoZero'] = pd.Series(Min_CO_AutoZero)

Mean_CO_AutoZero = CO_Cal_Data['CO (ppb)'].groupby(pd.Grouper(freq=Auto_Zero_Length)).mean()

CO_Cal_Data['Mean_CO_AutoZero'] = pd.Series(Mean_CO_AutoZero)

CO_Cal_Data['CO_Alignment_Flags'] = np.where((CO_Cal_Data['Mean_CO_AutoZero'].isnull() & (CO_Cal_Data['CO_Alignment_Flags'] == 1)), 3, CO_Cal_Data['CO_Alignment_Flags'])
CO_Cal_Data['CO_Alignment_Flags'] = np.where((CO_Cal_Data['CO (ppb)'].isnull() & CO_Cal_Data['Mean_CO_AutoZero'].notnull() & (CO_Cal_Data['CO_Alignment_Flags'] == 0)), 4, CO_Cal_Data['CO_Alignment_Flags'])

CO_Cal_Data.drop(CO_Cal_Data[(CO_Cal_Data.CO_Alignment_Flags == 0)].index,inplace =True)

CO_Cal_Data.drop(CO_Cal_Data[(CO_Cal_Data.CO_Alignment_Flags == 3)].index,inplace =True)

CO_Cal_Data['Min_CO_+1_offset'] = CO_Cal_Data['Min_CO_AutoZero'].shift(periods=1)
CO_Cal_Data['Mean_CO_+1_offset'] = CO_Cal_Data['Mean_CO_AutoZero'].shift(periods=1)
CO_Cal_Data['Flag_CO_+1_offset'] = CO_Cal_Data['CO_Alignment_Flags'].shift(periods=1)
CO_Cal_Data['Min_CO_AutoZero'] = np.where(CO_Cal_Data['Flag_CO_+1_offset'] == 4, CO_Cal_Data['Min_CO_+1_offset'], CO_Cal_Data['Min_CO_AutoZero'])
CO_Cal_Data['Mean_CO_AutoZero'] = np.where(CO_Cal_Data['Flag_CO_+1_offset'] == 4, CO_Cal_Data['Mean_CO_+1_offset'], CO_Cal_Data['Mean_CO_AutoZero'])

CO_Cal_Data.drop(CO_Cal_Data[(CO_Cal_Data.CO_Alignment_Flags == 4)].index,inplace =True)

CO_Cal_Data['Flag_CO_-1_offset'] = CO_Cal_Data['CO_Alignment_Flags'].shift(periods=-1)
CO_Cal_Data.drop(CO_Cal_Data[(CO_Cal_Data['Flag_CO_-1_offset'] == 1)].index,inplace =True)
CO_Cal_Data = CO_Cal_Data.drop(columns=['Min_CO_+1_offset', 'Mean_CO_+1_offset', 'Flag_CO_+1_offset', 'Flag_CO_-1_offset'])
CO_Cal_Data['CO_Alignment_Flags'] = np.where(CO_Cal_Data['CO_Alignment_Flags'] == 1, 2, CO_Cal_Data['CO_Alignment_Flags'])
CO_Cal_Data.drop(CO_Cal_Data[(CO_Cal_Data['Mean_CO_AutoZero'].isnull())].index,inplace =True)
CO_Cal_Data = CO_Cal_Data.drop(columns=['CO (ppb)', 'CO_Alignment_Flags'])
Old_CO_Cal = CO_Cal_Data
CO_Cal_Data = CO_Cal_Data.drop(columns=['Mean_CO_AutoZero'])

CO_Cal_Data = pd.concat([CO_Cal_Data, Automated_Cal])
CO_Cal_Data = CO_Cal_Data.sort_index()

CO_Cal_Data.rename(columns={'Min_CO_AutoZero' : 'CO Data Zero (ppb)'}, inplace=True)
#CO_Cal_Data.rename(columns={'CO Logfile Zero (ppb)' : 'CO_Zero'}, inplace=True)

CO_Cal_Data['CO_-1_offset'] = CO_Cal_Data['CO_Zero'].shift(periods=-1)
CO_Cal_Data['CO_+1_offset'] = CO_Cal_Data['CO_Zero'].shift(periods=1)

CO_Cal_Data['CO Logfile Zero (ppb)'] = np.where((CO_Cal_Data['CO_+1_offset'].notnull() & CO_Cal_Data['CO Data Zero (ppb)'].notnull()), CO_Cal_Data['CO_+1_offset'], np.nan)
CO_Cal_Data['CO Logfile Zero (ppb)'] = np.where((CO_Cal_Data['CO_-1_offset'].notnull() & CO_Cal_Data['CO Data Zero (ppb)'].notnull()), CO_Cal_Data['CO_-1_offset'], CO_Cal_Data['CO Logfile Zero (ppb)'])

#CO_Cal_Data['CO_Zero_Flags'] = np.where((CO_Cal_Data['CO (ppb)'].isnull() & CO_Cal_Data['CO_Zero'].isnull()), 1, 0)
#CO_Cal_Data = CO_Cal_Data.loc[CO_Cal_Data.CO_Zero_Flags == 0] 
#CO_Cal_Data = CO_Cal_Data.drop(columns=['CO_Zero_Flags'])

CO_Cal_Data.drop(CO_Cal_Data[(CO_Cal_Data['CO Data Zero (ppb)'].isnull())].index,inplace =True)

CO_Cal_Data = CO_Cal_Data.drop(columns=['CO_-1_offset', 'CO_+1_offset', 'CO_Zero'])
    
CO_Cal_Data['CO Logfile Zero (ppb)'] = np.where((CO_Cal_Data['CO Logfile Zero (ppb)'].isnull()), CO_Cal_Data['CO Data Zero (ppb)'], CO_Cal_Data['CO Logfile Zero (ppb)'])

#CO_Cal_Data.to_csv(str(Data_Output_Folder) + '8_CO_Auto-Zeros_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

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

#Audit 5
year_Audit_5 = 2021 #input the year of study
month_Audit_5 = 10 #input the month of study
day_Audit_5 = 27 #default start date set

start_Audit_Day_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,0,0,00)
end_Audit_Day_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,23,59,00)

#Audit 6
year_Audit_6 = 2022 #input the year of study
month_Audit_6 = 5 #input the month of study
day_Audit_6 = 4 #default start date set

start_Audit_Day_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,0,0,00)
end_Audit_Day_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,23,59,00)

#day of gas to firsgas happens on 14/11/2019

start = start_Audit_Day_1
end = end_Audit_Day_1

Audit_Date_Str = start.strftime("%Y-%m-%d")

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))
    
prior_date_1 = start - timedelta(days=1)
prior_day_1_str = str(prior_date_1.strftime("%Y")) + str(prior_date_1.strftime("%m")) + str(prior_date_1.strftime("%d"))

prior_date_2 = start - timedelta(days=2)
prior_day_2_str = str(prior_date_2.strftime("%Y")) + str(prior_date_2.strftime("%m")) + str(prior_date_2.strftime("%d"))

if end <= Start_of_file_change:
    if start_Audit_str == end_Audit_str: # if audit occurs over the same day
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_gas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_gas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_gas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    else: # if audit occurs over two days
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_gas.csv'
        Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_gas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_gas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_gas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)

    gas_frames = []
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,12,13,14,15,16,17])
        gas_frames.append(df)
        
    early_Data = pd.concat(gas_frames)
    
    early_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'NO (ppb)', 3: 'Diff (ppb)', 4: 'NOy (ppb)', 5: 'NOy Flow (l/min)'}, inplace=True)
    early_Data.rename(columns={6: 'NOy Pressure (mmHG)', 12: 'NO2 (ppb)', 13: 'Ozone (ppb)', 14: 'NOy Flags', 15: 'NO2 Status', 16: 'O3 Flags'}, inplace=True)
    
    early_Data['Date'] = early_Data['Date'].astype(str)
    early_Data['Date_length'] = early_Data['Date'].str.len()
    early_Data=early_Data.loc[early_Data.Date_length == 10] #check the data string length for corruption
    early_Data['datetime'] = early_Data['Date']+' '+early_Data['Time']# added Date and time into new columns
    early_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in early_Data['datetime']] #converts the dateTime format from string to python dateTime
    early_Data.index = early_Data['datetime']
    early_Data = early_Data.sort_index()
    early_Data = early_Data.drop(columns=['Date', 'Time','Date_length'])
    
    early_Data['CO (ppb)'] = np.nan
    early_Data['CO Flags'] = 0
    all_Data = early_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','NO2 (ppb)', 'NO2 Status','Ozone (ppb)', 'O3 Flags','CO (ppb)', 'CO Flags','datetime']]
    
#    NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
#    NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime']]
#    Ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime']]
#    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime']]

elif start >= End_of_file_change:
    if start_Audit_str == end_Audit_str: # if audit occurs over the same day
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_firsgas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_firsgas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_firsgas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    else: # if audit occurs over two days
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_firsgas.csv'
        Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_firsgas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_firsgas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_firsgas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    
    gas_frames = []
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,7,8,12,16,17,18,20])
        gas_frames.append(df)
        
    all_Data = pd.concat(gas_frames)
    
    all_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'NO (ppb)', 3: 'Diff (ppb)', 4: 'NOy (ppb)', 5: 'NOy Flow (l/min)', 6: 'NOy Pressure (mmHG)'}, inplace=True)
    all_Data.rename(columns={7: 'NO2 (ppb)', 8: 'Ozone (ppb)', 12: 'CO (ppb)', 16: 'NOy Flags', 17: 'O3 Flags', 18: 'NO2 Status', 20: 'CO Flags'}, inplace=True)
    
    all_Data['Date'] = all_Data['Date'].astype(str)
    all_Data['Date_length'] = all_Data['Date'].str.len()
    all_Data=all_Data.loc[all_Data.Date_length == 10] #check the data string length for corruption
    all_Data['datetime'] = all_Data['Date']+' '+all_Data['Time']# added Date and time into new columns
    all_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in all_Data['datetime']] #converts the dateTime format from string to python dateTime
    all_Data.index = all_Data['datetime']
    all_Data = all_Data.sort_index()
    all_Data = all_Data.drop(columns=['Date', 'Time','Date_length'])
    
    all_Data['CO Flags'] = all_Data['CO Flags'].astype(str)
    all_Data['CO_Flags_Prov'] = np.where(all_Data['CO Flags'] == 'FFFFFFFF', 0, all_Data['CO Flags'])
    all_Data['CO Flags'] = all_Data['CO_Flags_Prov']
    all_Data['CO (ppb)'] = np.where(all_Data['CO Flags'] == 0, np.nan, all_Data['CO (ppb)'])
    
#    NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
#    NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime']]
#    Ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime']]
#    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime']]
    
else:
    print('Data Not Found for ' + str(Audit_Date_Str))

all_Data = all_Data[start:end]
Audit_1_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','NO2 (ppb)', 'NO2 Status','Ozone (ppb)', 'O3 Flags','CO (ppb)', 'CO Flags','datetime']]

#NOy_Audit_1 = NOy_Data
#NO2_Audit_1 = NO2_Data
#Ozone_Audit_1 = Ozone_Data
#CO_Audit_1 = CO_Data

start = start_Audit_Day_2
end = end_Audit_Day_2

Audit_Date_Str = start.strftime("%Y-%m-%d")

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))
    
prior_date_1 = start - timedelta(days=1)
prior_day_1_str = str(prior_date_1.strftime("%Y")) + str(prior_date_1.strftime("%m")) + str(prior_date_1.strftime("%d"))

prior_date_2 = start - timedelta(days=2)
prior_day_2_str = str(prior_date_2.strftime("%Y")) + str(prior_date_2.strftime("%m")) + str(prior_date_2.strftime("%d"))

if end <= Start_of_file_change:
    if start_Audit_str == end_Audit_str: # if audit occurs over the same day
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_gas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_gas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_gas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    else: # if audit occurs over two days
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_gas.csv'
        Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_gas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_gas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_gas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)

    gas_frames = []
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,12,13,14,15,16,17])
        gas_frames.append(df)
        
    early_Data = pd.concat(gas_frames)
    
    early_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'NO (ppb)', 3: 'Diff (ppb)', 4: 'NOy (ppb)', 5: 'NOy Flow (l/min)'}, inplace=True)
    early_Data.rename(columns={6: 'NOy Pressure (mmHG)', 12: 'NO2 (ppb)', 13: 'Ozone (ppb)', 14: 'NOy Flags', 15: 'NO2 Status', 16: 'O3 Flags'}, inplace=True)
    
    early_Data['Date'] = early_Data['Date'].astype(str)
    early_Data['Date_length'] = early_Data['Date'].str.len()
    early_Data=early_Data.loc[early_Data.Date_length == 10] #check the data string length for corruption
    early_Data['datetime'] = early_Data['Date']+' '+early_Data['Time']# added Date and time into new columns
    early_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in early_Data['datetime']] #converts the dateTime format from string to python dateTime
    early_Data.index = early_Data['datetime']
    early_Data = early_Data.sort_index()
    early_Data = early_Data.drop(columns=['Date', 'Time','Date_length'])
    
    early_Data['CO (ppb)'] = np.nan
    early_Data['CO Flags'] = 0
    
    all_Data = early_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','NO2 (ppb)', 'NO2 Status','Ozone (ppb)', 'O3 Flags','CO (ppb)', 'CO Flags','datetime']]
    
#    NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
#    NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime']]
#    Ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime']]
#    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime']]

elif start >= End_of_file_change:
    if start_Audit_str == end_Audit_str: # if audit occurs over the same day
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_firsgas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_firsgas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_firsgas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_day_1_pattern) # + glob.glob(prior_day_2_pattern)
    else: # if audit occurs over two days
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_firsgas.csv'
        Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_firsgas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_firsgas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_firsgas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    
    gas_frames = []
    
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,7,8,12,16,17,18,20])
        gas_frames.append(df)
        
    all_Data = pd.concat(gas_frames)
    
    all_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'NO (ppb)', 3: 'Diff (ppb)', 4: 'NOy (ppb)', 5: 'NOy Flow (l/min)', 6: 'NOy Pressure (mmHG)'}, inplace=True)
    all_Data.rename(columns={7: 'NO2 (ppb)', 8: 'Ozone (ppb)', 12: 'CO (ppb)', 16: 'NOy Flags', 17: 'O3 Flags', 18: 'NO2 Status', 20: 'CO Flags'}, inplace=True)
    
    all_Data['Date'] = all_Data['Date'].astype(str)
    all_Data['Date_length'] = all_Data['Date'].str.len()
    all_Data=all_Data.loc[all_Data.Date_length == 10] #check the data string length for corruption
    all_Data['datetime'] = all_Data['Date']+' '+all_Data['Time']# added Date and time into new columns
    all_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in all_Data['datetime']] #converts the dateTime format from string to python dateTime
    all_Data.index = all_Data['datetime']
    all_Data = all_Data.sort_index()
    all_Data = all_Data.drop(columns=['Date', 'Time','Date_length'])
    
    all_Data['CO Flags'] = all_Data['CO Flags'].astype(str)
    all_Data['CO_Flags_Prov'] = np.where(all_Data['CO Flags'] == 'FFFFFFFF', 0, all_Data['CO Flags'])
    all_Data['CO Flags'] = all_Data['CO_Flags_Prov']
    all_Data['CO (ppb)'] = np.where(all_Data['CO Flags'] == 0, np.nan, all_Data['CO (ppb)'])
    
#    NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
#    NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime']]
#    Ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime']]
#    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime']]
    
else:
    print('Data Not Found for ' + str(Audit_Date_Str))

all_Data = all_Data[start:end]
Audit_2_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','NO2 (ppb)', 'NO2 Status','Ozone (ppb)', 'O3 Flags','CO (ppb)', 'CO Flags','datetime']]

#NOy_Audit_2 = NOy_Data
#NO2_Audit_2 = NO2_Data
#Ozone_Audit_2 = Ozone_Data
#CO_Audit_2 = CO_Data

start = start_Audit_Day_3
end = end_Audit_Day_3

Audit_Date_Str = start.strftime("%Y-%m-%d")

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))
    
prior_date_1 = start - timedelta(days=1)
prior_day_1_str = str(prior_date_1.strftime("%Y")) + str(prior_date_1.strftime("%m")) + str(prior_date_1.strftime("%d"))

prior_date_2 = start - timedelta(days=2)
prior_day_2_str = str(prior_date_2.strftime("%Y")) + str(prior_date_2.strftime("%m")) + str(prior_date_2.strftime("%d"))

if end <= Start_of_file_change:
    if start_Audit_str == end_Audit_str: # if audit occurs over the same day
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_gas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_gas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_gas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    else: # if audit occurs over two days
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_gas.csv'
        Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_gas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_gas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_gas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)

    gas_frames = []
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,12,13,14,15,16,17])
        gas_frames.append(df)
        
    early_Data = pd.concat(gas_frames)
    
    early_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'NO (ppb)', 3: 'Diff (ppb)', 4: 'NOy (ppb)', 5: 'NOy Flow (l/min)'}, inplace=True)
    early_Data.rename(columns={6: 'NOy Pressure (mmHG)', 12: 'NO2 (ppb)', 13: 'Ozone (ppb)', 14: 'NOy Flags', 15: 'NO2 Status', 16: 'O3 Flags'}, inplace=True)
    
    early_Data['Date'] = early_Data['Date'].astype(str)
    early_Data['Date_length'] = early_Data['Date'].str.len()
    early_Data=early_Data.loc[early_Data.Date_length == 10] #check the data string length for corruption
    early_Data['datetime'] = early_Data['Date']+' '+early_Data['Time']# added Date and time into new columns
    early_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in early_Data['datetime']] #converts the dateTime format from string to python dateTime
    early_Data.index = early_Data['datetime']
    early_Data = early_Data.sort_index()
    early_Data = early_Data.drop(columns=['Date', 'Time','Date_length'])
    
    early_Data['CO (ppb)'] = np.nan
    early_Data['CO Flags'] = 0
    
    all_Data = early_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','NO2 (ppb)', 'NO2 Status','Ozone (ppb)', 'O3 Flags','CO (ppb)', 'CO Flags','datetime']]
    
#    NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
#    NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime']]
#    Ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime']]
#    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime']]

elif start >= End_of_file_change:
    if start_Audit_str == end_Audit_str: # if audit occurs over the same day
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_firsgas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_firsgas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_firsgas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    else: # if audit occurs over two days
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_firsgas.csv'
        Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_firsgas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_firsgas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_firsgas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    
    gas_frames = []
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,7,8,12,16,17,18,20])
        gas_frames.append(df)
        
    all_Data = pd.concat(gas_frames)
    
    all_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'NO (ppb)', 3: 'Diff (ppb)', 4: 'NOy (ppb)', 5: 'NOy Flow (l/min)', 6: 'NOy Pressure (mmHG)'}, inplace=True)
    all_Data.rename(columns={7: 'NO2 (ppb)', 8: 'Ozone (ppb)', 12: 'CO (ppb)', 16: 'NOy Flags', 17: 'O3 Flags', 18: 'NO2 Status', 20: 'CO Flags'}, inplace=True)
    
    all_Data['Date'] = all_Data['Date'].astype(str)
    all_Data['Date_length'] = all_Data['Date'].str.len()
    all_Data=all_Data.loc[all_Data.Date_length == 10] #check the data string length for corruption
    all_Data['datetime'] = all_Data['Date']+' '+all_Data['Time']# added Date and time into new columns
    all_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in all_Data['datetime']] #converts the dateTime format from string to python dateTime
    all_Data.index = all_Data['datetime']
    all_Data = all_Data.sort_index()
    all_Data = all_Data.drop(columns=['Date', 'Time','Date_length'])
    
    all_Data['CO Flags'] = all_Data['CO Flags'].astype(str)
    all_Data['CO_Flags_Prov'] = np.where(all_Data['CO Flags'] == 'FFFFFFFF', 0, all_Data['CO Flags'])
    all_Data['CO Flags'] = all_Data['CO_Flags_Prov']
    all_Data['CO (ppb)'] = np.where(all_Data['CO Flags'] == 0, np.nan, all_Data['CO (ppb)'])
    
#    NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
#    NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime']]
#    Ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime']]
#    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime']]
    
else:
    print('Data Not Found for ' + str(Audit_Date_Str))

all_Data = all_Data[start:end]
Audit_3_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','NO2 (ppb)', 'NO2 Status','Ozone (ppb)', 'O3 Flags','CO (ppb)', 'CO Flags','datetime']]

#NOy_Audit_3 = NOy_Data
#NO2_Audit_3 = NO2_Data
#Ozone_Audit_3 = Ozone_Data
#CO_Audit_3 = CO_Data


start = start_Audit_Day_4
end = end_Audit_Day_4

Audit_Date_Str = start.strftime("%Y-%m-%d")

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))
    
prior_date_1 = start - timedelta(days=1)
prior_day_1_str = str(prior_date_1.strftime("%Y")) + str(prior_date_1.strftime("%m")) + str(prior_date_1.strftime("%d"))

prior_date_2 = start - timedelta(days=2)
prior_day_2_str = str(prior_date_2.strftime("%Y")) + str(prior_date_2.strftime("%m")) + str(prior_date_2.strftime("%d"))

if end <= Start_of_file_change:
    if start_Audit_str == end_Audit_str: # if audit occurs over the same day
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_gas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_gas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_gas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    else: # if audit occurs over two days
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_gas.csv'
        Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_gas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_gas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_gas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)

    gas_frames = []
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,12,13,14,15,16,17])
        gas_frames.append(df)
        
    early_Data = pd.concat(gas_frames)
    
    early_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'NO (ppb)', 3: 'Diff (ppb)', 4: 'NOy (ppb)', 5: 'NOy Flow (l/min)'}, inplace=True)
    early_Data.rename(columns={6: 'NOy Pressure (mmHG)', 12: 'NO2 (ppb)', 13: 'Ozone (ppb)', 14: 'NOy Flags', 15: 'NO2 Status', 16: 'O3 Flags'}, inplace=True)
    
    early_Data['Date'] = early_Data['Date'].astype(str)
    early_Data['Date_length'] = early_Data['Date'].str.len()
    early_Data=early_Data.loc[early_Data.Date_length == 10] #check the data string length for corruption
    early_Data['datetime'] = early_Data['Date']+' '+early_Data['Time']# added Date and time into new columns
    early_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in early_Data['datetime']] #converts the dateTime format from string to python dateTime
    early_Data.index = early_Data['datetime']
    early_Data = early_Data.sort_index()
    early_Data = early_Data.drop(columns=['Date', 'Time','Date_length'])
    
    early_Data['CO (ppb)'] = np.nan
    early_Data['CO Flags'] = 0
    
    all_Data = early_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','NO2 (ppb)', 'NO2 Status','Ozone (ppb)', 'O3 Flags','CO (ppb)', 'CO Flags','datetime']]
    
#    NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
#    NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime']]
#    Ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime']]
#    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime']]

elif start >= End_of_file_change:
    if start_Audit_str == end_Audit_str: # if audit occurs over the same day
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_firsgas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_firsgas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_firsgas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    else: # if audit occurs over two days
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_firsgas.csv'
        Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_firsgas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_firsgas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_firsgas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    
    gas_frames = []
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,7,8,12,16,17,18,20])
        gas_frames.append(df)
        
    all_Data = pd.concat(gas_frames)
    
    all_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'NO (ppb)', 3: 'Diff (ppb)', 4: 'NOy (ppb)', 5: 'NOy Flow (l/min)', 6: 'NOy Pressure (mmHG)'}, inplace=True)
    all_Data.rename(columns={7: 'NO2 (ppb)', 8: 'Ozone (ppb)', 12: 'CO (ppb)', 16: 'NOy Flags', 17: 'O3 Flags', 18: 'NO2 Status', 20: 'CO Flags'}, inplace=True)
    
    all_Data['Date'] = all_Data['Date'].astype(str)
    all_Data['Date_length'] = all_Data['Date'].str.len()
    all_Data=all_Data.loc[all_Data.Date_length == 10] #check the data string length for corruption
    all_Data['datetime'] = all_Data['Date']+' '+all_Data['Time']# added Date and time into new columns
    all_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in all_Data['datetime']] #converts the dateTime format from string to python dateTime
    all_Data.index = all_Data['datetime']
    all_Data = all_Data.sort_index()
    all_Data = all_Data.drop(columns=['Date', 'Time','Date_length'])
    
    all_Data['CO Flags'] = all_Data['CO Flags'].astype(str)
    all_Data['CO_Flags_Prov'] = np.where(all_Data['CO Flags'] == 'FFFFFFFF', 0, all_Data['CO Flags'])
    all_Data['CO Flags'] = all_Data['CO_Flags_Prov']
    all_Data['CO (ppb)'] = np.where(all_Data['CO Flags'] == 0, np.nan, all_Data['CO (ppb)'])
    
#    NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
#    NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime']]
#    Ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime']]
#    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime']]
    
else:
    print('Data Not Found for ' + str(Audit_Date_Str))

all_Data = all_Data[start:end]
Audit_4_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','NO2 (ppb)', 'NO2 Status', 'Ozone (ppb)', 'O3 Flags','CO (ppb)', 'CO Flags','datetime']]

#NOy_Audit_4 = NOy_Data
#NO2_Audit_4 = NO2_Data
#Ozone_Audit_4 = Ozone_Data
#CO_Audit_4 = CO_Data

start = start_Audit_Day_5
end = end_Audit_Day_5

Audit_Date_Str = start.strftime("%Y-%m-%d")

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))
    
prior_date_1 = start - timedelta(days=1)
prior_day_1_str = str(prior_date_1.strftime("%Y")) + str(prior_date_1.strftime("%m")) + str(prior_date_1.strftime("%d"))

prior_date_2 = start - timedelta(days=2)
prior_day_2_str = str(prior_date_2.strftime("%Y")) + str(prior_date_2.strftime("%m")) + str(prior_date_2.strftime("%d"))

if end <= Start_of_file_change:
    if start_Audit_str == end_Audit_str: # if audit occurs over the same day
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_gas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_gas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_gas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    else: # if audit occurs over two days
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_gas.csv'
        Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_gas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_gas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_gas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)

    gas_frames = []
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,12,13,14,15,16,17])
        gas_frames.append(df)
        
    early_Data = pd.concat(gas_frames)
    
    early_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'NO (ppb)', 3: 'Diff (ppb)', 4: 'NOy (ppb)', 5: 'NOy Flow (l/min)'}, inplace=True)
    early_Data.rename(columns={6: 'NOy Pressure (mmHG)', 12: 'NO2 (ppb)', 13: 'Ozone (ppb)', 14: 'NOy Flags', 15: 'NO2 Status', 16: 'O3 Flags'}, inplace=True)
    
    early_Data['Date'] = early_Data['Date'].astype(str)
    early_Data['Date_length'] = early_Data['Date'].str.len()
    early_Data=early_Data.loc[early_Data.Date_length == 10] #check the data string length for corruption
    early_Data['datetime'] = early_Data['Date']+' '+early_Data['Time']# added Date and time into new columns
    early_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in early_Data['datetime']] #converts the dateTime format from string to python dateTime
    early_Data.index = early_Data['datetime']
    early_Data = early_Data.sort_index()
    early_Data = early_Data.drop(columns=['Date', 'Time','Date_length'])
    
    early_Data['CO (ppb)'] = np.nan
    early_Data['CO Flags'] = 0
    
    all_Data = early_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','NO2 (ppb)', 'NO2 Status','Ozone (ppb)', 'O3 Flags','CO (ppb)', 'CO Flags','datetime']]
    
#    NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
#    NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime']]
#    Ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime']]
#    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime']]

elif start >= End_of_file_change:
    if start_Audit_str == end_Audit_str: # if audit occurs over the same day
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_firsgas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_firsgas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_firsgas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    else: # if audit occurs over two days
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_firsgas.csv'
        Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_firsgas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_firsgas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_firsgas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    
    gas_frames = []
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,7,8,12,16,17,18,20])
        gas_frames.append(df)
        
    all_Data = pd.concat(gas_frames)
    
    all_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'NO (ppb)', 3: 'Diff (ppb)', 4: 'NOy (ppb)', 5: 'NOy Flow (l/min)', 6: 'NOy Pressure (mmHG)'}, inplace=True)
    all_Data.rename(columns={7: 'NO2 (ppb)', 8: 'Ozone (ppb)', 12: 'CO (ppb)', 16: 'NOy Flags', 17: 'O3 Flags', 18: 'NO2 Status', 20: 'CO Flags'}, inplace=True)
    
    all_Data['Date'] = all_Data['Date'].astype(str)
    all_Data['Date_length'] = all_Data['Date'].str.len()
    all_Data=all_Data.loc[all_Data.Date_length == 10] #check the data string length for corruption
    all_Data['datetime'] = all_Data['Date']+' '+all_Data['Time']# added Date and time into new columns
    all_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in all_Data['datetime']] #converts the dateTime format from string to python dateTime
    all_Data.index = all_Data['datetime']
    all_Data = all_Data.sort_index()
    all_Data = all_Data.drop(columns=['Date', 'Time','Date_length'])
    
    all_Data['CO Flags'] = all_Data['CO Flags'].astype(str)
    all_Data['CO_Flags_Prov'] = np.where(all_Data['CO Flags'] == 'FFFFFFFF', 0, all_Data['CO Flags'])
    all_Data['CO Flags'] = all_Data['CO_Flags_Prov']
    all_Data['CO (ppb)'] = np.where(all_Data['CO Flags'] == 0, np.nan, all_Data['CO (ppb)'])
    
#    NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
#    NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime']]
#    Ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime']]
#    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime']]
    
else:
    print('Data Not Found for ' + str(Audit_Date_Str))

all_Data = all_Data[start:end]
Audit_5_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','NO2 (ppb)', 'NO2 Status','Ozone (ppb)', 'O3 Flags','CO (ppb)', 'CO Flags','datetime']]

start = start_Audit_Day_6
end = end_Audit_Day_6

Audit_Date_Str = start.strftime("%Y-%m-%d")

start_Audit_str = str(start.strftime("%Y")) + str(start.strftime("%m")) + str(start.strftime("%d"))
end_Audit_str = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))
    
prior_date_1 = start - timedelta(days=1)
prior_day_1_str = str(prior_date_1.strftime("%Y")) + str(prior_date_1.strftime("%m")) + str(prior_date_1.strftime("%d"))

prior_date_2 = start - timedelta(days=2)
prior_day_2_str = str(prior_date_2.strftime("%Y")) + str(prior_date_2.strftime("%m")) + str(prior_date_2.strftime("%d"))

if end <= Start_of_file_change:
    if start_Audit_str == end_Audit_str: # if audit occurs over the same day
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_gas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_gas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_gas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    else: # if audit occurs over two days
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_gas.csv'
        Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_gas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_gas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_gas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)

    gas_frames = []
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,12,13,14,15,16,17])
        gas_frames.append(df)
        
    early_Data = pd.concat(gas_frames)
    
    early_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'NO (ppb)', 3: 'Diff (ppb)', 4: 'NOy (ppb)', 5: 'NOy Flow (l/min)'}, inplace=True)
    early_Data.rename(columns={6: 'NOy Pressure (mmHG)', 12: 'NO2 (ppb)', 13: 'Ozone (ppb)', 14: 'NOy Flags', 15: 'NO2 Status', 16: 'O3 Flags'}, inplace=True)
    
    early_Data['Date'] = early_Data['Date'].astype(str)
    early_Data['Date_length'] = early_Data['Date'].str.len()
    early_Data=early_Data.loc[early_Data.Date_length == 10] #check the data string length for corruption
    early_Data['datetime'] = early_Data['Date']+' '+early_Data['Time']# added Date and time into new columns
    early_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in early_Data['datetime']] #converts the dateTime format from string to python dateTime
    early_Data.index = early_Data['datetime']
    early_Data = early_Data.sort_index()
    early_Data = early_Data.drop(columns=['Date', 'Time','Date_length'])
    
    early_Data['CO (ppb)'] = np.nan
    early_Data['CO Flags'] = 0
    
    all_Data = early_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','NO2 (ppb)', 'NO2 Status','Ozone (ppb)', 'O3 Flags','CO (ppb)', 'CO Flags','datetime']]
    
#    NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
#    NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime']]
#    Ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime']]
#    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime']]

elif start >= End_of_file_change:
    if start_Audit_str == end_Audit_str: # if audit occurs over the same day
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_firsgas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_firsgas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_firsgas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    else: # if audit occurs over two days
        Audit_Import_1 = str(Data_Source_Folder) + str(start_Audit_str) + '*_firsgas.csv'
        Audit_Import_2 = str(Data_Source_Folder) + str(end_Audit_str) + '*_firsgas.csv'
        prior_day_1_pattern = str(Data_Source_Folder) + str(prior_day_1_str) + '*_firsgas.csv'
        prior_day_2_pattern = str(Data_Source_Folder) + str(prior_day_2_str) + '*_firsgas.csv'
        csv_files = glob.glob(Audit_Import_1) + glob.glob(Audit_Import_2) + glob.glob(prior_day_1_pattern) + glob.glob(prior_day_2_pattern)
    
    gas_frames = []
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,7,8,12,16,17,18,20])
        gas_frames.append(df)
        
    all_Data = pd.concat(gas_frames)
    
    all_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'NO (ppb)', 3: 'Diff (ppb)', 4: 'NOy (ppb)', 5: 'NOy Flow (l/min)', 6: 'NOy Pressure (mmHG)'}, inplace=True)
    all_Data.rename(columns={7: 'NO2 (ppb)', 8: 'Ozone (ppb)', 12: 'CO (ppb)', 16: 'NOy Flags', 17: 'O3 Flags', 18: 'NO2 Status', 20: 'CO Flags'}, inplace=True)
    
    all_Data['Date'] = all_Data['Date'].astype(str)
    all_Data['Date_length'] = all_Data['Date'].str.len()
    all_Data=all_Data.loc[all_Data.Date_length == 10] #check the data string length for corruption
    all_Data['datetime'] = all_Data['Date']+' '+all_Data['Time']# added Date and time into new columns
    all_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in all_Data['datetime']] #converts the dateTime format from string to python dateTime
    all_Data.index = all_Data['datetime']
    all_Data = all_Data.sort_index()
    all_Data = all_Data.drop(columns=['Date', 'Time','Date_length'])
    
    all_Data['CO Flags'] = all_Data['CO Flags'].astype(str)
    all_Data['CO_Flags_Prov'] = np.where(all_Data['CO Flags'] == 'FFFFFFFF', 0, all_Data['CO Flags'])
    all_Data['CO Flags'] = all_Data['CO_Flags_Prov']
    all_Data['CO (ppb)'] = np.where(all_Data['CO Flags'] == 0, np.nan, all_Data['CO (ppb)'])
    
#    NOy_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
#    NO2_Data = all_Data[['NO2 (ppb)', 'NO2 Status', 'datetime']]
#    Ozone_Data = all_Data[['Ozone (ppb)', 'O3 Flags','datetime']]
#    CO_Data = all_Data[['CO (ppb)', 'CO Flags','datetime']]
    
else:
    print('Data Not Found for ' + str(Audit_Date_Str))

all_Data = all_Data[start:end]
Audit_6_Data = all_Data[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','NO2 (ppb)', 'NO2 Status','Ozone (ppb)', 'O3 Flags','CO (ppb)', 'CO Flags','datetime']]

#Audit_5_Data.to_csv(str(Data_Output_Folder) + '1_Gas_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

#NOy_Audit_6 = NOy_Data
#NO2_Audit_6 = NO2_Data
#Ozone_Audit_6 = Ozone_Data
#CO_Audit_6 = CO_Data

Calibrations = pd.concat([Audit_1_Data, Audit_2_Data, Audit_3_Data, Audit_4_Data, Audit_5_Data, Audit_6_Data])

pattern = str(Data_Source_Folder) + 'Cal_Record.csv' # Needs to be address of data location - Collect CSV files
Automated_Cal_File = glob.glob(pattern)

# Create an empty list
frames = []

#  Iterate over csv_files
for csv in Automated_Cal_File:
    df = pd.read_csv(csv) #
    frames.append(df)

Automated_Cal = pd.concat(frames)
Automated_Cal.rename(columns={0: 'Date'}, inplace=True)
Automated_Cal.rename(columns={1: 'Time'}, inplace=True)

Automated_Cal['Date'] = Automated_Cal['Date'].astype(str)
Automated_Cal['Date_length'] = Automated_Cal['Date'].str.len()
Automated_Cal=Automated_Cal.loc[Automated_Cal.Date_length == 10] #check the data string length for corruption
Automated_Cal['datetime'] = Automated_Cal['Date']+ ' ' + Automated_Cal['Time'] # added Date and time into new columns
Automated_Cal['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in Automated_Cal['datetime']] #converts the dateTime format from string to python dateTime
Automated_Cal.index =Automated_Cal['datetime']
Automated_Cal = Automated_Cal.sort_index()

Automated_Cal.rename(columns={'S2_CO_Zero': 'CO_Zero'}, inplace=True)
Automated_Cal.rename(columns={'S2_CO_Slope': 'CO_Slope'}, inplace=True)
Automated_Cal['CO_Zero'] = Automated_Cal['CO_Zero'].astype(float)
Automated_Cal['CO_Slope'] = Automated_Cal['CO_Slope'].astype(float)
#Automated_Cal['Cal Flag'] = np.where(Automated_Cal['CO_Zero'] == 0, 1, 0)
#Automated_Cal['Cal Flag'] = np.where(Automated_Cal['CO_Zero'] == -255, 1, Automated_Cal['Cal Flag'])
#Automated_Cal.drop(Automated_Cal[(Automated_Cal['Cal Flag'] == 1)].index,inplace =True)
Automated_Cal = Automated_Cal.drop(columns=['Date', 'Time', 'Date_length']) #, 'Cal Flag'

Cal_drop_list = list(Automated_Cal.columns.values)
Cal_drop_list.remove('datetime')
Cal_drop_list.remove('NOy_Zero')
Cal_drop_list.remove('NOy_Slope')
Cal_drop_list.remove('CO_Zero')
Cal_drop_list.remove('CO_Slope')
Automated_Cal = Automated_Cal.drop(columns=Cal_drop_list)

#Automated_Cal.to_csv(str(Data_Output_Folder) + '1_Original_Calibrations.csv')

NOy_Automated_Cal = Automated_Cal[['datetime', 'NOy_Zero', 'NOy_Slope']]
CO_Automated_Cal = Automated_Cal[['datetime', 'CO_Zero']]

NOy_Cals = Calibrations[['NO (ppb)', 'Diff (ppb)', 'NOy (ppb)', 'NOy Flow (l/min)', 'NOy Pressure (mmHG)', 'NOy Flags','datetime']]
NOy_Cals['NOy_Prov_Flag'] = np.nan

NOy_Cals['NOy_Prov_Flag'] = np.where(((NOy_Cals['NOy Flags'] == np.nan) | (NOy_Cals['NOy Flags'] == 'FFFFFFFF')), 0, NOy_Cals['NOy Flags']) # not sampling

NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC000000', 1, NOy_Cals['NOy_Prov_Flag']) #Sampling
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC030000', 2, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC000002', 3, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC030002', 4, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC000020', 5, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC030020', 6, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC000022', 7, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC030022', 8, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC000028', 9, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC030028', 10, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC000100', 11, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC030100', 12, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC000400', 13, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC030400', 14, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC000500', 15, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC030500', 16, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC000422', 17, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC030422', 18, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC000428', 19, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC030428', 20, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC008000', 21, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = np.where(NOy_Cals['NOy Flags'] == 'CC038000', 22, NOy_Cals['NOy_Prov_Flag'])
NOy_Cals['NOy_Prov_Flag'] = NOy_Cals['NOy_Prov_Flag'].astype(float)

NOy_Cals.drop(NOy_Cals[(NOy_Cals['NOy_Prov_Flag'] == 0)].index,inplace =True)

NOy_Cals['NOy_Prov_Status'] = np.nan
NOy_Cals['NOy_Prov_Status'] = np.where((NOy_Cals['NOy_Prov_Flag'] == 1)|(NOy_Cals['NOy_Prov_Flag'] == 2), 1, NOy_Cals['NOy_Prov_Status'])
NOy_Cals['NOy_Prov_Status'] = np.where((NOy_Cals['NOy_Prov_Flag'] == 3)|(NOy_Cals['NOy_Prov_Flag'] == 4), 3, NOy_Cals['NOy_Prov_Status'])
NOy_Cals['NOy_Prov_Status'] = np.where((NOy_Cals['NOy_Prov_Flag'] == 5)|(NOy_Cals['NOy_Prov_Flag'] == 6), 5, NOy_Cals['NOy_Prov_Status'])
NOy_Cals['NOy_Prov_Status'] = np.where((NOy_Cals['NOy_Prov_Flag'] == 7)|(NOy_Cals['NOy_Prov_Flag'] == 8), 7, NOy_Cals['NOy_Prov_Status'])
NOy_Cals['NOy_Prov_Status'] = np.where((NOy_Cals['NOy_Prov_Flag'] == 9)|(NOy_Cals['NOy_Prov_Flag'] == 10), 9, NOy_Cals['NOy_Prov_Status'])
NOy_Cals['NOy_Prov_Status'] = np.where((NOy_Cals['NOy_Prov_Flag'] == 11)|(NOy_Cals['NOy_Prov_Flag'] == 12), 11, NOy_Cals['NOy_Prov_Status'])
NOy_Cals['NOy_Prov_Status'] = np.where((NOy_Cals['NOy_Prov_Flag'] == 13)|(NOy_Cals['NOy_Prov_Flag'] == 14), 13, NOy_Cals['NOy_Prov_Status'])
NOy_Cals['NOy_Prov_Status'] = np.where((NOy_Cals['NOy_Prov_Flag'] == 15)|(NOy_Cals['NOy_Prov_Flag'] == 16), 15, NOy_Cals['NOy_Prov_Status'])
NOy_Cals['NOy_Prov_Status'] = np.where((NOy_Cals['NOy_Prov_Flag'] == 17)|(NOy_Cals['NOy_Prov_Flag'] == 18), 17, NOy_Cals['NOy_Prov_Status'])
NOy_Cals['NOy_Prov_Status'] = np.where((NOy_Cals['NOy_Prov_Flag'] == 19)|(NOy_Cals['NOy_Prov_Flag'] == 20), 19, NOy_Cals['NOy_Prov_Status'])
NOy_Cals['NOy_Prov_Status'] = np.where((NOy_Cals['NOy_Prov_Flag'] == 21)|(NOy_Cals['NOy_Prov_Flag'] == 22), 21, NOy_Cals['NOy_Prov_Status'])

NOy_Cals['NOy Cal Status'] = np.where((NOy_Cals['NOy_Prov_Status'] == NOy_Cals['NOy_Prov_Flag']), 0, 1)

NOy_Cal_Status = NOy_Cals['NOy Cal Status'].groupby(pd.Grouper(freq=av_Freq)).max()

min_NOy_flag = NOy_Cals['NOy_Prov_Flag'].groupby(pd.Grouper(freq=av_Freq)).min()
max_NOy_flag = NOy_Cals['NOy_Prov_Flag'].groupby(pd.Grouper(freq=av_Freq)).max()

min_NOy_status = NOy_Cals['NOy_Prov_Status'].groupby(pd.Grouper(freq=av_Freq)).min()
max_NOy_status = NOy_Cals['NOy_Prov_Status'].groupby(pd.Grouper(freq=av_Freq)).max()

NOy_Cals = NOy_Cals.groupby(pd.Grouper(freq=av_Freq)).mean()

NOy_Cals['min_NOy_flag'] = pd.Series(min_NOy_flag)
NOy_Cals['max_NOy_flag'] = pd.Series(max_NOy_flag)
NOy_Cals['NOy_Prov_Flag'] = NOy_Cals['max_NOy_flag']

NOy_Cals['min_NOy_status'] = pd.Series(min_NOy_status)
NOy_Cals['max_NOy_status'] = pd.Series(max_NOy_status)
NOy_Cals['NOy_Prov_Status'] = NOy_Cals['max_NOy_status']

NOy_Cals['NOy Cal Status'] = pd.Series(NOy_Cal_Status)

NOy_Cals.drop(NOy_Cals[(NOy_Cals['NOy_Prov_Flag'].isnull())].index,inplace =True)

NO2_Cals = Calibrations[['NO2 (ppb)', 'NO2 Status', 'datetime']]
NO2_Cals['NO2_Prov_Status'] = np.nan

NO2_Cals['NO2_Prov_Status'] = np.where(((NO2_Cals['NO2 Status']== np.nan) | (NO2_Cals['NO2 Status'] == 'FFFFFFFF')), 0, NO2_Cals['NO2 Status']) # not sampling
NO2_Cals['NO2_Prov_Status'] = np.where((NO2_Cals['NO2 Status'] == 'Sampling'), 1, NO2_Cals['NO2_Prov_Status']) #Sampling
NO2_Cals['NO2_Prov_Status'] = np.where(((NO2_Cals['NO2 Status'] == 'Zero Cal Check in progress') | (NO2_Cals['NO2 Status'] == 'Zero Cal In Progress')), 2, NO2_Cals['NO2_Prov_Status']) #Internal Zero
NO2_Cals['NO2_Prov_Status'] = np.where(((NO2_Cals['NO2 Status'] == 'Recovering')| (NO2_Cals['NO2 Status'] == 'RecoveringZ')), 3, NO2_Cals['NO2_Prov_Status'])#'Recovering from Zero
NO2_Cals['NO2_Prov_Status'] = np.where((NO2_Cals['NO2 Status'] == 'Span Check In Progress'), 4, NO2_Cals['NO2_Prov_Status']) #Internal Span Check In Progress
NO2_Cals['NO2_Prov_Status'] = np.where((NO2_Cals['NO2 Status'] == 'RecoveringS'), 5, NO2_Cals['NO2_Prov_Status']) #Recovering from Cal
NO2_Cals['NO2_Prov_Status'] = np.where((NO2_Cals['NO2 Status'] == 'External Cal'), 6, NO2_Cals['NO2_Prov_Status']) #External Cal
NO2_Cals['NO2_Prov_Status'] = NO2_Cals['NO2_Prov_Status'].astype(float)
NO2_Cals.drop(NO2_Cals[(NO2_Cals['NO2_Prov_Status'] == 0)].index,inplace =True)

min_NO2_flag = NO2_Cals['NO2_Prov_Status'].groupby(pd.Grouper(freq=av_Freq)).min()
max_NO2_flag = NO2_Cals['NO2_Prov_Status'].groupby(pd.Grouper(freq=av_Freq)).max()

NO2_Cals = NO2_Cals.groupby(pd.Grouper(freq=av_Freq)).mean()

NO2_Cals['min_NO2_flag'] = pd.Series(min_NO2_flag)
NO2_Cals['max_NO2_flag'] = pd.Series(max_NO2_flag)
NO2_Cals['NO2_Prov_Status'] = NO2_Cals['max_NO2_flag']
NO2_Cals.drop(NO2_Cals[(NO2_Cals['NO2_Prov_Status'].isnull())].index,inplace =True)

O3_Cals = Calibrations[['Ozone (ppb)', 'O3 Flags','datetime']]

O3_Cals['O3_Prov_Status'] = np.where(((O3_Cals['O3 Flags'] == np.nan) | (O3_Cals['O3 Flags'] == 'FFFFFFFF')), 0, O3_Cals['O3 Flags']) # not sampling
O3_Cals['O3_Prov_Status'] = np.where(O3_Cals['O3 Flags'] == '0C100000', 1, O3_Cals['O3_Prov_Status']) #Sampling
O3_Cals['O3_Prov_Status'] = np.where(O3_Cals['O3 Flags'] == '0C310000', 2, O3_Cals['O3_Prov_Status']) #Internal Zero
O3_Cals['O3_Prov_Status'] = np.where(O3_Cals['O3 Flags'] == '0CD00000', 3, O3_Cals['O3_Prov_Status']) #Span Check In Progress
O3_Cals['O3_Prov_Status'] = np.where(O3_Cals['O3 Flags'] == '0CF00000', 4, O3_Cals['O3_Prov_Status']) #External Cal
O3_Cals['O3_Prov_Status'] = np.where(O3_Cals['O3 Flags'] == '0C310500', 5, O3_Cals['O3_Prov_Status']) #External Zero
O3_Cals['O3_Prov_Status'] = np.where(O3_Cals['O3 Flags'] == '0C500000', 6, O3_Cals['O3_Prov_Status']) #Recovering from Cal
O3_Cals['O3_Prov_Status'] = np.where(O3_Cals['O3 Flags'] == '0C700000', 7, O3_Cals['O3_Prov_Status']) #'Recovering from Zero
O3_Cals['O3_Prov_Status'] = np.where(O3_Cals['O3 Flags'] == '0CF01000', 8, O3_Cals['O3_Prov_Status']) 
O3_Cals['O3_Prov_Status'] = np.where(O3_Cals['O3 Flags'] == '0CF10000', 9, O3_Cals['O3_Prov_Status']) 
O3_Cals['O3_Prov_Status'] = O3_Cals['O3_Prov_Status'].astype(float)
O3_Cals.drop(O3_Cals[(O3_Cals['O3_Prov_Status'] == 0)].index,inplace =True)

min_O3_flag = O3_Cals['O3_Prov_Status'].groupby(pd.Grouper(freq=av_Freq)).min()
max_O3_flag = O3_Cals['O3_Prov_Status'].groupby(pd.Grouper(freq=av_Freq)).max()

O3_Cals = O3_Cals.groupby(pd.Grouper(freq=av_Freq)).mean()

O3_Cals['min_O3_flag'] = pd.Series(min_O3_flag)
O3_Cals['max_O3_flag'] = pd.Series(max_O3_flag)
O3_Cals['O3_Prov_Status'] = O3_Cals['max_O3_flag']
O3_Cals.drop(O3_Cals[(O3_Cals['O3_Prov_Status'].isnull())].index,inplace =True)

CO_Cals = Calibrations[['CO (ppb)', 'CO Flags','datetime']]
CO_Cals['CO_Prov_Status'] = np.nan

CO_Cals['CO_Prov_Status'] = np.where(((CO_Cals['CO Flags']== np.nan) | (CO_Cals['CO Flags'] == 'FFFFFFFF')), 0, CO_Cals['CO Flags'])
CO_Cals['CO_Prov_Status'] = np.where(CO_Cals['CO Flags'] == '8C040000', 1, CO_Cals['CO_Prov_Status']) #Sampling
CO_Cals['CO_Prov_Status'] = np.where(CO_Cals['CO Flags'] == '8C050000', 2, CO_Cals['CO_Prov_Status']) #Internal Zero
CO_Cals['CO_Prov_Status'] = np.where(CO_Cals['CO Flags'] == '8C070000', 3, CO_Cals['CO_Prov_Status']) #External Zero
CO_Cals['CO_Prov_Status'] = np.where(CO_Cals['CO Flags'] == '8C070001', 4, CO_Cals['CO_Prov_Status']) #Span Cal Check In Progress
CO_Cals['CO_Prov_Status'] = np.where(CO_Cals['CO Flags'] == '8C074000', 5, CO_Cals['CO_Prov_Status']) #External Cal
CO_Cals['CO_Prov_Status'] = CO_Cals['CO_Prov_Status'].astype(float)
CO_Cals.drop(CO_Cals[(CO_Cals['CO_Prov_Status'] == 0)].index,inplace =True)

min_CO_flag = CO_Cals['CO_Prov_Status'].groupby(pd.Grouper(freq=av_Freq)).min()
max_CO_flag = CO_Cals['CO_Prov_Status'].groupby(pd.Grouper(freq=av_Freq)).max()

CO_Cals = CO_Cals.groupby(pd.Grouper(freq=av_Freq)).mean()

CO_Cals['min_CO_flag'] = pd.Series(min_CO_flag)
CO_Cals['max_CO_flag'] = pd.Series(max_CO_flag)
CO_Cals['CO_Prov_Status'] = CO_Cals['max_CO_flag']
CO_Cals.drop(CO_Cals[(CO_Cals['CO_Prov_Status'].isnull())].index,inplace =True)

NOy_Cals = NOy_Cals.drop(columns=['min_NOy_flag', 'max_NOy_flag', 'min_NOy_status', 'max_NOy_status'])
NO2_Cals = NO2_Cals.drop(columns=['min_NO2_flag', 'max_NO2_flag'])
O3_Cals = O3_Cals.drop(columns=['min_O3_flag', 'max_O3_flag'])
CO_Cals = CO_Cals.drop(columns=['min_CO_flag', 'max_CO_flag'])

#Calibrations = Calibrations.groupby(pd.Grouper(freq=av_Freq)).mean()

NOy_Cals['NOy Original Status'] = np.nan
NOy_Cals['NOy Status'] = np.nan
NO2_Cals['NO2 Status'] = np.nan
O3_Cals['O3 Status'] = np.nan
CO_Cals['CO Status'] = np.nan

NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 1, 'CC000000', NOy_Cals['NOy Original Status']) #Sampling
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 2, 'CC030000', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 3, 'CC000002', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 4, 'CC030002', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 5, 'CC000020', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 6, 'CC030020', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 7, 'CC000022', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 8, 'CC030022', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 9, 'CC000028', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 10, 'CC030028', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 11, 'CC000100', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 12, 'CC030100', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 13, 'CC000400', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 14, 'CC030400', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 15, 'CC000500', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 16, 'CC030500', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 17, 'CC000422', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 18, 'CC030422', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 19, 'CC000428', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 20, 'CC030428', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 21, 'CC008000', NOy_Cals['NOy Original Status'])
NOy_Cals['NOy Original Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 22, 'CC038000', NOy_Cals['NOy Original Status'])

NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 1, 'Sampling', NOy_Cals['NOy Status']) #Sampling
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 2, 'Cal Mode', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 3, 'Flagged Data', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 4, 'Cal Mode', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 5, 'NO Span Range', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 6, 'NO Span Range', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 7, 'NO Span Range', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 8, 'NO Span Range', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 9, 'NOy Span Range', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 10, 'NOy Span Range', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 11, 'Flagged Data', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 12, 'Cal Mode', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 13, 'Flagged Data', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 14, 'Flagged Data', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 15, 'NO Span Range', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 16, 'NO Span Range', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 17, 'NO Span Range', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 18, 'NO Span Range', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 19, 'Cal Mode', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 20, 'Cal Mode', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 21, 'Flagged Data', NOy_Cals['NOy Status'])
NOy_Cals['NOy Status'] = np.where(NOy_Cals['NOy_Prov_Flag'] == 22, 'Cal Mode', NOy_Cals['NOy Status'])

NOy_Cals = NOy_Cals.drop(columns=['NOy_Prov_Flag'])

NO2_Cals['NO2 Status'] = np.where((NO2_Cals['NO2_Prov_Status'] == 1), 'Sampling', NO2_Cals['NO2 Status'])
NO2_Cals['NO2 Status'] = np.where((NO2_Cals['NO2_Prov_Status'] == 2), 'Zero Cal Check in progress', NO2_Cals['NO2 Status'])
NO2_Cals['NO2 Status'] = np.where((NO2_Cals['NO2_Prov_Status'] == 3), 'Recovering from Zero Check', NO2_Cals['NO2 Status'])
NO2_Cals['NO2 Status'] = np.where((NO2_Cals['NO2_Prov_Status'] == 4), 'Span Check In Progress', NO2_Cals['NO2 Status'])
NO2_Cals['NO2 Status'] = np.where((NO2_Cals['NO2_Prov_Status'] == 5), 'Recovering from Span Check', NO2_Cals['NO2 Status'])
NO2_Cals['NO2 Status'] = np.where((NO2_Cals['NO2_Prov_Status'] == 6), 'External Cylinder Attached', NO2_Cals['NO2 Status'])

O3_Cals['O3 Status'] = np.where((O3_Cals['O3_Prov_Status'] == 1), 'Sampling', O3_Cals['O3 Status'])
O3_Cals['O3 Status'] = np.where((O3_Cals['O3_Prov_Status'] == 2), 'Internal Zero', O3_Cals['O3 Status'])
O3_Cals['O3 Status'] = np.where((O3_Cals['O3_Prov_Status'] == 3), 'Span Check In Progress', O3_Cals['O3 Status'])
O3_Cals['O3 Status'] = np.where((O3_Cals['O3_Prov_Status'] == 4), 'External Cal', O3_Cals['O3 Status'])
O3_Cals['O3 Status'] = np.where((O3_Cals['O3_Prov_Status'] == 5), 'External Zero', O3_Cals['O3 Status'])
O3_Cals['O3 Status'] = np.where((O3_Cals['O3_Prov_Status'] == 6), 'Recovering from Cal', O3_Cals['O3 Status'])
O3_Cals['O3 Status'] = np.where((O3_Cals['O3_Prov_Status'] == 7), 'Recovering from Zero', O3_Cals['O3 Status'])
O3_Cals['O3 Status'] = np.where((O3_Cals['O3_Prov_Status'] == 8), 'Cal Mode on', O3_Cals['O3 Status'])
O3_Cals['O3 Status'] = np.where((O3_Cals['O3_Prov_Status'] == 9), 'Cal Mode on', O3_Cals['O3 Status'])

O3_Cals['O3 Original Status'] = np.where((O3_Cals['O3_Prov_Status'] == 2), '0C310000', '0C100000')
O3_Cals['O3 Original Status'] = np.where((O3_Cals['O3_Prov_Status'] == 3), '0CD00000', O3_Cals['O3 Original Status'])
O3_Cals['O3 Original Status'] = np.where((O3_Cals['O3_Prov_Status'] == 4), '0CF00000', O3_Cals['O3 Original Status'])
O3_Cals['O3 Original Status'] = np.where((O3_Cals['O3_Prov_Status'] == 5), '0C500000', O3_Cals['O3 Original Status'])
O3_Cals['O3 Original Status'] = np.where((O3_Cals['O3_Prov_Status'] == 6), '0C500000', O3_Cals['O3 Original Status'])
O3_Cals['O3 Original Status'] = np.where((O3_Cals['O3_Prov_Status'] == 7), '0C700000', O3_Cals['O3 Original Status'])
O3_Cals['O3 Original Status'] = np.where((O3_Cals['O3_Prov_Status'] == 8), '0CF01000', O3_Cals['O3 Original Status'])
O3_Cals['O3 Original Status'] = np.where((O3_Cals['O3_Prov_Status'] == 9), '0CF10000', O3_Cals['O3 Original Status'])

CO_Cals['CO Status'] = np.where((CO_Cals['CO_Prov_Status'] == 1), 'Sampling', CO_Cals['CO Status'])
CO_Cals['CO Status'] = np.where((CO_Cals['CO_Prov_Status'] == 2), 'Internal Zero', CO_Cals['CO Status'])
CO_Cals['CO Status'] = np.where((CO_Cals['CO_Prov_Status'] == 3), 'External Zero', CO_Cals['CO Status'])
CO_Cals['CO Status'] = np.where((CO_Cals['CO_Prov_Status'] == 4), 'Span Cal Check In Progress', CO_Cals['CO Status'])
CO_Cals['CO Status'] = np.where((CO_Cals['CO_Prov_Status'] == 5), 'External Cal', CO_Cals['CO Status'])

CO_Cals['CO Original Status'] = np.where((CO_Cals['CO_Prov_Status'] == 2), '8C050000', '8C040000')
CO_Cals['CO Original Status'] = np.where((CO_Cals['CO_Prov_Status'] == 3), '8C070000', CO_Cals['CO Original Status'])
CO_Cals['CO Original Status'] = np.where((CO_Cals['CO_Prov_Status'] == 4), '8C070001', CO_Cals['CO Original Status'])
CO_Cals['CO Original Status'] = np.where((CO_Cals['CO_Prov_Status'] == 5), '8C074000', CO_Cals['CO Original Status'])

start_Audit_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,10,00)
end_Audit_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,11,18,00)
NOy_Audit_1 = NOy_Cals[start_Audit_1:end_Audit_1]
NOy_Audit_1['NOy Status'] = np.where((NOy_Audit_1['NOy Status'] == 'Sampling'), 'Flagged Data', NOy_Audit_1['NOy Status']) 
NOy_Adjusted_Status = NOy_Audit_1['NOy Status']
NOy_Cals['NOy Adjusted Status'] = pd.Series(NOy_Adjusted_Status)
NOy_Cals = NOy_Cals.drop(columns=['NOy Adjusted Status'])
NOy_Cals.drop(NOy_Cals[(NOy_Cals['NOy Status'] == 'Sampling')].index,inplace =True)

NO2_Audit_1 = NO2_Cals[start_Audit_1:end_Audit_1]
NO2_Audit_1['NO2 Status'] = np.where((NO2_Audit_1['NO2 Status'] == 'Sampling'), 'Flagged Data', NO2_Audit_1['NO2 Status']) 
NO2_Adjusted_Status = NO2_Audit_1['NO2 Status']
NO2_Cals['NO2 Adjusted Status'] = pd.Series(NO2_Adjusted_Status)
NO2_Cals = NO2_Cals.drop(columns=['NO2 Adjusted Status'])
NO2_Cals['NO2_Prov_Status'] = np.where((NO2_Cals['NO2 Status'] == 'Flagged Data'), 7, NO2_Cals['NO2_Prov_Status'])
NO2_Cals.drop(NO2_Cals[(NO2_Cals['NO2 Status'] == 'Sampling')].index,inplace =True)

O3_Audit_1 = O3_Cals[start_Audit_1:end_Audit_1]
O3_Audit_1['O3 Status'] = np.where((O3_Audit_1['O3 Status'] == 'Sampling'), 'Flagged Data', O3_Audit_1['O3 Status']) 
O3_Adjusted_Status = O3_Audit_1['O3 Status']
O3_Cals['O3 Adjusted Status'] = pd.Series(O3_Adjusted_Status)
O3_Cals = O3_Cals.drop(columns=['O3 Adjusted Status'])
O3_Cals['O3_Prov_Status'] = np.where((O3_Cals['O3 Status'] == 'Flagged Data'), 8, O3_Cals['O3_Prov_Status'])
O3_Cals.drop(O3_Cals[(O3_Cals['O3 Status'] == 'Sampling')].index,inplace =True)

#NOy_Cals.to_csv(str(Data_Output_Folder) + '3_Prov_NOy_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')
#NO2_Cals.to_csv(str(Data_Output_Folder) + '4_Prov_NO2_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')
#O3_Cals.to_csv(str(Data_Output_Folder) + '5_Prov_O3_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')
#CO_Cals.to_csv(str(Data_Output_Folder) + '6_Prov_CO_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

Calibrations = pd.concat([NOy_Cals, NO2_Cals, O3_Cals, CO_Cals])

Calibrations = Calibrations.sort_index()
Calibrations = Calibrations.groupby(pd.Grouper(freq=av_Freq)).mean()

Calibrations.rename(columns={'Ozone (ppb)': 'O3 (ppb)'}, inplace=True)

#Calibrations.to_csv(str(Data_Output_Folder) + '1_Gas_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

Calibrations['Cal Status'] = np.where((Calibrations['NO2 (ppb)'].isnull() & Calibrations['CO (ppb)'].isnull()), 1, 0)
Calibrations.drop(Calibrations[(Calibrations['Cal Status'] == 1)].index,inplace =True)


#NOy_Cals = pd.concat([NOy_Audit_1, NOy_Audit_2, NOy_Audit_3, NOy_Audit_4, NOy_Audit_5])
#NO2_Cals = pd.concat([NO2_Audit_1, NO2_Audit_2, NO2_Audit_3, NO2_Audit_4, NO2_Audit_5])
#Ozone_Cals = pd.concat([Ozone_Audit_1, Ozone_Audit_2, Ozone_Audit_3, Ozone_Audit_4, Ozone_Audit_5])
#CO_Cals = pd.concat([CO_Audit_1, CO_Audit_2, CO_Audit_3, CO_Audit_4, CO_Audit_5])

start_Audit_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,10,00)
end_Audit_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,11,18,00)

start_Audit_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,9,28,00)
end_Audit_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,14,35,00)

start_Audit_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,24,00)
end_Audit_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,10,44,00)

start_Audit_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,5,00)
end_Audit_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,14,40,00)

start_Audit_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,7,26,00)
end_Audit_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,11,13,00)

start_Audit_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,8,30,00)
end_Audit_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,12,13,00)

Calibrations['NO_Zero_Mean'] = np.nan
Calibrations['NO_Cal_Mean'] = np.nan
Calibrations['NOy_Zero_Mean'] = np.nan
Calibrations['NOy_Cal_Mean'] = np.nan
Calibrations['NO2_Zero_Mean'] = np.nan
Calibrations['NO2_Cal_Mean'] = np.nan
Calibrations['O3_Zero_Mean'] = np.nan
Calibrations['O3_Cal_Mean'] = np.nan
Calibrations['CO_Zero_Mean'] = np.nan
Calibrations['CO_Cal_Mean'] = np.nan

start_O3_Cal_1a = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,58,00)
end_O3_Cal_1a = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,6,59)
O3_Cal_1a = Calibrations[start_O3_Cal_1a:end_O3_Cal_1a]
O3_Cal_1a_mean = O3_Cal_1a['O3 (ppb)'].mean()

start_O3_Lin_1a = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,11,00)
end_O3_Lin_1a = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,16,59)
O3_Lin_1a = Calibrations[start_O3_Lin_1a:end_O3_Lin_1a]
O3_Lin_1a_mean = O3_Lin_1a['O3 (ppb)'].mean() 
O3_Lin_1a_real = 30

start_O3_Lin_1b = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,18,00)
end_O3_Lin_1b = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,27,59)
O3_Lin_1b = Calibrations[start_O3_Lin_1b:end_O3_Lin_1b]
O3_Lin_1b_mean = O3_Lin_1b['O3 (ppb)'].mean() 
O3_Lin_1b_real = 150

start_O3_Lin_1c = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,31,00)
end_O3_Lin_1c = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,42,59)
O3_Lin_1c = Calibrations[start_O3_Lin_1c:end_O3_Lin_1c]
O3_Lin_1c_mean = O3_Lin_1c['O3 (ppb)'].mean() 
O3_Lin_1c_real = 100

start_O3_Zero_1a = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,45,00)
end_O3_Zero_1a = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,52,59)
O3_Zero_1a = Calibrations[start_O3_Zero_1a:end_O3_Zero_1a]
O3_Zero_1a_min = O3_Zero_1a['O3 (ppb)'].min() 

minimum = min(start_Audit_1,end_O3_Zero_1a)
maximum = max(start_Audit_1,end_O3_Zero_1a)
Calibrations.loc[minimum:maximum, ('O3_Zero_Mean')] = O3_Zero_1a_min
Calibrations.loc[minimum:maximum, ('O3_Cal_Mean')] = O3_Cal_1a_mean 
Calibrations.loc[minimum:maximum, ('O3_lit_Response')] = 1.292

start_O3_Lin_1d = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,11,00)
end_O3_Lin_1d = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,14,59)
O3_Lin_1d = Calibrations[start_O3_Lin_1d:end_O3_Lin_1d]
O3_Lin_1d_mean = O3_Lin_1d['O3 (ppb)'].mean() 
O3_Lin_1d_real = 60

start_O3_Lin_1e = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,16,00)
end_O3_Lin_1e = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,21,59)
O3_Lin_1e = Calibrations[start_O3_Lin_1e:end_O3_Lin_1e]
O3_Lin_1e_mean = O3_Lin_1e['O3 (ppb)'].mean() 
O3_Lin_1e_real = 150

start_O3_Lin_1f = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,24,00)
end_O3_Lin_1f = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,29,59)
O3_Lin_1f = Calibrations[start_O3_Lin_1f:end_O3_Lin_1f]
O3_Lin_1f_mean = O3_Lin_1f['O3 (ppb)'].mean() 
O3_Lin_1f_real = 30

start_O3_Cal_1b = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,32,00)
end_O3_Cal_1b = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,37,59)
O3_Cal_1b = Calibrations[start_O3_Cal_1b:end_O3_Cal_1b]
O3_Cal_1b_mean = O3_Cal_1b['O3 (ppb)'].mean()

start_O3_Zero_1b = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,40,00)
end_O3_Zero_1b = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,43,59)
O3_Zero_1b = Calibrations[start_O3_Zero_1b:end_O3_Zero_1b]
O3_Zero_1b_mean = O3_Zero_1b['O3 (ppb)'].mean()

start_O3_Lin_1f = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,45,00)
end_O3_Lin_1f = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,49,59)
O3_Lin_1f = Calibrations[start_O3_Lin_1f:end_O3_Lin_1f]
O3_Lin_1f_mean = O3_Lin_1f['O3 (ppb)'].mean() 
O3_Lin_1f_real = 100

minimum = min(start_O3_Lin_1d,end_O3_Lin_1f,end_Audit_1)
maximum = max(start_O3_Lin_1d,end_O3_Lin_1f,end_Audit_1)
Calibrations.loc[minimum:maximum, ('O3_Zero_Mean')] = O3_Zero_1b_mean
Calibrations.loc[minimum:maximum, ('O3_Cal_Mean')] = O3_Cal_1b_mean 
Calibrations.loc[minimum:maximum, ('O3_lit_Response')] = 1.05

start_Diff_Cal_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,16,00)
end_Diff_Cal_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,23,59)
Diff_Cal_1 = Calibrations[start_Diff_Cal_1:end_Diff_Cal_1]
NO_Diff_Cal_1 = Diff_Cal_1['NO (ppb)'].mean()
NOy_Diff_Cal_1 = Diff_Cal_1['NOy (ppb)'].mean()

start_NO_Cal_1a = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,31,00)
end_NO_Cal_1a = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,40,59)
NO_Cal_1a = Calibrations[start_NO_Cal_1a:end_NO_Cal_1a]
NO_NO_Cal_1a = NO_Cal_1a['NO (ppb)'].mean()
NOy_NO_Cal_1a = NO_Cal_1a['NOy (ppb)'].mean()

start_NOy_Lin_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,48,00)
end_NOy_Lin_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,10,2,59)
NOy_Lin_1 = Calibrations[start_NOy_Lin_1:end_NOy_Lin_1]

start_NOy_Zero_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,10,5,00)
end_NOy_Zero_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,10,9,59)
NOy_Zero_1 = Calibrations[start_NOy_Zero_1:end_NOy_Zero_1]
NO_Zero_mean_1 = NOy_Zero_1['NO (ppb)'].mean()
NOy_Zero_mean_1 = NOy_Zero_1['NOy (ppb)'].mean()

start_NO_Cal_1b = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,10,26,00)
end_NO_Cal_1b = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,10,35,59)
NO_Cal_1b = Calibrations[start_NO_Cal_1b:end_NO_Cal_1b]
NO_NO_Cal_1b_mean = NO_Cal_1b['NO (ppb)'].mean()
NOy_NO_Cal_1b_mean = NO_Cal_1b['NOy (ppb)'].mean()

start_NO_Cal_1c = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,10,52,00)
end_NO_Cal_1c = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,11,0,59)
NO_Cal_1c = Calibrations[start_NO_Cal_1c:end_NO_Cal_1c]
NO_NO_Cal_1c_mean = NO_Cal_1c['NO (ppb)'].mean()
NOy_NO_Cal_1c_mean = NO_Cal_1c['NOy (ppb)'].mean()

start_NO2_Zero_1a = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,34,00)
end_NO2_Zero_1a = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,48,59)
NO2_Zero_1a = Calibrations[start_NO2_Zero_1a:end_NO2_Zero_1a]
NO2_Zero_1a_mean = NO2_Zero_1a['NO2 (ppb)'].mean()

start_NO2_Zero_1b = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,7,52,00)
end_NO2_Zero_1b = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,10,59)
NO2_Zero_1b = Calibrations[start_NO2_Zero_1b:end_NO2_Zero_1b]
NO2_Zero_1b_mean = NO2_Zero_1b['NO2 (ppb)'].min()

start_NO2_Cal_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,15,00)
end_NO2_Cal_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,22,59)
NO2_Cal_1 = Calibrations[start_NO2_Cal_1:end_NO2_Cal_1]
NO2_Cal_1_mean = NO2_Cal_1['NO2 (ppb)'].mean()  

start_NO2_Zero_1c = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,8,52,00)
end_NO2_Zero_1c = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,9,1,59)
NO2_Zero_1c = Calibrations[start_NO2_Zero_1c:end_NO2_Zero_1c]
NO2_Zero_1c_mean = NO2_Zero_1c['NO2 (ppb)'].mean()

start_NO2_Lin_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,10,35,00)
end_NO2_Lin_1 = datetime.datetime(year_Audit_1,month_Audit_1,day_Audit_1,11,16,59)
NO2_Lin_1 = Calibrations[start_NO2_Lin_1:end_NO2_Lin_1]

minimum = min(start_Audit_1,end_Audit_1)
maximum = max(start_Audit_1,end_Audit_1)

# Audit 1 Date 9th August 2019 
Calibrations.loc[minimum:maximum, ('NO_Zero_Mean')] = NO_Zero_mean_1
Calibrations.loc[minimum:maximum, ('NO_Cal_Mean')] = NO_NO_Cal_1c_mean 
Calibrations.loc[minimum:maximum, ('NOy_Zero_Mean')] = NOy_Zero_mean_1
Calibrations.loc[minimum:maximum, ('NOy_Cal_Mean')] = NOy_NO_Cal_1c_mean 
Calibrations.loc[minimum:maximum, ('NO2_Zero_Mean')] = NO2_Zero_1b_mean
Calibrations.loc[minimum:maximum, ('NO2_Cal_Mean')] = NO2_Cal_1_mean 
Calibrations.loc[minimum:maximum, ('Diff_Cal_Mean')] = NOy_Diff_Cal_1 - NO_Diff_Cal_1

Calibrations.loc[minimum:maximum, ('O3_calibration_cylinder_ppb')] = 200
Calibrations.loc[minimum:maximum, ('NO_calibration_cylinder_ppb')] = 434 
Calibrations.loc[minimum:maximum, ('NO2_calibration_cylinder_ppb')] = 210 
Calibrations.loc[minimum:maximum, ('NO_lit_Zero')] =  0.2
Calibrations.loc[minimum:maximum, ('NO_lit_Response')] = 1.267
Calibrations.loc[minimum:maximum, ('NOy_lit_Zero')] =  1.1
Calibrations.loc[minimum:maximum, ('NOy_lit_Response')] =  1.275
Calibrations.loc[minimum:maximum, ('NO2_lit_Zero')] =  -0.1
Calibrations.loc[minimum:maximum, ('NO2_lit_Response')] =  0.954
Calibrations.loc[minimum:maximum, ('O3_lit_Zero')] =  0


start_NOy_Zero_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,11,56,00)
end_NOy_Zero_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,12,1,59)
NOy_Zero_2 = Calibrations[start_NOy_Zero_2:end_NOy_Zero_2]
NO_Zero_mean_2 = NOy_Zero_2['NO (ppb)'].mean()
NOy_Zero_mean_2 = NOy_Zero_2['NOy (ppb)'].mean()

start_NO_Cal_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,12,5,00)
end_NO_Cal_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,12,9,59)
NO_Cal_2 = Calibrations[start_NO_Cal_2:end_NO_Cal_2]
NO_NO_Cal_2_mean = NO_Cal_2['NO (ppb)'].mean()
NOy_NO_Cal_2_mean = NO_Cal_2['NOy (ppb)'].mean()

start_Diff_Cal_2a = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,12,13,00)
end_Diff_Cal_2a = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,12,17,59)
Diff_Cal_2a = Calibrations[start_Diff_Cal_2a:end_Diff_Cal_2a]
NO_Diff_Cal_2a = Diff_Cal_2a['NO (ppb)'].mean()
NOy_Diff_Cal_2a = Diff_Cal_2a['NOy (ppb)'].mean()

start_Diff_Cal_2b = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,12,39,00)
end_Diff_Cal_2b = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,12,45,59)
Diff_Cal_2b = Calibrations[start_Diff_Cal_2b:end_Diff_Cal_2b]
NO_Diff_Cal_2b = Diff_Cal_2b['NO (ppb)'].mean()
NOy_Diff_Cal_2b = Diff_Cal_2b['NOy (ppb)'].mean()

start_NOy_Lin_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,12,57,00)
end_NOy_Lin_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,14,0,59)
NOy_Lin_2 = Calibrations[start_NOy_Lin_2:end_NOy_Lin_2]


start_NO2_Zero_2a = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,59,00)
end_NO2_Zero_2a = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,11,2,59)
NO2_Zero_2a = Calibrations[start_NO2_Zero_2a:end_NO2_Zero_2a]
NO2_Zero_2a_mean = NO2_Zero_2a['NO2 (ppb)'].mean()

start_NO2_Cal_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,11,7,00)
end_NO2_Cal_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,11,34,59)
NO2_Cal_2 = Calibrations[start_NO2_Cal_2:end_NO2_Cal_2]
NO2_Cal_2_mean = NO2_Cal_2['NO2 (ppb)'].mean()

start_NO2_Zero_2b = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,11,45,00)
end_NO2_Zero_2b = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,12,8,59)
NO2_Zero_2b = Calibrations[start_NO2_Zero_2b:end_NO2_Zero_2b]
NO2_Zero_2b_mean = NO2_Zero_2b['NO2 (ppb)'].mean()

start_NO2_Lin_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,13,30,00)
end_NO2_Lin_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,14,15,59)
NO2_Lin_2 = Calibrations[start_NO2_Lin_2:end_NO2_Lin_2]

start_O3_Cal_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,9,00)
end_O3_Cal_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,14,59)
O3_Cal_2 = Calibrations[start_O3_Cal_2:end_O3_Cal_2]
O3_Cal_2_mean = O3_Cal_2['O3 (ppb)'].mean()  

start_O3_Lin_2a = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,19,00)
end_O3_Lin_2a = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,24,59)
O3_Lin_2a = Calibrations[start_O3_Lin_2a:end_O3_Lin_2a]
O3_Lin_2a_mean = O3_Lin_2a['O3 (ppb)'].mean() 
O3_Lin_2a_real = 100

start_O3_Lin_2b = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,27,00)
end_O3_Lin_2b = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,35,59)
O3_Lin_2b = Calibrations[start_O3_Lin_2b:end_O3_Lin_2b]
O3_Lin_2b_mean = O3_Lin_2b['O3 (ppb)'].mean() 
O3_Lin_2b_real = 30

start_O3_Lin_2c = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,40,00)
end_O3_Lin_2c = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,53,59)
O3_Lin_2c = Calibrations[start_O3_Lin_2c:end_O3_Lin_2c]
O3_Lin_2c_mean = O3_Lin_2c['O3 (ppb)'].mean() 
O3_Lin_2c_real = 60

start_O3_Lin_2d = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,57,00)
end_O3_Lin_2d = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,11,5,59)
O3_Lin_2d = Calibrations[start_O3_Lin_2d:end_O3_Lin_2d]
O3_Lin_2d_mean = O3_Lin_2d['O3 (ppb)'].mean() 
O3_Lin_2d_real = 150

start_O3_Zero_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,11,9,00)
end_O3_Zero_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,11,19,59)
O3_Zero_2 = Calibrations[start_O3_Zero_2:end_O3_Zero_2]
O3_Zero_2_mean = O3_Zero_2['O3 (ppb)'].mean() 

start_CO_Zero_2a = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,1,00)
end_CO_Zero_2a = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,10,59)
CO_Zero_2a = Calibrations[start_CO_Zero_2a:end_CO_Zero_2a]
CO_Zero_2a_mean = CO_Zero_2a['CO (ppb)'].mean()

start_CO_Cal_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,16,00)
end_CO_Cal_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,10,30,59)
CO_Cal_2 = Calibrations[start_CO_Cal_2:end_CO_Cal_2]
CO_Cal_2_mean = CO_Cal_2['CO (ppb)'].mean()  

start_CO_Lin_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,12,12,00)
end_CO_Lin_2 = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,12,56,59)
CO_Lin_2 = Calibrations[start_CO_Lin_2:end_CO_Lin_2]

start_CO_Zero_2b = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,21,1,00)
end_CO_Zero_2b = datetime.datetime(year_Audit_2,month_Audit_2,day_Audit_2,21,4,59)
CO_Zero_2b = Calibrations[start_CO_Zero_2b:end_CO_Zero_2b]
CO_Zero_2b_mean = CO_Zero_2b['CO (ppb)'].mean()

minimum = min(start_Audit_2,end_Audit_2)
maximum = max(start_Audit_2,end_Audit_2)

Calibrations.loc[minimum:maximum, ('NO_Zero_Mean')] = NO_Zero_mean_2
Calibrations.loc[minimum:maximum, ('NO_Cal_Mean')] = NO_NO_Cal_2_mean 
Calibrations.loc[minimum:maximum, ('NOy_Zero_Mean')] = NOy_Zero_mean_2
Calibrations.loc[minimum:maximum, ('NOy_Cal_Mean')] = NOy_NO_Cal_2_mean 
Calibrations.loc[minimum:maximum, ('Diff_Cal_Mean')] = NOy_Diff_Cal_2a - NO_Diff_Cal_2a

Calibrations.loc[minimum:maximum, ('O3_Zero_Mean')] = O3_Zero_2_mean
Calibrations.loc[minimum:maximum, ('O3_Cal_Mean')] = O3_Cal_2_mean
Calibrations.loc[minimum:maximum, ('NO2_Zero_Mean')] = NO2_Zero_2b_mean
Calibrations.loc[minimum:maximum, ('NO2_Cal_Mean')] = NO2_Cal_2_mean 
Calibrations.loc[minimum:maximum, ('CO_Zero_Mean')] = CO_Zero_2b_mean
Calibrations.loc[minimum:maximum, ('CO_Cal_Mean')] = CO_Cal_2_mean 

# Audit 1 Date 18th March 2020
Calibrations.loc[minimum:maximum, ('O3_calibration_cylinder_ppb')] = 200 #Checked
Calibrations.loc[minimum:maximum, ('NO_calibration_cylinder_ppb')] = 461 #Checked
Calibrations.loc[minimum:maximum, ('NO2_calibration_cylinder_ppb')] = 210 #Checked
Calibrations.loc[minimum:maximum, ('CO_calibration_cylinder_ppb')] = 10.67*1000 #Checked
Calibrations.loc[minimum:maximum, ('O3_lit_Zero')] =  0
Calibrations.loc[minimum:maximum, ('O3_lit_Response')] = 1.044 #198.3/200
Calibrations.loc[minimum:maximum, ('NO_lit_Zero')] =  -0.01
Calibrations.loc[minimum:maximum, ('NO_lit_Response')] = 1.384
Calibrations.loc[minimum:maximum, ('NOy_lit_Zero')] =  3.3
Calibrations.loc[minimum:maximum, ('NOy_lit_Response')] =  1.367
Calibrations.loc[minimum:maximum, ('NO2_lit_Zero')] =  -0.01
Calibrations.loc[minimum:maximum, ('NO2_lit_Response')] =  0.941
Calibrations.loc[minimum:maximum, ('CO_lit_Zero')] =  -150
Calibrations.loc[minimum:maximum, ('CO_lit_Response')] = 1.033


start_NOy_Zero_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,39,00)
end_NOy_Zero_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,44,59)
NOy_Zero_3 = Calibrations[start_NOy_Zero_3:end_NOy_Zero_3]
NO_Zero_mean_3 = NOy_Zero_3['NO (ppb)'].mean()
NOy_Zero_mean_3 = NOy_Zero_3['NOy (ppb)'].mean()

start_Diff_Cal_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,49,00)
end_Diff_Cal_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,55,59)
Diff_Cal_3 = Calibrations[start_Diff_Cal_3:end_Diff_Cal_3]
NO_Diff_Cal_3 = Diff_Cal_3['NO (ppb)'].mean()
NOy_Diff_Cal_3 = Diff_Cal_3['NOy (ppb)'].mean()

start_NO_Cal_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,0,00)
end_NO_Cal_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,7,59)
NO_Cal_3 = Calibrations[start_NO_Cal_3:end_NO_Cal_3]
NO_NO_Cal_3_mean = NO_Cal_3['NO (ppb)'].mean()
NOy_NO_Cal_3_mean = NO_Cal_3['NOy (ppb)'].mean()

start_NOy_Lin_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,12,57,00)
end_NOy_Lin_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,14,0,59)
NOy_Lin_3 = Calibrations[start_NOy_Lin_3:end_NOy_Lin_3]


start_NO2_Cal_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,0,00)
end_NO2_Cal_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,2,59)
NO2_Cal_3 = Calibrations[start_NO2_Cal_3:end_NO2_Cal_3]
NO2_Cal_3_mean = NO2_Cal_3['NO2 (ppb)'].mean()  

start_NO2_Zero_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,50,00)
end_NO2_Zero_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,59,59)
NO2_Zero_3a = Calibrations[start_NO2_Zero_3a:end_NO2_Zero_3a]
NO2_Zero_3a_mean = NO2_Zero_3a['NO2 (ppb)'].mean()

start_NO2_Lin_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,57,00)
end_NO2_Lin_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,9,42,59)
NO2_Lin_3 = Calibrations[start_NO2_Lin_3:end_NO2_Lin_3]

start_NO2_Zero_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,10,10,00)
end_NO2_Zero_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,10,17,59)
NO2_Zero_3b = Calibrations[start_NO2_Zero_3b:end_NO2_Zero_3b]
NO2_Zero_3b_mean = NO2_Zero_3b['NO2 (ppb)'].mean()


start_O3_Zero_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,43,00)
end_O3_Zero_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,46,59)
O3_Zero_3a = Calibrations[start_O3_Zero_3a:end_O3_Zero_3a]
O3_Zero_3a_mean = O3_Zero_3a['O3 (ppb)'].mean() 

start_O3_Cal_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,51,00)
end_O3_Cal_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,53,59)
O3_Cal_3a = Calibrations[start_O3_Cal_3a:end_O3_Cal_3a]
O3_Cal_3a_mean = O3_Cal_3a['O3 (ppb)'].mean()  

start_O3_Lin_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,7,57,00)
end_O3_Lin_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,21,59)
O3_Lin_3a = Calibrations[start_O3_Lin_3a:end_O3_Lin_3a]
O3_Lin_3a_mean = O3_Lin_3a['O3 (ppb)'].mean() 
O3_Lin_3a_real = 100

start_O3_Lin_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,26,00)
end_O3_Lin_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,31,59)
O3_Lin_3b = Calibrations[start_O3_Lin_3b:end_O3_Lin_3b]
O3_Lin_3b_mean = O3_Lin_3b['O3 (ppb)'].mean() 
O3_Lin_3b_real = 30

start_O3_Lin_3c = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,35,00)
end_O3_Lin_3c = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,49,59)
O3_Lin_3c = Calibrations[start_O3_Lin_3c:end_O3_Lin_3c]
O3_Lin_3c_mean = O3_Lin_3c['O3 (ppb)'].mean() 
O3_Lin_3c_real = 150

start_O3_Lin_3d = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,53,00)
end_O3_Lin_3d = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,9,2,59)
O3_Lin_3d = Calibrations[start_O3_Lin_3d:end_O3_Lin_3d]
O3_Lin_3d_mean = O3_Lin_3d['O3 (ppb)'].mean() 
O3_Lin_3d_real = 60

start_O3_Cal_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,9,5,00)
end_O3_Cal_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,9,14,59)
O3_Cal_3b = Calibrations[start_O3_Cal_3b:end_O3_Cal_3b]
O3_Cal_3b_mean = O3_Cal_3b['O3 (ppb)'].mean()  

start_O3_Zero_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,9,18,00)
end_O3_Zero_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,9,24,59)
O3_Zero_3b = Calibrations[start_O3_Zero_3b:end_O3_Zero_3b]
O3_Zero_3b_mean = O3_Zero_3b['O3 (ppb)'].mean() 

start_CO_Zero_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,15,00)
end_CO_Zero_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,19,59)
CO_Zero_3a = Calibrations[start_CO_Zero_3a:end_CO_Zero_3a]
CO_Zero_3a_mean = CO_Zero_3a['CO (ppb)'].mean()

start_CO_Cal_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,23,00)
end_CO_Cal_3a = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,32,59)
CO_Cal_3a = Calibrations[start_CO_Cal_3a:end_CO_Cal_3a]
CO_Cal_3a_mean = CO_Cal_3a['CO (ppb)'].min()  

start_CO_Zero_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,36,00)
end_CO_Zero_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,43,59)
CO_Zero_3b = Calibrations[start_CO_Zero_3b:end_CO_Zero_3b]
CO_Zero_3b_mean = CO_Zero_3b['CO (ppb)'].mean()

start_CO_Cal_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,8,52,00)
end_CO_Cal_3b = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,9,6,59)
CO_Cal_3b = Calibrations[start_CO_Cal_3b:end_CO_Cal_3b]
CO_Cal_3b_mean = CO_Cal_3b['CO (ppb)'].mean()  

start_CO_Zero_3c = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,9,10,00)
end_CO_Zero_3c = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,9,16,59)
CO_Zero_3c = Calibrations[start_CO_Zero_3c:end_CO_Zero_3c]
CO_Zero_3c_mean = CO_Zero_3c['CO (ppb)'].mean()

start_CO_Lin_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,9,18,00)
end_CO_Lin_3 = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,10,11,59)
CO_Lin_3 = Calibrations[start_CO_Lin_3:end_CO_Lin_3]

start_CO_Zero_3d = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,10,14,00)
end_CO_Zero_3d = datetime.datetime(year_Audit_3,month_Audit_3,day_Audit_3,10,16,59)
CO_Zero_3d = Calibrations[start_CO_Zero_3d:end_CO_Zero_3d]
CO_Zero_3d_mean = CO_Zero_3d['CO (ppb)'].max()

minimum = min(start_Audit_3,end_Audit_3)
maximum = max(start_Audit_3,end_Audit_3)

#Audit 3 Date 2 October 2020
Calibrations.loc[minimum:maximum, ('NO_Zero_Mean')] = NO_Zero_mean_3
Calibrations.loc[minimum:maximum, ('NO_Cal_Mean')] = NO_NO_Cal_3_mean  
Calibrations.loc[minimum:maximum, ('NOy_Zero_Mean')] = NOy_Zero_mean_3
Calibrations.loc[minimum:maximum, ('NOy_Cal_Mean')] = NOy_NO_Cal_3_mean 
Calibrations.loc[minimum:maximum, ('Diff_Cal_Mean')] = NOy_Diff_Cal_3 - NO_Diff_Cal_3

Calibrations.loc[minimum:maximum, ('O3_Zero_Mean')] = O3_Zero_3b_mean
Calibrations.loc[minimum:maximum, ('O3_Cal_Mean')] = O3_Cal_3b_mean 
Calibrations.loc[minimum:maximum, ('NO2_Zero_Mean')] = NO2_Zero_3b_mean
Calibrations.loc[minimum:maximum, ('NO2_Cal_Mean')] = NO2_Cal_3_mean 
Calibrations.loc[minimum:maximum, ('CO_Zero_Mean')] = CO_Zero_3c_mean
Calibrations.loc[minimum:maximum, ('CO_Cal_Mean')] = CO_Cal_3a_mean 

Calibrations.loc[minimum:maximum, ('O3_calibration_cylinder_ppb')] = 200 
Calibrations.loc[minimum:maximum, ('NO_calibration_cylinder_ppb')] = 434 #NO 488 original 
Calibrations.loc[minimum:maximum, ('NO2_calibration_cylinder_ppb')] = 210 #NO2 439 original 
Calibrations.loc[minimum:maximum, ('CO_calibration_cylinder_ppb')] = 10.7*1000 
Calibrations.loc[minimum:maximum, ('O3_lit_Zero')] =  0
Calibrations.loc[minimum:maximum, ('O3_lit_Response')] = 1.044
Calibrations.loc[minimum:maximum, ('NO_lit_Zero')] =  -0.01
Calibrations.loc[minimum:maximum, ('NO_lit_Response')] = 1.384
Calibrations.loc[minimum:maximum, ('NOy_lit_Zero')] =  0.4
Calibrations.loc[minimum:maximum, ('NOy_lit_Response')] =  1.367
Calibrations.loc[minimum:maximum, ('NO2_lit_Zero')] =  -0.01
Calibrations.loc[minimum:maximum, ('NO2_lit_Response')] =  0.941
Calibrations.loc[minimum:maximum, ('CO_lit_Zero')] =  20
Calibrations.loc[minimum:maximum, ('CO_lit_Response')] = 1.033


start_NOy_Zero_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,41,00)
end_NOy_Zero_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,44,59)
NOy_Zero_4 = Calibrations[start_NOy_Zero_4:end_NOy_Zero_4]
NO_Zero_mean_4 = NOy_Zero_4['NO (ppb)'].mean()
NOy_Zero_mean_4 = NOy_Zero_4['NOy (ppb)'].mean()

start_NO_Cal_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,50,00)
end_NO_Cal_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,56,59)
NO_Cal_4 = Calibrations[start_NO_Cal_4:end_NO_Cal_4]
NO_NO_Cal_4 = NO_Cal_4['NO (ppb)'].mean()
NOy_NO_Cal_4 = NO_Cal_4['NOy (ppb)'].mean()

start_Diff_Cal_4a = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,7,00)
end_Diff_Cal_4a = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,18,59)
Diff_Cal_4a = Calibrations[start_Diff_Cal_4a:end_Diff_Cal_4a]
NO_Diff_Cal_4a = Diff_Cal_4a['NO (ppb)'].mean()
NOy_Diff_Cal_4a = Diff_Cal_4a['NOy (ppb)'].mean()

start_NOy_Lin_3 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,57,00)
end_NOy_Lin_3 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,11,35,59)
NOy_Lin_3 = Calibrations[start_NOy_Lin_3:end_NOy_Lin_3]

start_Diff_Cal_4b = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,11,48,00)
end_Diff_Cal_4b = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,11,53,59)
Diff_Cal_4b = Calibrations[start_Diff_Cal_4b:end_Diff_Cal_4b]
NO_Diff_Cal_4b = Diff_Cal_4b['NO (ppb)'].mean()
NOy_Diff_Cal_4b = Diff_Cal_4b['NOy (ppb)'].mean()


start_NO2_Zero_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,19,00)
end_NO2_Zero_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,27,59)
NO2_Zero_4 = Calibrations[start_NO2_Zero_4:end_NO2_Zero_4]
NO2_Zero_4_mean = NO2_Zero_4['NO2 (ppb)'].min()

start_NO2_Cal_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,37,00)
end_NO2_Cal_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,53,59)
NO2_Cal_4 = Calibrations[start_NO2_Cal_4:end_NO2_Cal_4]
NO2_Cal_4_mean = NO2_Cal_4['NO2 (ppb)'].max()  

start_NO2_Lin_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,10,45,00)
end_NO2_Lin_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,11,30,59)
NO2_Lin_4 = Calibrations[start_NO2_Lin_4:end_NO2_Lin_4]

start_O3_Cal_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,38,00)
end_O3_Cal_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,48,59)
O3_Cal_4 = Calibrations[start_O3_Cal_4:end_O3_Cal_4]
O3_Cal_4_mean = O3_Cal_4['O3 (ppb)'].mean()  

start_O3_Lin_4a = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,8,53,00)
end_O3_Lin_4a = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,0,59)
O3_Lin_4a = Calibrations[start_O3_Lin_4a:end_O3_Lin_4a]
O3_Lin_4a_mean = O3_Lin_4a['O3 (ppb)'].mean() 
O3_Lin_4a_real = 60

start_O3_Lin_4b = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,3,00)
end_O3_Lin_4b = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,9,59)
O3_Lin_4b = Calibrations[start_O3_Lin_4b:end_O3_Lin_4b]
O3_Lin_4b_mean = O3_Lin_4b['O3 (ppb)'].mean() 
O3_Lin_4b_real = 150

start_O3_Lin_4c = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,13,00)
end_O3_Lin_4c = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,31,59)
O3_Lin_4c = Calibrations[start_O3_Lin_4c:end_O3_Lin_4c]
O3_Lin_4c_mean = O3_Lin_4c['O3 (ppb)'].mean() 
O3_Lin_4c_real = 100

start_O3_Lin_4d = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,34,00)
end_O3_Lin_4d = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,41,59)
O3_Lin_4d = Calibrations[start_O3_Lin_4d:end_O3_Lin_4d]
O3_Lin_4d_mean = O3_Lin_4d['O3 (ppb)'].mean() 
O3_Lin_4d_real = 30

start_O3_Zero_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,44,00)
end_O3_Zero_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,10,17,59)
O3_Zero_4 = Calibrations[start_O3_Zero_4:end_O3_Zero_4]
O3_Zero_4_mean = O3_Zero_4['O3 (ppb)'].mean() 


start_CO_Zero_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,35,00)
end_CO_Zero_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,37,59)
CO_Zero_4 = Calibrations[start_CO_Zero_4:end_CO_Zero_4]
CO_Zero_4_mean = CO_Zero_4['CO (ppb)'].min()

start_CO_Cal_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,42,00)
end_CO_Cal_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,45,59)
CO_Cal_4 = Calibrations[start_CO_Cal_4:end_CO_Cal_4]
CO_Cal_4_mean = CO_Cal_4['CO (ppb)'].max()  
Calibrations.loc[start_CO_Cal_4:end_CO_Cal_4, ('CO_calibration_cylinder_ppb')] = 200

start_CO_Lin_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,9,56,00)
end_CO_Lin_4 = datetime.datetime(year_Audit_4,month_Audit_4,day_Audit_4,11,34,59)
CO_Lin_4 = Calibrations[start_CO_Lin_4:end_CO_Lin_4]

minimum = min(start_Audit_4,end_Audit_4)
maximum = max(start_Audit_4,end_Audit_4)

Calibrations.loc[minimum:maximum, ('NO_Zero_Mean')] = NO_Zero_mean_4
Calibrations.loc[minimum:maximum, ('NO_Cal_Mean')] = NO_NO_Cal_4 
Calibrations.loc[minimum:maximum, ('NOy_Zero_Mean')] = NOy_Zero_mean_4
Calibrations.loc[minimum:maximum, ('NOy_Cal_Mean')] = NOy_NO_Cal_4
Calibrations.loc[minimum:maximum, ('Diff_Cal_Mean')] = NOy_Diff_Cal_4b - NO_Diff_Cal_4b

Calibrations.loc[minimum:maximum, ('O3_Zero_Mean')] = O3_Zero_4_mean
Calibrations.loc[minimum:maximum, ('O3_Cal_Mean')] = O3_Cal_4_mean
Calibrations.loc[minimum:maximum, ('NO2_Zero_Mean')] = NO2_Zero_4_mean
Calibrations.loc[minimum:maximum, ('NO2_Cal_Mean')] = NO2_Cal_4_mean 
Calibrations.loc[minimum:maximum, ('CO_Zero_Mean')] = CO_Zero_4_mean
Calibrations.loc[minimum:maximum, ('CO_Cal_Mean')] = CO_Cal_4_mean 

#Audit 4 Date 30 March 2021
Calibrations.loc[minimum:maximum, ('O3_calibration_cylinder_ppb')] = 200 
Calibrations.loc[minimum:maximum, ('NO_calibration_cylinder_ppb')] = 488 #NO 488 original 434
Calibrations.loc[minimum:maximum, ('NO2_calibration_cylinder_ppb')] = 439 #NO2 439 original 395
Calibrations.loc[minimum:maximum, ('CO_calibration_cylinder_ppb')] = 10.9*1000 
Calibrations.loc[minimum:maximum, ('O3_lit_Zero')] =  0
Calibrations.loc[minimum:maximum, ('O3_lit_Response')] = 1.044
Calibrations.loc[minimum:maximum, ('NO_lit_Zero')] =  -0.01
Calibrations.loc[minimum:maximum, ('NO_lit_Response')] = 1.384
Calibrations.loc[minimum:maximum, ('NOy_lit_Zero')] =  0.4
Calibrations.loc[minimum:maximum, ('NOy_lit_Response')] =  1.367
Calibrations.loc[minimum:maximum, ('NO2_lit_Zero')] =  -0.01
Calibrations.loc[minimum:maximum, ('NO2_lit_Response')] =  1.0
Calibrations.loc[minimum:maximum, ('CO_lit_Zero')] =  3
Calibrations.loc[minimum:maximum, ('CO_lit_Response')] = 10.9/(14.29-3.14)


start_NOy_Zero_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,7,29,00)
end_NOy_Zero_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,7,35,59)
NOy_Zero_5 = Calibrations[start_NOy_Zero_5:end_NOy_Zero_5]
NO_Zero_mean_5 = NOy_Zero_5['NO (ppb)'].mean()
NOy_Zero_mean_5 = NOy_Zero_5['NOy (ppb)'].mean()

start_NO_Cal_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,7,41,00)
end_NO_Cal_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,7,45,59)
NO_Cal_5 = Calibrations[start_NO_Cal_5:end_NO_Cal_5]
NO_NO_Cal_5 = NO_Cal_5['NO (ppb)'].mean()
NOy_NO_Cal_5 = NO_Cal_5['NOy (ppb)'].mean()

start_Diff_Cal_5a = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,7,50,00)
end_Diff_Cal_5a = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,7,55,59)
Diff_Cal_5a = Calibrations[start_Diff_Cal_5a:end_Diff_Cal_5a]
NO_Diff_Cal_5a = Diff_Cal_5a['NO (ppb)'].mean()
NOy_Diff_Cal_5a = Diff_Cal_5a['NOy (ppb)'].mean()

start_NOy_Lin_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,59,00)
end_NOy_Lin_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,10,39,59)
NOy_Lin_5 = Calibrations[start_NOy_Lin_5:end_NOy_Lin_5]

start_Diff_Cal_5b = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,11,0,00)
end_Diff_Cal_5b = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,11,4,59)
Diff_Cal_5b = Calibrations[start_Diff_Cal_5b:end_Diff_Cal_5b]
NO_Diff_Cal_5b = Diff_Cal_5b['NO (ppb)'].mean()
NOy_Diff_Cal_5b = Diff_Cal_5b['NOy (ppb)'].mean()

start_NO2_Zero_5a = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,0,00)
end_NO2_Zero_5a = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,10,59)
NO2_Zero_5a = Calibrations[start_NO2_Zero_5a:end_NO2_Zero_5a]
NO2_Zero_5a_mean = NO2_Zero_5a['NO2 (ppb)'].mean()

start_NO2_Cal_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,18,00)
end_NO2_Cal_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,21,59)
NO2_Cal_5 = Calibrations[start_NO2_Cal_5:end_NO2_Cal_5]
NO2_Cal_5_mean = NO2_Cal_5['NO2 (ppb)'].mean()

start_NO2_Lin_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,9,45,00)
end_NO2_Lin_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,10,35,59)
NO2_Lin_5 = Calibrations[start_NO2_Lin_5:end_NO2_Lin_5]

start_NO2_Zero_5b = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,10,39,00)
end_NO2_Zero_5b = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,10,43,59)
NO2_Zero_5b = Calibrations[start_NO2_Zero_5b:end_NO2_Zero_5b]
NO2_Zero_5b_mean = NO2_Zero_5b['NO2 (ppb)'].mean()

start_O3_Cal_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,8,00)
end_O3_Cal_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,20,59)
O3_Cal_5 = Calibrations[start_O3_Cal_5:end_O3_Cal_5]
O3_Cal_5_mean = O3_Cal_5['O3 (ppb)'].mean()  
Calibrations.loc[start_O3_Cal_5:end_O3_Cal_5, ('O3_calibration_cylinder_ppb')] = 200

start_O3_Lin_5a = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,22,00)
end_O3_Lin_5a = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,25,59)
O3_Lin_5a = Calibrations[start_O3_Lin_5a:end_O3_Lin_5a]
O3_Lin_5a_mean = O3_Lin_5a['O3 (ppb)'].mean() 
O3_Lin_5a_real = 29.8

start_O3_Lin_5b = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,27,00)
end_O3_Lin_5b = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,33,59)
O3_Lin_5b = Calibrations[start_O3_Lin_5b:end_O3_Lin_5b]
O3_Lin_5b_mean = O3_Lin_5b['O3 (ppb)'].mean() 
O3_Lin_5b_real = 100

start_O3_Lin_5c = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,35,00)
end_O3_Lin_5c = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,39,59)
O3_Lin_5c = Calibrations[start_O3_Lin_5c:end_O3_Lin_5c]
O3_Lin_5c_mean = O3_Lin_5c['O3 (ppb)'].mean() 
O3_Lin_5c_real = 150

start_O3_Lin_5d = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,41,00)
end_O3_Lin_5d = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,50,59)
O3_Lin_5d = Calibrations[start_O3_Lin_5d:end_O3_Lin_5d]
O3_Lin_5d_mean = O3_Lin_5d['O3 (ppb)'].mean() 
O3_Lin_5d_real = 60

start_O3_Zero_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,53,00)
end_O3_Zero_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,9,15,59)
O3_Zero_5 = Calibrations[start_O3_Zero_5:end_O3_Zero_5]
O3_Zero_5_mean = O3_Zero_5['O3 (ppb)'].mean() 


start_CO_Zero_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,6,00)
end_CO_Zero_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,13,59)
CO_Zero_5 = Calibrations[start_CO_Zero_5:end_CO_Zero_5]
CO_Zero_5_mean = CO_Zero_5['CO (ppb)'].mean()

start_CO_Cal_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,26,00)
end_CO_Cal_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,31,59)
CO_Cal_5 = Calibrations[start_CO_Cal_5:end_CO_Cal_5]
CO_Cal_5_mean = CO_Cal_5['CO (ppb)'].mean()  

start_CO_Lin_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,8,53,00)
end_CO_Lin_5 = datetime.datetime(year_Audit_5,month_Audit_5,day_Audit_5,10,41,59)
CO_Lin_5 = Calibrations[start_CO_Lin_5:end_CO_Lin_5]

minimum = min(start_Audit_5,end_Audit_5)
maximum = max(start_Audit_5,end_Audit_5)

Calibrations.loc[minimum:maximum, ('NO_Zero_Mean')] = NO_Zero_mean_5
Calibrations.loc[minimum:maximum, ('NO_Cal_Mean')] = NO_NO_Cal_5 
Calibrations.loc[minimum:maximum, ('NOy_Zero_Mean')] = NOy_Zero_mean_5
Calibrations.loc[minimum:maximum, ('NOy_Cal_Mean')] = NOy_NO_Cal_5
Calibrations.loc[minimum:maximum, ('Diff_Cal_Mean')] = NOy_Diff_Cal_5a - NO_Diff_Cal_5a

Calibrations.loc[minimum:maximum, ('O3_Zero_Mean')] = O3_Zero_5_mean
Calibrations.loc[minimum:maximum, ('O3_Cal_Mean')] = O3_Cal_5_mean
Calibrations.loc[minimum:maximum, ('NO2_Zero_Mean')] = NO2_Zero_5a_mean
Calibrations.loc[minimum:maximum, ('NO2_Cal_Mean')] = NO2_Cal_5_mean
Calibrations.loc[minimum:maximum, ('CO_Zero_Mean')] = CO_Zero_5_mean
Calibrations.loc[minimum:maximum, ('CO_Cal_Mean')] = CO_Cal_5_mean 

#Audit 5 Date 27 Oct 2021
Calibrations.loc[minimum:maximum, ('O3_calibration_cylinder_ppb')] = 200
Calibrations.loc[minimum:maximum, ('NO_calibration_cylinder_ppb')] = 434 
Calibrations.loc[minimum:maximum, ('NO2_calibration_cylinder_ppb')] = 395 
Calibrations.loc[minimum:maximum, ('CO_calibration_cylinder_ppb')] = 10.9*1000 
Calibrations.loc[minimum:maximum, ('O3_lit_Zero')] =  -0.3
Calibrations.loc[minimum:maximum, ('O3_lit_Response')] = 0.968
Calibrations.loc[minimum:maximum, ('NO_lit_Zero')] =  -0.01
Calibrations.loc[minimum:maximum, ('NO_lit_Response')] = 1.384
Calibrations.loc[minimum:maximum, ('NOy_lit_Zero')] =  0.4
Calibrations.loc[minimum:maximum, ('NOy_lit_Response')] =  1.367
Calibrations.loc[minimum:maximum, ('NO2_lit_Zero')] =  0
Calibrations.loc[minimum:maximum, ('NO2_lit_Response')] =  0.98
Calibrations.loc[minimum:maximum, ('CO_lit_Zero')] =  3
Calibrations.loc[minimum:maximum, ('CO_lit_Response')] = 10.9/(14.29-3.14)


start_NOy_Zero_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,8,51,00)
end_NOy_Zero_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,8,55,59)
NOy_Zero_6 = Calibrations[start_NOy_Zero_6:end_NOy_Zero_6]
NO_Zero_mean_6 = NOy_Zero_6['NO (ppb)'].mean()
NOy_Zero_mean_6 = NOy_Zero_6['NOy (ppb)'].mean()

start_NO_Cal_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,9,11,00)
end_NO_Cal_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,9,13,59)
NO_Cal_6 = Calibrations[start_NO_Cal_6:end_NO_Cal_6]
NO_NO_Cal_6 = NO_Cal_6['NO (ppb)'].mean()
NOy_NO_Cal_6 = NO_Cal_5['NOy (ppb)'].mean()

start_Diff_Cal_6a = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,9,20,00)
end_Diff_Cal_6a = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,9,23,59)
Diff_Cal_6a = Calibrations[start_Diff_Cal_6a:end_Diff_Cal_6a]
NO_Diff_Cal_6a = Diff_Cal_6a['NO (ppb)'].mean()
NOy_Diff_Cal_6a = Diff_Cal_6a['NOy (ppb)'].mean()

start_NOy_Lin_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,36,00)
end_NOy_Lin_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,12,8,59)
NOy_Lin_6 = Calibrations[start_NOy_Lin_6:end_NOy_Lin_6]

start_NO2_Zero_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,8,47,00)
end_NO2_Zero_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,8,59,59)
NO2_Zero_6 = Calibrations[start_NO2_Zero_6:end_NO2_Zero_6]
NO2_Zero_6_mean = NO2_Zero_6['NO2 (ppb)'].mean()

start_NO2_Cal_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,9,27,00)
end_NO2_Cal_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,9,32,59)
NO2_Cal_6 = Calibrations[start_NO2_Cal_6:end_NO2_Cal_6]
NO2_Cal_6_mean = NO2_Cal_6['NO2 (ppb)'].max()

start_NO2_Lin_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,37,00)
end_NO2_Lin_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,12,15,59)
NO2_Lin_6 = Calibrations[start_NO2_Lin_6:end_NO2_Lin_6]

start_O3_Cal_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,9,38,00)
end_O3_Cal_6= datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,9,49,59)
O3_Cal_6 = Calibrations[start_O3_Cal_6:end_O3_Cal_6]
O3_Cal_6_mean = O3_Cal_6['O3 (ppb)'].mean() 
Calibrations.loc[start_O3_Cal_6:end_O3_Cal_6, ('O3_calibration_cylinder_ppb')] = 200

start_O3_Lin_6b = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,9,52,00)
end_O3_Lin_6b = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,9,57,59)
O3_Lin_6b = Calibrations[start_O3_Lin_6b:end_O3_Lin_6b]
O3_Lin_6b_mean = O3_Lin_6b['O3 (ppb)'].mean() 
O3_Lin_6b_real = 30

start_O3_Lin_6c = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,9,59,00)
end_O3_Lin_6c = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,3,59)
O3_Lin_6c = Calibrations[start_O3_Lin_6c:end_O3_Lin_6c]
O3_Lin_6c_mean = O3_Lin_6c['O3 (ppb)'].mean() 
O3_Lin_6c_real = 100

start_O3_Lin_6d = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,6,00)
end_O3_Lin_6d = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,10,59)
O3_Lin_6d = Calibrations[start_O3_Lin_6d:end_O3_Lin_6d]
O3_Lin_6d_mean = O3_Lin_6d['O3 (ppb)'].mean() 
O3_Lin_6d_real = 150

start_O3_Zero_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,18,00)
end_O3_Zero_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,21,59)
O3_Zero_6 = Calibrations[start_O3_Zero_6:end_O3_Zero_6]
O3_Zero_6_mean = O3_Zero_6['O3 (ppb)'].mean() 

start_O3_Lin_6a = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,26,00)
end_O3_Lin_6a = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,33,59)
O3_Lin_6a = Calibrations[start_O3_Lin_6a:end_O3_Lin_6a]
O3_Lin_6a_mean = O3_Lin_6a['O3 (ppb)'].mean()  
O3_Lin_6a_real = 200


start_CO_Zero_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,0,00)
end_CO_Zero_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,4,59)
CO_Zero_6 = Calibrations[start_CO_Zero_6:end_CO_Zero_6]
CO_Zero_6_mean = CO_Zero_6['CO (ppb)'].mean()

start_CO_Cal_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,11,00)
end_CO_Cal_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,17,59)
CO_Cal_6 = Calibrations[start_CO_Cal_6:end_CO_Cal_6]
CO_Cal_6_mean = CO_Cal_6['CO (ppb)'].max()  

start_CO_Lin_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,10,22,00)
end_CO_Lin_6 = datetime.datetime(year_Audit_6,month_Audit_6,day_Audit_6,12,7,59)
CO_Lin_6 = Calibrations[start_CO_Lin_6:end_CO_Lin_6]

minimum = min(start_Audit_6,end_Audit_6)
maximum = max(start_Audit_6,end_Audit_6)

Calibrations.loc[minimum:maximum, ('NO_Zero_Mean')] = NO_Zero_mean_6
Calibrations.loc[minimum:maximum, ('NO_Cal_Mean')] = NO_NO_Cal_6
Calibrations.loc[minimum:maximum, ('NOy_Zero_Mean')] = NOy_Zero_mean_6
Calibrations.loc[minimum:maximum, ('NOy_Cal_Mean')] = NOy_NO_Cal_6
Calibrations.loc[minimum:maximum, ('Diff_Cal_Mean')] = NOy_Diff_Cal_6a - NO_Diff_Cal_6a

Calibrations.loc[minimum:maximum, ('O3_Zero_Mean')] = O3_Zero_6_mean
Calibrations.loc[minimum:maximum, ('O3_Cal_Mean')] = O3_Cal_6_mean
Calibrations.loc[minimum:maximum, ('NO2_Zero_Mean')] = NO2_Zero_6_mean
Calibrations.loc[minimum:maximum, ('NO2_Cal_Mean')] = NO2_Cal_6_mean
Calibrations.loc[minimum:maximum, ('CO_Zero_Mean')] = CO_Zero_6_mean
Calibrations.loc[minimum:maximum, ('CO_Cal_Mean')] = CO_Cal_6_mean 

#Audit 6 Date 4th May 2022
Calibrations.loc[minimum:maximum, ('O3_calibration_cylinder_ppb')] = 200
Calibrations.loc[minimum:maximum, ('NO_calibration_cylinder_ppb')] = 530 
Calibrations.loc[minimum:maximum, ('NO2_calibration_cylinder_ppb')] = 400 
Calibrations.loc[minimum:maximum, ('CO_calibration_cylinder_ppb')] = 10.56*1000 
Calibrations.loc[minimum:maximum, ('O3_lit_Zero')] =  0.2
Calibrations.loc[minimum:maximum, ('O3_lit_Response')] = 0.915
Calibrations.loc[minimum:maximum, ('NO_lit_Zero')] =  0
Calibrations.loc[minimum:maximum, ('NO_lit_Response')] = 1.683
Calibrations.loc[minimum:maximum, ('NOy_lit_Zero')] =  0.9
Calibrations.loc[minimum:maximum, ('NOy_lit_Response')] =  1.715
Calibrations.loc[minimum:maximum, ('NO2_lit_Zero')] =  0
Calibrations.loc[minimum:maximum, ('NO2_lit_Response')] =  0.95
Calibrations.loc[minimum:maximum, ('CO_lit_Zero')] =  6.12*1000
Calibrations.loc[minimum:maximum, ('CO_lit_Response')] = 0.842

Calibrations.drop(Calibrations[(Calibrations['O3_Cal_Mean'].isnull())].index,inplace =True)

Calibrations = Calibrations.drop(columns=['NO (ppb)','Diff (ppb)','NOy (ppb)','NOy Flow (l/min)','NOy Pressure (mmHG)','NOy_Prov_Status','NOy Cal Status'])
Calibrations = Calibrations.drop(columns=['NO2 (ppb)', 'NO2_Prov_Status', 'O3 (ppb)', 'O3_Prov_Status'])
Calibrations = Calibrations.drop(columns=['CO_Prov_Status','CO (ppb)','Cal Status'])

Calibrations['O3_-1_offset'] = Calibrations['O3_Cal_Mean'].shift(periods=-1)
Calibrations['O3_+1_offset'] = Calibrations['O3_Cal_Mean'].shift(periods=1)

Calibrations['O3_offset_flags'] = np.where((Calibrations['O3_Cal_Mean'] != Calibrations['O3_-1_offset']), 1, 0)
Calibrations['O3_offset_flags'] = np.where((Calibrations['O3_Cal_Mean'] != Calibrations['O3_+1_offset']), 1, Calibrations['O3_offset_flags'])

Calibrations.drop(Calibrations[(Calibrations['O3_offset_flags'] == 0)].index,inplace =True)

Calibrations = Calibrations.drop(columns=['O3_-1_offset', 'O3_+1_offset', 'O3_offset_flags'])
#Calibrations.to_csv(str(Data_Output_Folder) + '1_Gas_Calibration_measurements_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

Calibrations['O3_Response'] = Calibrations['O3_calibration_cylinder_ppb']/(Calibrations['O3_Cal_Mean'] - Calibrations['O3_Zero_Mean'])
Calibrations['O3_Slope'] = Calibrations['O3_calibration_cylinder_ppb']/(Calibrations['O3_Cal_Mean'] - Calibrations['O3_Zero_Mean'])
Calibrations['O3_Intercept'] = 0 - Calibrations['O3_Slope']*Calibrations['O3_Zero_Mean']

Calibrations['NO2_Response'] = Calibrations['NO2_calibration_cylinder_ppb']/(Calibrations['NO2_Cal_Mean'] - Calibrations['NO2_Zero_Mean'])
Calibrations['NO2_Slope'] = Calibrations['NO2_calibration_cylinder_ppb']/(Calibrations['NO2_Cal_Mean'] - Calibrations['NO2_Zero_Mean'])

Calibrations.loc[start_Audit_1:end_Audit_1, ('NO2_Response')] = 0.954
Calibrations.loc[start_Audit_1:end_Audit_1, ('NO2_Slope')] = 0.954

Calibrations.loc[start_Audit_3:end_Audit_3, ('NO2_Response')] = 0.992 # no notes about concentration of NO2 cyclinder on 2nd Oct so taken from Audit certificates
Calibrations.loc[start_Audit_3:end_Audit_3, ('NO2_Slope')] = 0.992 # no notes about concentration of NO2 cyclinder on 2nd Oct so taken from Audit certificates

Calibrations['NO2_Intercept'] = 0 - Calibrations['NO2_Slope']*Calibrations['NO2_Zero_Mean']

#NO2_O3_Cals = Calibrations[['O3_Zero_Mean', 'O3_Response', 'O3_Intercept', 'O3_Slope', 'O3_lit_Zero', 'O3_lit_Response', 'NO2_Zero_Mean', 'NO2_Response', 'NO2_Intercept', 'NO2_Slope', 'NO2_lit_Zero', 'NO2_lit_Response']]

#NO2_O3_Cals.to_csv(str(Data_Output_Folder) + '13_NO2_O3_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

Calibrations['datetime'] = Calibrations.index


#Start Audit
cal_Freq = '60min' # 12 August 2022
start_file_date = datetime.datetime(2022,8,12,0,0,00)

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
    Monthly_files = str(Data_Source_Folder) + x + '*_firsgas.csv'
    csv_files = glob.glob(Monthly_files) 

    gas_frames = []
    
    for csv in csv_files:
        #csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
        df = pd.read_csv(csv, skiprows=1, header=None, usecols=[0,1,12,20])
        gas_frames.append(df)
        
    all_Data = pd.concat(gas_frames)
    
    all_Data.rename(columns={0: 'Date', 1: 'Time', 12: 'CO (ppb)', 20: 'CO Flags'}, inplace=True)
    
    all_Data['Date'] = all_Data['Date'].astype(str)
    all_Data['Time'] = all_Data['Time'].astype(str)
    all_Data['Date_length'] = all_Data['Date'].str.len()
    all_Data['Time_length'] = all_Data['Time'].str.len()
    all_Data=all_Data.loc[all_Data.Date_length == 10] #check the data string length for corruption
    all_Data=all_Data.loc[all_Data.Time_length == 8]
    all_Data['datetime'] = all_Data['Date']+' '+all_Data['Time']# added Date and time into new columns
    all_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in all_Data['datetime']] #converts the dateTime format from string to python dateTime
    all_Data.index = all_Data['datetime']
    all_Data = all_Data.sort_index()
    all_Data = all_Data.drop(columns=['Date', 'Time','Date_length','Time_length'])
    
    all_Data['CO Flags'] = all_Data['CO Flags'].astype(str)
    all_Data['CO_Flags_Prov'] = np.where(all_Data['CO Flags'] == 'FFFFFFFF', 0, all_Data['CO Flags'])
    all_Data['CO Flags'] = all_Data['CO_Flags_Prov']
    all_Data['CO (ppb)'] = np.where(all_Data['CO Flags'] == 0, np.nan, all_Data['CO (ppb)'])
    all_Data = all_Data.drop(columns=['CO_Flags_Prov'])
    
    if x == str(start_date_str):
        CO_Cal_Check = all_Data
    else:
        CO_Cal_Check = pd.concat([CO_Cal_Check, all_Data])
        CO_Cal_Check = CO_Cal_Check.sort_index()

CO_Cal_Check.drop(CO_Cal_Check[(CO_Cal_Check['CO (ppb)'].isnull() )].index,inplace =True)
CO_Cal_Check['CO (ppb)'] = CO_Cal_Check['CO (ppb)'].astype(float)
CO_Cal_Check.drop(CO_Cal_Check[(CO_Cal_Check['CO (ppb)']==0 )].index,inplace =True)

CO_Cal_Check['CO (ppb)'] = CO_Cal_Check['CO (ppb)'].astype(str)
CO_Cal_Check['CO_str_length'] = CO_Cal_Check['CO (ppb)'].str.len()
CO_Cal_Check=CO_Cal_Check[CO_Cal_Check.CO_str_length >= 1] 
CO_Cal_Check=CO_Cal_Check[CO_Cal_Check.CO_str_length <= 22]
CO_Cal_Check=CO_Cal_Check.drop(columns=['CO_str_length'])
CO_Cal_Check['CO (ppb)'] = CO_Cal_Check['CO (ppb)'].astype(float)
print(CO_Cal_Check)

CO_Cal_Check['CO_Prelim_Flag'] = np.where(CO_Cal_Check['CO Flags'].str.contains('8C041', case=False, na=False), 2, CO_Cal_Check['CO Flags'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where(CO_Cal_Check['CO Flags'].str.contains('8C06', case=False, na=False), 2, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where(CO_Cal_Check['CO Flags'].str.contains('8C045', case=False, na=False), 2, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where(CO_Cal_Check['CO Flags'].str.contains('8C049', case=False, na=False), 2, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where(CO_Cal_Check['CO Flags'].str.contains('AC0', case=False, na=False), 2, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C040000'), 1, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='FFFFFFFF'), 2, CO_Cal_Check['CO_Prelim_Flag']) #0
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags'].isnull() ), 0, CO_Cal_Check['CO_Prelim_Flag']) #0
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C040001'), 2, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C040005'), 2, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C040400'), 2, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C041415'), 2, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C040401'), 2, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C044000'), 2, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C050000'), 2, CO_Cal_Check['CO_Prelim_Flag']) #0
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C050400'), 2, CO_Cal_Check['CO_Prelim_Flag']) #0
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C070000'), 2, CO_Cal_Check['CO_Prelim_Flag']) #0
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C070001'), 2, CO_Cal_Check['CO_Prelim_Flag']) #0
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C074000'), 2, CO_Cal_Check['CO_Prelim_Flag']) #0
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='AC040000'), 2, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = np.where((CO_Cal_Check['CO Flags']=='8C041000'), 2, CO_Cal_Check['CO_Prelim_Flag'])
CO_Cal_Check['CO_Prelim_Flag'] = CO_Cal_Check['CO_Prelim_Flag'].astype(float)
CO_Cal_Check['CO_Prelim_Flag'] = CO_Cal_Check['CO_Prelim_Flag'].astype(int)
       
CO_Cal_Check.drop(CO_Cal_Check[(CO_Cal_Check['CO Flags'] =='0C100000')].index,inplace =True)

#print(start_file_date)
start = datetime.datetime(int(start_file_date.strftime("%Y")),int(start_file_date.strftime("%m")),int(start_file_date.strftime("%d")),0,0,00) 
end = datetime.datetime(int(today.strftime("%Y")),int(today.strftime("%m")),int(today.strftime("%d")),23,59,59) 

CO_Cal_Check = CO_Cal_Check[start:end]
CO_Cal_Check = CO_Cal_Check.groupby(pd.Grouper(freq=av_Freq)).mean()

min_CO_flag = CO_Cal_Check['CO_Prelim_Flag'].groupby(pd.Grouper(freq=av_Freq)).min()
max_CO_flag = CO_Cal_Check['CO_Prelim_Flag'].groupby(pd.Grouper(freq=av_Freq)).max()
CO_Cal_Check = CO_Cal_Check.groupby(pd.Grouper(freq=av_Freq)).mean()
CO_Cal_Check['min_CO_flag'] = pd.Series(min_CO_flag)
CO_Cal_Check['max_CO_flag'] = pd.Series(max_CO_flag)
CO_Cal_Check['CO_Prov_Status'] = CO_Cal_Check['max_CO_flag']
CO_Cal_Check.drop(CO_Cal_Check[(CO_Cal_Check['CO_Prov_Status'].isnull())].index,inplace =True)
CO_Cal_Check = CO_Cal_Check.drop(columns=['min_CO_flag', 'max_CO_flag'])
CO_Cal_Check['datetime'] = CO_Cal_Check.index


#CO_Cal_Data.to_csv(str(Data_Output_Folder) + '8_CO_Auto-Zeros_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

#Calibrations.to_csv(str(Data_Output_Folder) + '1_Gas_Calibration_measurements_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

if CO_Data_Source == 'database':
    CO_Cal_Data = CO_Cal_Data[['CO Data Zero (ppb)', 'datetime']]
    CO_Cal_Data.rename(columns={'CO Data Zero (ppb)': 'CO Zero (ppb)'}, inplace=True)

else:
    CO_Cal_Data = CO_Cal_Data[['CO Logfile Zero (ppb)', 'datetime']]
    CO_Cal_Data.rename(columns={'CO Logfile Zero (ppb)': 'CO Zero (ppb)'}, inplace=True)
print(CO_Cal_Data)

CO_Cal_Check['CO a'] = np.interp(CO_Cal_Check['datetime'], CO_Cal_Data['datetime'], CO_Cal_Data['CO Zero (ppb)'])

CO_Cal_Check['CO (ppb)'] = CO_Cal_Check['CO (ppb)'] - CO_Cal_Check['CO a']
CO_Cal_Check = CO_Cal_Check.drop(columns=['CO a','datetime', 'CO_Prelim_Flag','CO_Prov_Status'])
CO_Cal_Check=CO_Cal_Check[CO_Cal_Check['CO (ppb)'] > 5000]

CO_Cal_Check = CO_Cal_Check.groupby(pd.Grouper(freq=av_Freq)).mean()
CO_Cal_Check['Multi C Cal'] = np.where(CO_Cal_Check['CO (ppb)'].isnull() , np.nan, 1)

CO_Cal_Check['Cal-1'] = CO_Cal_Check['Multi C Cal'].shift(periods=-1)
CO_Cal_Check['Cal+1'] = CO_Cal_Check['Multi C Cal'].shift(periods=1)
CO_Cal_Check.drop(CO_Cal_Check[(CO_Cal_Check['Cal-1'].isnull() )].index,inplace =True) 
CO_Cal_Check.drop(CO_Cal_Check[(CO_Cal_Check['Cal+1'].isnull() )].index,inplace =True) 

CO_Cal_Check = CO_Cal_Check.groupby(pd.Grouper(freq=cal_Freq)).mean()
CO_Cal_Check.drop(CO_Cal_Check[(CO_Cal_Check['CO (ppb)'].isnull() )].index,inplace =True) 
CO_Cal_Check.rename(columns={'CO (ppb)': 'CO Cal'}, inplace=True)
CO_Cal_Check['CO Cal'] = 5000/(CO_Cal_Check['CO Cal'])
CO_Cal_Check = CO_Cal_Check.drop(columns=['Multi C Cal', 'Cal-1','Cal+1'])

CO_Cal_Check.rename(columns={'CO Cal' : 'CO_Response' }, inplace=True)
print(CO_Cal_Check)

if CO_Adjustments == True:
    Cal_CO_Inter = Calibrations[['CO_Zero_Mean', 'datetime']]
    Cal_CO_Inter['CO a'] = np.interp(Cal_CO_Inter['datetime'], CO_Cal_Data['datetime'], CO_Cal_Data['CO Zero (ppb)'])
    Cal_CO_Inter['CO_Zero_Diff'] = np.where((Cal_CO_Inter['CO_Zero_Mean'] < Cal_CO_Inter['CO a']), (Cal_CO_Inter['CO_Zero_Mean'] - Cal_CO_Inter['CO a']), 0)
    
    Calibrations['CO_Zero_Diff'] = np.interp(Calibrations['datetime'], Cal_CO_Inter['datetime'], Cal_CO_Inter['CO_Zero_Diff'])
    Calibrations['CO a'] = np.interp(Calibrations['datetime'], CO_Cal_Data['datetime'], CO_Cal_Data['CO Zero (ppb)'])
    Calibrations['CO_True_Zero (ppb)'] = Calibrations['CO a'] + Calibrations['CO_Zero_Diff']
    Calibrations['CO_Response'] = Calibrations['CO_calibration_cylinder_ppb']/(Calibrations['CO_True_Zero (ppb)'] - Calibrations['CO_Cal_Mean'])
    Calibrations = Calibrations.drop(columns=['CO_True_Zero (ppb)', 'CO a', 'CO_Zero_Diff'])
    Calibrations.drop(Calibrations[(Calibrations['O3_Cal_Mean'].isnull())].index,inplace =True)
    Calibrations = pd.concat([Calibrations, CO_Cal_Data])
    Calibrations = Calibrations.sort_index()
    Calibrations['CO_Zero_Diff'] = np.interp(Calibrations['datetime'], Cal_CO_Inter['datetime'], Cal_CO_Inter['CO_Zero_Diff'])
    Calibrations['CO_True_Zero (ppb)'] = Calibrations['CO Zero (ppb)'] + Calibrations['CO_Zero_Diff']
    Calibrations['CO_Zero_Flag'] = np.where((Calibrations['CO_True_Zero (ppb)'].notnull()), 1, 0)
    Calibrations['CO_Zero_Flag'] = np.where((Calibrations['O3_Cal_Mean'].notnull()), 1, Calibrations['CO_Zero_Flag'])
    Calibrations.drop(Calibrations[(Calibrations['CO_Zero_Flag'] == 0)].index,inplace =True)
    Calibrations = Calibrations.drop(columns=['CO_Zero_Flag', 'CO_Zero_Diff', 'CO Zero (ppb)'])
    Calibrations.rename(columns={'CO_True_Zero (ppb)': 'CO Zero (ppb)'}, inplace=True)

else:
    Calibrations['CO a'] = np.interp(Calibrations['datetime'], CO_Cal_Data['datetime'], CO_Cal_Data['CO Zero (ppb)'])
    Calibrations['CO_Response'] = Calibrations['CO_calibration_cylinder_ppb']/(Calibrations['CO_Cal_Mean'] - Calibrations['CO a'])
    Calibrations.drop(Calibrations[(Calibrations['O3_Cal_Mean'].isnull())].index,inplace =True)
    Calibrations = Calibrations.drop(columns=['CO a'])    
    Calibrations = pd.concat([Calibrations, CO_Cal_Data, CO_Cal_Check])
    Calibrations = Calibrations.sort_index()
    Calibrations.loc[start_Audit_3:end_Audit_3, ('CO_Response')] = 1.017 # no notes about concentration of CO cyclinder on 2nd Oct so taken from Audit certificates

Calibrations = pd.concat([Calibrations, CO_Cal_Check])

Calibrations = Calibrations.sort_index()

#Calibrations.to_csv(str(Data_Output_Folder) + '1_Gas_Calibration_measurements_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

if NOy_Data_Source == 'logbook':
    NOy_Cal_Source = NOy_Cal_Data[['NO_Lit_Zero', 'NO_Lit_Slope', 'datetime']]
    NOy_Cal_Source.rename(columns={'NO_Lit_Zero': 'NO_AutoZero', 'NO_Lit_Slope': 'NO_AutoSlope'}, inplace=True)

else:
    NOy_Cal_Source = NOy_Cal_Data[['NO_Calculated_AutoZero', 'NO_Calculated_Slope', 'datetime']]
    NOy_Cal_Source.rename(columns={'NO_Calculated_AutoZero': 'NO_AutoZero', 'NO_Calculated_Slope': 'NO_AutoSlope'}, inplace=True)

if NOy_Adjustments == True:
    Cal_NOy_Inter = Calibrations[['NO_Zero_Mean', 'NOy_Zero_Mean', 'datetime']]
    Cal_NOy_Inter['NO a'] = np.interp(Cal_NOy_Inter['datetime'], NOy_Cal_Source['datetime'], NOy_Cal_Source['NO_AutoZero'])
    Cal_NOy_Inter['NO_Zero_Diff'] = np.where((Cal_NOy_Inter['NO_Zero_Mean'] < Cal_NOy_Inter['NO a']), (Cal_NOy_Inter['NO_Zero_Mean'] - Cal_NOy_Inter['NO a']), 0)
    Cal_NOy_Inter['NOy_Zero_Diff'] = np.where((Cal_NOy_Inter['NOy_Zero_Mean'] < 3), (Cal_NOy_Inter['NOy_Zero_Mean'] - Cal_NOy_Inter['NO a']), np.nan)
    
    Calibrations['NOy_Zero_Mean'] = np.where(Calibrations['NOy_Zero_Mean']>3, 0.4, Calibrations['NOy_Zero_Mean'])
   
    Calibrations['NO_Response_Prov'] = Calibrations['NO_calibration_cylinder_ppb']/(Calibrations['NO_Zero_Mean'] - Calibrations['NO_Cal_Mean'])
    Calibrations['NOy_Response_Prov'] = Calibrations['NO_calibration_cylinder_ppb']/(Calibrations['NOy_Zero_Mean'] - Calibrations['NOy_Cal_Mean'])
    
    Cal_NOy_Diff = Calibrations[['NO_Response_Prov', 'NOy_Response_Prov', 'datetime']] 
    Cal_NOy_Diff['NO_Response_Differential'] = Cal_NOy_Diff['NO_Response_Prov']/Cal_NOy_Diff['NOy_Response_Prov']
    
    Calibrations = pd.concat([Calibrations, NOy_Cal_Source])
    Calibrations = Calibrations.sort_index()
    Calibrations['NO_Zero_Diff'] = np.interp(Calibrations['datetime'], Cal_NOy_Inter['datetime'], Cal_NOy_Inter['NO_Zero_Diff'])
    Calibrations['NOy_Zero_Diff'] = np.interp(Calibrations['datetime'], Cal_NOy_Inter['datetime'], Cal_NOy_Inter['NOy_Zero_Diff'])
    Calibrations['NO_Response_Differential'] = np.interp(Calibrations['datetime'], Cal_NOy_Inter['datetime'], Cal_NOy_Diff['NO_Response_Differential'])
    Calibrations.rename(columns={'NO_AutoZero': 'NO Zero (ppb)', 'NO_AutoSlope': 'NOy Response'}, inplace=True)
    Calibrations['NOy Zero (ppb)'] = Calibrations['NO Zero (ppb)']
    Calibrations['NO Zero (ppb)'] = Calibrations['NO Zero (ppb)'] + Calibrations['NO_Zero_Diff']
    Calibrations['NOy Zero (ppb)'] = Calibrations['NOy Zero (ppb)'] + Calibrations['NOy_Zero_Diff']
    Calibrations['NO Response'] = Calibrations['NOy Response'] / Calibrations['NO_Response_Differential']
    
    Calibrations['NO-Cal_Flag'] = np.where((Calibrations['CO Zero (ppb)'].notnull()), 1, 0)
    Calibrations['NO-Cal_Flag'] = np.where((Calibrations['O3_Cal_Mean'].notnull()), 1, Calibrations['NO-Cal_Flag'])
    Calibrations['NO-Cal_Flag'] = np.where((Calibrations['NO Response'].notnull()), 1, Calibrations['NO-Cal_Flag'])
    Calibrations.drop(Calibrations[(Calibrations['NO-Cal_Flag'] == 0)].index,inplace =True)
    Calibrations = Calibrations.drop(columns=['NO-Cal_Flag', 'NO_Zero_Diff', 'NOy_Zero_Diff', 'NO_Response_Differential', 'NO_Response_Prov', 'NOy_Response_Prov'])
    
else:
    Calibrations = pd.concat([Calibrations, NOy_Cal_Source])
    Calibrations = Calibrations.sort_index()
    Calibrations.rename(columns={'NO_AutoZero': 'NO Zero (ppb)', 'NO_AutoSlope': 'NO Response'}, inplace=True)
    Calibrations['NOy Zero (ppb)'] = Calibrations['NO Zero (ppb)']
    Calibrations['NOy Response'] = Calibrations['NO Response']
    
#Calibrations.to_csv(str(Data_Output_Folder) + '1_Gas_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')

Calibrations.rename(columns={'NO2_Zero_Mean': 'NO2 Zero (ppb)', 'O3_Zero_Mean': 'O3 Zero (ppb)'}, inplace=True)
Calibrations.rename(columns={'O3_Response': 'O3 Response', 'NO2_Response': 'NO2 Response', 'CO_Response': 'CO Response'}, inplace=True)
Calibrations = Calibrations[['NO Zero (ppb)', 'NO Response','NOy Zero (ppb)', 'NOy Response','O3 Zero (ppb)', 'O3 Response', 'NO2 Zero (ppb)', 'NO2 Response', 'CO Zero (ppb)', 'CO Response', 'datetime']]

Previous_Cal_Check = start_file_date - timedelta(days=1)

Calibrations.loc[Previous_Cal_Check, ('CO Response')] = 0.84047

Calibrations.loc[start_file_date, ('CO Response')] =  0.956669

Calibrations=Calibrations.sort_index()

Calibrations['datetime'] = Calibrations.index

Full_Cal_Folder = str(Data_Output_Folder) + "Gas_Cal_Files/"

if not os.path.exists(Full_Cal_Folder):
    os.makedirs(Full_Cal_Folder)

Old_Cal_Folder = str(Full_Cal_Folder) + "/Previous_Gas_Cal_Files/"

if not os.path.exists(Old_Cal_Folder):
    os.makedirs(Old_Cal_Folder)

full_cal_file = str(Full_Cal_Folder) + '1_Gas_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv'

if os.path.exists(str(full_cal_file)):
    os.rename(str(full_cal_file), str(Data_Output_Folder) + '1_Gas_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '_old.csv')
else:
    pass

#Calibrations.to_csv(str(Full_Cal_Folder) + '1_Gas_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')


pattern = '1_Overall_Gas_Calibrations*.csv'
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

start_accidental_duplicate = datetime.datetime(2023,1,5,10,30,00)
end_accidental_duplicate = datetime.datetime(2023,1,5,11,30,00)
Calibrations.drop(Calibrations.loc[start_accidental_duplicate:end_accidental_duplicate].index, inplace=True)

Calibrations.to_csv(str(Full_Cal_Folder) + '1_Overall_Gas_Calibrations_prior_to_' + str(current_day) + '_' + str(version_number) + '.csv')
