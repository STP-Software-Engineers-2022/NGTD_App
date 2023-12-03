import sqlite3

# Import output from test information request into the database
test_data = {
    'r_number': 'R208', 
    'panel_id': 635, 
    'panel_version': '2.11', 
    'signoff_status': 'GMS signed-off', 
    'genes': ['ATM', 'BRCA1', 'BRCA2', 'CHEK2', 'PALB2', 'RAD51C', 'RAD51D'], 
    'hgnc_id_list': ['HGNC:795', 'HGNC:1100', 'HGNC:1101', 'HGNC:16627', 'HGNC:26144', 'HGNC:9820', 'HGNC:9823']
}

def main():

    # Connect to the SQLite database
    ngtd_db = sqlite3.connect('ngtd.db')
    cursor = ngtd_db.cursor()

    if does_test_version_exist(cursor) != True:
        test_info_into_database(test_data, cursor, ngtd_db)
    
    # Close the cursor and connection
    cursor.close()
    ngtd_db.close()

# Check whether test with given version has already been imported (exists in table 'test')

def does_test_version_exist(cursor):

    cursor.execute('''
        SELECT test.panel_version
        FROM test
        WHERE test.r_number = (?)
    ''', (test_data['r_number'],))

    r_number = cursor.fetchone()

    if r_number:
        print('This panel is already saved in the database...')
        if r_number[0] == test_data['panel_version']:
            print('... under the same version!')
            return True
        else:
            print('... but under a different version!')
            return False
    else:
        print('This panel has not been saved in the database yet!')
        return False


def test_info_into_database(test_data, cursor, ngtd_db):

    # Insert data into Table 'test'
    cursor.execute('''
        INSERT INTO test (r_number, panel_id, panel_version, signoff_status)
        VALUES (?, ?, ?, ?)
    ''', (test_data['r_number'], test_data['panel_id'], test_data['panel_version'], test_data['signoff_status']))


    # Get the last inserted ID (at this point from table 'test')
    test_id = cursor.lastrowid


    # Insert data into table 'gene'
    for gene in test_data['genes']:
        position = test_data['genes'].index(gene)
        hgnc_id = test_data['hgnc_id_list'][position]

        cursor.execute('''
            INSERT INTO gene (symbol, hgnc_id)
            VALUES (?, ?)
        ''', (gene, hgnc_id))

        # Get the last inserted ID (at this point from table 'gene')
        gene_id = cursor.lastrowid

        # Insert data into join table 'test2gene' with the foreign key reference to tables 'test' and 'gene'
        cursor.execute('''
            INSERT INTO test2gene (test_id, gene_id)
            VALUES (?, ?)
        ''', (test_id, gene_id))

    # Commit the changes
    ngtd_db.commit()



if __name__ == '__main__':
    main()



