import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import date


class Logger:

    def __init__(self, name, log_level, log_dir='logs'):
        """Configures a daily logger
        Parameters
        __________
            name : str
                logger's name
            log_level : str
                logger severity configuration
            log_dir : str
                Directory where logs are stored
        """

        # Creates the logger
        self.logger = logging.getLogger(name)

        # Sets logger's severity threshold.
        self.logger.setLevel(log_level)

        # Sets log name 
        log_file_name = f"NGTD.log"

        # Creates a rotating log file that resets at midnight
        fh = TimedRotatingFileHandler(
            os.path.join(log_dir, log_file_name), 
            when='midnight', 
            interval=1
        )

        # Configures the log string format
        formatter = logging.Formatter(
            '%(name)-6s %(asctime)s %(levelname)-6s - %(message)s'
        )
        fh.setFormatter(formatter)

        # Adds the handler to the logger
        self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger