

import pandas as pd
import netCDF4 as nc
import datetime 
import glob
import numpy as np
from datetime import date
import datetime

#def check_times(allFiles):
version_number = 'v2.1' # version of the code 
direct = str(CPC_Folder) #'C:/Users/mbexknm5/Dropbox/Python_Scripts/'

today = date.today()
current_month = today.strftime("%B %Y")
month_studied = start.strftime("%B %Y")

#print(str(start_year_month_str))

if float(start_year_month_str) < 201906:
    if float(start_year_month_str) < 201812:
        sys.exit("Error Message: This program cannot be used for data prior to December 2018.")
    else:
        sys.exit("Error Message: This is Data measured from Simon Building. Just process to CSV, not to be converted to netCDF.")
elif float(start_year_month_str) == 202102 or float(start_year_month_str) == 202110 or float(start_year_month_str) == 202111 or float(start_year_month_str) == 202112 or float(start_year_month_str) == 202209:
    pass
else:
    sys.exit("Error Message: This program is only used for data where there are multiple CPCs used during the same month.")

cal_cert_1 = 'https://github.com/redoverit/OSCA/blob/main/TSI%203750-CEN%20certificates.pdf'
cal_cert_2 = 'https://github.com/naiwatson/OSCA/blob/main/TSI%203772%20CPC%20Cal%20certificates.pdf'
cal_cert_3 = 'unknown'

if Total_CPC_2_Serial_No == instrument_serial_no_1:
    current_instrument_model = instrument_model_1
    current_model_full = instrument_model_full_1
    current_serial_no = instrument_serial_no_1
    cal_cert = cal_cert_1
elif Total_CPC_2_Serial_No == instrument_serial_no_2:
    current_instrument_model = instrument_model_2
    current_model_full = instrument_model_full_2
    current_serial_no = instrument_serial_no_2
    cal_cert = cal_cert_2
elif Total_CPC_2_Serial_No == instrument_serial_no_3:
    current_instrument_model = instrument_model_3
    current_model_full = instrument_model_full_3
    current_serial_no = instrument_serial_no_3
    cal_cert = cal_cert_3
else:
    sys.exit("Error Message: No Serial number registered.")

print()

if float(start_year_month_str) == 202102:
    date_file_label = '20210210-to-20210228 ' #convert to 20210201-to-20210210 and 20210210-to-20210228 files
elif float(start_year_month_str) == 202110:
    date_file_label = '20211027-to-20211031' #convert to 20211001-to-20211027 and 20211027-to-20211031
elif float(start_year_month_str) == 202111:
    date_file_label = '20211010-to-20211030' #convert to 20211001-to-20211110 and 20211010-to-20211030
elif float(start_year_month_str) == 202112:
    date_file_label = '20211209-to-20212031' #convert to 20211201-to-20211209 and 20211209-to-20212031
elif float(start_year_month_str) == 202209:
    date_file_label = '20220901-to-20220930' #
else:
    pass

print(str(cal_cert))

dataset_out = nc.Dataset(direct + 'CPC-' + str(current_instrument_model) + '_maqs_' + str(date_file_label) + '_aerosol-concentration' + str(status) + str(version_number) + '.1.nc', 'w', format='NETCDF4_CLASSIC')

dataset_out.Conventions = 'CF-1.6, NCAS-AMF-1.1'
dataset_out.source = 'maqs-CPC-' + str(current_instrument_model) + '-1'
dataset_out.instrument_manufacturer = 'Thermo Systems Incorporated (TSI)'
dataset_out.instrument_model = 'Condensation Particle Counter ' + str(current_model_full)
dataset_out.instrument_serial_number = str(current_serial_no)
dataset_out.instrument_software = 'unknown'
dataset_out.instrument_software_version = 'unknown'
dataset_out.creator_name = 'Dr Nathan Watson'
dataset_out.creator_email = 'nathan.watson@manchester.ac.uk'
dataset_out.creator_url = 'https://orcid.org/0000-0001-9096-0926'
dataset_out.institution = 'University of Manchester'
dataset_out.processing_software_url = 'https://github.com/redoverit/OSCA/'
dataset_out.processing_software_version = str(version_number)
dataset_out.calibration_sensitivity = 'not known'
dataset_out.calibration_certification_url = str(cal_cert)
dataset_out.sampling_interval = '1 second' #confirmed
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
times.valid_min = Total_CPC_2_Data['TimeSecondsSince'][0]#(timeline[0]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
times.valid_max = Total_CPC_2_Data['TimeSecondsSince'][-1]#(timeline[-1]-datetime.datetime(1970,1,1,0,0,0)).total_seconds()
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
day_of_year.valid_min = Total_CPC_2_Data['day_year'].min()
day_of_year.valid_max = Total_CPC_2_Data['day_year'].max()

year = dataset_out.createVariable('year', np.int16, ('time',))
#year.name = 'year'
year.type = 'int'
year.dimension = 'time'
year.units = 1
year.standard_name = ''
year.long_name = 'Year'
year.valid_min = Total_CPC_2_Data['year'].min()
year.valid_max = Total_CPC_2_Data['year'].max()

month = dataset_out.createVariable('month', np.int16, ('time',))
#month.name = 'month'
month.type = 'int'
month.dimension = 'time'
month.units = 1
month.standard_name = ''
month.long_name = 'Month'
month.valid_min = Total_CPC_2_Data['month'].min()
month.valid_max = Total_CPC_2_Data['month'].max()

day = dataset_out.createVariable('day', np.int16, ('time',))
#day.name = 'day'
day.type = 'int'
day.dimension = 'time'
day.units = 1
day.standard_name = ''
day.long_name = 'Day'
day.valid_min = Total_CPC_2_Data['day'].min()
day.valid_max = Total_CPC_2_Data['day'].max()

hour = dataset_out.createVariable('hour', np.int16, ('time',))
#hour.name = 'hour'
hour.type = 'int'
hour.dimension = 'time'
hour.units = 1
hour.standard_name = ''
hour.long_name = 'Hour'
hour.valid_min = Total_CPC_2_Data['hour'].min()
hour.valid_max = Total_CPC_2_Data['hour'].max()

minute = dataset_out.createVariable('minute', np.int16, ('time',))
#minute.name = 'minute'
minute.type = 'int'
minute.dimension = 'time'
minute.units = 1
minute.standard_name = ''
minute.long_name = 'minute'
minute.valid_min = Total_CPC_2_Data['minute'].min()
minute.valid_max = Total_CPC_2_Data['minute'].max()

second = dataset_out.createVariable('second', np.float64, ('time',))
#second.name = 'second'
second.type = 'double'
second.dimension = 'time'
second.units = 1
second.standard_name = ''
second.long_name = 'second'
second.valid_min = Total_CPC_2_Data['second'].min()
second.valid_max = Total_CPC_2_Data['second'].max()


aerosol = dataset_out.createVariable('number_concentration_of_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00E+20)
aerosol.type = 'float32'
aerosol.dimension = 'time' 
aerosol.practical_units ='cm-3'
aerosol.standard_name = 'number_concentration_of_ambient_aerosol_particles_in_air' 
aerosol.long_name = 'Number Concentration of Ambient Aerosol Particles in air'
aerosol.valid_min = Total_CPC_2_Data['Conc (#/cc)'].min()
aerosol.valid_max = Total_CPC_2_Data['Conc (#/cc)'].max()
aerosol.call_methods = 'time:mean'
aerosol.coordinates =  '53.456636N -2.214244E'
aerosol.chemical_species = '##cc'

qc_flag = dataset_out.createVariable('qc_flag_number_concentration_of_ambient_aerosol_particles_in_air', 'b', ('time',))
qc_flag.type = 'byte'
qc_flag.dimension = 'time'
qc_flag.units = '1'
qc_flag.long_name = 'Data Quality flag' 
qc_flag.flag_values ='0b,1b,2b,3b' 
qc_flag.flag_meanings = '\n\rnot_used \n\rgood \n\rsuspect_data_bad_data_to_be_defined \n\rsuspect_data_time_stamp_error,'



# this bit writes the data from the master dataframe to the variables
times[:] = Total_CPC_2_Data['TimeSecondsSince'].values#nc.date2num(timeline[:],times.units)
day_of_year[:] = Total_CPC_2_Data['day_year'].values
year[:] = Total_CPC_2_Data['year'].values
month[:] = Total_CPC_2_Data['month'].values
day[:] = Total_CPC_2_Data['day'].values
hour[:] = Total_CPC_2_Data['hour'].values
minute[:] = Total_CPC_2_Data['minute'].values
second[:] = Total_CPC_2_Data['second'].values
latitudes[:] = 53.456636
longitudes[:] = -2.214244
aerosol[:] = Total_CPC_2_Data['Conc (#/cc)'].values
Flag_CPC_Byte = np.array(Total_CPC_2_Data['qc_flags']).astype(np.ubyte)
qc_flag[:] = Flag_CPC_Byte

dataset_out.close()
