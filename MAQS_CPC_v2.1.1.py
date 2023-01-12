# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 15:01:26 2020

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

sample_Freq = '1sec'
av_Freq = '1min' #averaging frequency required of the data
data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v2.1' #version of the code
year_start = 2022 #input the year of study by number
month_start = 12 #input the month of study by number
default_start_day = 1 #default start date set
day_start = default_start_day
validity_status = 'Ratified' #Ratified or Unratified

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
prior_date_1_str = str(prior_date_1.strftime("%Y")) + str(prior_date_1.strftime("%m")) + str(prior_date_1.strftime("%d"))

prior_date_2 = start - timedelta(days=2)
prior_date_2_str = str(prior_date_2.strftime("%Y")) + str(prior_date_2.strftime("%m")) + str(prior_date_2.strftime("%d"))

later_date_1 = end + timedelta(days=1)
later_date_1_str = str(later_date_1.strftime("%Y")) + str(later_date_1.strftime("%m")) + str(later_date_1.strftime("%d"))

later_date_2 = end + timedelta(days=2)
later_date_2_str = str(later_date_2.strftime("%Y")) + str(later_date_2.strftime("%m")) + str(later_date_2.strftime("%d"))

folder = np.where((str(version_number) == 'v0.6'), 'Preliminary', str(validity_status))
print("using a " + str(folder) + "_" + str(version_number) + " folder")

#instrument installed December 2018
if int(start_year_month_str) < 201812:
    sys.exit("Error Message: There is no data prior to December 2018.")
else:
    pass

#instrument installed In Simon Building between Dec 2018 and June 2019, after which installed in FIRS site
if int(start_year_month_str) < 201906:
    location_input = '_Simon-Building'
    print('Data collected in Simon Building.')
elif int(start_year_month_str) == 201906:
    location_input_1 = '_Simon-Building'
    location_input_2 = '_' #left blank for normal firs site
    print('Data collected at both in Simon Building and at the FIRS site')
else:
    location_input = '_'
    print('Data collected at FIRS site')

instrument_model_1 = '3750'
instrument_model_full_1 = '375000'
instrument_serial_no_1 = '3750180101'
instrument_model_2 = '3772'
instrument_model_full_2 = '3772-CEN'
instrument_serial_no_2 = '3772160904'
instrument_model_3 = '3750'
instrument_model_full_3 = '375000'
instrument_serial_no_3 = '3750180701'

Intercomparison_start = datetime.datetime(2021,2,10,15,44,00)

#CPC change over schedule
if int(start_year_month_str) == 202102:
    Total_CPC_1_Model = instrument_model_1
    Total_CPC_1_Serial_No = instrument_serial_no_1
    Total_CPC_2_Model = instrument_model_2
    Total_CPC_2_Serial_No = instrument_serial_no_2
elif int(start_year_month_str) >= 202103 and int(start_year_month_str) <= 202105:
    Total_CPC_1_Model = 'N/A'
    Total_CPC_1_Serial_No = 'N/A'
    Total_CPC_2_Model = instrument_model_2
    Total_CPC_2_Serial_No = instrument_serial_no_2
elif int(start_year_month_str) >= 202209 and int(start_year_month_str) <= 202212:
    Total_CPC_1_Model = instrument_model_1
    Total_CPC_1_Serial_No = instrument_serial_no_1
    Total_CPC_2_Model = instrument_model_2
    Total_CPC_2_Serial_No = instrument_serial_no_2
elif int(start_year_month_str) > 202212:
    Total_CPC_1_Model = instrument_model_2
    Total_CPC_1_Serial_No = instrument_serial_no_2
    Total_CPC_2_Model = 'N/A'
    Total_CPC_2_Serial_No = 'N/A'
elif int(start_year_month_str) == 202106:
    Total_CPC_1_Model = instrument_model_2
    Total_CPC_1_Serial_No = instrument_serial_no_2
    Total_CPC_2_Model = Total_CPC_1_Model
    Total_CPC_2_Serial_No = Total_CPC_1_Serial_No
elif int(start_year_month_str) >= 202107 and int(start_year_month_str) <= 202108:
    Total_CPC_1_Model = instrument_model_2
    Total_CPC_1_Serial_No = instrument_serial_no_2
    Total_CPC_2_Model = 'N/A'
    Total_CPC_2_Serial_No = 'N/A'
elif int(start_year_month_str) == 202109: # date of intercomparison 16/09/2021 - 27/10/2021 
    Total_CPC_1_Model = instrument_model_2 
    Total_CPC_1_Serial_No = instrument_serial_no_2
    Total_CPC_2_Model = instrument_model_1
    Total_CPC_2_Serial_No = instrument_serial_no_1
elif int(start_year_month_str) == 202110: 
    Total_CPC_1_Model = instrument_model_2 
    Total_CPC_1_Serial_No = instrument_serial_no_2
    Total_CPC_2_Model = instrument_model_1
    Total_CPC_2_Serial_No = instrument_serial_no_1
    switch_over = datetime.datetime(2021,10,27,0,0,00)
elif int(start_year_month_str) == 202111:
    Total_CPC_1_Model = instrument_model_1
    Total_CPC_1_Serial_No = instrument_serial_no_1
    Total_CPC_2_Model = instrument_model_2
    Total_CPC_2_Serial_No = instrument_serial_no_2
    Start_SMPS_Interrupt = datetime.datetime(2021,11,10,12,33,00)
elif int(start_year_month_str) == 202112:
    Total_CPC_1_Model = instrument_model_2
    Total_CPC_1_Serial_No = instrument_serial_no_2
    Total_CPC_2_Model = instrument_model_1
    Total_CPC_2_Serial_No = instrument_serial_no_1
    End_SMPS_Interrupt = datetime.datetime(2021,12,9,17,7,00)
else:
    Total_CPC_1_Model = instrument_model_1
    Total_CPC_1_Serial_No = instrument_serial_no_1
    Total_CPC_2_Model = 'N/A'
    Total_CPC_2_Serial_No = 'N/A'

CPC_2_Add = datetime.datetime(2022,9,1,9,15,00)
CPC_1_Remove = datetime.datetime(2022,12,5,17,45,00)

print('Total CPC 1 is: ' + str(Total_CPC_1_Model))
print('Total CPC 2 is: ' + str(Total_CPC_2_Model))

CPC_folder_1 = 'CPC'
CPC_folder_2 = np.where(int(start_year_month_str) < 202109, '3772', 'CPCCal')
CPC_folder_2 = np.where(int(start_year_month_str) > 202208, '3772', 'CPCCal')
print(CPC_folder_2)

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/', 'D:/FirsData/')

if Total_CPC_2_Model == 'N/A' or Total_CPC_1_Model == 'N/A' or int(start_year_month_str) == 202112:
    print('Only one CPC used.')
    if Total_CPC_2_Model == 'N/A' or int(start_year_month_str) == 202112:
        CPC_Source_Folder = str(Data_Source_Folder) + str(CPC_folder_1) + '/'
        print('Data collected for CPC ' + str(Total_CPC_1_Serial_No) + '.')
    else:
        CPC_Source_Folder = str(Data_Source_Folder) + str(CPC_folder_2) + '/'
        print('Data collected for CPC ' + str(Total_CPC_2_Serial_No) + '.')
    Prior_File_1 = str(CPC_Source_Folder) + str(prior_date_1_str) + '*' + '3750_CPC' + '.csv'
    Prior_File_2 = str(CPC_Source_Folder) + str(prior_date_2_str) + '*' + '3750_CPC' + '.csv'
    Later_File_1 = str(CPC_Source_Folder) + str(later_date_1_str) + '*' + '3750_CPC' + '.csv'
    Later_File_2 = str(CPC_Source_Folder) + str(later_date_2_str) + '*' + '3750_CPC' + '.csv'
    Month_files = str(CPC_Source_Folder) + str(date_file_label) + '*' + '3750_CPC' + '.csv'
    if int(start_year_month_str) == 201904:
        Month_files = str(CPC_Source_Folder) + '201903201016_3750_CPC' + '.csv'
    elif int(start_year_month_str) == 201905:
        Prior_File_1 = str(CPC_Source_Folder) + '201903201016_3750_CPC' + '.csv'
    elif int(start_year_month_str) == 201812:
        Month_files = str(CPC_Source_Folder) + '201812*' + '0000_3750_CPC.csv'
        Prior_File_1 = str(CPC_Source_Folder) + '201812*' + '2359_3750_CPC.csv'
        Prior_File_2 = str(CPC_Source_Folder) + '201812*' + '1217_3750_CPC.csv'
        Later_File_2 = str(CPC_Source_Folder) + '201812*' + '1508_3750_CPC.csv'
    #elif int(start_year_month_str) == 201903:
        #Prior_File_1 = str(CPC_Source_Folder) + '201903201016_3750_CPC' + '.csv'
    else:
        pass
    print(str(Month_files))
    print(str(Prior_File_1))
    CPC_csv_files = glob.glob(Month_files) + glob.glob(Prior_File_1) + glob.glob(Prior_File_2) + glob.glob(Later_File_1) + glob.glob(Later_File_2)
    CPCframes = []

    for csv in CPC_csv_files:
        df = pd.read_csv(csv, header=None, skiprows=3, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,18])
        CPCframes.append(df)

    CPC_Data = pd.concat(CPCframes, sort=True)

else:
    CPC_Source_Folder_1 = str(Data_Source_Folder) + str(CPC_folder_1) + '/'
    CPC_Source_Folder_2 = str(Data_Source_Folder) + str(CPC_folder_2) + '/'
    if Total_CPC_2_Serial_No == Total_CPC_1_Serial_No:
        print('Data collected for CPC ' + str(Total_CPC_1_Serial_No) + ' from multiple folders.')
        Prior_File_1 = str(CPC_Source_Folder_2) + str(prior_date_1_str) + '*' + '3750_CPC' + '.csv'
        Prior_File_2 = str(CPC_Source_Folder_2) + str(prior_date_2_str) + '*' + '3750_CPC' + '.csv'
        Later_File_1 = str(CPC_Source_Folder_1) + str(later_date_1_str) + '*' + '3750_CPC' + '.csv'
        Later_File_2 = str(CPC_Source_Folder_1) + str(later_date_2_str) + '*' + '3750_CPC' + '.csv'
        Month_files_1 = str(CPC_Source_Folder_2) + str(date_file_label) + '*' + '3750_CPC' + '.csv'
        Month_files_2 = str(CPC_Source_Folder_1) + str(date_file_label) + '*' + '3750_CPC' + '.csv'
        CPC_csv_files = glob.glob(Month_files_1) + glob.glob(Month_files_2) + glob.glob(Prior_File_1) + glob.glob(Prior_File_2) + glob.glob(Later_File_1) + glob.glob(Later_File_2)
        CPCframes = []
        
        for csv in CPC_csv_files:
            df = pd.read_csv(csv, header=None, skiprows=3, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,18])
            CPCframes.append(df)

        CPC_Data = pd.concat(CPCframes, sort=True)
        
    else:
        Prior_File_1a = str(CPC_Source_Folder_1) + str(prior_date_1_str) + '*' + '3750_CPC' + '.csv'
        Prior_File_1b = str(CPC_Source_Folder_1) + str(prior_date_2_str) + '*' + '3750_CPC' + '.csv'
        Later_File_1a = str(CPC_Source_Folder_1) + str(later_date_1_str) + '*' + '3750_CPC' + '.csv'
        Later_File_1b = str(CPC_Source_Folder_1) + str(later_date_2_str) + '*' + '3750_CPC' + '.csv'
        Month_files_1 = str(CPC_Source_Folder_1) + str(date_file_label) + '*' + '3750_CPC' + '.csv'
        CPC_csv_files = glob.glob(Month_files_1) + glob.glob(Prior_File_1a) + glob.glob(Prior_File_1b) + glob.glob(Later_File_1a) + glob.glob(Later_File_1b)
        CPCframes = []
        
        for csv in CPC_csv_files:
            df = pd.read_csv(csv, header=None, skiprows=3, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,18])
            CPCframes.append(df)

        CPC_Data = pd.concat(CPCframes, sort=True)
        
        Prior_File_2a = str(CPC_Source_Folder_2) + str(prior_date_1_str) + '*' + '3750_CPC' + '.csv'
        Prior_File_2b = str(CPC_Source_Folder_2) + str(prior_date_2_str) + '*' + '3750_CPC' + '.csv'
        Later_File_2a = str(CPC_Source_Folder_2) + str(later_date_1_str) + '*' + '3750_CPC' + '.csv'
        Later_File_2b = str(CPC_Source_Folder_2) + str(later_date_2_str) + '*' + '3750_CPC' + '.csv'
        Month_files_2 = str(CPC_Source_Folder_2) + str(date_file_label) + '*' + '3750_CPC' + '.csv'
        CPC_csv_files = glob.glob(Month_files_2) + glob.glob(Prior_File_2a) + glob.glob(Prior_File_2b) + glob.glob(Later_File_2a) + glob.glob(Later_File_2b)
        CPCframes = []
        
        for csv in CPC_csv_files:
            df = pd.read_csv(csv, header=None, skiprows=3, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,18])
            CPCframes.append(df)

        Intercomparison_CPC_Data = pd.concat(CPCframes, sort=True)
        print('Data collected for both CPCs ' + str(Total_CPC_1_Model) + ' and ' + str(Total_CPC_2_Model) + '.')

Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(folder) + '_' + str(version_number) + '/', 'D:/' + str(folder) + '_' + str(version_number) + '/')

if int(start_year_month_str) < 201906:
    pass
else:
    CPC_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/CPC_Total/'
    check_Folder = os.path.isdir(CPC_Folder)
    if not check_Folder:
        os.makedirs(CPC_Folder)
        print("created folder : ", CPC_Folder)
    else:
        print(CPC_Folder, "folder already exists.")

if Total_CPC_2_Model != 'N/A' and Total_CPC_1_Model != 'N/A' and Total_CPC_1_Model != Total_CPC_2_Model:
    Compare_CPC_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/CPC_Comparison/'
    check_Folder = os.path.isdir(Compare_CPC_Folder)
    if int(start_year_month_str) == 202112:
        pass
    else:
        if not check_Folder:
            os.makedirs(Compare_CPC_Folder)
            print("created folder : ", Compare_CPC_Folder)
        else:
            print(Compare_CPC_Folder, "folder already exists.")
elif int(start_year_month_str) < 201907:
    Simon_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/CPC_Simon_Building/'
    check_Folder = os.path.isdir(Simon_Folder)
    if not check_Folder:
        os.makedirs(Simon_Folder)
        print("created folder : ", Simon_Folder)
    else:
        print(Simon_Folder, "folder already exists.")
else:
    pass

CPC_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'Conc (#/cc)', 3: 'Saturator Temperture Alert', 4: 'Condensor Temperture Alert' }, inplace=True)
CPC_Data.rename(columns={5: 'Optics Temperature Alert', 6: 'Inlet Flow Alert', 7: 'Aerosol Flow Alert', 8: 'Laser Power Alert' }, inplace=True)
CPC_Data.rename(columns={9: 'Liquid Reservoir Alert', 10: 'Aerosol Concentration Flag', 11: 'Calibration Alert', 18: 'CPC Cal Mode' }, inplace=True)


CPC_Data['Date'] = CPC_Data['Date'].astype(str)
CPC_Data['Time'] = CPC_Data['Time'].astype(str)
CPC_Data['Date_length'] = CPC_Data['Date'].str.len()
CPC_Data['Time_length'] = CPC_Data['Time'].str.len()
CPC_Data=CPC_Data[CPC_Data.Date_length == 10]
CPC_Data=CPC_Data[CPC_Data.Time_length == 8]
CPC_Data['datetime'] = CPC_Data['Date'] + ' ' + CPC_Data['Time']# added Date and time into new columns
CPC_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in CPC_Data['datetime']] #converts the dateTime format from string to python dateTime
CPC_Data.index = CPC_Data['datetime']
CPC_Data = CPC_Data.sort_index()
CPC_Data = CPC_Data.drop(columns=['Time', 'Date', 'Date_length','Time_length'])
CPC_Data.drop(CPC_Data[(CPC_Data['Conc (#/cc)'].isnull())].index,inplace =True)
CPC_Data.drop(CPC_Data[(CPC_Data['Aerosol Flow Alert'].isnull())].index,inplace =True)

CPC_Data['Conc (#/cc)'] = CPC_Data['Conc (#/cc)'].astype(float)
CPC_Data.drop(CPC_Data[(CPC_Data['Conc (#/cc)'] == 0)].index,inplace =True)

CPC_Data['Saturator Temperture Alert'] = CPC_Data['Saturator Temperture Alert'].astype(str)
CPC_Data['Condensor Temperture Alert'] = CPC_Data['Condensor Temperture Alert'].astype(str)
CPC_Data['Optics Temperature Alert'] = CPC_Data['Optics Temperature Alert'].astype(str)
CPC_Data['Inlet Flow Alert'] = CPC_Data['Inlet Flow Alert'].astype(str)
CPC_Data['Aerosol Flow Alert'] = CPC_Data['Aerosol Flow Alert'].astype(str)
CPC_Data['Laser Power Alert'] = CPC_Data['Laser Power Alert'].astype(str)
CPC_Data['Liquid Reservoir Alert'] = CPC_Data['Liquid Reservoir Alert'].astype(str)
CPC_Data['Aerosol Concentration Flag'] = CPC_Data['Aerosol Concentration Flag'].astype(str)
CPC_Data['Calibration Alert'] = CPC_Data['Calibration Alert'].astype(str)
CPC_Data['CPC Cal Mode'] = CPC_Data['CPC Cal Mode'].astype(str)

CPC_Data.drop(CPC_Data[(CPC_Data['Saturator Temperture Alert'] == '>=')].index,inplace =True)
CPC_Data.drop(CPC_Data[(CPC_Data['Condensor Temperture Alert'] == '>=')].index,inplace =True)
CPC_Data.drop(CPC_Data[(CPC_Data['Optics Temperature Alert'] == '>=')].index,inplace =True)
CPC_Data.drop(CPC_Data[(CPC_Data['Inlet Flow Alert'] == '>=')].index,inplace =True)
CPC_Data.drop(CPC_Data[(CPC_Data['Aerosol Flow Alert'] == '>=')].index,inplace =True)
CPC_Data.drop(CPC_Data[(CPC_Data['Laser Power Alert'] == '>=')].index,inplace =True)
CPC_Data.drop(CPC_Data[(CPC_Data['Liquid Reservoir Alert'] == '>=')].index,inplace =True)
CPC_Data.drop(CPC_Data[(CPC_Data['Aerosol Concentration Flag'] == '>=')].index,inplace =True)
CPC_Data.drop(CPC_Data[(CPC_Data['Calibration Alert'] == '>=')].index,inplace =True)
CPC_Data.drop(CPC_Data[(CPC_Data['CPC Cal Mode'] == '>=')].index,inplace =True)

CPC_Data['Saturator Temperture Alert'] = CPC_Data['Saturator Temperture Alert'].astype(float)
CPC_Data['Condensor Temperture Alert'] = CPC_Data['Condensor Temperture Alert'].astype(float)
CPC_Data['Optics Temperature Alert'] = CPC_Data['Optics Temperature Alert'].astype(float)
CPC_Data['Inlet Flow Alert'] = CPC_Data['Inlet Flow Alert'].astype(float)
CPC_Data['Aerosol Flow Alert'] = CPC_Data['Aerosol Flow Alert'].astype(float)
CPC_Data['Laser Power Alert'] = CPC_Data['Laser Power Alert'].astype(float)
CPC_Data['Liquid Reservoir Alert'] = CPC_Data['Liquid Reservoir Alert'].astype(float)
CPC_Data['Aerosol Concentration Flag'] = CPC_Data['Aerosol Concentration Flag'].astype(float)
CPC_Data['Calibration Alert'] = CPC_Data['Calibration Alert'].astype(float)
CPC_Data['CPC Cal Mode'] = CPC_Data['CPC Cal Mode'].astype(float)

CPC_Data['datetime'] = CPC_Data.index
#CPC_Data.index = CPC_Data['datetime'] 

#if int(start_year_month_str) > 202004 and int(start_year_month_str) < 202102:
#    CPC_Data['Aerosol Flow Alert'] = 0
#elif int(start_year_month_str) == 202004:
#    start_False_Aerosol_1 = datetime.datetime(2020,4,13,9,55,00)
#    CPC_Data['Aerosol Flow Alert'] = np.where((CPC_Data['datetime']> start_False_Aerosol_1), 0, CPC_Data['Aerosol Flow Alert'])
#elif int(start_year_month_str) == 202102:
#    end_False_Aerosol_1 = datetime.datetime(2021,2,12,23,59,59)
#    CPC_Data['Aerosol Flow Alert'] = np.where((CPC_Data['datetime']< end_False_Aerosol_1), 0, CPC_Data['Aerosol Flow Alert'])
#else:
#    pass

start_False_Aerosol_1 = datetime.datetime(2020,4,13,9,55,00)
end_False_Aerosol_1 = datetime.datetime(2021,2,12,23,59,59)

CPC_Data['Aerosol Flow Alert'] = np.where(((CPC_Data['datetime']> start_False_Aerosol_1) & (CPC_Data['datetime']< end_False_Aerosol_1) ), 0, CPC_Data['Aerosol Flow Alert'])

#CPC_Data.loc[start_False_Aerosol_1:end_False_Aerosol_1, ('Aerosol Flow Alert')] = 0

CPC_Data['qc_flags'] = np.where((CPC_Data['Saturator Temperture Alert'] != 0), 2, 1)
CPC_Data['qc_flags'] = np.where((CPC_Data['Condensor Temperture Alert'] != 0), 2, CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['Optics Temperature Alert'] != 0), 2, CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['Inlet Flow Alert'] != 0), 2, CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['Aerosol Flow Alert'] != 0), 2, CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['Laser Power Alert'] != 0), 2, CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['Liquid Reservoir Alert'] != 0), 2, CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['Aerosol Concentration Flag'] != 0), 2, CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['Calibration Alert'] != 0), 2, CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['CPC Cal Mode'] != 0), 2, CPC_Data['qc_flags'])

CPC_Data = CPC_Data.drop(columns=['Saturator Temperture Alert', 'Condensor Temperture Alert', 'Optics Temperature Alert'])
CPC_Data = CPC_Data.drop(columns=['Inlet Flow Alert','Aerosol Flow Alert','Laser Power Alert','Liquid Reservoir Alert'])
CPC_Data = CPC_Data.drop(columns=['Aerosol Concentration Flag', 'Calibration Alert', 'CPC Cal Mode'])

max_CPC_flag = CPC_Data['qc_flags'].groupby(pd.Grouper(freq=av_Freq)).max()
CPC_Data = CPC_Data.groupby(pd.Grouper(key='datetime',freq=av_Freq)).mean()
CPC_Data['qc_flags'] = pd.Series(max_CPC_flag)

CPC_3010_Detection_limit = 10000
CPC_3772_Detection_limit = 50000
CPC_3750_Detection_limit = 100000

CPC_Data['datetime'] = CPC_Data.index

if int(start_year_month_str) == 202110 or int(start_year_month_str) == 202111 or int(start_year_month_str) == 202112 or int(start_year_month_str) == 202212:
    if int(start_year_month_str) == 202110:
        CPC_Data['detection_limit'] = np.where(CPC_Data['datetime'] < switch_over, CPC_3772_Detection_limit, CPC_3750_Detection_limit)
        CPC_Data['qc_flags'] = np.where((CPC_Data['Conc (#/cc)'] > CPC_Data['detection_limit']), 3, CPC_Data['qc_flags'])
        CPC_Data = CPC_Data.drop(columns=['detection_limit'])
    elif int(start_year_month_str) == 202111:
        CPC_Data['detection_limit'] = np.where(CPC_Data['datetime'] > Start_SMPS_Interrupt, CPC_3772_Detection_limit, CPC_3750_Detection_limit) #int(start_year_month_str) == 202112
        CPC_Data['qc_flags'] = np.where((CPC_Data['Conc (#/cc)'] > CPC_Data['detection_limit']), 3, CPC_Data['qc_flags'])
        CPC_Data = CPC_Data.drop(columns=['detection_limit'])
    elif int(start_year_month_str) == 202212:
        CPC_Data['detection_limit'] = np.where(CPC_Data['datetime'] > CPC_1_Remove, CPC_3772_Detection_limit, CPC_3750_Detection_limit) #int(start_year_month_str) == 202112
        CPC_Data['qc_flags'] = np.where((CPC_Data['Conc (#/cc)'] > CPC_Data['detection_limit']), 3, CPC_Data['qc_flags'])
        CPC_Data = CPC_Data.drop(columns=['detection_limit'])
    else:
        CPC_Data['detection_limit'] = np.where(CPC_Data['datetime'] > End_SMPS_Interrupt, CPC_3750_Detection_limit, CPC_3772_Detection_limit) #int(start_year_month_str) == 202112
        CPC_Data['qc_flags'] = np.where((CPC_Data['Conc (#/cc)'] > CPC_Data['detection_limit']), 3, CPC_Data['qc_flags'])
        CPC_Data = CPC_Data.drop(columns=['detection_limit'])
else:
    if str(Total_CPC_1_Model) == '3010':
        print('Detection Limit of ' + str(Total_CPC_1_Model) + ' Instrument is: ' + str(CPC_3010_Detection_limit) )
        CPC_Data['qc_flags'] = np.where((CPC_Data['Conc (#/cc)'] > CPC_3010_Detection_limit), 3, CPC_Data['qc_flags'])
    elif str(Total_CPC_1_Model) == '3772':
        print('Detection Limit of ' + str(Total_CPC_1_Model) + ' Instrument is: ' + str(CPC_3772_Detection_limit) )
        CPC_Data['qc_flags'] = np.where((CPC_Data['Conc (#/cc)'] > CPC_3772_Detection_limit), 3, CPC_Data['qc_flags'])
    else:
        print('Detection Limit of ' + str(Total_CPC_1_Model) + ' Instrument is: ' + str(CPC_3750_Detection_limit) )
        CPC_Data['qc_flags'] = np.where((CPC_Data['Conc (#/cc)'] > CPC_3750_Detection_limit), 3, CPC_Data['qc_flags'])

CPC_Data['qc_flags'] = np.where(CPC_Data['Conc (#/cc)']<0, 3, CPC_Data['qc_flags'])

CPC_Data['qc_flags_-6_offset'] = CPC_Data['qc_flags'].shift(periods=-6) 
CPC_Data['qc_flags_-5_offset'] = CPC_Data['qc_flags'].shift(periods=-5) 
CPC_Data['qc_flags_-4_offset'] = CPC_Data['qc_flags'].shift(periods=-4) 
CPC_Data['qc_flags_-3_offset'] = CPC_Data['qc_flags'].shift(periods=-3) 
CPC_Data['qc_flags_-2_offset'] = CPC_Data['qc_flags'].shift(periods=-2) 
CPC_Data['qc_flags_-1_offset'] = CPC_Data['qc_flags'].shift(periods=-1) 
CPC_Data['qc_flags_+1_offset'] = CPC_Data['qc_flags'].shift(periods=1) 
CPC_Data['qc_flags_+2_offset'] = CPC_Data['qc_flags'].shift(periods=2)
CPC_Data['qc_flags_+3_offset'] = CPC_Data['qc_flags'].shift(periods=3) 
CPC_Data['qc_flags_+4_offset'] = CPC_Data['qc_flags'].shift(periods=4)
CPC_Data['qc_flags_+5_offset'] = CPC_Data['qc_flags'].shift(periods=5) 
CPC_Data['qc_flags_+6_offset'] = CPC_Data['qc_flags'].shift(periods=6) 
CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags_-6_offset']==3),CPC_Data['qc_flags_-6_offset'],CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags_-5_offset']==3),CPC_Data['qc_flags_-5_offset'],CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags_-4_offset']==3),CPC_Data['qc_flags_-4_offset'],CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags_-3_offset']==3),CPC_Data['qc_flags_-3_offset'],CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags_-2_offset']==3),CPC_Data['qc_flags_-2_offset'],CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags_-1_offset']==3),CPC_Data['qc_flags_-1_offset'],CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags_+1_offset']==3),CPC_Data['qc_flags_+1_offset'],CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags_+2_offset']==3),CPC_Data['qc_flags_+2_offset'],CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags_+3_offset']==3),CPC_Data['qc_flags_+3_offset'],CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags_+4_offset']==3),CPC_Data['qc_flags_+4_offset'],CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags_+5_offset']==3),CPC_Data['qc_flags_+5_offset'],CPC_Data['qc_flags'])
CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags_+6_offset']==3),CPC_Data['qc_flags_+6_offset'],CPC_Data['qc_flags'])
CPC_Flag_Offset = list(CPC_Data.columns.values)
CPC_Flag_Offset.remove('Conc (#/cc)')
CPC_Flag_Offset.remove('qc_flags')
CPC_Data = CPC_Data.drop(columns=CPC_Flag_Offset)

start_Low_Count_2 = datetime.datetime(2022,9,1,9,3,00) # low count seen from early july
end_Low_Count_2 = datetime.datetime(2022,12,5,18,0,00)
CPC_Data.loc[start_Low_Count_2:end_Low_Count_2, ('qc_flags')] = 3
    

CPC_Data['qc_flags'] = np.where((CPC_Data['qc_flags'] == 3), 2, CPC_Data['qc_flags'])
#print(CPC_Data['qc_flags'])
if Total_CPC_2_Model == 'N/A' or Total_CPC_1_Model == 'N/A' or Total_CPC_1_Model == Total_CPC_2_Model or int(start_year_month_str) == 202112 :
    pass
else:
    Intercomparison_CPC_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'Conc (#/cc)', 3: 'Saturator Temperture Alert', 4: 'Condensor Temperture Alert' }, inplace=True)
    Intercomparison_CPC_Data.rename(columns={5: 'Optics Temperature Alert', 6: 'Inlet Flow Alert', 7: 'Aerosol Flow Alert', 8: 'Laser Power Alert' }, inplace=True)
    Intercomparison_CPC_Data.rename(columns={9: 'Liquid Reservoir Alert', 10: 'Aerosol Concentration Flag', 11: 'Calibration Alert', 18: 'CPC Cal Mode' }, inplace=True)
    Intercomparison_CPC_Data['Date'] = Intercomparison_CPC_Data['Date'].astype(str)
    Intercomparison_CPC_Data['Time'] = Intercomparison_CPC_Data['Time'].astype(str)
    Intercomparison_CPC_Data['Date_length'] = Intercomparison_CPC_Data['Date'].str.len()
    Intercomparison_CPC_Data['Time_length'] = Intercomparison_CPC_Data['Time'].str.len()
    Intercomparison_CPC_Data=Intercomparison_CPC_Data[Intercomparison_CPC_Data.Date_length == 10]
    Intercomparison_CPC_Data=Intercomparison_CPC_Data[Intercomparison_CPC_Data.Time_length == 8]
    Intercomparison_CPC_Data['datetime'] = Intercomparison_CPC_Data['Date'] + ' ' + Intercomparison_CPC_Data['Time'] # added Date and time into new columns
    Intercomparison_CPC_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in Intercomparison_CPC_Data['datetime']] #converts the dateTime format from string to python dateTime
    Intercomparison_CPC_Data.index = Intercomparison_CPC_Data['datetime']
    Intercomparison_CPC_Data = Intercomparison_CPC_Data.sort_index()
    Intercomparison_CPC_Data = Intercomparison_CPC_Data.drop(columns=['Time', 'Date', 'Date_length','Time_length'])
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Conc (#/cc)'].isnull())].index,inplace =True)
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Aerosol Flow Alert'].isnull())].index,inplace =True)
    
    Intercomparison_CPC_Data['Conc (#/cc)'] = Intercomparison_CPC_Data['Conc (#/cc)'].astype(float)
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Conc (#/cc)'] == 0)].index,inplace =True)
    
    Intercomparison_CPC_Data['Saturator Temperture Alert'] = Intercomparison_CPC_Data['Saturator Temperture Alert'].astype(str)
    Intercomparison_CPC_Data['Condensor Temperture Alert'] = Intercomparison_CPC_Data['Condensor Temperture Alert'].astype(str)
    Intercomparison_CPC_Data['Optics Temperature Alert'] = Intercomparison_CPC_Data['Optics Temperature Alert'].astype(str)
    Intercomparison_CPC_Data['Inlet Flow Alert'] = Intercomparison_CPC_Data['Inlet Flow Alert'].astype(str)
    Intercomparison_CPC_Data['Aerosol Flow Alert'] = Intercomparison_CPC_Data['Aerosol Flow Alert'].astype(str)
    Intercomparison_CPC_Data['Laser Power Alert'] = Intercomparison_CPC_Data['Laser Power Alert'].astype(str)
    Intercomparison_CPC_Data['Liquid Reservoir Alert'] = Intercomparison_CPC_Data['Liquid Reservoir Alert'].astype(str)
    Intercomparison_CPC_Data['Aerosol Concentration Flag'] = Intercomparison_CPC_Data['Aerosol Concentration Flag'].astype(str)
    Intercomparison_CPC_Data['Calibration Alert'] = Intercomparison_CPC_Data['Calibration Alert'].astype(str)
    Intercomparison_CPC_Data['CPC Cal Mode'] = Intercomparison_CPC_Data['CPC Cal Mode'].astype(str)

    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Saturator Temperture Alert'] == '>=')].index,inplace =True)
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Condensor Temperture Alert'] == '>=')].index,inplace =True)
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Optics Temperature Alert'] == '>=')].index,inplace =True)
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Inlet Flow Alert'] == '>=')].index,inplace =True)
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Aerosol Flow Alert'] == '>=')].index,inplace =True)
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Laser Power Alert'] == '>=')].index,inplace =True)
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Liquid Reservoir Alert'] == '>=')].index,inplace =True)
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Aerosol Concentration Flag'] == '>=')].index,inplace =True)
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Calibration Alert'] == '>=')].index,inplace =True)
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['CPC Cal Mode'] == '>=')].index,inplace =True)

    Intercomparison_CPC_Data['Saturator Temperture Alert'] = Intercomparison_CPC_Data['Saturator Temperture Alert'].astype(float)
    Intercomparison_CPC_Data['Condensor Temperture Alert'] = Intercomparison_CPC_Data['Condensor Temperture Alert'].astype(float)
    Intercomparison_CPC_Data['Optics Temperature Alert'] = Intercomparison_CPC_Data['Optics Temperature Alert'].astype(float)
    Intercomparison_CPC_Data['Inlet Flow Alert'] = Intercomparison_CPC_Data['Inlet Flow Alert'].astype(float)
    Intercomparison_CPC_Data['Aerosol Flow Alert'] = Intercomparison_CPC_Data['Aerosol Flow Alert'].astype(float)
    Intercomparison_CPC_Data['Laser Power Alert'] = Intercomparison_CPC_Data['Laser Power Alert'].astype(float)
    Intercomparison_CPC_Data['Liquid Reservoir Alert'] = Intercomparison_CPC_Data['Liquid Reservoir Alert'].astype(float)
    Intercomparison_CPC_Data['Aerosol Concentration Flag'] = Intercomparison_CPC_Data['Aerosol Concentration Flag'].astype(float)
    Intercomparison_CPC_Data['Calibration Alert'] = Intercomparison_CPC_Data['Calibration Alert'].astype(float)
    Intercomparison_CPC_Data['CPC Cal Mode'] = Intercomparison_CPC_Data['CPC Cal Mode'].astype(float)

    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Saturator Temperture Alert'] != 0), 2, 1)
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Condensor Temperture Alert'] != 0), 2, Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Optics Temperature Alert'] != 0), 2, Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Inlet Flow Alert'] != 0), 2, Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Aerosol Flow Alert'] != 0), 2, Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Laser Power Alert'] != 0), 2, Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Liquid Reservoir Alert'] != 0), 2, Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Aerosol Concentration Flag'] != 0), 2, Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Calibration Alert'] != 0), 2, Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['CPC Cal Mode'] != 0), 2, Intercomparison_CPC_Data['qc_flags'])

    Intercomparison_CPC_Data = Intercomparison_CPC_Data.drop(columns=['Saturator Temperture Alert', 'Condensor Temperture Alert', 'Optics Temperature Alert'])
    Intercomparison_CPC_Data = Intercomparison_CPC_Data.drop(columns=['Inlet Flow Alert','Aerosol Flow Alert','Laser Power Alert','Liquid Reservoir Alert'])
    Intercomparison_CPC_Data = Intercomparison_CPC_Data.drop(columns=['Aerosol Concentration Flag', 'Calibration Alert', 'CPC Cal Mode'])
    
    max_CPC_2_flag = Intercomparison_CPC_Data['qc_flags'].groupby(pd.Grouper(freq=av_Freq)).max()
    Intercomparison_CPC_Data = Intercomparison_CPC_Data.groupby(pd.Grouper(key='datetime',freq=av_Freq)).mean()
    Intercomparison_CPC_Data['qc_flags'] = pd.Series(max_CPC_2_flag)
    
    Intercomparison_CPC_Data['qc_flags'] = np.where(Intercomparison_CPC_Data['Conc (#/cc)']<0, 3, Intercomparison_CPC_Data['qc_flags'])
    
    Intercomparison_CPC_Data['datetime'] = Intercomparison_CPC_Data.index
    
    if int(start_year_month_str) == 202110:
        Intercomparison_CPC_Data['detection_limit'] = np.where(Intercomparison_CPC_Data['datetime'] > switch_over, CPC_3772_Detection_limit, CPC_3750_Detection_limit)
        Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Conc (#/cc)'] > Intercomparison_CPC_Data['detection_limit']), 3, Intercomparison_CPC_Data['qc_flags'])
        Intercomparison_CPC_Data = Intercomparison_CPC_Data.drop(columns=['detection_limit'])
    else:
        if str(Total_CPC_2_Model) == '3010':
            print('Detection Limit of ' + str(Total_CPC_2_Model) + ' Instrument is: ' + str(CPC_3010_Detection_limit) )
            Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Conc (#/cc)'] > CPC_3010_Detection_limit), 3, Intercomparison_CPC_Data['qc_flags'])
        elif str(Total_CPC_2_Model) == '3772':
            print('Detection Limit of ' + str(Total_CPC_2_Model) + ' Instrument is: ' + str(CPC_3772_Detection_limit) )
            Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Conc (#/cc)'] > CPC_3772_Detection_limit), 3, Intercomparison_CPC_Data['qc_flags'])
        else:
            print('Detection Limit of ' + str(Total_CPC_2_Model) + ' Instrument is: ' + str(CPC_3750_Detection_limit) )
            Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['Conc (#/cc)'] > CPC_3750_Detection_limit), 3, Intercomparison_CPC_Data['qc_flags'])
    
    
    Intercomparison_CPC_Data['qc_flags_-6_offset'] = Intercomparison_CPC_Data['qc_flags'].shift(periods=-6) 
    Intercomparison_CPC_Data['qc_flags_-5_offset'] = Intercomparison_CPC_Data['qc_flags'].shift(periods=-5) 
    Intercomparison_CPC_Data['qc_flags_-4_offset'] = Intercomparison_CPC_Data['qc_flags'].shift(periods=-4) 
    Intercomparison_CPC_Data['qc_flags_-3_offset'] = Intercomparison_CPC_Data['qc_flags'].shift(periods=-3) 
    Intercomparison_CPC_Data['qc_flags_-2_offset'] = Intercomparison_CPC_Data['qc_flags'].shift(periods=-2) 
    Intercomparison_CPC_Data['qc_flags_-1_offset'] = Intercomparison_CPC_Data['qc_flags'].shift(periods=-1) 
    Intercomparison_CPC_Data['qc_flags_+1_offset'] = Intercomparison_CPC_Data['qc_flags'].shift(periods=1) 
    Intercomparison_CPC_Data['qc_flags_+2_offset'] = Intercomparison_CPC_Data['qc_flags'].shift(periods=2)
    Intercomparison_CPC_Data['qc_flags_+3_offset'] = Intercomparison_CPC_Data['qc_flags'].shift(periods=3) 
    Intercomparison_CPC_Data['qc_flags_+4_offset'] = Intercomparison_CPC_Data['qc_flags'].shift(periods=4)
    Intercomparison_CPC_Data['qc_flags_+5_offset'] = Intercomparison_CPC_Data['qc_flags'].shift(periods=5) 
    Intercomparison_CPC_Data['qc_flags_+6_offset'] = Intercomparison_CPC_Data['qc_flags'].shift(periods=6) 
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags_-6_offset']==3),Intercomparison_CPC_Data['qc_flags_-6_offset'],Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags_-5_offset']==3),Intercomparison_CPC_Data['qc_flags_-5_offset'],Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags_-4_offset']==3),Intercomparison_CPC_Data['qc_flags_-4_offset'],Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags_-3_offset']==3),Intercomparison_CPC_Data['qc_flags_-3_offset'],Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags_-2_offset']==3),Intercomparison_CPC_Data['qc_flags_-2_offset'],Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags_-1_offset']==3),Intercomparison_CPC_Data['qc_flags_-1_offset'],Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags_+1_offset']==3),Intercomparison_CPC_Data['qc_flags_+1_offset'],Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags_+2_offset']==3),Intercomparison_CPC_Data['qc_flags_+2_offset'],Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags_+3_offset']==3),Intercomparison_CPC_Data['qc_flags_+3_offset'],Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags_+4_offset']==3),Intercomparison_CPC_Data['qc_flags_+4_offset'],Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags_+5_offset']==3),Intercomparison_CPC_Data['qc_flags_+5_offset'],Intercomparison_CPC_Data['qc_flags'])
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags_+6_offset']==3),Intercomparison_CPC_Data['qc_flags_+6_offset'],Intercomparison_CPC_Data['qc_flags'])
    CPC_Flag_Offset = list(Intercomparison_CPC_Data.columns.values)
    CPC_Flag_Offset.remove('Conc (#/cc)')
    CPC_Flag_Offset.remove('qc_flags')
    Intercomparison_CPC_Data = Intercomparison_CPC_Data.drop(columns=CPC_Flag_Offset)
#CPC_Data.drop(CPC_Data.loc[start_Low_Count_2:end_Low_Count_2].index, inplace=True)
    Intercomparison_CPC_Data['qc_flags'] = np.where((Intercomparison_CPC_Data['qc_flags'] == 3), 2, Intercomparison_CPC_Data['qc_flags'])
    

start_Accidental_Cal_1 = datetime.datetime(2021,9,16,13,0,00) 
end_Accidental_Cal_1 = datetime.datetime(2021,9,16,15,0,00)
CPC_Data.loc[start_Accidental_Cal_1:end_Accidental_Cal_1, ('qc_flags')] = 1

start_Accidental_Cal_2 = datetime.datetime(2021,9,16,15,0,00) 
end_Accidental_Cal_2= datetime.datetime(2021,9,17,16,0,00)
CPC_Data.loc[start_Accidental_Cal_2:end_Accidental_Cal_2, ('qc_flags')] = 1

start_Low_Count_1 = datetime.datetime(2021,1,12,0,0,00) #not sure when low counting started so backed to the end of the year
end_Low_Count_1 = datetime.datetime(2021,2,12,23,59,59)
CPC_Data.loc[start_Low_Count_1:Intercomparison_start, ('qc_flags')] = 2

start_Tarmac = datetime.datetime(2020,5,4,7,30,00)
end_Tarmac = datetime.datetime(2020,5,15,16,0,00)
CPC_Data.loc[start_Tarmac:end_Tarmac, ('qc_flags')] = 2

start_False_Zero_1 = datetime.datetime(2019,1,15,6,44,00)
end_False_Zero_1 = datetime.datetime(2019,1,16,14,50,00)
CPC_Data.loc[start_False_Zero_1:end_False_Zero_1, ('qc_flags')] = 2
#CPC_Data.drop(CPC_Data.loc[start_False_Zero_1:end_False_Zero_1].index, inplace=True)

start_False_Zero_2 = datetime.datetime(2019,2,5,7,5,00)
end_False_Zero_2 = datetime.datetime(2019,2,5,22,25,00)
CPC_Data.loc[start_False_Zero_2:end_False_Zero_2, ('qc_flags')] = 2
#CPC_Data.drop(CPC_Data.loc[start_False_Zero_2:end_False_Zero_2].index, inplace=True)

start_False_Zero_3 = datetime.datetime(2019,3,10,11,19,00)
end_False_Zero_3 = datetime.datetime(2019,3,11,14,34,00)
CPC_Data.loc[start_False_Zero_3:end_False_Zero_3, ('qc_flags')] = 2
#CPC_Data.drop(CPC_Data.loc[start_False_Zero_3:end_False_Zero_3].index, inplace=True)

start_False_Zero_4 = datetime.datetime(2021,9,27,10,50,00)
end_False_Zero_4 = datetime.datetime(2021,10,1,8,5,00)
#CPC_Data.drop(CPC_Data.loc[start_False_Zero_4:end_False_Zero_4].index, inplace=True)

start_False_Zero_5 = datetime.datetime(2019,3,10,11,19,00)
end_False_Zero_5 = datetime.datetime(2019,3,11,14,34,00)
CPC_Data.loc[start_False_Zero_5:end_False_Zero_5, ('qc_flags')] = 2
#CPC_Data.drop(CPC_Data.loc[start_False_Zero_3:end_False_Zero_3].index, inplace=True)

start_Pulse_1 = datetime.datetime(2019,9,27,12,0,00) #pulse height too high
end_Pulse_1 = datetime.datetime(2019,9,27,13,0,00)
CPC_Data.loc[start_Pulse_1:end_Pulse_1, ('qc_flags')] = 2
#CPC_Data.drop(CPC_Data.loc[start_False_Zero_4:end_False_Zero_4].index, inplace=True)

start_Flow_Error_1 = datetime.datetime(2020,4,15,12,15,00) #
end_Flow_Error_1 = datetime.datetime(2020,4,15,13,40,00)
CPC_Data.loc[start_Flow_Error_1:end_Flow_Error_1, ('qc_flags')] = 2
#CPC_Data.drop(CPC_Data.loc[start_False_Zero_4:end_False_Zero_4].index, inplace=True)

start_Flow_Error_2 = datetime.datetime(2022,3,7,7,15,00) #
end_Flow_Error_2 = datetime.datetime(2022,3,7,10,0,00)
CPC_Data.loc[start_Flow_Error_2:end_Flow_Error_2, ('qc_flags')] = 2
#CPC_Data.drop(CPC_Data.loc[start_Flow_Error_2:end_Flow_Error_2].index, inplace=True)

start_Low_Count_1 = datetime.datetime(2022,7,9,0,0,00) # low count seen from early july
end_Low_Count_1 = datetime.datetime(2022,9,1,9,3,00)
CPC_Data.loc[start_Low_Count_1:end_Low_Count_1, ('qc_flags')] = 2
#CPC_Data.drop(CPC_Data.loc[start_Flow_Error_2:end_Flow_Error_2].index, inplace=True)

start_Clean4 = datetime.datetime(2022,12,12,4,0,00) #cleaning denuder
end_Clean4 = datetime.datetime(2022,12,12,16,0,00)
#CPC_Data.loc[start_Clean4:end_Clean4, ('qc_Flags')] = 2
CPC_Data.drop(CPC_Data.loc[start_Clean4:end_Clean4].index, inplace=True)

CPC_Data.drop(CPC_Data[(CPC_Data['Conc (#/cc)'].isnull() )].index,inplace =True)
CPC_Data.drop(CPC_Data[(CPC_Data['qc_flags'].isnull() )].index,inplace =True)
CPC_Data['qc_flags'] = CPC_Data['qc_flags'].astype(float)
CPC_Data['qc_flags'] = CPC_Data['qc_flags'].astype(int)
CPC_Data['qc_flags'] = CPC_Data['qc_flags'].astype(str)

print(str(start))
print(str(end))
CPC_Data = CPC_Data[start:end]

if Total_CPC_2_Model == 'N/A' or Total_CPC_1_Model == 'N/A' or Total_CPC_1_Model == Total_CPC_2_Model or int(start_year_month_str) == 202112:
    pass
else:
    Intercomparison_CPC_Data.loc[start_Accidental_Cal_1:end_Accidental_Cal_1, ('qc_flags')] = 1
    Intercomparison_CPC_Data.loc[start_Accidental_Cal_2:end_Accidental_Cal_2, ('qc_flags')] = 1
    Intercomparison_CPC_Data.loc[start_False_Zero_4:end_False_Zero_4, ('qc_flags')] = 2
    Intercomparison_CPC_Data.loc[Intercomparison_start:end_Low_Count_1, ('qc_flags')] = 2
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['Conc (#/cc)'].isnull() )].index,inplace =True)
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data[(Intercomparison_CPC_Data['qc_flags'].isnull() )].index,inplace =True)
    Intercomparison_CPC_Data['qc_flags'] = Intercomparison_CPC_Data['qc_flags'].astype(float)
    Intercomparison_CPC_Data['qc_flags'] = Intercomparison_CPC_Data['qc_flags'].astype(int)
    Intercomparison_CPC_Data['qc_flags'] = Intercomparison_CPC_Data['qc_flags'].astype(str)
    Intercomparison_CPC_Data = Intercomparison_CPC_Data[start:end]

if int(start_year_month_str) == 201906:
    Install_Date = datetime.datetime(2019,6,20,14,00,00)
    Simon_CPC_Data = CPC_Data[start:Install_Date]
    Simon_CPC_Data = Simon_CPC_Data.sort_index()
    Firs_CPC_Data = CPC_Data[Install_Date:end]
    Firs_CPC_Data = Firs_CPC_Data.sort_index()
elif int(start_year_month_str) == 202102:
    Total_CPC_2_Data = Intercomparison_CPC_Data
    Total_CPC_2_Data = Total_CPC_2_Data.sort_index()
    Intercomparison_CPC_Data = CPC_Data[Intercomparison_start:end]
    Intercomparison_CPC_Data = Intercomparison_CPC_Data.sort_index()
    CPC_Data.drop(CPC_Data.loc[Intercomparison_start:end].index, inplace=True)  
    CPC_Data = CPC_Data.sort_index()
elif int(start_year_month_str) == 202110:
    Total_CPC_2_Data = CPC_Data[switch_over:end]
    Total_CPC_2_Data = Total_CPC_2_Data.sort_index()
    Intercomparison_CPC_2 = Intercomparison_CPC_Data[switch_over:end]
    Intercomparison_CPC_2 = Intercomparison_CPC_2.sort_index()
    CPC_Data.drop(CPC_Data.loc[switch_over:end].index, inplace=True) 
    CPC_Data = CPC_Data.sort_index()
    Intercomparison_CPC_Data.drop(Intercomparison_CPC_Data.loc[switch_over:end].index, inplace=True)  
    Intercomparison_CPC_Data = Intercomparison_CPC_Data.sort_index()
elif int(start_year_month_str) == 202111:
    Total_CPC_2_Data = CPC_Data[Start_SMPS_Interrupt:end] 
    Total_CPC_2_Data = Total_CPC_2_Data.sort_index()
    CPC_Data = CPC_Data[start:Start_SMPS_Interrupt] 
    CPC_Data = CPC_Data.sort_index()
elif int(start_year_month_str) == 202112:
    Total_CPC_2_Data = CPC_Data[End_SMPS_Interrupt:end] 
    Total_CPC_2_Data = Total_CPC_2_Data.sort_index()
    CPC_Data = CPC_Data[start:End_SMPS_Interrupt] 
    CPC_Data = CPC_Data.sort_index()
elif int(start_year_month_str) == 202209: #CPC_Data is data for first few hours of 1st september, Total_CPC_2_Data is low counting CPC
    Total_CPC_2_Data = Intercomparison_CPC_Data[CPC_2_Add:end]
    Intercomparison_CPC_Data = CPC_Data[CPC_2_Add:end]  
    CPC_Data = CPC_Data[start:CPC_2_Add]
    CPC_Data = CPC_Data.sort_index()
    Total_CPC_2_Data = Total_CPC_2_Data.sort_index()
    Intercomparison_CPC_Data = Intercomparison_CPC_Data.sort_index()
elif int(start_year_month_str) == 202212:
    Total_Other_CPC_Data = CPC_Data[start:CPC_1_Remove] 
    Total_Other_CPC_Data = Total_Other_CPC_Data.sort_index()
    CPC_Data = CPC_Data[CPC_1_Remove:end] 
    CPC_Data = pd.concat([Intercomparison_CPC_Data, CPC_Data])
    CPC_Data = CPC_Data.sort_index()
else:
    pass


if int(start_year_month_str) < 201906:
    plt.plot(CPC_Data['Conc (#/cc)'], label=('Particle Number at Firs Site from: CPC ' + str(Total_CPC_1_Model)))
    plt.legend()
    plt.ylabel('#/cc')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}
    
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    plt.figure()
    plt.show()
    CPC_Data.to_csv(str(Simon_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + str(location_input)  + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')

    

elif int(start_year_month_str) == 201906:
    plt.plot(Simon_CPC_Data['Conc (#/cc)'], label=('Particle Number in Simon Building from: CPC ' + str(Total_CPC_1_Model)) )
    plt.plot(Firs_CPC_Data['Conc (#/cc)'], label=('Particle Number at Firs Site from: CPC ' + str(Total_CPC_1_Model)))
    plt.legend()
    plt.ylabel('#/cc')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}
    
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    plt.figure()
    plt.show()
    
    Simon_CPC_Data.to_csv(str(Simon_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + str(location_input)  + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    Firs_CPC_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    CPC_Data = Firs_CPC_Data
elif int(start_year_month_str) == 202102:
    plt.plot(CPC_Data['Conc (#/cc)'], label='Particle Number from CPC: ' + str(Total_CPC_1_Model) + '_#1')
    plt.plot(Intercomparison_CPC_Data['Conc (#/cc)'], label='Intercomparison Particle Number from CPC: ' + str(Total_CPC_1_Model) + '_#1')
    plt.plot(Total_CPC_2_Data['Conc (#/cc)'], label='Particle Number from CPC: ' + str(Total_CPC_2_Model) )
    plt.legend()
    plt.ylabel('#/cc')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}
    
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    #plt.figure()
    plt.show()
    CPC_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + '01-to-' + str(date_file_label) + '10' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    Total_CPC_2_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_2_Model) + '_maqs_' + str(date_file_label) + '10-to-' + str(date_file_label) + '28' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    Intercomparison_CPC_Data.to_csv(str(Compare_CPC_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + '10-to-' + str(date_file_label) + '12' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
elif int(start_year_month_str) == 202109:
    # date of intercomparison 16/09/2021 - 27/10/2021 
    plt.plot(CPC_Data['Conc (#/cc)'], label='Particle Number count in upper position for CPC: ' + str(Total_CPC_1_Model))
    plt.plot(Intercomparison_CPC_Data['Conc (#/cc)'], label='Particle Number count in lower position for CPC: ' + str(Total_CPC_2_Model))
    plt.legend()
    plt.ylabel('#/cc')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}
    
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    #plt.figure()
    plt.show()
    CPC_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    Intercomparison_CPC_Data.to_csv(str(Compare_CPC_Folder) + 'CPC-' + str(Total_CPC_2_Model) + '_maqs_' + str(date_file_label) + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
elif int(start_year_month_str) == 202110:
    plt.plot(CPC_Data['Conc (#/cc)'], label='Particle Number count in upper position for CPC: ' + str(Total_CPC_1_Model))
    plt.plot(Intercomparison_CPC_Data['Conc (#/cc)'], label='Particle Number count in lower position for CPC: ' + str(Total_CPC_2_Model))
    plt.plot(Total_CPC_2_Data['Conc (#/cc)'], label='Particle Number count in upper position for CPC: ' + str(Total_CPC_2_Model))
    plt.plot(Intercomparison_CPC_2['Conc (#/cc)'], label='Particle Number count in lower position for CPC: ' + str(Total_CPC_1_Model))
    plt.legend()
    plt.ylabel('#/cc')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}
    
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    #plt.figure()
    plt.show()
    CPC_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + '01-to-' + str(date_file_label) + '27' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    Intercomparison_CPC_Data.to_csv(str(Compare_CPC_Folder) + 'CPC-' + str(Total_CPC_2_Model) + '_maqs_' + str(date_file_label) + '01-to-' + str(date_file_label) + '27' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    Total_CPC_2_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_2_Model) + '_maqs_' + str(date_file_label) + '27-to-' + str(date_file_label) + '31' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    Intercomparison_CPC_2.to_csv(str(Compare_CPC_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + '27-to-' + str(date_file_label) + '31' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
elif int(start_year_month_str) == 202111:
    plt.plot(CPC_Data['Conc (#/cc)'], label='Particle Number count between 1st-10th November in upper position for CPC: ' + str(Total_CPC_1_Model))
    plt.plot(Intercomparison_CPC_Data['Conc (#/cc)'], label='Particle Number count between 1st-10th November in lower position for CPC: ' + str(Total_CPC_2_Model))
    plt.plot(Total_CPC_2_Data['Conc (#/cc)'], label='Particle Number between 10th-31st November from Only Total CPC: ' + str(Total_CPC_2_Model))
    plt.legend()
    plt.ylabel('#/cc')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}
    
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    plt.figure()
    plt.show()
    
    CPC_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + '01-to-' + str(date_file_label) + '10' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    Intercomparison_CPC_Data.to_csv(str(Compare_CPC_Folder) + 'CPC-' + str(Total_CPC_2_Model) + '_maqs_' + str(date_file_label) + '01-to-' + str(date_file_label) + '10' + '_particle-concentration' + str(status) + str(version_number) + '.csv')
    Total_CPC_2_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_2_Model) + '_maqs_' + str(date_file_label) + '10-to-' + str(date_file_label) + '30' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
elif int(start_year_month_str) == 202112:
    plt.plot(CPC_Data['Conc (#/cc)'], label='Particle Number count between 1st-9th December from CPC: ' + str(Total_CPC_1_Model))
    plt.plot(Total_CPC_2_Data['Conc (#/cc)'], label='Particle Number between 9th-31st December from CPC: ' + str(Total_CPC_2_Model))
    plt.legend()
    plt.ylabel('#/cc')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}
    
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    plt.figure()
    plt.show()
    
    CPC_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + '01-to-' + str(date_file_label) + '09' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    Total_CPC_2_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_2_Model) + '_maqs_' + str(date_file_label) + '09-to-' + str(date_file_label) + '31' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
elif int(start_year_month_str) == 202209:
    plt.plot(CPC_Data['Conc (#/cc)'], label='Particle Number from CPC: ' + str(Total_CPC_1_Model) + '_#1')
    plt.plot(Intercomparison_CPC_Data['Conc (#/cc)'], label='Intercomparison Particle Number from CPC: ' + str(Total_CPC_1_Model) + '_#1')
    plt.plot(Total_CPC_2_Data['Conc (#/cc)'], label='Particle Number from CPC: ' + str(Total_CPC_2_Model) )
    plt.legend()
    plt.ylabel('#/cc')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}
    
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    #plt.figure()
    plt.show()
    CPC_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + '01' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    Total_CPC_2_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_2_Model) + '_maqs_' + str(date_file_label) + '01-to-' + str(date_file_label) + '30' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    Intercomparison_CPC_Data.to_csv(str(Compare_CPC_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + '01-to-' + str(date_file_label) + '30' + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
elif int(start_year_month_str) == 202210 or int(start_year_month_str) == 202211:
    # date of intercomparison September to November 2022
    plt.plot(CPC_Data['Conc (#/cc)'], label='Particle Number count in upper position for CPC: ' + str(Total_CPC_1_Model))
    plt.plot(Intercomparison_CPC_Data['Conc (#/cc)'], label='Particle Number count in lower position for CPC: ' + str(Total_CPC_2_Model))
    plt.legend()
    plt.ylabel('#/cc')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}
    
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    #plt.figure()
    plt.show()
    CPC_Data.to_csv(str(Compare_CPC_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    CPC_Data = Intercomparison_CPC_Data
    print(Intercomparison_CPC_Data)
    CPC_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_2_Model) + '_maqs_' + str(date_file_label) + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
elif int(start_year_month_str) == 202212:
    # date of intercomparison December 2022
    plt.plot(CPC_Data['Conc (#/cc)'], label='Particle Number count in upper position for CPC: ' + str(Total_CPC_2_Model))
    plt.plot(Total_Other_CPC_Data['Conc (#/cc)'], label='Particle Number count in lower position for CPC: ' + str(Total_CPC_1_Model))
    plt.legend()
    plt.ylabel('#/cc')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}
    
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    #plt.figure()
    plt.show()
    CPC_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_2_Model) + '_maqs_' + str(date_file_label) + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
    Total_Other_CPC_Data.to_csv(str(Compare_CPC_Folder) + 'CPC-' + str(Total_CPC_1_Model) + '_maqs_' + str(date_file_label) + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')
else:
    
    if Total_CPC_1_Model == 'N/A':
        Total_CPC_Model_No = Total_CPC_2_Model
    else: #Total_CPC_2_Model == 'N/A'
        Total_CPC_Model_No = Total_CPC_1_Model
        
    plt.plot(CPC_Data['Conc (#/cc)'], label= ('Particle Number from: CPC ' + str(Total_CPC_Model_No)))
    plt.legend()
    plt.ylabel('#/cc')
    plt.rc('figure', figsize=(60, 100))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}
    
    plt.rc('font', **font)
    #plt.ylim(10, 30)
    plt.figure()
    plt.show()
    
    CPC_Data.to_csv(str(CPC_Folder) + 'CPC-' + str(Total_CPC_Model_No) + '_maqs_' + str(date_file_label) + '_particle-concentration' + str(status) + str(version_number) + '.1.csv')

CPC_Data['TimeDateSince'] = CPC_Data.index-datetime.datetime(1970,1,1,0,0,00)
CPC_Data['TimeSecondsSince'] = CPC_Data['TimeDateSince'].dt.total_seconds()
CPC_Data['day_year'] = pd.DatetimeIndex(CPC_Data['TimeDateSince'].index).dayofyear
CPC_Data['year'] = pd.DatetimeIndex(CPC_Data['TimeDateSince'].index).year
CPC_Data['month'] = pd.DatetimeIndex(CPC_Data['TimeDateSince'].index).month
CPC_Data['day'] = pd.DatetimeIndex(CPC_Data['TimeDateSince'].index).day
CPC_Data['hour'] = pd.DatetimeIndex(CPC_Data['TimeDateSince'].index).hour
CPC_Data['minute'] = pd.DatetimeIndex(CPC_Data['TimeDateSince'].index).minute
CPC_Data['second'] = pd.DatetimeIndex(CPC_Data['TimeDateSince'].index).second

if int(start_year_month_str) == 202102 or int(start_year_month_str) == 202110 or int(start_year_month_str) == 202111 or int(start_year_month_str) == 202112 or int(start_year_month_str) == 202209:
    Total_CPC_2_Data['TimeDateSince'] = Total_CPC_2_Data.index-datetime.datetime(1970,1,1,0,0,00)
    Total_CPC_2_Data['TimeSecondsSince'] = Total_CPC_2_Data['TimeDateSince'].dt.total_seconds()
    Total_CPC_2_Data['day_year'] = pd.DatetimeIndex(Total_CPC_2_Data['TimeDateSince'].index).dayofyear
    Total_CPC_2_Data['year'] = pd.DatetimeIndex(Total_CPC_2_Data['TimeDateSince'].index).year
    Total_CPC_2_Data['month'] = pd.DatetimeIndex(Total_CPC_2_Data['TimeDateSince'].index).month
    Total_CPC_2_Data['day'] = pd.DatetimeIndex(Total_CPC_2_Data['TimeDateSince'].index).day
    Total_CPC_2_Data['hour'] = pd.DatetimeIndex(Total_CPC_2_Data['TimeDateSince'].index).hour
    Total_CPC_2_Data['minute'] = pd.DatetimeIndex(Total_CPC_2_Data['TimeDateSince'].index).minute
    Total_CPC_2_Data['second'] = pd.DatetimeIndex(Total_CPC_2_Data['TimeDateSince'].index).second
else:
    pass



