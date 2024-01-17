"""###########################################################################
Test Panel App Request Object
Hits PanelApp API to return a list of genes for a gene panel from a given
R number
###########################################################################"""

import pytest
import src.command_line_interface as cli
import src.panelapp_requests as panelapp_requests
from config import log

@pytest.fixture
def args():
    parser = cli.CommandLineInterface(["-g", "-r", "R134"])
    args = parser.args
    return args

@pytest.fixture
def bad_args():
    parser = cli.CommandLineInterface(["-g", "-r", "R428"])
    args = parser.args
    return args

def test_request_data(args):
    target = panelapp_requests.MyRequests(args)
    response = target.request_data()
    assert response.status_code == 200

def test_request_data_bad_r_code(bad_args):
    target = panelapp_requests.MyRequests(bad_args)
    with pytest.raises(SystemExit):
        target.request_data()
   
def test_gene_list(args):
    target = panelapp_requests.MyRequests(args)
    response = target.request_data()
    gene_list, signoff = target.gene_list(response)
    assert gene_list == ["APOB", "APOE", "LDLR", "LDLRAP1", "PCSK9", "GCKR"]
