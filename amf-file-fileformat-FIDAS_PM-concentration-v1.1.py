

import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date
import datetime

#def check_times(allFiles):
version_number = 'v1.1'
direct = str(fidas_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

today = date.today()
current_month = today.strftime("%B %Y")
first_month_studied = start.strftime("%B %Y")
last_month_studied = end.strftime("%B %Y")
months_studied = np.where(first_month_studied == last_month_studied, first_month_studied, str(first_month_studied) + ' till ' + str(last_month_studied))
print(months_studied)

dataset_out = nc.Dataset(direct + 'maqs-fidas-1_' + str(date_file_label) + '_PM-concentration_' + str(version_number) + '.nc', 'w', format='NETCDF4_CLASSIC')

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
dataset_out.processing_software_version = 'v1.0'
dataset_out.calibration_sensitivity = 'not known'
dataset_out.calibration_certification_url = 'https://github.com/redoverit/OSCA/blob/main/FIDAS%20calibration%20cert.pdf'
dataset_out.sampling_interval = '1 second'
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
dataset_out.title = 'Particulate Matter Concentration'
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
times.valid_min = fidas_PM['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = fidas_PM['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
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
day_of_year.valid_min = fidas_PM['day_year'].min()
day_of_year.valid_max = fidas_PM['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = fidas_PM['year'].min()
year.valid_max = fidas_PM['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = fidas_PM['month'].min()
month.valid_max = fidas_PM['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = fidas_PM['day'].min()
day.valid_max = fidas_PM['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = fidas_PM['hour'].min()
hour.valid_max = fidas_PM['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = fidas_PM['minute'].min()
minute.valid_max = fidas_PM['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = fidas_PM['second'].min()
second.valid_max = fidas_PM['second'].max()


PM1 = dataset_out.createVariable('mass_concentration_of_pm1_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00E+20)
PM1.type = 'float32'
PM1.dimension = 'time' 
PM1.units ='ug m-3'
PM1.standard_name = 'mass_concentration_of_pm1_ambient_aerosol_in_air' 
PM1.long_name = 'Mass Concentration of PM1 Ambient Aerosol in Air'
PM1.valid_min = fidas_PM['PM1 (ug/m3)'].min()
PM1.valid_max = fidas_PM['PM1 (ug/m3)'].max()
PM1.call_methods = 'time:point'
PM1.coordinates =  '53.456636N -2.214244E'

qc_flag_PM1 = dataset_out.createVariable('qc_flag_pm1', 'b', ('time',))
qc_flag_PM1.type = 'byte'
qc_flag_PM1.units = '1'
qc_flag_PM1.long_name = 'Data Quality flag: PM1' 
qc_flag_PM1.flag_values ='0b,1b,2b,3b,4b' 
qc_flag_PM1.flag_meanings = '\n\rnot_used \n\rgood \n\rbad \n\rsuspect \n\rlocal_unusual_activity,'

PM2p5 = dataset_out.createVariable('mass_concentration_of_pm2p5_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00E+20)
PM2p5.type = 'float32'
PM2p5.dimension = 'time' 
PM2p5.units ='ug m-3'
PM2p5.standard_name = 'mass_concentration_of_pm2p5_ambient_aerosol_in_air' 
PM2p5.long_name = 'Mass Concentration of PM2.5 Ambient Aerosol in Air'
PM2p5.valid_min = fidas_PM['PM2.5 (ug/m3)'].min()
PM2p5.valid_max = fidas_PM['PM2.5 (ug/m3)'].max()
PM2p5.call_methods = 'time:point'
PM2p5.coordinates =  '53.456636N -2.214244E'

qc_flag_PM2p5 = dataset_out.createVariable('qc_flag_pm2p5', 'b', ('time',))
qc_flag_PM2p5.type = 'byte'
qc_flag_PM2p5.units = '1'
qc_flag_PM2p5.long_name = 'Data Quality flag: PM2.5' 
qc_flag_PM2p5.flag_values ='0b,1b,2b,3b,4b' 
qc_flag_PM2p5.flag_meanings = '\n\rnot_used \n\rgood \n\rbad \n\rsuspect \n\rlocal_unusual_activity,'

PM10 = dataset_out.createVariable('mass_concentration_of_pm10_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00E+20)
PM10.type = 'float32'
PM10.dimension = 'time' 
PM10.units ='ug m-3'
PM10.standard_name = 'mass_concentration_of_pm10_ambient_aerosol_in_air' 
PM10.long_name = 'Mass Concentration of PM10 Ambient Aerosol in Air'
PM10.valid_min = fidas_PM['PM10 (ug/m3)'].min()
PM10.valid_max = fidas_PM['PM10 (ug/m3)'].max()
PM10.call_methods = 'time:point'
PM10.coordinates =  '53.456636N -2.214244E'

qc_flag_PM10 = dataset_out.createVariable('qc_flag_pm10', 'b', ('time',))
qc_flag_PM10.type = 'byte'
qc_flag_PM10.units = '1'
qc_flag_PM10.long_name = 'Data Quality flag: PM10' 
qc_flag_PM10.flag_values ='0b,1b,2b,3b,4b' 
qc_flag_PM10.flag_meanings = '\n\rnot_used \n\rgood \n\rbad \n\rsuspect \n\rlocal_unusual_activity,'

PM_Cn = dataset_out.createVariable('number_concentration_of_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
PM_Cn.type = 'float32'
PM_Cn.dimension = 'time' 
PM_Cn.units ='cm-3'
PM_Cn.standard_name = 'number_concentration_of_ambient_aerosol_particles_in_air' 
PM_Cn.long_name = 'Number Concentration of Ambient Aerosol Particles in air'
PM_Cn.valid_min = fidas_PM['Cn (P/cm3)'].min()
PM_Cn.valid_max = fidas_PM['Cn (P/cm3)'].max()
PM_Cn.call_methods = 'time:point'
PM_Cn.coordinates =  '53.456636N -2.214244E'

qc_flag_PM_Cn = dataset_out.createVariable('qc_flag_total_number', 'b', ('time',))
qc_flag_PM_Cn.type = 'byte'
qc_flag_PM_Cn.units = '1'
qc_flag_PM_Cn.long_name = 'Data Quality flag: Total Number' 
qc_flag_PM_Cn.flag_values ='0b,1b,2b,3b,4b' 
qc_flag_PM_Cn.flag_meanings = '\n\rnot_used \n\rgood \n\rbad \n\rsuspect \n\rlocal_unusual_activity,'

# this bit writes the data from the master dataframe to the variables
times[:] = fidas_PM['TimeSecondsSince'].values#nc.date2num(timeline[:],times.units)
day_of_year[:] = fidas_PM['day_year'].values
year[:] = fidas_PM['year'].values
month[:] = fidas_PM['month'].values
day[:] = fidas_PM['day'].values
hour[:] = fidas_PM['hour'].values
minute[:] = fidas_PM['minute'].values
second[:] = fidas_PM['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244
Flag_Byte = np.array(fidas_PM['PM_Flag']).astype(np.ubyte)
PM1[:] = fidas_PM['PM1 (ug/m3)'].values
qc_flag_PM1[:] = Flag_Byte
PM2p5[:] = fidas_PM['PM2.5 (ug/m3)'].values
qc_flag_PM2p5[:] = Flag_Byte
PM10[:] = fidas_PM['PM10 (ug/m3)'].values
qc_flag_PM10[:] = Flag_Byte
PM_Cn[:] = fidas_PM['Cn (P/cm3)'].values
qc_flag_PM_Cn[:] = Flag_Byte

dataset_out.close()
