import os
import sys
import pytest
from unittest.mock import patch
from urllib.error import URLError
import src.get_directory as get_directory
from config import td_url as url

@pytest.fixture
def directory_instance():
    """
    Fixture for creating an instance of the 'get_directory' class.
    """
    return get_directory.get_directory()

@pytest.fixture
def test_url():
    """
    Fixture for providing a test URL 'https://www.england.nhs.uk/publication/national-genomic-test-directories/'.
    """
    return 'https://www.england.nhs.uk/publication/national-genomic-test-directories/'

@pytest.fixture
def tmp_output():
    """
    Fixture for providing a temporary output path for downloaded files.
    """
    return os.path.join('Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx')

@pytest.fixture
def current_dir():
    """
    Fixture for providing the current working directory path.
    """
    return os.path.join(os.getcwd())


def test_regex_matching(directory_instance, capsys, tmp_path):
    """
    Test regex matching by providing HTML content that matches the expected pattern.
    """
    # Test regex matching by providing HTML content that matches the expected pattern
    html_content = "The National genomic test directory...Version 1.0...</p>\n<p>Some text..."
    with pytest.raises(SystemExit):
        with patch('builtins.print'):
            directory_instance.download_doc(True, None, html_content)

def test_failure_cases(directory_instance, capsys):
    """
    Test failure cases by simulating a URL error during the download.
    """
    with patch('urllib.request.urlopen', side_effect=URLError('https://www.england.nhs.uk/publication/national-genomic-test-directories/')):
        with pytest.raises(SystemExit):
            with patch('builtins.print'):
                directory_instance.download_doc(True, None, 'https://www.england.nhs.uk/publication/')

def test_successful_download_default_output(directory_instance, capsys, tmp_output, test_url):
    """
    Test successful download with default output.
    """
    # Test successful download with default output
    with patch('builtins.print'):
        directory_instance.download_doc(True, None, test_url)
    assert os.path.exists(tmp_output)

def test_successful_download_specified_output(directory_instance, capsys, test_url, current_dir, tmp_output):
    """
    Test successful download with specified output.
    """
    # Test successful download with specified output
    tmp_output_path = os.path.join(current_dir, tmp_output)
    with patch('builtins.print'):
        directory_instance.download_doc(True, current_dir, test_url)
    assert os.path.exists(tmp_output_path)

def test_edge_cases(directory_instance, capsys, test_url):
    """
    Test edge cases, such as providing no URL and setting get_doc to False.
    """
    # Test edge cases, such as providing no URL and setting get_doc to False
    with pytest.raises(SystemExit):
        with patch('builtins.print'):
            directory_instance.download_doc(False, None, test_url)

    with pytest.raises(SystemExit):
        with patch('builtins.print'):
            directory_instance.download_doc(True, None, '')

# Add more test cases as needed
