'''############################################################################
Test Command Line Interface Object
############################################################################'''

import pytest
import src.cli as cli

def test_cli():
    parser = cli.cli_obj(['-r', 'R134'])
    assert parser.args.r_number == 'R134'