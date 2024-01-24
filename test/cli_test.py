"""
Test Command Line Interface Object
Author: Niall Gallop
"""

import pytest
import src.command_line_interface as cli

# Broad, basic functional test of CommandLineInterface
def test_good_arg_selection():
    parser = cli.CommandLineInterface(["-g", "-r", "R134"])
    assert str(parser.args) == "Namespace(gene_list=True, create_bed=False, "\
                                "r_number='R134', download_directory=None)"

# Add error handling tests
def test_no_args():
    with pytest.raises(SystemExit) as err:
        parser = cli.CommandLineInterface([])
    err_message = "Error: Must select at least one of the following options: "\
                  "\"--gene_list\", \"--create_bed\", \"--download_directory\""
    assert str(err.value) == err_message


def test_r_flag_error():
    with pytest.raises(SystemExit) as err:
        parser = cli.CommandLineInterface(["-r", "R134"])
    err_message = "Error: If r_number given, at least one of the following "\
                  "options: \"--gene_list\", \"--create_bed\" must also be "\
                  "given."
    assert str(err.value) == err_message


def test_g_flag_error():
    with pytest.raises(SystemExit) as err:
        parser = cli.CommandLineInterface(["-g"])
    err_message = "If gene_list is selected, an R number must be given "\
                      "with flag -r"
    assert str(err.value) == err_message


def test_b_flag_error():
    with pytest.raises(SystemExit) as err:
        parser = cli.CommandLineInterface(["-b"])
    err_message = "If bed file creation selected, an R number must be"\
                      " passed with flag -r"
    assert str(err.value) == err_message
