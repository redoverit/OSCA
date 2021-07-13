

import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np

#def check_times(allFiles):
version_number = 'v1.0'
direct = 'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

dataset_out = nc.Dataset(direct + 'sonic_MAQS_201909_mean_winds.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.0'
dataset_out.source = 'MAQS-sonic-1'
dataset_out.instrument_manufacturer = 'Gill'
dataset_out.instrument_model = 'Windmaster'
dataset_out.instrument_serial_number = '180602'
dataset_out.instrument_software = 'Labview'
#dataset_out.operational_software_version = getattr(dataset_in, 'software_version')
dataset_out.creator_name = 'Dr Nicholas Marsden'
dataset_out.creator_email = 'nicholas.marsden@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-6242-929X'
dataset_out.institution = 'University of Manchester'
#dataset_out.processing_software_url = 'xyz_github_xyz'
dataset_out.processing_software_version = 'v2.0'
#dataset_out.calibration_sensitivity = 
#dataset_out.calibration_certification_url = '*link to pdf*'
dataset_out.averaging_interval = '1 minute'
dataset_out.product_version = version_number
dataset_out.processing_level = '3'
#dataset_out.last_revised_date = current_time_string
dataset_out.licence = 'Data usage licence - UK Government Open Licence agreement: http://www.nationalarchives.gov.uk/doc/open-government-licence'
dataset_out.acknowledgement = 'Acknowledgement of NERC +OSCA as the data provider is required whenever and wherever this data is used'
dataset_out.platform = 'Manchester Air Quality Supersite (MAQS)'
dataset_out.platform_type = 'stationary_platform'
dataset_out.title = 'Wind speed and direction'
dataset_out.featureType = 'timeSeries'
dataset_out.time_coverage_start = start.strftime('%Y-%m-%d %H:%M:%S')
dataset_out.time_coverage_end = end.strftime('%Y-%m-%d %H:%M:%S')
dataset_out.geospatial_bounds = '53.456636N, -2.214244E'
dataset_out.platform_altitude = '50 m'
dataset_out.location_keywords = 'MAQS, Supersite, Firs, Fallowfield'
#dataset_out.amf_vocabularies_release = 'https://github.com/ncasuk/AMF_CVs/releases/tag/v1.0.0'
dataset_out.history = ' Acquired Sept 2019, Data processed Feb2021'
dataset_out.comment = 'Measurement Height 7m above ground level'


# Dimensions
time_dim = dataset_out.createDimension('time',None)

# create variables (empty to begin with)

times = dataset_out.createVariable('time', np.float64, ('time',), fill_value=-1.00E+20)
times.type = 'float64'
times.dimension = 'time'
times.units = 'seconds since 1970-01-01 00:00:00 UTC'
times.standard_name = 'time'
times.axis = 'T'
times.valid_min = sonic_Data['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = sonic_Data['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.calendar = 'standard'

WindSp = dataset_out.createVariable('wind_speed', np.float32, ('time',), fill_value=-1.00E+20)
WindSp.type = 'float32'
WindSp.dimension = 'time'
WindSp.units ='ms-1'
WindSp.standard_name = 'wind_speed'
WindSp.long_name = 'Mean Wind Speed'
#WindSp.valid_min = '0'
#WindSp.valid_max = 'NA'
WindSp.call_methods = 'time:mean'
#WindSp.coordinates =  lat_lon_string

qc_flag_WindSp = dataset_out.createVariable('qc_flag_wind_Speed', np.float32, ('time',), fill_value=3)
qc_flag_WindSp.type = 'float32'
qc_flag_WindSp.dimension = 'time'
qc_flag_WindSp.units = 'units'
qc_flag_WindSp.long_name = 'Data Quality flag: Wind Speed' 
qc_flag_WindSp.flag_values ='1,2,3,4' 
qc_flag_WindSp.flag_meanings = 'good,bad,suspect,local_unusual_activity,'

MaxWindSp = dataset_out.createVariable('wind_speed_of_gust', np.float32, ('time',), fill_value=-1.00E+20)
MaxWindSp.type = 'float32'
MaxWindSp.dimension = 'time'
MaxWindSp.units ='ms-1'
MaxWindSp.standard_name = 'wind_speed_of_gust'
MaxWindSp.long_name = 'Maximum Wind Speed Observed in Averaging period'
#MaxWindSp.valid_min = '0'
#MaxWindSp.valid_max = 'NA'
MaxWindSp.call_methods = 'time:maximum'
#MaxWindSp.coordinates =  lat_lon_string

WindDir = dataset_out.createVariable('wind_from_direction', np.float32, ('time',), fill_value=-1.00E+20)
WindDir.type = 'float32'
WindDir.dimension = 'time'
WindDir.units ='degree'
WindDir.standard_name = 'wind_from_direction'
WindDir.long_name = 'Wind Direction'
#WindDir.valid_max = '360'
#WindDir.call_methods = 'time:mean'
#WindDir.coordinates =  lat_lon_string

qc_flag_WindDir = dataset_out.createVariable('qc_flag_wind_direction', np.float32, ('time',), fill_value=3)
qc_flag_WindDir.type = 'float32'
qc_flag_WindDir.dimension = 'time'
qc_flag_WindDir.units = 'units'
qc_flag_WindDir.long_name = 'Wind Direction flags' 
qc_flag_WindDir.flag_values ='1,2,3,4' 
qc_flag_WindDir.flag_meanings = 'good,bad/missing,suspect,local_unusual_activity,'


# this bit writes the data fporm the master datafram to the variables
times[:] = sonic_Data['TimeSecondsSince'].values#nc.date2num(timeline[:],times.units)
WindSp[:] = sonic_Data['wind_Sp (m/s)'].values
MaxWindSp[:] = sonic_Data['max_Gust'].values
qc_flag_WindSp[:] = sonic_Data['qc_Flags'].values
WindDir[:] = sonic_Data['wind_Dr'].values
qc_flag_WindDir[:] = sonic_Data['qc_Flags'].values


dataset_out.close()
