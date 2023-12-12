import pytest
import sqlite3
import logging

@pytest.fixture
def sqlite_test_db_with_data(tmp_path):
    db_path = tmp_path / 'test_database.db'

    logging.warning("********* DB PATH %s" % db_path)

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE test (
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
        CREATE TABLE gene (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            hgnc_id TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE test2gene (
            test_id TEXT,
            gene_id TEXT,
            PRIMARY KEY (test_id, gene_id),
            FOREIGN KEY (test_id) REFERENCES test(id),
            FOREIGN KEY (gene_id) REFERENCES gene(id)
        )
    ''')

    cursor.execute('''
        INSERT INTO test (r_number,panel_id, panel_version, signoff_status, date_added)
        VALUES ('R208', 635, '2.11', 'GMS signed-off', '08-Dec-2023'), ('R169', 1207, '1.1', 'GMS signed-off', '09-Dec-2023')
    ''')

    cursor.execute('''
        INSERT INTO gene (symbol, hgnc_id)
        VALUES ('ATM', 'HGNC:795'), ('BRCA1', 'HGNC:1100'), ('BRCA2', 'HGNC:1101'), ('CHEK2', 'HGNC:16627'), ('PALB2', 'HGNC:26144'), ('RAD51C', 'HGNC:9820'), ('RAD51D', 'HGNC:9823'), ('HMBS', 'HGNC:4982')
    ''')

    conn.commit()
    conn.close()

    return str(db_path)


# @pytest.fixture
# def sqlite_test_db_empty(tmp_path):
#     db_path = tmp_path / 'test_database.db'

#     conn = sqlite3.connect(str(db_path))
#     cursor = conn.cursor()

#     cursor.execute('''
#         CREATE TABLE test (
#             id INTEGER PRIMARY KEY,
#             r_number TEXT,
#             panel_id INTEGER,
#             panel_version TEXT,
#             signoff_status TEXT,
#             bedfile_id TEXT,
#             date_added TEXT,
#             FOREIGN KEY (bedfile_id) REFERENCES bedfile(id)
#         )
#     ''')

#     cursor.execute('''
#         CREATE TABLE gene (
#             id INTEGER PRIMARY KEY,
#             symbol TEXT,
#             hgnc_id TEXT
#         )
#     ''')

#     cursor.execute('''
#         CREATE TABLE test2gene (
#             test_id TEXT,
#             gene_id TEXT,
#             PRIMARY KEY (test_id, gene_id),
#             FOREIGN KEY (test_id) REFERENCES test(id),
#             FOREIGN KEY (gene_id) REFERENCES gene(id)
#         )
#     ''')

#     conn.commit()
#     conn.close()

#     return str(db_path)