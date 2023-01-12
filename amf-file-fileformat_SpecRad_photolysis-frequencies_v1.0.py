
import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date
import datetime

#def check_times(allFiles):
direct = str(SpecRad_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

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


dataset_out = nc.Dataset(direct + 'spectral-radiometer_maqs_' + str(date_file_label) + '_photolysis-rates_' + str(validity_status) + '_' + str(version_number) + '.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.1'
dataset_out.source = 'Spectral Radiometer at Manchester Air Quality Site'
dataset_out.instrument_manufacturer = 'Ocean Optics Inc.'
dataset_out.instrument_model = 'FLAME-S-UV-VIS-ES'
dataset_out.instrument_serial_number = 'FLMS12526'
dataset_out.instrument_software = 'Man Fac'
dataset_out.instrument_software_version = 'v1.0'
dataset_out.creator_name = 'Dr Nathan Watson'
dataset_out.creator_email = 'nathan.watson@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-9096-0926'
dataset_out.institution = 'University of Manchester'
dataset_out.processing_software_url = 'https://github.com/naiwatson/OSCA/'
dataset_out.processing_software_version = str(version_number)
dataset_out.calibration_sensitivity = 'See Calibration Certificate'
dataset_out.calibration_certification_url = 'https://github.com/naiwatson/OSCA/blob/main/Specrad%20Calibration%20Cert.pdf'
dataset_out.sampling_interval = '6 seconds' 
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
dataset_out.title = 'Solar radiation and Photolysis Rates'
dataset_out.measurement_technique = 'The spectral radiometer (Metcon GmbH) provides a measurement of solar actinic radiation integrated over selected wavelength ranges by means of a filtered photomultiplier to produce the j(O1D) and j(NO2) photolysis rates'
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
times.valid_min = complete_Photolysis['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = complete_Photolysis['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
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
day_of_year.valid_min = complete_Photolysis['day_year'].min()
day_of_year.valid_max = complete_Photolysis['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = complete_Photolysis['year'].min()
year.valid_max = complete_Photolysis['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = complete_Photolysis['month'].min()
month.valid_max = complete_Photolysis['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = complete_Photolysis['day'].min()
day.valid_max = complete_Photolysis['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = complete_Photolysis['hour'].min()
hour.valid_max = complete_Photolysis['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = complete_Photolysis['minute'].min()
minute.valid_max = complete_Photolysis['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = complete_Photolysis['second'].min()
second.valid_max = complete_Photolysis['second'].max()


solar_actinic_flux = dataset_out.createVariable('solar_actinic_flux', np.float32, ('time',), fill_value=-1.00E+20)
solar_actinic_flux.type = 'float32'
solar_actinic_flux.dimension = 'time' 
solar_actinic_flux.practical_units ='W/m2'
solar_actinic_flux.standard_name = 'solar_actinic_flux' 
solar_actinic_flux.long_name = 'Solar Actinic Flux (280–420 nm)'
solar_actinic_flux.valid_min = complete_Photolysis['Solar Actinic Flux (W/m2)'].min()
solar_actinic_flux.valid_max = complete_Photolysis['Solar Actinic Flux (W/m2)'].max()
solar_actinic_flux.call_methods = 'time:mean'
solar_actinic_flux.coordinates =  '53.456636N -2.214244E'


photolysis_frequencies_jno2 = dataset_out.createVariable('photolysis_frequencies_jno2', np.float32, ('time',), fill_value=-1.00E+20)
photolysis_frequencies_jno2.type = 'float32'
photolysis_frequencies_jno2.dimension = 'time' 
photolysis_frequencies_jno2.practical_units ='s-1'
photolysis_frequencies_jno2.standard_name = 'photolysis_frequencies_jno2' 
photolysis_frequencies_jno2.long_name = 'Photolysis Frequencies (j(NO(2))'
photolysis_frequencies_jno2.valid_min = complete_Photolysis['JNO2 (s-1)'].min()
photolysis_frequencies_jno2.valid_max = complete_Photolysis['JNO2 (s-1)'].max()
photolysis_frequencies_jno2.call_methods = 'time:mean'
photolysis_frequencies_jno2.coordinates =  '53.456636N -2.214244E'


photolysis_frequencies_jo1d = dataset_out.createVariable('photolysis_frequencies_jo1d', np.float32, ('time',), fill_value=-1.00E+20)
photolysis_frequencies_jo1d.type = 'float32'
photolysis_frequencies_jo1d.dimension = 'time' 
photolysis_frequencies_jo1d.practical_units ='s-1'
photolysis_frequencies_jo1d.standard_name = 'photolysis_frequencies_jo1d' 
photolysis_frequencies_jo1d.long_name = 'Photolysis Frequencies (j(O(1))(D))'
photolysis_frequencies_jo1d.valid_min = complete_Photolysis['JO1D (s-1)'].min()
photolysis_frequencies_jo1d.valid_max = complete_Photolysis['JO1D (s-1)'].max()
photolysis_frequencies_jo1d.call_methods = 'time:mean'
photolysis_frequencies_jo1d.coordinates =  '53.456636N -2.214244E'


#photolysis_frequencies_jhcho = dataset_out.createVariable('photolysis_frequencies_jhcho', np.float32, ('time',), fill_value=-1.00E+20)
#photolysis_frequencies_jhcho.type = 'float32'
#photolysis_frequencies_jhcho.dimension = 'time' 
#photolysis_frequencies_jhcho.practical_units ='s-1'
#photolysis_frequencies_jhcho.standard_name = 'photolysis_frequencies_jhcho2' 
#photolysis_frequencies_jhcho.long_name = 'Photolysis Frequencies (j(HCHO))'
#photolysis_frequencies_jhcho.valid_min = complete_Photolysis['JHCHO (s-1)'].min()
#photolysis_frequencies_jhcho.valid_max = complete_Photolysis['JHCHO (s-1)'].max()
#photolysis_frequencies_jhcho.call_methods = 'time:mean'
#photolysis_frequencies_jhcho.coordinates =  '53.456636N -2.214244E'


#photolysis_frequencies_jhono = dataset_out.createVariable('photolysis_frequencies_jhono', np.float32, ('time',), fill_value=-1.00E+20)
#photolysis_frequencies_jhono.type = 'float32'
#photolysis_frequencies_jhono.dimension = 'time' 
#photolysis_frequencies_jhono.practical_units ='s-1'
#photolysis_frequencies_jhono.standard_name = 'photolysis_frequencies_jhono' 
#photolysis_frequencies_jhono.long_name = 'Photolysis Frequencies (j(HONO))'
#photolysis_frequencies_jhono.valid_min = complete_Photolysis['JHONO (s-1)'].min()
#photolysis_frequencies_jhono.valid_max = complete_Photolysis['JHONO (s-1)'].max()
#photolysis_frequencies_jhono.call_methods = 'time:mean'
#photolysis_frequencies_jhono.coordinates =  '53.456636N -2.214244E'


qc_flag = dataset_out.createVariable('qc_flags', 'b', ('time',))
qc_flag.type = 'byte'
qc_flag.dimension = 'time'
qc_flag.units = '1'
qc_flag.long_name = 'Data Quality flag' 
qc_flag.flag_values ='0b,1b,2b,3b' 
qc_flag.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'

times[:] = complete_Photolysis['TimeSecondsSince'].values#nc.date2num(timeline[:],times.units)
day_of_year[:] = complete_Photolysis['day_year'].values
year[:] = complete_Photolysis['year'].values
month[:] = complete_Photolysis['month'].values
day[:] = complete_Photolysis['day'].values
hour[:] = complete_Photolysis['hour'].values
minute[:] = complete_Photolysis['minute'].values
second[:] = complete_Photolysis['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244
solar_actinic_flux[:] = complete_Photolysis['Solar Actinic Flux (W/m2)'].values
photolysis_frequencies_jno2[:] = complete_Photolysis['JNO2 (s-1)'].values
photolysis_frequencies_jo1d[:] = complete_Photolysis['JO1D (s-1)'].values
#photolysis_frequencies_jhcho[:] = complete_Photolysis['JHCHO (s-1)'].values
#photolysis_frequencies_jhono[:] = complete_Photolysis['JHONO (s-1)'].values
Flag_actinic_Byte = np.array(complete_Photolysis['qc_Flags']).astype(np.ubyte)
qc_flag[:] = Flag_actinic_Byte

dataset_out.close()
