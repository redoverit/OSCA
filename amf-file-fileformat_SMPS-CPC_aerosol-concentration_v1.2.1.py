
import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date
import datetime

#def check_times(allFiles):
direct = str(smps_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

today = date.today()
current_month = today.strftime("%B %Y")
month_studied = start.strftime("%B %Y")

#print(str(start_year_month_str))


if float(start_year_month_str) < 1906:
    if float(start_year_month_str) < 1812:
        sys.exit("Error Message: This program cannot be used for data prior to December 2018.")
    else:
        #pass
        sys.exit("Error Message: This is Data measured from Simon Building. Just process to CSV, not to be converted to netCDF.")
else:
    pass

cal_cert_1 = 'https://github.com/redoverit/OSCA/blob/main/TSI%203750-CEN%20certificates.pdf'
cal_cert_2 = 'https://github.com/naiwatson/OSCA/blob/main/TSI%203772%20CPC%20Cal%20certificates.pdf'
cal_cert_3 = 'unknown'

current_SMPS_model = '308200'
current_SMPS_no = '3082001807001'
smps_CPC_cal_cert = 'https://github.com/naiwatson/OSCA/blob/main/SMPS%20Calibration%20certs.pdf'
current_CPC_model = '375000'
current_CPC_no = '3750180701' 


dataset_out = nc.Dataset(direct + 'SMPS-' + str(current_SMPS_model) + '-CPC-' + str(current_CPC_model) + '_maqs_20' + str(date_file_label) + '_aerosol-size-distribution' + str(status) + str(version_number) + '.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.1'
dataset_out.source = 'maqs-SMPS_' + str(current_SMPS_model) + '-CPC_' + str(current_CPC_model) + '-1'
dataset_out.instrument_SMPS_manufacturer = 'Thermo Systems Incorporated (TSI)'
dataset_out.instrument_SMPS_model = 'Condensation Particle Counter ' + str(current_SMPS_model)
dataset_out.instrument_SMPS_serial_number = str(current_SMPS_no)
dataset_out.instrument_CPC_manufacturer = 'Thermo Systems Incorporated (TSI)'
dataset_out.instrument_CPC_model = 'Condensation Particle Counter ' + str(current_CPC_model) #
dataset_out.instrument_CPC_serial_number = str(current_CPC_no)
dataset_out.instrument_software = 'Aerosol Instrument Manager'
dataset_out.instrument_software_version = '10.3'
dataset_out.creator_name = 'Dr Nathan Watson'
dataset_out.creator_email = 'nathan.watson@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-9096-0926'
dataset_out.institution = 'University of Manchester'
dataset_out.processing_software_url = 'https://github.com/naiwatson/OSCA/'
dataset_out.processing_software_version = str(version_number)
dataset_out.calibration_SMPS_CPC_sensitivity = 'not known'
dataset_out.calibration_SMPS_CPC_certification_url = str(smps_CPC_cal_cert)
dataset_out.sampling_interval = '5 minutes' 
dataset_out.averaging_interval = '5 minutes'
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
dataset_out.title = 'Ambient Aerosol Size Distribution in air'
dataset_out.measurement_technique = 'Measurement technique that the instrument employs is: Electrostatic Mobility'
dataset_out.featureType = 'timeSeries'
dataset_out.time_coverage_start = start.strftime('%Y-%m-%dT%H:%M:%S')
dataset_out.time_coverage_end = end.strftime('%Y-%m-%d %HT%M:%S')
dataset_out.geospatial_bounds = '53.456636N -2.214244E'
dataset_out.platform_altitude = '50 m'
dataset_out.location_keywords = 'MAQS, Supersite, Firs, Fallowfield'
dataset_out.amf_vocabularies_release = 'https://github.com/ncasuk/AMF_CVs/releases/tag/v1.0.0'
dataset_out.history = ' Acquired ' + str(month_studied) + ' and Data processed ' + str(current_month)
dataset_out.comment = 'Measurement Height 7m above ground level'
min_dma_radius = 0.937 
max_dma_radius = 1.961 
length_dma = 44.369 
diameter_impactor = 0.0457
dataset_out.dma_inner_radius = 'Physical diameter of inner column: ' + str(min_dma_radius) + ' cm'
dataset_out.dma_outer_radius = 'Physical diameter of outer column: ' + str(max_dma_radius) + ' cm'
dataset_out.dma_length = 'Physical length of column: ' + str(length_dma) + ' cm'
dataset_out.impactor_orifice_diameter = 'Diameter of Impactor nozzle: ' + str(diameter_impactor) + ' cm'
dataset_out.lower_channel_cut_off = 'Theoretical lower size limit: ' + str(cut_off_low_channel) + 'e-9  m'
dataset_out.upper_channel_cut_off = 'Theoretical upper size limit: ' + str(cut_off_high_channel) + 'e-9 m'


# Dimensions
time_dim = dataset_out.createDimension('time',None) 
latitude_dim = dataset_out.createDimension('latitude',1)
longitude_dim = dataset_out.createDimension('longitude',1)
aerosol_dim = dataset_out.createDimension('ambient_aerosol_particle_diameter',int(last_column))
#measurement_technique = dataset_out.createDimension('measurement_technique',1)
#dma_inner_radius = dataset_out.createDimension('dma_inner_radius',1)
#dma_outer_radius = dataset_out.createDimension('dma_outer_radius',1)
#dma_length = dataset_out.createDimension('dma_length',1)
#impactor_orifice_diameter = dataset_out.createDimension('impactor_orifice_diameter',1)
#lower_channel_cut_off = dataset_out.createDimension('lower_channel_cut_off',1)
#upper_channel_cut_off = dataset_out.createDimension('upper_channel_cut_off',1)


# create variables (empty to begin with)

times = dataset_out.createVariable('time', np.float64, ('time',))
times.type = 'float64'
times.units = 'seconds since 1970-01-01T00:00:00'
times.long_name = 'Time (seconds since 1970-01-01 00:00:00)'
times.axis = 'T'
times.valid_min = smps['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = smps['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
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

ambient_aerosol_particle_diameter = dataset_out.createVariable('ambient_aerosol_particle_diameter', np.float32, ('ambient_aerosol_particle_diameter',))
ambient_aerosol_particle_diameter.type = 'float64' 
ambient_aerosol_particle_diameter.units = 'nm'
ambient_aerosol_particle_diameter.standard_name = 'ambient_aerosol_particle_diameter' 
ambient_aerosol_particle_diameter.long_name = 'Ambient Aerosol Particle Diameter'
ambient_aerosol_particle_diameter.valid_min = float(Smallest_Aerosol)
ambient_aerosol_particle_diameter.valid_max = float(Largest_Aerosol)


day_of_year = dataset_out.createVariable('day_of_year', np.float32, ('time',))
day_of_year.type = 'float32'
day_of_year.dimension = 'time'
day_of_year.units = '1'
day_of_year.standard_name = ''
day_of_year.long_name = 'Day of Year'
day_of_year.valid_min = smps['day_year'].min()
day_of_year.valid_max = smps['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = smps['year'].min()
year.valid_max = smps['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = smps['month'].min()
month.valid_max = smps['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = smps['day'].min()
day.valid_max = smps['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = smps['hour'].min()
hour.valid_max = smps['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = smps['minute'].min()
minute.valid_max = smps['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = smps['second'].min()
second.valid_max = smps['second'].max()


times[:] = smps['TimeSecondsSince'].values#nc.date2num(timeline[:],times.units)
day_of_year[:] = smps['day_year'].values
year[:] = smps['year'].values
month[:] = smps['month'].values
day[:] = smps['day'].values
hour[:] = smps['hour'].values
minute[:] = smps['minute'].values
second[:] = smps['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244
raw_smps_data = smps.iloc[:,int(first_column):int(last_column)]
raw_smps_data.iloc[-1] = raw_smps_data.columns #smps.iloc[:,int(first_column):int(last_column)]

ambient_aerosol_particle_diameter[:] = raw_smps_data.iloc[-1,int(first_column):int(last_column)] # smps.iloc[:,int(first_column):int(last_column)]
smps.drop(smps[(smps['Sample Temp (C)'] == 'Sample Temp (C)')].index,inplace =True)
#ambient_aerosol_particle_diameter[:] = data_smps_labels.loc['Label_pt_2'] 
#dma_inner_radius[:] = 0.937
#dma_outer_radius[:] = 19.58
#dma_length[:] = 44.44
#impactor_orifice_diameter[:] = 0.0457
#lower_channel_cut_off[:] = 14.6e-9
#upper_channel_cut_off[:] = 661.2e-9

#smps.iloc[int(first_column):int(last_column)]

#print(smps.iloc[:,1:107])
smps.iloc[:,int(first_column):int(last_column)] = smps.iloc[:,int(first_column):int(last_column)].astype(float)
smps['qc_Flags'] = smps['qc_Flags'].astype(str)
#print(smps.iloc[:,int(first_column):int(last_column)])
#print(smps.iloc[:,int(first_column):int(last_column)].min())
#print((smps.iloc[:,int(first_column):int(last_column)].max()).max())

distribution = dataset_out.createVariable('ambient_aerosol_size_distribution', np.float32, ('time', 'ambient_aerosol_particle_diameter',), fill_value=-1.00E+20) 
distribution.type = 'float32'
distribution.dimension = 'time'
distribution.practical_units = 'cm3-1 um-1'
distribution.standard_name = 'ambient_aerosol_size_distribution'
distribution.long_name = 'Ambient Aerosol Size Distribution'
distribution.valid_min = (smps.iloc[:,int(first_column):int(last_column)].min()).min()
distribution.valid_max = (smps.iloc[:,int(first_column):int(last_column)].max()).max() 
distribution.call_methods = 'time:mean'
distribution.coordinates =  '53.456636N -2.214244E'
distribution[:] = smps.iloc[:,int(first_column):int(last_column)]


total_number_concentration_of_ambient_aerosol_particles_in_air = dataset_out.createVariable('total_number_concentration_of_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
total_number_concentration_of_ambient_aerosol_particles_in_air.type = 'float32'
total_number_concentration_of_ambient_aerosol_particles_in_air.dimension = 'time' 
total_number_concentration_of_ambient_aerosol_particles_in_air.practical_units ='(##/cm^3)'
total_number_concentration_of_ambient_aerosol_particles_in_air.standard_name = 'total_number_concentration_of_ambient_aerosol_particles_in_air' 
total_number_concentration_of_ambient_aerosol_particles_in_air.long_name = 'Number Concentration of Ambient Aerosol Particles in air (N)'
total_number_concentration_of_ambient_aerosol_particles_in_air.valid_min = smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'].min()
total_number_concentration_of_ambient_aerosol_particles_in_air.valid_max = smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'].max()
total_number_concentration_of_ambient_aerosol_particles_in_air.call_methods = 'time:mean'
total_number_concentration_of_ambient_aerosol_particles_in_air.coordinates =  '53.456636N -2.214244E'
total_number_concentration_of_ambient_aerosol_particles_in_air[:] = smps['Number Concentration of Ambient Aerosol Particles in air (##/cm^3)'].values

ambient_aerosol_particle_diameter = dataset_out.createVariable('ambient_geometric_mean_aerosol_particle_diameter', np.float32, ('time',), fill_value=-1.00E+20)
ambient_aerosol_particle_diameter.type = 'float32'
ambient_aerosol_particle_diameter.dimension = 'time' 
ambient_aerosol_particle_diameter.practical_units ='nm'
ambient_aerosol_particle_diameter.standard_name = 'ambient_geometric_mean_aerosol_particle_diameter' 
ambient_aerosol_particle_diameter.long_name = 'Ambient Geometric Mean Aerosol Particle Diameter'
ambient_aerosol_particle_diameter.valid_min = smps['Geometric Mean (nm)'].min()
ambient_aerosol_particle_diameter.valid_max = smps['Geometric Mean (nm)'].max()
ambient_aerosol_particle_diameter.call_methods = 'time:mean'
ambient_aerosol_particle_diameter.coordinates =  '53.456636N -2.214244E'
ambient_aerosol_particle_diameter[:] = smps['Geometric Mean (nm)'].values


sample_pressure = dataset_out.createVariable('sample_pressure', np.float32, ('time',), fill_value=-1.00E+20)
sample_pressure.type = 'float32'
sample_pressure.dimension = 'time' 
sample_pressure.practical_units ='kPa'
sample_pressure.standard_name = 'sample_pressure' 
sample_pressure.long_name = 'Pressure of Sample Stream'
sample_pressure.valid_min = smps['Sample Pressure (kPa)'].min()
sample_pressure.valid_max = smps['Sample Pressure (kPa)'].max()
sample_pressure.call_methods = 'time:mean'
sample_pressure.coordinates =  '53.456636N -2.214244E'
sample_pressure[:] = smps['Sample Pressure (kPa)'].values

sample_temperature = dataset_out.createVariable('sample_temperature', np.float32, ('time',), fill_value=-1.00E+20)
sample_temperature.type = 'float32'
sample_temperature.dimension = 'time' 
sample_temperature.practical_units ='K'
sample_temperature.standard_name = 'sample_temperature' 
sample_temperature.long_name = 'Temperature of Sample Stream'
sample_temperature.valid_min = smps['Sample Temp (K)'].min()
sample_temperature.valid_max = smps['Sample Temp (K)'].max()
sample_temperature.call_methods = 'time:mean'
sample_temperature.coordinates =  '53.456636N -2.214244E'
sample_temperature[:] = smps['Sample Temp (K)'].values

sample_mean_free_path = dataset_out.createVariable('sample_mean_free_path', np.float32, ('time',), fill_value=-1.00E+20)
sample_mean_free_path.type = 'float32'
sample_mean_free_path.dimension = 'time' 
sample_mean_free_path.practical_units ='m'
sample_mean_free_path.standard_name = 'sample_mean_free_path' 
sample_mean_free_path.long_name = 'Mean Free Path of Sample Stream'
sample_mean_free_path.valid_min = smps['Mean Free Path (m)'].min()
sample_mean_free_path.valid_max = smps['Mean Free Path (m)'].max()
sample_mean_free_path.call_methods = 'time:mean'
sample_mean_free_path.coordinates =  '53.456636N -2.214244E'
sample_mean_free_path[:] = smps['Mean Free Path (m)'].values

sample_gas_viscosity = dataset_out.createVariable('sample_gas_viscosity', np.float32, ('time',), fill_value=-1.00E+20)
sample_gas_viscosity.type = 'float32'
sample_gas_viscosity.dimension = 'time' 
sample_gas_viscosity.practical_units ='Pa*s'
sample_gas_viscosity.standard_name = 'sample_gas_viscosity' 
sample_gas_viscosity.long_name = 'Gas Viscosity of Sample Stream'
sample_gas_viscosity.valid_min = smps['Gas Viscosity (Pa*s)'].min()
sample_gas_viscosity.valid_max = smps['Gas Viscosity (Pa*s)'].max()
sample_gas_viscosity.call_methods = 'time:mean'
sample_gas_viscosity.coordinates =  '53.456636N -2.214244E'
sample_gas_viscosity[:] = smps['Gas Viscosity (Pa*s)'].values

qc_flag = dataset_out.createVariable('qc_flags', 'b', ('time',))
qc_flag.type = 'byte'
qc_flag.dimension = 'time'
qc_flag.units = '1'
qc_flag.long_name = 'Data Quality flag' 
qc_flag.flag_values ='0b,1b,2b,3b' 
qc_flag.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'
Flag_SMPS_Byte = np.array(smps['qc_Flags']).astype(np.ubyte)
qc_flag[:] = Flag_SMPS_Byte


dataset_out.close()

