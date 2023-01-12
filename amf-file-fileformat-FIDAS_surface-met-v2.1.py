

import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date
import datetime

#def check_times(allFiles):

direct = str(fidas_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

today = date.today()
current_month = today.strftime("%B %Y")
first_month_studied = start.strftime("%B %Y")
last_month_studied = end.strftime("%B %Y")
months_studied = np.where(first_month_studied == last_month_studied, first_month_studied, str(first_month_studied) + ' till ' + str(last_month_studied))
print(months_studied)

dataset_out = nc.Dataset(direct + 'fidas_maqs_' + str(original_date_file_label) + '_surface-met_' + str(datatype) + '_' + str(version_number) + '.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.1'
dataset_out.source = 'maqs-fidas-1'
dataset_out.instrument_manufacturer = 'Palas'
dataset_out.instrument_model = 'FIDAS 200 E'
dataset_out.instrument_serial_number = '9380'
dataset_out.instrument_software = 'unknown'
dataset_out.instrument_software_version = '100434'
dataset_out.creator_name = 'Dr Nathan Watson'
dataset_out.creator_email = 'nathan.watson@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-9096-0926'
dataset_out.institution = 'University of Manchester'
dataset_out.processing_software_url = 'https://github.com/redoverit/OSCA/'
dataset_out.processing_software_version = str(version_number)
dataset_out.calibration_sensitivity = 'not known'
dataset_out.calibration_certification_url = 'https://github.com/redoverit/OSCA/blob/main/FIDAS%20calibration%20cert.pdf'
dataset_out.sampling_interval = '1 second'
dataset_out.averaging_interval = '1 minute'
dataset_out.product_version = str(version_number) 
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
dataset_out.title = 'Surface Meteorology'
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
times.valid_min = fidas_Met['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = fidas_Met['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
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
day_of_year.valid_min = fidas_Met['day_year'].min()
day_of_year.valid_max = fidas_Met['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = fidas_Met['year'].min()
year.valid_max = fidas_Met['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = fidas_Met['month'].min()
month.valid_max = fidas_Met['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = fidas_Met['day'].min()
day.valid_max = fidas_Met['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = fidas_Met['hour'].min()
hour.valid_max = fidas_Met['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = fidas_Met['minute'].min()
minute.valid_max = fidas_Met['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = fidas_Met['second'].min()
second.valid_max = fidas_Met['second'].max()


AirPres = dataset_out.createVariable('air_pressure', np.float32, ('time',), fill_value=-1.00E+20)
AirPres.type = 'float32'
AirPres.dimension = 'time' 
AirPres.units ='hPa'
AirPres.long_name = 'Air Pressure'
AirPres.valid_min = fidas_Met['Pressure (mbar)'].min()
AirPres.valid_max = fidas_Met['Pressure (mbar)'].max()
AirPres.call_methods = 'time:mean'
AirPres.coordinates =  '53.456636N -2.214244E'

qc_flag_AirPres = dataset_out.createVariable('qc_flag_air_pressure', 'b', ('time',))
qc_flag_AirPres.type = 'byte'
qc_flag_AirPres.units = '1'
qc_flag_AirPres.long_name = 'Data Quality flag: Air Pressure' 
qc_flag_AirPres.flag_values ='0b,1b,2b,3b,4b' 
qc_flag_AirPres.flag_meanings = '\n\rnot_used \n\rgood \n\rbad \n\rsuspect \n\rlocal_unusual_activity,'

AirTemp = dataset_out.createVariable('air_temperature', np.float32, ('time',), fill_value=-1.00E+20)
AirTemp.type = 'float32'
AirTemp.dimension = 'time' 
AirTemp.units ='K'
AirTemp.long_name = 'Air Temperature'
AirTemp.valid_min = fidas_Met['Temperature (K)'].min()
AirTemp.valid_max = fidas_Met['Temperature (K)'].max()
AirTemp.call_methods = 'time:mean'
AirTemp.coordinates =  '53.456636N -2.214244E'

qc_flag_AirTemp = dataset_out.createVariable('qc_flag_air_temperature', 'b', ('time',))
qc_flag_AirTemp.type = 'byte'
qc_flag_AirTemp.units = '1'
qc_flag_AirTemp.long_name = 'Data Quality flag: Air Temperature' 
qc_flag_AirTemp.flag_values ='0b,1b,2b,3b,4b' 
qc_flag_AirTemp.flag_meanings = '\n\rnot_used \n\rgood \n\rbad \n\rsuspect \n\rlocal_unusual_activity,'

RelHum = dataset_out.createVariable('relative_humidity', np.float32, ('time',), fill_value=-1.00E+20)
RelHum.type = 'float32'
RelHum.dimension = 'time' 
RelHum.units ='%'
RelHum.long_name = 'Relative Humidity'
RelHum.valid_min = fidas_Met['Humidity (%)'].min()
RelHum.valid_max = fidas_Met['Humidity (%)'].max()
RelHum.call_methods = 'time:mean'
RelHum.coordinates =  '53.456636N -2.214244E'

qc_flag_RelHum = dataset_out.createVariable('qc_flag_relative_humidity', 'b', ('time',))
qc_flag_RelHum.type = 'byte'
qc_flag_RelHum.units = '1'
qc_flag_RelHum.long_name = 'Data Quality flag: Relative Humidity' 
qc_flag_RelHum.flag_values ='0b,1b,2b,3b,4b' 
qc_flag_RelHum.flag_meanings = '\n\rnot_used \n\rgood \n\rbad \n\rsuspect \n\rlocal_unusual_activity,'


# this bit writes the data from the master dataframe to the variables
times[:] = fidas_Met['TimeSecondsSince'].values #nc.date2num(timeline[:],times.units)
day_of_year[:] = fidas_Met['day_year'].values
year[:] = fidas_Met['year'].values
month[:] = fidas_Met['month'].values
day[:] = fidas_Met['day'].values
hour[:] = fidas_Met['hour'].values
minute[:] = fidas_Met['minute'].values
second[:] = fidas_Met['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244
Flag_Pressure_Byte = np.array(fidas_Met['Pressure_Flag']).astype(np.ubyte)
AirPres[:] = fidas_Met['Pressure (mbar)'].values
qc_flag_AirPres[:] = Flag_Pressure_Byte
Flag_Temp_Byte = np.array(fidas_Met['Temperature_Flag']).astype(np.ubyte)
AirTemp[:] = fidas_Met['Temperature (K)'].values
qc_flag_AirTemp[:] = Flag_Temp_Byte
Flag_Humidity_Byte = np.array(fidas_Met['Humidity_Flag']).astype(np.ubyte)
RelHum[:] = fidas_Met['Humidity (%)'].values
qc_flag_RelHum[:] = Flag_Humidity_Byte

dataset_out.close()
