import sqlite3

ngtd_db = sqlite3.connect('ngtd.db')

cursor = ngtd_db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS patient_details (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        patient_name TEXT,
        patient_surname TEXT,
        date_of_birth TEXT,
        clinical_features TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tests (
        id INTEGER PRIMARY KEY,
        test_id TEXT,
        panelapp_id_number TEXT,
        gms_signed_off TEXT,
        gms_signed_off_version TEXT,
        gms_signed_off_date TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS genes_list (
        id INTEGER PRIMARY KEY,
        symbol TEXT,
        hgnc_id TEXT,
        transcript TEXT,
        chr TEXT,
        start_coordinate TEXT,
        end_coordinates TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS patient_tests (
        patient_id INTEGER,
        test_id TEXT,
        reference_genome TEXT,
        PRIMARY KEY (patient_id, test_id),
        FOREIGN KEY (patient_id) REFERENCES patient_details(id),
        FOREIGN KEY (test_id) REFERENCES tests(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS gene_tests (
        test_id INTEGER,
        gene_id TEXT,
        PRIMARY KEY (test_id, gene_id),
        FOREIGN KEY (test_id) REFERENCES tests(id),
        FOREIGN KEY (gene_id) REFERENCES genes_list(id)
    )
''')

ngtd_db.commit()