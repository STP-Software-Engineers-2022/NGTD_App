import sqlite3

ngtd_db = sqlite3.connect('ngtd.db')

cursor = ngtd_db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS patient (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        patient_name TEXT,
        patient_surname TEXT,
        date_of_birth TEXT,
        clinical_features TEXT
    )
''')

cursor.execute('''
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
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS gene (
        id INTEGER PRIMARY KEY,
        symbol TEXT,
        hgnc_id TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bedfile (
        id INTEGER PRIMARY KEY,
        file_path TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS patient2test (
        patient_id INTEGER,
        test_id TEXT,
        PRIMARY KEY (patient_id, test_id),
        FOREIGN KEY (patient_id) REFERENCES patient(id),
        FOREIGN KEY (test_id) REFERENCES test(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS test2gene (
        test_id TEXT,
        gene_id TEXT,
        PRIMARY KEY (test_id, gene_id),
        FOREIGN KEY (test_id) REFERENCES test(id),
        FOREIGN KEY (gene_id) REFERENCES gene(id)
    )
''')

ngtd_db.commit()

ngtd_db.close()