"""
Conftest file for data_import_test.py fixtures
Written by Caroline Riehl
Last updated: Caroline Riehl - 21-Jan-2024
"""

import pytest
import sqlite3

@pytest.fixture
def sqlite_cursor():

    connection = sqlite3.connect(":memory:")

    # Create table patient
    connection.execute("""
        CREATE TABLE IF NOT EXISTS patient (
            id INTEGER PRIMARY KEY,
            patient_record_number INTEGER,
            patient_name TEXT,
            patient_surname TEXT,
            date_of_birth TEXT,
            clinical_features TEXT
        )
    """)

    # Create table test
    connection.execute("""
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
    connection.execute("""
        CREATE TABLE IF NOT EXISTS gene (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            hgnc_id TEXT
        )
    """)

    # Create table bedfile
    connection.execute("""
        CREATE TABLE IF NOT EXISTS bedfile (
            id INTEGER PRIMARY KEY,
            file_path TEXT
        )
    """)

    # Create table patient2test
    connection.execute("""
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
    connection.execute("""
        CREATE TABLE IF NOT EXISTS test2gene (
            test_id TEXT,
            gene_id TEXT,
            PRIMARY KEY (test_id, gene_id),
            FOREIGN KEY (test_id) REFERENCES test(id),
            FOREIGN KEY (gene_id) REFERENCES gene(id)
        )
    """)
    cursor = connection.cursor()
    
    # Add test information to table test
    cursor.execute("""
        INSERT INTO test (
                   r_number, 
                   panel_id, 
                   panel_version, 
                   signoff_status, 
                   bedfile_id, 
                   date_added
                   )
        VALUES ("R208", 635, "2.11", "GMS signed-off", 1, "08-Dec-2023"), 
               ("R169", 1207, "1.1", "GMS signed-off", 2, "09-Dec-2023")
    """)

    # Add list of genes to table gene
    cursor.execute("""
        INSERT INTO gene (
                   symbol, 
                   hgnc_id
                   )
        VALUES ("ATM", "HGNC:795"), 
               ("BRCA1", "HGNC:1100"), 
               ("BRCA2", "HGNC:1101"), 
               ("CHEK2", "HGNC:16627"), 
               ("PALB2", "HGNC:26144"), 
               ("RAD51C", "HGNC:9820"), 
               ("RAD51D", "HGNC:9823"), 
               ("HMBS", "HGNC:4982")
    """)

    # Add bedfile pathway to table bedfile
    cursor.execute("""
        INSERT INTO bedfile (file_path)
        VALUES ("/output/R208_GCRh37_V2.11.bed"), 
               ("/output/R169_GCRh38_V1.1.bed")
    """)

    # Add foreign keys of tests and genes in test2gene table
    cursor.execute("""
        INSERT INTO test2gene (test_id, gene_id)
        VALUES (1, 1), 
               (1, 2), 
               (1, 3), 
               (1, 4), 
               (1, 5), 
               (1, 6), 
               (1, 7), 
               (2, 1)
    """)

    yield cursor

    connection.close()
