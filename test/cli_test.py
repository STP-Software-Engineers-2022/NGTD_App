"""###########################################################################
Test Command Line Interface Object
###########################################################################"""

import pytest
import src.command_line_interface as cli

def test_cli():
    parser = cli.CommandLineInterface(["-g", "-r", "R134"])
    assert parser.args.r_number == "R134"