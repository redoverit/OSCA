# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 10:48:07 2022

@author: j65808nw
"""


import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date
import datetime

#def check_times(allFiles):
direct = str(fidas_Dis_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

today = date.today()
current_month = today.strftime("%B %Y")
month_studied = start.strftime("%B %Y")

print(str(month_studied))


if float(start_year_month_str) < 1906:
    if float(start_year_month_str) < 1812:
        sys.exit("Error Message: This program cannot be used for data prior to December 2018.")
    else:
        #pass
        sys.exit("Error Message: This is Data measured from Simon Building. Just process to CSV, not to be converted to netCDF.")
else:
    pass

dataset_out = nc.Dataset(direct + 'fidas_maqs_' + str(date_file_label) + '_PM-distribution_' + str(datatype) + '_' + str(version_number) + '.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.1'
dataset_out.source = 'maqs-fidas-1'
dataset_out.instrument_manufacturer = 'Palas'
dataset_out.instrument_model = 'FIDAS 200 E'
dataset_out.instrument_serial_number = str(FIDAS_PM_serial_number)
dataset_out.instrument_software = 'unknown'
dataset_out.instrument_software_version = '100434'
dataset_out.creator_name = 'Dr Nathan Watson'
dataset_out.creator_email = 'nathan.watson@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-9096-0926'
dataset_out.institution = 'University of Manchester'
dataset_out.processing_software_url = 'https://github.com/redoverit/OSCA/'
dataset_out.processing_software_version = str(version_number)
dataset_out.calibration_sensitivity = 'not known'
dataset_out.calibration_certification_url = str(FIDAS_PM_cal_cert)
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
dataset_out.title = 'Particulate Matter Distribution'
dataset_out.featureType = 'timeSeries'
dataset_out.time_coverage_start = start.strftime('%Y-%m-%dT%H:%M:%S')
dataset_out.time_coverage_end = end.strftime('%Y-%m-%d %HT%M:%S')
dataset_out.geospatial_bounds = '53.456636N -2.214244E'
dataset_out.platform_altitude = '50 m'
dataset_out.location_keywords = 'MAQS, Supersite, Firs, Fallowfield'
dataset_out.amf_vocabularies_release = 'https://github.com/ncasuk/AMF_CVs/releases/tag/v1.0.0'
dataset_out.history = ' Acquired ' + str(month_studied) + ' and Data processed ' + str(current_month)
dataset_out.comment = 'Measurement Height 7m above ground level'


# Dimensions
time_dim = dataset_out.createDimension('time',None) 
latitude_dim = dataset_out.createDimension('latitude',1)
longitude_dim = dataset_out.createDimension('longitude',1)
aerosol_dim = dataset_out.createDimension('ambient_aerosol_particle_diameter',(int(last_column)-int(first_column)))


# create variables (empty to begin with)

times = dataset_out.createVariable('time', np.float64, ('time',))
times.type = 'float64'
times.units = 'seconds since 1970-01-01T00:00:00'
times.long_name = 'Time (seconds since 1970-01-01 00:00:00)'
times.axis = 'T'
times.valid_min = fidas_Dist['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = fidas_Dist['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
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

fidas_Dist_labels.iloc[0,0:(int(last_column)-int(first_column))] = fidas_Dist_labels.iloc[0,0:(int(last_column)-int(first_column))].astype(float)

ambient_aerosol_particle_diameter = dataset_out.createVariable('ambient_aerosol_particle_diameter', np.float32, ('ambient_aerosol_particle_diameter',))
ambient_aerosol_particle_diameter.type = 'float64' 
ambient_aerosol_particle_diameter.units = 'um'
ambient_aerosol_particle_diameter.standard_name = 'ambient_aerosol_particle_diameter' 
ambient_aerosol_particle_diameter.long_name = 'Ambient Aerosol Particle Diameter'
ambient_aerosol_particle_diameter.valid_min = float(Smallest_Aerosol)
ambient_aerosol_particle_diameter.valid_max = float(Largest_Aerosol)
ambient_aerosol_particle_diameter[:] = fidas_Dist_labels.iloc[0,0:(int(last_column)-int(first_column))]
print(fidas_Dist_labels)

day_of_year = dataset_out.createVariable('day_of_year', np.float32, ('time',))
day_of_year.type = 'float32'
day_of_year.dimension = 'time'
day_of_year.units = '1'
day_of_year.standard_name = ''
day_of_year.long_name = 'Day of Year'
day_of_year.valid_min = fidas_Dist['day_year'].min()
day_of_year.valid_max = fidas_Dist['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = fidas_Dist['year'].min()
year.valid_max = fidas_Dist['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = fidas_Dist['month'].min()
month.valid_max = fidas_Dist['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = fidas_Dist['day'].min()
day.valid_max = fidas_Dist['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = fidas_Dist['hour'].min()
hour.valid_max = fidas_Dist['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = fidas_Dist['minute'].min()
minute.valid_max = fidas_Dist['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = fidas_Dist['second'].min()
second.valid_max = fidas_Dist['second'].max()

times[:] = fidas_Dist['TimeSecondsSince'].values#nc.date2num(timeline[:],times.units)
day_of_year[:] = fidas_Dist['day_year'].values
year[:] = fidas_Dist['year'].values
month[:] = fidas_Dist['month'].values
day[:] = fidas_Dist['day'].values
hour[:] = fidas_Dist['hour'].values
minute[:] = fidas_Dist['minute'].values
second[:] = fidas_Dist['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244

fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))] = fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))].astype(float)

distribution = dataset_out.createVariable('ambient_aerosol_size_distribution', np.float32, ('time', 'ambient_aerosol_particle_diameter',), fill_value=-1.00E+20) #,'ambient_aerosol_particle_diameter'
distribution.type = 'float32'
distribution.dimension = 'time'
distribution.practical_units = '##/cm^3'
distribution.standard_name = 'ambient_aerosol_size_distribution'
distribution.long_name = 'Ambient Aerosol Size Distribution'
distribution.valid_min = (fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))].min()).min()
distribution.valid_max = (fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))].max()).max() 
distribution.call_methods = 'time:mean'
distribution.coordinates =  '53.456636N -2.214244E'
distribution[:] = fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))]

#print(fidas_Dist.iloc[:,0:(int(last_column)-int(first_column))])

PM_Cn = dataset_out.createVariable('number_concentration_of_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
PM_Cn.type = 'float32'
PM_Cn.dimension = 'time' 
PM_Cn.units ='##/cm^3'
PM_Cn.standard_name = 'number_concentration_of_ambient_aerosol_particles_in_air' 
PM_Cn.long_name = 'Number Concentration of Ambient Aerosol Particles in air'
PM_Cn.valid_min = fidas_Dist['Cn (P/cm3)'].min()
PM_Cn.valid_max = fidas_Dist['Cn (P/cm3)'].max()
PM_Cn.call_methods = 'time:point'
PM_Cn.coordinates =  '53.456636N -2.214244E'
PM_Cn[:] = fidas_Dist['Cn (P/cm3)']

fidas_Dist['Distr_Flag'] = fidas_Dist['Distr_Flag'].astype(float)
fidas_Dist['Distr_Flag'] = fidas_Dist['Distr_Flag'].astype(int)
fidas_Dist['Distr_Flag'] = fidas_Dist['Distr_Flag'].astype(str)

qc_flag = dataset_out.createVariable('qc_flags', 'b', ('time',))
qc_flag.type = 'byte'
qc_flag.dimension = 'time'
qc_flag.units = '1'
qc_flag.long_name = 'Data Quality flag' 
qc_flag.flag_values ='0b,1b,2b,3b' 
qc_flag.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'
Flag_fidas_Byte = np.array(fidas_Dist['Distr_Flag']).astype(np.ubyte)
qc_flag[:] = Flag_fidas_Byte


dataset_out.close()
