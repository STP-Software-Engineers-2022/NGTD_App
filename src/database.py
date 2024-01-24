"""Script to create the database
Author: Caroline Riehl
Last Updated: Caroline Riehl 21-Jan-2024
"""
import sqlite3

def create_database():

    ngtd_db = sqlite3.connect("ngtd.db")
    cursor = ngtd_db.cursor()

    # Create table patient
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient (
            id INTEGER PRIMARY KEY,
            patient_record_number INTEGER,
            patient_name TEXT,
            patient_surname TEXT,
            date_of_birth TEXT,
            clinical_features TEXT,
            sex TEXT
        )
    """)

    # Create table test
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test (
            id INTEGER PRIMARY KEY,
            r_number TEXT,
            panel_id INTEGER,
            panel_version TEXT,
            signoff_status TEXT,
            bedfile_id TEXT,
            date_added TEXT,
            FOREIGN KEY (bedfile_id) REFERENCES bedfile(id)
        )
    """)

    # Create table gene
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gene (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            hgnc_id TEXT
        )
    """)

    # Create table bedfile
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bedfile (
            id INTEGER PRIMARY KEY,
            file_path TEXT
        )
    """)

    # Create table patient2test
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient2test (
            patient_id INTEGER,
            test_id TEXT,
            date_tested TEXT, 
            PRIMARY KEY (patient_id, test_id),
            FOREIGN KEY (patient_id) REFERENCES patient(id),
            FOREIGN KEY (test_id) REFERENCES test(id)
        )
    """)

    # Create table test2gene
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test2gene (
            test_id TEXT,
            gene_id TEXT,
            PRIMARY KEY (test_id, gene_id),
            FOREIGN KEY (test_id) REFERENCES test(id),
            FOREIGN KEY (gene_id) REFERENCES gene(id)
        )
    """)

    ngtd_db.commit()
    ngtd_db.close()

if __name__ == "__main__":
    create_database()
