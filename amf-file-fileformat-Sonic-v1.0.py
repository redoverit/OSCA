

import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date

#def check_times(allFiles):
version_number = 'v1.0'
direct = str(sonic_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'
today = date.today()
current_month = today.strftime("%B %Y")
first_month_studied = start.strftime("%B %Y")
last_month_studied = end.strftime("%B %Y")
months_studied = np.where(first_month_studied == last_month_studied, first_month_studied, str(first_month_studied) + ' till ' + str(last_month_studied))

dataset_out = nc.Dataset(direct + 'maqs-sonic-1_maqs_' + str(date_file_label) + '_mean-winds_v1.0.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.1'
dataset_out.source = 'maqs-sonic-1'
dataset_out.instrument_manufacturer = 'Gill'
dataset_out.instrument_model = 'Windmaster'
dataset_out.instrument_serial_number = '180602'
dataset_out.instrument_software = 'unknown'
dataset_out.instrument_software_version = 'unknown'
dataset_out.creator_name = 'Dr Nathan Watson'
dataset_out.creator_email = 'nathan.watson@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-9096-0926'
dataset_out.institution = 'University of Manchester'
dataset_out.processing_software_url = 'https://github.com/redoverit/OSCA/'
dataset_out.processing_software_version = 'v3.0'
dataset_out.calibration_sensitivity = 'not known'
dataset_out.calibration_certification_url = 'not known'
dataset_out.sampling_interval = '0.1 second'
dataset_out.averaging_interval = '1 minute'
dataset_out.product_version = version_number
dataset_out.processing_level = '1'
dataset_out.last_revised_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
dataset_out.project = 'NERC Integrated Research Observation System for Clean Air (OSCA)'
dataset_out.project_principal_investigator = 'Hugh Coe'
dataset_out.project_princiapl_invstigator_email = 'hugh.coe@manchester.ac.uk'
dataset_out.project_principal_investigator_url = 'https://www.research.manchester.ac.uk/portal/hugh.coe.html'
dataset_out.licence = 'Data usage licence - UK Government Open Licence agreement: http://www.nationalarchives.gov.uk/doc/open-government-licence'
dataset_out.acknowledgement = 'Acknowledgement of NERC +OSCA as the data provider is required whenever and wherever this data is used'
dataset_out.platform = 'Manchester Air Quality Supersite (maqs)'
dataset_out.platform_type = 'stationary_platform'
dataset_out.deployment_mode = 'land'
dataset_out.title = 'Wind speed and direction'
dataset_out.featureType = 'timeSeries'
dataset_out.time_coverage_start = start.strftime('%Y-%m-%dT%H:%M:%S')
dataset_out.time_coverage_end = end.strftime('%Y-%m-%d %HT%M:%S')
dataset_out.geospatial_bounds = '53.456636N -2.214244E'
dataset_out.platform_altitude = '50 m'
dataset_out.location_keywords = 'MAQS, Supersite, Firs, Fallowfield'
dataset_out.amf_vocabularies_release = 'https://github.com/ncasuk/AMF_CVs/releases/tag/v1.0.0'
dataset_out.history = ' Acquired ' + str(months_studied) + ' and Data processed ' + str(current_month)
dataset_out.comment = 'Measurement Height 7m above ground level'

# Dimensions
time_dim = dataset_out.createDimension('time',None)
latitude_dim = dataset_out.createDimension('latitude',1)
longitude_dim = dataset_out.createDimension('longitude',1)


# create variables (empty to begin with)

times = dataset_out.createVariable('time', np.float64, ('time',))
times.type = 'float64'
times.units = 'seconds since 1970-01-01T00:00:00'
times.long_name = 'Time (seconds since 1970-01-01 00:00:00)'
times.axis = 'T'
times.valid_min = sonic_Data['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = sonic_Data['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.calendar = 'standard'

latitudes = dataset_out.createVariable('latitude', np.float32, ('latitude',))
latitudes.type = 'float32'
latitudes.dimension = 'latitude'
latitudes.units = 'degree_north'
latitudes.standard_name = 'latitude'
latitudes.long_name = 'Latitude'


longitudes = dataset_out.createVariable('longitude', np.float32, ('longitude',))
longitudes.type = 'float32'
longitudes.dimension = 'longitude'
longitudes.units = 'degree_east'
longitudes.standard_name = 'longitude'
longitudes.long_name = 'Longitude'


day_of_year = dataset_out.createVariable('day_of_year', np.float32, ('time',))
day_of_year.type = 'float32'
day_of_year.dimension = 'time'
day_of_year.units = '1'
day_of_year.standard_name = ''
day_of_year.long_name = 'Day of Year'
day_of_year.valid_min = sonic_Data['day_year'].min()
day_of_year.valid_max = sonic_Data['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = sonic_Data['year'].min()
year.valid_max = sonic_Data['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = sonic_Data['month'].min()
month.valid_max = sonic_Data['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = sonic_Data['day'].min()
day.valid_max = sonic_Data['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = sonic_Data['hour'].min()
hour.valid_max = sonic_Data['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = sonic_Data['minute'].min()
minute.valid_max = sonic_Data['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = sonic_Data['second'].min()
second.valid_max = sonic_Data['second'].max()


WindSp = dataset_out.createVariable('wind_speed', np.float32, ('time',), fill_value=-1.00E+20)
WindSp.type = 'float32'
WindSp.units ='m s-1'
WindSp.long_name = 'Mean Wind Speed'
WindSp.valid_min = sonic_Data['wind_Sp (m/s)'].min()
WindSp.valid_max = sonic_Data['wind_Sp (m/s)'].max()
WindSp.call_methods = 'time:mean'
WindSp.coordinates =  '53.456636N, -2.214244E'

qc_flag_WindSp = dataset_out.createVariable('qc_flag_wind_speed', 'b', ('time',))
qc_flag_WindSp.type = 'byte'
qc_flag_WindSp.units = '1'
qc_flag_WindSp.long_name = 'Data Quality flag: Wind Speed' 
qc_flag_WindSp.flag_values ='0b,1b,2b,3b,4b' 
qc_flag_WindSp.flag_meanings = '\n\rnot_used \n\rgood \n\rbad \n\rsuspect \n\rlocal_unusual_activity,'

MaxWindSp = dataset_out.createVariable('wind_speed_of_gust', np.float32, ('time',), fill_value=-1.00E+20)
MaxWindSp.type = 'float32'
MaxWindSp.units ='m s-1'
MaxWindSp.long_name = 'Maximum Wind Speed Observed in Averaging period'
MaxWindSp.valid_min = sonic_Data['max_Gust (m/s)'].min()
MaxWindSp.valid_max = sonic_Data['max_Gust (m/s)'].max()
MaxWindSp.call_methods = 'time:maximum'
MaxWindSp.coordinates =  '53.456636N, -2.214244E'

WindDir = dataset_out.createVariable('wind_from_direction', np.float32, ('time',), fill_value=-1.00E+20)
WindDir.type = 'float32'
WindDir.units ='degree'
WindDir.long_name = 'Wind From Direction'
WindDir.valid_min = sonic_Data['max_Gust (m/s)'].min()
WindDir.valid_max = sonic_Data['max_Gust (m/s)'].max()
WindDir.call_methods = 'time:mean'
WindDir.coordinates =  '53.456636N, -2.214244E'

qc_flag_WindDir = dataset_out.createVariable('qc_flag_wind_direction', 'b', ('time',))
qc_flag_WindDir.type = 'byte'
qc_flag_WindDir.units = '1'
qc_flag_WindDir.long_name = 'Wind Direction flags' 
qc_flag_WindDir.flag_values ='0b,1b,2b,3b,4b' 
qc_flag_WindDir.flag_meanings = '\n\rnot_used \n\rgood \n\rbad \n\rsuspect \n\rlocal_unusual_activity,'


# this bit writes the data from the master dataframe to the variables
times[:] = sonic_Data['TimeSecondsSince'].values#nc.date2num(timeline[:],times.units)
day_of_year[:] = sonic_Data['day_year'].values
year[:] = sonic_Data['year'].values
month[:] = sonic_Data['month'].values
day[:] = sonic_Data['day'].values
hour[:] = sonic_Data['hour'].values
minute[:] = sonic_Data['minute'].values
second[:] = sonic_Data['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244
WindSp[:] = sonic_Data['wind_Sp (m/s)'].values
Flag_WindSp_Byte = np.array(sonic_Data['qc_flag_wind_Sp']).astype(np.ubyte)
qc_flag_WindSp[:] = Flag_WindSp_Byte
MaxWindSp[:] = sonic_Data['max_Gust (m/s)'].values
WindDir[:] = sonic_Data['wind_Dr (deg)'].values
Flag_WindDir_Byte = np.array(sonic_Data['qc_flag_wind_Dr']).astype(np.ubyte)
qc_flag_WindDir[:] = Flag_WindDir_Byte


dataset_out.close()
