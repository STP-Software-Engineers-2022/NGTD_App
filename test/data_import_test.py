'''############################################################################
Test data_import.py functions
Imports panels/tests into the database
############################################################################'''

import pytest
import sqlite3
import src.data_import as data_import


def test_does_test_version_exist_true(sqlite_test_db_with_data):
    """Testing with existing test and same version in database"""

    temp_dict = {
        'r_number': 'R208', 
        'panel_id': 635, 
        'panel_version': '2.11', 
        'signoff_status': 'GMS signed-off', 
        'genes': ['ATM', 'BRCA1', 'BRCA2', 'CHEK2', 'PALB2', 'RAD51C', 'RAD51D'], 
        'hgnc_id_list': ['HGNC:795', 'HGNC:1100', 'HGNC:1101', 'HGNC:16627', 'HGNC:26144', 'HGNC:9820', 'HGNC:9823']
        }
    db_path = sqlite_test_db_with_data
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    result = data_import.does_test_version_exist(cursor, temp_dict)

    assert result == True


def test_does_test_version_exist_false_dif_version(sqlite_test_db_with_data):
    """Testing with existing test but different version in database"""

    temp_dict = {
        'r_number': 'R208', 
        'panel_id': 635, 
        'panel_version': '2.12', 
        'signoff_status': 'GMS signed-off', 
        'genes': ['ATM', 'BRCA1', 'BRCA2', 'CHEK2', 'PALB2', 'RAD51C', 'RAD51D'], 
        'hgnc_id_list': ['HGNC:795', 'HGNC:1100', 'HGNC:1101', 'HGNC:16627', 'HGNC:26144', 'HGNC:9820', 'HGNC:9823']
        }
    db_path = sqlite_test_db_with_data
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    result = data_import.does_test_version_exist(cursor, temp_dict)

    assert result == False


def test_does_test_version_exist_false_missing(sqlite_test_db_with_data):
    """Testing with non-existing test in database"""

    temp_dict = {
        'r_number': 'R184', 
        'panel_id': 1318, 
        'panel_version': '1.1', 
        'signoff_status': 'GMS signed-off', 
        'genes': ['CFTR'], 
        'hgnc_id_list': ['GNC:1884']
        }
    db_path = sqlite_test_db_with_data
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    result = data_import.does_test_version_exist(cursor, temp_dict)

    assert result == False

# TODO: add unit tests for panel_into_test_table(panel_data, cursor, ngtd_db) and genes_into_gene_table(panel_data, test_id, cursor, ngtd_db)

#  def test_panel_into_test_table(sqlite_test_db_empty):

#     temp_dict = {
#         'r_number': 'R184', 
#         'panel_id': 1318, 
#         'panel_version': '1.1', 
#         'signoff_status': 'GMS signed-off', 
#         'genes': ['CFTR'], 
#         'hgnc_id_list': ['GNC:1884']
#         }
    
#     data_import.panel_into_test_table(temp_dict, cursor, ngtd_db)

    
