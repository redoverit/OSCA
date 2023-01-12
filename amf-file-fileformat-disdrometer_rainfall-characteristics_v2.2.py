

import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date
import datetime
import os


#def check_times(allFiles):
version_number = 'v2.2' #version of the code
direct = str(Distrometer_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

today = date.today()
current_month = today.strftime("%B %Y")
month_studied = start.strftime("%B %Y")

print(str(month_studied))

if float(start_year_month_str) < 201907:
    sys.exit("Error Message: This program cannot be used for data prior to July 2019.")
else:
    pass

dataset_out = nc.Dataset(direct + 'laser-precipitation-monitor_maqs_' + str(date_file_label) + '_precipitation' + str(status) + str(version_number) + '.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.1'
dataset_out.source = 'maqs-disdrometer' 
dataset_out.instrument_manufacturer = 'Thies Clima'
dataset_out.instrument_model = 'Laser Precipitation Monitor 5.4110.00.000'
dataset_out.instrument_serial_number = '2448'
dataset_out.instrument_software = 'LNM-View (9.1700.99.000)'
dataset_out.instrument_software_version = '2.6'
dataset_out.creator_name = 'Dr Nathan Watson'
dataset_out.creator_email = 'nathan.watson@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-9096-0926'
dataset_out.institution = 'University of Manchester'
dataset_out.processing_software_url = 'https://github.com/redoverit/OSCA/'
dataset_out.processing_software_version = str(version_number)
dataset_out.calibration_sensitivity = 'not known'
dataset_out.calibration_certification_url = 'not known'
dataset_out.sampling_interval = '1 minute' #confirmed
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
dataset_out.title = 'Rainfall Rate and Velocity'
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
diameter_dim = dataset_out.createDimension('diameter',22)
fallspeed_dim = dataset_out.createDimension('fallspeed',20)
diameter_higher_dim = dataset_out.createDimension('diameter_channel_higher_limit',22)
fallspeed_higher_dim = dataset_out.createDimension('fallspeed_channel_higher_limit',20)


# create variables (empty to begin with)

times = dataset_out.createVariable('time', np.float64, ('time',))
times.type = 'float64'
times.units = 'seconds since 1970-01-01T00:00:00'
times.long_name = 'Time (seconds since 1970-01-01 00:00:00)'
times.axis = 'T'
times.valid_min = distrometer_Data['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = distrometer_Data['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
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
day_of_year.valid_min = distrometer_Data['day_year'].min()
day_of_year.valid_max = distrometer_Data['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = distrometer_Data['year'].min()
year.valid_max = distrometer_Data['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = distrometer_Data['month'].min()
month.valid_max = distrometer_Data['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = distrometer_Data['day'].min()
day.valid_max = distrometer_Data['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = distrometer_Data['hour'].min()
hour.valid_max = distrometer_Data['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = distrometer_Data['minute'].min()
minute.valid_max = distrometer_Data['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = distrometer_Data['second'].min()
second.valid_max = distrometer_Data['second'].max()

times[:] = distrometer_Data['TimeSecondsSince'].values
day_of_year[:] = distrometer_Data['day_year'].values
year[:] = distrometer_Data['year'].values
month[:] = distrometer_Data['month'].values
day[:] = distrometer_Data['day'].values
hour[:] = distrometer_Data['hour'].values
minute[:] = distrometer_Data['minute'].values
second[:] = distrometer_Data['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244


diameter = dataset_out.createVariable('diameter', np.float32, ('diameter',))
diameter.type = 'float32'
diameter.dimension = 'diameter'
diameter.units = 'mm'
diameter.standard_name = 'diameter_channel_lower_limit'
diameter.long_name = 'The Lower Limit for Each Diameter Class'
diameter.valid_min = 0
diameter.valid_max = rainfall_labels['all_diameter_classes'].max()
diameter.coordinates =  '53.456636N -2.214244E'
diameter[:] = rainfall_labels['all_diameter_classes']


diameter_channel_higher_limit = dataset_out.createVariable('diameter_channel_higher_limit', np.float32, ('diameter_channel_higher_limit',))
diameter_channel_higher_limit.type = 'float32'
diameter_channel_higher_limit.dimension = 'diameter_channel_higher_limit'
diameter_channel_higher_limit.units = 'mm'
diameter_channel_higher_limit.standard_name = 'diameter_channel_higher_limit'
diameter_channel_higher_limit.long_name = 'The Upper Limit for Each Diameter Class'
diameter_channel_higher_limit.valid_min = distribution_labels['upper diameter channel limit'].min()
diameter_channel_higher_limit.valid_max = distribution_labels['upper diameter channel limit'].max()
diameter_channel_higher_limit.coordinates =  '53.456636N -2.214244E'
diameter_channel_higher_limit[:] = distribution_labels['upper diameter channel limit']


fallspeed = dataset_out.createVariable('fallspeed', np.float32, ('fallspeed',))
fallspeed.type = 'float32'
fallspeed.dimension = 'fallspeed'
fallspeed.units = 'm s-1'
fallspeed.standard_name = 'fallspeed_channel_lower_limit'
fallspeed.long_name = 'fallspeed'
fallspeed.valid_min = 0
fallspeed.valid_max = speed_labels['all_speed_classes'].max()
fallspeed.coordinates =  '53.456636N -2.214244E'
fallspeed[:] = speed_labels['all_speed_classes']


fallspeed_channel_higher_limit = dataset_out.createVariable('fallspeed_channel_higher_limit', np.float32, ('fallspeed_channel_higher_limit',))
fallspeed_channel_higher_limit.type = 'float32'
fallspeed_channel_higher_limit.dimension = 'fallspeed_channel_higher_limit'
fallspeed_channel_higher_limit.units = 'mm'
fallspeed_channel_higher_limit.standard_name = 'fallspeed_channel_higher_limit'
fallspeed_channel_higher_limit.long_name = 'The Upper Limit for Each fallspeed Class'
fallspeed_channel_higher_limit.valid_min = speed_labels['upper speed channel limit'].min()
fallspeed_channel_higher_limit.valid_max = speed_labels['upper speed channel limit'].max()
fallspeed_channel_higher_limit.coordinates =  '53.456636N -2.214244E'
fallspeed_channel_higher_limit[:] = speed_labels['upper speed channel limit']

number_of_hydrometeors = dataset_out.createVariable('number_of_hydrometeors', np.float32, ('time','fallspeed','diameter'), fill_value=-1.00E+20)
number_of_hydrometeors.type = 'float32'
number_of_hydrometeors.dimension = 'time' 
number_of_hydrometeors.practical_units ='##cc'
number_of_hydrometeors.standard_name = 'number_of_hydrometeors' 
number_of_hydrometeors.long_name = 'Number of Hydrometeors Detected'
number_of_hydrometeors.valid_min = ((distrometer_Distribution.iloc[:,0:440].min()).min()) # distrometer_Data[:].min()
number_of_hydrometeors.valid_max = ((distrometer_Distribution.iloc[:,0:440].max()).max()) #distrometer_Data[:].max()
number_of_hydrometeors.call_methods = 'time:mean'
number_of_hydrometeors.coordinates =  '53.456636N -2.214244E'
number_of_hydrometeors[:] = distrometer_Distribution.iloc[:,0:440]
print()
print()

fallspeed_distribution = dataset_out.createVariable('fallspeed_distribution', np.float32, ('time','fallspeed'), fill_value=-1.00E+20)
fallspeed_distribution.type = 'float32'
fallspeed_distribution.dimension = 'time' 
fallspeed_distribution.practical_units ='##cc'
fallspeed_distribution.standard_name = 'fallspeed_distribution' 
fallspeed_distribution.long_name = 'Distribution of Hydrometeor Fallspeeds'
fallspeed_distribution.valid_min = (rainfall_speed_distribution[:].min()).min()
fallspeed_distribution.valid_max = (rainfall_speed_distribution[:].max()).max()
fallspeed_distribution.call_methods = 'time:mean'
fallspeed_distribution.coordinates =  '53.456636N -2.214244E'
fallspeed_distribution[:] = rainfall_speed_distribution[:]
print((rainfall_speed_distribution[:].min()).min())
print((rainfall_speed_distribution[:].max()).max())

diameter_distribution = dataset_out.createVariable('diameter_distribution', np.float32, ('time','diameter'), fill_value=-1.00E+20)
diameter_distribution.type = 'float32'
diameter_distribution.dimension = 'time' 
diameter_distribution.practical_units ='1'
diameter_distribution.standard_name = 'diameter_distribution' 
diameter_distribution.long_name = 'Distribution of Hydrometeor Diameters'
diameter_distribution.valid_min = (rainfall_diameter_distribution[:].min()).min()
diameter_distribution.valid_max = (rainfall_diameter_distribution[:].max()).max()
diameter_distribution.call_methods = 'time:mean'
diameter_distribution.coordinates =  '53.456636N -2.214244E'
diameter_distribution[:] = rainfall_diameter_distribution[:]
print((rainfall_diameter_distribution[:].min()).min())
print((rainfall_diameter_distribution[:].max()).max())


rainfall_minute = dataset_out.createVariable('thickness_of_rainfall_amount', np.float32, ('time',), fill_value=-1.00E+20)
rainfall_minute.type = 'float32'
rainfall_minute.dimension = 'time' 
rainfall_minute.practical_units ='mm'
rainfall_minute.standard_name = 'thickness_of_rainfall_amount' 
rainfall_minute.long_name = 'Rain Accumulated in Averaging Period (over a Minute)'
rainfall_minute.valid_min = distrometer_Data['Rain Accumulated in one minute (mm)'].min()
rainfall_minute.valid_max = distrometer_Data['Rain Accumulated in one minute (mm)'].max()
rainfall_minute.call_methods = 'time:mean'
rainfall_minute.coordinates =  '53.456636N -2.214244E'


rainfall_rate = dataset_out.createVariable('rainfall_rate', np.float32, ('time',), fill_value=-1.00E+20)
rainfall_rate.type = 'float32'
rainfall_rate.dimension = 'time' 
rainfall_rate.practical_units ='mm hr-1'
rainfall_rate.standard_name = 'rainfall_rate' 
rainfall_rate.long_name = 'Rainfall Rate'
rainfall_rate.valid_min = distrometer_Data['Liquid Precipitation Rate (mm/hr)'].min()
rainfall_rate.valid_max = distrometer_Data['Liquid Precipitation Rate (mm/hr)'].max()
rainfall_rate.call_methods = 'time:mean'
rainfall_rate.coordinates =  '53.456636N -2.214244E'

total_precipitation = dataset_out.createVariable('total_precipitation_rate', np.float32, ('time',), fill_value=-1.00E+20)
total_precipitation.type = 'float32'
total_precipitation.dimension = 'time' 
total_precipitation.practical_units ='mm hr-1'
total_precipitation.standard_name = 'total_precipitation_rate' 
total_precipitation.long_name = 'Total Precipitation Rate'
total_precipitation.valid_min = distrometer_Data['Total Precipitation Rate (mm/hr)'].min()
total_precipitation.valid_max = distrometer_Data['Total Precipitation Rate (mm/hr)'].max()
total_precipitation.call_methods = 'time:mean'
total_precipitation.coordinates =  '53.456636N -2.214244E'

solid_precipitation = dataset_out.createVariable('solid_precipitation_rate', np.float32, ('time',), fill_value=-1.00E+20)
solid_precipitation.type = 'float32'
solid_precipitation.dimension = 'time' 
solid_precipitation.practical_units ='mm hr-1'
solid_precipitation.standard_name = 'solid_precipitation_rate' 
solid_precipitation.long_name = 'Solid Precipitation Rate'
solid_precipitation.valid_min = distrometer_Data['Solid Precipitation Rate (mm/hr)'].min()
solid_precipitation.valid_max = distrometer_Data['Solid Precipitation Rate (mm/hr)'].max()
solid_precipitation.call_methods = 'time:mean'
solid_precipitation.coordinates =  '53.456636N -2.214244E'

#hail_intensity = dataset_out.createVariable('hail_intensity', np.float32, ('time',), fill_value=-1.00E+20)
#hail_intensity.type = 'float32'
#hail_intensity.dimension = 'time' 
#hail_intensity.practical_units ='hits cm-2'
#hail_intensity.standard_name = 'hail_intensity' 
#hail_intensity.long_name = 'Hail Intensity'
#hail_intensity.valid_min = distrometer_Data['Hail Intensity (hits cm-2)'].min()
#hail_intensity.valid_max = distrometer_Data['Hail Intensity (hits cm-2)'].max()
#hail_intensity.call_methods = 'time:mean'
#hail_intensity.coordinates =  '53.456636N -2.214244E'

#hail_rate = dataset_out.createVariable('hail_intensity', np.float32, ('time',), fill_value=-1.00E+20)
#hail_rate.type = 'float32'
#hail_rate.dimension = 'time' 
#hail_rate.practical_units ='hits cm-2'
#hail_rate.standard_name = 'hail_rate' 
#hail_rate.long_name = 'Hail Rate'
#hail_rate.valid_min = distrometer_Data['Hail Rate (hits cm-2 hr-1)'].min()
#hail_rate.valid_max = distrometer_Data['Hail Rate (hits cm-2 hr-1)'].max()
#hail_rate.call_methods = 'time:mean'
#hail_rate.coordinates =  '53.456636N -2.214244E'

#hail_diameter = dataset_out.createVariable('maximum_diameter_of_hail', np.float32, ('time',), fill_value=-1.00E+20)
#hail_diameter.type = 'float32'
#hail_diameter.dimension = 'time' 
#hail_diameter.practical_units = 'mm hr-1'
#hail_diameter.standard_name = 'maximum_diameter_of_hail' 
#hail_diameter.long_name = 'Maximum Diameter of Hail'
#hail_diameter.valid_min = distrometer_Data['Maximum Diameter Hail (mm)'].min()
#hail_diameter.valid_max = distrometer_Data['Maximum Diameter Hail (mm)'].max()
#hail_diameter.call_methods = 'time:mean'
#hail_diameter.coordinates =  '53.456636N -2.214244E'

number_of_drops = dataset_out.createVariable('number_of_drops', np.float32, ('time',), fill_value=-1.00E+20)
number_of_drops.type = 'float32'
number_of_drops.dimension = 'time' 
number_of_drops.practical_units = '##cc'
number_of_drops.standard_name = 'number_of_drops' 
number_of_drops.long_name = 'Number of Pulses\Drops Counted in Integration Period'
number_of_drops.valid_min = distrometer_Data['Total No. of hydrometeors'].min()
number_of_drops.valid_max = distrometer_Data['Total No. of hydrometeors'].max()
number_of_drops.call_methods = 'time:mean'
number_of_drops.coordinates =  '53.456636N -2.214244E'

reflectivity = dataset_out.createVariable('equivalent_reflectivity_factor', np.float32, ('time',), fill_value=-1.00E+20)
reflectivity.type = 'float32'
reflectivity.dimension = 'time' 
reflectivity.practical_units ='dBZ'
reflectivity.standard_name = 'equivalent_reflectivity_factor' 
reflectivity.long_name = 'Equivalent Radar Reflectivity Factor'
reflectivity.valid_min = distrometer_Data['Radar Reflectivity (dBZ)'].min()
reflectivity.valid_max = distrometer_Data['Radar Reflectivity (dBZ)'].max()
reflectivity.call_methods = 'time:mean'
reflectivity.coordinates =  '53.456636N -2.214244E'

visibility = dataset_out.createVariable('precipitation_visibility', np.float32, ('time',), fill_value=-1.00E+20)
visibility.type = 'float32'
visibility.dimension = 'time' 
visibility.practical_units ='m'
visibility.standard_name = 'precipitation_visibility' 
visibility.long_name = 'Visibility Reduction Caused by Precipitation.'
visibility.valid_min = distrometer_Data['Visibility in precipitation (m)'].min()
visibility.valid_max = distrometer_Data['Visibility in precipitation (m)'].max()
visibility.call_methods = 'time:mean'
visibility.coordinates =  '53.456636N -2.214244E'


rainfall_minute[:] = distrometer_Data['Rain Accumulated in one minute (mm)'].values
rainfall_rate[:] = distrometer_Data['Liquid Precipitation Rate (mm/hr)'].values
total_precipitation[:] = distrometer_Data['Total Precipitation Rate (mm/hr)'].values
solid_precipitation[:] = distrometer_Data['Solid Precipitation Rate (mm/hr)'].values
#hail_intensity[:] = distrometer_Data['hail_intensity (hits cm-2)'].values
#hail_rate[:] = distrometer_Data['hail_intensity (hits cm-2 hr-1)'].values
#hail_diameter[:] = distrometer_Data['Maximum Diameter Hail (mm)'].values
number_of_drops[:] = distrometer_Data['Total No. of hydrometeors'].values
reflectivity[:] = distrometer_Data['Radar Reflectivity (dBZ)'].values
visibility[:] = distrometer_Data['Visibility in precipitation (m)'].values

qc_flag = dataset_out.createVariable('qc_flag', 'b', ('time',))
qc_flag.type = 'byte'
qc_flag.dimension = 'time'
qc_flag.units = '1'
qc_flag.long_name = 'Data Quality flag' 
qc_flag.flag_values ='0b,1b,2b,3b,4b,5b' 
qc_flag.flag_meanings = '\n\rnot_used \n\rgood \n\rinstrument_error \n\rbad_data_precipitation_rate_<_0_mm_hr-1 \n\rsuspect_data_precipitation_rate_>_300_mm_hr-1 \n\rsuspect_data_solid_precipitation_rate_>_300_mm_hr-1,'
Flag_Precipitation_Byte = np.array(distrometer_Data['qc_flag']).astype(np.ubyte)
qc_flag[:] = Flag_Precipitation_Byte



dataset_out.close()

