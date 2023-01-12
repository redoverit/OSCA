

import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date
import datetime

#def check_times(allFiles):
direct = str(ACSM_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

today = date.today()
current_month = today.strftime("%B %Y")
first_month_studied = start.strftime("%B %Y")
last_month_studied = end.strftime("%B %Y")
months_studied = np.where(first_month_studied == last_month_studied, first_month_studied, str(first_month_studied) + ' till ' + str(last_month_studied))
print(months_studied)

if int(date_file_label) < 201909:
    sys.exit("Error Message: This program cannot be used for data prior to September 2019.")
else:
    pass

dataset_out = nc.Dataset(direct + 'ACSM_maqs_' + str(date_file_label) + '_non-refractory-aerosol-composition' + str(status) + str(version_number) + '.1.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.1'
dataset_out.source = 'maqs-acsm-1'
dataset_out.instrument_manufacturer = 'Colossal'
dataset_out.instrument_model = 'Aerosol Chemical Speciation Monitor (ACSM)'
dataset_out.instrument_serial_number = '140221.000'
dataset_out.instrument_software = 'Igor Pro'
dataset_out.instrument_software_version = '7.04'
dataset_out.data_visualisation_software = 'ACSM_local'
dataset_out.data_visualisation_software_version = '1.6.1.0'
dataset_out.creator_name = 'Dr Nathan Watson'
dataset_out.creator_email = 'nathan.watson@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-9096-0926'
dataset_out.institution = 'University of Manchester'
dataset_out.processing_software_url = 'https://github.com/redoverit/OSCA/'
dataset_out.processing_software_version = str(version_number) + '.1'
dataset_out.calibration_sensitivity = 'not known'
dataset_out.calibration_certification_url = 'N/A'
dataset_out.sampling_interval = 'Usually 29 mins and 17 seconds'
dataset_out.averaging_interval = 'Usually 29 mins and 17 seconds'
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
dataset_out.title = 'Non-refractory (Ammonium, Sulphate, Chloride, Organic & Nitrate) composition of Tropospheric Aerosols'
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
times.valid_min = ACSM_Data['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = ACSM_Data['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
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
day_of_year.valid_min = ACSM_Data['day_year'].min()
day_of_year.valid_max = ACSM_Data['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = ACSM_Data['year'].min()
year.valid_max = ACSM_Data['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = ACSM_Data['month'].min()
month.valid_max = ACSM_Data['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = ACSM_Data['day'].min()
day.valid_max = ACSM_Data['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = ACSM_Data['hour'].min()
hour.valid_max = ACSM_Data['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = ACSM_Data['minute'].min()
minute.valid_max = ACSM_Data['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = ACSM_Data['second'].min()
second.valid_max = ACSM_Data['second'].max()


NO3 = dataset_out.createVariable('mass_concentration_of_nitrate_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
NO3.type = 'float32'
NO3.dimension = 'time' 
NO3.units ='ug m-3'
NO3.standard_name = 'mass_concentration_of_nitrate_in_ambient_aerosol_particles_in_air' 
NO3.long_name = 'Mass concentration of the NO3 component of ambient aerosol particles in air'
NO3.valid_min = ACSM_Data['NO3 (ug/m3)'].min()
NO3.valid_max = ACSM_Data['NO3 (ug/m3)'].max()
NO3.call_methods = 'time:point'
NO3.coordinates =  '53.456636N -2.214244E'
NO3.chemical_species = 'NO3'

qc_flag_NO3 = dataset_out.createVariable('qc_flag_mass_concentration_of_nitrate_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag_NO3.type = 'byte'
qc_flag_NO3.units = '1'
qc_flag_NO3.long_name = 'Data Quality flag: NO3' 
qc_flag_NO3.flag_values ='0b,1b,2b,3b' 
qc_flag_NO3.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

SO4 = dataset_out.createVariable('mass_concentration_of_sulfate_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
SO4.type = 'float32'
SO4.dimension = 'time' 
SO4.units ='ug m-3'
SO4.standard_name = 'mass_concentration_of_sulfate_in_ambient_aerosol_particles_in_air' 
SO4.long_name = 'Mass concentration of the SO4 component of ambient aerosol particles in air'
SO4.valid_min = ACSM_Data['SO4 (ug/m3)'].min()
SO4.valid_max = ACSM_Data['SO4 (ug/m3)'].max()
SO4.call_methods = 'time:point'
SO4.coordinates =  '53.456636N -2.214244E'
SO4.chemical_species = 'SO4'

qc_flag_SO4 = dataset_out.createVariable('qc_flag_mass_concentration_of_sulfate_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag_SO4.type = 'byte'
qc_flag_SO4.units = '1'
qc_flag_SO4.long_name = 'Data Quality flag: SO4' 
qc_flag_SO4.flag_values ='0b,1b,2b,3b' 
qc_flag_SO4.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

NH4 = dataset_out.createVariable('mass_concentration_of_ammonia_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
NH4.type = 'float32'
NH4.dimension = 'time' 
NH4.units ='ug m-3'
NH4.standard_name = 'mass_concentration_of_ammonia_in_ambient_aerosol_particles_in_air' 
NH4.long_name = 'Mass concentration of the NH4 component of ambient aerosol particles in air'
NH4.valid_min = ACSM_Data['NH4 (ug/m3)'].min()
NH4.valid_max = ACSM_Data['NH4 (ug/m3)'].max()
NH4.call_methods = 'time:point'
NH4.coordinates =  '53.456636N -2.214244E'
NH4.chemical_species = 'NH4'

qc_flag_NH4 = dataset_out.createVariable('qc_flag_mass_concentration_of_ammonia_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag_NH4.type = 'byte'
qc_flag_NH4.units = '1'
qc_flag_NH4.long_name = 'Data Quality flag: NH4' 
qc_flag_NH4.flag_values ='0b,1b,2b,3b' 
qc_flag_NH4.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

organic = dataset_out.createVariable('mass_concentration_of_organics_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
organic.type = 'float32'
organic.dimension = 'time' 
organic.units ='ug m-3'
organic.standard_name = 'mass_concentration_of_organics_in_ambient_aerosol_particles_in_air' 
organic.long_name = 'Mass concentration of the organic component of ambient aerosol particles in air'
organic.valid_min = ACSM_Data['organic (ug/m3)'].min()
organic.valid_max = ACSM_Data['organic (ug/m3)'].max()
organic.call_methods = 'time:point'
organic.coordinates =  '53.456636N -2.214244E'
organic.chemical_species = 'organic'

qc_flag_organic = dataset_out.createVariable('qc_flag_mass_concentration_of_organics_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag_organic.type = 'byte'
qc_flag_organic.units = '1'
qc_flag_organic.long_name = 'Data Quality flag: organics' 
qc_flag_organic.flag_values ='0b,1b,2b,3b' 
qc_flag_organic.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'


Cl = dataset_out.createVariable('mass_concentration_of_chlorides_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
Cl.type = 'float32'
Cl.dimension = 'time' 
Cl.units ='ug m-3'
Cl.standard_name = 'mass_concentration_of_chlorides_in_ambient_aerosol_particles_in_air' 
Cl.long_name = 'Mass concentration of the Chl component of ambient aerosol particles in air'
Cl.valid_min = ACSM_Data['Chl (ug/m3)'].min()
Cl.valid_max = ACSM_Data['Chl (ug/m3)'].max()
Cl.call_methods = 'time:point'
Cl.coordinates =  '53.456636N -2.214244E'
Cl.chemical_species = 'Cl'

qc_flag_Cl = dataset_out.createVariable('qc_flag_mass_concentration_of_chlorides_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag_Cl.type = 'byte'
qc_flag_Cl.units = '1'
qc_flag_Cl.long_name = 'Data Quality flag: Chl' 
qc_flag_Cl.flag_values ='0b,1b,2b,3b' 
qc_flag_Cl.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

# this bit writes the data from the master dataframe to the variables
times[:] = ACSM_Data['TimeSecondsSince'].values #nc.date2num(timeline[:],times.units)
day_of_year[:] = ACSM_Data['day_year'].values
year[:] = ACSM_Data['year'].values
month[:] = ACSM_Data['month'].values
day[:] = ACSM_Data['day'].values
hour[:] = ACSM_Data['hour'].values
minute[:] = ACSM_Data['minute'].values
second[:] = ACSM_Data['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244
NO3[:] = ACSM_Data['NO3 (ug/m3)'].values
Flag_NO3_Byte = np.array(ACSM_Data['qc_Flag_NO3']).astype(np.ubyte)
qc_flag_NO3[:] = Flag_NO3_Byte
SO4[:] = ACSM_Data['SO4 (ug/m3)'].values
Flag_SO4_Byte = np.array(ACSM_Data['qc_Flag_SO4']).astype(np.ubyte)
qc_flag_SO4[:] = Flag_SO4_Byte
NH4[:] = ACSM_Data['NH4 (ug/m3)'].values
Flag_NH4_Byte = np.array(ACSM_Data['qc_Flag_NH4']).astype(np.ubyte)
qc_flag_NH4[:] = Flag_NH4_Byte
organic[:] = ACSM_Data['organic (ug/m3)'].values
Flag_organic_Byte = np.array(ACSM_Data['qc_Flag_organic']).astype(np.ubyte)
qc_flag_organic[:] = Flag_organic_Byte
Cl[:] = ACSM_Data['Chl (ug/m3)'].values
Flag_Cl_Byte = np.array(ACSM_Data['qc_Flag_Chl']).astype(np.ubyte)
qc_flag_Cl[:] = Flag_Cl_Byte

dataset_out.close()
