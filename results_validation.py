import os
from pprint import pprint
import configparser
import csv

#####################################
# setup config path
#####################################

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

#####################################
# setup file locations and data files
#####################################

INPUT_FILES = os.path.join(BASE_PATH, 'final_output_data')
#OUTPUT_DATA = os.path.join(BASE_PATH, 'final_output_data')

#####################################
# setup yearly increments
#####################################

BASE_YEAR = 2012
END_YEAR = 2016
TIMESTEP_INCREMENT = 1
TIMESTEPS = range(BASE_YEAR, END_YEAR + 1, TIMESTEP_INCREMENT)

#####################################
# import data
#####################################

def import_results():
    """
    """
    msoa_data = []

    with open(os.path.join(INPUT_FILES, 'nga_availability.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        #reader = [next(reader) for x in range(N)]
        for line in reader:
            msoa_data.append({
                'year': int(line[0]),
                'msoa': line[1],
                'precentage_coverage': float(line[2]),
                'prems_covered': float(line[3]),
                'delivery_points': float(line[4]),
            })
    
    return msoa_data

#####################################
# read msoa lookup
#####################################

def read_msoa_lut():
    """
    """
    msoa_lut_data = []

    with open(os.path.join(INPUT_FILES, '..', 'msoa_lookup', 'msoa_lookup_england.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        for line in reader:
            msoa_lut_data.append(line[0])
   
    #msoa_lut_data.append('misc_msoa_key')

    return msoa_lut_data

#####################################
# select England
#####################################

def select_england(data, msoa_lut):
    """
    """
    england_data = []

    for msoa in msoa_lut:
        for row in data:
            if row['msoa'] == msoa:  
                #print(row)  
                england_data.append({
                    'year': row['year'],
                    'msoa': row['msoa'],
                    'precentage_coverage': row['precentage_coverage'],
                    'prems_covered': row['prems_covered'],
                    'delivery_points': row['delivery_points']
                })
        
    return england_data

#####################################
# aggregate data annually
#####################################

def aggregate_results_annually(data, annual_increments):
    """
    """
    annual_data = []

    for year in annual_increments:
        data_selection = [datum for datum in data if datum['year'] == year]
        prems_covered = sum(int(item['prems_covered']) for item in data_selection)
        delivery_points = sum(int(item['delivery_points']) for item in data_selection)     

        try:
            percentage_coverage = (prems_covered / delivery_points)* 100

        except ZeroDivisionError:
            percentage_coverage = 0

        annual_data.append ({
            'year': year,
            'percentage_coverage': round(percentage_coverage),
            'prems_covered': prems_covered,
            'delivery_points': delivery_points
        })

    return annual_data


#####################################
# apply functions
#####################################

if __name__ == "__main__":
    
    my_data = import_results()

    msoa_lut_data = read_msoa_lut()

    my_data = select_england(my_data, msoa_lut_data)

    my_data = aggregate_results_annually(my_data, TIMESTEPS)

    pprint(my_data)




