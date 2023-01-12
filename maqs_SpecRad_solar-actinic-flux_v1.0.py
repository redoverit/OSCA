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
#daily_Freq = '1440min'
data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v1.0' #version of the code
year_start = 2019 #input the year of study by number
month_start = 12 #input the month of study by number
default_start_day = 1 #default start date set
day_start = default_start_day #can put number
end_day = "default" # put either "default" or your end day
validity_status = 'Ratified' #Ratified or Unratified
integration_time = 0.00616 # (s)

status = np.where(validity_status == 'Unratified' , '_Unratified_', '_Ratified_')

today = date.today()
current_day = today.strftime("%Y%m%d")

#New_Start = datetime.datetime(2020,5,1,0,0,0) 
#New_End = datetime.datetime(2020,5,3,23,59,59) 

start = datetime.datetime(year_start,month_start,day_start,0,0,0) #start time of the period 
month_After = start + dateutil.relativedelta.relativedelta(months=1)
default_end_date = month_After - timedelta(minutes=1) #last day of month more complex so established here

default_end_day = str(default_end_date.strftime("%Y")) + str(default_end_date.strftime("%m")) + str(default_end_date.strftime("%d"))

year_end = int(default_end_date.strftime("%Y")) #this converts the default_end_day into the end of time selected
month_end = int(default_end_date.strftime("%m"))
day_end = int(default_end_date.strftime("%d"))

if end_day == "default":
    end = datetime.datetime(year_end,month_end,day_end,23,59,59) #if new end date needed to can be changed here 
else:
    end = datetime.datetime(year_end,month_end,end_day,23,59,59) #if new end date needed to can be changed here 

start_year_month_str = str(start.strftime("%Y")) + str(start.strftime("%m")) # convert start and end months to strings
end_year_month_str = str(end.strftime("%Y")) + str(end.strftime("%m"))

end_Date_Check = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

date_file_label = np.where(start_year_month_str == end_year_month_str, start_year_month_str, str(start_year_month_str) + "-" + str(end_year_month_str))

folder = np.where((str(version_number) == 'v0.6'), 'Preliminary', str(validity_status))
print("using a " + str(folder) + "_" + str(version_number) + " folder")

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/SpecRad/', 'D:/FirsData/SpecRad/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(folder) + '_' + str(version_number) + '/', 'D:/' + str(folder) + '_' + str(version_number) + '/')

#Individual_Files = str(Data_Source_Folder) + str(date_file_label) + '*' + 'FirsSpecRad' + '*' + '.txt'

Group_Files = 'FLMS125261' 
time_of_file = '15-50-16'
time_group_file = '155016'

Title_File_Name = str(Data_Source_Folder) + 'Specrad_Cal_Photolysis_Param.csv'

Title_Files = glob.glob(Title_File_Name)

frames = []

for csv in Title_Files:
    csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv, low_memory=False, header=None, index_col=False,skip_blank_lines=True, error_bad_lines=False, na_filter=True) ##, usecols=[0,1,5,6,7,8,9,10,11,12], skiprows=
    frames.append(df)
    
Specrad_Titles = pd.concat(frames)
Specrad_Titles = Specrad_Titles.transpose()
Specrad_Titles[:] = Specrad_Titles[:].astype(float)

Cal_File = Specrad_Titles[[0,1,2]]
Cal_File.rename(columns={0: 'Wavelength', 1: 'Dark_Array', 2: 'Cal_Array'}, inplace=True)
Cal_File.index = Cal_File['Wavelength']
Cal_File = Cal_File.sort_index()
Cal_File.drop(Cal_File[(Cal_File['Cal_Array'].isnull() )].index,inplace =True)


O1D_Cross_Section = Specrad_Titles[[3,4]]
O1D_Cross_Section.rename(columns={3: 'Wavelength', 4: 'O1D_Cross_Section'}, inplace=True)
O1D_Cross_Section.drop(O1D_Cross_Section[(O1D_Cross_Section['O1D_Cross_Section'].isnull() )].index,inplace =True)
O1D_Cross_Section.index = O1D_Cross_Section['Wavelength']
O1D_Cross_Section = O1D_Cross_Section.sort_index()

O1D_Yield = Specrad_Titles[[5,6]]
O1D_Yield.rename(columns={5: 'Wavelength', 6: 'O1D_Yield'}, inplace=True)
O1D_Yield.drop(O1D_Yield[(O1D_Yield['O1D_Yield'].isnull() )].index,inplace =True)
O1D_Yield.index = O1D_Yield['Wavelength']
O1D_Yield = O1D_Yield.sort_index()

NO2_Cross_Section = Specrad_Titles[[7,8]]
NO2_Cross_Section.rename(columns={7: 'Wavelength', 8: 'NO2_Cross_Section'}, inplace=True)
NO2_Cross_Section.drop(NO2_Cross_Section[(NO2_Cross_Section['NO2_Cross_Section'].isnull() )].index,inplace =True)
NO2_Cross_Section.index = NO2_Cross_Section['Wavelength']
NO2_Cross_Section = NO2_Cross_Section.sort_index()

NO2_Yield = Specrad_Titles[[9,10]]
NO2_Yield.rename(columns={9: 'Wavelength', 10: 'NO2_Yield'}, inplace=True)
NO2_Yield.drop(NO2_Yield[(NO2_Yield['NO2_Yield'].isnull() )].index,inplace =True)
NO2_Yield.index = NO2_Yield['Wavelength']
NO2_Yield = NO2_Yield.sort_index()

Cal_File['O1D_Cross_Section'] = np.interp(Cal_File['Wavelength'], O1D_Cross_Section['Wavelength'], O1D_Cross_Section['O1D_Cross_Section'])
Cal_File['O1D_Cross_Section'] = Cal_File['O1D_Cross_Section'] * 1E-20
Cal_File['O1D_Yield'] = np.interp(Cal_File['Wavelength'], O1D_Yield['Wavelength'], O1D_Yield['O1D_Yield'])
Cal_File['NO2_Cross_Section'] = np.interp(Cal_File['Wavelength'], NO2_Cross_Section['Wavelength'], NO2_Cross_Section['NO2_Cross_Section'])
Cal_File['NO2_Cross_Section'] = Cal_File['NO2_Cross_Section'] * 1E-20
Cal_File['NO2_Yield'] = np.interp(Cal_File['Wavelength'], NO2_Yield['Wavelength'], NO2_Yield['NO2_Yield'])

Cal_File['hc/wavelength'] = 1.9864568E-25/(Cal_File['Wavelength'] * 1E-9)

Cal_File['Wavelength+1_offset'] = Cal_File['Wavelength'].shift(periods=1)
Cal_File['Wavelength+1_offset'] = np.where(Cal_File['Wavelength+1_offset'].isnull() , 178.289, Cal_File['Wavelength+1_offset'])

Cal_File['Bandwidth Array'] = Cal_File['Wavelength'] - Cal_File['Wavelength+1_offset']

Specrad_Titles = Specrad_Titles.transpose()
Cal_File = Cal_File.transpose()

Specrad_Titles = Specrad_Titles[0:2]

SpecRad_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/SpecRad/'
check_Folder = os.path.isdir(SpecRad_Folder)
if not check_Folder:
    os.makedirs(SpecRad_Folder)
    print("created folder : ", SpecRad_Folder)

else:
    print(SpecRad_Folder, "folder already exists.")

Intercept = 0.872638
Coefficient_1 = 5.083020E-06
Coefficient_2 = 3.465250E-10
Coefficient_3 = 4.115760E-14
Coefficient_4 = 1.760150E-18
Coefficient_5 = 3.859870E-23
Coefficient_6 = 4.327830E-28
Coefficient_7 = 1.982860E-33


if int(month_start) == 4 or int(month_start) == 6 or int(month_start) == 9 or int(month_start) == 11:
    month_days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
elif int(month_start)==2:
    if int(day_end) == 28:
        month_days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']
    else:
        month_days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29']
else:
    #month_days = ['01','02','03']
    month_days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']

for x in month_days:
    if x == '01':
        Individual_Files = str(Data_Source_Folder) + '*' + str(date_file_label) + x + '*' + 'FirsSpecRad' + '*' + '.txt'
    elif x == '02' and str(date_file_label) == '201912':
        Individual_Files = str(Data_Source_Folder) + '*' + str(date_file_label) + x + '*' + 'FirsSpecRad' + '*' + '.txt'
    elif x == '06' and str(date_file_label) == '202001':
        Individual_Files = str(Data_Source_Folder) + '*' + str(date_file_label) + x + '*' + 'FirsSpecRad' + '*' + '.txt'
    elif x == '03' and str(date_file_label) == '202002':
        Individual_Files = str(Data_Source_Folder) + '*' + str(date_file_label) + x + '*' + 'FirsSpecRad' + '*' + '.txt'
    elif x == '02' and str(date_file_label) == '202003':
        Individual_Files = str(Data_Source_Folder) + '*' + str(date_file_label) + x + '*' + 'FirsSpecRad' + '*' + '.txt'
    elif x == '04' and str(date_file_label) == '202005':
        Individual_Files = str(Data_Source_Folder) + '*' + str(date_file_label) + x + '*' + 'FirsSpecRad' + '*' + '.txt'
    else:
        Individual_Files = str(Data_Source_Folder) +  str(date_file_label) + x + '*' + 'FirsSpecRad' + '*' + '.txt'
    Spec_Rad_file = glob.glob(str(Individual_Files))
    print(x)
    
    rows_to_skip = np.where(float(str(date_file_label) + x) < 20200505, 15, 0)
    rows_to_skip = np.where(float(str(date_file_label) + x) == 20210630, 15, int(rows_to_skip))
    rows_to_skip = np.where(float(str(date_file_label) + x) == 20200512, 15, int(rows_to_skip))
    rows_to_skip = np.where(float(str(date_file_label) + x) == 20200812, 15, int(rows_to_skip))
    rows_to_skip = np.where(float(str(date_file_label) + x) == 20220301, 15, int(rows_to_skip))
    rows_to_skip = np.where(float(str(date_file_label) + x) == 20220625, 15, int(rows_to_skip))
    print(float(str(date_file_label) + x))
    print(Individual_Files)
    frames = []
        
    try:
        for csv in Spec_Rad_file:
            csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
            df = pd.read_csv(csv, sep="\t", skiprows=int(rows_to_skip), low_memory=False, header=None, index_col=False, skip_blank_lines=True, error_bad_lines=False, na_filter=True) ##, usecols=[0,1,5,6,7,8,9,10,11,12], skiprows=
            frames.append(df)
        
        actinic_Data = pd.concat(frames)
        
    except ValueError:
        Individual_Files = str(Data_Source_Folder) +'20190808_FirsSpecRad.txt'
        Spec_Rad_file = glob.glob(str(Individual_Files))
        
        for csv in Spec_Rad_file:
            csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
            df = pd.read_csv(csv, sep="\t", skiprows=15, low_memory=False, header=None, index_col=False, skip_blank_lines=True, error_bad_lines=False, na_filter=True) ##, usecols=[0,1,5,6,7,8,9,10,11,12], skiprows=
            frames.append(df)
        
        actinic_Data = pd.concat(frames)
    
    actinic_Data = actinic_Data.drop(columns=[1])
    Datetime = actinic_Data.iloc[:,0:1]
    Datetime = Datetime.iloc[:,0].str.split('.', expand=True)
    actinic_Data[0] = Datetime[0]

    actinic_Data.rename(columns={0: 'datetime' }, inplace=True)

    actinic_Data['datetime'] = actinic_Data['datetime'].astype(str)
    actinic_Data['datetime_length'] = actinic_Data['datetime'].str.len()
    actinic_Data=actinic_Data[actinic_Data.datetime_length < 21]
    actinic_Data=actinic_Data[actinic_Data.datetime_length > 17]
    actinic_Data['datetime'] = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in actinic_Data['datetime']] #converts the dateTime format from string to python dateTime
    actinic_Data.index = actinic_Data['datetime']
    actinic_Data = actinic_Data.sort_index()
    actinic_Data = actinic_Data.drop(columns=['datetime','datetime_length'])

    actinic_Data.columns = actinic_Data.columns - 2

    actinic_Data.iloc[:] = actinic_Data.iloc[:].astype(float)

    #actinic_Data = pd.concat([Specrad_Titles, actinic_Data])
    Cal_File.iloc[0] = Cal_File.iloc[0].astype(float)
    cal_titles = list(Cal_File.iloc[0])
    #actinic_Data.iloc[0] = actinic_Data.iloc[0].astype(float)
    actinic_Data.columns = cal_titles
    #actinic_Data.drop(actinic_Data[(actinic_Data.iloc[:,0] == 178.674 )].index,inplace =True)
    Cal_File.iloc[1] = Cal_File.iloc[1].astype(float)
    actinic_Data.iloc[:] = actinic_Data.iloc[:].astype(float)
    actinic_Data.iloc[0:] = actinic_Data.iloc[0:] - Cal_File.iloc[1]
    actinic_Data = actinic_Data.iloc[0:]
    actinic_Data.index.name = 'datetime'
    
    actinic_Data = actinic_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
    actinic_Data = actinic_Data.drop(actinic_Data[actinic_Data.iloc[:,0].isnull() ].index)

    actinic_Data['Zero Correction'] = (actinic_Data.iloc[:,267:(267+27)].sum(axis=1))/27
    actinic_Data.iloc[:,0:2049] = actinic_Data.iloc[:,0:2049].astype(float)
    actinic_Data['Zero Correction'] = actinic_Data['Zero Correction'].astype(float)

    actinic_Data = actinic_Data.sub(actinic_Data['Zero Correction'], axis=0)
    actinic_Data = actinic_Data.drop(columns=['Zero Correction'])

    Raw_Counts = actinic_Data

    Lin_Counts = (Raw_Counts.multiply(Coefficient_1)) + Intercept
    Lin_Counts = Lin_Counts.add((Raw_Counts.pow(2)).multiply(Coefficient_2))
    Lin_Counts = Lin_Counts.sub((Raw_Counts.pow(3)).multiply(Coefficient_3))
    Lin_Counts = Lin_Counts.add((Raw_Counts.pow(4)).multiply(Coefficient_4))
    Lin_Counts = Lin_Counts.sub((Raw_Counts.pow(5)).multiply(Coefficient_5))
    Lin_Counts = Lin_Counts.add((Raw_Counts.pow(6)).multiply(Coefficient_6))
    Lin_Counts = Lin_Counts.sub((Raw_Counts.pow(7)).multiply(Coefficient_7))
    Lin_Counts = Raw_Counts.div(Lin_Counts)

    Calibrated_Counts = (Lin_Counts.multiply(Cal_File.iloc[2], axis='columns')) * 1E-6

    integration_value = 1.75 * 1.75 * np.pi * float(integration_time) 

    Actinic_Flux_Array = (Calibrated_Counts.div(Cal_File.iloc[7], axis='columns'))/float(integration_value)

    O1D_Photolysis_Array = Actinic_Flux_Array.multiply(Cal_File.iloc[3], axis='columns')
    O1D_Photolysis_Array = O1D_Photolysis_Array.multiply(Cal_File.iloc[4], axis='columns')
    #O1D_Photolysis_Array = O1D_Photolysis_Array.iloc[:,320:(320+95)]

    NO2_Photolysis_Array = Actinic_Flux_Array.multiply(Cal_File.iloc[5], axis='columns')
    NO2_Photolysis_Array = NO2_Photolysis_Array.multiply(Cal_File.iloc[6], axis='columns')
    #NO2_Photolysis_Array = NO2_Photolysis_Array.iloc[:,320:(320+340)]

    Actinic_Flux_Array = Actinic_Flux_Array.div(Cal_File.iloc[9], axis='columns')

    integration_value_1 = float(integration_value) * 0.0001

    Calibrated_Counts = Calibrated_Counts/float(integration_value_1)

    Photolysis_Data = Calibrated_Counts.iloc[:,0:]
    Photolysis_Data['Solar Radiation (W/m2)'] = (Photolysis_Data.iloc[:,320:].sum(axis=1)) * 1.5625 #280-420 nm
    Photolysis_Data['JO1D (s-1)'] = O1D_Photolysis_Array.iloc[:,320:(320+95)].sum(axis=1)
    Photolysis_Data['JNO2 (s-1)'] = NO2_Photolysis_Array.iloc[:,320:(320+340)].sum(axis=1)

    Photolysis_Data = Photolysis_Data[['Solar Radiation (W/m2)', 'JO1D (s-1)', 'JNO2 (s-1)']]

    Photolysis_Data['datetime'] = Photolysis_Data.index
    Photolysis_Data['datetime'] = Photolysis_Data['datetime'].astype(str)
    Photolysis_Data['datetime'] = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in Photolysis_Data['datetime']] #converts the dateTime format from string to python dateTime
    Photolysis_Data.index = Photolysis_Data['datetime']
    Photolysis_Data = Photolysis_Data.sort_index()
    Photolysis_Data = Photolysis_Data.drop(columns=['datetime'])
    Photolysis_Data = Photolysis_Data.groupby(pd.Grouper(freq=av_Freq)).mean()
    Photolysis_Data = Photolysis_Data[start:end]
    Photolysis_Data = Photolysis_Data.drop(Photolysis_Data[Photolysis_Data['Solar Radiation (W/m2)'].isnull() ].index)

    Calibrated_Counts = Calibrated_Counts.div(Cal_File.iloc[9], axis='columns')

    #actinic_distribution = Calibrated_Counts.iloc[:,0:]
    actinic_distribution = Calibrated_Counts.iloc[:,187:]
    actinic_distribution = actinic_distribution.drop(actinic_distribution[actinic_distribution.iloc[:,188].isnull() ].index)
    actinic_distribution['datetime'] = actinic_distribution.index
    actinic_distribution['datetime'] = actinic_distribution['datetime'].astype(str)
    actinic_distribution['datetime'] = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in actinic_distribution['datetime']] #converts the dateTime format from string to python dateTime
    actinic_distribution.index = actinic_distribution['datetime']
    actinic_distribution = actinic_distribution.sort_index()
    actinic_distribution = actinic_distribution.drop(columns=['datetime'])
    actinic_distribution = actinic_distribution.groupby(pd.Grouper(freq=av_Freq)).mean()
    actinic_distribution = actinic_distribution[start:end]
    actinic_distribution = actinic_distribution.drop(actinic_distribution[actinic_distribution.iloc[:,0].isnull() ].index)
    Photolysis_Data = Photolysis_Data.drop(Photolysis_Data[Photolysis_Data['JNO2 (s-1)'].isnull() ].index)
    Photolysis_Data.rename(columns={'Solar Radiation (W/m2)' : 'Solar Actinic Flux (W/m2)'}, inplace=True)
    
    actinic_distribution['qc_Flags'] = '1'
    Photolysis_Data['qc_Flags'] = '1'
    
    start_peak_1 = datetime.datetime(2019,8,7,14,0,00) #4th October 2022 - Radiometer dome cleaned 10:30 to 11:00
    end_peak_1 = datetime.datetime(2019,8,7,15,0,00)
    #Photolysis_Data.loc[start_peak_1:end_peak_1, 'qc_Flags'] = '2'
    Photolysis_Data.drop(Photolysis_Data.loc[start_peak_1:end_peak_1].index, inplace=True)
    #actinic_distribution.loc[start_peak_1:end_peak_1, 'qc_Flags'] = '2'
    actinic_distribution.drop(actinic_distribution.loc[start_peak_1:end_peak_1].index, inplace=True)
    
    start_software_1 = datetime.datetime(2020,5,7,0,1,00) #7 May 2020 - 00:01 All Labview software stopped logging due to an error generated by SpecRad viewer. Error was cleared around 9.30am and logging resumed. SpecRad viewer has been modified to avoid the reoccurrence of that error.
    end_software_1 = datetime.datetime(2020,5,7,9,45,00)
    Photolysis_Data.loc[start_software_1:end_software_1, 'qc_Flags'] = '2'
    #Photolysis_Data.drop(Photolysis_Data.loc[start_software_1:end_software_1].index, inplace=True)
    actinic_distribution.loc[start_software_1:end_software_1, 'qc_Flags'] = '2'
    #actinic_distribution.drop(actinic_distribution.loc[start_software_1:end_software_1].index, inplace=True)
    
    start_software_2 = datetime.datetime(2020,5,12,11,14,00) #12 May 2020 - 11:14 A few software updates installed: SR Software - updated to better handle file changeover at midnight
    end_software_2 = datetime.datetime(2020,5,12,12,14,00)
    Photolysis_Data.loc[start_software_2:end_software_2, 'qc_Flags'] = '2'
    #Photolysis_Data.drop(Photolysis_Data.loc[start_software_2:end_software_2].index, inplace=True)
    actinic_distribution.loc[start_software_2:end_software_2, 'qc_Flags'] = '2'
    #actinic_distribution.drop(actinic_distribution.loc[start_software_2:end_software_2].index, inplace=True)
    
    start_software_3 = datetime.datetime(2020,6,12,0,0,00) #12 June 2020 - Specrad plotting software updated, should now correctly calculate actinic flux and photolysis rates.
    end_software_3 = datetime.datetime(2020,6,12,23,59,00)
    Photolysis_Data.loc[start_software_3:end_software_3, 'qc_Flags'] = '2'
    #Photolysis_Data.drop(Photolysis_Data.loc[start_software_3:end_software_3].index, inplace=True)
    actinic_distribution.loc[start_software_3:end_software_3, 'qc_Flags'] = '2'
    #actinic_distribution.drop(actinic_distribution.loc[start_software_3:end_software_3].index, inplace=True)
    
    start_clean_1 = datetime.datetime(2022,4,7,9,0,00) #7 April 2022 - 09:35 Disdrometer windows cleaned, radiometer dome cleaned.
    end_clean_1 = datetime.datetime(2022,4,7,10,0,00)
    Photolysis_Data.loc[start_clean_1:end_clean_1, 'qc_Flags'] = '2'
    #Photolysis_Data.drop(Photolysis_Data.loc[start_clean_1:end_clean_1].index, inplace=True)
    actinic_distribution.loc[start_clean_1:end_clean_1, 'qc_Flags'] = '2'
    #actinic_distribution.drop(actinic_distribution.loc[start_clean_1:end_clean_1].index, inplace=True)
    
    start_clean_2 = datetime.datetime(2022,10,4,10,30,00) #4th October 2022 - Radiometer dome cleaned 10:30 to 11:00
    end_clean_2 = datetime.datetime(2022,10,4,11,30,00)
    Photolysis_Data.loc[start_clean_2:end_clean_2, 'qc_Flags'] = '2'
    #Photolysis_Data.drop(Photolysis_Data.loc[start_clean_2:end_clean_2].index, inplace=True)
    actinic_distribution.loc[start_clean_2:end_clean_2, 'qc_Flags'] = '2'
    #actinic_distribution.drop(actinic_distribution.loc[start_clean_2:end_clean_2].index, inplace=True)
    
    
    if x == '01':
        #Photolysis_Data.to_csv(str(SpecRad_Folder) + 'spectral-radiometer_maqs_' + str(start_year_month_str) + '_photolysis-rates' + str(status) +  str(version_number) + '.csv')
        #actinic_distribution.to_csv(str(SpecRad_Folder) + 'spectral-radiometer_maqs_' + str(start_year_month_str) + '_solar-actinic-spectra' + str(status) +  str(version_number) + '.csv')
        complete_actinic = actinic_distribution
        complete_Photolysis = Photolysis_Data        
    else:
        #Photolysis_Data.to_csv(str(SpecRad_Folder) + 'spectral-radiometer_maqs_' + str(start_year_month_str) + '_photolysis-rates' + str(status) +  str(version_number) + '.csv', mode='a', header=False)
        #actinic_distribution.to_csv(str(SpecRad_Folder) + 'spectral-radiometer_maqs_' + str(start_year_month_str) + '_solar-actinic-spectra' + str(status) +  str(version_number) + '.csv', mode='a', header=False)
        complete_actinic = pd.concat([complete_actinic, actinic_distribution])
        complete_Photolysis = pd.concat([complete_Photolysis, Photolysis_Data])
        complete_actinic = complete_actinic.sort_index()
        complete_Photolysis = complete_Photolysis.sort_index()

flag_spectral = complete_actinic['qc_Flags']
complete_actinic = complete_actinic.drop(columns=['qc_Flags'])

first_column = 0
last_column = int(len(complete_actinic.columns)) - 1

first_column = int(first_column)
last_column = int(last_column)

columns = list(range(int(first_column), int(last_column)))

dates = complete_actinic.index # setting x-axis
frequencies = complete_actinic.columns # setting y-axis
frequencies = frequencies.astype(float)
stride = 20                                                 #change stride to change averaging period
dates_subset = dates[::stride]
size_matrix = np.zeros((len(columns), dates_subset.size))
# align the particle size columns as rows into the size matrix
for ind, col in enumerate(columns):    
    size_matrix[ind,:] = complete_actinic.iloc[::stride, col]

x = dates_subset
y = frequencies
z_min, z_max = size_matrix[:].min(), size_matrix[:].max()
z = size_matrix[:]

print(z_max)

fig, ax = plt.subplots()
myplot = ax.pcolormesh(x, y, z, cmap='RdYlBu_r', vmin=z_min, vmax=z_max)
ax.set_title('Solar Actinic Flux')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
plt.colorbar(myplot)
plt.figure()
plt.show
()

complete_actinic['qc_Flags'] = pd.Series(flag_spectral)

plt.plot(complete_Photolysis['Solar Actinic Flux (W/m2)'], label='Solar Actinic Flux')
plt.legend()
plt.ylabel('W/m2')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}
#ax.set_xticks(ax.get_xticks()[::2])
plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

plt.plot(complete_Photolysis['JO1D (s-1)'], label='O1D Photolysis Rates')
plt.legend()
plt.ylabel('s-1')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}
#ax.set_xticks(ax.get_xticks()[::2])
plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

plt.plot(complete_Photolysis['JNO2 (s-1)'], label='NO2 Photolysis Rates')
plt.legend()
plt.ylabel('s-1')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}
#ax.set_xticks(ax.get_xticks()[::2])
plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()

complete_actinic['TimeDateSince'] = complete_actinic.index-datetime.datetime(1970,1,1,0,0,00)
complete_actinic['TimeSecondsSince'] = complete_actinic['TimeDateSince'].dt.total_seconds()
complete_actinic['day_year'] = pd.DatetimeIndex(complete_actinic['TimeDateSince'].index).dayofyear
complete_actinic['year'] = pd.DatetimeIndex(complete_actinic['TimeDateSince'].index).year
complete_actinic['month'] = pd.DatetimeIndex(complete_actinic['TimeDateSince'].index).month
complete_actinic['day'] = pd.DatetimeIndex(complete_actinic['TimeDateSince'].index).day
complete_actinic['hour'] = pd.DatetimeIndex(complete_actinic['TimeDateSince'].index).hour
complete_actinic['minute'] = pd.DatetimeIndex(complete_actinic['TimeDateSince'].index).minute
complete_actinic['second'] = pd.DatetimeIndex(complete_actinic['TimeDateSince'].index).second

complete_Photolysis['TimeDateSince'] = complete_Photolysis.index-datetime.datetime(1970,1,1,0,0,00)
complete_Photolysis['TimeSecondsSince'] = complete_Photolysis['TimeDateSince'].dt.total_seconds()
complete_Photolysis['day_year'] = pd.DatetimeIndex(complete_Photolysis['TimeDateSince'].index).dayofyear
complete_Photolysis['year'] = pd.DatetimeIndex(complete_Photolysis['TimeDateSince'].index).year
complete_Photolysis['month'] = pd.DatetimeIndex(complete_Photolysis['TimeDateSince'].index).month
complete_Photolysis['day'] = pd.DatetimeIndex(complete_Photolysis['TimeDateSince'].index).day
complete_Photolysis['hour'] = pd.DatetimeIndex(complete_Photolysis['TimeDateSince'].index).hour
complete_Photolysis['minute'] = pd.DatetimeIndex(complete_Photolysis['TimeDateSince'].index).minute
complete_Photolysis['second'] = pd.DatetimeIndex(complete_Photolysis['TimeDateSince'].index).second

