import requests
import certifi
import ssl
import re
import os
from urllib.request import urlopen

class get_directory:
        # Method to download National Test directory document            
    def download_doc(self, get_doc, output):
        if get_doc:
            # Specify the CA bundle path - to acoid SSL certificate verification failure
            cafile = certifi.where()
            context = ssl.create_default_context(cafile=cafile)

            # Open html page as text to be search through
            url = "https://www.england.nhs.uk/publication/national-genomic-test-directories/"
            page = urlopen(url, context=context)
            html = page.read().decode("utf-8")

            # Create regular expressions to find document version
            version_pattern = ("The National genomic test directory.*rare "
            "and inherited disorders.*</p>\n<p>Version.*</p>")
            html_tag_pattern = "<.*?>.*<.*?>"
            match_version_results = re.search(version_pattern, html, re.IGNORECASE)
            match_html_tag_results = re.search(html_tag_pattern, match_version_results[0], re.IGNORECASE)
            doc_version = re.sub("^<.*?>|</.*?>", "", match_html_tag_results[0])
            doc_version = doc_version.split(" ") # remove unnecessary text
            print("Downloaded Test Directory", doc_version[0], doc_version[1])

            # Create regex to download NGTD document
            excel_download_pattern = ("<a href=.*Rare-and-inherited-disease-"
            "national-genomic-test-directory-version.*xlsx")
            match_results_three = re.search(excel_download_pattern, html, re.IGNORECASE)
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