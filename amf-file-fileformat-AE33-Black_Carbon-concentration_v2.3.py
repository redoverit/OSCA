

import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date
import datetime

#def check_times(allFiles):
version_number = 'v2.3' #version of the code
direct = str(AE33_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

today = date.today()
current_month = today.strftime("%B %Y")
month_studied = start.strftime("%B %Y")

print(str(start.strftime("%B")) + ' ' + str(start.strftime("%Y")))

if float(start_year_month_str) < 201907:
    if float(start_year_month_str) < 201812:
        sys.exit("Error Message: This program cannot be used for data prior to December 2018.")
    else:
        sys.exit("Error Message: This is Data measured from Simon Building or van. Just process to CSV, not to be converted to netCDF.")
else:
    pass

dataset_out = nc.Dataset(direct + 'AE33_maqs_' + str(date_file_label) + '_black-carbon-concentration' + str(status) + str(version_number) + '.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.1'
dataset_out.source = 'maqs-AE33-1'
dataset_out.instrument_manufacturer = 'Magee Scientific'
dataset_out.instrument_model = 'Aethalometer Model AE33 with Dualspot technology'
dataset_out.instrument_serial_number = 'AE33-S07-00664'
dataset_out.instrument_software = 'AethNET'
dataset_out.instrument_software_version = '1.4.2.0'
dataset_out.creator_name = 'Dr Nathan Watson'
dataset_out.creator_email = 'nathan.watson@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-9096-0926'
dataset_out.institution = 'University of Manchester'
dataset_out.processing_software_url = 'https://github.com/redoverit/OSCA/'
dataset_out.processing_software_version = str(version_number)
dataset_out.calibration_sensitivity = 'not known'
dataset_out.calibration_certification_url = 'https://github.com/redoverit/OSCA/blob/main/AE33%20Calibration%20Cert.pdf'
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
dataset_out.title = 'Number Concentration of Ambient Aerosol Particles in air'
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
times.valid_min = aeth_Data['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = aeth_Data['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
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
day_of_year.valid_min = aeth_Data['day_year'].min()
day_of_year.valid_max = aeth_Data['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = aeth_Data['year'].min()
year.valid_max = aeth_Data['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = aeth_Data['month'].min()
month.valid_max = aeth_Data['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = aeth_Data['day'].min()
day.valid_max = aeth_Data['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = aeth_Data['hour'].min()
hour.valid_max = aeth_Data['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = aeth_Data['minute'].min()
minute.valid_max = aeth_Data['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = aeth_Data['second'].min()
second.valid_max = aeth_Data['second'].max()

aerosol_880 = dataset_out.createVariable('mass_concentration_of_black_carbon_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
aerosol_880.type = 'float32'
aerosol_880.dimension = 'time' 
aerosol_880.practical_units ='ug m-3'
aerosol_880.Mass_Absorption_Cross_Section = '7.77 (m^2/g)'
aerosol_880.standard_name = 'mass_concentration_of_black_carbon_in_ambient_aerosol_particles_in_air' 
aerosol_880.long_name = 'Mass concentration of the Black Carbon (measured at 880nm wavelength) component of ambient aerosol particles in air'
aerosol_880.valid_min = aeth_Data['BC Conc (ug/m3)'].min()
aerosol_880.valid_max = aeth_Data['BC Conc (ug/m3)'].max()
aerosol_880.call_methods = 'time:mean'
aerosol_880.coordinates =  '53.456636N -2.214244E'
aerosol_880.chemical_species = 'BC'

qc_flag_880 = dataset_out.createVariable('qc_flag_mass_concentration_of_black_carbon_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag_880.type = 'byte'
qc_flag_880.dimension = 'time'
qc_flag_880.units = '1'
qc_flag_880.long_name = 'Data Quality flag' 
qc_flag_880.flag_values ='0b,1b,2b,3b' 
qc_flag_880.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

aerosol_370 = dataset_out.createVariable('mass_concentration_of_UVPM_370_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
aerosol_370.type = 'float32'
aerosol_370.dimension = 'time' 
aerosol_370.practical_units = 'ug m-3'
aerosol_370.Mass_Absorption_Cross_Section = '18.47 (m^2/g)'
aerosol_370.standard_name = 'mass_concentration_of_UVPM_370_in_ambient_aerosol_particles_in_air' 
aerosol_370.long_name = 'Mass concentration of the Ultraviolent Particulate Matter (measured at 370nm wavelength) component of ambient aerosol particles in air'
aerosol_370.valid_min = aeth_Data['UVPM_370_nm (ug/m3)'].min()
aerosol_370.valid_max = aeth_Data['UVPM_370_nm (ug/m3)'].max()
aerosol_370.call_methods = 'time:mean'
aerosol_370.coordinates =  '53.456636N -2.214244E'
aerosol_370.chemical_species = 'UVPM_370'

qc_flag_370 = dataset_out.createVariable('qc_flag_mass_concentration_of_UVPM_370_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag_370.type = 'byte'
qc_flag_370.dimension = 'time'
qc_flag_370.units = '1'
qc_flag_370.long_name = 'Data Quality flag' 
qc_flag_370.flag_values ='0b,1b,2b,3b' 
qc_flag_370.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

aerosol_470 = dataset_out.createVariable('mass_concentration_of_black_carbon_470_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
aerosol_470.type = 'float32'
aerosol_470.dimension = 'time' 
aerosol_470.practical_units ='ug m-3'
aerosol_470.Mass_Absorption_Cross_Section = '14.54 (m^2/g)'
aerosol_470.standard_name = 'mass_concentration_of_black_carbon_470_in_ambient_aerosol_particles_in_air' 
aerosol_470.long_name = 'Mass concentration of the Black Carbon (measured at 470nm wavelength) component of ambient aerosol particles in air'
aerosol_470.valid_min = aeth_Data['BC_470 (ug/m3)'].min()
aerosol_470.valid_max = aeth_Data['BC_470 (ug/m3)'].max()
aerosol_470.call_methods = 'time:mean'
aerosol_470.coordinates =  '53.456636N -2.214244E'
aerosol_470.chemical_species = 'BC_470'

qc_flag_470 = dataset_out.createVariable('qc_flag_mass_concentration_of_black_carbon_470_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag_470.type = 'byte'
qc_flag_470.dimension = 'time'
qc_flag_470.units = '1'
qc_flag_470.long_name = 'Data Quality flag' 
qc_flag_470.flag_values ='0b,1b,2b,3b' 
qc_flag_470.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

aerosol_520 = dataset_out.createVariable('mass_concentration_of_black_carbon_520_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
aerosol_520.type = 'float32'
aerosol_520.dimension = 'time' 
aerosol_520.practical_units ='ug m-3'
aerosol_520.Mass_Absorption_Cross_Section = '13.14 (m^2/g)'
aerosol_520.standard_name = 'mass_concentration_of_black_carbon_520_in_ambient_aerosol_particles_in_air' 
aerosol_520.long_name = 'Mass concentration of the Black Carbon (measured at 520nm wavelength) component of ambient aerosol particles in air'
aerosol_520.valid_min = aeth_Data['BC_520 (ug/m3)'].min()
aerosol_520.valid_max = aeth_Data['BC_520 (ug/m3)'].max()
aerosol_520.call_methods = 'time:mean'
aerosol_520.coordinates =  '53.456636N -2.214244E'
aerosol_520.chemical_species = 'BC_520'

qc_flag_520 = dataset_out.createVariable('qc_flag_mass_concentration_of_black_carbon_520_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag_520.type = 'byte'
qc_flag_520.dimension = 'time'
qc_flag_520.units = '1'
qc_flag_520.long_name = 'Data Quality flag' 
qc_flag_520.flag_values ='0b,1b,2b,3b' 
qc_flag_520.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

aerosol_590 = dataset_out.createVariable('mass_concentration_of_black_carbon_590_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
aerosol_590.type = 'float32'
aerosol_590.dimension = 'time' 
aerosol_590.practical_units ='ug m-3'
aerosol_590.Mass_Absorption_Cross_Section = '11.58 (m^2/g)'
aerosol_590.standard_name = 'mass_concentration_of_black_carbon_590_in_ambient_aerosol_particles_in_air' 
aerosol_590.long_name = 'Mass concentration of the Black Carbon (measured at 590nm wavelength) component of ambient aerosol particles in air'
aerosol_590.valid_min = aeth_Data['BC_590 (ug/m3)'].min()
aerosol_590.valid_max = aeth_Data['BC_590 (ug/m3)'].max()
aerosol_590.call_methods = 'time:mean'
aerosol_590.coordinates =  '53.456636N -2.214244E'
aerosol_590.chemical_species = 'BC_590'


qc_flag_590 = dataset_out.createVariable('qc_flag_mass_concentration_of_black_carbon_590_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag_590.type = 'byte'
qc_flag_590.dimension = 'time'
qc_flag_590.units = '1'
qc_flag_590.long_name = 'Data Quality flag' 
qc_flag_590.flag_values ='0b,1b,2b,3b' 
qc_flag_590.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'


aerosol_660 = dataset_out.createVariable('mass_concentration_of_black_carbon_660_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
aerosol_660.type = 'float32'
aerosol_660.dimension = 'time' 
aerosol_660.practical_units ='ug m-3'
aerosol_660.Mass_Absorption_Cross_Section = '10.35 (m^2/g)'
aerosol_660.standard_name = 'mass_concentration_of_black_carbon_660_in_ambient_aerosol_particles_in_air' 
aerosol_660.long_name = 'Mass concentration of the Black Carbon (measured at 660nm wavelength) component of ambient aerosol particles in air'
aerosol_660.valid_min = aeth_Data['BC_660 (ug/m3)'].min()
aerosol_660.valid_max = aeth_Data['BC_660 (ug/m3)'].max()
aerosol_660.call_methods = 'time:mean'
aerosol_660.coordinates =  '53.456636N -2.214244E'
aerosol_660.chemical_species = 'BC_660'


qc_flag_660 = dataset_out.createVariable('qc_flag_mass_concentration_of_black_carbon_660_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag_660.type = 'byte'
qc_flag_660.dimension = 'time'
qc_flag_660.units = '1'
qc_flag_660.long_name = 'Data Quality flag' 
qc_flag_660.flag_values ='0b,1b,2b,3b' 
qc_flag_660.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'


aerosol_950 = dataset_out.createVariable('mass_concentration_of_black_carbon_950_in_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
aerosol_950.type = 'float32'
aerosol_950.dimension = 'time' 
aerosol_950.practical_units ='ug m-3'
aerosol_950.Mass_Absorption_Cross_Section = '7.19 (m^2/g)'
aerosol_950.standard_name = 'mass_concentration_of_black_carbon_950_in_ambient_aerosol_particles_in_air' 
aerosol_950.long_name = 'Mass concentration of the Black Carbon (measured at 950nm wavelength) component of ambient aerosol particles in air'
aerosol_950.valid_min = aeth_Data['BC_950 (ug/m3)'].min()
aerosol_950.valid_max = aeth_Data['BC_950 (ug/m3)'].max()
aerosol_950.call_methods = 'time:mean'
aerosol_950.coordinates =  '53.456636N -2.214244E'
aerosol_950.chemical_species = 'BC_950'

qc_flag_950 = dataset_out.createVariable('qc_flag_mass_concentration_of_black_carbon_950_in_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag_950.type = 'byte'
qc_flag_950.dimension = 'time'
qc_flag_950.units = '1'
qc_flag_950.long_name = 'Data Quality flag' 
qc_flag_950.flag_values ='0b,1b,2b,3b' 
qc_flag_950.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

# this bit writes the data from the master dataframe to the variables
times[:] = aeth_Data['TimeSecondsSince'].values#nc.date2num(timeline[:],times.units)
day_of_year[:] = aeth_Data['day_year'].values
year[:] = aeth_Data['year'].values
month[:] = aeth_Data['month'].values
day[:] = aeth_Data['day'].values
hour[:] = aeth_Data['hour'].values
minute[:] = aeth_Data['minute'].values
second[:] = aeth_Data['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244
aerosol_880[:] = aeth_Data['BC Conc (ug/m3)']
aerosol_370[:] = aeth_Data['UVPM_370_nm (ug/m3)']
aerosol_470[:] = aeth_Data['BC_470 (ug/m3)']
aerosol_520[:] = aeth_Data['BC_520 (ug/m3)']
aerosol_590[:] = aeth_Data['BC_590 (ug/m3)']
aerosol_660[:] = aeth_Data['BC_660 (ug/m3)']
aerosol_950[:] = aeth_Data['BC_950 (ug/m3)']
Flag_BC_Byte = np.array(aeth_Data['qc_flag_BC']).astype(np.ubyte)
qc_flag_880[:] = Flag_BC_Byte
Flag_370_Byte = np.array(aeth_Data['qc_flag_UVPM']).astype(np.ubyte)
qc_flag_370[:] = Flag_370_Byte
Flag_470_Byte = np.array(aeth_Data['qc_flag_BC_470']).astype(np.ubyte)
qc_flag_470[:] = Flag_470_Byte
Flag_520_Byte = np.array(aeth_Data['qc_flag_BC_520']).astype(np.ubyte)
qc_flag_520[:] = Flag_520_Byte
Flag_590_Byte = np.array(aeth_Data['qc_flag_BC_590']).astype(np.ubyte)
qc_flag_590[:] = Flag_590_Byte
Flag_660_Byte = np.array(aeth_Data['qc_flag_BC_660']).astype(np.ubyte)
qc_flag_660[:] = Flag_660_Byte
Flag_950_Byte = np.array(aeth_Data['qc_flag_BC_950']).astype(np.ubyte)
qc_flag_950[:] = Flag_950_Byte

dataset_out.close()

