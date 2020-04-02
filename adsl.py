import os
from pprint import pprint
import configparser
import csv
import pandas as pd
from tqdm import tqdm

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

def load_pcd_to_exchange():

    data1 = pd.read_csv(os.path.join(INPUT_FILES, 'pcd_to_exchange', 'openreach1.csv'))
    data2 = pd.read_csv(os.path.join(INPUT_FILES, 'pcd_to_exchange', 'openreach2.csv'))
    all_data = data1.append(data2)
    all_data['Postcode'] = all_data['Postcode'].str.replace(' ', '')

    return all_data


def read_pcd_data():
    """
    """
    pcd_data = []

    #2012
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

    #2013
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

    #2014
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

    #2015
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

    #2016
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

    # for year in TIMESTEPS:
    for filename in os.listdir(os.path.join(INPUT_FILES, 'codepoint', 'data')):
        with open(os.path.join(INPUT_FILES, 'codepoint', 'data', filename), 'r', encoding='utf8', errors='replace') as system_file:
            reader = csv.reader(system_file)
            #next(reader) no header
            for line in reader:
                if line[18] == 'S':
                    codepoint_data.append({
                        'postcode': line[0].replace(' ', ''),
                        'delivery_points': int(line[3]),
                        'type': line[18],
                        # 'year': year
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

    # for year in TIMESTEPS:
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
                'lad': line[8],
                # 'year': year
            })

    with open(os.path.join(INPUT_FILES, 'scotland_postcode_lookup', 'Postcode lookup (revised 100113).csv'), 'r', encoding='utf8', errors='replace') as system_file:
        reader = csv.reader(system_file)
        next(reader)
        for line in reader:

            pcd_lut_data.append({
                'postcode': line[0].replace(' ', ''),
                'msoa_id': line[14],
                'msoa_name': line[15],
                'lad': line[17],
                # 'year': year
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


    BASE_YEAR = 1999
    END_YEAR = 2007
    TIMESTEP_INCREMENT = 1
    TIMESTEPS = range(BASE_YEAR, END_YEAR + 1, TIMESTEP_INCREMENT)

    ##############
    # READ
    ##############

    path = os.path.join(OUTPUT_DATA, 'pcd_data.csv')

    if not os.path.exists(path):

        pcd_data = load_pcd_to_exchange()

        #read exchange
        exchanges = pd.read_csv(os.path.join(INPUT_FILES, 'kitz', 'exchange.data.kitz.csv'))
        exchanges = exchanges.drop('Postcode', 1)

        pcd_data = pcd_data.merge(exchanges, left_on='Exchange ID', right_on='OLO', )
        pcd_data['Enabled'] = pcd_data['Enabled'].str[6:]
        pcd_data = pcd_data[['Postcode', 'Enabled']]
        #OLO and Enabled

        # Read codepoint
        print('read_codepoint')
        codepoint = read_codepoint()

        # {'postcode': 'AB118DL', 'delivery_points': '25', 'type': 'S', 'year': 2012},
        codepoint = pd.DataFrame(codepoint)

        pcd_data = pcd_data.merge(codepoint, left_on='Postcode', right_on='postcode')
        pcd_data = pcd_data[['Postcode', 'Enabled', 'delivery_points', 'type']]

        # Read LUT
        print('Read postcode LUT')
        my_pcd_lut = read_pcd_lut()

        #{'postcode': 'TR36PJ', 'msoa_id': 'E02003911', 'msoa_name': 'Cornwall 047', 'year': 2000}
        my_pcd_lut = pd.DataFrame(my_pcd_lut)
        pcd_data = pd.merge(my_pcd_lut, pcd_data, how='left', left_on='postcode', right_on='Postcode')
        pcd_data = pcd_data[['postcode', 'Enabled', 'delivery_points', 'type', 'msoa_id', 'lad']]
        pcd_data = pcd_data[pcd_data['Enabled'].notna()]
        # pcd_data.to_csv(path, index=False)

        pcd_data = pcd_data.to_dict('records')#[:4]

        timeseries = []
        for year in TIMESTEPS:
            print('Working on {}'.format(year))
            for item in pcd_data:
                # print(year, item['Enabled'])
                if year >= int(item['Enabled']):
                    # item['adsl'] = int(item['delivery_points'])
                    # item['year'] = year
                    timeseries.append({
                        'postcode': item['postcode'],
                        'Enabled': item['Enabled'],
                        'delivery_points': item['delivery_points'],
                        'type': item['type'],
                        'msoa_id': item['msoa_id'],
                        'lad': item['lad'],
                        'adsl': int(item['delivery_points']),
                        'year': year,
                    })
                else:
                    # item['adsl'] = 0
                    # item['year'] = year
                    timeseries.append({
                        'postcode': item['postcode'],
                        'Enabled': item['Enabled'],
                        'delivery_points': item['delivery_points'],
                        'type': item['type'],
                        'msoa_id': item['msoa_id'],
                        'lad': item['lad'],
                        'adsl': 0,
                        'year': year,
                    })

        timeseries = pd.DataFrame(timeseries)
        timeseries.to_csv(path, index=False)

    else:
        print('Reading already processed pcd_data')
        timeseries = pd.read_csv(path)#[:1000]

    timeseries = timeseries.to_dict('records')

    # for item in timeseries:
    #     if item['lad'] == 'Cambridge':
    #         if item['year'] == 1999:
    #             print(item)

    output = []

    print('Starting aggregation')
    lads = list(set([p['lad'] for p in timeseries]))
    print('lads = {}'.format(len(lads)))

    for lad in tqdm(lads):

        # print('Working on {}'.format(lad))

        # if not lad == 'Cambridge':
        #     continue

        lad_data = []

        for item in timeseries:
            if lad == item['lad']:
                lad_data.append(item)

        # print(sum([d['delivery_points'] for d in lad_data]))

        msoas = list(set([p['msoa_id'] for p in lad_data]))
        print('--msoas = {}'.format(len(msoas)))

        for year in TIMESTEPS:

            print('Working on {}'.format(year))

            yearly_data = []

            for item in lad_data:
                if year == item['year']:
                    yearly_data.append(item)

            for msoa in msoas:

                adsl = 0
                total_prems = 0

                for item in yearly_data:
                    if msoa == item['msoa_id']:
                        total_prems += int(item['delivery_points'])
                        adsl += int(item['adsl'])

                if adsl > 0:
                    adsl_perc = round((adsl/total_prems)*100)
                elif adsl == 0:
                    adsl_perc = 0
                else:
                    print('problem with adsl perc calc')
                    print(adsl, total_prems)

                output.append({
                    'year': year,
                    'msoa': msoa,
                    'lad': lad,
                    'delivery_points': total_prems,
                    'adsl': adsl,
                    'adsl_percentage': adsl_perc,
                })

    output = pd.DataFrame(output)
    output.to_csv(os.path.join(OUTPUT_DATA, 'adsl.csv'), index=False)
    # print(output.delivery_points.sum())
