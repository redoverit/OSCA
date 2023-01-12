

import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date
import datetime

#def check_times(allFiles):
version_number = str(version_number) #version of the code
direct = str(TCA_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

today = date.today()
current_month = today.strftime("%B %Y")
month_studied = start.strftime("%B %Y")

print(str(start.strftime("%B")) + ' ' + str(start.strftime("%Y")))

if float(start_year_month_str) < 202202:
    sys.exit("Error Message: This program cannot be used for data prior to February 2022.")
else:
    pass

dataset_out = nc.Dataset(direct + 'TCA_maqs_' + str(date_file_label) + '_aerosol-carbon-content_' + str(validity_status) + '_' + str(version_number) + '.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.1'
dataset_out.source = 'maqs-TCA-08-1'
dataset_out.instrument_manufacturer = 'Magee Scientific'
dataset_out.instrument_model = 'Total Carbon Analyzer Model TCA 08'
dataset_out.instrument_serial_number = 'TCA08-S02-00202'
dataset_out.instrument_software = 'AE33 software'
dataset_out.instrument_software_version = '1.4.4.0'
dataset_out.creator_name = 'Dr Nathan Watson'
dataset_out.creator_email = 'nathan.watson@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-9096-0926'
dataset_out.institution = 'University of Manchester'
dataset_out.processing_software_url = 'https://github.com/redoverit/OSCA/'
dataset_out.processing_software_version = str(version_number)
dataset_out.calibration_sensitivity = 'not known'
dataset_out.calibration_certification_url = 'none'
dataset_out.sampling_interval = '60 minute'
dataset_out.averaging_interval = '60 minute'
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
dataset_out.title = 'Total Carbon Content of Ambient Aerosols'
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


# create variables (empty to begin with)

times = dataset_out.createVariable('time', np.float64, ('time',))
times.type = 'float64'
times.units = 'seconds since 1970-01-01T00:00:00'
times.long_name = 'Time (seconds since 1970-01-01 00:00:00)'
times.axis = 'T'
times.valid_min = TCA_Data['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = TCA_Data['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
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
day_of_year.valid_min = TCA_Data['day_year'].min()
day_of_year.valid_max = TCA_Data['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = TCA_Data['year'].min()
year.valid_max = TCA_Data['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = TCA_Data['month'].min()
month.valid_max = TCA_Data['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = TCA_Data['day'].min()
day.valid_max = TCA_Data['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = TCA_Data['hour'].min()
hour.valid_max = TCA_Data['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = TCA_Data['minute'].min()
minute.valid_max = TCA_Data['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = TCA_Data['second'].min()
second.valid_max = TCA_Data['second'].max()

Total_Carbon = dataset_out.createVariable('total_mass_concentration_of_carbon_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
Total_Carbon.type = 'float32'
Total_Carbon.dimension = 'time' 
Total_Carbon.practical_units ='ug m-3'
Total_Carbon.standard_name = 'total_mass_concentration_of_carbon_in_ambient_aerosol_particles_in_air' 
Total_Carbon.long_name = 'Total Mass concentration of the Carbon component of Ambient Aerosol Particles in Air'
Total_Carbon.valid_min = TCA_Data['Total Carbon (ug/m3)'].min()
Total_Carbon.valid_max = TCA_Data['Total Carbon (ug/m3)'].max()
Total_Carbon.call_methods = 'time:mean'
Total_Carbon.coordinates =  '53.456636N -2.214244E'
Total_Carbon.chemical_species = 'TC'

qc_Flag_TC = dataset_out.createVariable('qc_flag_total_mass_concentration_of_carbon_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_Flag_TC.type = 'byte'
qc_Flag_TC.dimension = 'time'
qc_Flag_TC.units = '1'
qc_Flag_TC.long_name = 'Data Quality flag for Total Aerosol Content Carbon' 
qc_Flag_TC.flag_values ='0b,1b,2b,3b' 
qc_Flag_TC.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

Organic_Carbon = dataset_out.createVariable('mass_concentration_of_organic_carbon_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
Organic_Carbon.type = 'float32'
Organic_Carbon.dimension = 'time' 
Organic_Carbon.practical_units ='ug m-3'
Organic_Carbon.standard_name = 'mass_concentration_of_organic_carbon_in_ambient_aerosol_particles_in_air' 
Organic_Carbon.long_name = 'Mass concentration of the Organic Carbon component of Ambient Aerosol Particles in Air'
Organic_Carbon.valid_min = TCA_Data['Organic Carbon (ug/m3)'].min()
Organic_Carbon.valid_max = TCA_Data['Organic Carbon (ug/m3)'].max()
Organic_Carbon.call_methods = 'time:mean'
Organic_Carbon.coordinates =  '53.456636N -2.214244E'
Organic_Carbon.chemical_species = 'TC'

qc_Flag_OC = dataset_out.createVariable('qc_flag_mass_concentration_of_organic_carbon_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_Flag_OC.type = 'byte'
qc_Flag_OC.dimension = 'time'
qc_Flag_OC.units = '1'
qc_Flag_OC.long_name = 'Organic Carbon Aerosol Content - Data Quality flag' 
qc_Flag_OC.flag_values ='0b,1b,2b,3b' 
qc_Flag_OC.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

Elemental_Carbon = dataset_out.createVariable('mass_concentration_of_elemental_carbon_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
Elemental_Carbon.type = 'float32'
Elemental_Carbon.dimension = 'time' 
Elemental_Carbon.practical_units ='ug m-3'
Elemental_Carbon.standard_name = 'mass_concentration_of_elemental_carbon_in_ambient_aerosol_particles_in_air' 
Elemental_Carbon.long_name = 'Mass concentration of the Elemental Carbon component of Ambient Aerosol Particles in Air'
Elemental_Carbon.valid_min = TCA_Data['Elemental Carbon (ug/m3)'].min()
Elemental_Carbon.valid_max = TCA_Data['Elemental Carbon (ug/m3)'].max()
Elemental_Carbon.call_methods = 'time:mean'
Elemental_Carbon.coordinates =  '53.456636N -2.214244E'
Elemental_Carbon.chemical_species = 'EC'

qc_Flag_EC = dataset_out.createVariable('qc_flag_mass_concentration_of_elemental_carbon_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_Flag_EC.type = 'byte'
qc_Flag_EC.dimension = 'time'
qc_Flag_EC.units = '1'
qc_Flag_EC.long_name = 'Elemental Carbon Aerosol Content - Data Quality flag' 
qc_Flag_EC.flag_values ='0b,1b,2b,3b' 
qc_Flag_EC.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'


#Average_CO2 = dataset_out.createVariable('mole_fraction_of_carbon_dioxide_in_air', np.float32, ('time',), fill_value=-1.00E+20)
#Average_CO2.type = 'float32'
#Average_CO2.dimension = 'time' 
#Average_CO2.units ='ppm'
#Average_CO2.standard_name = 'mole_fraction_of_carbon_dioxide_in_air'
#Average_CO2.long_name = 'Molar Fraction of Carbon Dioxide in air'
#Average_CO2.valid_min = TCA_Data['CO2 (ppm)'].min()
#Average_CO2.valid_max = TCA_Data['CO2 (ppm)'].max()
#Average_CO2.call_methods = 'time:mean'
#Average_CO2.coordinates =  '53.456636N, -2.214244E'
#Average_CO2.chemical_species = 'CO2'

#qc_Flag_CO2 = dataset_out.createVariable('qc_flag_mole_fraction_of_carbon_dioxide_in_air', 'b', ('time',))
#qc_Flag_CO2.type = 'byte'
#qc_Flag_CO2.units = '1'
#qc_Flag_CO2.long_name = 'Carbon Dioxide Data Quality flag' 
#qc_Flag_CO2.flag_values ='0b,1b,2b,3b,4b' #'0b,1b,2b,3b'
#qc_Flag_CO2.flag_meanings = '\n\rnot_used \n\rgood \n\rbad \n\rsuspect \n\rlocal_unusual_activity,' #'\n\rnot_used \n\rgood_data \n\rsuspect_data_data_not_quality_controlled \n\rbad_data_do_not_use ,'

# this bit writes the data from the master dataframe to the variables
times[:] = TCA_Data['TimeSecondsSince'].values#nc.date2num(timeline[:],times.units)
day_of_year[:] = TCA_Data['day_year'].values
year[:] = TCA_Data['year'].values
month[:] = TCA_Data['month'].values
day[:] = TCA_Data['day'].values
hour[:] = TCA_Data['hour'].values
minute[:] = TCA_Data['minute'].values
second[:] = TCA_Data['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244
Total_Carbon[:] = TCA_Data['Total Carbon (ug/m3)']
Organic_Carbon[:] = TCA_Data['Organic Carbon (ug/m3)']
Elemental_Carbon[:] = TCA_Data['Elemental Carbon (ug/m3)']
Flag_TC_Byte = np.array(TCA_Data['qc_Flag_TC']).astype(np.ubyte)
qc_Flag_TC[:] = Flag_TC_Byte
Flag_OC_Byte = np.array(TCA_Data['qc_Flag_OC']).astype(np.ubyte)
qc_Flag_OC[:] = Flag_OC_Byte
Flag_EC_Byte = np.array(TCA_Data['qc_Flag_EC']).astype(np.ubyte)
qc_Flag_EC[:] = Flag_EC_Byte
#Average_CO2[:] = TCA_Data['CO2 (ppm)']
#Flag_CO2_Byte = np.array(TCA_Data['qc_Flag_CO2']).astype(np.ubyte)
#qc_Flag_CO2[:] = Flag_CO2_Byte


dataset_out.close()

