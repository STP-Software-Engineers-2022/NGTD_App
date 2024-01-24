"""
Test data_import.py functions
Author: Caroline Riehl
Last Updated: Caroline Riehl - 21-Jan-2024
"""

import pytest
import sqlite3
import src.data_import as data_import
from datetime import datetime

def test_does_data_entry_exist_test_exists_same_version_ref(sqlite_cursor):
    """ Test that existing test with same version + reference returns True"""

    panel_data = {
        "r_number": "R208", 
        "panel_id": 635, 
        "panel_version": "2.11", 
        "signoff_status": "GMS signed-off", 
        "genes": [
            "ATM", 
            "BRCA1", 
            "BRCA2", 
            "CHEK2", 
            "PALB2", 
            "RAD51C", 
            "RAD51D"
            ], 
        "hgnc_id_list": [
            "HGNC:795", 
            "HGNC:1100", 
            "HGNC:1101", 
            "HGNC:16627", 
            "HGNC:26144", 
            "HGNC:9820", 
            "HGNC:9823"
            ]
    }
    bed_file_link = "/output/R208_GCRh37_V2.11.bed"

    result = data_import.does_data_entry_exist(sqlite_cursor, 
                                               panel_data, 
                                               bed_file_link)

    result_expected = True

    assert result == result_expected


def test_does_data_entry_exist_test_exist_same_version_dif_ref(sqlite_cursor):
    """ Test that existing test with same version, dif reference returns F """

    panel_data = {
        "r_number": "R208", 
        "panel_id": 635, 
        "panel_version": "2.11", 
        "signoff_status": "GMS signed-off", 
        "genes": [
            "ATM", 
            "BRCA1", 
            "BRCA2", 
            "CHEK2", 
            "PALB2", 
            "RAD51C", 
            "RAD51D"
            ], 
        "hgnc_id_list": [
            "HGNC:795", 
            "HGNC:1100", 
            "HGNC:1101", 
            "HGNC:16627", 
            "HGNC:26144", 
            "HGNC:9820", 
            "HGNC:9823"
            ]
    }
    bed_file_link = "/output/R208_GCRh38_V2.11.bed"

    result = data_import.does_data_entry_exist(sqlite_cursor, 
                                               panel_data, 
                                               bed_file_link)

    result_expected = False

    assert result == result_expected


def test_does_data_entry_exist_existing_test_dif_version(sqlite_cursor):
    """ Test that existing test with different version returns False"""

    panel_data = {
        "r_number": "R208", 
        "panel_id": 635, 
        "panel_version": "2.10", 
        "signoff_status": "GMS signed-off", 
        "genes": [
            "ATM", 
            "BRCA1", 
            "BRCA2", 
            "CHEK2", 
            "PALB2", 
            "RAD51C", 
            "RAD51D"
            ], 
        "hgnc_id_list": [
            "HGNC:795", 
            "HGNC:1100", 
            "HGNC:1101", 
            "HGNC:16627", 
            "HGNC:26144", 
            "HGNC:9820", 
            "HGNC:9823"
            ]
    }
    bed_file_link = None

    result = data_import.does_data_entry_exist(sqlite_cursor, 
                                               panel_data, 
                                               bed_file_link)

    result_expected = False

    assert result == result_expected


def test_does_data_entry_not_existing_test(sqlite_cursor):
    """ Test that not existing test returns False"""

    panel_data = {
        "r_number": "R168", 
        "panel_id": 513, 
        "panel_version": "1.23", 
        "signoff_status": "GMS signed-off", 
        "genes": [
            "ALAD", 
            "ALAS2", 
            "CPOX", 
            "FECH", 
            "HMBS", 
            "PPOX", 
            "UROD", 
            "UROS", 
            "GATA1"
            ], 
        "hgnc_id_list": [
            "HGNC:395", 
            "HGNC:397", 
            "HGNC:2321", 
            "HGNC:3647", 
            "HGNC:4982", 
            "HGNC:9280", 
            "HGNC:12591", 
            "HGNC:12592", 
            "HGNC:4170"
            ]
    }
    bed_file_link = None

    result = data_import.does_data_entry_exist(sqlite_cursor, 
                                               panel_data, 
                                               bed_file_link)

    result_expected = False

    assert result == result_expected


def test_bed_file_link_into_bed_table(sqlite_cursor):
    """ Test that the bedfile link is correctly added into the database """

    bed_file_link = "output/R19_GCRh38_V1.1.bed"

    data_import.bed_file_link_into_bed_table(bed_file_link, 
                                             sqlite_cursor)
    
    sqlite_cursor.execute("""
        SELECT id, file_path
        FROM bedfile
        WHERE file_path = ?
    """, (bed_file_link,))
    
    # Collects imported information
    result = sqlite_cursor.fetchone()

    bed_file_expected_pk = 3

    assert result is not None
    assert result[0] == bed_file_expected_pk
    assert result[1] == bed_file_link


def test_panel_into_test_table(sqlite_cursor):
    """ Test that tests are added to the database correctly"""

    panel_data = {
        "r_number": "R168", 
        "panel_id": 513, 
        "panel_version": "1.23", 
        "signoff_status": "GMS signed-off", 
        "genes": [
            "ALAD", 
            "ALAS2", 
            "CPOX", 
            "FECH", 
            "HMBS", 
            "PPOX", 
            "UROD", 
            "UROS", 
            "GATA1"
            ], 
        "hgnc_id_list": [
            "HGNC:395", 
            "HGNC:397", 
            "HGNC:2321", 
            "HGNC:3647", 
            "HGNC:4982", 
            "HGNC:9280", 
            "HGNC:12591", 
            "HGNC:12592", 
            "HGNC:4170"
            ]
    }
    
    bedfile_id = "3"
    current_date = datetime.now().strftime("%d-%b-%Y")

    data_import.panel_into_test_table(panel_data, 
                                      bedfile_id, 
                                      sqlite_cursor)
    
    sqlite_cursor.execute("""
        SELECT r_number, 
               panel_id, 
               panel_version, 
               signoff_status, 
               bedfile_id, 
               date_added
        FROM test
        WHERE r_number = ? AND 
              panel_id = ? AND 
              panel_version = ? AND 
              signoff_status = ? AND 
              bedfile_id = ? AND 
              date_added = ?;
    """, (
        panel_data["r_number"],
        panel_data["panel_id"], 
        panel_data["panel_version"], 
        panel_data["signoff_status"], 
        bedfile_id, 
        current_date
        ))
    
    result = sqlite_cursor.fetchone()

    assert result is not None
    assert result[0] == panel_data["r_number"]
    assert result[1] == panel_data["panel_id"]
    assert result[2] == panel_data["panel_version"]
    assert result[3] == panel_data["signoff_status"]
    assert result[4] == bedfile_id
    assert result[5] == current_date


def test_genes_into_gene_table_one_gene(sqlite_cursor):
    """ Test that single gene is added correctly to the database"""

    panel_data = {
        "r_number": "R169", 
        "panel_id": 1207, 
        "panel_version": "1.1", 
        "signoff_status": "GMS signed-off", 
        "genes": ["HMBS"], 
        "hgnc_id_list": ["HGNC:4982"]
        }
    
    test_id = "3"

    data_import.genes_into_gene_table(panel_data, test_id, 
                                      sqlite_cursor)

    sqlite_cursor.execute("""
        SELECT symbol, hgnc_id
        FROM gene
        WHERE symbol = ? AND hgnc_id = ?;
    """, (
        panel_data["genes"][0],
        panel_data["hgnc_id_list"][0]
    ))
    
    result = sqlite_cursor.fetchone()

    assert result is not None
    assert result[0] == panel_data["genes"][0]
    assert result[1] == panel_data["hgnc_id_list"][0]


def test_genes_into_gene_table_multiple_genes(sqlite_cursor):
    """ Test that multiple genes are added correctly to the database"""

    panel_data = {
        "r_number": "R168", 
        "panel_id": 513, 
        "panel_version": "1.23", 
        "signoff_status": "GMS signed-off", 
        "genes": [
            "ALAD", 
            "ALAS2", 
            "CPOX", 
            "FECH", 
            "HMBS", 
            "PPOX", 
            "UROD", 
            "UROS", 
            "GATA1"
            ], 
        "hgnc_id_list": [
            "HGNC:395", 
            "HGNC:397", 
            "HGNC:2321", 
            "HGNC:3647", 
            "HGNC:4982", 
            "HGNC:9280", 
            "HGNC:12591", 
            "HGNC:12592", 
            "HGNC:4170"
            ]
    }
    
    test_id = "3"

    data_import.genes_into_gene_table(panel_data, 
                                      test_id, 
                                      sqlite_cursor)

    # Check that gene data added to gene table
    for gene_iteration in range(len(panel_data["hgnc_id_list"])):
        sqlite_cursor.execute("""
            SELECT symbol, hgnc_id
            FROM gene
            WHERE symbol = ? AND hgnc_id = ?;
        """, (
            panel_data["genes"][gene_iteration],
            panel_data["hgnc_id_list"][gene_iteration]
        ))

        result = sqlite_cursor.fetchone()

        assert result is not None
        assert result[0] == panel_data["genes"][gene_iteration]
        assert result[1] == panel_data["hgnc_id_list"][gene_iteration]

    # Check that a hgnc id present in 2 tests is not duplicated in table gene
    overlapping_hgnc_id = "HGNC:4982"
    overlapping_hgnc_id_exepcted_pk = 8
    sqlite_cursor.execute("""
        SELECT id
        FROM gene
        WHERE hgnc_id = ?;
    """, (overlapping_hgnc_id,
    ))

    result = sqlite_cursor.fetchone()

    assert result is not None
    assert result[0] == overlapping_hgnc_id_exepcted_pk
    assert len(result) == 1 #check that hgnc_id only has one pk
