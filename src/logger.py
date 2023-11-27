import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import date


class Logger:

    def __init__(self, name, log_level, prefix='da-', log_dir='logs'):
        """
        Configures a daily logger
        :param name: logger's name
        :param log_level: logger severity configuration
        :param prefix: a prefix that will be added to the log file
        """

        # 1. Creates a logger using Python's logging facility.
        self.logger = logging.getLogger(name)

        # 2. Sets logger's severity threshold.
        self.logger.setLevel(log_level)

        # 3. Creates log name from prefix and suffix using today's date
        log_file_name = f"{prefix}{date.today()}.log"

        # 4. Creates a daily log file and stores it at log_dir
        # prepending a prefix.
        fh = TimedRotatingFileHandler(
            os.path.join(log_dir, log_file_name), 
            when='midnight', 
            interval=1
        )

        # 5. Configures the log string format
        formatter = logging.Formatter(
            '%(name)-6s %(asctime)s %(levelname)-6s '
            'thread:%(thread)-8d - %(message)s'
        )
        fh.setFormatter(formatter)

        # Adds the handler to the logger
        self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger