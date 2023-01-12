

import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date
import datetime

#def check_times(allFiles):
version_number = 'v2.1'
direct = str(XACT_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

today = date.today()
current_month = today.strftime("%B %Y")
first_month_studied = start.strftime("%B %Y")
last_month_studied = end.strftime("%B %Y")
months_studied = np.where(first_month_studied == last_month_studied, first_month_studied, str(first_month_studied) + ' till ' + str(last_month_studied))
print(months_studied)

if int(start_year_month_str) > 202011:
    pass
else:
    sys.exit("Error Message: This program cannot be used for data prior to December 2020. Use program for PM10 only")

dataset_out = nc.Dataset(direct + 'XACT-625i_maqs_' + str(date_file_label) + '_elemental-composition-of-pm2p5-aerosols' + str(status) + str(version_number) + '.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.1'
dataset_out.source = 'maqs-XACT_625i-1'
dataset_out.instrument_manufacturer = 'Cooper Environmental Services'
dataset_out.instrument_model = 'Xact 625i Ambient Metals Monitor'
dataset_out.instrument_serial_number = '626-00-171201H'
dataset_out.instrument_software = 'Automated Data Analysis & Plotting Toolset (ADAPT)'
dataset_out.instrument_software_version = 'not known'
dataset_out.creator_name = 'Dr Nathan Watson'
dataset_out.creator_email = 'nathan.watson@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-9096-0926'
dataset_out.institution = 'University of Manchester'
dataset_out.processing_software_url = 'https://github.com/redoverit/OSCA/'
dataset_out.processing_software_version = str(version_number)
dataset_out.calibration_sensitivity = 'not known'
dataset_out.calibration_certification_url = 'not known'
dataset_out.sampling_interval = '2 hour'
dataset_out.averaging_interval = '2 hour'
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
dataset_out.title = 'Metal Concentrations in PM10 and PM2.5 Ambient Aerosol Particles in Air'
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
times.valid_min = xact_PM2p5_csv['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = xact_PM2p5_csv['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
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
day_of_year.valid_min = xact_PM2p5_csv['day_year'].min()
day_of_year.valid_max = xact_PM2p5_csv['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = xact_PM2p5_csv['year'].min()
year.valid_max = xact_PM2p5_csv['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = xact_PM2p5_csv['month'].min()
month.valid_max = xact_PM2p5_csv['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = xact_PM2p5_csv['day'].min()
day.valid_max = xact_PM2p5_csv['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = xact_PM2p5_csv['hour'].min()
hour.valid_max = xact_PM2p5_csv['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = xact_PM2p5_csv['minute'].min()
minute.valid_max = xact_PM2p5_csv['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = xact_PM2p5_csv['second'].min()
second.valid_max = xact_PM2p5_csv['second'].max()


Ag_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Ag_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Ag_PM2p5.type = 'float32'
Ag_PM2p5.dimension = 'time' 
Ag_PM2p5.units ='ug m-3'
Ag_PM2p5.standard_name = 'mass_concentration_of_ag_in_pm2p5_ambient_aerosol_particles_in_air'
Ag_PM2p5.long_name = 'Mass concentration of the Silver component in PM2.5 ambient aerosol particles in air'
Ag_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Ag 47 (ug/m3)'].min()
Ag_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Ag 47 (ug/m3)'].max()
Ag_PM2p5.call_methods = 'time:mean'
Ag_PM2p5.coordinates =  '53.456636N, -2.214244E'
Ag_PM2p5.chemical_species = 'Ag_PM2.5'


qc_flag_Ag_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Ag_PM2p5', 'b', ('time',))
qc_flag_Ag_PM2p5.type = 'byte'
qc_flag_Ag_PM2p5.units = '1'
qc_flag_Ag_PM2p5.long_name = 'Data Quality flag: Ag_PM2.5'
qc_flag_Ag_PM2p5.flag_values ='0b,1b,2b,3b' #'0b,1b,2b,3b'
qc_flag_Ag_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' #'\n\rnot_used \n\rgood_data \n\rsuspect_data_data_not_quality_controlled \n\rbad_data_do_not_use ,'

Ag_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Ag_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Ag_Uncert_PM2p5.type = 'float32'
Ag_Uncert_PM2p5.dimension = 'time' 
Ag_Uncert_PM2p5.units ='ug m-3'
Ag_Uncert_PM2p5.standard_name = 'uncertainty_of_ag_in_pm2p5_ambient_aerosol_particles_in_air'
Ag_Uncert_PM2p5.long_name = 'Uncertainty of the Silver component in PM2.5 ambient aerosol particles in air'
Ag_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Ag Uncert (ug/m3)'].min()
Ag_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Ag Uncert (ug/m3)'].max()
Ag_Uncert_PM2p5.call_methods = 'time:mean'

Al_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Al_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Al_PM2p5.type = 'float32'
Al_PM2p5.dimension = 'time' 
Al_PM2p5.units ='ug m-3'
Al_PM2p5.standard_name = 'mass_concentration_of_al_in_pm2p5_ambient_aerosol_particles_in_air'
Al_PM2p5.long_name = 'Mass concentration of the Aluminium component in PM2.5 ambient aerosol particles in air'
Al_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Al 13 (ug/m3)'].min()
Al_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Al 13 (ug/m3)'].max()
Al_PM2p5.call_methods = 'time:mean'
Al_PM2p5.coordinates =  '53.456636N, -2.214244E'
Al_PM2p5.chemical_species = 'Al_PM2.5'

qc_flag_Al_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Al_PM2p5', 'b', ('time',))
qc_flag_Al_PM2p5.type = 'byte'
qc_flag_Al_PM2p5.units = '1'
qc_flag_Al_PM2p5.long_name = 'Data Quality flag: Al_PM2.5'
qc_flag_Al_PM2p5.flag_values ='0b,1b,2b,3b' #'0b,1b,2b,3b'
qc_flag_Al_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' #'\n\rnot_used \n\rgood_data \n\rsuspect_data_data_not_quality_controlled \n\rbad_data_do_not_use ,'


Al_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Al_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Al_Uncert_PM2p5.type = 'float32'
Al_Uncert_PM2p5.dimension = 'time' 
Al_Uncert_PM2p5.units ='ug m-3'
Al_Uncert_PM2p5.standard_name = 'uncertainty_of_Al_in_pm2p5_ambient_aerosol_particles_in_air'
Al_Uncert_PM2p5.long_name = 'Uncertainty of the Aluminium component in PM2.5 ambient aerosol particles in air'
Al_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Al Uncert (ug/m3)'].min()
Al_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Al Uncert (ug/m3)'].max()
Al_Uncert_PM2p5.call_methods = 'time:mean'

As_PM2p5 = dataset_out.createVariable('Mass_Conc_of_As_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
As_PM2p5.type = 'float32'
As_PM2p5.dimension = 'time' 
As_PM2p5.units ='ug m-3'
As_PM2p5.standard_name = 'mass_concentration_of_as_in_pm2p5_ambient_aerosol_particles_in_air'
As_PM2p5.long_name = 'Mass concentration of the Arsenic component in PM2.5 ambient aerosol particles in air'
As_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_As 33 (ug/m3)'].min()
As_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_As 33 (ug/m3)'].max()
As_PM2p5.call_methods = 'time:mean'
As_PM2p5.coordinates =  '53.456636N, -2.214244E'
As_PM2p5.chemical_species = 'As_PM2.5'

qc_flag_As_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_As_PM2p5', 'b', ('time',))
qc_flag_As_PM2p5.type = 'byte'
qc_flag_As_PM2p5.units = '1'
qc_flag_As_PM2p5.long_name = 'Data Quality flag: As_PM2.5'
qc_flag_As_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_As_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' #'\n\rnot_used \n\rgood_data \n\rsuspect_data_data_not_quality_controlled \n\rbad_data_do_not_use ,'


As_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_As_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
As_Uncert_PM2p5.type = 'float32'
As_Uncert_PM2p5.dimension = 'time' 
As_Uncert_PM2p5.units ='ug m-3'
As_Uncert_PM2p5.standard_name = 'uncertainty_of_As_in_pm2p5_ambient_aerosol_particles_in_air'
As_Uncert_PM2p5.long_name = 'Uncertainty of the Arsenic component in PM2.5 ambient aerosol particles in air'
As_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_As Uncert (ug/m3)'].min()
As_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_As Uncert (ug/m3)'].max()
As_Uncert_PM2p5.call_methods = 'time:mean'

Ba_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Ba_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Ba_PM2p5.type = 'float32'
Ba_PM2p5.dimension = 'time' 
Ba_PM2p5.units ='ug m-3'
Ba_PM2p5.standard_name = 'mass_concentration_of_ba_in_pm2p5_ambient_aerosol_particles_in_air'
Ba_PM2p5.long_name = 'Mass concentration of the Barium component in PM2.5 ambient aerosol particles in air'
Ba_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Ba 56 (ug/m3)'].min()
Ba_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Ba 56 (ug/m3)'].max()
Ba_PM2p5.call_methods = 'time:mean'
Ba_PM2p5.coordinates =  '53.456636N, -2.214244E'
Ba_PM2p5.chemical_species = 'Ba_PM2.5'

qc_flag_Ba_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Ba_PM2p5', 'b', ('time',))
qc_flag_Ba_PM2p5.type = 'byte'
qc_flag_Ba_PM2p5.units = '1'
qc_flag_Ba_PM2p5.long_name = 'Data Quality flag: Ba_PM2.5'
qc_flag_Ba_PM2p5.flag_values ='0b,1b,2b,3b' #'0b,1b,2b,3b'
qc_flag_Ba_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' #'\n\rnot_used \n\rgood_data \n\rsuspect_data_data_not_quality_controlled \n\rbad_data_do_not_use ,'


Ba_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Ba_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Ba_Uncert_PM2p5.type = 'float32'
Ba_Uncert_PM2p5.dimension = 'time' 
Ba_Uncert_PM2p5.units ='ug m-3'
Ba_Uncert_PM2p5.standard_name = 'uncertainty_of_Ba_in_pm2p5_ambient_aerosol_particles_in_air'
Ba_Uncert_PM2p5.long_name = 'Uncertainty of the Barium component in PM2.5 ambient aerosol particles in air'
Ba_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Ba Uncert (ug/m3)'].min()
Ba_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Ba Uncert (ug/m3)'].max()
Ba_Uncert_PM2p5.call_methods = 'time:mean'

Br_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Br_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Br_PM2p5.type = 'float32'
Br_PM2p5.dimension = 'time' 
Br_PM2p5.units ='ug m-3'
Br_PM2p5.standard_name = 'mass_concentration_of_br_in_pm2p5_ambient_aerosol_particles_in_air'
Br_PM2p5.long_name = 'Mass concentration of the Bromine component in PM2.5 ambient aerosol particles in air'
Br_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Br 35 (ug/m3)'].min()
Br_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Br 35 (ug/m3)'].max()
Br_PM2p5.call_methods = 'time:mean'
Br_PM2p5.coordinates =  '53.456636N, -2.214244E'
Br_PM2p5.chemical_species = 'Br_PM2.5'

qc_flag_Br_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Br_PM2p5', 'b', ('time',))
qc_flag_Br_PM2p5.type = 'byte'
qc_flag_Br_PM2p5.units = '1'
qc_flag_Br_PM2p5.long_name = 'Data Quality flag: Br_PM2.5'
qc_flag_Br_PM2p5.flag_values ='0b,1b,2b,3b' #'0b,1b,2b,3b'
qc_flag_Br_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' #'\n\rnot_used \n\rgood_data \n\rsuspect_data_data_not_quality_controlled \n\rbad_data_do_not_use ,'


Br_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Br_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Br_Uncert_PM2p5.type = 'float32'
Br_Uncert_PM2p5.dimension = 'time' 
Br_Uncert_PM2p5.units ='ug m-3'
Br_Uncert_PM2p5.standard_name = 'uncertainty_of_Br_in_pm2p5_ambient_aerosol_particles_in_air'
Br_Uncert_PM2p5.long_name = 'Uncertainty of the Bromine component in PM2.5 ambient aerosol particles in air'
Br_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Br Uncert (ug/m3)'].min()
Br_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Br Uncert (ug/m3)'].max()
Br_Uncert_PM2p5.call_methods = 'time:mean'

Ca_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Ca_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Ca_PM2p5.type = 'float32'
Ca_PM2p5.dimension = 'time' 
Ca_PM2p5.units ='ug m-3'
Ca_PM2p5.standard_name = 'mass_concentration_of_ca_in_pm2p5_ambient_aerosol_particles_in_air'
Ca_PM2p5.long_name = 'Mass concentration of the Calcium component in PM2.5 ambient aerosol particles in air'
Ca_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Ca 20 (ug/m3)'].min()
Ca_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Ca 20 (ug/m3)'].max()
Ca_PM2p5.call_methods = 'time:mean'
Ca_PM2p5.coordinates =  '53.456636N, -2.214244E'
Ca_PM2p5.chemical_species = 'Ca_PM2.5'

qc_flag_Ca_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Ca_PM2p5', 'b', ('time',))
qc_flag_Ca_PM2p5.type = 'byte'
qc_flag_Ca_PM2p5.units = '1'
qc_flag_Ca_PM2p5.long_name = 'Data Quality flag: Ca_PM2.5'
qc_flag_Ca_PM2p5.flag_values ='0b,1b,2b,3b' #'0b,1b,2b,3b'
qc_flag_Ca_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' #'\n\rnot_used \n\rgood_data \n\rsuspect_data_data_not_quality_controlled \n\rbad_data_do_not_use ,'


Ca_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Ca_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Ca_Uncert_PM2p5.type = 'float32'
Ca_Uncert_PM2p5.dimension = 'time' 
Ca_Uncert_PM2p5.units ='ug m-3'
Ca_Uncert_PM2p5.standard_name = 'uncertainty_of_Ca_in_pm2p5_ambient_aerosol_particles_in_air'
Ca_Uncert_PM2p5.long_name = 'Uncertainty of the Calcium component in PM2.5 ambient aerosol particles in air'
Ca_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Ca Uncert (ug/m3)'].min()
Ca_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Ca Uncert (ug/m3)'].max()
Ca_Uncert_PM2p5.call_methods = 'time:mean'

Cl_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Cl_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Cl_PM2p5.type = 'float32'
Cl_PM2p5.dimension = 'time' 
Cl_PM2p5.units ='ug m-3'
Cl_PM2p5.standard_name = 'mass_concentration_of_cl_in_pm2p5_ambient_aerosol_particles_in_air'
Cl_PM2p5.long_name = 'Mass concentration of the Chlorine component in PM2.5 ambient aerosol particles in air'
Cl_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Cl 17 (ug/m3)'].min()
Cl_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Cl 17 (ug/m3)'].max()
Cl_PM2p5.call_methods = 'time:mean'
Cl_PM2p5.coordinates =  '53.456636N, -2.214244E'
Cl_PM2p5.chemical_species = 'Cl_PM2.5'

qc_flag_Cl_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Cl_PM2p5', 'b', ('time',))
qc_flag_Cl_PM2p5.type = 'byte'
qc_flag_Cl_PM2p5.units = '1'
qc_flag_Cl_PM2p5.long_name = 'Data Quality flag: Cl_PM2.5'
qc_flag_Cl_PM2p5.flag_values ='0b,1b,2b,3b' #'0b,1b,2b,3b'
qc_flag_Cl_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' #'\n\rnot_used \n\rgood_data \n\rsuspect_data_data_not_quality_controlled \n\rbad_data_do_not_use ,'

Cl_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Cl_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Cl_Uncert_PM2p5.type = 'float32'
Cl_Uncert_PM2p5.dimension = 'time' 
Cl_Uncert_PM2p5.units ='ug m-3'
Cl_Uncert_PM2p5.standard_name = 'uncertainty_of_Cl_in_pm2p5_ambient_aerosol_particles_in_air'
Cl_Uncert_PM2p5.long_name = 'Uncertainty of the Chlorine component in PM2.5 ambient aerosol particles in air'
Cl_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Cl Uncert (ug/m3)'].min()
Cl_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Cl Uncert (ug/m3)'].max()
Cl_Uncert_PM2p5.call_methods = 'time:mean'


Cr_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Cr_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Cr_PM2p5.type = 'float32'
Cr_PM2p5.dimension = 'time' 
Cr_PM2p5.units ='ug m-3'
Cr_PM2p5.standard_name = 'mass_concentration_of_cr_in_pm2p5_ambient_aerosol_particles_in_air'
Cr_PM2p5.long_name = 'Mass concentration of the Chromium component in PM2.5 ambient aerosol particles in air'
Cr_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Cr 24 (ug/m3)'].min()
Cr_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Cr 24 (ug/m3)'].max()
Cr_PM2p5.call_methods = 'time:mean'
Cr_PM2p5.coordinates =  '53.456636N, -2.214244E'
Cr_PM2p5.chemical_species = 'Cr_PM2.5'

qc_flag_Cr_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Cr_PM2p5', 'b', ('time',))
qc_flag_Cr_PM2p5.type = 'byte'
qc_flag_Cr_PM2p5.units = '1'
qc_flag_Cr_PM2p5.long_name = 'Data Quality flag: Cr_PM2.5'
qc_flag_Cr_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_Cr_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' 

Cr_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Cr_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Cr_Uncert_PM2p5.type = 'float32'
Cr_Uncert_PM2p5.dimension = 'time' 
Cr_Uncert_PM2p5.units ='ug m-3'
Cr_Uncert_PM2p5.standard_name = 'uncertainty_of_Cr_in_pm2p5_ambient_aerosol_particles_in_air'
Cr_Uncert_PM2p5.long_name = 'Uncertainty of the Chromium component in PM2.5 ambient aerosol particles in air'
Cr_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Cr Uncert (ug/m3)'].min()
Cr_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Cr Uncert (ug/m3)'].max()
Cr_Uncert_PM2p5.call_methods = 'time:mean'


Cu_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Cu_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Cu_PM2p5.type = 'float32'
Cu_PM2p5.dimension = 'time' 
Cu_PM2p5.units ='ug m-3'
Cu_PM2p5.standard_name = 'mass_concentration_of_cu_in_pm2p5_ambient_aerosol_particles_in_air'
Cu_PM2p5.long_name = 'Mass concentration of the Copper component in PM2.5 ambient aerosol particles in air'
Cu_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Cu 29 (ug/m3)'].min()
Cu_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Cu 29 (ug/m3)'].max()
Cu_PM2p5.call_methods = 'time:mean'
Cu_PM2p5.coordinates =  '53.456636N, -2.214244E'
Cu_PM2p5.chemical_species = 'Cu_PM2.5'

qc_flag_Cu_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Cu_PM2p5', 'b', ('time',))
qc_flag_Cu_PM2p5.type = 'byte'
qc_flag_Cu_PM2p5.units = '1'
qc_flag_Cu_PM2p5.long_name = 'Data Quality flag: Cu_PM2.5'
qc_flag_Cu_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_Cu_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' 

Cu_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Cu_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Cu_Uncert_PM2p5.type = 'float32'
Cu_Uncert_PM2p5.dimension = 'time' 
Cu_Uncert_PM2p5.units ='ug m-3'
Cu_Uncert_PM2p5.standard_name = 'uncertainty_of_Cu_in_pm2p5_ambient_aerosol_particles_in_air'
Cu_Uncert_PM2p5.long_name = 'Uncertainty of the Copper component in PM2.5 ambient aerosol particles in air'
Cu_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Cu Uncert (ug/m3)'].min()
Cu_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Cu Uncert (ug/m3)'].max()
Cu_Uncert_PM2p5.call_methods = 'time:mean'


Fe_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Fe_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Fe_PM2p5.type = 'float32'
Fe_PM2p5.dimension = 'time' 
Fe_PM2p5.units ='ug m-3'
Fe_PM2p5.standard_name = 'mass_concentration_of_fe_in_pm2p5_ambient_aerosol_particles_in_air'
Fe_PM2p5.long_name = 'Mass concentration of the Iron component in PM2.5 ambient aerosol particles in air'
Fe_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Fe 26 (ug/m3)'].min()
Fe_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Fe 26 (ug/m3)'].max()
Fe_PM2p5.call_methods = 'time:mean'
Fe_PM2p5.coordinates =  '53.456636N, -2.214244E'
Fe_PM2p5.chemical_species = 'Fe_PM2.5'

qc_flag_Fe_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Fe_PM2p5', 'b', ('time',))
qc_flag_Fe_PM2p5.type = 'byte'
qc_flag_Fe_PM2p5.units = '1'
qc_flag_Fe_PM2p5.long_name = 'Data Quality flag: Fe_PM2.5'
qc_flag_Fe_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_Fe_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' 

Fe_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Fe_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Fe_Uncert_PM2p5.type = 'float32'
Fe_Uncert_PM2p5.dimension = 'time' 
Fe_Uncert_PM2p5.units ='ug m-3'
Fe_Uncert_PM2p5.standard_name = 'uncertainty_of_Fe_in_pm2p5_ambient_aerosol_particles_in_air'
Fe_Uncert_PM2p5.long_name = 'Uncertainty of the Iron component in PM2.5 ambient aerosol particles in air'
Fe_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Fe Uncert (ug/m3)'].min()
Fe_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Fe Uncert (ug/m3)'].max()
Fe_Uncert_PM2p5.call_methods = 'time:mean'


K_PM2p5 = dataset_out.createVariable('Mass_Conc_of_K_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
K_PM2p5.type = 'float32'
K_PM2p5.dimension = 'time' 
K_PM2p5.units ='ug m-3'
K_PM2p5.standard_name = 'mass_concentration_of_k_in_pm2p5_ambient_aerosol_particles_in_air'
K_PM2p5.long_name = 'Mass concentration of the Potassium component in PM2.5 ambient aerosol particles in air'
K_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_K 19 (ug/m3)'].min()
K_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_K 19 (ug/m3)'].max()
K_PM2p5.call_methods = 'time:mean'
K_PM2p5.coordinates =  '53.456636N, -2.214244E'
K_PM2p5.chemical_species = 'K_PM2.5'

qc_flag_K_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_K_PM2p5', 'b', ('time',))
qc_flag_K_PM2p5.type = 'byte'
qc_flag_K_PM2p5.units = '1'
qc_flag_K_PM2p5.long_name = 'Data Quality flag: K_PM2.5'
qc_flag_K_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_K_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' 

K_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_K_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
K_Uncert_PM2p5.type = 'float32'
K_Uncert_PM2p5.dimension = 'time' 
K_Uncert_PM2p5.units ='ug m-3'
K_Uncert_PM2p5.standard_name = 'uncertainty_of_K_in_pm2p5_ambient_aerosol_particles_in_air'
K_Uncert_PM2p5.long_name = 'Uncertainty of the Potassium component in PM2.5 ambient aerosol particles in air'
K_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_K Uncert (ug/m3)'].min()
K_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_K Uncert (ug/m3)'].max()
K_Uncert_PM2p5.call_methods = 'time:mean'


Mn_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Mn_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Mn_PM2p5.type = 'float32'
Mn_PM2p5.dimension = 'time' 
Mn_PM2p5.units ='ug m-3'
Mn_PM2p5.standard_name = 'mass_concentration_of_mn_in_pm2p5_ambient_aerosol_particles_in_air'
Mn_PM2p5.long_name = 'Mass concentration of the Manganese component in PM2.5 ambient aerosol particles in air'
Mn_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Mn 25 (ug/m3)'].min()
Mn_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Mn 25 (ug/m3)'].max()
Mn_PM2p5.call_methods = 'time:mean'
Mn_PM2p5.coordinates =  '53.456636N, -2.214244E'
Mn_PM2p5.chemical_species = 'Mn_PM2.5'

qc_flag_Mn_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Mn_PM2p5', 'b', ('time',))
qc_flag_Mn_PM2p5.type = 'byte'
qc_flag_Mn_PM2p5.units = '1'
qc_flag_Mn_PM2p5.long_name = 'Data Quality flag: Mn_PM2.5'
qc_flag_Mn_PM2p5.flag_values ='0b,1b,2b,3b' #'0b,1b,2b,3b'
qc_flag_Mn_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

Mn_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Mn_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Mn_Uncert_PM2p5.type = 'float32'
Mn_Uncert_PM2p5.dimension = 'time' 
Mn_Uncert_PM2p5.units ='ug m-3'
Mn_Uncert_PM2p5.standard_name = 'uncertainty_of_Mn_in_pm2p5_ambient_aerosol_particles_in_air'
Mn_Uncert_PM2p5.long_name = 'Uncertainty of the Manganese component in PM2.5 ambient aerosol particles in air'
Mn_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Mn Uncert (ug/m3)'].min()
Mn_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Mn Uncert (ug/m3)'].max()
Mn_Uncert_PM2p5.call_methods = 'time:mean'

Ni_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Ni_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Ni_PM2p5.type = 'float32'
Ni_PM2p5.dimension = 'time' 
Ni_PM2p5.units ='ug m-3'
Ni_PM2p5.standard_name = 'mass_concentration_of_ni_in_pm2p5_ambient_aerosol_particles_in_air'
Ni_PM2p5.long_name = 'Mass concentration of the Nickel component in PM2.5 ambient aerosol particles in air'
Ni_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Ni 28 (ug/m3)'].min()
Ni_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Ni 28 (ug/m3)'].max()
Ni_PM2p5.call_methods = 'time:mean'
Ni_PM2p5.coordinates =  '53.456636N, -2.214244E'
Ni_PM2p5.chemical_species = 'Ni_PM2.5'

qc_flag_Ni_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Ni_PM2p5', 'b', ('time',))
qc_flag_Ni_PM2p5.type = 'byte'
qc_flag_Ni_PM2p5.units = '1'
qc_flag_Ni_PM2p5.long_name = 'Data Quality flag: Ni_PM2.5'
qc_flag_Ni_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_Ni_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' 

Ni_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Ni_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Ni_Uncert_PM2p5.type = 'float32'
Ni_Uncert_PM2p5.dimension = 'time' 
Ni_Uncert_PM2p5.units ='ug m-3'
Ni_Uncert_PM2p5.standard_name = 'uncertainty_of_Ni_in_pm2p5_ambient_aerosol_particles_in_air'
Ni_Uncert_PM2p5.long_name = 'Uncertainty of the Nickel component in PM2.5 ambient aerosol particles in air'
Ni_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Ni Uncert (ug/m3)'].min()
Ni_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Ni Uncert (ug/m3)'].max()
Ni_Uncert_PM2p5.call_methods = 'time:mean'


Pb_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Pb_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Pb_PM2p5.type = 'float32'
Pb_PM2p5.dimension = 'time' 
Pb_PM2p5.units ='ug m-3'
Pb_PM2p5.standard_name = 'mass_concentration_of_pb_in_pm2p5_ambient_aerosol_particles_in_air'
Pb_PM2p5.long_name = 'Mass concentration of the Lead component in PM2.5 ambient aerosol particles in air'
Pb_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Pb 82 (ug/m3)'].min()
Pb_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Pb 82 (ug/m3)'].max()
Pb_PM2p5.call_methods = 'time:mean'
Pb_PM2p5.coordinates =  '53.456636N, -2.214244E'
Pb_PM2p5.chemical_species = 'Pb_PM2.5'

qc_flag_Pb_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Pb_PM2p5', 'b', ('time',))
qc_flag_Pb_PM2p5.type = 'byte'
qc_flag_Pb_PM2p5.units = '1'
qc_flag_Pb_PM2p5.long_name = 'Data Quality flag: Pb_PM2.5'
qc_flag_Pb_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_Pb_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' 

Pb_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Pb_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Pb_Uncert_PM2p5.type = 'float32'
Pb_Uncert_PM2p5.dimension = 'time' 
Pb_Uncert_PM2p5.units ='ug m-3'
Pb_Uncert_PM2p5.standard_name = 'uncertainty_of_Pb_in_pm2p5_ambient_aerosol_particles_in_air'
Pb_Uncert_PM2p5.long_name = 'Uncertainty of the Lead component in PM2.5 ambient aerosol particles in air'
Pb_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Pb Uncert (ug/m3)'].min()
Pb_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Pb Uncert (ug/m3)'].max()
Pb_Uncert_PM2p5.call_methods = 'time:mean'


Pd_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Pd_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Pd_PM2p5.type = 'float32'
Pd_PM2p5.dimension = 'time' 
Pd_PM2p5.units ='ug m-3'
Pd_PM2p5.standard_name = 'mass_concentration_of_pd_in_pm2p5_ambient_aerosol_particles_in_air'
Pd_PM2p5.long_name = 'Mass concentration of the Palladium component in PM2.5 ambient aerosol particles in air'
Pd_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Pd 46 (ug/m3)'].min()
Pd_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Pd 46 (ug/m3)'].max()
Pd_PM2p5.call_methods = 'time:mean'
Pd_PM2p5.coordinates =  '53.456636N, -2.214244E'
Pd_PM2p5.chemical_species = 'Pd_PM2.5'

qc_flag_Pd_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Pd_PM2p5', 'b', ('time',))
qc_flag_Pd_PM2p5.type = 'byte'
qc_flag_Pd_PM2p5.units = '1'
qc_flag_Pd_PM2p5.long_name = 'Data Quality flag: Pd_PM2.5'
qc_flag_Pd_PM2p5.flag_values ='0b,1b,2b,3b' #
qc_flag_Pd_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' 

Pd_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Pd_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Pd_Uncert_PM2p5.type = 'float32'
Pd_Uncert_PM2p5.dimension = 'time' 
Pd_Uncert_PM2p5.units ='ug m-3'
Pd_Uncert_PM2p5.standard_name = 'uncertainty_of_Pd_in_pm2p5_ambient_aerosol_particles_in_air'
Pd_Uncert_PM2p5.long_name = 'Uncertainty of the Palladium component in PM2.5 ambient aerosol particles in air'
Pd_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Pd Uncert (ug/m3)'].min()
Pd_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Pd Uncert (ug/m3)'].max()
Pd_Uncert_PM2p5.call_methods = 'time:mean'


S_PM2p5 = dataset_out.createVariable('Mass_Conc_of_S_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
S_PM2p5.type = 'float32'
S_PM2p5.dimension = 'time' 
S_PM2p5.units ='ug m-3'
S_PM2p5.standard_name = 'mass_concentration_of_s_in_pm2p5_ambient_aerosol_particles_in_air'
S_PM2p5.long_name = 'Mass concentration of the Sulfur component in PM2.5 ambient aerosol particles in air'
S_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_S 16 (ug/m3)'].min()
S_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_S 16 (ug/m3)'].max()
S_PM2p5.call_methods = 'time:mean'
S_PM2p5.coordinates =  '53.456636N, -2.214244E'
S_PM2p5.chemical_species = 'S_PM2.5'

qc_flag_S_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_S_PM2p5', 'b', ('time',))
qc_flag_S_PM2p5.type = 'byte'
qc_flag_S_PM2p5.units = '1'
qc_flag_S_PM2p5.long_name = 'Data Quality flag: S_PM2.5'
qc_flag_S_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_S_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

S_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_S_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
S_Uncert_PM2p5.type = 'float32'
S_Uncert_PM2p5.dimension = 'time' 
S_Uncert_PM2p5.units ='ug m-3'
S_Uncert_PM2p5.standard_name = 'uncertainty_of_S_in_pm2p5_ambient_aerosol_particles_in_air'
S_Uncert_PM2p5.long_name = 'Uncertainty of the Sulfur component in PM2.5 ambient aerosol particles in air'
S_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_S Uncert (ug/m3)'].min()
S_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_S Uncert (ug/m3)'].max()
S_Uncert_PM2p5.call_methods = 'time:mean'


Sb_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Sb_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Sb_PM2p5.type = 'float32'
Sb_PM2p5.dimension = 'time' 
Sb_PM2p5.units ='ug m-3'
Sb_PM2p5.standard_name = 'mass_concentration_of_sb_in_pm2p5_ambient_aerosol_particles_in_air'
Sb_PM2p5.long_name = 'Mass concentration of the Antimony component in PM2.5 ambient aerosol particles in air'
Sb_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Sb 51 (ug/m3)'].min()
Sb_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Sb 51 (ug/m3)'].max()
Sb_PM2p5.call_methods = 'time:mean'
Sb_PM2p5.coordinates =  '53.456636N, -2.214244E'
Sb_PM2p5.chemical_species = 'Sb_PM2.5'

qc_flag_Sb_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Sb_PM2p5', 'b', ('time',))
qc_flag_Sb_PM2p5.type = 'byte'
qc_flag_Sb_PM2p5.units = '1'
qc_flag_Sb_PM2p5.long_name = 'Data Quality flag: Sb_PM2.5'
qc_flag_Sb_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_Sb_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' 

Sb_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Sb_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Sb_Uncert_PM2p5.type = 'float32'
Sb_Uncert_PM2p5.dimension = 'time' 
Sb_Uncert_PM2p5.units ='ug m-3'
Sb_Uncert_PM2p5.standard_name = 'uncertainty_of_Sb_in_pm2p5_ambient_aerosol_particles_in_air'
Sb_Uncert_PM2p5.long_name = 'Uncertainty of the Antimony component in PM2.5 ambient aerosol particles in air'
Sb_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Sb Uncert (ug/m3)'].min()
Sb_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Sb Uncert (ug/m3)'].max()
Sb_Uncert_PM2p5.call_methods = 'time:mean'


Se_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Se_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Se_PM2p5.type = 'float32'
Se_PM2p5.dimension = 'time' 
Se_PM2p5.units ='ug m-3'
Se_PM2p5.standard_name = 'mass_concentration_of_se_in_pm2p5_ambient_aerosol_particles_in_air'
Se_PM2p5.long_name = 'Mass concentration of the Selenium component in PM2.5 ambient aerosol particles in air'
Se_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Se 34 (ug/m3)'].min()
Se_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Se 34 (ug/m3)'].max()
Se_PM2p5.call_methods = 'time:mean'
Se_PM2p5.coordinates =  '53.456636N, -2.214244E'
Se_PM2p5.chemical_species = 'Se_PM2.5'

qc_flag_Se_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Se_PM2p5', 'b', ('time',))
qc_flag_Se_PM2p5.type = 'byte'
qc_flag_Se_PM2p5.units = '1'
qc_flag_Se_PM2p5.long_name = 'Data Quality flag: Se_PM2.5'
qc_flag_Se_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_Se_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' 

Se_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Se_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Se_Uncert_PM2p5.type = 'float32'
Se_Uncert_PM2p5.dimension = 'time' 
Se_Uncert_PM2p5.units ='ug m-3'
Se_Uncert_PM2p5.standard_name = 'uncertainty_of_Se_in_pm2p5_ambient_aerosol_particles_in_air'
Se_Uncert_PM2p5.long_name = 'Uncertainty of the Selenium component in PM2.5 ambient aerosol particles in air'
Se_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Se Uncert (ug/m3)'].min()
Se_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Se Uncert (ug/m3)'].max()
Se_Uncert_PM2p5.call_methods = 'time:mean'


Si_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Si_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Si_PM2p5.type = 'float32'
Si_PM2p5.dimension = 'time' 
Si_PM2p5.units ='ug m-3'
Si_PM2p5.standard_name = 'mass_concentration_of_si_in_pm2p5_ambient_aerosol_particles_in_air'
Si_PM2p5.long_name = 'Mass concentration of the Silicon component in PM2.5 ambient aerosol particles in air'
Si_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Si 14 (ug/m3)'].min()
Si_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Si 14 (ug/m3)'].max()
Si_PM2p5.call_methods = 'time:mean'
Si_PM2p5.coordinates =  '53.456636N, -2.214244E'
Si_PM2p5.chemical_species = 'Si_PM2.5'

qc_flag_Si_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Si_PM2p5', 'b', ('time',))
qc_flag_Si_PM2p5.type = 'byte'
qc_flag_Si_PM2p5.units = '1'
qc_flag_Si_PM2p5.long_name = 'Data Quality flag: Si_PM2.5'
qc_flag_Si_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_Si_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' 

Si_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Si_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Si_Uncert_PM2p5.type = 'float32'
Si_Uncert_PM2p5.dimension = 'time' 
Si_Uncert_PM2p5.units ='ug m-3'
Si_Uncert_PM2p5.standard_name = 'uncertainty_of_Si_in_pm2p5_ambient_aerosol_particles_in_air'
Si_Uncert_PM2p5.long_name = 'Uncertainty of the Silicon component in PM2.5 ambient aerosol particles in air'
Si_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Si Uncert (ug/m3)'].min()
Si_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Si Uncert (ug/m3)'].max()
Si_Uncert_PM2p5.call_methods = 'time:mean'


Sr_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Sr_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Sr_PM2p5.type = 'float32'
Sr_PM2p5.dimension = 'time' 
Sr_PM2p5.units ='ug m-3'
Sr_PM2p5.standard_name = 'mass_concentration_of_sr_in_pm2p5_ambient_aerosol_particles_in_air'
Sr_PM2p5.long_name = 'Mass concentration of the Strontium component in PM2.5 ambient aerosol particles in air'
Sr_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Sr 38 (ug/m3)'].min()
Sr_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Sr 38 (ug/m3)'].max()
Sr_PM2p5.call_methods = 'time:mean'
Sr_PM2p5.coordinates =  '53.456636N, -2.214244E'
Sr_PM2p5.chemical_species = 'Sr_PM2.5'

qc_flag_Sr_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Sr_PM2p5', 'b', ('time',))
qc_flag_Sr_PM2p5.type = 'byte'
qc_flag_Sr_PM2p5.units = '1'
qc_flag_Sr_PM2p5.long_name = 'Data Quality flag: Sr_PM2.5'
qc_flag_Sr_PM2p5.flag_values ='0b,1b,2b,3b' #'0b,1b,2b,3b'
qc_flag_Sr_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

Sr_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Sr_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Sr_Uncert_PM2p5.type = 'float32'
Sr_Uncert_PM2p5.dimension = 'time' 
Sr_Uncert_PM2p5.units ='ug m-3'
Sr_Uncert_PM2p5.standard_name = 'uncertainty_of_Sr_in_pm2p5_ambient_aerosol_particles_in_air'
Sr_Uncert_PM2p5.long_name = 'Uncertainty of the Strontium component in PM2.5 ambient aerosol particles in air'
Sr_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Sr Uncert (ug/m3)'].min()
Sr_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Sr Uncert (ug/m3)'].max()
Sr_Uncert_PM2p5.call_methods = 'time:mean'


Te_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Te_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Te_PM2p5.type = 'float32'
Te_PM2p5.dimension = 'time' 
Te_PM2p5.units ='ug m-3'
Te_PM2p5.standard_name = 'mass_concentration_of_te_in_pm2p5_ambient_aerosol_particles_in_air'
Te_PM2p5.long_name = 'Mass concentration of the Tellurium component in PM2.5 ambient aerosol particles in air'
Te_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Te 52 (ug/m3)'].min()
Te_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Te 52 (ug/m3)'].max()
Te_PM2p5.call_methods = 'time:mean'
Te_PM2p5.coordinates =  '53.456636N, -2.214244E'
Te_PM2p5.chemical_species = 'Te_PM2.5'

qc_flag_Te_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Te_PM2p5', 'b', ('time',))
qc_flag_Te_PM2p5.type = 'byte'
qc_flag_Te_PM2p5.units = '1'
qc_flag_Te_PM2p5.long_name = 'Data Quality flag: Te_PM2.5'
qc_flag_Te_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_Te_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

Te_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Te_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Te_Uncert_PM2p5.type = 'float32'
Te_Uncert_PM2p5.dimension = 'time' 
Te_Uncert_PM2p5.units ='ug m-3'
Te_Uncert_PM2p5.standard_name = 'uncertainty_of_Te_in_pm2p5_ambient_aerosol_particles_in_air'
Te_Uncert_PM2p5.long_name = 'Uncertainty of the Tellurium component in PM2.5 ambient aerosol particles in air'
Te_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Te Uncert (ug/m3)'].min()
Te_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Te Uncert (ug/m3)'].max()
Te_Uncert_PM2p5.call_methods = 'time:mean'


Ti_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Ti_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Ti_PM2p5.type = 'float32'
Ti_PM2p5.dimension = 'time' 
Ti_PM2p5.units ='ug m-3'
Ti_PM2p5.standard_name = 'mass_concentration_of_ti_in_pm2p5_ambient_aerosol_particles_in_air'
Ti_PM2p5.long_name = 'Mass concentration of the Titanium component in PM2.5 ambient aerosol particles in air'
Ti_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Ti 22 (ug/m3)'].min()
Ti_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Ti 22 (ug/m3)'].max()
Ti_PM2p5.call_methods = 'time:mean'
Ti_PM2p5.coordinates =  '53.456636N, -2.214244E'
Ti_PM2p5.chemical_species = 'Ti_PM2.5'

qc_flag_Ti_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Ti_PM2p5', 'b', ('time',))
qc_flag_Ti_PM2p5.type = 'byte'
qc_flag_Ti_PM2p5.units = '1'
qc_flag_Ti_PM2p5.long_name = 'Data Quality flag: Ti_PM2.5'
qc_flag_Ti_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_Ti_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' 

Ti_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Ti_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Ti_Uncert_PM2p5.type = 'float32'
Ti_Uncert_PM2p5.dimension = 'time' 
Ti_Uncert_PM2p5.units ='ug m-3'
Ti_Uncert_PM2p5.standard_name = 'uncertainty_of_Ti_in_pm2p5_ambient_aerosol_particles_in_air'
Ti_Uncert_PM2p5.long_name = 'Uncertainty of the Titanium component in PM2.5 ambient aerosol particles in air'
Ti_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Ti Uncert (ug/m3)'].min()
Ti_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Ti Uncert (ug/m3)'].max()
Ti_Uncert_PM2p5.call_methods = 'time:mean'


V_PM2p5 = dataset_out.createVariable('Mass_Conc_of_V_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
V_PM2p5.type = 'float32'
V_PM2p5.dimension = 'time' 
V_PM2p5.units ='ug m-3'
V_PM2p5.standard_name = 'mass_concentration_of_v_in_pm2p5_ambient_aerosol_particles_in_air'
V_PM2p5.long_name = 'Mass concentration of the Vanadium component in PM2.5 ambient aerosol particles in air'
V_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_V 23 (ug/m3)'].min()
V_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_V 23 (ug/m3)'].max()
V_PM2p5.call_methods = 'time:mean'
V_PM2p5.coordinates =  '53.456636N, -2.214244E'
V_PM2p5.chemical_species = 'V_PM2.5'

qc_flag_V_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_V_PM2p5', 'b', ('time',))
qc_flag_V_PM2p5.type = 'byte'
qc_flag_V_PM2p5.units = '1'
qc_flag_V_PM2p5.long_name = 'Data Quality flag: V_PM2.5'
qc_flag_V_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_V_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,' 

V_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_V_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
V_Uncert_PM2p5.type = 'float32'
V_Uncert_PM2p5.dimension = 'time' 
V_Uncert_PM2p5.units ='ug m-3'
V_Uncert_PM2p5.standard_name = 'uncertainty_of_V_in_pm2p5_ambient_aerosol_particles_in_air'
V_Uncert_PM2p5.long_name = 'Uncertainty of the Vanadium component in PM2.5 ambient aerosol particles in air'
V_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_V Uncert (ug/m3)'].min()
V_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_V Uncert (ug/m3)'].max()
V_Uncert_PM2p5.call_methods = 'time:mean'


Zn_PM2p5 = dataset_out.createVariable('Mass_Conc_of_Zn_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Zn_PM2p5.type = 'float32'
Zn_PM2p5.dimension = 'time' 
Zn_PM2p5.units ='ug m-3'
Zn_PM2p5.standard_name = 'mass_concentration_of_zn_in_pm2p5_ambient_aerosol_particles_in_air'
Zn_PM2p5.long_name = 'Mass concentration of the Zinc component in PM2.5 ambient aerosol particles in air'
Zn_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Zn 30 (ug/m3)'].min()
Zn_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Zn 30 (ug/m3)'].max()
Zn_PM2p5.call_methods = 'time:mean'
Zn_PM2p5.coordinates =  '53.456636N, -2.214244E'
Zn_PM2p5.chemical_species = 'Zn_PM2.5'

qc_flag_Zn_PM2p5 = dataset_out.createVariable('qc_flag_Mass_Conc_of_Zn_PM2p5', 'b', ('time',))
qc_flag_Zn_PM2p5.type = 'byte'
qc_flag_Zn_PM2p5.units = '1'
qc_flag_Zn_PM2p5.long_name = 'Data Quality flag: Zn_PM2.5'  
qc_flag_Zn_PM2p5.flag_values ='0b,1b,2b,3b' 
qc_flag_Zn_PM2p5.flag_meanings = '\n\rnot_used \n\rgood_data \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

Zn_Uncert_PM2p5 = dataset_out.createVariable('Uncertainty_of_Zn_PM2p5', np.float32, ('time',), fill_value=-1.00E+20)
Zn_Uncert_PM2p5.type = 'float32'
Zn_Uncert_PM2p5.dimension = 'time' 
Zn_Uncert_PM2p5.units ='ug m-3'
Zn_Uncert_PM2p5.standard_name = 'uncertainty_of_Zn_in_pm2p5_ambient_aerosol_particles_in_air'
Zn_Uncert_PM2p5.long_name = 'Uncertainty of the Zinc component in PM2.5 ambient aerosol particles in air'
Zn_Uncert_PM2p5.valid_min = xact_PM2p5_csv['PM2.5_Zn Uncert (ug/m3)'].min()
Zn_Uncert_PM2p5.valid_max = xact_PM2p5_csv['PM2.5_Zn Uncert (ug/m3)'].max()
Zn_Uncert_PM2p5.call_methods = 'time:mean'



# this bit writes the data from the master dataframe to the variables
times[:] = xact_PM2p5_csv['TimeSecondsSince'].values#nc.date2num(timeline[:],times.units)
day_of_year[:] = xact_PM2p5_csv['day_year'].values
year[:] = xact_PM2p5_csv['year'].values
month[:] = xact_PM2p5_csv['month'].values
day[:] = xact_PM2p5_csv['day'].values
hour[:] = xact_PM2p5_csv['hour'].values
minute[:] = xact_PM2p5_csv['minute'].values
second[:] = xact_PM2p5_csv['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244
Ag_PM2p5[:] = xact_PM2p5_csv['PM2.5_Ag 47 (ug/m3)'].values
Flag_Ag_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Ag_flag']).astype(np.ubyte)
Ag_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Ag Uncert (ug/m3)'].values
qc_flag_Ag_PM2p5[:] = Flag_Ag_PM2p5_Byte
Al_PM2p5[:] = xact_PM2p5_csv['PM2.5_Al 13 (ug/m3)'].values
Flag_Al_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Al_flag']).astype(np.ubyte)
Al_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Al Uncert (ug/m3)'].values
qc_flag_Al_PM2p5[:] = Flag_Al_PM2p5_Byte
As_PM2p5[:] = xact_PM2p5_csv['PM2.5_As 33 (ug/m3)'].values
Flag_As_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_As_flag']).astype(np.ubyte)
As_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_As Uncert (ug/m3)'].values
qc_flag_As_PM2p5[:] = Flag_As_PM2p5_Byte
Ba_PM2p5[:] = xact_PM2p5_csv['PM2.5_Ba 56 (ug/m3)'].values
Flag_Ba_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Ba_flag']).astype(np.ubyte)
Ba_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Ba Uncert (ug/m3)'].values
qc_flag_Ba_PM2p5[:] = Flag_Ba_PM2p5_Byte
Br_PM2p5[:] = xact_PM2p5_csv['PM2.5_Br 35 (ug/m3)'].values
Flag_Br_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Br_flag']).astype(np.ubyte)
Br_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Br Uncert (ug/m3)'].values
qc_flag_Br_PM2p5[:] = Flag_Br_PM2p5_Byte
Ca_PM2p5[:] = xact_PM2p5_csv['PM2.5_Ca 20 (ug/m3)'].values
Flag_Ca_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Ca_flag']).astype(np.ubyte)
Ca_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Ca Uncert (ug/m3)'].values
qc_flag_Ca_PM2p5[:] = Flag_Ca_PM2p5_Byte
Cl_PM2p5[:] = xact_PM2p5_csv['PM2.5_Cl 17 (ug/m3)'].values
Flag_Cl_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Cl_flag']).astype(np.ubyte)
Cl_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Cl Uncert (ug/m3)'].values
qc_flag_Cl_PM2p5[:] = Flag_Cl_PM2p5_Byte
Cr_PM2p5[:] = xact_PM2p5_csv['PM2.5_Cr 24 (ug/m3)'].values
Flag_Cr_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Cr_flag']).astype(np.ubyte)
Cr_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Cr Uncert (ug/m3)'].values
qc_flag_Cr_PM2p5[:] = Flag_Cr_PM2p5_Byte
Cu_PM2p5[:] = xact_PM2p5_csv['PM2.5_Cu 29 (ug/m3)'].values
Flag_Cu_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Cu_flag']).astype(np.ubyte)
Cu_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Cu Uncert (ug/m3)'].values
qc_flag_Cu_PM2p5[:] = Flag_Cu_PM2p5_Byte
Fe_PM2p5[:] = xact_PM2p5_csv['PM2.5_Fe 26 (ug/m3)'].values
Flag_Fe_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Fe_flag']).astype(np.ubyte)
Fe_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Fe Uncert (ug/m3)'].values
qc_flag_Fe_PM2p5[:] = Flag_Fe_PM2p5_Byte
K_PM2p5[:] = xact_PM2p5_csv['PM2.5_K 19 (ug/m3)'].values
Flag_K_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_K_flag']).astype(np.ubyte)
K_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_K Uncert (ug/m3)'].values
qc_flag_K_PM2p5[:] = Flag_K_PM2p5_Byte
Mn_PM2p5[:] = xact_PM2p5_csv['PM2.5_Mn 25 (ug/m3)'].values
Flag_Mn_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Mn_flag']).astype(np.ubyte)
Mn_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Mn Uncert (ug/m3)'].values
qc_flag_Mn_PM2p5[:] = Flag_Mn_PM2p5_Byte
Ni_PM2p5[:] = xact_PM2p5_csv['PM2.5_Ni 28 (ug/m3)'].values
Flag_Ni_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Ni_flag']).astype(np.ubyte)
Ni_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Ni Uncert (ug/m3)'].values
qc_flag_Ni_PM2p5[:] = Flag_Ni_PM2p5_Byte
Pb_PM2p5[:] = xact_PM2p5_csv['PM2.5_Pb 82 (ug/m3)'].values
Flag_Pb_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Pb_flag']).astype(np.ubyte)
Pb_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Pb Uncert (ug/m3)'].values
qc_flag_Pb_PM2p5[:] = Flag_Pb_PM2p5_Byte
Pd_PM2p5[:] = xact_PM2p5_csv['PM2.5_Pd 46 (ug/m3)'].values
Flag_Pd_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Pd_flag']).astype(np.ubyte)
Pd_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Pd Uncert (ug/m3)'].values
qc_flag_Pd_PM2p5[:] = Flag_Pd_PM2p5_Byte
S_PM2p5[:] = xact_PM2p5_csv['PM2.5_S 16 (ug/m3)'].values
Flag_S_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_S_flag']).astype(np.ubyte)
S_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_S Uncert (ug/m3)'].values
qc_flag_S_PM2p5[:] = Flag_S_PM2p5_Byte
Sb_PM2p5[:] = xact_PM2p5_csv['PM2.5_Sb 51 (ug/m3)'].values
Flag_Sb_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Sb_flag']).astype(np.ubyte)
Sb_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Sb Uncert (ug/m3)'].values
qc_flag_Sb_PM2p5[:] = Flag_Sb_PM2p5_Byte
Se_PM2p5[:] = xact_PM2p5_csv['PM2.5_Se 34 (ug/m3)'].values
Flag_Se_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Se_flag']).astype(np.ubyte)
Se_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Se Uncert (ug/m3)'].values
qc_flag_Se_PM2p5[:] = Flag_Se_PM2p5_Byte
Si_PM2p5[:] = xact_PM2p5_csv['PM2.5_Si 14 (ug/m3)'].values
Flag_Si_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Si_flag']).astype(np.ubyte)
Si_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Si Uncert (ug/m3)'].values
qc_flag_Si_PM2p5[:] = Flag_Si_PM2p5_Byte
Sr_PM2p5[:] = xact_PM2p5_csv['PM2.5_Sr 38 (ug/m3)'].values
Flag_Sr_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Sr_flag']).astype(np.ubyte)
Sr_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Sr Uncert (ug/m3)'].values
qc_flag_Sr_PM2p5[:] = Flag_Sr_PM2p5_Byte
Te_PM2p5[:] = xact_PM2p5_csv['PM2.5_Te 52 (ug/m3)'].values
Flag_Te_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Te_flag']).astype(np.ubyte)
Te_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Te Uncert (ug/m3)'].values
qc_flag_Te_PM2p5[:] = Flag_Te_PM2p5_Byte
Ti_PM2p5[:] = xact_PM2p5_csv['PM2.5_Ti 22 (ug/m3)'].values
Flag_Ti_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Ti_flag']).astype(np.ubyte)
Ti_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Ti Uncert (ug/m3)'].values
qc_flag_Ti_PM2p5[:] = Flag_Ti_PM2p5_Byte
V_PM2p5[:] = xact_PM2p5_csv['PM2.5_V 23 (ug/m3)'].values
Flag_V_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_V_flag']).astype(np.ubyte)
V_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_V Uncert (ug/m3)'].values
qc_flag_V_PM2p5[:] = Flag_V_PM2p5_Byte
Zn_PM2p5[:] = xact_PM2p5_csv['PM2.5_Zn 30 (ug/m3)'].values
Flag_Zn_PM2p5_Byte = np.array(xact_PM2p5_csv['PM2.5_Zn_flag']).astype(np.ubyte)
Zn_Uncert_PM2p5[:] = xact_PM2p5_csv['PM2.5_Zn Uncert (ug/m3)'].values
qc_flag_Zn_PM2p5[:] = Flag_Zn_PM2p5_Byte

dataset_out.close()
