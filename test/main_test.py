'''############################################################################
Test executable python file
############################################################################'''

import pytest
import main as target

#test = True

def test_main():
    assert target.main() == True