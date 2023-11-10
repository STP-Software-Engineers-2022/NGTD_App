'''############################################################################
Test executable python file
############################################################################'''

import pytest
'''
import importlib as imp

target = imp.load_source('main', 'main.py')
'''
import main as target

def test_main():
    assert target.main() == True