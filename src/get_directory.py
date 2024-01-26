"""
This module downloads the National Genomic Test Excel spreadsheet.

Example:
    ngtd_dir = get_directory(args)
    ngtd_dir.download_doc()

Author: D. Ajayi
Last Updated: Niall Gallop 24-Jan-2024
"""
import requests
import certifi
import ssl
import re
import os
from config import log
from urllib.request import urlopen
from urllib.error import URLError


class GetDirectory:
    """
    The get_directory class handles the downloading of the National 
    Genomic Test Directory spreadsheet.

    And downloads the latest version of the National Genomic Test 
    Directory document from the NHS website, taking care of URL processing, 
    SSL context for secure connections, and file download management.

    Attributes
    ----------
    output : str
        The path to the directory where the downloaded document will be saved.

    Methods
    -------
    download_doc()
        Downloads the National Genomic Test Directory document from the NHS
        website and saves it to the specified directory.
    """
    def __init__(self, args):
        self.output = args.download_directory
          
    def download_doc(self):
        """
        This method downloads the National Test directory document from a 
        specified URL.
        The method also sets up SSL context for secure download and handles
        the file writing process.

        Notes
        -----
        - The method prints the version of the downloaded document.
        - And the download location is printed after the file is saved.
        """

        output = self.output
        # Specify the CA bundle path - to avoid SSL certificate verification 
        # failure
        cafile = certifi.where()
        context = ssl.create_default_context(cafile=cafile)

        # Open html page as text to be search through
        try:
            url = "https://www.england.nhs.uk/publication/national-"\
                "genomic-test-directories/"
            page = urlopen(url, context=context)
            html = page.read().decode("utf-8")
            log.debug("-d: opened url")
        except URLError as urlerr:
            print(f"-d: Failed to open URL: {urlerr.reason}")
            log.error(urlerr.args[0])
            return False

        # Create regular expressions to find document version
        version_pattern = ("The National genomic test directory.*rare "
        "and inherited disorders.*</p>\n<p>Version.*</p>")
        html_tag_pattern = "<.*?>.*<.*?>"
        match_version_results = re.search(version_pattern, html, 
                                re.IGNORECASE)
        
        if match_version_results is None:
            msg = "Version pattern not found in the HTML code."
            print(msg)
            log.warning(msg)
            return False
        
        else:
            match_html_tag_results = re.search(html_tag_pattern, 
                                    match_version_results[0], re.IGNORECASE)
            doc_version = re.sub(
                "^<.*?>|</.*?>", "", match_html_tag_results[0])

            doc_version = doc_version.split(" ") # remove unnecessary text
            log.debug("-d: found document version")
            print("Downloading Test Directory:", doc_version[0], 
                  doc_version[1])


        # Create regex to download NGTD document
        excel_download_pattern = ("<a href=.*Rare-and-inherited-disease-"\
        "national-genomic-test-directory-version.*xlsx")
        match_download_pattern = re.search(excel_download_pattern, html, 
                                re.IGNORECASE)
        
        if match_download_pattern is None:
            msg = "Directory download link not seen in HTML code"
            print(msg)
            log.warning(msg)
            return False
        else:
            doc_url = re.sub("<a href=\"", "", match_download_pattern[0])

            doc_file = doc_url.split("/")
            try:
                doc_request = requests.get(doc_url, allow_redirects = True)
                if output:
                    output = os.path.realpath(output)
                    output = "".join([output,"/", doc_file[7]])
                    open(output, "wb").write(doc_request.content)
                    print("It can be found in:", output)
                    log.debug("NGTD downloaded successfully")
                else:
                    open(doc_file[7], "wb").write(doc_request.content)
                    print("in current directory:", os.path.realpath("."))
                    log.debug("NGTD downloaded successfully")
            except requests.exceptions.RequestException as reqerr:
                log.error(reqerr.args[0])
                print(f"Error downloading the file: {reqerr}")
                return False
        
        return True
            