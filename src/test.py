actual_data = {
    'r_number': 'R208', 
    'panel_id': 635, 
    'panel_version': '2.11', 
    'signoff_status': 'GMS signed-off', 
    'genes': ['ATM', 'BRCA1', 'BRCA2', 'CHEK2', 'PALB2', 'RAD51C', 'RAD51D'], 
    'hgnc_id_list': ['HGNC:795', 'HGNC:1100', 'HGNC:1101', 'HGNC:16627', 'HGNC:26144', 'HGNC:9820', 'HGNC:9823']
}


import sqlite3

# Import output from test information request into the database
actual_data = {
    'r_number': 'R208', 
    'panel_id': 635, 
    'panel_version': '2.1', 
    'signoff_status': 'GMS signed-off', 
    'genes': ['ATM', 'BRCA1', 'BRCA2', 'CHEK2', 'PALB2', 'RAD51C', 'RAD51D'], 
    'hgnc_id_list': ['HGNC:795', 'HGNC:1100', 'HGNC:1101', 'HGNC:16627', 'HGNC:26144', 'HGNC:9820', 'HGNC:9823']
}

# Connect to the SQLite database
ngtd2 = sqlite3.connect('ngtd2.db')
cursor = ngtd2.cursor()

# Check whether test with given version has already been imported (exists in table 'test')

cursor.execute('''
    SELECT test.panel_version
    FROM test
    WHERE test.r_number = (?)
''', (actual_data['r_number'],))

r_number = cursor.fetchone()

if r_number:
    print('This panel is already saved in the database...')
    if r_number[0] == actual_data['panel_version']:
        print('... under the same version!')
    else:
        print('... but under a different version!')
else:
    print('This panel has not been saved in the database yet!')


ngtd2.close()

