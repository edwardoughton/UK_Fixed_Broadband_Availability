#####################################
# PROCESS MSOA LUT 
#####################################
import os
import configparser
import csv

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

#####################################
# setup file locations and data files
#####################################

INPUT_FILES = os.path.join(BASE_PATH)
OUTPUT_DATA = os.path.join(BASE_PATH, 'final_output_data')

#####################################
# READ LOOK UP TABLE (LUT) DATA
#####################################

def read_msoa_lut():
    """
    """
    msoa_id_lut = []

    with open(os.path.join(INPUT_FILES, 'england_postcode_lookup', 'PCD11_OA11_LSOA11_MSOA11_LAD11_EW_LU_aligned_v2.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        for line in reader:

            if(len(line) < 1): # check for blank lines
                continue

            msoa_id_lut.append({
                'msoa_id': line[5],
                'msoa_name': line[6],
                #'lad_id': line[7],
                #'lad_name': line[8]
            })

    with open(os.path.join(INPUT_FILES, 'scotland_postcode_lookup', 'Postcode lookup (revised 100113).csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        for line in reader:
            msoa_id_lut.append({
                'msoa_id': line[14],
                'msoa_name': line[15],
                #'lad_id': line[16],
                #'lad_name': line[17]
            })
    
    return msoa_id_lut

#####################################
# WRITE LOOK UP TABLE (LUT) DATA
#####################################

def write_msoa_lut(data):
    """
    """
    #output_fieldnames = ['msoa_id', 'msoa_name', 'lad_id', 'lad_name']
    output_fieldnames = ['msoa_id', 'msoa_name']

    with open(os.path.join(INPUT_FILES, 'msoa_lookup', 'msoa_lookup.csv'), 'w') as csv_file:
        writer = csv.DictWriter(csv_file, output_fieldnames, lineterminator = '\n')
        writer.writeheader()
        writer.writerows(data)

#####################################
# GET LIST OF UNIQUE DICTS IN LIST
#####################################

def unique_dicts(data, id_variable):

    unique_lookup_entries = list({v[id_variable]:v for v in data}.values())

    return unique_lookup_entries

#####################################
# APPLY METHODS
#####################################

if __name__ == "__main__":

    print('reading msoa lut')
    msoa_lookup = read_msoa_lut()
    
    print('find unique dicts')
    msoa_lookup = unique_dicts(msoa_lookup, 'msoa_id')

    print('writing unique lut entries to csv')
    write_msoa_lut(msoa_lookup)

    print('script finished')