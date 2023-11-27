from src.logger import Logger

log = Logger(name='NGTD_APP', log_level='DEBUG', log_dir='logs/').get_logger()
td_url = "https://www.england.nhs.uk/publication/national-genomic-test-directories/"