import os
from pprint import pprint
import configparser
import csv
import pprint as pprint

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

BASE_YEAR = 2012
END_YEAR = 2016
TIMESTEP_INCREMENT = 1
TIMESTEPS = range(BASE_YEAR, END_YEAR + 1, TIMESTEP_INCREMENT)

#####################################
# setup file locations and data files
#####################################

INPUT_FILES = os.path.join(BASE_PATH)
OUTPUT_DATA = os.path.join(BASE_PATH, 'final_output_data')

#####################################
# READ LOOK UP TABLE (LUT) DATA
#####################################

def read_pcd_data():
    """
    """
    pcd_data = []

    #2012####
    with open(os.path.join(INPUT_FILES, '2012', 'ofcoma.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        for line in reader:
            pcd_data.append({
                'postcode': line[0].replace(' ', ''),
                'nga_availability': line[6],
                'year': 2012
            })

    with open(os.path.join(INPUT_FILES, '2012', 'ofcomb.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        for line in reader:
            pcd_data.append({
                'postcode': line[0].replace(' ', ''),
                'nga_availability': line[6],
                'year': 2012
            })

    ####2013####
    with open(os.path.join(INPUT_FILES, '2013', 'ofcom-part1-fixed-broadband-postcode-level-data-2013.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        for line in reader:
            pcd_data.append({
                'postcode': line[0].replace(' ', ''),
                'nga_availability': line[6],
                'year': 2013
            })

    with open(os.path.join(INPUT_FILES, '2013', 'ofcom-part2-fixed-broadband-postcode-level-data-2013.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        for line in reader:
            pcd_data.append({
                'postcode': line[0].replace(' ', ''),
                'nga_availability': line[6],
                'year': 2013
            })

    ####2014####
    with open(os.path.join(INPUT_FILES, '2014', 'fixed_postcode_2014.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        for line in reader:
            pcd_data.append({
                'postcode': line[0].replace(' ', ''),
                'nga_availability': line[1], ### convert this to being a binary indicator, or do it later when with premises
                'year': 2014
            })

    ###2015####
    with open(os.path.join(INPUT_FILES, '2015', 'Fixed_Postcode_updated_01022016.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        for line in reader:
            pcd_data.append({
                'postcode': line[0].replace(' ', ''),
                'nga_availability': line[1], ### convert this to being a binary indicator, or do it later when with premises
                'year': 2015
            })

    ###2016####
    for filename in os.listdir(os.path.join(INPUT_FILES, '2016')):
        with open(os.path.join(INPUT_FILES, '2016', filename), 'r', encoding='utf8', errors='replace') as system_file:
            reader = csv.reader(system_file)
            next(reader)
            for line in reader:
                pcd_data.append({
                    'postcode': line[0].replace(' ', ''),
                    'nga_availability': line[5], 
                    'year': 2016
                })

    return pcd_data

#####################################
# READ CODEPOINT 
#####################################

def read_codepoint():
    """
    """
    codepoint_data = []

    for year in TIMESTEPS:
        for filename in os.listdir(os.path.join(INPUT_FILES, 'codepoint', 'data')):
            with open(os.path.join(INPUT_FILES, 'codepoint', 'data', filename), 'r', encoding='utf8', errors='replace') as system_file:
                reader = csv.reader(system_file)
                #next(reader) no header
                for line in reader:
                    if line[18] == 'S':
                        codepoint_data.append({
                            'postcode': line[0].replace(' ', ''),
                            'delivery_points': line[3],
                            'type': line[18],
                            'year': year
                        })
                    else:
                        pass

    return codepoint_data

#####################################
# MERGE POSTCODES AND CODEPOINT
#####################################

# def merge_postcodes_and_codepoint(postcode_data, codepoint_data):
    
#     for postcode, postcode_codepoint in zip(postcode_data, codepoint_data):
#         postcode.update(postcode_codepoint)
    
#     return postcode_data

#####################################
# MERGE POSTCODES AND CODEPOINT
#####################################

def merge_two_lists_of_dicts(list_of_dicts_1, list_of_dicts_2, parameter1, parameter2):
    """
    Combine the list of dicts 1 and with list of dicts 2 using the household indicator and year keys. 
    """
    d1 = {(d[parameter1], d[parameter2]):d for d in list_of_dicts_2}

    list_of_dicts_1 = [dict(d, **d1.get((d[parameter1], d[parameter2]), {})) for d in list_of_dicts_1]	

    return list_of_dicts_1

#####################################
# PROCESS OFCOM AVAILABILITY INDICATORS
#####################################

def process_availability_indicators(data):

    for row in data:
        if row['year'] == 2012 or row['year'] == 2013:
            if row['nga_availability'] == 'Y':
                row['nga_availability'] = 1
            if row['nga_availability'] == 'N':
                row['nga_availability'] = 0     
    
    for row in data:
        if row['year'] == 2012 or row['year'] == 2013:
            try:
                row['premises_with_nga'] = (row['nga_availability']) * int(row['delivery_points'])
            except:
                pass

    for row in data:
        if not row['year'] == 2012 and not row['year'] == 2013:
            try:
                if int(row['nga_availability']) > 0:            
                    row['premises_with_nga'] = (row['nga_availability']/100) * int(row['delivery_points'])
                if int(row['nga_availability']) == 0:            
                    row['premises_with_nga'] = (row['nga_availability']/100) * int(row['delivery_points'])
            except:
                pass

    return data
#####################################
# PROCESS MSOA LUT 
#####################################

def read_msoa_lut():
    """
    """
    msoa_id_lut = []

    with open(os.path.join(INPUT_FILES, 'postcode_lookup', 'pcd_lookup.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        for line in reader:
            if line[5] not in msoa_id_lut:
                msoa_id_lut.append({
                    'msoa_id': line[5],
                })
    
    return msoa_id_lut

def write_msoa_lut(data):
    """
    """
    output_fieldnames = ['msoa_id']

    with open(os.path.join(INPUT_FILES, 'msoa_lookup', 'msoa_lookup.csv'), 'w') as csv_file:
        writer = csv.DictWriter(csv_file, output_fieldnames, lineterminator = '\n')
        writer.writeheader()
        writer.writerows(data)

#####################################
# READ LUT (ENG & WALES)
#####################################

def read_pcd_msoa_lut():
    """
    """
    lut_data = []

    for year in TIMESTEPS:
        with open(os.path.join(INPUT_FILES, 'postcode_lookup', 'pcd_lookup.csv'), 'r', encoding='utf8', errors='replace') as system_file:
            reader = csv.reader(system_file)
            next(reader)
            for line in reader:
                if len(line) > 1:
                    lut_data.append({
                        'postcode': line[0].replace(' ', ''),
                        'msoa_id': line[5],
                        'msoa_name': line[6],
                        'year': year
                    })

    return lut_data



#####################################
# WRITE DATA
#####################################

def csv_writer(data):
    """
    Write data to a CSV file path
    """

    for year in TIMESTEPS:
            
        output_name_year_files = {
            year: os.path.join(OUTPUT_DATA, 'nga_availability_{}.csv'.format(year))
        }    

        #print(output_name_year_files)

        output_fieldnames = ['postcode', 'nga_availability','year', 'delivery_points', 'type', 'premises_with_nga', 'msoa_id', 'msoa_name']

        #print(output_fieldnames)

        for filename in output_name_year_files.values():
            with open(filename, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, output_fieldnames, lineterminator = '\n')
                writer.writeheader()
                writer.writerows(data)

#####################################
# APPLY METHODS
#####################################

if __name__ == "__main__":
    
    # # Read Ofcom data
    # print('read_pcd_data')
    # pcd_data = read_pcd_data()

    # # Read codepoint
    # print('read_codepoint')
    # codepoint = read_codepoint()

    # # Merge postcodes and codepoint
    # print('Merging postcodes and codepoint postcodes')
    # #pcd_data = merge_postcodes_and_codepoint(pcd_data, codepoint)
    # pcd_data = merge_two_lists_of_dicts(pcd_data, codepoint, 'postcode', 'year')

    # # Process availability indicators
    # print('Processing availability indicators') 
    # pcd_data = process_availability_indicators(pcd_data)

    # Read LUT
    #print('Read LUT')
    #my_lut = read_pcd_msoa_lut()
    
    #msoa_lookup = read_msoa_lut()
    
    #write_msoa_lut(msoa_lookup)

    #print(msoa_lookup)
    # print('Merging postcodes and msoa lut')
    # pcd_data = merge_two_lists_of_dicts(pcd_data, my_lut, 'postcode', 'year')

    # # Write LUTs
    # print('write data')
    # csv_writer(pcd_data)

    #print('script finished')


# my_data =[{'year':2012, 'pcd':'A', 'delivery_points':40, 'prems_covered':20, 'area': 'cambridge'},
#           {'year':2012, 'pcd':'B', 'delivery_points':40, 'prems_covered':40, 'area': 'cambridge'},
#           {'year':2012, 'pcd':'C', 'delivery_points':20, 'prems_covered':10, 'area': 'oxford'},
#           {'year':2012, 'pcd':'D', 'delivery_points':20, 'prems_covered':20, 'area': 'oxford'},
#           {'year':2013, 'pcd':'E', 'delivery_points':80, 'prems_covered':60, 'area': 'cambridge'},      
#           {'year':2013, 'pcd':'F', 'delivery_points':20, 'prems_covered':20, 'area': 'cambridge'},
#           {'year':2013, 'pcd':'G', 'delivery_points':50, 'prems_covered':40, 'area': 'oxford'},
#           {'year':2013, 'pcd':'H', 'delivery_points':80, 'prems_covered':60, 'area': 'oxford'},    
# ]

# msoa_areas = ['cambridge', 'oxford']

# BASE_YEAR = 2012
# END_YEAR = 2013
# TIMESTEP_INCREMENT = 1
# TIMESTEPS = range(BASE_YEAR, END_YEAR + 1, TIMESTEP_INCREMENT)

# for year in TIMESTEPS:
#     for msoa in msoa_areas:
#         for row in my_data:
#             if row['year'] == year:
#                 if row['area'] == msoa:
#                     row['percentage_coverage'] = (sum(row['prems_covered']) / sum(row['delivery_points']) ) * 100

# my_data =[{'year':2012, 'percentage_coverage':75, 'delivery_points':80, 'prems_covered':60, 'area': 'cambridge'},
#           {'year':2012, 'percentage_coverage':75, 'delivery_points':40, 'prems_covered':30, 'area': 'oxford'},
#           {'year':2013, 'percentage_coverage':80, 'delivery_points':100, 'prems_covered':80, 'area': 'cambridge'},      
#           {'year':2013, 'percentage_coverage':77, 'delivery_points':130, 'prems_covered':100, 'area': 'oxford'},
# ]


