"""
This module initializes and configures a logger for the NGTD_APP application.
It also stores the URL for downloading the Directory spreadsheet of tests

Attributes
----------
log : logging.Logger
    A logging.Logger instance configured for the NGTD_APP application.

Usage
-----
To log messages in different parts of the application, import the `log`
instance from this script and use its methods like `log.debug()`,
`log.info()`, `log.warning()`, `log.error()`, and `log.critical()`.

Example
-------
    from your_script_name import log
    log.info("This is an info message")
"""
from src.logger import Logger

log = Logger(name="NGTD_APP", log_level="DEBUG", log_dir="logs/").get_logger()
td_url = "https://www.england.nhs.uk/publication/national-genomic-test-"
"directories/"