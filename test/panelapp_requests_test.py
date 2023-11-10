'''############################################################################
Test Panel App Request Object
Hits PanelApp API to return a list of genes for a gene panel from a given
R number
############################################################################'''

import pytest
import src.panelapp_requests as panelapp_requests

def test_request_data():
    r_code = 'R134'
    target = panelapp_requests.MyRequests(r_code)
    response = target.request_data()
    assert response.status_code == 200

def test_print_info():
    r_code = 'R134'
    target = panelapp_requests.MyRequests(r_code)
    response = target.request_data()
    