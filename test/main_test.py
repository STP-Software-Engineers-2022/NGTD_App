"""###########################################################################
Test executable python file
###########################################################################"""

import pytest
import main as target

def test_main(monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest", "-g", "-r", "R134"])
    assert target.main()
    