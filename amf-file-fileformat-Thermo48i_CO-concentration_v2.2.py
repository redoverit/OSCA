

import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date
import datetime

#def check_times(allFiles):
version_number = 'v2.2' #version of the code
direct = str(gas_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

today = date.today()
current_month = today.strftime("%B %Y")
first_month_studied = start.strftime("%B %Y")
last_month_studied = end.strftime("%B %Y")
months_studied = np.where(first_month_studied == last_month_studied, first_month_studied, str(first_month_studied) + ' till ' + str(last_month_studied))
print(months_studied)

status = np.where(validity_status == 'Unratified' , '_Unratified_', '_Ratified_')

dataset_out = nc.Dataset(direct + 'Thermo-48i_maqs_' + str(date_file_label) + '_CO-concentration' + str(status) + str(version_number) + '.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.1'
dataset_out.source = 'maqs-48i-1'
dataset_out.instrument_manufacturer = 'Thermo'
dataset_out.instrument_model = '48i'
dataset_out.instrument_serial_number = 'unknown'
dataset_out.instrument_software = 'unknown'
dataset_out.instrument_software_version = 'unknown'
dataset_out.creator_name = 'Dr Nathan Watson'
dataset_out.creator_email = 'nathan.watson@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-9096-0926'
dataset_out.institution = 'University of Manchester'
dataset_out.processing_software_url = 'https://github.com/redoverit/OSCA/'
dataset_out.processing_software_version = str(version_number)
dataset_out.calibration_sensitivity = 'not known'
dataset_out.calibration_certification_url = 'https://github.com/redoverit/OSCA/blob/main/CO%Thermo%20cert.pdf'
dataset_out.sampling_interval = '10 second'
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
dataset_out.title = 'Carbon Monoxide Concentration'
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
times.valid_min = CO_Data['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = CO_Data['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
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
day_of_year.valid_min = CO_Data['day_year'].min()
day_of_year.valid_max = CO_Data['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = CO_Data['year'].min()
year.valid_max = CO_Data['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = CO_Data['month'].min()
month.valid_max = CO_Data['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = CO_Data['day'].min()
day.valid_max = CO_Data['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = CO_Data['hour'].min()
hour.valid_max = CO_Data['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = CO_Data['minute'].min()
minute.valid_max = CO_Data['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = CO_Data['second'].min()
second.valid_max = CO_Data['second'].max()


CO = dataset_out.createVariable('mass_fraction_of_carbon_monoxide_in_air', np.float32, ('time',), fill_value=-1.00E+20)
CO.type = 'float32'
CO.dimension = 'time' 
CO.practical_units ='ppb'
CO.standard_name = 'mass_fraction_of_carbon_monoxide_in_air' 
CO.long_name = 'Mass Fraction of Carbon Monoxide in air'
CO.valid_min = CO_Data['CO (ppb)'].min()
CO.valid_max = CO_Data['CO (ppb)'].max()
CO.call_methods = 'time:mean'
CO.coordinates =  '53.456636N -2.214244E'
CO.chemical_species = 'CO'

qc_flag_CO = dataset_out.createVariable('qc_flag_co', 'b', ('time',))
qc_flag_CO.type = 'byte'
qc_flag_CO.units = '1'
qc_flag_CO.long_name = 'Data Quality flag' 
qc_flag_CO.flag_values ='0b,1b,2b,3b,4b' 
qc_flag_CO.flag_meanings = '\n\rnot_used \n\rgood \n\rbad \n\rsuspect \n\rlocal_unusual_activity,'



# this bit writes the data from the master dataframe to the variables
times[:] = CO_Data['TimeSecondsSince'].values#nc.date2num(timeline[:],times.units)
day_of_year[:] = CO_Data['day_year'].values
year[:] = CO_Data['year'].values
month[:] = CO_Data['month'].values
day[:] = CO_Data['day'].values
hour[:] = CO_Data['hour'].values
minute[:] = CO_Data['minute'].values
second[:] = CO_Data['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244
CO[:] = CO_Data['CO (ppb)'].values
Flag_CO_Byte = np.array(CO_Data['CO_qc_flags']).astype(np.ubyte)
qc_flag_CO[:] = Flag_CO_Byte

dataset_out.close()
