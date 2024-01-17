"""
Test Command Line Interface Object
Author: Niall Gallop
"""

import pytest
import src.command_line_interface as cli

# Broad, basic functional test of CommandLineInterface
def test_cli():
    parser = cli.CommandLineInterface(["-g", "-r", "R134"])
    assert parser.args.r_number == "R134"

# Add error handling tests
