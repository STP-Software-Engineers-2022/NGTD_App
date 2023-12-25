# Script to import panel information and bed file into database
# Created by Caroline Riehl
# Last updated 25-Dec-2023

import sqlite3
from datetime import datetime

def main(panel_data, bed_file_link):
    """
    MAIN METHOD

    This public function takes an output of NGTD_App/main.py, panel_data, to upload the user requested panel appropriately  

    Argument:
    - panel_data (dict): A dictionary containing panel information to be stored in the database

      The dictionary is expected to have the following structure:
      {
        'r_number': str,
        'panel_id': int,
        'panel_version': str,
        'signoff_status': str,
        'genes': list of strings,
        'hgnc_id': list of strings
      }
    - bed_file_link (str): a string that represents the file path of the generated bed file

    Returns:
    - None
    """

    # Connect to the SQLite database
    ngtd_db = sqlite3.connect('ngtd.db')
    cursor = ngtd_db.cursor()

    # Add test/pannel to the database if it doesn't already exist with the same version
    if does_data_entry_exist(cursor, panel_data, bed_file_link) != True:
        test_info_into_database(panel_data, bed_file_link, cursor, ngtd_db)
        print('\nPanel information and associated bed file added to the database successfully!') 

    # Commit the changes
    ngtd_db.commit()
    
    # Close the cursor and connection
    cursor.close()
    ngtd_db.close()

def does_data_entry_exist(cursor, panel_data, bed_file_link):
    """Checks whether the same test (including the version) has already been added to the database"""

    # Query database for the requested test's version
    cursor.execute('''
        SELECT test.panel_version
        FROM test
        WHERE test.r_number = (?)
    ''', (panel_data['r_number'],))

    # Retrives previous query result
    r_number = cursor.fetchone()

    # Checks whether previous query found a record of the test in the database
    if r_number:
        print('\nThis panel is already saved in the database', end = ' ')

        # Checks if the test's version record is the same as the requested test
        if r_number[0] == panel_data['panel_version']:
            print('under the same version', end = ' ')

            cursor.execute('''
                SELECT bedfile.id
                FROM bedfile
                WHERE bedfile.file_path = (?)
            ''', (bed_file_link,))

            bedfile_pk = cursor.fetchone() 

            # Checks if the test's bed file was generated for the same reference genome build as previously recorded
            if bedfile_pk is not None:
                print('and the same reference genome build. This data entry will therefore not be added again to prevent duplications.')
                return True
            else: 
                print('but under a different reference genome build. This panel with the new reference build will therefore be added to the database.')

        else:
            print('but under a different version. The information of this newer version will therefore be added to the database.')
            return False
    else:
        print('\nThis panel has not been saved in the database yet. Panel information import to the database to proceed.')
        return False


def test_info_into_database(panel_data, bed_file_link, cursor, ngtd_db):
    """Adds the panel information to the database"""

    bedfile_id = bed_file_link_into_bed_table(bed_file_link, cursor, ngtd_db)
    test_id = panel_into_test_table(panel_data, bedfile_id, cursor, ngtd_db)
    genes_into_gene_table(panel_data, test_id, cursor, ngtd_db)


def bed_file_link_into_bed_table(bed_file_link, cursor, ngtd_db):
    """Adds the link to the bed file into the 'bedfile' table"""

    cursor.execute('''
        INSERT INTO bedfile (file_path)
        VALUES (?)
    ''', (bed_file_link,))
    
    # Get the last inserted ID (at this point from table 'bedfile')
    bedfile_id = cursor.lastrowid

    return bedfile_id

def panel_into_test_table(panel_data, bedfile_id, cursor, ngtd_db):
    """Adds panel information to 'test' table"""

    current_date = datetime.now().strftime('%d-%b-%Y') # dd-mmm-yyyy format (e.g. 01-Apr-2023)

    # Insert data into Table 'test'
    cursor.execute('''
        INSERT INTO test (r_number, panel_id, panel_version, signoff_status, bedfile_id, date_added)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (panel_data['r_number'], panel_data['panel_id'], panel_data['panel_version'], panel_data['signoff_status'], bedfile_id, current_date))

    # Get the last inserted ID (at this point from table 'test')
    test_id = cursor.lastrowid

    return test_id

def genes_into_gene_table(panel_data, test_id, cursor, ngtd_db):
    """Adds gene information to 'gene' table"""

    # Insert genes into table 'gene'
    for hgnc in panel_data['hgnc_id_list']:

        # Query database for a record of the hgnc id
        cursor.execute('''
            SELECT gene.id
            FROM gene
            WHERE hgnc_id = ?
        ''', (hgnc,))

        gene_id = cursor.fetchone()

        # Checks if a record of the hgnc id already exists
        if gene_id:

            # If a record of the hgnc id already exists, its PK is added to the 'test2gene' join table with the test PK
            cursor.execute('''
                INSERT INTO test2gene (test_id, gene_id)
                VALUES (?, ?)
            ''', (test_id, gene_id[0]))
        
        # If a record of the hgnc id does not already exist, it is added to the 'gene' table along with its corresponding symbol
        else:

            # Find the hgnc id's corresponding gene symbol via list positioning 
            position = panel_data['hgnc_id_list'].index(hgnc)
            symbol = panel_data['genes'][position]

            # Add the hgnc id and gene symbol to the 'gene' table
            cursor.execute('''
                INSERT INTO gene (symbol, hgnc_id)
                VALUES (?, ?)
            ''', (symbol, hgnc))

            # Get the last inserted ID (at this point from table 'gene')
            gene_id = cursor.lastrowid

            # Insert data into the join table 'test2gene' with the foreign key reference to tables 'test' and 'gene'
            cursor.execute('''
                INSERT INTO test2gene (test_id, gene_id)
                VALUES (?, ?)
            ''', (test_id, gene_id))


if __name__ == '__main__':
    main()
