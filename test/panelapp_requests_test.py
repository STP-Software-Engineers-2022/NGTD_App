'''############################################################################
Test Panel App Request Object
Hits PanelApp API to return a list of genes for a gene panel from a given
R number
############################################################################'''

import pytest
import src.panelapp_requests as panelapp_requests
from config import log

@pytest.fixture
def r_code():
    """
    Fixture for providing a sample valid R-code (e.g., 'R134') for testing.
    """
    r_code = 'R134'
    return r_code

@pytest.fixture
def target():
    """
    Fixture for creating a target with a known valid R-code (provided by 'r_code') for testing API requests.
    """
    r_code = 'R134'
    target = panelapp_requests.MyRequests(r_code)
    return target

@pytest.fixture
def bad_r_target():
    """
    Fixture for creating a target with a known bad R-code (e.g., 'R428') for testing error handling.
    """
    bad_r_code = 'R428'
    corrupt_target = panelapp_requests.MyRequests(bad_r_code)
    return corrupt_target

def test_request_data(target):
    """
    Test status code 200 upon API request
    """
    response = target.request_data()
    assert response.status_code == 200

def test_request_data_bad_r_code(bad_r_target):
    """
    Test incorrect R code
    """
    with pytest.raises(SystemExit):
        bad_r_target.request_data()
   
def test_gene_list(target):
    """
    Test correct gene list being returned
    """
    response = target.request_data()
    gene_list, signoff = target.gene_list(response)
    assert gene_list == ['APOB', 'APOE', 'LDLR', 'LDLRAP1', 'PCSK9', 'GCKR']

def test_signoff(target):
    """
    Test expected value of signoff variable
    """
    response = target.request_data()
    gene_list, signoff = target.gene_list(response)
    assert signoff == "GMS signed-off"
    

"""
Tests for get_panel_info
"""
def test_panel_info(target):
    """
    Test correct hgnc list being returned
    """
    response = target.request_data()
    h_list, panel_id, p_version = target.get_panel_info(response)
    assert h_list == ['HGNC:603', 'HGNC:613', 'HGNC:6547', 'HGNC:18640', 'HGNC:20001', 'HGNC:4196']
    assert panel_id == 772
    assert p_version ==  "2.4"

"""
Tests for database_postage
"""

@pytest.fixture
def bed():
    """
    Fixture for providing a boolean value 'True', representing the presence of a bed in a database request.
    """
    bed = True
    return bed

@pytest.fixture
def no_bed():
    """
    Fixture for providing a boolean value 'False', representing the absence of a bed in a database request.
    """
    no_bed = False
    return no_bed

@pytest.fixture
def g_list():
    """
    Fixture for providing a list of genes ['APOB', 'APOE', 'LDLR', 'LDLRAP1', 'PCSK9', 'GCKR'] for testing.
    """
    g_list = ['APOB', 'APOE', 'LDLR', 'LDLRAP1', 'PCSK9', 'GCKR']
    return g_list

@pytest.fixture
def signoff():
    """
    Fixture for providing a string 'GMS signed-off' representing the sign-off status for testing.
    """
    signoff = "GMS signed-off"
    return signoff

@pytest.fixture
def not_signoff():
    """
    Fixture for providing a string 'not GMS signed-off' representing the non-sign-off status for testing.
    """
    signoff = "not GMS signed-off"
    return signoff

def test_database_postage_bed_true(target, r_code, bed, g_list, signoff):
    """
    Test function for database postage with bed 'True' in the request.
    """
    response = target.request_data()
    result = target.database_postage(response, r_code, bed, g_list, signoff)
    result["bed_request"] = bed
    assert result == {"r_number": "R134", "panel_id": 772, "panel_version": "2.4",
                      "signoff_status": "GMS signed-off", "genes": ['APOB', 'APOE', 'LDLR', 'LDLRAP1', 'PCSK9', 'GCKR'], 
                      "hgnc_id_list": ['HGNC:603', 'HGNC:613', 'HGNC:6547', 'HGNC:18640', 'HGNC:20001', 'HGNC:4196'], "bed_request": True}
    
def test_database_postage_bed_false(target, r_code, no_bed, g_list, signoff):
    """
    Test function for database postage with bed 'False' in the request.
    """
    response = target.request_data()
    result = target.database_postage(response, r_code, no_bed, g_list, signoff)
    result["bed_request"] = no_bed
    assert result == {"r_number": "R134", "panel_id": 772, "panel_version": "2.4",
                      "signoff_status": "GMS signed-off", "genes": ['APOB', 'APOE', 'LDLR', 'LDLRAP1', 'PCSK9', 'GCKR'], 
                      "hgnc_id_list": ['HGNC:603', 'HGNC:613', 'HGNC:6547', 'HGNC:18640', 'HGNC:20001', 'HGNC:4196'], "bed_request": False}
