"""
Test BED file Creation
Author: Niall Gallop
"""

import pytest
import os
import src.create_beds as target

@pytest.fixture
def panel_info_dict():
    return {'r_number': 'R134', 'panel_id': 772, 'panel_version': '2.4', 
            'signoff_status': 'GMS signed-off', 
            'genes': ['APOB', 'APOE', 'LDLR', 'LDLRAP1', 'PCSK9', 'GCKR'], 
            'hgnc_id_list': ['HGNC:603', 'HGNC:613', 'HGNC:6547',
                             'HGNC:18640', 'HGNC:20001', 'HGNC:4196']}

@pytest.fixture
def ref_genome():
    return '38'

# Functional Test for overall object


# test __get_responses()
def test_init(panel_info_dict, ref_genome):
    test_object = target.RequestBedData(ref_genome, panel_info_dict)
    assert type(test_object.gene_dict) is dict
    assert bool(test_object.gene_dict)

# test create_bed_files()
def test_create_bed_files(panel_info_dict, ref_genome):
    test_object = target.RequestBedData(ref_genome, panel_info_dict)
    test_dir = "test_dir/"
    test_object.output_dir = test_dir
    os.mkdir(test_dir)
    bed_file = test_object.create_bed_file()
    assert os.path.isfile(bed_file)
    os.remove(bed_file)
    os.rmdir(test_dir)
    assert os.path.isdir(test_dir) == False