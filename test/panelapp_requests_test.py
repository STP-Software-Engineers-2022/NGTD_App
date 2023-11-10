'''############################################################################
Test Panel App Request Object
Hits PanelApp API to return a list of genes for a gene panel from a given
R number
############################################################################'''

import pytest
import src.panelapp_requests as panelapp_requests

@pytest.fixture
def r_code():
    r_code = 'R134'
    return r_code

@pytest.fixture
def target():
    r_code = 'R134'
    target = panelapp_requests.MyRequests(r_code)
    return target

def test_request_data(target):
    response = target.request_data()
    assert response.status_code == 200

def test_print_info(capsys, r_code, target):
    response = target.request_data()
    target.print_info(response, r_code)
    captured = capsys.readouterr()
    assert captured.out == '\n\nClinical Indication: Familial hypercholesterolaemia (GMS)\nGenes included in the R134 panel: APOB APOE LDLR LDLRAP1 PCSK9 GCKR\n\n\n'