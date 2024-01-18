"""
Top to bottom functional tests, running from main script
Author: Niall Gallop
"""

import os
import shutil
import main as target
import src.get_directory as getdir

"""
Test use cases:
    1. Return Gene List from an R number to plug into pipeline
    2. Maintain a repository of gene panels, R numbers and bed files
    3. Download the latest version of the National Genomic Test Directory

N.B. misuse not tested here, wrong arguments handled by CommandLineInterface 
and are therefore tested there.
"""
# Use case 1
def test_gene_list(monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest", "-g", "-r", "R134"])
    assert target.main()

# Use case 2
def test_bed_file(monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest", "-b", "-r", "R134"])
    monkeypatch.setattr("builtins.input", lambda _: "38")
    assert target.main()

# Use case 3
def test_download_ngtd(monkeypatch):
    try:
        test_dir = "test_dir/"
        os.mkdir(test_dir)
        monkeypatch.setattr("sys.argv", ["pytest", "-d", test_dir])
        assert target.main()
    finally:
        shutil.rmtree(test_dir)
