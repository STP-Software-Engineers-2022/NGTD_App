"""Test get_directory functions
Author: D. Ajayi
Last Updated: Niall Gallop 24-Jan-2024
"""
import pytest
from unittest.mock import patch, MagicMock
import src.get_directory as get_directory

class ArgsMock:
    def __init__(self, download_directory):
        self.download_directory = download_directory

@pytest.fixture
def directory_instance(tmp_path):
    """
    Fixture for creating an instance of the 'get_directory' class with a 
    temporary download directory.
    """
    args_mock = ArgsMock(download_directory=str(tmp_path))
    return get_directory.GetDirectory(args_mock)

# ... other fixtures ...

def test_successful_download(directory_instance, tmp_path):
    """
    Test successful download of the document.
    """
    # Assuming the download_doc method in get_directory class does not require
    # additional arguments
    with patch('src.get_directory.urlopen') as mock_urlopen:
        mock_response = MagicMock()
    mock_html = (
            "<html>\n"
            "<body>\n"
            "<p>The National genomic test directory for rare and inherited"
            "disorders</p>\n"
            "<p>Version 5.1</p>\n"
            "<a href=\"https://example.com/Rare-and-inherited-disease-"
            "national-genomic-test-directory-version-5.1.xlsx\">Download"
            "</a>\n"
            "</body>\n"
            "</html>"
                )
    mock_response.read.return_value = mock_html
    mock_urlopen.return_value = mock_response
        
    print("Mocked HTML content:", mock_html) 


    directory_instance.download_doc()
    files = list(tmp_path.glob("*national-genomic-test-directory-"
                               "version*.xlsx"))

    assert len(files) > 0

def test_unsuccessful_download_missing_link(directory_instance, tmp_path):
    """
    Test unsuccessful download due to missing download link in HTML content.
    """
    mock_html = "<html><body><p>Some content without download link</p></body"
    "</html>"
    
    with patch('src.get_directory.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = mock_html.encode()
        mock_urlopen.return_value = mock_response
        
        directory_instance.download_doc()

        files = list(tmp_path.glob("*national-genomic-test-directory-version*."
                                   "xlsx"))
        assert len(files) == 0