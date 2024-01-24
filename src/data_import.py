# Script to import panel information and bed file into database
# Created by Caroline Riehl
# Last updated: Caroline Riehl - 18-Jan-2023

import sqlite3
from datetime import datetime
from config import log

def import_into_database(panel_data, bed_file_link):
    """
    Method to import data to database

    This public function takes an output of NGTD_App/main.py, panel_data, 
    to upload the user requested panel appropriately  

    Parameters
    __________
    panel_data (dict): A dictionary containing panel information to be 
                         stored in the database
            The dictionary is expected to have the following structure:
            {
                "r_number": str,
                "panel_id": int,
                "panel_version": str,
                "signoff_status": str,
                "genes": list of strings,
                "hgnc_id": list of strings
            }
    bed_file_link (str): a string that represents the file path of the 
                         generated bed file

    Returns:
    None
    """

    # Connect to the SQLite database
    ngtd_db = sqlite3.connect("ngtd.db")
    cursor = ngtd_db.cursor()

    # Add test to the database if not already present with the same version
    if does_data_entry_exist(cursor, panel_data, bed_file_link) != True:
        test_info_into_database(panel_data, bed_file_link, cursor)
        msg = "Panel information and associated bed file path" +\
            f" ({bed_file_link}) added to the database successfully!"
        print("\n"+msg)
        log.info(msg)

    # Commit the changes
    ngtd_db.commit()
    
    # Close the cursor and connection
    cursor.close()
    ngtd_db.close()

def does_data_entry_exist(cursor, panel_data, bed_file_link):
    """Checks whether the entry exists in the database"""

    # Query database for the requested test's version
    log.debug("Checking if database entry already exists...")
    cursor.execute("""
        SELECT test.panel_version
        FROM test
        WHERE test.r_number = (?)
    """, (panel_data["r_number"],))

    # Retrives previous query result
    panel_version = cursor.fetchone()
 
    # Checks whether previous query found a record of the test in the database
    if panel_version:
        msg = "This panel is already saved in the database"

        # Checks if the test's version record is the same as the requested one
        if panel_version[0] == panel_data["panel_version"]:
            msg = msg + " under the same version"

            cursor.execute("""
                SELECT bedfile.id
                FROM bedfile
                WHERE bedfile.file_path = (?)
            """, (bed_file_link,))

            bedfile_pk = cursor.fetchone() 

            # Checks if the reference genome is the same
            if bedfile_pk is not None:
                msg = msg + " and the same reference genome build. "+\
                    "This data entry will therefore not be added again to "+\
                    "prevent duplications."
                print("\n" + msg)
                log.debug(msg)
                return True
            else: 
                msg = msg + " but under a different reference genome build. "+\
                    "This panel with the new reference build will therefore"+\
                    "be added to the database."
                print("\n" + msg)
                log.debug(msg)
                return False

        else:
            msg = msg + " but under a different version. "+\
                "The information of this newer version will therefore be "+\
                "added to the database."
            print("\n" + msg)
            log.debug(msg)
            return False
    else:
        msg = "This panel has not been saved in the database yet. "+\
            "Panel information import to the database to proceed."
        print("\n" + msg)
        log.debug(msg)

        return False


def test_info_into_database(panel_data, bed_file_link, cursor):
    """Adds the panel information to the database"""

    bedfile_id = bed_file_link_into_bed_table(bed_file_link, cursor)
    test_id = panel_into_test_table(panel_data, bedfile_id, cursor)
    genes_into_gene_table(panel_data, test_id, cursor)


def bed_file_link_into_bed_table(bed_file_link, cursor):
    """Adds the link to the bed file into the "bedfile" table"""

    cursor.execute("""
        INSERT INTO bedfile (file_path)
        VALUES (?)
    """, (bed_file_link,))
    
    # Get the last inserted ID (at this point from table "bedfile")
    bedfile_id = cursor.lastrowid
    log.debug("BED file link added to database")
    return bedfile_id

def panel_into_test_table(panel_data, bedfile_id, cursor):
    """Adds panel information to "test" table"""

    # dd-mmm-yyyy format (e.g. 01-Apr-2023)
    current_date = datetime.now().strftime("%d-%b-%Y")

    # Insert data into Table "test"
    cursor.execute("""
        INSERT INTO test (
            r_number, 
            panel_id, 
            panel_version, 
            signoff_status, 
            bedfile_id, 
            date_added
            )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        panel_data["r_number"], 
        panel_data["panel_id"], 
        panel_data["panel_version"], 
        panel_data["signoff_status"], 
        bedfile_id, 
        current_date
        ))

    # Get the last inserted ID (at this point from table "test")
    test_id = cursor.lastrowid
    log.debug("Panel information added to database")
    return test_id

def genes_into_gene_table(panel_data, test_id, cursor):
    """Adds gene information to "gene" table"""

    # Insert genes into table "gene"
    for hgnc in panel_data["hgnc_id_list"]:

        # Query database for a record of the hgnc id
        cursor.execute("""
            SELECT gene.id
            FROM gene
            WHERE hgnc_id = ?
        """, (hgnc,))

        gene_id = cursor.fetchone()

        # Checks if a record of the hgnc id already exists
        if gene_id:

            # If hgnc id already exists, its PK is added to "test2gene"
            cursor.execute("""
                INSERT INTO test2gene (
                    test_id, 
                    gene_id)
                VALUES (?, ?)
            """, (
                test_id, 
                gene_id[0]
                ))
            log.debug("hgnc already exists - PK added to database")
        
        # If hgnc id does not already exist, new entry created
        else:

            # Find hgnc id's corresponding gene symbol via list positioning 
            position = panel_data["hgnc_id_list"].index(hgnc)
            symbol = panel_data["genes"][position]

            # Add the hgnc id and gene symbol to the "gene" table
            cursor.execute("""
                INSERT INTO gene (
                    symbol, 
                    hgnc_id)
                VALUES (?, ?)
            """, (
                symbol, 
                hgnc))

            # Get the last inserted ID (at this point from table "gene")
            gene_id = cursor.lastrowid

            # Foreign keys of tables "test" and "gene" added to "test2gene"
            cursor.execute("""
                INSERT INTO test2gene (
                    test_id, 
                    gene_id)
                VALUES (?, ?)
            """, (
                test_id, 
                gene_id))
            log.debug("New entry created for hgnc in database")


if __name__ == "__main__":
    import_into_database()
