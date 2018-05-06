import os
from pprint import pprint
import configparser
import csv

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

BASE_YEAR = 2012
END_YEAR = 2016
TIMESTEP_INCREMENT = 1
TIMESTEPS = range(BASE_YEAR, END_YEAR + 1, TIMESTEP_INCREMENT)
#N = 100000

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

    2012####
    with open(os.path.join(INPUT_FILES, '2012', 'ofcoma.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        #reader = [next(reader) for x in range(N)]
        for line in reader:
            pcd_data.append({
                'postcode': line[0].replace(' ', ''),
                'nga_availability': line[6],
                'year': 2012
            })

    with open(os.path.join(INPUT_FILES, '2012', 'ofcomb.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        #reader = [next(reader) for x in range(N)]
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
        #reader = [next(reader) for x in range(N)]
        for line in reader:
            pcd_data.append({
                'postcode': line[0].replace(' ', ''),
                'nga_availability': line[6],
                'year': 2013
            })

    with open(os.path.join(INPUT_FILES, '2013', 'ofcom-part2-fixed-broadband-postcode-level-data-2013.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        #reader = [next(reader) for x in range(N)]
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
        #reader = [next(reader) for x in range(N)]
        for line in reader:
            pcd_data.append({
                'postcode': line[0].replace(' ', ''),
                'nga_availability': line[1], ### convert this to being a binary indicator, or do it later when with premises
                'year': 2014
            })

    ##2015####
    with open(os.path.join(INPUT_FILES, '2015', 'Fixed_Postcode_updated_01022016.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        #reader = [next(reader) for x in range(N)]
        for line in reader:
            pcd_data.append({
                'postcode': line[0].replace(' ', ''),
                'nga_availability': line[1], ### convert this to being a binary indicator, or do it later when with premises
                'year': 2015
            })

    2016###
    for filename in os.listdir(os.path.join(INPUT_FILES, '2016')):
        with open(os.path.join(INPUT_FILES, '2016', filename), 'r', encoding='utf8', errors='replace') as system_file:
            reader = csv.reader(system_file)
            next(reader)
            # reader = [next(reader) for x in range(N)]
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
# READ POSTCODE LUT (ENG & WALES)
#####################################

def read_pcd_lut():
    """
    """
    pcd_lut_data = []

    for year in TIMESTEPS:
        with open(os.path.join(INPUT_FILES, 'postcode_lookup', 'PCD11_OA11_LSOA11_MSOA11_LAD11_EW_LU_aligned_v2.csv'), 'r', encoding='utf8', errors='replace') as system_file:
            reader = csv.reader(system_file)
            next(reader)
            for line in reader:

                if(len(line) < 1): # check for blank lines
                    continue

                pcd_lut_data.append({
                    'postcode': line[0].replace(' ', ''),
                    'msoa_id': line[5],
                    'msoa_name': line[6],
                    'year': year
                })

        with open(os.path.join(INPUT_FILES, 'scotland_postcode_lookup', 'Postcode lookup (revised 100113).csv'), 'r', encoding='utf8', errors='replace') as system_file:
            reader = csv.reader(system_file)
            next(reader)
            for line in reader:
                pcd_lut_data.append({
                    'postcode': line[0].replace(' ', ''),
                    'msoa_id': line[14],
                    'msoa_name': line[15],
                    'year': year
                })

    return pcd_lut_data

#####################################
# READ MSOA LUT (ENG & WALES)
#####################################

def read_msoa_lut():
    """
    """
    msoa_lut_data = []

    with open(os.path.join(INPUT_FILES, 'msoa_lookup', 'msoa_lookup.csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        for line in reader:
            msoa_lut_data.append(line[0])
   
    msoa_lut_data.append('misc_msoa_key')

    return msoa_lut_data

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
# ADD MISSING NGA_AVAILABILITY INDICATOR    
#####################################

def add_missing_nga_availability_keys(data):

    for element in data:
        if 'premises_with_nga' not in element:
            element['premises_with_nga'] = 0

    return data

#####################################
# ADD MISSING DELIVERY POINTS INDICATOR    
#####################################

def add_missing_delivery_points_keys(data):

    for element in data:
        if 'delivery_points' not in element:
            element['delivery_points'] = 0

    return data

#####################################
# ADD MISC MSOA FOR MISSING KEYS
#####################################

def add_missing_msoa_keys(data):

    for element in data:
        if 'msoa_id' not in element:
            element['msoa_id'] = 'misc_msoa_key'

    return data
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
                    row['premises_with_nga'] = (int(row['nga_availability'])/100) * int(row['delivery_points'])
                if int(row['nga_availability']) == 0:            
                    row['premises_with_nga'] = (int(row['nga_availability'])/100) * int(row['delivery_points'])                  
            except:
                print(row)
                raise Exception

    return data

    
#####################################
# READ LUT (ENG & WALES)
#####################################

def calculate_msoa_coverage(data, annual_increments, msoa_lut):
    """
    """
    msoa_coverage = []

    for year in annual_increments:
        for msoa in msoa_lut:
            data_selection = [datum for datum in data if datum['year'] == year and datum['msoa_id']== msoa]
  
            prems_covered = sum(item['premises_with_nga'] for item in data_selection)
            delivery_points = sum(int(item['delivery_points']) for item in data_selection)
        
            try:
                percentage_coverage = (prems_covered / delivery_points)* 100

            except ZeroDivisionError:
                percentage_coverage = 0

            msoa_coverage.append ({
                'year': year,
                'msoa': msoa, 
                'percentage_coverage': percentage_coverage,
                'prems_covered': prems_covered,
                'delivery_points': delivery_points
            })

    return msoa_coverage


#####################################
# WRITE DATA - SINGLE FILE PER YEAR
#####################################

def csv_writer_multifiles(data, output_fieldnames):
    """
    Write data to a CSV file path
    """

    for year in TIMESTEPS:
            
        output_name_year_files = {
            year: os.path.join(OUTPUT_DATA, 'nga_availability_{}.csv'.format(year))
        }    

        for filename in output_name_year_files.values():
            with open(filename, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, output_fieldnames, lineterminator = '\n')
                writer.writeheader()
                writer.writerows(data)

#####################################
# WRITE DATA - SINGLE FILE FOR ALL
#####################################

def csv_writer(data, output_fieldnames, filename):
    """
    Write data to a CSV file path
    """
    with open(os.path.join(OUTPUT_DATA, filename), 'w') as csv_file:
        writer = csv.DictWriter(csv_file, output_fieldnames, lineterminator = '\n')
        writer.writeheader()
        writer.writerows(data)

#####################################
# APPLY METHODS
#####################################

if __name__ == "__main__":
    
    ##############
    # READ
    ##############

    #Read Ofcom data
    print('read_pcd_data')
    pcd_data = read_pcd_data()

    # Read codepoint
    print('read_codepoint')
    codepoint = read_codepoint()

    # Read LUT
    print('Read postcode LUT')
    my_pcd_lut = read_pcd_lut()

    # Read LUT
    print('Read msoa LUT')
    my_msoa_lut = read_msoa_lut()

    ##############
    # MERGE AND PROCESS
    ##############

    # Merge postcodes and codepoint
    print('Merging postcodes and codepoint postcodes')
    #pcd_data = merge_postcodes_and_codepoint(pcd_data, codepoint)
    pcd_data = merge_two_lists_of_dicts(pcd_data, codepoint, 'postcode', 'year')

    # Process availability indicators
    print('Adding any missing nga availability keys') 
    pcd_data = add_missing_nga_availability_keys(pcd_data)

    # Process availability indicators
    print('Adding any missing delivery points keys') 
    pcd_data = add_missing_delivery_points_keys(pcd_data)

    # Process availability indicators
    print('Processing availability indicators') 
    pcd_data = process_availability_indicators(pcd_data)

    # Merge postcodes and msoa lut 
    print('Merging postcodes and msoa lut')
    pcd_data = merge_two_lists_of_dicts(pcd_data, my_pcd_lut, 'postcode', 'year')
    
    # Add any missing msoa keys
    print('Adding any missing msoa keys')
    pcd_data = add_missing_msoa_keys(pcd_data)

    ##############
    # CALC COVERAGE
    ##############

    # Calculate coverage
    print('Calculating msoa coverage')
    msoa_coverage = calculate_msoa_coverage(pcd_data, TIMESTEPS, my_msoa_lut) 

    # #Write LUTs
    # #print('write postcode data')
    # #postcode_output_fieldnames = ['postcode', 'nga_availability','year', 'delivery_points', 'type', 'premises_with_nga', 'msoa_id', 'msoa_name']
    # #csv_writer(pcd_data, postcode_output_fieldnames, 'test.csv')

    # # Write LUTs
    print('write msoa data')
    msoa_output_fieldnames = ['year', 'msoa', 'percentage_coverage', 'prems_covered', 'delivery_points']
    csv_writer(msoa_coverage, msoa_output_fieldnames, 'nga_availability.csv')

    print('script finished')











    # my_data =[{'year':2012, 'pcd':'A', 'delivery_points':40, 'prems_covered':20, 'area': 'cambridge'},
    #         {'year':2012, 'pcd':'B', 'delivery_points':40, 'prems_covered':40, 'area': 'cambridge'},
    #         {'year':2012, 'pcd':'C', 'delivery_points':20, 'prems_covered':10, 'area': 'oxford'},
    #         {'year':2012, 'pcd':'D', 'delivery_points':20, 'prems_covered':20, 'area': 'oxford'},
    #         {'year':2013, 'pcd':'E', 'delivery_points':80, 'prems_covered':60, 'area': 'cambridge'},      
    #         {'year':2013, 'pcd':'F', 'delivery_points':20, 'prems_covered':20, 'area': 'cambridge'},
    #         {'year':2013, 'pcd':'G', 'delivery_points':50, 'prems_covered':40, 'area': 'oxford'},
    #         {'year':2013, 'pcd':'H', 'delivery_points':80, 'prems_covered':60, 'area': 'oxford'},    
    # ]
    
    # BASE_YEAR = 2012
    # END_YEAR = 2013
    # TIMESTEP_INCREMENT = 1
    # TIMESTEPS = range(BASE_YEAR, END_YEAR + 1, TIMESTEP_INCREMENT)

    # msoa_areas = ['cambridge', 'oxford']

    # msoa_coverage = []


    
    # pprint.pprint(msoa_coverage)


    #         for row in my_data:
    #             if row['year'] == year:
    #                 if row['area'] == msoa:
    #                     row['percentage_coverage'] = (sum(row['prems_covered']) / sum(row['delivery_points']) ) * 100

    # my_data =[{'year':2012, 'percentage_coverage':75, 'delivery_points':80, 'prems_covered':60, 'area': 'cambridge'},
    #         {'year':2012, 'percentage_coverage':75, 'delivery_points':40, 'prems_covered':30, 'area': 'oxford'},
    #         {'year':2013, 'percentage_coverage':80, 'delivery_points':100, 'prems_covered':80, 'area': 'cambridge'},      
    #         {'year':2013, 'percentage_coverage':77, 'delivery_points':130, 'prems_covered':100, 'area': 'oxford'},
    # ]

