import requests
import certifi
import ssl
import re
import os
import sys
from config import log
from urllib.request import urlopen
from config import td_url as url
from urllib.error import URLError

class get_directory:
        # Method to download National Test directory document            
    def download_doc(self, get_doc, output, url):
        if get_doc:
            # Specify the CA bundle path - to avoid SSL certificate verification failure
            cafile = certifi.where()
            context = ssl.create_default_context(cafile=cafile)

            # Open html page as text to be search through
            try:
                page = urlopen(url, context=context, timeout=10)
                html = page.read().decode("utf-8")

                try:
                    # Create regular expressions to find document version
                    pattern = ("The National genomic test directory.*rare "
                    "and inherited disorders.*</p>\n<p>Version.*</p>")
                    pattern_two = "<.*?>.*<.*?>"
                    match_results = re.search(pattern, html, re.IGNORECASE)
                    match_results_two = re.search(pattern_two, match_results[0], re.IGNORECASE)
                    doc_version = re.sub("^<.*?>|</.*?>", "", match_results_two[0])
                    doc_version = doc_version.split(" ") # remove unnecessary text
                    print(f"\nDownloaded Test Directory", doc_version[0], doc_version[1])
                except Exception as e:
                    print(f"Problem getting the document version number, check the regex: {e}")
                    log.error(e)
                    sys.exit(1)

                try:
                    # Create regex to download NGTD document
                    pattern_three = ("<a href=.*Rare-and-inherited-disease-"
                    "national-genomic-test-directory-version.*xlsx")
                    match_results_three = re.search(pattern_three, html, re.IGNORECASE)
                    doc_url = re.sub("<a href=\"", "", match_results_three[0])
                    doc_file = doc_url.split("/")
                    doc_request = requests.get(doc_url, allow_redirects = True)
                    if output:
                        output = os.path.realpath(output)
                        output = "".join([output,"/", doc_file[7]])
                        open(output, "wb").write(doc_request.content)
                        print("It can be found in:", output)
                    else:
                        open(doc_file[7], "wb").write(doc_request.content)
                        print("in current directory:", os.path.realpath("."))
                except Exception as e:
                    print(f"Problem getting the NGTD document URL from webpage, check the regex: {e}")
                    log.error(e)
                    sys.exit(1)

            except URLError as urlerr:
                print(f"Failed to open URL due to a broken URL check config file: {urlerr}")
                log.error(urlerr)
                sys.exit(1)
            except requests.exceptions.HTTPError as httperr:
                print(f"Failed to open URL due to an HTTP error: {httperr}")
                log.error(httperr)
                sys.exit(1)
            except requests.exceptions.Timeout as timeerr:
                print(f"Connection timed out: {timeerr}")
                log.error(timeerr)
                sys.exit(1)
            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred: {e}")
                log.error(e)
                sys.exit(1)
                